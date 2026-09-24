import json
import unittest
from pathlib import Path
from src.strategic_drift_guard import strategic_drift_errors
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(p.read_text())
class Scan168AseanOpsRailsTests(unittest.TestCase):
 def test_broad_source_and_zero_retention(self):
  x=load(ROOT/'data/research_runs/attraction_scan_168.json')
  self.assertEqual(x['scan_id'],'ATTRACTION_SCAN_168')
  self.assertEqual(strategic_drift_errors(x),[])
  self.assertEqual(len(x['examined_formations']),3)
  self.assertEqual(len(x['authoritative_closures']),3)
  self.assertEqual(x['retained_research_formations'],[])
  self.assertEqual(x['high_attraction_beacons'],[])
 def test_independent_evidence_not_vendor_marketing_promoted(self):
  x=load(ROOT/'data/research_runs/attraction_scan_168.json')
  rows={f['formation_id']:f for f in x['examined_formations']}
  self.assertIn('LOCUS_SPOT_RFQ',rows['ATTRACTION_SCAN_168-F1']['decisive_action_gate_owner_state'])
  self.assertIn('KINTONE',rows['ATTRACTION_SCAN_168-F2']['decisive_action_gate_owner_state'])
  self.assertIn('ZKH',rows['ATTRACTION_SCAN_168-F3']['decisive_action_gate_owner_state'])
  self.assertEqual(x['bootstrap_queue'],[])
  self.assertEqual(x['commercial_candidates'],[])
  self.assertEqual(x['first_external_value_flow'],'NOT_PROVEN')
 def test_prior_verified_merge_and_monotonic_epoch(self):
  s=load(ROOT/'data/commercial_reset_state.json')
  self.assertGreaterEqual(int(s['last_completed_scan_id'].rsplit('_',1)[1]),168)
  self.assertGreaterEqual(int(s['next_scan_id'].rsplit('_',1)[1]),169)
  s167=s['scan167_cross_channel_trust_care_handoff']
  self.assertEqual(s167['final_repository_ci_test_count'],852)
  self.assertEqual(s167['final_jev_run_id'],35949289463)
  self.assertEqual(s167['merged_pr'],482)
  self.assertEqual(s['scan168_asean_fragmented_ops_action_rails']['retained_research_formations'],[])
if __name__=='__main__': unittest.main()
