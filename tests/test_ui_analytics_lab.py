"""Regression checks for presentation-only Analytics Lab helpers."""
import unittest
from unittest.mock import patch, MagicMock

import ui_analytics_lab as lab


class AnalyticsLabTests(unittest.TestCase):
    def test_all_views_have_consistent_navigation_labels(self):
        from app import VIEWS
        self.assertEqual(len(VIEWS), 8)
        for name in VIEWS:
            self.assertIn(name, lab.nav_label(name))
            self.assertIn(name, lab.SUBTITLES)

    def test_theme_tokens_are_distinct_and_accessible_focus_exists(self):
        light, dark = lab.theme_css(False), lab.theme_css(True)
        self.assertNotEqual(light, dark)
        for css in (light, dark):
            self.assertIn("focus-visible", css)
            self.assertIn("lab-hero", css)
            self.assertIn("max-width:740px", css)

    def test_hero_and_section_escape_untrusted_text(self):
        with patch.object(lab.st, "markdown") as markdown:
            lab.hero("<img src=x onerror=alert(1)>")
            output = markdown.call_args.args[0]
            self.assertIn("&lt;img", output)
            self.assertNotIn("<img", output)
            lab.section("<script>")
            self.assertIn("&lt;script&gt;", markdown.call_args.args[0])

    def test_home_keeps_demo_safe_and_navigation_callbacks(self):
        note = MagicMock()
        note.title = "<unsafe>"
        note.summary = "Synthetic note"
        note.para = "resources"
        note.created = "2026-01-01"
        st = lab.st
        with patch.object(st, "columns", side_effect=lambda n, **k: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]), \
             patch.object(st, "button") as button, \
             patch.object(st, "markdown"), \
             patch.object(st, "metric"), \
             patch.object(st, "text") as text, \
             patch.object(st, "write"), \
             patch.object(st, "caption"), \
             patch.object(st, "container") as container:
            container.return_value.__enter__.return_value = MagicMock()
            lab.home([note], {"edge_count":2, "node_count":1, "generated_at":"synthetic"}, lambda _: None)
            self.assertTrue(button.called)
            text.assert_any_call("<unsafe>")
            self.assertFalse(any("Registry" in str(call) for call in text.call_args_list))


if __name__ == "__main__":
    unittest.main()
