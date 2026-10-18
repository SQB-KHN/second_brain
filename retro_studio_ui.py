"""Presentation-only Retro Studio × Y2K design system.

Uses native Streamlit controls, preserves accessibility and all local-first workflows.
No remote assets, filesystem access or provider calls.
"""
from __future__ import annotations

import streamlit as st


def css(dark: bool = False) -> str:
    if dark:
        paper, canvas, sidebar, ink, secondary, frame, mint, yellow = (
            "#20232c", "#171b22", "#262d36", "#edf0e7", "#acb8b4",
            "#57636a", "#385e58", "#786342"
        )
    else:
        paper, canvas, sidebar, ink, secondary, frame, mint, yellow = (
            "#fffdf4", "#f4f0df", "#e9e5d6", "#292b2c", "#6f716d",
            "#858578", "#d6ece1", "#f6d77c"
        )
    # Streamlit internals remain lightly scoped: no global hide, pointer-events, or
    # injected user content. Widget labels and accessibility semantics are retained.
    return f"""<style>
    :root{{--retro-canvas:{canvas};--retro-paper:{paper};--retro-ink:{ink};
      --retro-secondary:{secondary};--retro-frame:{frame};
      --retro-mint:{mint};--retro-yellow:{yellow}}}
    .stApp{{background:{canvas}!important;color:{ink}!important;
      --background-color:{canvas};--text-color:{ink};
      --secondary-background-color:{paper};--primary-color:#537f70}}
    [data-testid="stHeader"]{{background:{canvas}!important}}
    [data-testid="stSidebar"]{{background:{sidebar}!important;
      border-right:2px solid {frame}!important}}
    [data-testid="stSidebar"] h2{{font-family:Georgia,serif!important;
      letter-spacing:-.04em!important}}
    [data-testid="stSidebar"] [role="radiogroup"] label{{
      padding:.5rem .6rem;border-radius:8px;
      transition:background .12s ease}}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover{{
      background:{paper}}}
    .block-container{{max-width:1480px;padding-top:1.25rem!important}}
    .stApp h1,.stApp h2{{font-family:Georgia,serif;letter-spacing:-.035em}}
    .stApp h1{{font-size:clamp(2rem,3vw,2.8rem);line-height:1.12}}
    .stApp [data-testid="stVerticalBlockBorderWrapper"] > div[style*="border"],
    .stApp [data-testid="stMetric"]{{
      border:1px solid {frame}!important;border-radius:9px!important;
      background:{paper}!important;box-shadow:3px 3px 0 {frame}30!important}}
    .stApp [data-testid="stMetric"]{{padding:1rem}}
    .stApp div[data-testid="stForm"]{{
      border:1px solid {frame};background:{paper};border-radius:10px;
      padding:1rem}}
    .stApp .stButton > button{{
      border:1px solid {frame}!important;border-radius:7px!important;
      background:{paper}!important;color:{ink}!important;
      min-height:2.4rem;box-shadow:1px 2px 0 {frame}50!important;
      font-weight:650}}
    .stApp .stButton > button:active{{transform:translate(1px,1px);
      box-shadow:none!important}}
    .stApp .stButton > button[kind="primary"]{{
      background:{mint}!important;color:{ink}!important}}
    .stApp input,.stApp textarea,
    .stApp [data-baseweb="select"]>div{{
      background:{paper}!important;color:{ink}!important;
      -webkit-text-fill-color:{ink}!important}}
    .stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,
    .stApp [data-testid="stCaptionContainer"]{{color:{ink}!important}}
    .retro-kicker{{font:700 .7rem ui-monospace,monospace;letter-spacing:.13em;
      color:{secondary};margin:0 0 .3rem}}
    .retro-topline{{display:flex;align-items:center;gap:.6rem;
      padding:.6rem .85rem;margin:.5rem 0 1rem;border:1px solid {frame};
      border-radius:7px;background:{mint};font:700 .8rem ui-monospace,monospace}}
    .retro-dots{{color:#bc7974;letter-spacing:.2em}}
    .retro-timeline{{background:{paper};border:1px solid {frame};
      border-radius:9px;padding:.8rem 1rem;margin:.7rem 0 1rem;
      box-shadow:3px 3px 0 {frame}30}}
    .retro-time{{font:700 .72rem ui-monospace,monospace;color:{secondary};
      margin:0 0 .45rem}}
    .retro-task{{border-left:6px solid var(--task-accent);
      border-radius:5px;padding:.8rem .9rem;background:var(--task-bg);
      color:#2d2a2b;box-shadow:1px 2px 0 #33333324}}
    .retro-task-title{{font-weight:750;font-size:.98rem}}
    .retro-task-meta{{font-size:.76rem;color:#55545a;margin-top:.25rem}}
    .retro-empty{{padding:1.5rem 1rem;background:{paper};
      border:1px dashed {frame};border-radius:10px;color:{secondary}}}
    @media(max-width:700px){{
      .block-container{{padding:.85rem .8rem 6.5rem!important}}
      .retro-timeline{{padding:.7rem}}
      .stApp h1{{font-size:2rem}}
    }}
    @media(prefers-reduced-motion:reduce){{
      .stApp *{{transition:none!important;animation:none!important}}
    }}
    </style>"""


def apply(dark: bool = False) -> None:
    st.markdown(css(dark), unsafe_allow_html=True)


def topbar(label: str = "my_day.exe") -> None:
    import html
    st.markdown(
        '<div class="retro-topline"><span class="retro-dots">● ● ●</span>'
        '<span>▣ ' + html.escape(label) + '</span></div>',
        unsafe_allow_html=True,
    )
