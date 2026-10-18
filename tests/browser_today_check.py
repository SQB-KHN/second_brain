"""Real Chromium planner acceptance in an isolated synthetic workspace."""
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from playwright.sync_api import sync_playwright, expect


REPO = Path(__file__).resolve().parents[1]
# This header must render as text, never as an automatically fetched image.



def main():
    with tempfile.TemporaryDirectory(prefix='secondself-browser-datasets-') as temporary:
        root = Path(temporary).resolve()
        for source in REPO.glob('*.py'):
            shutil.copyfile(source,root/source.name)
        shutil.copytree(REPO/'tools',root/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(REPO/'demo',root/'demo')
        with socket.socket() as listener:
            listener.bind(('127.0.0.1',0))
            port = listener.getsockname()[1]
        env = dict(os.environ, DEPLOY_MODE='false', SECONDSELF_DATA_DIR=str(root/'workspace'), PYTHON_DOTENV_DISABLED='1', OPENAI_API_KEY='', XAI_API_KEY='', GROQ_API_KEY='')
        log = (root/'server.log').open('w')
        process = subprocess.Popen([sys.executable,'-m','streamlit','run','app.py','--server.headless=true','--server.address=127.0.0.1',f'--server.port={port}','--browser.gatherUsageStats=false'],cwd=root,env=env,stdout=log,stderr=log)
        try:
            url = f'http://127.0.0.1:{port}'
            for _ in range(150):
                try:
                    urllib.request.urlopen(url+'/_stcore/health',timeout=1)
                    break
                except OSError:
                    if process.poll() is not None:
                        raise RuntimeError((root/'server.log').read_text())
                    time.sleep(.1)
            with sync_playwright() as p:
                chrome = os.environ.get('SECONDSELF_TEST_CHROME','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
                browser = p.chromium.launch(executable_path=chrome if Path(chrome).exists() else p.chromium.executable_path,headless=True)
                page = browser.new_page()
                page.set_default_timeout(30000)
                # No outbound requests, including AI/provider requests, allowed by the browser.
                leaked_requests = []
                page.on('request', lambda request: leaked_requests.append(request.url) if 'example.invalid' in request.url else None)
                page.route('**/*',lambda route: route.continue_() if route.request.url.startswith(url) else route.abort())
                page.goto(url)
                expect(page.get_by_role('heading', name='Today', exact=True)).to_be_visible()
                page.get_by_label('Task title', exact=True).fill('Synthetic focus <script>alert(1)</script>')
                page.get_by_label('Project label', exact=True).fill('Synthetic project')
                page.get_by_label('Details', exact=True).fill('![tracker](https://example.invalid/leak) <script>alert(1)</script>')
                page.get_by_role('button', name='Save task', exact=True).click()
                expect(page.get_by_text('Synthetic focus <script>alert(1)</script> · todo · P2', exact=True).first).to_be_visible()
                page.get_by_role('button', name='Edit / reschedule', exact=True).first.click()
                expect(page.get_by_role('heading',name='Edit task',exact=True)).to_be_visible()
                page.get_by_text('Schedule this task', exact=True).click()
                import datetime
                day = datetime.date.today().isoformat()
                page.get_by_label('Scheduled start', exact=True).fill(day+'T09:00')
                page.get_by_label('Scheduled end', exact=True).fill(day+'T10:00')
                page.get_by_role('button', name='Save task', exact=True).click()
                try:
                    expect(page.locator('.today-rail')).to_have_count(1)
                except Exception:
                    print(page.locator('body').inner_text())
                    raise
                page.get_by_role('button', name='Complete', exact=True).first.click()
                expect(page.get_by_text('Synthetic focus <script>alert(1)</script> · done · P2', exact=True)).to_be_visible()
                page.reload()
                expect(page.get_by_text('Synthetic focus <script>alert(1)</script> · done · P2', exact=True)).to_be_visible()
                page.get_by_label('Task title', exact=True).fill('Synthetic due only')
                page.get_by_label('Due date (optional)', exact=True).fill(day)
                page.get_by_role('button',name='Save task',exact=True).click()
                expect(page.get_by_text('Synthetic due only · todo · P2',exact=True)).to_be_visible()
                expect(page.locator('.today-rail')).to_have_count(1)
                page.get_by_label('Planning view', exact=True).click()
                page.keyboard.press('ArrowDown')
                page.keyboard.press('Enter')
                expect(page.get_by_role('heading',name='Week timeline',exact=True)).to_be_visible()
                for width in (1440, 390):
                    page.set_viewport_size(dict(width=width,height=900))
                    if width == 390:
                        page.wait_for_timeout(600)
                        collapse = page.get_by_test_id('stSidebarCollapseButton').get_by_role('button')
                        if collapse.is_visible():
                            collapse.press('Enter')
                            page.wait_for_timeout(400)
                        expect(page.locator('.st-key-today-mobile').get_by_role('button',name='Research',exact=True)).to_be_visible()
                    expect(page.get_by_role('heading',name='Today',exact=True)).to_be_visible()
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                    page.screenshot(path=f'/tmp/secondself-today-{width}.png',full_page=True)
                page.set_viewport_size(dict(width=1440,height=900))
                expand = page.get_by_test_id('stSidebarCollapsedControl').get_by_role('button')
                if expand.is_visible():
                    expand.press('Enter')
                    page.wait_for_timeout(400)
                page.locator('.st-key-today-desktop').get_by_role('button',name='Research',exact=True).click()
                expect(page.get_by_role('heading',name='Ask',exact=True)).to_be_visible()
                sidebar = page.get_by_test_id('stSidebar')
                sidebar.get_by_text('Today',exact=True).click()
                page.locator('.st-key-today-desktop').get_by_role('button',name='Analytics',exact=True).click()
                expect(page.get_by_role('heading',name='Analyse',exact=True)).to_be_visible()
                for view in ('Home','Capture','Ask','Explore','Library','Insights','Datasets','Analyse','Today'):
                    sidebar.get_by_text(view,exact=True).click()
                    expect(page.get_by_role('heading',name=view,exact=True)).to_be_visible()
                    assert page.get_by_test_id('stException').count() == 0
                assert not leaked_requests
                browser.close()
        finally:
            process.terminate()
            process.wait(timeout=10)
            log.close()
    print('Today browser acceptance passed (synthetic only).')


if __name__ == '__main__':
    main()
