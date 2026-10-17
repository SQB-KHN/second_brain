"""Real Chromium Analyse acceptance using a temporary synthetic workspace only."""
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


def main():
    with tempfile.TemporaryDirectory(prefix='secondself-browser-analysis-') as temporary:
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
                page.set_default_timeout(45000)
                expect.set_options(timeout=45000)
                # No outbound requests, including AI/provider requests, allowed by the browser.
                leaked_requests = []
                page.on('request', lambda request: leaked_requests.append(request.url) if 'example.invalid' in request.url else None)
                page.route('**/*',lambda route: route.continue_() if route.request.url.startswith(url) else route.abort())
                page.goto(url)
                sidebar = page.get_by_test_id('stSidebar')
                sidebar.get_by_text('Analyse',exact=True).click()
                expect(page.get_by_text('Register a dataset in Datasets to begin analysis.',exact=True)).to_be_visible()
                sidebar.get_by_text('Datasets',exact=True).click()
                source = b'x,y\n1,2\n2,5\n3,4\n4,8\n5,6\n6,11\n7,9\n8,13\n9,12\n10,16\n,2\nNA,3\n'
                source = b'\n'.join(line+(b',![tracker](https://example.invalid/leak)' if i==0 else b',A') for i,line in enumerate(source.splitlines()))+b'\n'
                page.locator('input[type=file]').set_input_files(dict(name='synthetic.csv',mimeType='text/csv',buffer=source))
                page.get_by_role('button',name='Preview dataset',exact=True).click()
                page.get_by_role('button',name='Confirm dataset import',exact=True).click()
                expect(page.get_by_text('Imported: synthetic · version 1',exact=True)).to_be_visible()
                page.get_by_role('button',name='Analyse this version',exact=True).click()
                expect(page.get_by_role('heading',name='Analyse',exact=True)).to_be_visible()
                run = page.get_by_role('button',name='Run and save analysis',exact=True)
                expect(run).to_be_disabled()
                for method in ('Exploratory statistics','Pearson correlation','Spearman correlation','Paired t-test','OLS regression'):
                    page.wait_for_timeout(700)
                    if method != 'Exploratory statistics':
                        page.get_by_role('combobox',name='Analysis method',exact=True).click()
                        page.get_by_role('combobox',name='Analysis method',exact=True).press('ArrowDown')
                        page.get_by_role('option',name=method,exact=True).click()
                    expect(run).to_be_disabled()
                    page.get_by_role('button',name='Preview analysis and exclusions',exact=True).click()
                    expect(page.get_by_role('heading',name='Analysis preview',exact=True)).to_be_visible()
                    expect(run).to_be_enabled()
                    run.click()
                    expect(page.get_by_text('Immutable analysis run saved locally.',exact=True)).to_be_visible()
                    expect(page.get_by_role('heading',name='Diagnostics and exclusions',exact=True)).to_be_visible()
                    expect(page.get_by_role('heading',name='Charts',exact=True)).to_be_visible()
                    expect(page.get_by_role('button',name='Download as PNG',exact=True).first).to_be_visible()
                    assert page.get_by_test_id('stException').count()==0
                with page.expect_download() as downloaded:
                    page.get_by_role('button',name='Download analysis JSON',exact=True).click()
                import json
                manifest = json.loads(Path(downloaded.value.path()).read_text())
                assert manifest['observations']['used']==10
                assert manifest['observations']['excluded']==2
                assert manifest['dataset']['version']==1
                assert manifest['software']['scipy'] and manifest['software']['statsmodels']
                with page.expect_download() as downloaded:
                    page.get_by_role('button',name='Download analysis CSV',exact=True).click()
                assert '/output_hash' in Path(downloaded.value.path()).read_text()
                page.get_by_role('combobox',name='Analysis method',exact=True).click()
                page.get_by_role('combobox',name='Analysis method',exact=True).press('ArrowDown')
                page.get_by_role('option',name='Binary logistic regression',exact=True).click()
                expect(run).to_be_disabled()
                page.get_by_role('button',name='Preview analysis and exclusions',exact=True).click()
                expect(run).to_be_enabled()
                run.click()
                expect(page.get_by_text('Binary logistic outcome must contain exactly numeric 0 and 1; event is 1.',exact=True)).to_be_visible()
                page.reload()
                sidebar.get_by_text('Analyse',exact=True).click()
                expect(page.get_by_label('Saved analysis run',exact=True)).to_be_visible()
                for view in ('Home','Capture','Ask','Explore','Library','Insights','Datasets','Analyse'):
                    sidebar.get_by_text(view,exact=True).click()
                    expect(page.get_by_role('heading',name=view,exact=True)).to_be_visible()
                    assert page.get_by_test_id('stException').count()==0
                page.set_viewport_size(dict(width=390,height=844))
                assert not leaked_requests, leaked_requests
                browser.close()
            check = subprocess.run([sys.executable,'-c',"from dataset_registry import Registry; import statistical_engine as e; r=Registry(); rows=r.inventory(); assert len(rows)==1; runs=e.history(r,rows[0]['id']); assert len(runs)==5; assert len(list(r.root.glob('*.source')))==1"],cwd=root,env=env,capture_output=True,text=True)
            assert check.returncode==0, check.stderr
            print('PASS browser Analyse: Dataset Manager handoff, preview, exclusions, five procedures, invalid outcome, charts, JSON/CSV downloads, persistent history, navigation, mobile, no outbound requests')
        finally:
            if sys.exc_info()[0]:
                print((root/'server.log').read_text()[-5000:])
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            log.close()


if __name__=='__main__':
    main()
