import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import prepare_deploy as publication


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.source = self.root / 'private'
        self.dest = self.root / 'bundle'
        self.manifest = self.root / 'manifest.json'
        self.approvals = []
        self.note('approved', approve=True)
        self.note('unapproved', approve=False)
        self.save_manifest()

    def note(self, name, approve=False, links='[]', body=''):
        path = self.source / 'wiki' / 'resources' / (name + '.md')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'---\nid: {name}\npara: resources\nsummary: Synthetic fixture\nlinks: {links}\n---\n# Synthetic sample\n{body}\n')
        if approve:
            self.approvals.append({'path': 'resources/' + path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        return path

    def save_manifest(self):
        self.manifest.write_text(json.dumps({'version': 1, 'notes': self.approvals}))

    def publish(self):
        return publication.publish(self.source, self.dest, self.manifest)

    def snapshot(self):
        return {p.relative_to(self.dest).as_posix(): p.read_bytes() for p in self.dest.rglob('*') if p.is_file()}

    def test_only_approved_notes_and_rebuilt_metadata(self):
        (self.source / 'wiki' / '.index.json').write_text('{"unapproved":"resources/unapproved.md"}')
        (self.source / 'embeddings').mkdir()
        (self.source / 'embeddings' / 'unapproved.npy').write_bytes(b'synthetic vector')
        self.assertEqual(self.publish(), 1)
        self.assertFalse((self.dest / 'wiki/resources/unapproved.md').exists())
        self.assertNotIn(b'unapproved', b''.join(self.snapshot().values()))
        self.assertEqual(json.loads((self.dest / 'embeddings/index.json').read_text()), {})

    def test_removed_samples_and_stale_files_disappear(self):
        self.publish()
        (self.dest / 'stale.bin').write_bytes(b'synthetic stale artifact')
        self.approvals.clear()
        self.save_manifest()
        self.assertEqual(self.publish(), 0)
        self.assertFalse((self.dest / 'wiki/resources/approved.md').exists())
        self.assertFalse((self.dest / 'stale.bin').exists())
        self.assertEqual(json.loads((self.dest / 'graph.json').read_text())['nodes'], [])

    def test_changed_or_missing_sample_preserves_previous_bundle(self):
        self.publish()
        before = self.snapshot()
        sample = self.source / 'wiki/resources/approved.md'
        sample.write_text('Synthetic changed fixture')
        with self.assertRaises(publication.PublicationError):
            self.publish()
        self.assertEqual(before, self.snapshot())
        sample.unlink()
        with self.assertRaises(OSError):
            self.publish()
        self.assertEqual(before, self.snapshot())

    def test_failed_replacement_restores_previous_bundle(self):
        self.publish()
        before = self.snapshot()
        original = Path.rename
        def fail_stage(path, target):
            if path.name == 'bundle' and path.parent.name.startswith('.secondself-stage-'):
                raise OSError('Synthetic replacement failure')
            return original(path, target)
        with patch.object(Path, 'rename', fail_stage):
            with self.assertRaises(OSError):
                self.publish()
        self.assertEqual(before, self.snapshot())

    def test_failed_recovery_retains_previous_bundle(self):
        self.publish()
        before = self.snapshot()
        original = Path.rename
        def fail_replacement_and_recovery(path, target):
            if path.parent.name.startswith('.secondself-stage-'):
                raise OSError('Synthetic rename failure')
            return original(path, target)
        with patch.object(Path, 'rename', fail_replacement_and_recovery):
            with self.assertRaises(publication.PublicationError):
                self.publish()
        recovery = list(self.root.glob('.secondself-stage-*/previous'))
        self.assertEqual(len(recovery), 1)
        self.assertEqual(before, {p.relative_to(recovery[0]).as_posix(): p.read_bytes() for p in recovery[0].rglob('*') if p.is_file()})

    def test_failed_validation_does_not_create_bundle(self):
        with patch.object(publication, 'write_json', side_effect=OSError('Synthetic write failure')):
            with self.assertRaises(OSError):
                self.publish()
        self.assertFalse(self.dest.exists())

    def test_excluded_references_fail_closed(self):
        for links, body in [(' [unapproved]', ''), ('[]', '[[unapproved]]'), ('[]', '[asset](../../private.txt)')]:
            self.approvals.clear()
            self.note('approved', approve=True, links=links, body=body)
            self.save_manifest()
            with self.assertRaises(publication.PublicationError):
                self.publish()

    def test_path_escape_symlink_and_overlap_rejected(self):
        self.approvals[0]['path'] = '../outside.md'
        self.save_manifest()
        with self.assertRaises(publication.PublicationError):
            self.publish()
        with self.assertRaises(publication.PublicationError):
            publication.publish(self.source, self.source / 'output', self.manifest)
        self.dest.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(publication.PublicationError):
            self.publish()

    def test_cli_failure_does_not_log_content(self):
        self.manifest.write_text('Synthetic invalid JSON')
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(publication.main(['--source', str(self.source), '--dest', str(self.dest), '--manifest', str(self.manifest)]), 1)
        self.assertNotIn('Synthetic', stderr.getvalue())

    def test_approved_edges_only(self):
        self.note('second', approve=True, links='[approved]', body='[[approved]]')
        self.save_manifest()
        self.publish()
        graph = json.loads((self.dest / 'graph.json').read_text())
        self.assertEqual(graph['edges'], [{'source': 'second', 'target': 'approved', 'type': 'explicit'}])

    def test_interrupt_restores_previous_bundle_at_both_rename_boundaries(self):
        self.publish()
        before = self.snapshot()
        original = Path.rename
        for boundary in ('after_backup', 'before_install', 'after_install'):
            def interrupt(path, target):
                if boundary == 'after_backup' and path == self.dest:
                    original(path, target)
                    raise KeyboardInterrupt()
                if path.name == 'bundle' and path.parent.name.startswith('.secondself-stage-'):
                    if boundary == 'after_install':
                        original(path, target)
                    raise KeyboardInterrupt()
                return original(path, target)
            with self.subTest(boundary=boundary), patch.object(Path, 'rename', interrupt):
                with self.assertRaises((KeyboardInterrupt, publication.RecoveryRequired)):
                    self.publish()
            self.assertTrue(self.dest.is_dir())
            self.assertEqual(before, self.snapshot())
            if boundary == 'after_install':
                self.assertEqual(len(list(self.root.glob('.secondself-stage-*/previous'))), 1)

    def test_interrupt_during_restore_retains_previous_and_reports_recovery(self):
        self.publish()
        before = self.snapshot()
        original = Path.rename
        def interrupt(path, target):
            if path.parent.name.startswith('.secondself-stage-'):
                raise KeyboardInterrupt()
            return original(path, target)
        stderr = io.StringIO()
        with patch.object(Path, 'rename', interrupt), contextlib.redirect_stderr(stderr):
            code = publication.main(['--source', str(self.source), '--dest', str(self.dest), '--manifest', str(self.manifest)])
        self.assertEqual(code, 1)
        previous = list(self.root.glob('.secondself-stage-*/previous'))
        self.assertEqual(len(previous), 1)
        self.assertIn(str(previous[0]), stderr.getvalue())
        self.assertIn('recovery steps', stderr.getvalue())
        self.assertEqual(before, {p.relative_to(previous[0]).as_posix(): p.read_bytes() for p in previous[0].rglob('*') if p.is_file()})

    def approve_content(self, content):
        path = self.source / 'wiki/resources/approved.md'
        path.write_text(content)
        self.approvals[0]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.save_manifest()

    def test_adversarial_body_syntax_is_rejected(self):
        self.publish()
        before = self.snapshot()
        for body in ('[hidden][ref]\n[ref]: ../../excluded.md',
                     '[hidden](https://example.com/excluded)',
                     '<a href="../../excluded.md">hidden</a>',
                     '<img src="../../excluded.png">',
                     '<!-- [[approved]] -->', '[[excluded]]',
                     '[[approved|excluded]]', '[[approved#excluded]]',
                     '<https://example.com/excluded>',
                     '</script><script>window.SYNTHETIC_MARKER=1</script>'):
            with self.subTest(body=body):
                self.approve_content('---\nid: approved\npara: resources\nsummary: Synthetic\n---\n' + body)
                with self.assertRaises(publication.PublicationError):
                    self.publish()
                self.assertEqual(before, self.snapshot())

    def test_adversarial_metadata_is_rejected(self):
        for field in ('source: ../../excluded.md', 'embedding_id: excluded',
                      'summary: "See [[excluded]]"', 'summary: "../../excluded.md"',
                      'links: [excluded]', 'tags: "not a list"', 'tags: ["[[excluded]]"]',
                      'created: ../../excluded.md', 'custom_reference: excluded',
                      'id: ../../excluded', 'summary: &alias Synthetic\ntags: [*alias]',
                      'summary: !!str Synthetic', 'links: null'):
            with self.subTest(field=field):
                # Replace the field instead of creating accidental duplicate keys.
                meta = {'id': 'approved', 'para': 'resources', 'summary': 'Synthetic'}
                meta.pop(field.split(':', 1)[0], None)
                header = '\n'.join(k + ': ' + v for k, v in meta.items())
                self.approve_content('---\n' + header + '\n' + field + '\n---\nSynthetic')
                with self.assertRaises(publication.PublicationError):
                    self.publish()

    def test_duplicate_yaml_keys_rejected(self):
        self.approve_content('---\nid: approved\nid: excluded\npara: resources\nsummary: Synthetic\n---\nSynthetic')
        with self.assertRaises(publication.PublicationError):
            self.publish()

    def test_strict_manifest_schema_and_hashes(self):
        original = json.loads(self.manifest.read_text())
        for modify in (lambda s: s.update(version=True), lambda s: s.update(extra=1),
                       lambda s: s['notes'][0].update(extra=1),
                       lambda s: s['notes'][0].update(sha256=None),
                       lambda s: s['notes'][0].update(sha256='invalid'),
                       lambda s: s['notes'][0].update(path=None),
                       lambda s: s['notes'][0].update(sha256='0'*64),
                       lambda s: s['notes'][0].update(path='/absolute.md'),
                       lambda s: s['notes'][0].update(path='resources/../approved.md')):
            spec = json.loads(json.dumps(original))
            modify(spec)
            self.manifest.write_text(json.dumps(spec))
            with self.assertRaises(publication.PublicationError):
                self.publish()
        self.manifest.write_text('{"version":1,"version":1,"notes":[]}')
        with self.assertRaises(publication.PublicationError):
            self.publish()

    def test_symlink_components_are_rejected(self):
        alias = self.root / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        for source, dest, manifest in (
            (alias / 'private', self.dest, self.manifest),
            (self.source, alias / 'bundle', self.manifest),
            (self.source, self.dest, alias / 'manifest.json')):
            with self.assertRaises(publication.PublicationError):
                publication.publish(source, dest, manifest)
        linked_manifest = self.root / 'linked.json'
        linked_manifest.symlink_to(self.manifest)
        with self.assertRaises(publication.PublicationError):
            publication.publish(self.source, self.dest, linked_manifest)
        note = self.source / 'wiki/resources/approved.md'
        linked_note = self.root / 'real-note.md'
        linked_note.write_bytes(note.read_bytes())
        note.unlink()  # Synthetic fixture only.
        note.symlink_to(linked_note)
        with self.assertRaises(publication.PublicationError):
            self.publish()

    def test_missing_source_empty_manifest_is_safe(self):
        self.approvals.clear()
        self.save_manifest()
        self.assertEqual(publication.publish(self.root / 'missing', self.dest, self.manifest), 0)

    def test_legacy_flag_still_rebuilds(self):
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            code = publication.main(['--source', str(self.source), '--dest', str(self.dest), '--manifest', str(self.manifest), '--skip-rebuild'])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads((self.dest / 'graph.json').read_text())['nodes']), 1)


if __name__ == '__main__':
    unittest.main()
