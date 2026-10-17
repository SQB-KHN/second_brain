"""Real browser upload workflow, isolated synthetic workspace and mocked Ollama.

Run: PYTHONPATH=.:tests .venv/bin/python tests/browser_document_check.py
Requires Playwright and Chrome (or SECONDSELF_TEST_CHROME).
"""
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from playwright.sync_api import sync_playwright
from test_document_ingestion import pdf, xlsx

REPO = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='secondself-browser-docs-') as temporary:
        root = Path(temporary)
        for path in REPO.glob('*.py'):
            shutil.copyfile(path, root / path.name)
        shutil.copytree(REPO / 'tools', root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        (root / 'browser_app.py').write_text('''
import runpy
from pathlib import Path
import refresh, ask

def embed(text):
    if Path('offline').exists():
        raise RuntimeError('Synthetic offline')
    return [1., 0., 0.]
refresh.create_embedder = lambda *args: embed
ask.embed = lambda text: __import__('numpy').array([1., 0., 0.])
ask.get_llm_client = lambda: (object(), 'synthetic')
ask.call_rag_llm = lambda *args: ('Synthetic consented answer', 1)
# Equal synthetic vectors tie; retrieve every fixture segment for citation checks.
if not hasattr(ask, '_browser_original_ask'):
    ask._browser_original_ask = ask.ask
ask.ask = lambda question, **kwargs: ask._browser_original_ask(question, top_k=20, **kwargs)
runpy.run_path('app.py', run_name='__main__')
''')
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            port = listener.getsockname()[1]
        env = dict(os.environ, DEPLOY_MODE='false', SECONDSELF_DATA_DIR=str(root / 'data'), PYTHON_DOTENV_DISABLED='1', EMBEDDING_PROVIDER='ollama', OLLAMA_BASE_URL='http://127.0.0.1:11434', XAI_API_KEY='synthetic', OPENAI_API_KEY='', GROQ_API_KEY='')
        log = (root / 'server.log').open('w')
        process = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'browser_app.py', '--server.headless=true', '--server.address=127.0.0.1', f'--server.port={port}', '--browser.gatherUsageStats=false'], cwd=root, env=env, stdout=log, stderr=log)
        try:
            url = f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    urllib.request.urlopen(url + '/_stcore/health', timeout=1)
                    break
                except OSError:
                    if process.poll() is not None:
                        raise RuntimeError((root / 'server.log').read_text())
                    time.sleep(.1)
            with sync_playwright() as p:
                chrome = os.environ.get('SECONDSELF_TEST_CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
                browser = p.chromium.launch(executable_path=chrome if Path(chrome).exists() else p.chromium.executable_path, headless=True)
                page = browser.new_page()
                page.set_default_timeout(15000)
                page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(url) or route.request.url.startswith('ws:') else route.abort())
                page.goto(url)
                page.get_by_text('Capture', exact=True).first.click()
                def open_import():
                    label = page.get_by_text('Import document', exact=True)
                    if not label.evaluate('(el) => el.closest("details").open'):
                        label.click()
                open_import()
                upload = page.locator('input[type=file]').first
                def send(name, content, mime):
                    page.wait_for_timeout(1000)
                    remove = page.get_by_role('button', name='Remove file', exact=False)
                    if remove.count():
                        remove.first.click()
                        page.wait_for_timeout(500)
                    upload.set_input_files({'name': name, 'mimeType': mime, 'buffer': content})
                    page.wait_for_timeout(500)
                    open_import()
                send('bad.pdf', b'not pdf', 'application/pdf')
                page.get_by_text('Invalid PDF signature.', exact=True).wait_for()
                assert not list((root / 'data/imports').glob('*/source'))
                send('report.pdf', pdf(), 'application/pdf')
                page.get_by_text('report.pdf · page 2', exact=True).wait_for()
                page.get_by_role('button', name='Save & Index document', exact=True).click()
                page.get_by_text('Document indexed (identical reuploads reuse the existing import).', exact=True).wait_for()
                page.get_by_role('button', name='Save & Index document', exact=True).click()
                page.get_by_text('Document indexed (identical reuploads reuse the existing import).', exact=True).wait_for()
                assert len(list((root / 'data/imports').glob('*/source'))) == 1
                send('budget.xlsx', xlsx(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                page.get_by_text('budget.xlsx · sheet Plans, rows 1–1', exact=True).wait_for()
                (root / 'offline').touch()
                page.get_by_role('button', name='Save & Index document', exact=True).click()
                page.get_by_text('Indexing failed. Check local Ollama and refresh status, then retry.', exact=True).wait_for()
                (root / 'offline').unlink()
                page.get_by_role('button', name='Retry import', exact=True).click()
                page.wait_for_timeout(500)
                open_import()
                page.get_by_text('budget.xlsx · indexed', exact=False).wait_for()
                send('table.csv', b'Name,Value\nSynthetic,42', 'text/csv')
                page.get_by_text('table.csv · sheet CSV, rows 2–2', exact=True).wait_for()
                page.get_by_role('button', name='Save & Index document', exact=True).click()
                page.get_by_text('Document indexed (identical reuploads reuse the existing import).', exact=True).wait_for()
                # Exercise the merged features against the same imported evidence.
                send('facts.csv', b'Fact\nAtlas | retention | 2026-01-01: 30 days\nAtlas | retention | 2026-01-01: 90 days\nAtlas | owner | 2026-01-01: Mira', 'text/csv')
                page.get_by_text('facts.csv · sheet CSV, rows 4–4', exact=True).wait_for()
                page.get_by_role('button', name='Save & Index document', exact=True).click()
                page.get_by_text('Document indexed (identical reuploads reuse the existing import).', exact=True).wait_for()
                sidebar = page.locator('[data-testid="stSidebar"]')
                sidebar.get_by_text('Library', exact=True).click()
                page.get_by_text('Imported source evidence is read-only. Reimport a changed document as a new version.', exact=True).wait_for()
                assert page.get_by_role('combobox', name='Open note', exact=True).count() == 1
                sidebar.get_by_text('Explore', exact=True).click()
                page.get_by_role('combobox', name='Read node details', exact=True).wait_for()
                assert any('indexed notes' in text for text in page.locator('[data-testid="stCaptionContainer"]').all_text_contents())
                sidebar.get_by_text('Insights', exact=True).click()
                page.get_by_role('button', name='Generate Insights', exact=True).click()
                page.get_by_text('Potential contradiction', exact=True).first.wait_for()
                page.get_by_text('Hypothesis: differing stated retention for atlas on 2026-01-01', exact=True).first.wait_for()
                page.get_by_text('Saved status: New', exact=True).first.wait_for()
                page.get_by_text('Ask', exact=True).first.click()
                page.get_by_placeholder('Ask anything about your knowledge…').fill('What synthetic evidence?')
                page.get_by_placeholder('Ask anything about your knowledge…').press('Enter')
                page.get_by_text('Document sources retrieved locally.', exact=False).wait_for()
                page.get_by_text('Allow sending retrieved document excerpts and my question to the configured external LLM (Grok/xAI, OpenAI or Groq); charges may apply.', exact=True).click()
                page.wait_for_timeout(500)
                page.get_by_placeholder('Ask anything about your knowledge…').fill('Summarize synthetic evidence')
                page.get_by_placeholder('Ask anything about your knowledge…').press('Enter')
                page.get_by_text('Synthetic consented answer', exact=True).wait_for()
                page.get_by_text('report.pdf · page 1', exact=True).first.wait_for()
                assert not page.locator('[data-testid=stException]').count()
                browser.close()
                print('PASS browser: malformed PDF, page/sheet/row previews, PDF/CSV/XLSX upload, duplicate, failed indexing/retry, Ask provenance and consent, imported Library/Graph/Insights evidence')
        except Exception:
            print((root / 'server.log').read_text()[-4000:])
            raise
        finally:
            process.terminate()
            process.wait(timeout=15)
            log.close()


if __name__ == '__main__':
    main()
