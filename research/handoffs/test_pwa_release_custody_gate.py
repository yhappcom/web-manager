import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote
from pwa_release_custody_gate import digest, main

SHA = 'a' * 40

class CustodyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'normal'
        self.root.mkdir()
        self.receipt = self.base / 'normal-receipt.json'
        self.create_fixture()

    def write(self, name, data):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data if isinstance(data, bytes) else data.encode())
        return {'path': '/'.join(quote(part, safe='') for part in name.split('/')),
                'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}

    def create_fixture(self):
        shell = [self.write(p, 'body') for p in ('index.html', 'main.dart.js', 'manifest.json',
                  'canvaskit/canvaskit.js', 'canvaskit/canvaskit.wasm')]
        fontset = 'stage-c-test'
        shell.append(self.write('flutter_bootstrap.js', f'fontFallbackBaseUrl font-fallback/{fontset}/'))
        fonts = [self.write(f'font-fallback/{fontset}/font{i:03}.woff2', b'font') for i in range(724)]
        notices = [self.write(f'font-fallback/{fontset}/license{i:03}/OFL.txt', b'license') for i in range(144)]
        notices += [self.write(f'font-fallback/{fontset}/NOTICE{i}.txt', b'notice') for i in range(4)]
        build = digest(json.dumps(shell, ensure_ascii=False, separators=(',', ':')).encode())[:32]
        manifest = {'schemaVersion': 2, 'apiVersion': 2, 'databaseCapability': 17,
                    'appBuildId': build, 'fontSetId': fontset,
                    'shell': shell, 'fonts': fonts, 'fontNotices': notices}
        self.write('logmate-offline-manifest.json', json.dumps(manifest))
        self.write('logmate_service_worker.js', 'const OFFLINE_MANIFEST = ' + json.dumps(manifest) + ';\nconst CONTROL_CACHE = 1;')

    def run_gate(self, mode='freeze', kind='normal', root=None, receipt=None):
        return main([mode, '--root', str(root or self.root), '--kind', kind,
                     '--source-sha', SHA, '--receipt', str(receipt or self.receipt)])

    def test_freeze_verify(self):
        self.assertEqual(self.run_gate(), 0)
        self.assertEqual(self.run_gate('verify'), 0)
        record = json.loads(self.receipt.read_text())
        self.assertEqual(record['fileCount'], 880)
        self.assertEqual(record['kind'], 'normal')

    def test_changed_unlisted_file(self):
        self.assertEqual(self.run_gate(), 0)
        self.write('extra-unlisted.txt', b'new file')
        self.assertEqual(self.run_gate('verify'), 2)

    def test_changed_worker_without_shell_change(self):
        self.assertEqual(self.run_gate(), 0)
        with (self.root / 'logmate_service_worker.js').open('a') as f: f.write('// changed worker')
        self.assertEqual(self.run_gate('verify'), 2)

    def test_marker_leak(self):
        with (self.root / 'main.dart.js').open('ab') as f: f.write(b'LOGMATE_PERSISTENCE_ACCEPTANCE_FLIGHT_V1')
        self.assertEqual(self.run_gate(), 2)

    def test_missing_acceptance_marker(self):
        self.assertEqual(self.run_gate(kind='acceptance'), 2)

    def test_corrupt_manifest_record(self):
        p = self.root / 'logmate-offline-manifest.json'
        m = json.loads(p.read_text()); m['fonts'][0]['sha256'] = '0'*64
        p.write_text(json.dumps(m))
        self.assertEqual(self.run_gate(), 2)

    def test_manifest_traversal(self):
        p = self.root / 'logmate-offline-manifest.json'
        m = json.loads(p.read_text()); m['fonts'][0]['path'] = '%2e%2e/outside.txt'
        p.write_text(json.dumps(m))
        self.assertEqual(self.run_gate(), 2)

    def test_symlink(self):
        (self.root / 'shortcut').symlink_to(self.root / 'index.html')
        self.assertEqual(self.run_gate(), 2)

    def test_no_overwrite_receipt(self):
        self.assertEqual(self.run_gate(), 0)
        self.assertEqual(self.run_gate(), 2)

    def test_receipt_in_root(self):
        self.assertEqual(self.run_gate(receipt=self.root / 'receipt.json'), 2)

    def test_worker_manifest_divergence(self):
        p = self.root / 'logmate_service_worker.js'
        p.write_text(p.read_text().replace('stage-c-test', 'stage-c-other'))
        self.assertEqual(self.run_gate(), 2)

    def test_root_symlink(self):
        alias = self.base / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        self.assertEqual(self.run_gate(root=alias), 2)

    def test_hosting_root_mismatch(self):
        config = self.base / 'firebase.json'
        config.write_text(json.dumps({'hosting': {'public': 'build/web'}}))
        self.assertEqual(main(['freeze', '--root', str(self.root), '--kind', 'normal',
                         '--source-sha', SHA, '--receipt', str(self.receipt),
                         '--firebase-config', str(config)]), 2)

    def test_hosting_root_match(self):
        config = self.base / 'firebase.json'
        config.write_text(json.dumps({'hosting': {'public': 'normal'}}))
        self.assertEqual(main(['freeze', '--root', str(self.root), '--kind', 'normal',
                         '--source-sha', SHA, '--receipt', str(self.receipt),
                         '--firebase-config', str(config)]), 0)

    def test_bad_source_sha(self):
        self.assertEqual(main(['freeze', '--root', str(self.root), '--kind', 'normal',
                         '--source-sha', 'main', '--receipt', str(self.receipt)]), 2)

if __name__ == '__main__': unittest.main()
