"""Real Chromium dataset workflow, synthetic isolated local workspace only."""
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
from test_datasets import CSV, workbook, parquet

REPO = Path(__file__).resolve().parents[1]
# This header must render as text, never as an automatically fetched image.
CSV = CSV.replace(b'group', b'![tracker](https://example.invalid/leak)')


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
                sidebar = page.get_by_test_id('stSidebar')
                sidebar.get_by_text('Datasets',exact=True).click()
                def send(name,content):
                    remove = page.get_by_role('button',name='Remove file',exact=False)
                    if remove.count():
                        remove.first.click()
                        page.wait_for_timeout(350)
                    page.locator('input[type=file]').set_input_files(dict(name=name,mimeType='application/octet-stream',buffer=content))
                    expect(page.get_by_label('Dataset name',exact=True)).to_have_value(name.rsplit('.',1)[0])
                    page.wait_for_timeout(500)
                def preview():
                    page.get_by_role('button',name='Preview dataset',exact=True).click()
                    expect(page.get_by_role('heading',name='Import preview',exact=True)).to_be_visible()
                def confirm(message):
                    page.get_by_role('button',name='Confirm dataset import',exact=True).click()
                    expect(page.get_by_text(message,exact=True)).to_be_visible()
                send('bad.csv',b'a\n\xff')
                page.get_by_role('button',name='Preview dataset',exact=True).click()
                expect(page.get_by_text('Unsupported CSV encoding.',exact=False)).to_be_visible()
                send('bad.parquet',b'not parquet')
                page.get_by_role('button',name='Preview dataset',exact=True).click()
                expect(page.get_by_text('Invalid Parquet signature.',exact=True)).to_be_visible()
                send('bad.xlsx',b'not a workbook')
                expect(page.get_by_text('Corrupt or unsupported file.',exact=False)).to_be_visible()
                remove = page.get_by_role('button',name='Remove file',exact=False)
                if remove.count():
                    remove.first.click()
                    page.wait_for_timeout(500)
                page.locator('input[type=file]').set_input_files(dict(name='oversized.csv',mimeType='text/csv',buffer=b'x'*(10*1024*1024+1)))
                expect(page.get_by_text('File exceeds 10 MiB.',exact=False)).to_be_visible()
                send('study.csv',CSV)
                preview()
                expect(page.get_by_role('button',name='Confirm dataset import')).to_be_visible()
                assert list((root/'workspace/datasets').glob('*.source')) == []
                confirm('Imported: study · version 1')
                confirm('Already imported: study · version 1')
                page.get_by_role('button',name='Compute and save statistics',exact=True).click()
                expect(page.get_by_text('Reproducible statistics saved locally.',exact=True)).to_be_visible()
                dictionary = page.get_by_test_id('stExpander').filter(has=page.locator('summary').get_by_text('number',exact=True))
                dictionary.locator('summary').click()
                dictionary.get_by_label('Description',exact=True).fill('Synthetic mass')
                dictionary.get_by_label('Units',exact=True).fill('kg')
                page.get_by_role('button',name='Save data dictionary',exact=True).click()
                expect(page.get_by_text('Data dictionary saved; original bytes unchanged.',exact=True)).to_be_visible()
                send('study.csv',CSV.replace(b'1,A',b'2,A'))
                preview()
                confirm('Imported: study · version 2')
                send('book.xlsx',workbook())
                expect(page.get_by_role('button',name='Preview dataset')).to_be_disabled()
                page.get_by_label('Worksheet',exact=True).click()
                page.get_by_role('option',name='Second',exact=True).click()
                preview()
                expect(page.get_by_text('Workbook: book.xlsx · Sheet: Second',exact=True)).to_be_visible()
                confirm('Imported: book · version 1')
                send('arrow.parquet',parquet())
                preview()
                confirm('Imported: arrow · version 1')
                page.get_by_role('button',name='Reprofile selected version',exact=True).click()
                expect(page.get_by_text('Profile refreshed from verified original bytes.',exact=True)).to_be_visible()
                page.reload()
                sidebar.get_by_text('Datasets',exact=True).click()
                expect(page.get_by_text('Dataset inventory',exact=True)).to_be_visible()
                assert not leaked_requests, leaked_requests
                for view in ('Home','Capture','Ask','Explore','Library','Insights','Datasets'):
                    sidebar.get_by_text(view,exact=True).click()
                    expect(page.get_by_role('heading',name=view,exact=True)).to_be_visible()
                    assert page.get_by_test_id('stException').count()==0
                page.set_viewport_size(dict(width=390,height=844))
                assert page.get_by_test_id('stException').count()==0
                browser.close()
            # Verify durable records and metadata outside the browser, still only synthetic data.
            check = subprocess.run([sys.executable,'-c',"from dataset_registry import Registry; r=Registry(); rows=r.inventory(); assert len(rows)==4; study=next(x for x in rows if x['name']=='study' and x['version']==1); assert r.get(study['id'])['dictionary']['number']['units']=='kg'; assert r.saved_statistics(study['id']); assert len(list(r.root.glob('*.source')))==4"],cwd=root,env=env,capture_output=True,text=True)
            if check.returncode:
                raise AssertionError(check.stderr)
            print('PASS browser datasets: invalid encoding, preview/confirmation, CSV/XLSX/Parquet, deduplication, versions, sheet selection, dictionary, statistics, reprofile, reload, all workspace views, mobile viewport')
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            log.close()


if __name__=='__main__':
    main()
