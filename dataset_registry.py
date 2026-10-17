"""Private immutable source bytes and transactional metadata. No AI dependencies."""
from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import tempfile
import uuid
import config
from dataset_parser import parse, filename, MAX_BYTES
from dataset_profile import profile, describe


def now():
    return datetime.now(timezone.utc).isoformat()


def _json(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True)


class Registry:
    def __init__(self, data_dir=None):
        base = Path(data_dir if data_dir is not None else config.DATA_DIR).absolute()
        if config.DEPLOY_MODE or base.resolve().is_relative_to((config.ROOT / 'demo').resolve()):
            raise ValueError('Datasets are disabled in the read-only demo; private storage is not accessed.')
        # Reject symlinks in every existing path component, including a redirected DATA_DIR.
        if '..' in base.parts:
            raise ValueError('Dataset storage must not contain parent traversal.')
        for p in [base, *base.parents]:
            if p.is_symlink():
                raise ValueError('Dataset storage must not traverse symbolic links.')
        self.root = base / 'datasets'
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.root.is_symlink() or not self.root.is_dir():
            raise ValueError('Unsafe dataset storage directory.')
        os.chmod(self.root, 0o700)
        self.db = self.root / 'registry.sqlite3'
        with self.connection() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS datasets (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, version INTEGER NOT NULL,
                filename TEXT NOT NULL, format TEXT NOT NULL, sha256 TEXT NOT NULL,
                bytes INTEGER NOT NULL, created TEXT NOT NULL, origin TEXT NOT NULL,
                options TEXT NOT NULL, profile TEXT NOT NULL, dictionary TEXT NOT NULL,
                UNIQUE(name,version), UNIQUE(sha256,format,options));
            CREATE TABLE IF NOT EXISTS statistics (
                id TEXT PRIMARY KEY, dataset_id TEXT NOT NULL REFERENCES datasets(id),
                created TEXT NOT NULL, output TEXT NOT NULL);
            ''')

    def _check_storage(self):
        if config.DEPLOY_MODE:
            raise ValueError('Datasets are disabled in the read-only demo; private storage is not accessed.')
        if any(p.is_symlink() for p in (self.root, *self.root.parents)):
            raise ValueError('Dataset storage must not traverse symbolic links.')

    @contextmanager
    def connection(self):
        self._check_storage()
        for name in ('registry.sqlite3', 'registry.sqlite3-journal', 'registry.sqlite3-wal', 'registry.sqlite3-shm'):
            p = self.root / name
            if p.is_symlink() or (p.exists() and (not p.is_file() or p.stat().st_nlink != 1)):
                raise ValueError('Unsafe dataset registry path.')
        # Exclusive creation ensures a private DB even with a permissive process umask.
        try:
            fd = os.open(self.db, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
            os.close(fd)
        except FileExistsError:
            pass
        os.chmod(self.db, 0o600)
        db = sqlite3.connect(self.db, timeout=10)
        db.row_factory = sqlite3.Row
        db.create_function('casefold', 1, lambda value: value.casefold(), deterministic=True)
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA synchronous=FULL')
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def record(row):
        if row is None:
            raise ValueError('Dataset version was not found. Refresh the inventory.')
        result = dict(row)
        for key in ('options', 'profile', 'dictionary'):
            result[key] = json.loads(result[key])
        return result

    def inventory_count(self, query=''):
        with self.connection() as db:
            return db.execute("SELECT count(*) FROM datasets WHERE instr(casefold(name || ' ' || filename), casefold(?)) > 0", (query,)).fetchone()[0]

    def inventory(self, query='', page=0):
        if not isinstance(page, int) or page < 0:
            raise ValueError('Inventory page must be a nonnegative integer.')
        with self.connection() as db:
            rows = db.execute("SELECT * FROM datasets WHERE instr(casefold(name || ' ' || filename), casefold(?)) > 0 ORDER BY created DESC, id LIMIT 100 OFFSET ?", (query,page*100)).fetchall()
        return [self.record(r) for r in rows]

    def get(self, dataset_id):
        with self.connection() as db:
            return self.record(db.execute('SELECT * FROM datasets WHERE id=?', (dataset_id,)).fetchone())

    def _blob(self, digest):
        if len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('Invalid stored digest.')
        return self.root / (digest + '.source')

    def source(self, record):
        self._check_storage()
        path = self._blob(record['sha256'])
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, 'rb') as handle:
                info = os.fstat(handle.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > MAX_BYTES:
                    raise ValueError('Unsafe source file.')
                content = handle.read(MAX_BYTES + 1)
        except OSError:
            raise ValueError('Source unavailable or unsafe. Restore the immutable source from a local backup.') from None
        if len(content) != record['bytes'] or hashlib.sha256(content).hexdigest() != record['sha256']:
            raise ValueError('Source integrity check failed. Restore from a local backup.')
        return content

    def register(self, name, source_name, content, sheet=None):
        name = name.strip()
        if not name or len(name) > 128 or any(ord(c) < 32 or ord(c) == 127 for c in name):
            raise ValueError('Dataset name must contain 1–128 printable characters.')
        fmt = filename(source_name)
        table = parse(source_name, content, sheet)
        if table.get('selection_required'):
            raise ValueError('Preview and select a worksheet before confirming import.')
        options = dict(sheet=table.get('sheet'), parser_version=1)
        sha = hashlib.sha256(content).hexdigest()
        metadata = profile(table)
        metadata.update(sheets=table.get('sheets'), sheet=table.get('sheet'), physical_types=table.get('physical_types'))
        identity = uuid.uuid4().hex
        path = self._blob(sha)
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            found = db.execute('SELECT * FROM datasets WHERE sha256=? AND format=? AND options=?', (sha,fmt,_json(options))).fetchone()
            if found:
                record = self.record(found)
                self.source(record)
                return record, False
            version = db.execute('SELECT COALESCE(MAX(version),0)+1 FROM datasets WHERE name=?', (name,)).fetchone()[0]
            if path.exists() or path.is_symlink():
                self.source(dict(sha256=sha, bytes=len(content)))
            else:
                # Unreferenced file is invisible to inventory until SQLite commits.
                fd, temporary = tempfile.mkstemp(prefix='.source-', dir=self.root)
                try:
                    with os.fdopen(fd, 'wb') as handle:
                        handle.write(content)
                        handle.flush()
                        os.fsync(handle.fileno())
                    os.chmod(temporary, 0o400)
                    # Atomic no-overwrite publication; interrupted writes remain unreferenced.
                    os.link(temporary, path, follow_symlinks=False)
                finally:
                    os.unlink(temporary)
                directory = os.open(self.root, os.O_RDONLY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
            dictionary = {c: dict(description='', units='') for c in table['columns']}
            db.execute('INSERT INTO datasets VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (identity,name,version,source_name,fmt,sha,len(content),now(),'local upload',_json(options),_json(metadata),_json(dictionary)))
        return self.get(identity), True

    def inspect(self, dataset_id):
        record = self.get(dataset_id)
        table = parse(record['filename'], self.source(record), record['options']['sheet'])
        return record, table

    def reprofile(self, dataset_id):
        record, table = self.inspect(dataset_id)
        metadata = profile(table)
        metadata.update(sheets=table.get('sheets'), sheet=table.get('sheet'), physical_types=table.get('physical_types'))
        with self.connection() as db:
            db.execute('UPDATE datasets SET profile=? WHERE id=?', (_json(metadata),dataset_id))
        return metadata

    def dictionary(self, dataset_id, values):
        record = self.get(dataset_id)
        if set(values) != set(record['dictionary']):
            raise ValueError('Dictionary must retain the existing columns.')
        for item in values.values():
            if set(item) != {'description','units'} or any(not isinstance(v,str) or len(v)>1000 for v in item.values()):
                raise ValueError('Dictionary supports descriptions and units up to 1000 characters each.')
        with self.connection() as db:
            db.execute('UPDATE datasets SET dictionary=? WHERE id=?', (_json(values),dataset_id))

    def statistics(self, dataset_id, columns):
        record, table = self.inspect(dataset_id)
        result = describe(table, columns)
        result.update(id=uuid.uuid4().hex, dataset_id=dataset_id, dataset_sha256=record['sha256'], dataset_version=record['version'], import_options=record['options'], columns=columns, timestamp=now())
        with self.connection() as db:
            db.execute('INSERT INTO statistics VALUES (?,?,?,?)', (result['id'],dataset_id,result['timestamp'],_json(result)))
        return result

    def saved_statistics(self, dataset_id):
        with self.connection() as db:
            return [json.loads(r[0]) for r in db.execute('SELECT output FROM statistics WHERE dataset_id=? ORDER BY created DESC LIMIT 50', (dataset_id,))]
