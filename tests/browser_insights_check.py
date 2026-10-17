"""Synthetic local Ollama + real Chrome acceptance. No cloud calls.
Run: .venv/bin/python tests/browser_insights_check.py
Requires running Ollama/nomic-embed-text and Chrome (SECONDSELF_TEST_CHROME).
"""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from playwright.sync_api import sync_playwright
from test_demo_runtime import DemoRuntimeTests


def main():
    fixture = DemoRuntimeTests('test_empty_and_approved_streamlit_app')
    fixture.setUp()
    server = None
    try:
        fixture.env.update(DEPLOY_MODE='false', SECONDSELF_DATA_DIR=str(fixture.root / 'workspace'),
                           EMBEDDING_PROVIDER='ollama', EMBEDDING_MODEL='nomic-embed-text',
                           XAI_API_KEY='', OPENAI_API_KEY='', GROQ_API_KEY='')
        fixture.run_python('''
from pathlib import Path
import config, refresh
bodies = ['Atlas | retention | 2026-01-01: 30 days',
          'Atlas | retention | 2026-01-01: 90 days',
          'Atlas | owner | 2026-01-01: Mira', 'Synthetic metadata gap',
          'Atlas | review | 2026-01-01: monthly']
for i, body in enumerate(bodies):
    path = config.DATA_DIR / 'wiki/resources' / f'{i}.md'
    path.write_text(f'---\\nid: s{i}\\npara: resources\\nsummary: Synthetic\\n---\\n# Synthetic {i}\\n{body}\\n')
refresh.refresh(config.DATA_DIR)
''')
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        def start():
            return subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.headless=true',
                f'--server.port={port}', '--browser.gatherUsageStats=false'], cwd=fixture.root,
                env=fixture.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        server = start()
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=os.environ.get('SECONDSELF_TEST_CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'), headless=True)
            page = browser.new_page()
            def open_app():
                for _ in range(60):
                    try:
                        page.goto(f'http://127.0.0.1:{port}', timeout=2000)
                        page.get_by_text('YOUR KNOWLEDGE, CONNECTED', exact=True).wait_for(timeout=5000)
                        return
                    except Exception:
                        time.sleep(.5)
                raise AssertionError('Streamlit failed to start')
            def view(name):
                page.locator('[data-testid="stSidebar"]').get_by_text(name, exact=True).click()
                page.get_by_role('heading', name=name, exact=True).wait_for()
            open_app()
            view('Insights')
            page.get_by_role('button', name='Generate Insights', exact=True).click()
            page.get_by_text('Indexed note lacks tags, creation date', exact=True).first.wait_for()
            page.get_by_text('Synthetic 0 · s0', exact=True).first.click()
            page.get_by_text('Atlas | retention | 2026-01-01: 30 days', exact=False).first.wait_for()
            statuses = page.get_by_role('combobox', name='Review status', exact=True)
            statuses.nth(0).click()
            page.keyboard.press('ArrowDown')
            page.keyboard.press('Enter')
            page.get_by_role('button', name='Save review', exact=True).nth(0).click()
            page.get_by_text('Saved status: Useful', exact=True).wait_for()
            statuses.nth(1).click()
            page.keyboard.press('ArrowDown')
            page.keyboard.press('ArrowDown')
            page.keyboard.press('Enter')
            page.get_by_role('button', name='Save review', exact=True).nth(1).click()
            page.get_by_text('Saved status: Dismissed', exact=True).wait_for()
            fixture.run_python("import insights, config; assert {'Useful', 'Dismissed'}.issubset({r['status'] for r in insights.load(config.DATA_DIR).values()})")
            server.terminate()
            server.wait(timeout=10)
            server = start()
            open_app()
            view('Insights')
            page.get_by_role('combobox', name='Review status', exact=True).first.wait_for()
            page.get_by_text('Saved status: Useful', exact=True).wait_for()
            page.get_by_text('Saved status: Dismissed', exact=True).wait_for()
            fixture.run_python("import config; p=config.DATA_DIR/'wiki/resources/0.md'; p.write_text(p.read_text()+'Edited synthetic evidence\\n')")
            page.reload()
            view('Insights')
            page.get_by_text('Stale insight: generation or source evidence changed. Regenerate before relying on it.', exact=True).first.wait_for()
            for name in ('Ask', 'Capture', 'Library', 'Explore', 'Home'):
                view(name)
                assert page.locator('[data-testid="stException"]').count() == 0
            view('Insights')
            page.set_viewport_size({'width': 390, 'height': 844})
            assert page.locator('[data-testid="stException"]').count() == 0
            browser.close()
        print('PASS real Ollama refresh; Insights generate/evidence/review/restart/stale; all workspace views; mobile viewport')
    finally:
        if server:
            server.terminate()
            server.wait(timeout=10)
        fixture.tearDown()


if __name__ == '__main__':
    main()
