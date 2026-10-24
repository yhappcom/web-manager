import hashlib
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
import pwa_served_byte_gate as gate


def digest(b):
    return hashlib.sha256(b).hexdigest()


class FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        key = self.path.lstrip('/')
        cfg = self.server.config
        if key in cfg.get('redirect', set()):
            self.send_response(302)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return
        if key in cfg.get('missing', set()):
            self.send_error(404)
            return
        body = cfg['files'].get(key, b'')
        if key in cfg.get('mutate', {}):
            body = cfg['mutate'][key]
        self.send_response(200)
        typ = 'application/javascript' if key.endswith('.js') else 'text/html' if key.endswith('.html') else 'application/json' if key.endswith('.json') else 'application/wasm' if key.endswith('.wasm') else 'text/plain'
        typ = cfg.get('types', {}).get(key, typ)
        self.send_header('Content-Type', typ)
        self.send_header('Cache-Control', cfg.get('cache', {}).get(key, 'no-cache, no-store'))
        if key in cfg.get('encoding', {}):
            self.send_header('Content-Encoding', cfg['encoding'][key])
        self.send_header('Content-Length', str(len(body) + cfg.get('length_bias', {}).get(key, 0)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass
    def log_message(self, *args):
        pass


class TestServedGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), FixtureHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.files = {p: (b'data:' + p.encode()) for p in gate.REQUIRED}
        self.files['extra.txt'] = b'extra'
        self.server.config = {'files': self.files}
        inv = {p: {'bytes': len(b), 'sha256': digest(b)} for p, b in self.files.items()}
        self.receipt = {'schema': 1, 'kind': 'normal', 'files': inv, 'fileCount': len(inv),
                        'workerSha256': inv['logmate_service_worker.js']['sha256'],
                        'treeSha256': digest(json.dumps(inv, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())}
        self.raw = json.dumps(self.receipt).encode()
        self.pin = digest(self.raw)

    def run_gate(self, scope='critical'):
        return gate.audit(self.raw, self.pin, self.origin, scope=scope, allow_loopback=True)

    def test_critical_two_rounds(self):
        result = self.run_gate()
        self.assertEqual(result['verdict'], 'HOST_CRITICAL_MATCH_UNVERIFIED')
        self.assertEqual(result['checkedRequests'], 16)

    def test_all_tree_two_rounds(self):
        result = self.run_gate('all')
        self.assertEqual(result['checkedRequests'], 18)

    def test_mutated_critical_bytes_rejected(self):
        self.server.config['mutate'] = {'main.dart.js': b'evil'}
        with self.assertRaisesRegex(gate.GateError, 'Content-Length mismatch|served bytes differ'):
            self.run_gate()

    def test_mutated_unlisted_file_detected_only_all(self):
        self.server.config['mutate'] = {'extra.txt': b'other'}
        self.run_gate()
        with self.assertRaisesRegex(gate.GateError, 'served bytes differ'):
            self.run_gate('all')

    def test_redirect_rejected(self):
        self.server.config['redirect'] = {'index.html'}
        with self.assertRaisesRegex(gate.GateError, 'redirect rejected'):
            self.run_gate()

    def test_missing_rejected(self):
        self.server.config['missing'] = {'index.html'}
        with self.assertRaisesRegex(gate.GateError, 'HTTP transport failed'):
            self.run_gate()

    def test_html_fallback_rejected(self):
        self.server.config['types'] = {'main.dart.js': 'text/html'}
        with self.assertRaisesRegex(gate.GateError, 'unexpected content type'):
            self.run_gate()

    def test_compressed_rejected(self):
        self.server.config['encoding'] = {'main.dart.js': 'gzip'}
        with self.assertRaisesRegex(gate.GateError, 'content-encoding'):
            self.run_gate()

    def test_mutable_cache_missing(self):
        self.server.config['cache'] = {'logmate_service_worker.js': 'public, max-age=3600'}
        with self.assertRaisesRegex(gate.GateError, 'cache policy'):
            self.run_gate()

    def test_declared_length_wrong(self):
        self.server.config['length_bias'] = {'main.dart.js': 5}
        with self.assertRaisesRegex(gate.GateError, 'Content-Length mismatch'):
            self.run_gate()

    def test_receipt_pin_mismatch(self):
        with self.assertRaisesRegex(gate.GateError, 'independent SHA'):
            gate.audit(self.raw, '0' * 64, self.origin, allow_loopback=True)

    def test_acceptance_receipt_rejected(self):
        r = dict(self.receipt, kind='acceptance')
        b = json.dumps(r).encode()
        with self.assertRaisesRegex(gate.GateError, 'NORMAL'):
            gate.audit(b, digest(b), self.origin, allow_loopback=True)

    def test_receipt_self_consistency(self):
        r = dict(self.receipt, workerSha256='0' * 64)
        b = json.dumps(r).encode()
        with self.assertRaisesRegex(gate.GateError, 'self-consistency'):
            gate.audit(b, digest(b), self.origin, allow_loopback=True)

    def test_path_traversal_rejected(self):
        self.assertRaises(gate.GateError, gate.path_check, '../secret')
        self.assertRaises(gate.GateError, gate.path_check, 'a%2fb')
        self.assertRaises(gate.GateError, gate.path_check, '/abs')

    def test_non_https_rejected(self):
        with self.assertRaisesRegex(gate.GateError, 'HTTPS'):
            gate.origin_base(self.origin, False)

    def test_credentials_query_rejected(self):
        self.assertRaises(gate.GateError, gate.origin_base, 'https://user:pw@example.com', False)
        self.assertRaises(gate.GateError, gate.origin_base, 'https://example.com/?x=1', False)

    def test_one_round_rejected(self):
        with self.assertRaisesRegex(gate.GateError, 'rounds'):
            gate.audit(self.raw, self.pin, self.origin, rounds=1, allow_loopback=True)

    def test_invalid_scope_rejected(self):
        with self.assertRaisesRegex(gate.GateError, 'scope'):
            gate.audit(self.raw, self.pin, self.origin, scope='partial', allow_loopback=True)


if __name__ == '__main__':
    unittest.main()
