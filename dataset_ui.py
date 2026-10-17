"""Local Datasets workspace, deliberately separate from knowledge/AI workflows."""
import hashlib
import json
import string
import streamlit as st
import config
from dataset_parser import parse, MAX_BYTES
from dataset_profile import profile
from dataset_registry import Registry


def plain(value):
    # Streamlit labels support Markdown images; uploaded labels must stay text.
    return ''.join('\\'+c if c in string.punctuation else c for c in str(value))


def preview(table):
    info = profile(table)
    a,b,c = st.columns(3)
    a.metric('Rows', info['row_count'])
    b.metric('Columns', info['column_count'])
    c.metric('Duplicate rows', info['duplicate_rows'])
    st.caption('Types are inferred. Blanks are missing; literal NA/NaN strings are retained. Numeric-looking identifiers may be ambiguous.')
    st.dataframe(info['columns'], hide_index=True, use_container_width=True)
    # Bound both axes and each rendered cell; no full-table rendering.
    st.caption('Sample: first 10 rows × 10 columns; values truncated to 120 characters.')
    st.dataframe([{n: str(r[i])[:120] if r[i] is not None else None for i,n in enumerate(table['columns'][:10])} for r in table['rows'][:10]], hide_index=True)


def render():
    if config.DEPLOY_MODE:
        st.info('Datasets are disabled in the read-only demo. Private datasets are not accessed.')
        return
    st.caption('Local tables · immutable versions · descriptive statistics. Dataset contents stay on this machine and are never sent to AI services.')
    st.caption('Limits: 10 MiB/file, 20 sheets, 20,000 rows, 100 columns, 100,000 cells, 4096 characters/cell. No deletion or cloud sync.')
    try:
        registry = Registry()
        upload = st.file_uploader('Upload dataset', type=['csv','xlsx','parquet'], key='dataset_upload')
        if upload:
            if upload.size > MAX_BYTES:
                st.error('File exceeds 10 MiB. Split it before uploading.')
            else:
                content = upload.getvalue()
                digest = hashlib.sha256(content).hexdigest()
                name = st.text_input('Dataset name', value=upload.name.rsplit('.',1)[0], key='dataset_name_'+digest)
                sheet = None
                if upload.name.lower().endswith('.xlsx'):
                    manifest = parse(upload.name, content)
                    sheet = st.selectbox('Worksheet', manifest['sheets'], index=None, placeholder='Select a worksheet')
                token = (digest, sheet, upload.name)
                if st.button('Preview dataset', disabled=upload.name.lower().endswith('.xlsx') and sheet is None):
                    st.session_state.dataset_preview = (token, parse(upload.name, content, sheet))
                pending = st.session_state.get('dataset_preview')
                if pending and pending[0] == token:
                    st.subheader('Import preview')
                    if sheet:
                        st.text(f'Workbook: {upload.name} · Sheet: {sheet}')
                    preview(pending[1])
                    if st.button('Confirm dataset import', type='primary'):
                        record, created = registry.register(name,upload.name,content,sheet)
                        st.success(f"{'Imported' if created else 'Already imported'}: {plain(record['name'])} · version {record['version']}")
        st.subheader('Dataset inventory')
        st.caption('100 versions per page, newest first. Search by dataset or source name.')
        query = st.text_input('Search datasets')
        if st.button('Refresh inventory'):
            st.session_state.pop('dataset_preview', None)
        total = registry.inventory_count(query)
        page = st.number_input('Inventory page', min_value=1, max_value=max(1,(total+99)//100), value=1, step=1)
        records = registry.inventory(query, page=int(page)-1)
        if not records:
            st.info('No datasets found. Preview an upload to begin.')
            return
        st.dataframe([dict(name=r['name'],source=r['filename'],version=r['version'],format=r['format'],rows=r['profile']['row_count'],columns=r['profile']['column_count'],created=r['created']) for r in records], hide_index=True)
        selected = st.selectbox('Inspect dataset version', [r['id'] for r in records], format_func=lambda identity: next(f"{r['name']} · v{r['version']} · {r['filename']} · {r['options'].get('sheet') or r['format']}" for r in records if r['id']==identity))
        record, table = registry.inspect(selected)
        st.caption(f"SHA-256: {record['sha256']} · {record['bytes']} bytes · {record['origin']} · {record['created']}")
        preview(table)
        def analyse():
            st.session_state.analyse_dataset = selected
            st.session_state.view = 'Analyse'
        st.button('Analyse this version', on_click=analyse)
        if st.button('Reprofile selected version'):
            registry.reprofile(selected)
            st.success('Profile refreshed from verified original bytes.')
        st.subheader('Data dictionary')
        st.caption('Metadata only. Edits never change the original table or inferred types.')
        with st.form('dictionary_'+selected):
            edits = {}
            for column, item in record['dictionary'].items():
                with st.expander(plain(column)):
                    edits[column] = dict(description=st.text_area('Description', value=item['description'], max_chars=1000, key=selected+column+'description'), units=st.text_input('Units', value=item['units'], max_chars=1000, key=selected+column+'units'))
            if st.form_submit_button('Save data dictionary'):
                registry.dictionary(selected, edits)
                st.success('Data dictionary saved; original bytes unchanged.')
        st.subheader('Descriptive statistics')
        st.caption('Counts, missingness, sample standard deviation and linearly interpolated quartiles. No statistical tests, regression or inference.')
        columns = st.multiselect('Statistics columns', table['columns'], default=table['columns'][:5], key='statistics_columns_'+selected)
        if st.button('Compute and save statistics', disabled=not columns):
            registry.statistics(selected,columns)
            st.success('Reproducible statistics saved locally.')
        st.caption('The 50 most recent saved runs for this version are shown.')
        outputs = registry.saved_statistics(selected)
        if outputs:
            output = st.selectbox('Saved statistics run', list(range(len(outputs))), format_func=lambda i: outputs[i]['timestamp'])
            st.json(outputs[output])
            st.download_button('Download statistics JSON', json.dumps(outputs[output], indent=2), file_name='dataset-statistics.json', mime='application/json')
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error('Dataset operation failed. Check local storage permissions and available disk space, then refresh and retry. Existing dataset versions are preserved.')
