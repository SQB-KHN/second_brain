"""Optional real-Chrome check. Requires playwright and Chrome; uses synthetic data only.

Run: python tests/browser_demo_check.py
No personal browser profile is opened. Only the pinned vis-network script is fetched.
"""
import json
import os
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright

from test_demo_runtime import DemoRuntimeTests


def main():
    fixture = DemoRuntimeTests('test_empty_and_approved_streamlit_app')
    fixture.setUp()
    try:
        chrome = os.environ.get('SECONDSELF_TEST_CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        if not Path(chrome).is_file():
            raise RuntimeError('Set SECONDSELF_TEST_CHROME to a Chrome executable')
        # Use the application's actual pinned graph library, not a rendering mock.
        response = requests.get('https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js', timeout=30)
        response.raise_for_status()
        library = response.text + '''\n;const OriginalNetwork = vis.Network;
vis.Network = function(...args) { const network = new OriginalNetwork(...args); window.__testNetwork = network; return network; };
'''
        def make_html(name):
            fixture.run_python("from render_graph import render_graph_html; from pathlib import Path; Path(" + repr(name) + ").write_text(render_graph_html())")
            return (fixture.root / name).as_uri()
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=chrome, headless=True, env=fixture.env)
            context = browser.new_context()
            def route_request(route):
                url = route.request.url
                if url.startswith('file:'):
                    route.continue_()
                elif url == 'https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js':
                    route.fulfill(status=200, content_type='application/javascript', body=library)
                elif url.endswith('/styles/vis-network.min.css'):
                    route.fulfill(status=200, content_type='text/css', body='')
                else:
                    route.abort()
            context.route('**/*', route_request)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            fixture.publish()
            page.goto(make_html('empty.html'))
            page.locator('#empty-panel').wait_for(state='visible')
            assert page.locator('#network').is_hidden()
            print('PASS empty graph browser state')
            fixture.add_sample()
            fixture.publish()
            page.goto(make_html('sample.html'))
            page.locator('#network canvas').wait_for(state='visible')
            page.wait_for_function('window.__testNetwork && window.__testNetwork.body.data.nodes.length === 1')
            page.locator('.filter-btn[data-para="archives"]').click()
            assert page.evaluate('window.__testNetwork.body.data.nodes.length') == 0
            page.locator('.filter-btn[data-para="resources"]').click()
            # Stop physics before calculating coordinates; GitHub's Linux Chromium
            # may otherwise move the node between positioning and the click.
            page.evaluate('window.__testNetwork.stopSimulation(); window.__testNetwork.fit({animation:false})')
            point = page.evaluate('window.__testNetwork.canvasToDOM(window.__testNetwork.getPositions(["synthetic"])["synthetic"])')
            # canvasToDOM is relative to the vis-network container, not necessarily
            # the nested canvas element (their origins can differ across platforms).
            hit = page.evaluate('(p) => window.__testNetwork.getNodeAt(p)', point)
            if hit != 'synthetic':
                diagnostics = page.evaluate("""(p) => {
                    const n = window.__testNetwork;
                    const outer = document.querySelector('#network').getBoundingClientRect();
                    const canvas = document.querySelector('#network canvas').getBoundingClientRect();
                    return {point:p, hit:n.getNodeAt(p), position:n.getPositions(['synthetic']),
                        scale:n.getScale(), viewPosition:n.getViewPosition(),
                        container:{x:outer.x,y:outer.y,width:outer.width,height:outer.height},
                        canvas:{x:canvas.x,y:canvas.y,width:canvas.width,height:canvas.height},
                        devicePixelRatio:window.devicePixelRatio,
                        physicalNodes:n.body.data.nodes.getIds()};
                }""", point)
                print('GRAPH_CLICK_DIAGNOSTICS', json.dumps(diagnostics), flush=True)
                page.screenshot(path='/tmp/secondself-graph-click-failure.png')
            assert hit == 'synthetic', 'Synthetic node did not resolve at calculated DOM point'
            box = page.locator('#network').bounding_box()
            page.mouse.click(box['x'] + point['x'], box['y'] + point['y'])
            page.locator('#detail-content h2').wait_for(state='visible')
            assert page.locator('#detail-content h2').inner_text() == 'Synthetic Visible Note'
            print('PASS approved note canvas, filters, and physical node click')
            # Renderer must remain safe for arbitrary graphs, even independently
            # of the publication syntax restrictions.
            fixture.run_python('''
from render_graph import render_graph_html
from pathlib import Path
payload = '</script><script>window.SYNTHETIC_MARKER=1</script><img src=x onerror="window.SYNTHETIC_MARKER=2">'
graph = {'nodes':[{'id':'synthetic','label':'Synthetic payload','summary':payload,'tags':[payload],'para':'resources'}], 'edges':[], 'meta':{'generated_at':payload}}
Path('hostile.html').write_text(render_graph_html(graph))
''')
            page.goto((fixture.root / 'hostile.html').as_uri())
            page.locator('#network canvas').wait_for(state='visible')
            # Stop physics before calculating coordinates; GitHub's Linux Chromium
            # may otherwise move the node between positioning and the click.
            page.evaluate('window.__testNetwork.stopSimulation(); window.__testNetwork.fit({animation:false})')
            point = page.evaluate('window.__testNetwork.canvasToDOM(window.__testNetwork.getPositions(["synthetic"])["synthetic"])')
            # canvasToDOM is relative to the vis-network container, not necessarily
            # the nested canvas element (their origins can differ across platforms).
            assert page.evaluate('(p) => window.__testNetwork.getNodeAt(p)', point) == 'synthetic', 'Synthetic node did not resolve at calculated DOM point'
            box = page.locator('#network').bounding_box()
            page.mouse.move(box['x'] + point['x'], box['y'] + point['y'])
            page.wait_for_timeout(500)  # Actual tooltip delay is 120 ms.
            page.mouse.click(box['x'] + point['x'], box['y'] + point['y'])
            page.locator('#detail-content').wait_for(state='visible')
            assert page.evaluate('window.SYNTHETIC_MARKER === undefined')
            assert page.locator('img').count() == 0
            assert not errors, errors
            print('PASS closing-script payload, metadata, tooltip, and detail rendering; no injected image/script execution')
            browser.close()
    finally:
        fixture.doCleanups()


if __name__ == '__main__':
    main()
