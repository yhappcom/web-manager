"""Static/server contract tests; do NOT certify a Chromium or product run."""
import json
import threading
import unittest
from urllib.request import urlopen
from pwa_mixed_generation_browser_lab import APP_JS, LabServer

class LabSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LabServer(('127.0.0.1', 0))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(timeout=2)
    def get(self, path):
        with urlopen(self.origin + path, timeout=2) as r:
            return r.status, r.headers, r.read().decode()
    def test_old_page_is_generation_16(self):
        _, _, html = self.get('/old/')
        self.assertIn('generation=16', html)
    def test_new_page_is_generation_17(self):
        _, _, html = self.get('/new/')
        self.assertIn('generation=17', html)
    def test_both_paths_share_single_script_and_database_name(self):
        _, _, js = self.get('/app.js?generation=16')
        self.assertIn('minttap-synthetic-mixed-generation', js)
        self.assertIn('indexedDB.open(DB_NAME, 1)', js)
        self.assertIn('CAPABILITY_VERSION_GUARD', js)
        self.assertIn('unsafe:', js)
    def test_sw_update_is_byte_distinct_and_no_store(self):
        _, headers, before = self.get('/sw.js')
        self.assertEqual(headers['Cache-Control'], 'no-store')
        self.server.worker_version = 2
        _, _, after = self.get('/sw.js')
        self.assertNotEqual(before, after)
        self.assertIn('const V=2', after)
    def test_worker_intercepts_only_marker_url(self):
        _, _, js = self.get('/sw.js')
        self.assertIn("pathname==='/worker-version'", js)
        self.assertIn('clients.claim()', js)
        self.assertIn('skipWaiting()', js)
    def test_network_fallback_marker(self):
        _, _, value = self.get('/worker-version')
        self.assertEqual(value, 'network-uncontrolled')
    def test_source_separates_synthetic_from_product(self):
        self.assertIn('Not LogMate', __import__('pwa_mixed_generation_browser_lab').__doc__)

if __name__ == '__main__': unittest.main()
