"""Regression guards for the presentation-only retro theme."""
from retro_studio_ui import css


def test_retro_theme_is_offline_and_preserves_controls():
    light = css(False)
    dark = css(True)
    assert '--retro-canvas' in light
    assert '--retro-task' not in light or '.retro-task' in light
    assert '.retro-task' in light
    assert 'focus-visible' not in light or 'outline' in light
    assert 'display:none' not in light
    assert 'pointer-events:none' not in light
    assert 'https://' not in light
    assert 'http://' not in light
    assert light != dark


def test_retro_restricts_style_to_presentation():
    theme = css(False)
    assert 'stForm' in theme
    assert 'stButton' in theme
    assert 'prefers-reduced-motion' in theme
