"""Synthetic analytical reference fixtures; no personal data or network."""
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import patch, Mock
import config
from dataset_registry import Registry
import statistical_engine as engine


class StatisticsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.demo = patch.object(config,'DEPLOY_MODE',False)
        self.demo.start()
        self.registry = Registry(Path(self.temp.name).resolve())

    def tearDown(self):
        self.demo.stop()
        self.temp.cleanup()

    def register(self, content):
        return self.registry.register('Synthetic','fixture.csv',content)[0]['id']

    def run_analysis(self, content, method, columns, **options):
        return engine.execute(self.registry,self.register(content),dict(method=method,columns=columns,**options))

    def test_exploratory_analytical_and_repeatability(self):
        source = b'x,y\n1,2\n2,5\n3,4\n4,8\n5,6\n'
        identity = self.register(source)
        p = dict(method='exploratory',columns=['x'])
        first = engine.execute(self.registry,identity,p)
        second = engine.execute(self.registry,identity,p)
        item = first['results']['x']
        self.assertEqual(item['mean'],3)
        self.assertEqual(item['median'],3)
        self.assertAlmostEqual(item['sd'],math.sqrt(2.5))
        self.assertAlmostEqual(item['mean_confidence_interval'][0],1.036756838522439)
        self.assertEqual(item['q25'],2)
        for key in ('results','diagnostics','observations','charts','software','parameters'):
            self.assertEqual(first[key],second[key])
        self.assertNotEqual(first['id'],second['id'])
        self.assertEqual(first['dataset']['sha256'],hashlib.sha256(source).hexdigest())
        self.assertEqual(self.registry.source(self.registry.get(identity)),source)
        self.assertEqual(len(engine.history(self.registry,identity)),2)
        self.assertEqual(json.loads(json.dumps(first)),first)

    def test_correlation_reference(self):
        csv = b'x,y\n-2,-2\n-1,-3\n0,3\n1,1\n2,6\n'
        pearson = self.run_analysis(csv,'pearson',['x','y'])['results']
        self.assertAlmostEqual(pearson['correlation'],math.sqrt(40/54))
        self.assertAlmostEqual(pearson['p_value'],0.06111416919489394)
        ranks = self.run_analysis(csv,'spearman',['x','y'])['results']
        self.assertAlmostEqual(ranks['correlation'],.8)
        self.assertIn('Approximate',ranks['ci_method'])

    def test_paired_reference(self):
        run = self.run_analysis(b'a,b\n2,1\n4,2\n6,3\n8,4\n10,5\n','paired_t',['a','b'])
        result = run['results']
        self.assertAlmostEqual(result['statistic'],3/math.sqrt(.5))
        self.assertAlmostEqual(result['p_value'],.0132355995636827)
        self.assertAlmostEqual(result['cohens_dz'],3/math.sqrt(2.5))
        self.assertEqual(result['df'],4)

    def test_independent_welch_and_pooled(self):
        csv = b'x,g\n1,A\n2,A\n3,A\n4,A\n5,A\n2,B\n4,B\n6,B\n8,B\n10,B\n'
        welch = self.run_analysis(csv,'independent_t',['x','g'])['results']
        self.assertAlmostEqual(welch['statistic'],-3/math.sqrt(2.5))
        self.assertAlmostEqual(welch['df'],100/17)
        self.assertAlmostEqual(welch['cohens_d'],-1.2)
        pooled = self.run_analysis(csv,'independent_t',['x','g'],equal_var=True)['results']
        self.assertEqual(pooled['df'],8)
        self.assertEqual(pooled['group_sizes'],[5,5])
        self.assertLess(welch['confidence_interval'][0],welch['mean_difference'])

    def test_chi_square_reference_and_sparse_warning(self):
        csv = b'a,b\n'+b'A,X\n'*10+b'A,Y\n'*20+b'B,X\n'*20+b'B,Y\n'*10
        result = self.run_analysis(csv,'chi_square',['a','b'])['results']
        self.assertAlmostEqual(result['statistic'],20/3)
        self.assertAlmostEqual(result['p_value'],.009823274507519247)
        self.assertAlmostEqual(result['cramers_v'],1/3)
        self.assertEqual(result['expected'],[[15,15],[15,15]])
        run = self.run_analysis(b'a,b\nA,X\nA,Y\nB,X\nB,Y\n','chi_square',['a','b'])
        self.assertEqual(run['diagnostics']['expected_cells_below_5'],4)
        self.assertTrue(any('Expected counts' in s for s in run['caveats']))

    def test_ols_analytical_reference(self):
        run = self.run_analysis(b'x,y\n-2,-2\n-1,-3\n0,3\n1,1\n2,6\n','ols',['y','x'])
        result = run['results']
        intercept,slope = result['coefficients']
        self.assertAlmostEqual(intercept['estimate'],1)
        self.assertAlmostEqual(slope['estimate'],2)
        self.assertAlmostEqual(slope['standard_error'],math.sqrt(14/30))
        self.assertAlmostEqual(intercept['standard_error'],math.sqrt(14/15))
        self.assertAlmostEqual(result['r_squared'],40/54)
        self.assertAlmostEqual(result['rmse'],math.sqrt(14/3))
        self.assertIn('breusch_pagan',run['diagnostics'])
        self.assertEqual(len(run['charts']),2)

    def test_logistic_analytical_reference(self):
        csv = b'x,y\n'+b'-1,0\n'*30+b'-1,1\n'*10+b'1,0\n'*10+b'1,1\n'*30
        run = self.run_analysis(csv,'logistic',['y','x'])
        result = run['results']
        intercept,slope = result['coefficients']
        self.assertAlmostEqual(intercept['estimate'],0)
        self.assertAlmostEqual(slope['estimate'],math.log(3))
        self.assertAlmostEqual(slope['standard_error'],math.sqrt(1/15))
        self.assertAlmostEqual(slope['odds_ratio'],3)
        self.assertAlmostEqual(result['log_likelihood'],60*math.log(.75)+20*math.log(.25))
        self.assertAlmostEqual(run['diagnostics']['brier_score'],.1875)
        self.assertTrue(run['diagnostics']['converged'])

    def test_preview_exclusions_and_no_persistence(self):
        identity = self.register(b'x,y\n1,2\n2,3\n3,5\n,4\nNA,5\nNaN,\n')
        params = dict(method='pearson',columns=['x','y'])
        preview = engine.execute(self.registry,identity,params,preview=True)
        self.assertEqual(preview['observations']['used'],3)
        self.assertEqual(preview['observations']['excluded'],3)
        self.assertEqual(preview['observations']['exclusion_reasons'],dict(missing=2,invalid_numeric=1))
        self.assertEqual(preview['observations']['invalid_numeric_by_column']['x'],2)
        self.assertEqual(engine.history(self.registry,identity),[])
        run = engine.execute(self.registry,identity,params)
        self.assertEqual(run['observations'],preview['observations'])

    def test_invalid_assumptions_and_parameters(self):
        csv = b'x,y,z\n1,1,2\n2,2,4\n3,3,6\n4,4,8\n5,5,10\n'
        identity = self.register(csv)
        cases = [dict(method='exec',columns=['x']),dict(method='ols',columns=['y','x','z']),dict(method='logistic',columns=['y','x']),dict(method='paired_t',columns=['x','x']),dict(method='pearson',columns=['x','y'],confidence=float('nan')),dict(method='pearson',columns=['x','y'],formula='y~x'),dict(method='independent_t',columns=['x','y']),dict(method='ols',columns=['y','x'])]
        for params in cases:
            with self.subTest(params=params), self.assertRaises(ValueError):
                engine.execute(self.registry,identity,params)
        for method in ('exploratory','pearson','paired_t'):
            with self.assertRaises(ValueError):
                self.run_analysis(b'x,y\n1,1\n1,2\n1,3\n',method,['x'] if method=='exploratory' else ['x','y'])
        with self.assertRaises(ValueError):
            self.run_analysis(b'x,y\n-2,0\n-1,0\n1,1\n2,1\n3,1\n4,1\n','logistic',['y','x'])
        self.assertEqual(engine.history(self.registry,identity),[])

    def test_multicollinearity_caveats(self):
        csv = ('x,z,y\n'+'\n'.join(f'{i},{i+(.001 if i%2 else 0)},{2*i+(i%3)}' for i in range(40))+'\n').encode()
        run = self.run_analysis(csv,'ols',['y','x','z'])
        self.assertTrue(any('Multicollinearity' in s for s in run['caveats']))

    def test_atomic_recovery_immutable_integrity_pagination(self):
        identity = self.register(b'x\n1\n2\n3\n4\n')
        engine.history(self.registry,identity)
        with self.registry.connection() as db:
            db.execute("CREATE TRIGGER fail_analysis BEFORE INSERT ON analysis_runs BEGIN SELECT RAISE(ABORT,'synthetic'); END")
        with self.assertRaises(sqlite3.IntegrityError):
            engine.execute(self.registry,identity,dict(method='exploratory',columns=['x']))
        self.assertEqual(engine.history(self.registry,identity),[])
        with self.registry.connection() as db:
            db.execute('DROP TRIGGER fail_analysis')
        run = engine.execute(self.registry,identity,dict(method='exploratory',columns=['x']))
        with self.assertRaises(sqlite3.IntegrityError), self.registry.connection() as db:
            db.execute('UPDATE analysis_runs SET manifest=?',(engine.encode(run),))
        with self.assertRaises(sqlite3.IntegrityError), self.registry.connection() as db:
            db.execute('DELETE FROM analysis_runs')
        for i in range(21):
            copy = dict(run,id='synthetic-'+str(i))
            copy.pop('output_hash')
            copy['output_hash'] = engine.digest(copy)
            engine.save(self.registry,copy)
        self.assertEqual(len(engine.history(self.registry,identity)),20)
        self.assertEqual(len(engine.history(self.registry,identity,page=1)),2)
        with self.assertRaises(ValueError):
            engine.history(self.registry,identity,page=-1)
        with self.registry.connection() as db:
            db.execute('DROP TRIGGER analysis_no_update')
            copy['results'] = {}
            db.execute('UPDATE analysis_runs SET manifest=? WHERE id=?',(engine.encode(copy),run['id']))
        with self.assertRaisesRegex(ValueError,'integrity'):
            engine.history(self.registry,identity)

    def test_bounded_output_safe_exports_timeout(self):
        with self.assertRaisesRegex(ValueError,'1 MiB'):
            engine.save(self.registry,dict(value='x'*(engine.MAX_OUTPUT+1)))
        output = engine.export_csv(dict(label='=HYPERLINK("https://example.invalid")',other='\t=evil',negative=-2))
        self.assertIn("'=HYPERLINK",output)
        self.assertIn("'\t=evil",output)
        identity = self.register(b'x\n1\n2\n3\n')
        process = Mock()
        process.communicate.side_effect = [subprocess.TimeoutExpired('synthetic',30),(None,None)]
        with patch.object(self.registry,'inspect',return_value=self.registry.inspect(identity)), patch.object(engine.subprocess,'Popen',return_value=process), self.assertRaisesRegex(ValueError,'30 seconds'):
            engine.execute(self.registry,identity,dict(method='exploratory',columns=['x']))
        process.kill.assert_called_once()
        self.assertEqual(engine.history(self.registry,identity),[])

    def test_source_integrity_blocks_analysis(self):
        identity = self.register(b'x,y\n1,2\n2,3\n3,5\n')
        record = self.registry.get(identity)
        blob = self.registry._blob(record['sha256'])
        blob.chmod(0o600)
        blob.write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError,'integrity'):
            engine.execute(self.registry,identity,dict(method='pearson',columns=['x','y']))
        self.assertEqual(engine.history(self.registry,identity),[])

    def test_category_limits_boolean_numeric_and_inert_code(self):
        identity = self.register(b'x,g\n1,=cmd()\n2,__import__(os)\n3,=cmd()\n4,__import__(os)\n')
        run = engine.execute(self.registry,identity,dict(method='independent_t',columns=['x','g']))
        self.assertIn('str:=cmd()',run['results']['groups'])
        self.assertIn('str:__import__(os)',run['results']['groups'])
        csv = ('a,b\n'+'\n'.join(f'{i},'+str(i%2) for i in range(21))+'\n').encode()
        with self.assertRaisesRegex(ValueError,'2–20'):
            self.run_analysis(csv,'chi_square',['a','b'])
        counts = engine.calculate(dict(columns=['x'],rows=[[True],[False],[None],['NaN'],['1e101'],[1],[2],[3]]),dict(method='exploratory',columns=['x'],confidence=.95),preview=True)['observations']
        self.assertEqual(counts['used'],3)
        self.assertEqual(counts['exclusion_reasons'],dict(missing=1,invalid_numeric=4))

    def test_worker_credentials_are_not_inherited_and_output_is_bounded(self):
        identity = self.register(b'x\n1\n2\n3\n')
        real = engine.subprocess.Popen
        calls = []
        def launch(*args, **kwargs):
            calls.append(kwargs['env'])
            return real(*args, **kwargs)
        with patch.dict(engine.os.environ,{'OPENAI_API_KEY':'synthetic-private-value','CUSTOM_SECRET':'synthetic-private-value'}), patch.object(engine.subprocess,'Popen',side_effect=launch):
            result = engine.execute(self.registry,identity,dict(method='exploratory',columns=['x']))
        self.assertTrue(calls)
        self.assertTrue(all('OPENAI_API_KEY' not in env and 'CUSTOM_SECRET' not in env for env in calls))
        self.assertNotIn('synthetic-private-value',engine.encode(result))
        fake = Mock(returncode=0)
        def oversized(*args,**kwargs):
            kwargs['stdout'].write(b'x'*(engine.MAX_OUTPUT+1))
            return fake
        with patch.object(self.registry,'inspect',return_value=self.registry.inspect(identity)), patch.object(engine.subprocess,'Popen',side_effect=oversized), self.assertRaisesRegex(ValueError,'resource limit'):
            engine.execute(self.registry,identity,dict(method='exploratory',columns=['x']))
        self.assertEqual(len(engine.history(self.registry,identity)),1)

    def test_demo_no_private_access_and_ux(self):
        from streamlit.testing.v1 import AppTest
        import analysis_ui
        with patch.object(config,'DEPLOY_MODE',True), patch.object(analysis_ui,'Registry',side_effect=AssertionError('private access')):
            at = AppTest.from_string('from analysis_ui import render; render()', default_timeout=45).run()
            self.assertFalse(at.exception)
            self.assertIn('read-only',at.info[0].value)
        with patch.object(config,'DEPLOY_MODE',True), self.assertRaises(ValueError):
            engine.history(self.registry,'unknown')
        with patch.object(config,'DEPLOY_MODE',True), self.assertRaises(ValueError):
            engine.execute(self.registry,'unknown',{})
        with patch.object(config,'DATA_DIR',Path(self.temp.name).resolve()):
            self.register(b'x,y\n1,2\n2,5\n3,4\n4,8\n5,6\n')
            at = AppTest.from_string('from analysis_ui import render; render()', default_timeout=45).run()
            self.assertFalse(at.exception)
            next(b for b in at.button if b.label=='Preview analysis and exclusions').click().run()
            self.assertFalse(at.exception)
            next(b for b in at.button if b.label=='Run and save analysis').click().run()
            self.assertFalse(at.exception)
            self.assertTrue(at.success)
            self.assertTrue(any(s.value=='Charts' for s in at.subheader))
            self.assertFalse(at.error)


if __name__ == '__main__':
    unittest.main()
