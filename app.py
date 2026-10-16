#!/usr/bin/env python3
"""
SecondSelf Streamlit app — interactive graph + RAG Q&A.

Phase 7 — Integration (Streamlit app).

Usage:
  streamlit run app.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
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
    DATA_DIR,
    DEPLOY_MODE,
    ENABLE_CAPTURE,
    ENABLE_REFRESH_BRAIN,
    GROQ_API_KEY,
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

GRAPH_COMPONENT_HEIGHT = 600
PIPELINE_SCRIPTS = ("refresh.py",)


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


def count_nodes_by_para(nodes: list[dict[str, Any]], para: str) -> int:
    if para == "all":
        return len(nodes)
    return sum(1 for node in nodes if node.get("para") == para)


def run_pipeline_step(script_name: str) -> tuple[bool, str]:
    script_path = ROOT / script_name
    result = subprocess.run(
        [sys.executable, str(script_path), "refresh"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "") + (result.stderr or "")
    output = output.strip() or f"{script_name} finished with no output."
    return result.returncode == 0, output


def refresh_brain() -> tuple[bool, list[str]]:
    logs: list[str] = []
    for script_name in PIPELINE_SCRIPTS:
        ok, output = run_pipeline_step(script_name)
        logs.append(f"$ python {script_name}\n{output}")
        if not ok:
            return False, logs
    return True, logs


def llm_configured() -> bool:
    return bool(OPENAI_API_KEY or GROQ_API_KEY)


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
    path = temp_dir / uploaded_file.name
    path.write_bytes(uploaded_file.getvalue())
    return path, temp_dir


def submit_capture(
    note_text: str,
    url_text: str,
    uploaded_file: Any | None,
) -> tuple[bool, str]:
    """Capture a note, link, or file using the same logic as capture.py."""
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
        st.markdown(
            f"- **{source.title}** · `{source.para}` · score `{source.score:.3f}`  \n"
            f"  {source.summary}"
        )


def main() -> None:
    st.set_page_config(
        page_title="SecondSelf",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "ask_busy" not in st.session_state:
        st.session_state.ask_busy = False
    if "refresh_busy" not in st.session_state:
        st.session_state.refresh_busy = False
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = None
    if "ask_timestamps" not in st.session_state:
        st.session_state.ask_timestamps = []
    if "capture_timestamps" not in st.session_state:
        st.session_state.capture_timestamps = []
    if "capture_busy" not in st.session_state:
        st.session_state.capture_busy = False

    stats = load_graph_stats()
    nodes = stats["nodes"]

    st.title("SecondSelf")
    st.caption("Your self-organizing personal AI knowledge system")

    if DEPLOY_MODE:
        st.info(
            "Public demo mode — sample knowledge corpus only. "
            "Do not enter personal information."
        )

    busy = st.session_state.refresh_busy or st.session_state.ask_busy or st.session_state.capture_busy

    st.subheader("Capture")
    if ENABLE_CAPTURE:
        if DEPLOY_MODE:
            st.caption(
                "Captures are stored on the server filesystem and may not persist "
                "after the app restarts on Streamlit Cloud."
            )
        note_text = st.text_area(
            "Note",
            placeholder="Type a thought, idea, or meeting note...",
            height=120,
            disabled=busy,
            label_visibility="collapsed",
        )
        with st.expander("Link or file"):
            url_text = st.text_input(
                "URL",
                placeholder="https://example.com/article",
                disabled=busy,
            )
            uploaded_file = st.file_uploader(
                "File",
                disabled=busy,
                label_visibility="collapsed",
            )

        capture_clicked = st.button(
            "Capture",
            type="primary",
            disabled=busy,
        )
        if capture_clicked:
            st.session_state.capture_busy = True
            with st.spinner("Saving capture..."):
                ok, message = submit_capture(note_text, url_text, uploaded_file)
            st.session_state.capture_busy = False
            if ok:
                st.success(message)
                st.info(
                    "Capture queued for classification. Review classification and embedding "
                    "API costs before processing it; see docs/phase2-operations.md."
                )
            else:
                st.error(message)
    else:
        st.caption(
            "Capture is disabled in public deploy mode. "
            "Set `ENABLE_CAPTURE=true` in Streamlit secrets, or run locally with "
            "`./capture.sh --text \"your note\"`."
        )

    st.divider()

    with st.sidebar:
        st.header("Brain stats")
        st.metric("Notes", stats["node_count"])
        st.metric("Links", stats["edge_count"])
        st.caption(f"Graph generated: {stats['generated_at']}")
        st.caption(f"Data source: `{DATA_DIR.relative_to(ROOT)}`")

        para_filter = st.selectbox(
            "Filter by PARA",
            ["all", *PARA_FOLDERS],
            format_func=lambda value: "All categories" if value == "all" else value.title(),
        )
        filtered_count = count_nodes_by_para(nodes, para_filter)
        st.caption(f"{filtered_count} note(s) in this category")

        st.divider()
        st.header("Pipeline")

        if ENABLE_REFRESH_BRAIN:
            refresh_disabled = busy
            if st.button("Refresh brain", disabled=refresh_disabled, use_container_width=True):
                st.session_state.refresh_busy = True
                with st.spinner("Refreshing verified knowledge artifacts..."):
                    ok, logs = refresh_brain()
                st.session_state.refresh_busy = False
                if ok:
                    st.success("Brain refreshed.")
                    st.rerun()
                else:
                    st.error("Refresh failed. See log below.")
                    st.code("\n\n".join(logs), language="text")
        else:
            st.caption("Refresh brain is disabled in public deploy mode.")

        if not ENABLE_CAPTURE:
            st.caption(
                "Capture is disabled. Set ENABLE_CAPTURE=true in secrets to enable."
            )

        if not llm_configured():
            st.warning("Ask requires OPENAI_API_KEY or GROQ_API_KEY in secrets/.env.")
        elif not OPENAI_API_KEY:
            st.warning("Embeddings require OPENAI_API_KEY. Ask retrieval may be limited.")

        st.divider()
        st.markdown("**Legend**")
        st.markdown(
            "- Projects · green\n"
            "- Areas · blue\n"
            "- Resources · orange\n"
            "- Archives · gray"
        )

    st.subheader("Knowledge graph")
    st.caption("Hover for summaries, drag to rearrange, click a node for details.")
    graph_html = render_graph_html(graph_file=GRAPH_FILE)
    components.html(graph_html, height=GRAPH_COMPONENT_HEIGHT, scrolling=False)

    st.divider()
    st.subheader("Ask your brain")

    question = st.text_input(
        "Ask anything about your knowledge...",
        placeholder="What projects am I working on?",
        disabled=busy,
    )
    ask_clicked = st.button(
        "Ask",
        type="primary",
        disabled=busy or st.session_state.ask_busy,
    )

    if ask_clicked:
        if not question.strip():
            st.error("Question cannot be empty.")
        elif not llm_configured():
            st.error("API key not configured. Set OPENAI_API_KEY or GROQ_API_KEY in secrets/.env.")
        elif ask_rate_limited():
            st.error(
                f"Rate limit reached ({ASK_RATE_LIMIT_PER_MINUTE} questions per minute). "
                "Please wait and try again."
            )
        else:
            st.session_state.ask_busy = True
            with st.spinner("Searching your notes and synthesizing an answer..."):
                try:
                    result = ask(question)
                    record_ask_request()
                except AskError as exc:
                    st.error(str(exc))
                    result = None
            st.session_state.ask_busy = False
            st.session_state.last_answer = result

    result = st.session_state.last_answer
    if isinstance(result, AskResult):
        st.markdown("### Answer")
        st.markdown(result.answer)
        render_sources(result)
        if result.tokens_used is not None:
            st.caption(f"Tokens used: {result.tokens_used}")


if __name__ == "__main__":
    main()
