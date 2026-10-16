"""Only temp files and artificial notes; no external API calls."""
from dataclasses import dataclass
from pathlib import Path
import tempfile
import unittest

import numpy as np
from tools.embedding_freshness import source_fingerprint, vector_fingerprint
from tools.verified_vectors import select_verified_vectors


@dataclass
class Note:
    id: str = "synthetic"
    embed_text: str = "synthetic payload"
    wiki_path: str = "data/wiki/resources/synthetic.md"


class VerifiedVectorsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vector_dir = Path(self.tmp.name)
        self.vector = self.vector_dir / "synthetic.npy"
        np.save(self.vector, np.array([1., 2.], dtype=np.float32))
        self.entry = {
            "schema_version": 1, "wiki_path": Note.wiki_path,
            "path": self.vector.as_posix(),
            "source_sha256": source_fingerprint(Note.embed_text),
            "embedding_model": "model-a",
            "vector_sha256": vector_fingerprint(self.vector.read_bytes()),
            "embedding_dimensions": 2,
        }

    def choose(self, notes=None, index=None, model="model-a"):
        return select_verified_vectors(
            [Note()] if notes is None else notes,
            {"synthetic": self.entry} if index is None else index,
            self.vector_dir, model)

    def test_verified_only(self):
        chosen, counts = self.choose()
        self.assertEqual(set(chosen), {"synthetic"})
        self.assertEqual(counts, {})

    def test_repo_relative_index_path_accepted(self):
        self.entry["path"] = "data/embeddings/synthetic.npy"
        chosen, counts = self.choose()
        self.assertEqual(set(chosen), {"synthetic"})
        self.assertEqual(counts, {})

    def test_arbitrary_index_path_rejected(self):
        self.entry["path"] = "../private/synthetic.npy"
        chosen, counts = self.choose()
        self.assertFalse(chosen)
        self.assertEqual(counts["unknown"], 1)

    def test_changed_note_rejected(self):
        chosen, counts = self.choose(notes=[Note(embed_text="edited")])
        self.assertFalse(chosen)
        self.assertEqual(counts["stale"], 1)

    def test_model_change_rejected(self):
        chosen, counts = self.choose(model="model-b")
        self.assertFalse(chosen)
        self.assertEqual(counts["stale"], 1)

    def test_legacy_rejected_without_deletion(self):
        initial = self.vector.read_bytes()
        chosen, counts = self.choose(index={"synthetic": {"path": self.vector.as_posix(),
                                                    "wiki_path": Note.wiki_path}})
        self.assertFalse(chosen)
        self.assertEqual(counts["legacy_unknown"], 1)
        self.assertEqual(self.vector.read_bytes(), initial)

    def test_corrupted_vector_rejected_without_deletion(self):
        self.vector.write_bytes(b"broken")
        chosen, _ = self.choose()
        self.assertFalse(chosen)
        self.assertTrue(self.vector.exists())

    def test_missing_vector_rejected(self):
        self.vector.unlink()
        chosen, counts = self.choose()
        self.assertFalse(chosen)
        self.assertEqual(counts["missing"], 1)

    def test_duplicate_ids_rejected(self):
        chosen, counts = self.choose(notes=[Note(), Note()])
        self.assertEqual(len(chosen), 1)
        self.assertEqual(counts["unknown"], 1)

    def test_untrusted_note_id_rejected(self):
        chosen, counts = self.choose(notes=[Note(id="../escape")])
        self.assertFalse(chosen)
        self.assertEqual(counts["unknown"], 1)


if __name__ == "__main__":
    unittest.main()
