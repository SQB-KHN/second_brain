"""Synthetic-only tests for Ask's fail-closed retrieval gate."""
import unittest
from unittest.mock import patch

import numpy as np
import ask


class AskFreshnessGateTests(unittest.TestCase):
    def test_nonempty_legacy_index_fails_closed_without_api_calls(self):
        with (patch.object(ask, "load_embedding_index", return_value={"x": {"path": "legacy.npy"}}),
              patch.object(ask, "scan_wiki_notes", return_value=[object()]),
              patch.object(ask, "select_verified_vectors", return_value=({}, {"legacy_unknown": 1})) as selector,
              patch.object(ask, "embed", side_effect=AssertionError("embedding API must not be used")),
              patch.object(ask, "get_llm_client", side_effect=AssertionError("LLM must not be used"))):
            outcome = ask.ask("synthetic question")
        self.assertEqual(outcome.sources, [])
        self.assertIn("No verified embeddings", outcome.answer)
        selector.assert_called_once()

    def test_empty_index_keeps_existing_not_indexed_message(self):
        with (patch.object(ask, "load_embedding_index", return_value={}),
              patch.object(ask, "embed", side_effect=AssertionError("API not expected"))):
            outcome = ask.ask("synthetic question")
        self.assertIn("Brain not indexed", outcome.answer)

    def test_no_notes_keeps_existing_message(self):
        with (patch.object(ask, "load_embedding_index", return_value={"x": {}}),
              patch.object(ask, "scan_wiki_notes", return_value=[]),
              patch.object(ask, "select_verified_vectors", side_effect=AssertionError("no notes"))):
            outcome = ask.ask("synthetic question")
        self.assertIn("No notes", outcome.answer)


if __name__ == "__main__":
    unittest.main()
