import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).with_name('pwa_worker_claim_browser_probe.py')
spec = importlib.util.spec_from_file_location('probe_module', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class VerdictTests(unittest.TestCase):
    def baseline(self):
        return {'first_claim_asset': {'status': 200}, 'controlled_asset': {'status': 200},
                'offline_asset': {'status': 200}, 'cold_process_asset': {'status': 200},
                'controlled_reload_status': 200, 'offline_reload_status': 200,
                'cold_process_reopen_status': 200}
    def test_complete_success(self):
        self.assertEqual(module.classify(self.baseline()), 'BOUNDED_CHROMIUM_PATH_PASS')
    def test_initial_503(self):
        x=self.baseline();x['first_claim_asset']['status']=503
        self.assertEqual(module.classify(x), 'FIRST_CLAIM_ASSET_FAILURE_OBSERVED')
    def test_initial_404(self):
        x=self.baseline();x['first_claim_asset']['status']=404
        self.assertEqual(module.classify(x), 'FIRST_CLAIM_ASSET_FAILURE_OBSERVED')
    def test_controlled_asset_failure(self):
        x=self.baseline();x['controlled_asset']['status']=503
        self.assertEqual(module.classify(x), 'RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED')
    def test_offline_asset_failure(self):
        x=self.baseline();x['offline_asset']['status']=503
        self.assertEqual(module.classify(x), 'RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED')
    def test_cold_asset_failure(self):
        x=self.baseline();x['cold_process_asset']['status']=503
        self.assertEqual(module.classify(x), 'RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED')
    def test_cold_nav_failure(self):
        x=self.baseline();x['cold_process_reopen_status']=404
        self.assertEqual(module.classify(x), 'RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED')
    def test_offline_nav_failure(self):
        x=self.baseline();x['offline_reload_status']=404
        self.assertEqual(module.classify(x), 'RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED')
    def test_incomplete_cannot_pass(self):
        x=self.baseline();del x['cold_process_asset']
        self.assertEqual(module.classify(x), 'INCOMPLETE_OR_ERROR')
    def test_bad_status_cannot_pass(self):
        x=self.baseline();x['first_claim_asset']['status']='200'
        self.assertEqual(module.classify(x), 'INCOMPLETE_OR_ERROR')
    def test_empty_cannot_pass(self):
        self.assertEqual(module.classify({}), 'INCOMPLETE_OR_ERROR')

if __name__=='__main__': unittest.main()
