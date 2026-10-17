"""Synthetic end-to-end provider integration; never contacts a real API."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import numpy as np
import ask
import config
import refresh
from tools import embedding_provider as provider


class OllamaIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.note = self.root / 'wiki/resources/a.md'
        self.note.parent.mkdir(parents=True)
        self.note.write_text('---\nid: a\npara: resources\nsummary: Synthetic\n---\n# Alpha\nSynthetic body\n')
        self.opener = Mock()
        def respond(request, timeout):
            self.requests.append(json.loads(request.data))
            self.assertEqual(request.full_url, 'http://localhost:11434/api/embed')
            self.assertEqual(timeout, 120)
            return io.BytesIO(json.dumps({'embeddings': [[1.] + [0.] * 767]}).encode())
        self.requests = []
        self.opener.open.side_effect = respond
        self.transport = patch.object(provider.urllib.request, 'build_opener', return_value=self.opener)
        self.transport.start()
        self.addCleanup(self.transport.stop)
        self.url = patch.object(provider, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.url.start()
        self.addCleanup(self.url.stop)

    def test_local_refresh_question_graph_reuse_and_restore(self):
        original = self.note.read_bytes()
        with patch('link.require_embedding_api_key', side_effect=AssertionError('No OpenAI')):
            refresh.refresh(self.root)
            generation, manifest = refresh.current(self.root)
            self.assertEqual(manifest['model'], 'ollama:nomic-embed-text')
            notes, vectors, excluded = refresh.verified_active_vectors(self.root)
            self.assertFalse(excluded)
            self.assertEqual(vectors['a'].shape, (768,))
            self.assertEqual(self.requests[0], {'model': 'nomic-embed-text', 'input': notes[0].embed_text, 'truncate': False})
            with (patch.object(config, 'DATA_DIR', self.root),
                  patch.object(ask, 'get_llm_client', return_value=(object(), 'synthetic')),
                  patch.object(ask, 'call_rag_llm', return_value=('Synthetic answer', 1))):
                self.assertEqual(ask.ask('Synthetic question').sources[0].id, 'a')
            self.assertEqual(self.requests[-1]['input'], 'Synthetic question')
            self.assertEqual(refresh.active_graph(self.root)['nodes'][0]['id'], 'a')
            count = len(self.requests)
            refresh.refresh(self.root)
            self.assertEqual(len(self.requests), count)
            refresh.restore(self.root, generation.name)
        self.assertEqual(self.note.read_bytes(), original)

    def test_provider_switch_never_reuses_equal_dimension_vectors(self):
        refresh.refresh(self.root)
        plan = refresh.inventory(self.root, provider='openai')[3]
        self.assertEqual(plan['affected'], ['a'])
        with self.assertRaisesRegex(ValueError, 'External embedding'):
            refresh.refresh(self.root, provider='openai')
        self.assertFalse(refresh.verified_active_vectors(self.root, provider='openai')[1])
        refresh.refresh(self.root, provider='openai', allow_api=True,
                        approve_plan=plan['approval_digest'], price_per_million=1,
                        max_cost=1, embedder=lambda text: [1.] + [0.] * 767)
        self.assertEqual(refresh.inventory(self.root)[3]['affected'], ['a'])
        self.assertFalse(refresh.verified_active_vectors(self.root)[1])
        refresh.refresh(self.root)
        self.assertTrue(refresh.verified_active_vectors(self.root)[1])

    def test_failure_preserves_pointer_and_stale_ask_does_not_embed(self):
        refresh.refresh(self.root)
        pointer = self.root / 'knowledge/current.json'
        before = pointer.read_bytes()
        self.note.write_bytes(self.note.read_bytes() + b'Changed\n')
        for payload in ({}, {'embeddings': []}, {'embeddings': [[0.]]},
                        {'embeddings': [['1']]}, {'embeddings': [[float('nan')]]}):
            self.opener.open.side_effect = lambda *a, **k: io.BytesIO(json.dumps(payload).encode())
            with self.assertRaises(ValueError):
                refresh.refresh(self.root)
            self.assertEqual(pointer.read_bytes(), before)
        with (patch.object(config, 'DATA_DIR', self.root),
              patch.object(ask, 'embed', side_effect=AssertionError('Stale'))):
            self.assertFalse(ask.ask('Synthetic question').sources)

    def test_nonlocal_endpoints_rejected_before_request(self):
        for url in ('https://example.com', 'http://192.168.1.2:11434',
                    'http://localhost:11434/redirect', 'http://user@localhost:11434'):
            with patch.object(provider, 'OLLAMA_BASE_URL', url):
                with self.assertRaisesRegex(ValueError, 'loopback'):
                    provider.create_embedder()
        self.opener.open.assert_not_called()

    def test_xai_is_optional_and_selected_with_key(self):
        with (patch.object(ask, 'XAI_API_KEY', 'synthetic'),
              patch.object(ask, 'OpenAI') as client):
            self.assertEqual(ask.get_llm_client()[1], config.XAI_LLM_MODEL)
            client.assert_called_once_with(api_key='synthetic', base_url='https://api.x.ai/v1')
