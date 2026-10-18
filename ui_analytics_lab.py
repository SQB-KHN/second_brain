"""Presentation-only Analytics Lab components for the SecondSelf Streamlit workspace.

No filesystem, network, indexing, dataset registry or provider side effects.
"""
from __future__ import annotations

import html

import streamlit as st


NAV_GROUPS = (
    ("WORKSPACE", ("Home", "Ask", "Capture")),
    ("KNOWLEDGE", ("Library", "Explore", "Insights")),
    ("RESEARCH & DATA", ("Datasets", "Analyse")),
)

NAV_ICONS = {
    "Home": "◫", "Ask": "◈", "Capture": "＋", "Library": "▤",
    "Explore": "◎", "Insights": "✦", "Datasets": "▦", "Analyse": "◩",
}

SUBTITLES = {
    "Home": "An overview of your local intelligence workspace",
    "Capture": "Collect and index traceable knowledge",
    "Ask": "Ask grounded questions with transparent sources",
    "Explore": "Investigate connections in verified knowledge",
    "Library": "Browse and manage your source-backed notes",
    "Insights": "Review evidence-backed findings and their limitations",
    "Datasets": "Inspect and version structured data locally",
    "Analyse": "Run reproducible statistical procedures on registered data",
}

def nav_label(view: str) -> str:
    return f"{NAV_ICONS.get(view, '•')}  {view}"

def theme_css(dark: bool) -> str:
    """Curated, view-independent visual tokens; does not affect widget behaviour."""
    if dark:
        base, surface, surface2, ink, muted, line, accent, sidebar = (
            "#0b1220", "#152239", "#1c2b44", "#e8eef8",
            "#a5b4ca", "#31425a", "#60a5fa", "#101b2e"
        )
    else:
        base, surface, surface2, ink, muted, line, accent, sidebar = (
            "#f5f7fb", "#ffffff", "#edf3fa", "#192b46",
            "#59708d", "#dce5f0", "#2563eb", "#eaf0f8"
        )
    return f"""<style>
    :root{{--lab-base:{base};--lab-surface:{surface};--lab-surface2:{surface2};
      --lab-ink:{ink};--lab-muted:{muted};--lab-line:{line};--lab-accent:{accent}}}
    .block-container{{max-width:1440px;padding-top:1.6rem;padding-bottom:4rem}}
    .stApp{{background:{base};color:{ink}}}
    [data-testid="stSidebar"]{{background:{sidebar};border-right:1px solid {line}}}
    [data-testid="stSidebar"] [data-testid="stRadio"] label{{line-height:1.6}}
    [data-testid="stHeader"]{{background:{base}}}
    .lab-kicker{{font-size:.72rem;font-weight:750;letter-spacing:.13em;color:{accent};
      text-transform:uppercase;margin:0 0 .4rem}}
    .lab-hero{{border:1px solid {line};border-radius:18px;
      padding:1.25rem 1.5rem;background:{surface};margin:.2rem 0 1.25rem}}
    .lab-hero h2{{font-size:1.65rem;letter-spacing:-.035em;color:{ink};
      margin:0 0 .3rem;font-weight:750;line-height:1.25}}
    .lab-hero p{{font-size:.92rem;color:{muted};margin:0}}
    .lab-section{{font-size:.76rem;text-transform:uppercase;letter-spacing:.12em;
      font-weight:750;color:{muted};margin:1.4rem 0 .7rem}}
    [data-testid="stMetric"]{{background:{surface};border:1px solid {line};
      border-radius:14px;padding:1rem 1.15rem;box-shadow:0 2px 8px #00000008}}
    [data-testid="stMetricLabel"]{{font-size:.83rem;letter-spacing:.012em}}
    [data-testid="stVerticalBlockBorderWrapper"] > div[style*="border"]{{
      border-color:{line}!important;border-radius:14px!important}}
    .stButton > button{{border-radius:10px;min-height:2.55rem;font-weight:600}}
    .stButton > button[kind="primary"]{{background:{accent};color:white;border-color:{accent}}}
    [data-testid="stDataFrame"]{{border:1px solid {line};border-radius:12px;overflow:hidden}}
    .lab-note{{color:{muted};font-size:.82rem}}
    button:focus-visible,input:focus-visible,textarea:focus-visible,
    [role="radiogroup"] label:focus-within{{outline:2px solid {accent}!important;outline-offset:2px}}
    @media (max-width:740px){{
      .block-container{{padding:1rem .85rem 3rem}}
      .lab-hero{{padding:1rem}}.lab-hero h2{{font-size:1.35rem}}
    }}
    </style>"""

def hero(name: str) -> None:
    subtitle = SUBTITLES.get(name, "Your local research workspace")
    st.markdown(
        '<div class="lab-hero"><div class="lab-kicker">Analytics Lab / '
        + html.escape(name)
        + '</div><h2>' + html.escape(name)
        + '</h2><p>' + html.escape(subtitle) + '</p></div>',
        unsafe_allow_html=True,
    )

def section(label: str) -> None:
    st.markdown('<div class="lab-section">' + html.escape(label) + '</div>',
                unsafe_allow_html=True)

def home(notes, graph_stats, navigate) -> None:
    """Only use already-read note/index metadata: works in demo without dataset access."""
    hero("Home")
    section("Knowledge at a glance")
    cols = st.columns(4)
    metrics = (
        ("Indexed notes", len(notes)),
        ("Graph connections", graph_stats["edge_count"]),
        ("Knowledge areas", len({n.para for n in notes})),
        ("Graph nodes", graph_stats["node_count"]),
    )
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)
    section("Start a workflow")
    shortcuts = (
        ("＋ Capture a note", "Capture", "Write and index knowledge"),
        ("◈ Ask knowledge", "Ask", "Question your sources"),
        ("▦ Open datasets", "Datasets", "Inspect structured data"),
        ("◩ Start analysis", "Analyse", "Statistical workflows"),
    )
    for col, (label, target, description) in zip(st.columns(4), shortcuts):
        with col:
            st.button(label, key="lab_home_" + target, on_click=navigate,
                      args=(target,), use_container_width=True)
            st.caption(description)
    left, right = st.columns([3, 2], gap="large")
    with left:
        section("Recent knowledge")
        if not notes:
            st.info("No notes yet. Capture your first note to begin.")
        for note in notes[:6]:
            with st.container(border=True):
                # Titles and summaries are untrusted source material: render as plain text.
                st.text(note.title)
                st.caption(f"{note.para.title()} · {note.created[:10] or 'No date'}")
                st.write(note.summary)
    with right:
        section("Workspace status")
        with st.container(border=True):
            st.write("Verified graph")
            st.caption("Last update: " + str(graph_stats["generated_at"]))
            st.caption("Local-first knowledge and dataset workflows")
            st.caption("External AI requests are explicitly user-initiated")
        section("Explore")
        st.button("◎ Explore graph", on_click=navigate, args=("Explore",),
                  use_container_width=True, key="lab_graph")
        st.button("✦ Review insights", on_click=navigate, args=("Insights",),
                  use_container_width=True, key="lab_insights")
