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
    return dict(run_id='synthetic-test',workflow_url='https://example.test/ci/1',browser='Chromium',browser_version='142.0.0.0',platform='linux',source_v16=OLD,source_v17=V17,v16_build_sha256='b'*64,v17_build_sha256='c'*64,build_kind='test_instrumented',origin=origin,profile_id=profile,fixture_kind='synthetic_no_personal_data',evidence_kind='real_chrome',events=[
        dict(kind='old_open',process_id='p1',tab_id='old',tab_state='open',binary_sha=OLD,build_sha256='b'*64,capability=16,**common),
        dict(kind='migration',process_id='p1',tab_id='new',old_tab_still_open=True,binary_sha=V17,build_sha256='c'*64,capability=17,store_count=37,ledger_digest=D,remote_receipts=0,remote_authority=False,unsynced_count=2,**common),
        dict(kind='stale_write',process_id='p1',tab_id='old',old_tab_still_open=True,binary_sha=OLD,build_sha256='b'*64,method='commitLedgerMutation',outcome='rejected',error_code='capability_mismatch',preconditions_validated=True,capability_marker_observed=17,rejection_class='capability_version_guard',before_digest=D,after_digest=D,remote_receipts=0,remote_authority=False,unsynced_count=2,**common),
        dict(kind='browser_exit',process_id='p1',outcome='closed',all_tabs_closed=True,**common),
        dict(kind='restart_readback',process_id='p2',binary_sha=V17,build_sha256='c'*64,profile_reused=True,reseeded=False,capability=17,store_count=37,ledger_digest=D,remote_receipts=0,remote_authority=False,unsynced_count=2,**common)])

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

    def test_old_event_artifact_mismatch_rejected(self):
        t=fixture();t['events'][0]['build_sha256']='d'*64;self.assertEqual(assess(t)[0],'INVALID')
    def test_stale_event_artifact_mismatch_rejected(self):
        t=fixture();t['events'][2]['build_sha256']='d'*64;self.assertEqual(assess(t)[0],'INVALID')
    def test_restart_artifact_mismatch_rejected(self):
        t=fixture();t['events'][4]['build_sha256']='d'*64;self.assertEqual(assess(t)[0],'INVALID')
    def test_old_tab_closed_before_migration_rejected(self):
        t=fixture();t['events'][1]['old_tab_still_open']=False;self.assertEqual(assess(t)[0],'INVALID')
    def test_old_tab_closed_before_write_rejected(self):
        t=fixture();t['events'][2]['old_tab_still_open']=False;self.assertEqual(assess(t)[0],'INVALID')
    def test_rejection_from_wrong_precondition_rejected(self):
        t=fixture();t['events'][2]['preconditions_validated']=False;self.assertEqual(assess(t)[0],'INVALID')
    def test_owner_lock_not_capability_rejection_rejected(self):
        t=fixture();t['events'][2]['rejection_class']='owner_locked';self.assertEqual(assess(t)[0],'INVALID')
    def test_old_capability_marker_rejected(self):
        t=fixture();t['events'][2]['capability_marker_observed']=16;self.assertEqual(assess(t)[0],'INVALID')
    def test_false_profile_reuse_rejected(self):
        t=fixture();t['events'][4]['profile_reused']=False;self.assertEqual(assess(t)[0],'INVALID')
    def test_restart_reseed_rejected(self):
        t=fixture();t['events'][4]['reseeded']=True;self.assertEqual(assess(t)[0],'INVALID')
    def test_boolean_receipt_count_rejected(self):
        t=fixture();t['events'][1]['remote_receipts']=False;self.assertEqual(assess(t)[0],'INVALID')
    def test_boolean_unsynced_count_rejected(self):
        t=fixture();t['events'][2]['unsynced_count']=True;self.assertEqual(assess(t)[0],'INVALID')
    def test_origin_with_credentials_rejected(self):
        t=fixture();t['origin']='https://user:secret@example.test';self.assertEqual(assess(t)[0],'INVALID')
    def test_malformed_port_rejected(self):
        t=fixture();t['origin']='https://example.test:99999';self.assertEqual(assess(t)[0],'INVALID')
    def test_non_numeric_browser_version_rejected(self):
        t=fixture();t['browser_version']='synthetic';self.assertEqual(assess(t)[0],'INVALID')
    def test_missing_process_closure_rejected(self):
        t=fixture();t['events'][3]['all_tabs_closed']=False;self.assertEqual(assess(t)[0],'INVALID')

if __name__=='__main__':unittest.main()
