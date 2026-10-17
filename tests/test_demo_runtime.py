"""Integration checks run copied application code with synthetic data and no secrets."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
APP_DEPS = all(importlib.util.find_spec(m) for m in ('streamlit', 'openai', 'dotenv', 'numpy', 'yaml', 'requests', 'bs4'))


@unittest.skipUnless(APP_DEPS, 'Install requirements.txt to run isolated app integration tests')
class DemoRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='secondself-runtime-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        for path in REPO.glob('*.py'):
            shutil.copyfile(path, self.root / path.name)
        shutil.copytree(REPO / 'tools', self.root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copyfile(REPO / 'prepare_deploy.sh', self.root / 'prepare_deploy.sh')
        self.env = {'PATH': os.environ.get('PATH', ''), 'HOME': str(self.root),
                    'DEPLOY_MODE': 'true', 'OPENAI_API_KEY': 'synthetic-no-network-key',
                    'GROQ_API_KEY': '', 'PYTHON_DOTENV_DISABLED': '1'}
        self.manifest = self.root / 'manifest.json'
        self.manifest.write_text('{"version":1,"notes":[]}')

    def run_python(self, code):
        result = subprocess.run([sys.executable, '-c', code], cwd=self.root, env=self.env,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def publish(self):
        self.run_python("import prepare_deploy as p; p.publish(p.ROOT/'source', p.ROOT/'demo', p.ROOT/'manifest.json')")

    def add_sample(self):
        note = self.root / 'source/wiki/resources/synthetic.md'
        note.parent.mkdir(parents=True)
        note.write_text('---\nid: synthetic\npara: resources\nsummary: Synthetic summary\ntags: [synthetic]\nlinks: []\n---\n# Synthetic Visible Note\nSynthetic body\n')
        self.manifest.write_text(json.dumps({'version': 1, 'notes': [{'path': 'resources/synthetic.md', 'sha256': hashlib.sha256(note.read_bytes()).hexdigest()}]}))

    def test_empty_and_approved_streamlit_app(self):
        for expected in (0, 1):
            if expected:
                self.add_sample()
            self.publish()
            with self.subTest(nodes=expected):
                self.run_python('''
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import ask
from render_graph import render_graph_html
at = AppTest.from_file('app.py', default_timeout=30).run()
assert not at.exception, [e.message for e in at.exception]
assert next(m.value for m in at.metric if m.label == 'Notes') == str(EXPECTED)
assert ('Synthetic Visible Note' in render_graph_html()) == bool(EXPECTED)
for view in ('Capture', 'Explore', 'Library', 'Ask', 'Insights', 'Home'):
    at.radio[0].set_value(view).run()
    assert not at.exception
at.radio[0].set_value('Ask').run()
# No API/embedding work should occur on this path.
with patch.object(ask, 'embed', side_effect=AssertionError('API must not be used')), patch.object(ask, 'get_llm_client', side_effect=AssertionError('API must not be used')):
    result = ask.ask('Synthetic question')
    assert result.sources == [] and 'Brain not indexed' in result.answer
    at.chat_input[0].set_value('Synthetic question').run()
    assert not at.exception
    assert any('Brain not indexed' in str(m.value) for m in at.markdown)
'''.replace('EXPECTED', str(expected)))

    def test_local_drafts_save_retry_and_navigation(self):
        self.env.update(DEPLOY_MODE='false', SECONDSELF_DATA_DIR=str(self.root/'workspace'), EMBEDDING_PROVIDER='ollama')
        self.run_python("""
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import workspace, refresh

def publish(root):
    return refresh.refresh(root, embedder=lambda text: [1., 0., 0.])

def button(at, label):
    return next(b for b in at.button if b.label == label)

at = AppTest.from_file('app.py', default_timeout=30).run()
at.radio[0].set_value('Capture').run()
at.text_input(key='draft_title').set_value('Synthetic UI title').run()
at.text_area(key='draft_body').set_value('Synthetic body').run()
button(at, 'Keep session draft').click().run()
at.radio[0].set_value('Home').run()
at.radio[0].set_value('Capture').run()
assert at.text_area(key='draft_body').value == 'Synthetic body'
with patch.object(workspace, 'refresh', side_effect=ValueError('offline')):
    button(at, 'Save & Index').click().run()
assert not at.exception
assert len(workspace.notes()) == 1
assert at.error
with patch.object(workspace, 'refresh', side_effect=publish):
    button(at, 'Retry indexing').click().run()
assert not at.exception
assert at.success
assert at.text_area(key='draft_body').value == ''
assert len(workspace.notes()) == 1
at.radio[0].set_value('Explore').run()
assert not at.exception
at.radio[0].set_value('Library').run()
assert not at.exception
assert at.text_input(key='edit_' + workspace.notes()[0].id + '_title').value == 'Synthetic UI title'
""")

    def test_renderer_script_payload_roundtrips_without_html_injection(self):
        self.run_python(r'''
import json
from html.parser import HTMLParser
from render_graph import render_graph_html
payload = '</script><script>window.SYNTHETIC_MARKER=1</script><img src=x onerror="window.SYNTHETIC_MARKER=2">&\u2028\u2029'
payload = payload.replace('\\u2028', '\u2028').replace('\\u2029', '\u2029')
graph = {'nodes':[{'id':'synthetic', 'label':payload, 'summary':payload, 'tags':[payload], 'para':'resources', 'path':payload, 'created':payload}], 'edges':[], 'meta':{'generated_at':payload}}
html = render_graph_html(graph)
assert '</script><script>window.SYNTHETIC_MARKER' not in html
assert '<img src=x' not in html
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.scripts = []
    def handle_starttag(self, tag, attrs):
        if tag == 'script': self.scripts.append(attrs)
p = Parser(); p.feed(html)
assert len(p.scripts) == 3, p.scripts
assignment = html.split('window.__SECONDSELF_GRAPH__ = ', 1)[1].split(';\n  </script>', 1)[0]
decoded = json.loads(assignment)
assert decoded['nodes'][0]['raw']['summary'] == payload
assert decoded['meta']['generated_at'] == payload
assert '<' not in assignment and '>' not in assignment and '&' not in assignment
assert '<' not in decoded['nodes'][0]['title']
''')

    def test_shell_legacy_flag_and_explicit_demo_html(self):
        self.add_sample()
        # The real shell wrapper still uses its documented local .venv interface.
        (self.root / '.venv/bin').mkdir(parents=True)
        (self.root / '.venv/bin/python').symlink_to(Path(sys.executable).absolute())
        result = subprocess.run(['bash', 'prepare_deploy.sh', '--source', str(self.root/'source'), '--dest', str(self.root/'demo'), '--manifest', str(self.manifest), '--skip-rebuild'], cwd=self.root, env=self.env, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('deprecated', result.stderr)
        self.assertFalse((self.root / 'graph.html').exists())
        self.run_python("import render_graph as r; r.main(['--graph-file','demo/graph.json','--output','demo-preview.html'])")
        self.assertIn('Synthetic Visible Note', (self.root / 'demo-preview.html').read_text())
        self.assertFalse((self.root / 'graph.html').exists())


if __name__ == '__main__':
    unittest.main()
