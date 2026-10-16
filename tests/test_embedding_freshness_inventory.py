"""Synthetic-only Phase 2A tests; never open the user's knowledge corpus."""
import json
from pathlib import Path
import tempfile
import unittest

from tools.embedding_freshness_inventory import inspect_index


class EmbeddingIndexInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "index.json"

    def write(self, data):
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def test_absent_index_is_not_a_failure(self):
        self.assertFalse(inspect_index(self.path)["index_exists"])

    def test_legacy_entries_are_unknown_not_current(self):
        self.write({"one": {"path": "embeddings/one.npy", "updated": "yesterday"}})
        x = inspect_index(self.path)
        self.assertEqual(x["legacy_unknown"], 1)
        self.assertEqual(x["versioned_candidate"], 0)

    def test_versioned_fields_only_mark_candidate_not_fresh(self):
        self.write({"a": {"schema_version": 1, "path": "embeddings/a.npy",
                          "source_sha256": "abc", "embedding_model": "synthetic",
                          "vector_sha256": "def"}})
        x = inspect_index(self.path)
        self.assertEqual(x["versioned_candidate"], 1)
        self.assertEqual(x["schema_versions"], {"1": 1})

    def test_invalid_record_is_reported(self):
        self.write({"one": []})
        self.assertEqual(inspect_index(self.path)["invalid_entries"], 1)

    def test_non_object_index_rejected(self):
        self.write(["unexpected"])
        with self.assertRaises(ValueError):
            inspect_index(self.path)

    def test_invalid_json_rejected(self):
        self.path.write_text("{ invalid")
        with self.assertRaises(ValueError):
            inspect_index(self.path)

    def test_missing_vector_path_is_reported_without_opening_vector(self):
        self.write({"n": {"path": ""}})
        self.assertEqual(inspect_index(self.path)["missing_vector_paths"], 1)


if __name__ == "__main__":
    unittest.main()
