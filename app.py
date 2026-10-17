#!/usr/bin/env python3
"""
SecondSelf personal knowledge workspace — capture, connect, and discover.

Usage:
  streamlit run app.py
"""

from __future__ import annotations

import shutil
import tempfile
import time
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from ask import AskError, AskResult, ask
from capture import capture_file, capture_text, capture_url, ensure_meta_index, write_capture
from config import (
    ASK_RATE_LIMIT_PER_MINUTE,
    DEPLOY_MODE,
    ENABLE_CAPTURE,
    ENABLE_REFRESH_BRAIN,
    GROQ_API_KEY,
    XAI_API_KEY,
    GRAPH_FILE,
    OPENAI_API_KEY,
    PARA_FOLDERS,
    ROOT,
)

try:
    from config import CAPTURE_RATE_LIMIT_PER_MINUTE
except ImportError:
    CAPTURE_RATE_LIMIT_PER_MINUTE = 5
from render_graph import load_graph, render_graph_html


def load_graph_stats() -> dict[str, Any]:
    graph = load_graph(GRAPH_FILE)
    meta = graph.get("meta") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    return {
        "meta": meta,
        "nodes": nodes,
        "edges": edges,
        "node_count": meta.get("node_count", len(nodes)),
        "edge_count": meta.get("edge_count", len(edges)),
        "generated_at": meta.get("generated_at", "unknown"),
    }


def llm_configured() -> bool:
    return bool(XAI_API_KEY or OPENAI_API_KEY or GROQ_API_KEY)


def ask_rate_limited() -> bool:
    now = time.time()
    window_start = now - 60
    timestamps = st.session_state.get("ask_timestamps", [])
    timestamps = [ts for ts in timestamps if ts >= window_start]
    st.session_state.ask_timestamps = timestamps
    return len(timestamps) >= ASK_RATE_LIMIT_PER_MINUTE


def record_ask_request() -> None:
    timestamps = st.session_state.setdefault("ask_timestamps", [])
    timestamps.append(time.time())
    st.session_state.ask_timestamps = timestamps


def capture_rate_limited() -> bool:
    now = time.time()
    window_start = now - 60
    timestamps = st.session_state.get("capture_timestamps", [])
    timestamps = [ts for ts in timestamps if ts >= window_start]
    st.session_state.capture_timestamps = timestamps
    return len(timestamps) >= CAPTURE_RATE_LIMIT_PER_MINUTE


def record_capture_request() -> None:
    timestamps = st.session_state.setdefault("capture_timestamps", [])
    timestamps.append(time.time())
    st.session_state.capture_timestamps = timestamps


def save_uploaded_file(uploaded_file: Any) -> tuple[Path, Path]:
    """Write an uploaded file to a temp path for capture_file(). Returns (file path, temp dir)."""
    temp_dir = Path(tempfile.mkdtemp(prefix="secondself_upload_"))
    path = temp_dir / Path(uploaded_file.name).name
    path.write_bytes(uploaded_file.getvalue())
    return path, temp_dir


def submit_capture(
    note_text: str,
    url_text: str,
    uploaded_file: Any | None,
) -> tuple[bool, str]:
    """Capture a note, link, or file using the same logic as capture.py."""
    if DEPLOY_MODE or not ENABLE_CAPTURE:
        return False, 'Capture is disabled in this workspace.'
    note = note_text.strip()
    url = url_text.strip()
    has_file = uploaded_file is not None

    inputs = sum([bool(note), bool(url), has_file])
    if inputs == 0:
        return False, "Enter a note, URL, or file to capture."
    if inputs > 1:
        return False, "Provide only one input: note, URL, or file."

    if capture_rate_limited():
        return False, (
            f"Rate limit reached ({CAPTURE_RATE_LIMIT_PER_MINUTE} captures per minute). "
            "Please wait and try again."
        )

    temp_dir: Path | None = None
    try:
        ensure_meta_index()
        if note:
            record = capture_text(note)
        elif url:
            record = capture_url(url)
        else:
            temp_path, temp_dir = save_uploaded_file(uploaded_file)
            record = capture_file(str(temp_path))

        output_path = write_capture(record)
        record_capture_request()
        return True, (
            f"Captured {record['type']} · ID `{record['id']}` · "
            f"`{output_path.relative_to(ROOT)}`"
        )
    except (ValueError, FileNotFoundError, OSError) as exc:
        return False, str(exc)
    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir, ignore_errors=True)


def render_sources(result: AskResult) -> None:
    if not result.sources:
        return

    st.markdown("**Sources**")
    for source in result.sources:
        if source.provenance:
            from document_ingestion import citation
            st.text(citation(source.provenance))
        st.markdown(
            f"- **{source.title}** · `{source.para}` · score `{source.score:.3f}`  \n"
            f"  {source.summary}"
        )


VIEWS = ('Home', 'Capture', 'Ask', 'Explore', 'Library', 'Insights', 'Datasets', 'Analyse')


def navigate(view):
    st.session_state.view = view


def remember(key):
    st.session_state['saved_' + key] = st.session_state[key]


def field(kind, label, key, default='', **kwargs):
    if key not in st.session_state:
        st.session_state[key] = st.session_state.get('saved_' + key, default)
    return getattr(st, kind)(label, key=key, on_change=remember, args=(key,), **kwargs)


def publish_saved():
    from workspace import index_notes
    try:
        with st.spinner('Indexing notes and publishing a verified graph…'):
            index_notes()
        st.session_state.pop('pending_index', None)
        if st.session_state.pop('pending_capture', False):
            st.session_state.reset_draft = True
        st.session_state.notice = 'Saved and indexed. Your graph and Ask sources are up to date.'
        st.rerun()
    except Exception:
        st.session_state.index_error = True
        st.rerun()


def new_draft():
    for name, value in [('title', ''), ('body', ''), ('tags', ''), ('para', 'resources')]:
        st.session_state['draft_' + name] = value
        st.session_state['saved_draft_' + name] = value


def keep_draft():
    drafts = st.session_state.setdefault('drafts', {})
    values = {name: st.session_state.get('draft_' + name, '') for name in ['title', 'body', 'tags', 'para']}
    if values['title'].strip() or values['body'].strip():
        drafts[values['title'] or 'Untitled draft'] = values


def restore_draft():
    values = st.session_state.drafts[st.session_state.draft_choice]
    for name, value in values.items():
        st.session_state['draft_' + name] = value
        st.session_state['saved_draft_' + name] = value


def capture_view():
    from workspace import save_note
    st.caption('A place for your next thought. Drafts stay in this browser session until you save.')
    if DEPLOY_MODE or not (ENABLE_CAPTURE and ENABLE_REFRESH_BRAIN):
        st.info('Capture is read-only here. Run locally with capture and refresh enabled to save notes.')
        return
    with st.expander('Import document'):
        document_import_view()
    if st.session_state.get('pending_index'):
        st.warning('A saved change is waiting for indexing. Retry before saving another note.')
        if st.button('Retry indexing', type='primary'):
            publish_saved()
        return
    if st.session_state.pop('reset_draft', False):
        new_draft()
    drafts = st.session_state.get('drafts', {})
    if drafts:
        st.selectbox('Saved session drafts', list(drafts), key='draft_choice')
        st.button('Open draft', on_click=restore_draft)
    st.button('New draft', on_click=new_draft)
    title = field('text_input', 'Title', 'draft_title', placeholder='Give this thought a name')
    body = field('text_area', 'Note', 'draft_body', height=300, placeholder='Write freely. Markdown is welcome.')
    left, right = st.columns(2)
    with left:
        para = field('selectbox', 'Category', 'draft_para', default='resources', options=list(PARA_FOLDERS))
    with right:
        tags = field('text_input', 'Tags', 'draft_tags', placeholder='ideas, work, learning')
    if st.button('Save & Index', type='primary'):
        if capture_rate_limited():
            st.error('Capture rate limit reached. Please try again in a minute.')
        else:
            try:
                path = save_note(title, body, para, tags)
                record_capture_request()
                st.session_state.pending_index = str(path)
                st.session_state.pending_capture = True
                publish_saved()
            except (ValueError, OSError) as exc:
                st.error(str(exc))
    st.button('Keep session draft', on_click=keep_draft)
    st.caption('Draft text is retained when you switch views. Session drafts are lost if the server session ends.')
    with st.expander('Import a link or file'):
        st.caption('Imports enter the raw capture inbox for classification. They are not indexed until processed.')
        url = st.text_input('URL')
        upload = st.file_uploader('File')
        if st.button('Save import to inbox'):
            with st.spinner('Importing…'):
                ok, message = submit_capture('', url, upload)
            (st.success if ok else st.error)(message)


def document_import_view():
    import document_ingestion as documents
    st.caption('PDF / UTF-8 CSV / XLSX · maximum 25 MiB. Extraction and Ollama indexing stay local. No OCR. Sources are saved only after confirmation.')
    uploaded = st.file_uploader('Document', type=['pdf', 'csv', 'xlsx'], key='document_upload')
    if uploaded is not None:
        try:
            preview = documents.extract(uploaded.name, uploaded.getvalue())
            st.write(preview['filename'])
            st.caption(f"SHA-256: {preview['sha256']} · {len(preview['segments'])} segments · pages: {preview.get('pages', '—')} · sheets: {', '.join(preview.get('sheets', []))}")
            for warning in preview['warnings']:
                st.warning(warning)
            for segment in preview['segments'][:20]:
                meta = dict(segment, filename=preview['filename'])
                st.text(documents.citation(meta))
                st.code(segment['text'], language=None)
            if len(preview['segments']) > 20:
                st.caption('Showing first 20 segments. Full extracted text is available below.')
            st.download_button('Review all extracted segments', data='\n\n'.join(documents.citation(dict(seg, filename=preview['filename'])) + '\n' + seg['text'] for seg in preview['segments']), file_name='extraction-preview.txt')
            if st.button('Save & Index document', type='primary'):
                with st.spinner('Saving and indexing locally…'):
                    documents.save_and_index(uploaded.name, uploaded.getvalue())
                st.success('Document indexed (identical reuploads reuse the existing import).')
        except Exception as exc:
            st.error(str(exc) if isinstance(exc, ValueError) else 'Import failed. Check local dependencies and retry.')
    st.markdown('**Import history**')
    for item in documents.history():
        st.text(f"{item['filename']} · {item['status']} · {item['sha256'][:12]}")
        with st.expander('Provenance ' + item['id'][:12]):
            st.json({k: v for k, v in item.items() if k != 'segments'})
        if item['status'] != 'indexed' and st.button('Retry import', key='retry_' + item['id']):
            try:
                documents.save_and_index(ident=item['id'])
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def ask_view():
    st.caption('Ask across your indexed notes. Questions and retrieved excerpts go to your configured answer provider (including Grok); Ollama embeddings stay local.')
    consent = st.checkbox('Allow sending retrieved document excerpts and my question to the configured external LLM (Grok/xAI, OpenAI or Groq); charges may apply.', value=False)
    history = st.session_state.setdefault('chat_history', [])
    for result in history:
        with st.chat_message('user'):
            st.write(result.question)
        with st.chat_message('assistant'):
            st.markdown(result.answer)
            render_sources(result)
    question = st.chat_input('Ask anything about your knowledge…')
    if question:
        if ask_rate_limited():
            st.error('Question rate limit reached. Please try again in a minute.')
        else:
            record_ask_request()
            try:
                with st.spinner('Finding sources and composing an answer…'):
                    result = ask(question, allow_document_external=consent)
                history.append(result)
                st.rerun()
            except AskError as exc:
                st.error(str(exc))
            except Exception:
                st.error('The answer provider could not complete this request. Please try again.')
    if history and st.button('Clear conversation'):
        st.session_state.chat_history = []
        st.rerun()


def filtered_notes(all_notes, prefix):
    query = field('text_input', 'Search notes', prefix + '_query', placeholder='Search titles, text or tags').casefold()
    para = field('selectbox', 'Category', prefix + '_para', default='all', options=['all', *PARA_FOLDERS])
    tags = sorted({tag for note in all_notes for tag in note.tags})
    selected = st.multiselect('Tags', tags, key=prefix + '_tags')
    return [n for n in all_notes if (para == 'all' or n.para == para)
            and (not selected or set(selected).issubset(n.tags))
            and query in (' '.join([n.title, n.body, *n.tags])).casefold()]


def library_view(all_notes):
    from workspace import save_note
    found = filtered_notes(all_notes, 'library')
    st.caption(f'{len(found)} notes · Select a note to read or edit')
    if not found:
        st.info('No matching notes. Try another search or capture your first thought.')
        return
    by_id = {n.id: n for n in found}
    ident = st.selectbox('Open note', list(by_id), format_func=lambda i: by_id[i].title)
    note = by_id[ident]
    st.caption(f'{note.para.title()} · ' + ', '.join(note.tags))
    st.markdown(note.body)
    if DEPLOY_MODE or not (ENABLE_CAPTURE and ENABLE_REFRESH_BRAIN):
        st.caption('This library is read-only.')
        return
    if note.frontmatter.get('document'):
        from document_ingestion import citation
        st.text(citation(note.frontmatter['document']))
        st.caption('Imported source evidence is read-only. Reimport a changed document as a new version.')
        return
    with st.expander('Edit note'):
        key = 'edit_' + ident
        snapshot_key = 'snapshot_' + ident
        st.session_state.setdefault(snapshot_key, note.path.read_text())
        def reopen():
            st.session_state[snapshot_key] = note.path.read_text()
            for suffix in ['title', 'body', 'tags']:
                st.session_state.pop(key + '_' + suffix, None)
                st.session_state.pop('saved_' + key + '_' + suffix, None)
        st.button('Reload from disk', key=key + '_reload', on_click=reopen)
        title = field('text_input', 'Title', key + '_title', note.title)
        body_default = note.body.split('\n', 1)[1].lstrip() if note.body.startswith('# ') else note.body
        body = field('text_area', 'Body', key + '_body', body_default, height=280)
        tags = field('text_input', 'Tags (comma separated)', key + '_tags', ', '.join(note.tags))
        if st.button('Save changes & Index', disabled=bool(st.session_state.get('pending_index'))):
            try:
                path = save_note(title, body, note.para, tags, path=note.path,
                                 expected=st.session_state[snapshot_key])
                st.session_state[snapshot_key] = path.read_text()
                st.session_state.pending_index = str(path)
                publish_saved()
            except (ValueError, OSError) as exc:
                st.error(str(exc))


def explore_view(all_notes, stats, appearance):
    found = filtered_notes(all_notes, 'explore')
    ids = {n.id for n in found}
    nodes = [n for n in stats['nodes'] if n['id'] in ids]
    edges = [e for e in stats['edges'] if e['source'] in ids and e['target'] in ids]
    st.caption(f'{len(nodes)} indexed notes · {len(edges)} connections. Drag to explore; select a node for details.')
    if not nodes:
        st.info('No verified graph matches these filters. Save & Index a note or refresh your knowledge.')
        return
    graph = {'nodes': nodes, 'edges': edges, 'meta': stats['meta']}
    markup = render_graph_html(graph, theme=appearance.lower())
    components.html(markup, height=780, scrolling=True)
    selected = st.selectbox('Read node details', nodes, format_func=lambda n: n.get('label', n['id']))
    st.write(selected.get('summary', ''))
    match = next((n for n in found if n.id == selected['id']), None)
    if match:
        with st.expander('Read full note'):
            st.markdown(match.body)


def insights_view():
    import insights
    from config import DATA_DIR
    st.caption('Evidence-backed candidates for human review. Local only by default; notes are never edited.')
    if DEPLOY_MODE:
        st.info('Insights are disabled in the read-only demo.')
        return
    scope = st.selectbox('Insight scope', ['all', *PARA_FOLDERS])
    cap = st.number_input('Maximum candidates', min_value=1, max_value=10, value=10)
    try:
        if st.button('Generate Insights', type='primary'):
            with st.spinner('Checking verified local evidence…'):
                items = insights.generate(DATA_DIR, scope, int(cap))
            if not items:
                st.info('No supported candidates in this scope. Small corpora may only support metadata observations.')
        records = insights.load(DATA_DIR)
        try:
            generation, notes, _ = insights.snapshot(DATA_DIR)
        except (ValueError, OSError, KeyError):
            generation, notes = None, []
            st.warning('Refresh the verified index before generating. Saved candidates below are stale.')
        for item in records.values():
            if scope != 'all' and any(s.get('para') != scope for s in item['sources']):
                continue
            with st.container(border=True):
                st.subheader(item['type'])
                st.write(item['claim'])
                is_stale = insights.stale(item, generation, notes)
                if is_stale:
                    st.warning('Stale insight: generation or source evidence changed. Regenerate before relying on it.')
                st.write(item['rationale'])
                for source in item['sources']:
                    with st.expander(source['title'] + ' · ' + source['id']):
                        st.text(source['excerpt'])
                        st.caption('Source fingerprint: ' + source['fingerprint'])
                st.caption('Generation: ' + item['generation'])
                st.write('Limitations: ' + item['limitations'])
                st.write('Suggested question/action: ' + item['question'])
                status = st.selectbox('Review status', insights.STATUSES,
                    index=insights.STATUSES.index(item['status']), key='status_' + item['id'] + '_' + item['status'])
                st.caption('Saved status: ' + item['status'])
                if st.button('Save review', key='review_' + item['id']):
                    insights.review(DATA_DIR, item['id'], status)
                    st.rerun()
                authorized = st.checkbox('Authorize sending these excerpts to xAI (leaves device; may cost money)', key='cloud_' + item['id'])
                if st.button('Ask xAI to select a review question', key='send_' + item['id'], disabled=is_stale or not authorized):
                    st.write(insights.cloud_question(DATA_DIR, item['id'], authorized=authorized))
    except ValueError as exc:
        st.error(str(exc))
    except (OSError, KeyError, TypeError):
        st.error('Insights unavailable. Check verified index, metadata, local storage and provider configuration. Existing notes are preserved.')


def main():
    from workspace import notes
    st.set_page_config(page_title='SecondSelf · Workspace', page_icon='◈', layout='wide')
    st.markdown('''<style>
    .block-container{max-width:1280px;padding-top:2.5rem;padding-bottom:4rem}
    h1{letter-spacing:-.045em;font-weight:700}h2,h3{letter-spacing:-.025em}
    [data-testid="stMetric"]{border:1px solid var(--workspace-border,#d5dce5);border-radius:14px;padding:1rem}
    [data-testid="stSidebar"]{border-right:1px solid var(--workspace-border,#d5dce5)}
    button:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid #818cf8!important;outline-offset:3px}
    @media(max-width:640px){.block-container{padding:1.2rem 1rem}h1{font-size:2rem}}
    </style>''', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown('## ◈ SecondSelf')
        st.caption('YOUR KNOWLEDGE, CONNECTED')
        view = st.radio('Workspace', VIEWS, key='view')
        st.divider()
        appearance = st.selectbox('Appearance', ['Light', 'Dark'])
        st.caption('Demo workspace' if DEPLOY_MODE else 'Local workspace')
        st.caption('Capture → Connect → Discover')
        if not DEPLOY_MODE and ENABLE_REFRESH_BRAIN:
            if st.button('Refresh index', use_container_width=True):
                try:
                    from workspace import index_notes
                    with st.spinner('Refreshing verified knowledge…'):
                        index_notes()
                    st.session_state.pop('pending_index', None)
                    st.session_state.notice = 'Knowledge index refreshed.'
                    st.rerun()
                except Exception:
                    st.error('Refresh failed. Check provider availability and the approved refresh workflow.')
    dark = appearance == 'Dark'
    bg, panel, fg, border = ('#101827', '#192437', '#f1f5f9', '#46566e') if dark else ('#fafbfe', '#f0f3f9', '#172033', '#d5dce5')
    st.markdown(f'''<style>:root{{--workspace-border:{border}}}
    .stApp{{background:{bg};color:{fg};--text-color:{fg};--background-color:{bg};--secondary-background-color:{panel};--primary-color:#6366f1}}
    [data-testid="stSidebar"]{{background:{panel};color:{fg}}}
    [data-testid="stHeader"]{{background:{bg}}}
    [data-baseweb="input"],[data-baseweb="textarea"],[data-baseweb="select"]>div{{background:{panel};color:{fg}}}
    .stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp h4,
    .stApp [data-testid="stMetricValue"],.stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stCaptionContainer"]{{color:{fg}!important}}
    .stApp button{{background:{panel};color:{fg};border-color:{border}}}
    .stApp button[kind="primary"]{{background:#4f46e5;color:#fff}}
    .stApp button[kind="primary"] p{{color:#fff!important}}
    .stApp [data-baseweb="select"]>div,.stApp [data-baseweb="input"],
    .stApp [data-baseweb="textarea"]{{background:{panel}!important;color:{fg}!important}}
    .stApp [data-baseweb="select"] span{{color:{fg}!important}}
    input,textarea{{background:{panel}!important;color:{fg}!important;-webkit-text-fill-color:{fg}!important}}
    input::placeholder,textarea::placeholder{{color:{fg}!important;opacity:.7}}
    [role="listbox"],[role="option"]{{background:{panel}!important;color:{fg}!important}}

    </style>''', unsafe_allow_html=True)
    if DEPLOY_MODE:
        st.info('Demo · Sample knowledge only. Do not enter personal information. Capture and editing are disabled.')
    if st.session_state.pop('index_error', False):
        st.error('Your note is saved, but indexing did not finish. Check your embedding provider and refresh approval settings, then retry. Drafts are preserved.')
        st.caption('For external embedding approval or legacy migration, see docs/phase2-operations.md.')
    if notice := st.session_state.pop('notice', None):
        st.success(notice)
    st.title(view)
    stats = load_graph_stats()
    all_notes = notes()
    if stats['meta'].get('error') or isinstance(stats['meta'].get('freshness'), dict):
        st.warning('Your graph needs a verified refresh. Saved notes remain available in Library.')
    if st.session_state.get('pending_index') and view != 'Capture':
        st.warning('A saved change needs indexing. Open Capture to retry.')
    if view == 'Home':
        st.caption('Make room for ideas. Find the connections that matter.')
        cols = st.columns(3)
        for col, label, value in zip(cols, ['Notes', 'Connections', 'Categories'], [len(all_notes), stats['edge_count'], len({n.para for n in all_notes})]):
            col.metric(label, value)
        st.subheader('Pick up where you left off')
        cols = st.columns(3)
        for col, label, target in zip(cols, ['＋ Capture a thought', 'Ask your knowledge', 'Explore connections'], ['Capture', 'Ask', 'Explore']):
            col.button(label, on_click=navigate, args=(target,), use_container_width=True)
        st.subheader('Recent notes')
        if not all_notes:
            st.info('Your workspace starts with one thought. Open Capture to add your first note.')
        for note in all_notes[:6]:
            with st.container(border=True):
                st.markdown('**' + note.title.replace('*', '') + '**')
                st.caption(f'{note.para.title()} · {note.created[:10] or "No date"}')
                st.write(note.summary)
        st.caption(f'Last graph update: {stats["generated_at"]}')
    elif view == 'Capture':
        capture_view()
    elif view == 'Ask':
        ask_view()
    elif view == 'Datasets':
        from dataset_ui import render
        render()
    elif view == 'Analyse':
        from analysis_ui import render
        render()
    elif view == 'Insights':
        insights_view()
    elif view == 'Explore':
        explore_view(all_notes, stats, appearance)
    else:
        library_view(all_notes)


if __name__ == '__main__':
    main()
