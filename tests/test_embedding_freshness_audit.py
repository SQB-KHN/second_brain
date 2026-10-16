"""Read-only synthetic fixture tests; never access actual SecondSelf data."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from tools.embedding_freshness_audit import audit, _embed_text
from tools.embedding_freshness import source_fingerprint, vector_fingerprint


class FreshnessAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.wiki = self.root / "data" / "wiki"
        self.notes = self.wiki / "resources"
        self.notes.mkdir(parents=True)
        self.emb = self.root / "data" / "embeddings"
        self.emb.mkdir()
        self.index = self.emb / "index.json"
        self.note = self.notes / "sample.md"
        self.note.write_text("---\nid: sample\npara: resources\ntitle: Sample\nsummary: Summary\ntags: [demo]\n---\nBody\n")
        self.index.write_text("{}")

    def test_missing(self):
        self.assertEqual(audit(self.wiki, self.index, "m")["missing"], 1)

    def test_legacy_unknown(self):
        self.index.write_text(json.dumps({"sample": {"path": "data/embeddings/sample.npy",
                                                      "wiki_path": "data/wiki/resources/sample.md"}}))
        self.assertEqual(audit(self.wiki, self.index, "m")["legacy_unknown"], 1)

    def test_current_and_mutated_source(self):
        id_, text = _embed_text(self.note)
        self.assertEqual(id_, "sample")
        vec = self.emb / "sample.npy"
        np.save(vec, np.array([1, 2, 3], dtype=np.float32))
        self.index.write_text(json.dumps({"sample": {
            "schema_version": 1, "wiki_path": "data/wiki/resources/sample.md",
            "path": "data/embeddings/sample.npy", "source_sha256": source_fingerprint(text),
            "embedding_model": "m", "vector_sha256": vector_fingerprint(vec.read_bytes()),
            "embedding_dimensions": 3}}))
        self.assertEqual(audit(self.wiki, self.index, "m")["current"], 1)
        self.note.write_text(self.note.read_text() + "Edited\n")
        self.assertEqual(audit(self.wiki, self.index, "m")["stale"], 1)
        self.assertEqual(audit(self.wiki, self.index, "other")["stale"], 1)

    def test_read_only(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        audit(self.wiki, self.index, "m")
        after = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_orphan_index(self):
        self.index.write_text(json.dumps({"deleted": {"path": "none"}}))
        self.assertEqual(audit(self.wiki, self.index, "m")["orphan_index_entries"], 1)


if __name__ == "__main__":
    unittest.main()
