#!/usr/bin/env python3
"""
SecondSelf Streamlit app — interactive graph + RAG Q&A.

Phase 7 — Integration (Streamlit app).

Usage:
  streamlit run app.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from ask import AskError, AskResult, ask
from config import (
    ASK_RATE_LIMIT_PER_MINUTE,
    DATA_DIR,
    DEPLOY_MODE,
    ENABLE_REFRESH_BRAIN,
    GROQ_API_KEY,
    GRAPH_FILE,
    OPENAI_API_KEY,
    PARA_FOLDERS,
    ROOT,
)
from render_graph import load_graph, render_graph_html

GRAPH_COMPONENT_HEIGHT = 600
PIPELINE_SCRIPTS = ("classify.py", "link.py", "build_graph.py")


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
        [sys.executable, str(script_path)],
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

    stats = load_graph_stats()
    nodes = stats["nodes"]

    st.title("SecondSelf")
    st.caption("Your self-organizing personal AI knowledge system")

    if DEPLOY_MODE:
        st.info(
            "Public demo mode — sample knowledge corpus only. "
            "Do not enter personal information."
        )

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
            refresh_disabled = st.session_state.ask_busy or st.session_state.refresh_busy
            if st.button("Refresh brain", disabled=refresh_disabled, use_container_width=True):
                st.session_state.refresh_busy = True
                with st.spinner("Running classify → link → build_graph..."):
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
        disabled=st.session_state.refresh_busy,
    )
    ask_clicked = st.button(
        "Ask",
        type="primary",
        disabled=st.session_state.refresh_busy or st.session_state.ask_busy,
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
