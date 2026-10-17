"""Allowlisted, local statistics. No formulas, generated code, providers or network."""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid

ENGINE_VERSION = 1
METHODS = ('exploratory', 'pearson', 'spearman', 'paired_t', 'independent_t', 'chi_square', 'ols', 'logistic')
MAX_OUTPUT = 1024 * 1024
TIMEOUT = 30


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def parameters(table, supplied):
    if not isinstance(supplied, dict) or set(supplied) - {'method', 'columns', 'confidence', 'equal_var'}:
        raise ValueError('Unsupported analysis parameters.')
    method = supplied.get('method')
    columns = supplied.get('columns')
    if method not in METHODS:
        raise ValueError('Select an allowlisted analysis method.')
    if not isinstance(columns, list) or not 1 <= len(columns) <= 20 or any(not isinstance(c, str) or c not in table['columns'] for c in columns) or len(set(columns)) != len(columns):
        raise ValueError('Select 1–20 unique existing columns.')
    if method in ('pearson', 'spearman', 'paired_t', 'independent_t', 'chi_square') and len(columns) != 2:
        raise ValueError('This method requires exactly two columns.')
    if method in ('ols', 'logistic') and not 2 <= len(columns) <= 11:
        raise ValueError('Regression requires an outcome followed by 1–10 numeric predictors.')
    confidence = supplied.get('confidence', .95)
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not .80 <= confidence <= .99:
        raise ValueError('Confidence must be between 0.80 and 0.99.')
    equal = supplied.get('equal_var', False)
    if not isinstance(equal, bool) or ('equal_var' in supplied and method != 'independent_t'):
        raise ValueError('Equal variance is a boolean option for independent t-tests only.')
    result = dict(method=method, columns=columns, confidence=float(confidence))
    if method == 'independent_t':
        result['equal_var'] = equal
    return result


def execute(registry, dataset_id, supplied, *, preview=False):
    record, table = registry.inspect(dataset_id)
    params = parameters(table, supplied)
    payload = encode(dict(table=table, parameters=params, preview=preview)).encode()
    with tempfile.TemporaryFile() as output:
        process = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--worker'], stdin=subprocess.PIPE, stdout=output, stderr=subprocess.DEVNULL,
            env={**{k:v for k,v in os.environ.items() if k in ('PATH','SYSTEMROOT','WINDIR','TMPDIR','LANG','LC_ALL')}, 'OPENBLAS_NUM_THREADS':'1', 'OMP_NUM_THREADS':'1', 'MKL_NUM_THREADS':'1'})
        try:
            process.communicate(payload, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            raise ValueError('Analysis exceeded 30 seconds; reduce rows or predictors.') from None
        output.seek(0)
        raw = output.read(MAX_OUTPUT + 1)
    if process.returncode or len(raw) > MAX_OUTPUT:
        raise ValueError(f'Analysis exceeded a resource limit or failed (worker exit {process.returncode}); simplify the analysis.')
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeError):
        raise ValueError('Analysis worker failed to return valid results.') from None
    if 'error' in result:
        raise ValueError(result['error'])
    if preview:
        return result
    from dataset_registry import now
    manifest = dict(id=uuid.uuid4().hex, timestamp=now(), engine_version=ENGINE_VERSION,
        dataset=dict(id=record['id'], version=record['version'], sha256=record['sha256'], filename=record['filename'], origin=record['origin'], import_options=record['options']),
        parameters=params, **result)
    manifest['output_hash'] = digest(manifest)
    save(registry, manifest)
    return manifest


def initialize(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS analysis_runs (
      id TEXT PRIMARY KEY, dataset_id TEXT NOT NULL REFERENCES datasets(id),
      created TEXT NOT NULL, manifest TEXT NOT NULL CHECK(length(manifest)<=1048576));
    CREATE TRIGGER IF NOT EXISTS analysis_no_update BEFORE UPDATE ON analysis_runs
      BEGIN SELECT RAISE(ABORT,'Analysis runs are immutable'); END;
    CREATE TRIGGER IF NOT EXISTS analysis_no_delete BEFORE DELETE ON analysis_runs
      BEGIN SELECT RAISE(ABORT,'Analysis runs are immutable'); END;
    ''')


def save(registry, manifest):
    content = encode(manifest)
    if len(content.encode()) > MAX_OUTPUT:
        raise ValueError('Analysis manifest exceeds 1 MiB.')
    with registry.connection() as db:
        initialize(db)
        db.execute('INSERT INTO analysis_runs VALUES (?,?,?,?)', (manifest['id'], manifest['dataset']['id'], manifest['timestamp'], content))


def history(registry, dataset_id, page=0):
    if type(page) is not int or page < 0:
        raise ValueError('History page must be a nonnegative integer.')
    with registry.connection() as db:
        initialize(db)
        rows = db.execute('SELECT manifest FROM analysis_runs WHERE dataset_id=? ORDER BY created DESC,id LIMIT 20 OFFSET ?', (dataset_id, page*20)).fetchall()
    results = [json.loads(r[0]) for r in rows]
    for manifest in results:
        check = dict(manifest)
        saved = check.pop('output_hash')
        if digest(check) != saved:
            raise ValueError('Saved analysis integrity check failed. Restore from a local backup.')
    return results


def export_csv(manifest):
    """Long-form spreadsheet-safe results; raw rows are never exported."""
    import csv
    import io
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(['path', 'value'])
    def walk(value, path):
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, path + '/' + str(k))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, path + '/' + str(i))
        else:
            def safe(v):
                s = str(v) if v is not None else ''
                return "'" + s if s.lstrip().startswith(('=', '+', '-', '@')) or any(c in s for c in '\t\r\n') else s
            writer.writerow([safe(path), safe(value)])
    walk(manifest, '')
    return out.getvalue()


def calculate(table, params, preview=False):
    method = params['method']
    columns = params['columns']
    selected = [table['columns'].index(c) for c in columns]
    rows = table['rows']
    if len(rows) > 20000 or len(rows)*len(table['columns']) > 100000:
        raise ValueError('Analysis exceeds dataset resource limits.')
    categorical = set(range(2)) if method == 'chi_square' else ({1} if method == 'independent_t' else set())
    converted, reasons = [], dict(missing=0, invalid_numeric=0)
    missing = {c: 0 for c in columns}
    invalid = {c: 0 for c in columns}
    for row in rows:
        values, absent, bad = [], False, False
        for j, index in enumerate(selected):
            value = row[index]
            if value is None:
                absent = True
                missing[columns[j]] += 1
                values.append(None)
            elif j in categorical:
                values.append(type(value).__name__ + ':' + str(value))
            else:
                try:
                    number = float(value)
                    if isinstance(value, bool) or not math.isfinite(number) or abs(number) > 1e100:
                        raise ValueError()
                    values.append(number)
                except (TypeError, ValueError, OverflowError):
                    bad = True
                    invalid[columns[j]] += 1
                    values.append(None)
        if absent:
            reasons['missing'] += 1
        elif bad:
            reasons['invalid_numeric'] += 1
        else:
            converted.append(values)
    n = len(converted)
    counts = dict(total=len(rows), used=n, excluded=len(rows)-n, exclusion_reasons=reasons, missing_by_column=missing, invalid_numeric_by_column=invalid,
        rule='Listwise complete finite numeric cases across selected columns; blanks/nulls missing; booleans and literal NA/NaN invalid numeric; categorical values retain typed labels. Missing takes precedence in row exclusion counts.')
    if preview:
        return dict(observations=counts, parameters=params)
    import warnings
    import platform
    import importlib.metadata
    import numpy as np
    import scipy
    from scipy import stats
    import statsmodels
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_breuschpagan
    from statsmodels.stats.stattools import durbin_watson
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    if n < 3:
        raise ValueError('At least three complete observations are required.')
    caveats = ['Associations do not establish causation. Independence and representative sampling require study-design review.', 'P-values and confidence intervals are unadjusted for multiple testing.']
    if n < 30:
        caveats.append('Low sample size: estimates and assumption tests may be unreliable.')
    diagnostics, charts = {}, []
    confidence = params['confidence']
    alpha = 1-confidence
    def normal(values):
        if len(values) < 3 or np.ptp(values) == 0:
            return dict(test='Shapiro-Wilk', available=False, reason='Requires three nonconstant observations.')
        v = np.asarray(values)[:5000]
        w, p = stats.shapiro(v)
        if p < .05:
            caveats.append('Normality check p < 0.05; review distribution and method assumptions.')
        return dict(test='Shapiro-Wilk', statistic=float(w), p_value=float(p), observations=len(v), capped_at=5000)
    def hist(values, label):
        freq, edges = np.histogram(values, bins=min(20, max(3, int(np.sqrt(len(values))))))
        charts.append(dict(kind='histogram', label=label, data=[dict(bin=float((edges[i]+edges[i+1])/2), count=int(v)) for i,v in enumerate(freq)]))
    def scalar(v):
        return float(v)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        if method == 'chi_square':
            levels = [sorted({r[j] for r in converted}) for j in range(2)]
            if any(not 2 <= len(v) <= 20 for v in levels) or len(levels[0])*len(levels[1]) > 100:
                raise ValueError('Chi-square requires 2–20 levels per variable and at most 100 cells.')
            observed = np.zeros((len(levels[0]), len(levels[1])), dtype=int)
            for a,b in converted:
                observed[levels[0].index(a), levels[1].index(b)] += 1
            statistic, p, df, expected = stats.chi2_contingency(observed, correction=False)
            sparse = int((expected < 5).sum())
            if sparse:
                caveats.append('Expected counts below 5: chi-square approximation may be unreliable; collect more data or choose an exact method outside v1.')
            result = dict(statistic=scalar(statistic), p_value=scalar(p), df=int(df), cramers_v=scalar(np.sqrt(statistic/(n*min(observed.shape[0]-1, observed.shape[1]-1)))), observed=observed.tolist(), expected=expected.tolist(), levels=levels, correction=False)
            diagnostics['expected_cells_below_5'] = sparse
            charts.append(dict(kind='contingency', label='Observed counts', data=[dict(group=levels[0][i]+' / '+levels[1][j], count=int(observed[i,j])) for i in range(len(levels[0])) for j in range(len(levels[1]))]))
        elif method == 'independent_t':
            levels = sorted({r[1] for r in converted})
            if len(levels) != 2:
                raise ValueError('Independent t-test requires exactly two groups.')
            a,b = [np.array([r[0] for r in converted if r[1] == level]) for level in levels]
            if min(len(a),len(b)) < 2 or min(np.var(a,ddof=1),np.var(b,ddof=1)) <= 0:
                raise ValueError('Each group requires at least two observations and positive variance.')
            test = stats.ttest_ind(a,b,equal_var=params['equal_var'])
            ci = test.confidence_interval(confidence)
            pooled = np.sqrt(((len(a)-1)*np.var(a,ddof=1)+(len(b)-1)*np.var(b,ddof=1))/(n-2))
            result = dict(statistic=scalar(test.statistic), p_value=scalar(test.pvalue), df=scalar(test.df), mean_difference=scalar(a.mean()-b.mean()), confidence_interval=list(map(float,ci)), cohens_d=scalar((a.mean()-b.mean())/pooled), groups=levels, group_sizes=[len(a),len(b)], group_means=[float(a.mean()),float(b.mean())], effect_definition='Cohen d: first minus second group / pooled sample SD')
            lev = stats.levene(a,b,center='median')
            diagnostics['group_normality'] = [normal(a), normal(b)]
            if np.isfinite(lev.statistic) and np.isfinite(lev.pvalue):
                diagnostics['levene'] = dict(statistic=scalar(lev.statistic), p_value=scalar(lev.pvalue))
            else:
                diagnostics['levene'] = dict(available=False, reason='Absolute group deviations have no usable variance.')
                caveats.append('Levene variance check is undefined for these group deviations; review equal-variance assumptions manually.')
            if lev.pvalue < .05:
                caveats.append('Unequal group variances detected; Welch is preferred to pooled t-test.')
            if min(len(a), len(b)) < 30:
                caveats.append('Small independent groups: normality and variance estimates may be unreliable.')
            hist(a,levels[0])
            hist(b,levels[1])
        else:
            data = np.asarray(converted, dtype=float)
            for j,c in enumerate(columns):
                if np.ptp(data[:,j]) == 0:
                    raise ValueError('Selected numeric columns must have positive variance.')
            if method == 'exploratory':
                result = {}
                for j,c in enumerate(columns):
                    x = data[:,j]
                    ci = stats.t.interval(confidence, n-1, loc=x.mean(), scale=stats.sem(x))
                    result[c] = dict(n=n,mean=scalar(x.mean()),median=scalar(np.median(x)),sd=scalar(x.std(ddof=1)),min=scalar(x.min()),max=scalar(x.max()),q25=scalar(np.quantile(x,.25)),q75=scalar(np.quantile(x,.75)),mean_confidence_interval=list(map(float,ci)),skewness=scalar(stats.skew(x,bias=False)))
                    diagnostics[c] = normal(x)
                    hist(x,c)
            elif method in ('pearson','spearman'):
                x,y = data.T
                test = stats.pearsonr(x,y) if method == 'pearson' else stats.spearmanr(x,y)
                r,p = map(float,test)
                if method == 'pearson':
                    ci = list(map(float,test.confidence_interval(confidence)))
                    ci_method = 'SciPy Fisher transform'
                elif n > 3:
                    z = np.arctanh(np.clip(r,-1+1e-15,1-1e-15))
                    width = stats.norm.ppf(1-alpha/2)/np.sqrt(n-3)
                    ci = np.tanh([z-width,z+width]).tolist()
                    ci_method = 'Approximate Fisher transform of rank correlation'
                else:
                    ci,ci_method = None,'Unavailable with three observations'
                result = dict(correlation=r,p_value=p,confidence_interval=ci,ci_method=ci_method,effect_size=r)
                diagnostics.update(normality=[normal(x),normal(y)])
                if method == 'spearman':
                    caveats.append('Spearman p-values use an asymptotic approximation; small-sample inference and approximate rank-correlation CIs require caution.')
                caveats.append('Review linearity for Pearson or monotonicity for Spearman and outliers in the scatter plot.')
                charts.append(dict(kind='scatter',label='First 200 complete observations',data=[dict(x=float(a),y=float(b)) for a,b in data[:200]]))
            elif method == 'paired_t':
                diff = data[:,0]-data[:,1]
                if np.std(diff,ddof=1) == 0:
                    raise ValueError('Paired differences must have positive variance.')
                test = stats.ttest_rel(data[:,0], data[:,1])
                result = dict(statistic=scalar(test.statistic),p_value=scalar(test.pvalue),df=scalar(test.df),mean_difference=scalar(diff.mean()),confidence_interval=list(map(float,test.confidence_interval(confidence))),cohens_dz=scalar(diff.mean()/diff.std(ddof=1)),effect_definition='Paired Cohen dz: mean difference / sample SD of differences')
                diagnostics['difference_normality'] = normal(diff)
                caveats.append('Rows must represent matched pairs; pairing cannot be inferred from values.')
                hist(diff,'Paired differences')
            else:
                y = data[:,0]
                X = sm.add_constant(data[:,1:],has_constant='add')
                if n <= X.shape[1]+1:
                    raise ValueError('Regression requires more observations than coefficients plus one.')
                if np.linalg.matrix_rank(X) < X.shape[1]:
                    raise ValueError('Singular design matrix: remove redundant predictors.')
                condition = float(np.linalg.cond(X))
                vif = [float(variance_inflation_factor(X,j)) for j in range(1,X.shape[1])]
                diagnostics.update(condition_number=condition,variance_inflation_factors=dict(zip(columns[1:],vif)))
                if condition > 1000 or max(vif) > 5:
                    caveats.append('Multicollinearity or poor scaling detected; coefficients may be unstable.')
                if method == 'logistic':
                    if set(y) != {0.,1.}:
                        raise ValueError('Binary logistic outcome must contain exactly numeric 0 and 1; event is 1.')
                    if min((y==0).sum(),(y==1).sum()) < 10*X.shape[1]:
                        caveats.append('Few events/non-events per coefficient: logistic estimates may be unstable.')
                    try:
                        fitted = sm.Logit(y,X).fit(disp=False,maxiter=100)
                    except Exception:
                        raise ValueError('Logistic fit failed: singularity or perfect separation. Review predictors and outcome.') from None
                    if not fitted.mle_retvals['converged']:
                        raise ValueError('Logistic fit did not converge; possible separation or unstable predictors.')
                    if any('separation' in str(w.message).lower() for w in captured) or np.max(np.abs(fitted.params)) > 30:
                        raise ValueError('Perfect/quasi separation or extreme logistic coefficients; rescale and review predictors.')
                    prediction = fitted.predict()
                    result = dict(log_likelihood=float(fitted.llf),null_log_likelihood=float(fitted.llnull),pseudo_r_squared=float(fitted.prsquared),likelihood_ratio_p_value=float(fitted.llr_pvalue),aic=float(fitted.aic),bic=float(fitted.bic),event=1)
                    diagnostics.update(converged=True,iterations=int(fitted.mle_retvals['iterations']),brier_score=float(np.mean((prediction-y)**2)),accuracy_at_half=float(np.mean((prediction>=.5)==y)))
                    charts.append(dict(kind='scatter',label='Predicted probability vs observed (first 200)',data=[dict(x=float(p),y=float(v)) for p,v in zip(prediction[:200],y[:200])]))
                    caveats.append('Logistic diagnostics are in-sample; accuracy does not establish predictive validity. Review logit linearity and calibration.')
                else:
                    fitted = sm.OLS(y,X).fit()
                    resid = fitted.resid
                    if np.std(resid) < np.finfo(float).eps*max(1,np.std(y))*10:
                        raise ValueError('Perfect OLS fit: residual variance is insufficient for reliable inference.')
                    bp = het_breuschpagan(resid,X)
                    diagnostics.update(residual_normality=normal(resid),breusch_pagan=dict(statistic=float(bp[0]),p_value=float(bp[1])),durbin_watson=float(durbin_watson(resid)),max_cooks_distance=float(np.max(fitted.get_influence().cooks_distance[0])))
                    if bp[1] < .05:
                        caveats.append('Heteroskedasticity detected; conventional OLS standard errors may be unreliable.')
                    result = dict(r_squared=float(fitted.rsquared),adjusted_r_squared=float(fitted.rsquared_adj),f_statistic=float(fitted.fvalue),f_p_value=float(fitted.f_pvalue),aic=float(fitted.aic),bic=float(fitted.bic),residual_df=float(fitted.df_resid),rmse=float(np.sqrt(fitted.mse_resid)))
                    charts.append(dict(kind='scatter',label='Fitted vs residual (first 200)',data=[dict(x=float(p),y=float(v)) for p,v in zip(fitted.fittedvalues[:200],resid[:200])]))
                    ordered = np.sort(resid)
                    positions = np.linspace(0,n-1,min(n,200)).astype(int)
                    charts.append(dict(kind='scatter',label='Residual normal Q-Q',data=[dict(x=float(stats.norm.ppf((i+.5)/n)),y=float(ordered[i])) for i in positions]))
                    caveats.append('Review residual plots for linearity, constant variance, independence and influential observations.')
                intervals = fitted.conf_int(alpha=alpha)
                result['coefficients'] = []
                for i,name in enumerate(['Intercept',*columns[1:]]):
                    item = dict(term=name,estimate=float(fitted.params[i]),standard_error=float(fitted.bse[i]),statistic=float(fitted.tvalues[i]),p_value=float(fitted.pvalues[i]),confidence_interval=intervals[i].tolist())
                    if method == 'logistic':
                        item.update(odds_ratio=float(np.exp(fitted.params[i])),odds_ratio_confidence_interval=np.exp(intervals[i]).tolist())
                    result['coefficients'].append(item)
        if captured:
            caveats.append('Numerical library warnings occurred; review diagnostics before interpreting results.')
    output = dict(observations=counts,results=result,diagnostics=diagnostics,caveats=list(dict.fromkeys(caveats)),charts=charts,
        software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,statsmodels=statsmodels.__version__,engine=ENGINE_VERSION,**{name: importlib.metadata.version(name) for name in ('pyarrow','openpyxl')}),
        conventions=dict(confidence=confidence,alternative='two-sided',intercept=True if method in ('ols','logistic') else None,standard_errors='conventional',quantiles='linear',randomness='none'))
    try:
        encode(output)
    except ValueError:
        raise ValueError('Nonfinite numerical results: rescale data or review degenerate inputs.') from None
    return output


def worker():
    # Input is a bounded parser table. Cap worker CPU, address space and output too.
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU,(25,25))
        resource.setrlimit(resource.RLIMIT_FSIZE,(MAX_OUTPUT,MAX_OUTPUT))
        if sys.platform.startswith('linux'):
            resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
        raw = sys.stdin.buffer.read(16*1024*1024+1)
        if len(raw) > 16*1024*1024:
            raise ValueError('Analysis input exceeds resource limit.')
        payload = json.loads(raw)
        params = parameters(payload['table'],payload['parameters'])
        result = calculate(payload['table'],params,payload['preview'])
    except ValueError as exc:
        result = dict(error=str(exc))
    except Exception:
        result = dict(error='Numerical analysis failed. Review inputs, scaling and method assumptions.')
    encoded = encode(result)
    if len(encoded) > MAX_OUTPUT:
        encoded = encode(dict(error='Analysis output exceeds 1 MiB.'))
    sys.stdout.write(encoded)


if __name__ == '__main__':
    worker()
