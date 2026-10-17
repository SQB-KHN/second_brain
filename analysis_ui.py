"""Analyse registered immutable versions without accessing AI workflows."""
import json
import streamlit as st
import config
from dataset_registry import Registry
import statistical_engine as engine

LABELS = dict(exploratory='Exploratory statistics', pearson='Pearson correlation', spearman='Spearman correlation', paired_t='Paired t-test', independent_t='Independent t-test', chi_square='Chi-square test', ols='OLS regression', logistic='Binary logistic regression')


def show(manifest):
    st.caption(f"Run {manifest['id']} · {manifest['timestamp']} · SHA-256 {manifest['output_hash']}")
    counts = manifest['observations']
    a,b,c = st.columns(3)
    a.metric('Observations used',counts['used'])
    b.metric('Observations excluded',counts['excluded'])
    c.metric('Total observations',counts['total'])
    for caveat in manifest['caveats']:
        st.warning(caveat)
    st.subheader('Results')
    st.json(manifest['results'])
    st.subheader('Diagnostics and exclusions')
    st.json(dict(diagnostics=manifest['diagnostics'],observations=counts))
    st.subheader('Charts')
    for chart in manifest['charts']:
        st.text(chart['label'])
        if chart['kind'] == 'scatter':
            st.scatter_chart(chart['data'],x='x',y='y')
        elif chart['kind'] == 'histogram':
            st.bar_chart(chart['data'],x='bin',y='count')
        else:
            st.bar_chart(chart['data'],x='group',y='count')
    with st.expander('Reproducible run manifest'):
        st.json(manifest)
    st.download_button('Download analysis JSON',json.dumps(manifest,indent=2,allow_nan=False),file_name='analysis-'+manifest['id']+'.json',mime='application/json')
    st.download_button('Download analysis CSV',engine.export_csv(manifest),file_name='analysis-'+manifest['id']+'.csv',mime='text/csv')


def render():
    if config.DEPLOY_MODE:
        st.info('Analyse is disabled in the read-only demo. Private datasets and runs are not accessed.')
        return
    st.caption('Local SciPy and statsmodels · immutable dataset versions · reproducible analyses. No AI calls or dataset transfers.')
    st.caption('Limits: 20 variables, 10 regression predictors, 20,000 rows, 100,000 cells, 30 seconds/run and 1 MiB/manifest. Scatter charts show at most 200 observations; normality checks use at most the first 5,000.')
    try:
        registry = Registry()
        query = st.text_input('Find dataset version', key='analyse_query')
        total = registry.inventory_count(query)
        page = st.number_input('Dataset version page', min_value=1, max_value=max(1,(total+99)//100), value=1)
        records = registry.inventory(query, page=int(page)-1)
        if not records:
            st.info('Register a dataset in Datasets to begin analysis.')
            return
        ids = [r['id'] for r in records]
        preferred = st.session_state.get('analyse_dataset')
        selected = st.selectbox('Analysis dataset version', ids, index=ids.index(preferred) if preferred in ids else 0,
            format_func=lambda identity: next(f"{r['name']} · v{r['version']} · {r['filename']}" for r in records if r['id']==identity))
        record, table = registry.inspect(selected)
        st.text(f"Source: {record['filename']} · version {record['version']} · SHA-256: {record['sha256']}")
        method = st.selectbox('Analysis method',engine.METHODS,format_func=LABELS.get)
        st.caption('Select columns in order. Regression: outcome first, then numeric predictors. Independent t-test: numeric measurement first, group second. Paired t-test: first minus second; each row is a pair. Logistic event is numeric 1, reference is 0.')
        columns = st.multiselect('Analysis variables (ordered)',table['columns'],default=table['columns'][:2],key='analysis_columns_'+selected)
        confidence = st.selectbox('Confidence level',[.90,.95,.99],index=1)
        params = dict(method=method,columns=columns,confidence=confidence)
        if method == 'independent_t':
            params['equal_var'] = st.checkbox('Assume equal group variances (pooled t-test)',value=False)
            st.caption('Default: Welch t-test. Group labels are ordered lexicographically by typed value; difference is first minus second.')
        st.caption('Missingness: listwise deletion across selected variables. Invalid or nonfinite numeric values are excluded explicitly. No imputation. Review exclusions before running.')
        token = engine.digest(dict(dataset=selected,hash=record['sha256'],parameters=params))
        if st.button('Preview analysis and exclusions',disabled=not columns):
            st.session_state.analysis_preview = (token,engine.execute(registry,selected,params,preview=True))
        pending = st.session_state.get('analysis_preview')
        ready = pending and pending[0] == token
        if ready:
            st.subheader('Analysis preview')
            st.json(pending[1])
        if st.button('Run and save analysis',type='primary',disabled=not ready):
            with st.spinner('Computing locally…'):
                engine.execute(registry,selected,params)
            st.success('Immutable analysis run saved locally.')
        st.subheader('Analysis history')
        history_page = st.number_input('Run history page',min_value=1,value=1,step=1)
        runs = engine.history(registry,selected,page=int(history_page)-1)
        st.caption('20 immutable runs per page, newest first. Exports include source provenance, parameters, diagnostics and software versions.')
        if runs:
            run = st.selectbox('Saved analysis run',range(len(runs)),format_func=lambda i: f"{runs[i]['timestamp']} · {LABELS[runs[i]['parameters']['method']]} · {runs[i]['id'][:8]}")
            show(runs[run])
        else:
            st.info('No saved runs on this page.')
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error('Analysis failed. Check local storage and dependencies, then retry. Existing sources and saved runs are preserved.')
