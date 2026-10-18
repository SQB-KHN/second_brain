"""Private transactional local planner. No providers, networking or deletion."""
from contextlib import contextmanager
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import uuid
from zoneinfo import ZoneInfo
import config


def local_time(value, zone, fold=None):
    """Resolve a wall time, rejecting gaps and requiring an explicit repeated-hour choice."""
    z = ZoneInfo(zone)
    naive = datetime.fromisoformat(value)
    if naive.tzinfo is not None:
        raise ValueError('Enter local time without an offset; choose a timezone.')
    valid = [naive.replace(tzinfo=z, fold=f) for f in (0, 1)
             if naive.replace(tzinfo=z, fold=f).astimezone(timezone.utc).astimezone(z).replace(tzinfo=None) == naive]
    if not valid:
        raise ValueError('This local time does not exist because clocks change.')
    if len({v.utcoffset() for v in valid}) > 1 and fold is None:
        raise ValueError('Repeated daylight-saving hour: choose first or second occurrence.')
    return naive.replace(tzinfo=z, fold=fold or 0).astimezone(timezone.utc).isoformat()


class Tasks:
    def __init__(self, data_dir=None):
        self.base = Path(data_dir if data_dir is not None else config.DATA_DIR).absolute()
        self.root = self.base / 'planner'
        self.db = self.root / 'tasks.sqlite3'
        self._safe()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)
        with self.connection() as db:
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version > 1:
                raise ValueError('Unsupported planner schema; restore compatible software.')
            if version == 0:
                db.execute('CREATE TABLE projects (id TEXT PRIMARY KEY, label TEXT NOT NULL UNIQUE, status TEXT NOT NULL CHECK(status IN (\'active\',\'done\')))')
                db.execute('CREATE TABLE project_history (sequence INTEGER PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id), recorded TEXT NOT NULL, status TEXT NOT NULL)')
                db.execute("""CREATE TABLE tasks (id TEXT PRIMARY KEY, record TEXT NOT NULL CHECK(
                    json_valid(record) AND json_extract(record,'$.id')=id
                    AND json_extract(record,'$.status') IN ('todo','doing','done')
                    AND json_extract(record,'$.priority') IN (1,2,3)
                    AND json_extract(record,'$.schema_version')=1))""")
                db.execute('CREATE TABLE history (sequence INTEGER PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(id), recorded TEXT NOT NULL, record TEXT NOT NULL)')
                db.execute('PRAGMA user_version=1')

    def _safe(self):
        if config.DEPLOY_MODE or self.base.resolve().is_relative_to((config.ROOT / 'demo').resolve()):
            raise ValueError('Planner storage is disabled in demo.')
        if '..' in self.base.parts or any(p.is_symlink() for p in (self.root, *self.root.parents)):
            raise ValueError('Unsafe planner directory.')
        for suffix in ('', '-journal', '-wal', '-shm'):
            p = Path(str(self.db) + suffix)
            if p.is_symlink() or (p.exists() and (not p.is_file() or p.stat().st_nlink != 1)):
                raise ValueError('Unsafe planner registry.')

    @contextmanager
    def connection(self):
        self._safe()
        try:
            fd = os.open(self.db, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            os.close(fd)
        except FileExistsError:
            pass
        os.chmod(self.db, 0o600)
        db = sqlite3.connect(self.db, timeout=10)
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('PRAGMA synchronous=FULL')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def list(self):
        with self.connection() as db:
            rows = [json.loads(r[0]) for r in db.execute('SELECT record FROM tasks')]
        return sorted(rows, key=lambda r: (r['status'] == 'done', r['priority'], r['scheduled_start'] or '9999', r['created'], r['id']))

    def save(self, *, task_id=None, expected_updated=None, title, details='', status='todo', priority=2,
             scheduled_start=None, scheduled_end=None, due=None, timezone_id='UTC', project='', references=None):
        ZoneInfo(timezone_id)
        if not isinstance(title, str) or not title.strip() or len(title) > 300 or len(details) > 20000:
            raise ValueError('Title is required (maximum 300 characters); details maximum 20000.')
        if status not in ('todo', 'doing', 'done') or type(priority) is not int or priority not in (1, 2, 3):
            raise ValueError('Invalid status or priority.')
        if bool(scheduled_start) != bool(scheduled_end):
            raise ValueError('Both scheduled times are required.')
        if scheduled_start:
            start, end = map(datetime.fromisoformat, (scheduled_start, scheduled_end))
            if start.tzinfo is None or end.tzinfo is None or end <= start:
                raise ValueError('Scheduled end must follow start with timezone offsets.')
            scheduled_start, scheduled_end = (v.astimezone(timezone.utc).isoformat() for v in (start, end))
        if due:
            due = date.fromisoformat(due).isoformat()
        refs = references or []
        if not isinstance(refs, list):
            raise ValueError('References must be a list of local relative file paths.')
        for ref in refs:
            if not isinstance(ref, str):
                raise ValueError('Invalid reference.')
            p = self.base / ref
            if not isinstance(ref, str) or Path(ref).is_absolute() or '..' in Path(ref).parts or not p.resolve().is_relative_to(self.base.resolve()) or any(x.is_symlink() for x in (p, *p.parents)) or not p.is_file() or Path(ref).parts[0] not in ('wiki', 'knowledge', 'datasets'):
                raise ValueError('Reference must identify an existing local knowledge/dataset/analysis file.')
        if len(project) > 100:
            raise ValueError('Project label is too long.')
        stamp = datetime.now(timezone.utc).isoformat()
        with self.connection() as db:
            old = None
            if task_id:
                row = db.execute('SELECT record FROM tasks WHERE id=?', (task_id,)).fetchone()
                if not row:
                    raise ValueError('Task not found.')
                old = json.loads(row[0])
                if expected_updated != old['updated']:
                    raise ValueError('Task changed; reload before saving.')
            project_id = None
            if project.strip():
                db.execute('INSERT OR IGNORE INTO projects VALUES (?, ?, ?)', (str(uuid.uuid4()), project.strip(), 'active'))
                project_id = db.execute('SELECT id FROM projects WHERE label=?', (project.strip(),)).fetchone()[0]
                if not db.execute('SELECT 1 FROM project_history WHERE project_id=?', (project_id,)).fetchone():
                    db.execute('INSERT INTO project_history(project_id,recorded,status) VALUES (?,?,?)', (project_id, stamp, 'active'))
            record = dict(id=task_id or str(uuid.uuid4()), title=title.strip(), details=details, status=status,
                          priority=priority, scheduled_start=scheduled_start, scheduled_end=scheduled_end,
                          due=due, timezone=timezone_id, project=project.strip(), project_id=project_id,
                          references=refs, recurrence=None, created=old['created'] if old else stamp,
                          updated=stamp, schema_version=1)
            payload = json.dumps(record)
            db.execute('INSERT INTO tasks VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET record=excluded.record', (record['id'], payload))
            db.execute('INSERT INTO history(task_id,recorded,record) VALUES (?,?,?)', (record['id'], stamp, payload))
        return record

    def projects(self):
        with self.connection() as db:
            return [dict(id=r[0], label=r[1], status=r[2]) for r in db.execute('SELECT id,label,status FROM projects ORDER BY label')]

    def project_status(self, project_id, status):
        if status not in ('active', 'done'):
            raise ValueError('Invalid project status.')
        with self.connection() as db:
            if db.execute('UPDATE projects SET status=? WHERE id=?', (status, project_id)).rowcount != 1:
                raise ValueError('Project not found.')
            db.execute('INSERT INTO project_history(project_id,recorded,status) VALUES (?,?,?)', (project_id, datetime.now(timezone.utc).isoformat(), status))


def for_day(records, day, zone='UTC'):
    z = ZoneInfo(zone)
    start = datetime.combine(day, datetime.min.time(), z)
    from datetime import timedelta
    end = start + timedelta(days=1)
    scheduled = [r for r in records if r['scheduled_start'] and datetime.fromisoformat(r['scheduled_start']) < end and datetime.fromisoformat(r['scheduled_end']) > start]
    due = [r for r in records if r['due'] == day.isoformat()]
    unscheduled = [r for r in records if not r['scheduled_start'] and not r['due']]
    return sorted(scheduled, key=lambda r: r['scheduled_start']), due, unscheduled
