"""Local workspace operations; all graph/retrieval publication uses verified refresh."""
from datetime import datetime, timezone
from pathlib import Path
import os
import tempfile
import uuid

import yaml

from config import DATA_DIR, DEPLOY_MODE, ENABLE_CAPTURE, ENABLE_REFRESH_BRAIN, PARA_FOLDERS
from link import load_wiki_note
from refresh import refresh, writer_lock


def writable():
    if DEPLOY_MODE or DATA_DIR.resolve().is_relative_to(Path(__file__).resolve().parent / 'demo'):
        raise ValueError('The demo workspace is read-only.')
    if not ENABLE_CAPTURE or not ENABLE_REFRESH_BRAIN:
        raise ValueError('Capture and refresh must both be enabled to save and index.')


def note_path(path):
    path = Path(path)
    base = (DATA_DIR / 'wiki').resolve()
    if path.is_symlink() or not path.resolve().is_relative_to(base) or path.suffix != '.md':
        raise ValueError('Invalid note path.')
    relative = path.absolute().relative_to((DATA_DIR / 'wiki').absolute())
    if any(((DATA_DIR / 'wiki') / Path(*relative.parts[:i])).is_symlink() for i in range(len(relative.parts))):
        raise ValueError('Symlink note paths are not supported.')
    return path


def notes():
    result = []
    for para in PARA_FOLDERS:
        for path in sorted((DATA_DIR / 'wiki' / para).rglob('*.md')):
            try:
                note = load_wiki_note(note_path(path))
                if note:
                    result.append(note)
            except (ValueError, OSError):
                continue
    return sorted(result, key=lambda n: (n.created, n.id), reverse=True)


def save_note(title, body, para, tags, *, path=None, expected=None):
    writable()
    with writer_lock(DATA_DIR / 'knowledge'):
        return _save_note(title, body, para, tags, path=path, expected=expected)


def _save_note(title, body, para, tags, *, path=None, expected=None):
    """Save canonical markdown once. Caller retains path if publication fails."""
    writable()
    if not title.strip() or not body.strip():
        raise ValueError('Add a title and note text before saving.')
    if para not in PARA_FOLDERS:
        raise ValueError('Choose a valid category.')
    metadata = {}
    if path is not None:
        path = note_path(path)
        existing = path.read_text()
        if expected is None or existing != expected:
            raise ValueError('This note changed since you opened it. Reopen it before saving.')
        note = load_wiki_note(path)
        if not note:
            raise ValueError('Cannot edit invalid note metadata.')
        metadata = dict(note.frontmatter)
        # Keep identity and category/path alignment stable during editing.
        para = note.para
    else:
        ident = uuid.uuid4().hex
        path = note_path(DATA_DIR / 'wiki' / para / f'{ident}.md')
        metadata.update(id=ident, created=datetime.now(timezone.utc).isoformat(), links=[])
    metadata.update(para=para, tags=[t.strip() for t in tags.split(',') if t.strip()],
                    summary=body.strip()[:300])
    metadata.setdefault('source_type', 'text')
    content = '---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + '---\n# ' + title.strip().replace('\n', ' ') + '\n\n' + body.strip() + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.note-')
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return path


def index_notes():
    writable()
    # Preserve external-provider plan/budget approval and legacy migration gates.
    return refresh(DATA_DIR)
