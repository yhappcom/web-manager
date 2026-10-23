"""Synthetic contract tests only. They are not browser product validation."""
import copy
import unittest
from mixed_generation_trace_gate import assess, V17

OLD = '59cd171176c58b598a4db55d128ffd21d406e862'  # exact historical SHA; trace itself is synthetic
D = 'a' * 64

def fixture():
    origin='https://example.test'
    profile='sha256:synthetic-profile'
    common=dict(origin=origin, profile_id=profile)
    return dict(run_id='synthetic-test',workflow_url='https://example.test/ci/1',browser='Chromium',browser_version='synthetic',platform='linux',source_v16=OLD,source_v17=V17,v16_build_sha256='b'*64,v17_build_sha256='c'*64,build_kind='test_instrumented',origin=origin,profile_id=profile,fixture_kind='synthetic_no_personal_data',evidence_kind='real_chrome',events=[
        dict(kind='old_open',process_id='p1',tab_id='old',binary_sha=OLD,capability=16,**common),
        dict(kind='migration',process_id='p1',tab_id='new',binary_sha=V17,capability=17,store_count=37,ledger_digest=D,remote_receipts=0,remote_authority=False,unsynced_count=2,**common),
        dict(kind='stale_write',process_id='p1',tab_id='old',binary_sha=OLD,method='commitLedgerMutation',outcome='rejected',error_code='capability_mismatch',before_digest=D,after_digest=D,remote_receipts=0,remote_authority=False,unsynced_count=2,**common),
        dict(kind='browser_exit',process_id='p1',outcome='closed',**common),
        dict(kind='restart_readback',process_id='p2',binary_sha=V17,capability=17,store_count=37,ledger_digest=D,remote_receipts=0,remote_authority=False,unsynced_count=2,**common)])

class GateTests(unittest.TestCase):
    def test_shape_reference_pass(self):
        self.assertEqual(assess(fixture())[0], 'TRACE_CONSISTENT_UNVERIFIED')
    def test_synthetic_flag_rejected(self):
        t=fixture();t['evidence_kind']='synthetic';self.assertEqual(assess(t)[0],'INVALID')
    def test_missing_migration_rejected(self):
        t=fixture();del t['events'][1];self.assertEqual(assess(t)[0],'INVALID')
    def test_wrong_origin_rejected(self):
        t=fixture();t['events'][2]['origin']='https://other.test';self.assertEqual(assess(t)[0],'INVALID')
    def test_changed_profile_rejected(self):
        t=fixture();t['events'][4]['profile_id']='new';self.assertEqual(assess(t)[0],'INVALID')
    def test_same_process_restart_rejected(self):
        t=fixture();t['events'][4]['process_id']='p1';self.assertEqual(assess(t)[0],'INVALID')
    def test_wrong_binary_rejected(self):
        t=fixture();t['events'][2]['binary_sha']=V17;self.assertEqual(assess(t)[0],'INVALID')
    def test_wrong_method_rejected(self):
        t=fixture();t['events'][2]['method']='create';self.assertEqual(assess(t)[0],'INVALID')
    def test_stale_write_accepted_rejected(self):
        t=fixture();t['events'][2]['outcome']='accepted';self.assertEqual(assess(t)[0],'INVALID')
    def test_stale_mutates_data_rejected(self):
        t=fixture();t['events'][2]['after_digest']='c'*64;self.assertEqual(assess(t)[0],'INVALID')
    def test_receipt_fabrication_rejected(self):
        t=fixture();t['events'][4]['remote_receipts']=1;self.assertEqual(assess(t)[0],'INVALID')
    def test_unsynced_loss_rejected(self):
        t=fixture();t['events'][4]['unsynced_count']=0;self.assertEqual(assess(t)[0],'INVALID')
    def test_wrong_store_count_rejected(self):
        t=fixture();t['events'][4]['store_count']=30;self.assertEqual(assess(t)[0],'INVALID')
    def test_no_real_source_pin_rejected(self):
        t=fixture();t['source_v17']='c'*40;self.assertEqual(assess(t)[0],'INVALID')
    def test_insecure_origin_rejected(self):
        t=fixture();t['origin']='http://example.test';self.assertEqual(assess(t)[0],'INVALID')
    def test_bad_artifact_digest_rejected(self):
        t=fixture();t['v17_build_sha256']='oops';self.assertEqual(assess(t)[0],'INVALID')

if __name__=='__main__':unittest.main()
