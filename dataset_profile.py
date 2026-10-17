"""Deterministic descriptive statistics, without models or expressions."""
import datetime as dt
import importlib.metadata
import math
import platform
import statistics

PROFILE_VERSION = 1


def numeric(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (ValueError, TypeError, OverflowError):
        return None


def temporal(value):
    try:
        dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def profile(table):
    columns = []
    rows = table['rows']
    for i, name in enumerate(table['columns']):
        values = [r[i] for r in rows if r[i] is not None]
        nums = [numeric(v) is not None for v in values]
        dates = [temporal(v) for v in values]
        distinct = len({(type(v).__name__, str(v)) for v in values})
        ambiguity = []
        if not values:
            kind = 'textual'
            ambiguity.append('All values missing; type unknown')
        elif all(nums):
            kind = 'numeric'
            if any(isinstance(v, str) and v.strip().startswith('0') and len(v.strip()) > 1 and v.strip()[1].isdigit() for v in values):
                ambiguity.append('Leading zeros: numbers may be identifiers')
        elif all(dates):
            kind = 'temporal'
        elif distinct <= 50 and max(map(lambda v: len(str(v)), values)) <= 128:
            kind = 'categorical'
        else:
            kind = 'textual'
        if any(nums) and not all(nums):
            ambiguity.append('Mixed numeric and nonnumeric values; excluded from numeric statistics')
        if any(dates) and not all(dates):
            ambiguity.append('Mixed temporal and other values')
        columns.append(dict(name=name, type=kind, nulls=len(rows)-len(values), distinct=distinct, ambiguities=ambiguity))
    return dict(profile_version=PROFILE_VERSION, row_count=len(rows), column_count=len(columns), duplicate_rows=len(rows)-len({tuple((type(v).__name__, str(v)) for v in r) for r in rows}), columns=columns)


def quantile(ordered, q):
    pos = (len(ordered)-1)*q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    return ordered[lo] * (1-(pos-lo)) + ordered[hi] * (pos-lo)


def describe(table, selected):
    if not selected or len(selected) != len(set(selected)) or any(n not in table['columns'] for n in selected):
        raise ValueError('Select existing, unique columns.')
    schema = {c['name']: c for c in profile(table)['columns']}
    result = {}
    for name in selected:
        i = table['columns'].index(name)
        values = [r[i] for r in table['rows'] if r[i] is not None]
        item = dict(count=len(values), missing=len(table['rows'])-len(values), missing_fraction=(len(table['rows'])-len(values))/len(table['rows']) if table['rows'] else 0, type=schema[name]['type'])
        if item['type'] == 'numeric' and values:
            nums = sorted(numeric(v) for v in values)
            try:
                item.update(mean=statistics.mean(nums), median=statistics.median(nums), std=statistics.stdev(nums) if len(nums)>1 else None, min=nums[0], max=nums[-1], quantiles={str(q): quantile(nums, q) for q in (.25, .5, .75)})
                if any(v is not None and not math.isfinite(v) for k,v in item.items() if k in ('mean','median','std','min','max')) or any(not math.isfinite(v) for v in item['quantiles'].values()):
                    raise OverflowError()
            except (OverflowError, ValueError):
                raise ValueError('Numeric range exceeds reliable descriptive arithmetic. Rescale source values.') from None
        elif item['type'] == 'categorical':
            counts = {}
            for v in values:
                key = f'{type(v).__name__}:{v}'
                counts[key] = counts.get(key, 0) + 1
            item['category_counts'] = dict(sorted(counts.items()))
        result[name] = item
    return dict(statistics=result, parameters=dict(quantiles=[.25,.5,.75], quantile_method='linear interpolation (n-1)*q', std_ddof=1, missing='null, blank/whitespace, nonfinite native floats; literal NA/NaN retained', numeric_policy='entire nonmissing column must parse as finite numeric; booleans excluded'), software=dict(python=platform.python_version(), profile_version=PROFILE_VERSION, **{n: importlib.metadata.version(n) for n in ('pyarrow','openpyxl')}))
