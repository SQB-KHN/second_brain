"""Phase 2B pure freshness tests with synthetic strings and bytes only."""
import unittest

from tools.embedding_freshness import (
    SCHEMA_VERSION, classify_embedding, source_fingerprint, vector_fingerprint
)


class FreshnessContractTests(unittest.TestCase):
    def setUp(self):
        self.source = source_fingerprint("Title: Synthetic\\n\\nBody")
        self.vector = vector_fingerprint(b"synthetic-vector")
        self.entry = {
            "schema_version": SCHEMA_VERSION,
            "source_sha256": self.source,
            "embedding_model": "synthetic-model",
            "embedding_dimensions": 3,
            "vector_sha256": self.vector,
        }

    def test_matching_provenance_is_current(self):
        self.assertEqual(classify_embedding(self.entry, source_sha256=self.source,
                         model="synthetic-model", vector_sha256=self.vector, dimensions=3), "current")

    def test_edited_text_is_stale(self):
        self.assertEqual(classify_embedding(self.entry, source_sha256=source_fingerprint("edited"),
                         model="synthetic-model", vector_sha256=self.vector), "stale")

    def test_model_changed_is_stale(self):
        self.assertEqual(classify_embedding(self.entry, source_sha256=self.source,
                         model="new-model", vector_sha256=self.vector), "stale")

    def test_vector_changed_is_stale(self):
        self.assertEqual(classify_embedding(self.entry, source_sha256=self.source,
                         model="synthetic-model", vector_sha256=vector_fingerprint(b"other")), "stale")

    def test_missing_vector_is_missing(self):
        self.assertEqual(classify_embedding(self.entry, source_sha256=self.source,
                         model="synthetic-model", vector_sha256=None), "missing")

    def test_missing_entry_is_missing(self):
        self.assertEqual(classify_embedding(None, source_sha256=self.source,
                         model="synthetic-model", vector_sha256=self.vector), "missing")

    def test_legacy_metadata_unknown(self):
        self.assertEqual(classify_embedding({"path": "vectors/a.npy"},
                         source_sha256=self.source, model="synthetic-model",
                         vector_sha256=self.vector), "legacy_unknown")

    def test_corrupt_dimensions_detected(self):
        self.assertEqual(classify_embedding(self.entry, source_sha256=self.source,
                         model="synthetic-model", vector_sha256=self.vector,
                         dimensions=7), "stale")

    def test_malformed_record_unknown(self):
        bad = dict(self.entry, vector_sha256="not-a-hash")
        self.assertEqual(classify_embedding(bad, source_sha256=self.source,
                         model="synthetic-model", vector_sha256=self.vector), "legacy_unknown")

    def test_fingerprint_deterministic_and_sensitive(self):
        self.assertEqual(source_fingerprint("x"), source_fingerprint("x"))
        self.assertNotEqual(source_fingerprint("x"), source_fingerprint("x "))


if __name__ == "__main__":
    unittest.main()
