import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from datetime import date
import config
from task_service import Tasks, for_day, local_time


class TodayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        p = patch.object(config, 'DEPLOY_MODE', False)
        p.start()
        self.addCleanup(p.stop)
        self.store = Tasks(self.base)

    def test_lifecycle_and_restart(self):
        r = self.store.save(title='<script>private synthetic</script>', project='Synthetic', priority=1)
        self.assertIsNone(r['scheduled_start'])
        r2 = self.store.save(task_id=r['id'], expected_updated=r['updated'], title=r['title'], status='done')
        self.assertEqual(Tasks(self.base).list(), [r2])
        with self.store.connection() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM history').fetchone()[0], 2)
        self.assertEqual(r['created'], r2['created'])
        with self.assertRaises(ValueError):
            self.store.save(task_id=r['id'], expected_updated=r['updated'], title='stale')
        self.assertEqual(os.stat(self.store.db).st_mode & 0o777, 0o600)

    def test_dates(self):
        for value in ('2026-03-08T02:30', '2026-11-01T01:30'):
            with self.assertRaises(ValueError):
                local_time(value, 'America/New_York')
        self.assertNotEqual(local_time('2026-11-01T01:30', 'America/New_York', 0), local_time('2026-11-01T01:30', 'America/New_York', 1))
        for kw in (dict(due='2026-02-30'), dict(priority=0), dict(scheduled_start='2026-01-01T12:00', scheduled_end='2026-01-01T13:00')):
            with self.assertRaises(ValueError):
                self.store.save(title='Synthetic', **kw)
        r = self.store.save(title='Overnight', scheduled_start=local_time('2026-01-01T23:00','UTC'), scheduled_end=local_time('2026-01-02T02:00','UTC'))
        self.assertEqual(for_day([r], date(2026,1,2))[0], [r])

    def test_order_and_categories(self):
        self.store.save(title='Low', priority=3)
        self.store.save(title='High', priority=1)
        self.store.save(title='Due', due='2026-01-01')
        rows = self.store.list()
        self.assertEqual(rows[0]['title'], 'High')
        scheduled, due, unscheduled = for_day(rows, date(2026,1,1))
        self.assertFalse(scheduled)
        self.assertEqual(len(due),1)
        self.assertEqual(len(unscheduled),2)

    def test_atomic_recovery_migration(self):
        with self.assertRaises(RuntimeError):
            with self.store.connection() as db:
                db.execute("INSERT INTO projects VALUES ('rollback','rollback','active')")
                raise RuntimeError()
        with self.store.connection() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM projects').fetchone()[0],0)
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],1)
            db.execute('PRAGMA user_version=99')
        with self.assertRaises(ValueError):
            Tasks(self.base)

    def test_demo_and_unsafe_storage(self):
        with patch.object(config, 'DEPLOY_MODE', True):
            with self.assertRaises(ValueError):
                Tasks(self.base / 'unused')
            self.assertFalse((self.base/'unused').exists())
            with self.assertRaises(ValueError):
                self.store.list()
        with self.assertRaises(ValueError):
            self.store.save(title='bad', references=['../outside'])
        outside = self.base/'outside'
        outside.write_text('synthetic')
        self.store.db.unlink()
        self.store.db.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.store.list()
        self.assertEqual(outside.read_text(), 'synthetic')

    def test_history_failure_rolls_back_entire_save(self):
        with self.store.connection() as db:
            db.execute("CREATE TRIGGER fail_history BEFORE INSERT ON history BEGIN SELECT RAISE(ABORT, 'synthetic failure'); END")
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.save(title='Synthetic transaction', project='Rolled back')
        self.assertEqual(self.store.list(), [])
        self.assertEqual(self.store.projects(), [])
        with self.store.connection() as db:
            db.execute('DROP TRIGGER fail_history')
        self.store.save(title='Recovery')
        self.assertEqual(len(self.store.list()), 1)

    def test_project_status_audit_and_references(self):
        folder = self.base / 'wiki'
        folder.mkdir()
        (folder / 'synthetic.md').write_text('Synthetic only')
        r = self.store.save(title='Project task', project='Synthetic', references=['wiki/synthetic.md'])
        self.store.project_status(r['project_id'], 'done')
        self.assertEqual(self.store.projects()[0]['status'], 'done')
        with self.store.connection() as db:
            states = db.execute('SELECT status FROM project_history ORDER BY sequence').fetchall()
        self.assertEqual(states, [('active',), ('done',)])
        with self.assertRaises(ValueError):
            self.store.save(title='Missing reference', references=['wiki/missing.md'])

    def test_migration_failure_is_transactional(self):
        other = self.base / 'other' / 'planner'
        other.mkdir(parents=True)
        db = sqlite3.connect(other / 'tasks.sqlite3')
        db.execute('CREATE TABLE tasks (incompatible TEXT)')
        db.commit()
        db.close()
        with self.assertRaises(sqlite3.OperationalError):
            Tasks(other.parent)
        db = sqlite3.connect(other / 'tasks.sqlite3')
        self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 0)
        self.assertFalse(db.execute("SELECT name FROM sqlite_master WHERE name='projects'").fetchall())
        db.close()

    def test_demo_ui_never_opens_storage(self):
        from streamlit.testing.v1 import AppTest
        import today_ui
        script = self.base / 'demo_app.py'
        script.write_text("import streamlit as st\nst.set_page_config(layout='wide')\nfrom today_ui import render\nrender(lambda view: None)\n")
        with patch.object(config, 'DEPLOY_MODE', True), patch.object(today_ui, 'Tasks', side_effect=AssertionError('Private storage accessed')):
            app = AppTest.from_file(str(script)).run()
            self.assertFalse(app.exception)
            self.assertFalse(any(b.label == 'Save task' for b in app.button))
            self.assertTrue(any('Synthetic examples' in i.value for i in app.info))
