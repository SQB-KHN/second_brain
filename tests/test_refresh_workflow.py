"""Complete local workflow with synthetic notes and fake provider responses."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock

import numpy as np
import ask
import capture
import classify
import config
import render_graph
import refresh as r


class RefreshWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for para in config.PARA_FOLDERS:
            (self.root / 'wiki' / para).mkdir(parents=True)
        (self.root / 'raw').mkdir()
        self.provider = Mock(return_value=[1., 0., 0.])

    def note(self, id='a', body='Alpha', links='[]'):
        path = self.root / 'wiki/resources' / (id + '.md')
        path.write_text(f'---\nid: {id}\npara: resources\nsummary: Synthetic\nlinks: {links}\n---\n# {id}\n{body}\n')
        return path

    def update(self, **kwargs):
        plan = r.inventory(self.root)[3]
        options = dict(allow_api=True, approve_plan=plan['approval_digest'],
                       price_per_million=0.02, max_cost=1., embedder=self.provider)
        options.update(kwargs)
        return r.refresh(self.root, **options)

    def assert_consumers(self, ids):
        notes, vectors, excluded = r.verified_active_vectors(self.root)
        self.assertFalse(excluded)
        self.assertEqual(set(vectors), set(ids))
        graph = r.active_graph(self.root)
        self.assertEqual({n['id'] for n in graph['nodes']}, set(ids))
        graph_path = self.root / 'graph.json'
        with (patch.object(config, 'DATA_DIR', self.root),
              patch.object(config, 'DEPLOY_MODE', False),
              patch.object(render_graph, 'GRAPH_FILE', graph_path)):
            self.assertEqual(render_graph.load_graph(graph_path), graph)
        with (patch.object(config, 'DATA_DIR', self.root),
              patch.object(ask, 'embed', return_value=np.array([1., 0., 0.])),
              patch.object(ask, 'get_llm_client', return_value=(object(), 'fake')),
              patch.object(ask, 'call_rag_llm', return_value=('Synthetic answer', 1))):
            answer = ask.ask('Synthetic question', top_k=20)
        self.assertEqual({s.id for s in answer.sources}, set(ids))
        return graph

    def test_capture_edit_rename_delete_refresh_ask_graph(self):
        record = capture.capture_text('Synthetic captured knowledge')
        with (patch.object(capture, 'RAW_DIR', self.root / 'raw'),
              patch.object(capture, 'ROOT', self.root),
              patch.object(capture, 'META_FILE', self.root / 'meta.json'),
              patch.object(capture, 'LEGACY_META_FILE', self.root / 'raw/meta.json')):
            raw = capture.write_capture(record)
        raw_capture = classify.load_raw_capture(raw)
        result = classify.ClassificationResult('Captured', 'resources', ['synthetic'], 'Synthetic capture')
        with (patch.object(classify, 'WIKI_DIR', self.root / 'wiki'),
              patch.object(classify, 'ROOT', self.root)):
            captured = classify.write_wiki_note(raw_capture, result, {})
        cid = record['id']
        a = self.note(links=f'[{cid}]')
        before = {p: p.read_bytes() for p in self.root.rglob('*.md')}
        self.update()
        graph = self.assert_consumers(['a', cid])
        self.assertTrue(any(e['type'] == 'explicit' for e in graph['edges']))
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*.md')})
        self.provider.reset_mock()
        a.write_text(a.read_text() + 'Edited knowledge\n')
        self.assertEqual(r.verified_active_vectors(self.root)[1], {})
        self.assertEqual(r.active_graph(self.root)['nodes'], [])
        with (patch.object(config, 'DATA_DIR', self.root),
              patch.object(ask, 'embed', side_effect=AssertionError('No network on stale generation'))):
            self.assertEqual(ask.ask('question').sources, [])
        self.update()
        self.provider.assert_called_once()
        self.assert_consumers(['a', cid])
        renamed = a.with_name('renamed.md')
        a.rename(renamed)
        self.provider.reset_mock()
        self.assertEqual(r.inventory(self.root)[3]['renamed'], ['a'])
        r.refresh(self.root)
        self.provider.assert_not_called()
        self.assert_consumers(['a', cid])
        captured.unlink()
        self.assertEqual(r.inventory(self.root)[3]['deleted'], [cid])
        r.refresh(self.root)
        graph = self.assert_consumers(['a'])
        self.assertEqual(graph['edges'], [])
        self.assertIn(cid, renamed.read_text())  # Manual link retained, orphan not emitted.
        self.assertTrue(raw.exists())

    def test_approval_budget_and_obsolete_plan(self):
        path = self.note()
        plan = r.inventory(self.root, provider='openai')[3]
        for options in ({}, {'allow_api': True}, {'allow_api': True, 'approve_plan': plan['approval_digest']}):
            with self.assertRaises(ValueError):
                r.refresh(self.root, provider='openai', embedder=self.provider, **options)
        with self.assertRaises(ValueError):
            r.refresh(self.root, provider='openai', allow_api=True, approve_plan=plan['approval_digest'], price_per_million=1, max_cost=0, embedder=self.provider)
        path.write_text(path.read_text() + 'Changed\n')
        with self.assertRaises(ValueError):
            self.update(approve_plan=plan['approval_digest'])
        self.provider.assert_not_called()

    def test_legacy_is_reembedded_not_certified(self):
        self.note()
        emb = self.root / 'embeddings'
        emb.mkdir()
        np.save(emb / 'a.npy', np.array([0., 1., 0.]))
        (emb / 'index.json').write_text(json.dumps({'a': {'wiki_path': 'wiki/resources/a.md', 'path': str(emb / 'a.npy')}}))
        before = {p: p.read_bytes() for p in emb.iterdir()}
        self.assertEqual(r.inventory(self.root)[3]['legacy_unknown'], ['a'])
        with self.assertRaises(ValueError):
            self.update()
        self.provider.assert_not_called()
        self.update(migrate_legacy=True)
        self.provider.assert_called_once()
        self.assertEqual(before, {p: p.read_bytes() for p in emb.iterdir()})
        self.assert_consumers(['a'])

    def test_api_failure_and_publish_failure_preserve_previous(self):
        path = self.note()
        self.update()
        pointer = self.root / 'knowledge/current.json'
        previous = pointer.read_bytes()
        path.write_text(path.read_text() + 'Changed\n')
        self.provider.side_effect = RuntimeError('Provider failed')
        with self.assertRaises(RuntimeError):
            self.update()
        self.assertEqual(pointer.read_bytes(), previous)
        self.provider.side_effect = None
        with patch.object(r.os, 'replace', side_effect=OSError('Disk failure')):
            with self.assertRaises(OSError):
                self.update()
        self.assertEqual(pointer.read_bytes(), previous)
        self.assertTrue(r.current(self.root))
        self.assertGreater(len(list((self.root / 'knowledge/generations').iterdir())), 1)

    def test_mid_refresh_edit_blocks_publication(self):
        path = self.note()
        def mutate(text):
            path.write_text(path.read_text() + 'Concurrent edit\n')
            return [1., 0., 0.]
        with self.assertRaisesRegex(ValueError, 'changed during refresh'):
            self.update(embedder=mutate)
        self.assertFalse((self.root / 'knowledge/current.json').exists())

    def test_corrupt_artifacts_and_model_change(self):
        self.note()
        self.update()
        directory, _ = r.current(self.root)
        vector = directory / 'a.npy'
        vector.write_bytes(b'corrupt')
        self.assertEqual(r.verified_active_vectors(self.root)[1], {})
        self.update()
        self.assert_consumers(['a'])
        self.assertEqual(r.verified_active_vectors(self.root, model='changed')[1], {})
        directory, _ = r.current(self.root)
        (directory / 'relationships.json').write_text('[]')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            r.current(self.root)

    def test_empty_deleted_corpus_and_lock(self):
        path = self.note()
        self.update()
        path.unlink()
        r.refresh(self.root)
        self.assertEqual(r.active_graph(self.root)['nodes'], [])
        with r.writer_lock(self.root / 'knowledge'):
            with self.assertRaisesRegex(ValueError, 'Another refresh'):
                r.refresh(self.root)

    def test_invalid_duplicate_and_unsafe_notes(self):
        a = self.note()
        b = a.with_name('duplicate.md')
        b.write_bytes(a.read_bytes())
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            r.inventory(self.root)
        b.unlink()
        a.write_text('invalid')
        with self.assertRaisesRegex(ValueError, 'Invalid note'):
            r.inventory(self.root)
        a.write_text('---\nid: ../escape\npara: resources\nsummary: Synthetic\n---\nBody')
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            r.inventory(self.root)

    def test_restore_rejects_stale_and_recovers_corrupt_pointer(self):
        path = self.note()
        original = path.read_bytes()
        self.update()
        generation = r.current(self.root)[0].name
        pointer = self.root / 'knowledge/current.json'
        path.write_bytes(original + b'Edited\n')
        with self.assertRaisesRegex(ValueError, 'does not match'):
            r.restore(self.root, generation)
        path.write_bytes(original)
        pointer.write_bytes(b'broken pointer')
        r.restore(self.root, generation)
        self.assert_consumers(['a'])

    def test_invalid_provider_vectors_preserve_pointer(self):
        path = self.note()
        self.update()
        pointer = self.root / 'knowledge/current.json'
        before = pointer.read_bytes()
        path.write_text(path.read_text() + 'Edit\n')
        for vector in ([float('nan')], [0., 0.], [[1.]], [1., 2.]):
            with self.subTest(vector=vector):
                # The last response changes dimensions, which is valid for a full
                # corpus replacement; use another unchanged note to catch mixing.
                self.note('b')
                if vector == [1., 2.]:
                    self.provider.return_value = [1., 0., 0.]
                    self.update()
                    before = pointer.read_bytes()
                    path.write_text(path.read_text() + 'Edit again\n')
                self.provider.return_value = vector
                with self.assertRaises(ValueError):
                    self.update()
                self.assertEqual(pointer.read_bytes(), before)

    def test_provider_contract_and_model_rebuild(self):
        self.note()
        import link
        client = Mock()
        client.with_options.return_value = client
        client.embeddings.create.return_value = Mock(data=[Mock(embedding=[1., 0., 0.])])
        with patch.object(link, 'require_embedding_api_key', return_value=client):
            self.update(embedder=None, provider='openai', approve_plan=r.inventory(self.root, provider='openai')[3]['approval_digest'])
        client.with_options.assert_called_once_with(max_retries=0)
        client.embeddings.create.assert_called_once_with(
            model=config.EMBEDDING_MODEL, input=r.scan(self.root)[0][0].embed_text)
        changed = r.inventory(self.root, 'replacement-model')[3]
        self.assertEqual(changed['affected'], ['a'])
        r.refresh(self.root, model='replacement-model', allow_api=True,
                  approve_plan=changed['approval_digest'], price_per_million=0.02,
                  max_cost=1, embedder=self.provider)
        self.assertEqual(set(r.verified_active_vectors(self.root, 'replacement-model')[1]), {'a'})
        self.assertFalse(r.verified_active_vectors(self.root)[1])

    def test_local_legacy_graph_is_not_a_verified_generation(self):
        path = self.root / 'graph.json'
        path.write_text(json.dumps({'nodes': [{'id': 'stale'}], 'edges': [], 'meta': {}}))
        with (patch.object(config, 'DATA_DIR', self.root),
              patch.object(config, 'DEPLOY_MODE', False),
              patch.object(render_graph, 'GRAPH_FILE', path)):
            graph = render_graph.load_graph(path)
        self.assertEqual(graph['nodes'], [])
        self.assertEqual(graph['meta']['error'], 'missing_generation')

    def test_status_and_dry_run_do_not_mutate(self):
        self.note()
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch('builtins.print'):
            self.assertEqual(r.main(['status', '--data-dir', str(self.root)]), 0)
            self.assertEqual(r.main(['dry-run', '--data-dir', str(self.root), '--price-per-million', '0.02']), 0)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        self.provider.assert_not_called()


if __name__ == '__main__':
    unittest.main()
