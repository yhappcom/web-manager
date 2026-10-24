import copy
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from pwa_archive_transport_gate import audit, sha, GateError, REQUIRED

SOURCE = 'a' * 40

def make_receipt(files, kind='normal'):
    inv = {p: {'bytes': len(b), 'sha256': sha(b)} for p, b in files.items()}
    return {'schema': 1, 'kind': kind, 'sourceSha': SOURCE, 'fileCount': len(inv),
            'workerSha256': inv['logmate_service_worker.js']['sha256'],
            'manifestSha256': inv['logmate-offline-manifest.json']['sha256'],
            'treeSha256': sha(json.dumps(inv, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()),
            'files': inv}

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.zip = self.base / 'normal.zip'
        self.receipt_path = self.base / 'receipt.json'
        self.files = {p: p.encode() for p in REQUIRED}
        self.files['fonts/A.woff2'] = b'font' * 40
        self.files['.well-known/assetlinks.json'] = b'{}'
        self.entries = list(self.files.items())
        self.receipt = make_receipt(self.files)
        self.build()

    def build(self):
        with zipfile.ZipFile(self.zip, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for path, data in self.entries:
                z.writestr(path, data)
        self.receipt_path.write_text(json.dumps(self.receipt), encoding='utf-8')

    def run_gate(self, *, archive_pin=None, receipt_pin=None, source=SOURCE):
        return audit(self.zip, self.receipt_path, archive_pin or sha(self.zip.read_bytes()),
                     receipt_pin or sha(self.receipt_path.read_bytes()), source)

    def test_positive(self):
        r = self.run_gate()
        self.assertEqual(r['verdict'], 'ARCHIVE_BYTES_MATCH_UNVERIFIED')
        self.assertEqual(r['fileCount'], len(self.files))

    def test_hidden_file_preserved(self):
        self.assertIn('.well-known/assetlinks.json', self.receipt['files'])
        self.run_gate()

    def test_archive_pin_drift(self):
        with self.assertRaises(GateError): self.run_gate(archive_pin='0'*64)

    def test_receipt_pin_drift(self):
        with self.assertRaises(GateError): self.run_gate(receipt_pin='0'*64)

    def test_wrong_source(self):
        with self.assertRaises(GateError): self.run_gate(source='b'*40)

    def test_acceptance(self):
        self.receipt['kind'] = 'acceptance'; self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_file_tamper(self):
        self.entries[0] = (self.entries[0][0], b'tampered'); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_missing_file(self):
        self.entries.pop(); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_extra_file(self):
        self.entries.append(('evil.js', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_duplicate(self):
        self.entries.append(self.entries[0]); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_casefold_collision(self):
        self.entries.append(('INDEX.HTML', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_traversal(self):
        self.entries.append(('../escape', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_absolute(self):
        self.entries.append(('/absolute', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_backslash(self):
        self.entries.append(('evil\\x', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_encoded_traversal(self):
        self.entries.append(('%2e%2e/escape', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_unicode_normalization(self):
        self.entries.append(('e\u0301.txt', b'x')); self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_symlink(self):
        with zipfile.ZipFile(self.zip, 'w') as z:
            for path, data in self.entries: z.writestr(path, data)
            info = zipfile.ZipInfo('shortcut')
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, 'index.html')
        with self.assertRaises(GateError): self.run_gate()

    def test_expansion_ratio(self):
        p = 'fonts/A.woff2'
        self.files[p] = b'0' * 2000000
        self.entries = list(self.files.items())
        self.receipt = make_receipt(self.files)
        self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_tree_hash_tamper(self):
        self.receipt['treeSha256'] = '0'*64; self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_worker_digest_tamper(self):
        self.receipt['workerSha256'] = '0'*64; self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_invalid_receipt_file_size(self):
        self.receipt['files']['index.html']['bytes'] += 1; self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_missing_required_receipt(self):
        del self.receipt['files']['index.html']; self.receipt['fileCount'] -= 1
        self.receipt['treeSha256'] = sha(json.dumps(self.receipt['files'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())
        self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_duplicate_receipt_casefold(self):
        self.receipt['files']['INDEX.HTML'] = copy.deepcopy(self.receipt['files']['index.html'])
        self.receipt['fileCount'] += 1
        self.receipt['treeSha256'] = sha(json.dumps(self.receipt['files'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())
        self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_directory_positive(self):
        self.entries.append(('extra-dir/', b'')); self.build()
        self.run_gate()

    def test_file_directory_prefix_collision(self):
        self.receipt['files']['index.html/subfile'] = {'bytes': 1, 'sha256': sha(b'x')}
        self.receipt['fileCount'] += 1
        self.receipt['treeSha256'] = sha(json.dumps(self.receipt['files'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())
        self.build()
        with self.assertRaises(GateError): self.run_gate()

    def test_oversized_receipt(self):
        self.receipt_path.write_bytes(b'x' * (16 * 1024 * 1024 + 1))
        with self.assertRaises(GateError): self.run_gate()

    def test_nonzip(self):
        self.zip.write_bytes(b'not a zip')
        with self.assertRaises(GateError): self.run_gate()

    def test_wrong_pin_format(self):
        with self.assertRaises(GateError): self.run_gate(archive_pin='a')

if __name__ == '__main__': unittest.main()
