"""Synthetic workspace saves exercise the real verified publication pipeline."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
import config
import ask
import refresh
import workspace as w


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, value in [('DATA_DIR', self.root), ('DEPLOY_MODE', False),
                            ('ENABLE_CAPTURE', True), ('ENABLE_REFRESH_BRAIN', True)]:
            p = patch.object(w, name, value)
            p.start()
            self.addCleanup(p.stop)

    def test_save_edit_index_graph_and_retrieval(self):
        def publish(root):
            plan = refresh.inventory(root)[3]
            return refresh.refresh(root, allow_api=True, approve_plan=plan['approval_digest'], price_per_million=0, max_cost=0, embedder=lambda text: [1., 0., 0.])
        with patch.object(w, 'refresh', side_effect=publish):
            path = w.save_note('Synthetic title', 'A useful thought', 'resources', 'work, ideas')
            w.index_notes()
            self.assertEqual(len(refresh.active_graph(self.root)['nodes']), 1)
            note = w.notes()[0]
            before = path.read_text()
            w.save_note('Edited title', 'Changed knowledge', note.para, 'work', path=path, expected=before)
            self.assertEqual(refresh.active_graph(self.root)['nodes'], [])
            w.index_notes()
            self.assertEqual(refresh.active_graph(self.root)['nodes'][0]['label'], 'Edited title')
            with patch.object(config, 'DATA_DIR', self.root), patch.object(ask, 'embed', return_value=np.array([1., 0., 0.])), patch.object(ask, 'get_llm_client', return_value=(object(), 'fake')), patch.object(ask, 'call_rag_llm', return_value=('Answer', 1)):
                self.assertEqual(ask.ask('question').sources[0].id, note.id)
            with self.assertRaisesRegex(ValueError, 'changed'):
                w.save_note('Conflict', 'Text', note.para, '', path=path, expected=before)

    def test_demo_and_path_guards(self):
        with patch.object(w, 'DEPLOY_MODE', True):
            with self.assertRaises(ValueError):
                w.save_note('Title', 'Body', 'resources', '')
            with self.assertRaises(ValueError):
                w.index_notes()
        with self.assertRaises(ValueError):
            w.note_path(self.root / 'outside.md')
        with self.assertRaises(ValueError):
            w.save_note('', 'Body', 'resources', '')
        with patch.object(w, 'ENABLE_REFRESH_BRAIN', False):
            with self.assertRaises(ValueError):
                w.save_note('Title', 'Body', 'resources', '')
        outside = self.root / 'outside'
        outside.mkdir()
        (self.root / 'wiki').mkdir(exist_ok=True)
        (self.root / 'wiki' / 'resources').symlink_to(outside)
        with self.assertRaises(ValueError):
            w.save_note('Title', 'Body', 'resources', '')

    def test_provider_failure_preserves_saved_note(self):
        path = w.save_note('Keep me', 'Draft body', 'resources', '')
        with patch.object(w, 'refresh', side_effect=ValueError('offline')):
            with self.assertRaises(ValueError):
                w.index_notes()
        self.assertTrue(path.exists())
        self.assertEqual(len(w.notes()), 1)
