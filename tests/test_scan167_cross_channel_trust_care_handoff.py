import json
import unittest
from pathlib import Path
from src.strategic_drift_guard import strategic_drift_errors
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads(path.read_text())
class Scan167RealityTrustCareTests(unittest.TestCase):
 def test_current_reality_scan_is_truth_bound_and_guard_clean(self):
  x=load(ROOT/'data/research_runs/attraction_scan_167.json')
  self.assertEqual(x['scan_id'],'ATTRACTION_SCAN_167')
  self.assertEqual(strategic_drift_errors(x),[])
  self.assertEqual(len(x['examined_formations']),3)
  self.assertEqual(len(x['authoritative_closures']),3)
  self.assertEqual(x['high_attraction_beacons'],[])
  self.assertEqual(x['retained_research_formations'],[])
 def test_no_counterfactual_or_regulated_right_is_promoted(self):
  x=load(ROOT/'data/research_runs/attraction_scan_167.json')
  rows={f['formation_id']:f for f in x['examined_formations']}
  self.assertIn('BRAND_GRANT',rows['ATTRACTION_SCAN_167-F1']['decisive_action_gate_owner_state'])
  self.assertIn('GOVERNMENT_PERMISSION',rows['ATTRACTION_SCAN_167-F2']['decisive_action_gate_owner_state'])
  self.assertIn('MARKETPLACE_ACCOUNT_PERMISSION',rows['ATTRACTION_SCAN_167-F3']['decisive_action_gate_owner_state'])
  self.assertEqual(x['bootstrap_queue'],[])
  self.assertEqual(x['commercial_candidates'],[])
  self.assertEqual(x['first_external_value_flow'],'NOT_PROVEN')
 def test_commercial_machine_epoch_is_monotonic(self):
  s=load(ROOT/'data/commercial_reset_state.json')
  self.assertGreaterEqual(int(s['last_completed_scan_id'].rsplit('_',1)[1]),167)
  self.assertGreaterEqual(int(s['next_scan_id'].rsplit('_',1)[1]),168)
  self.assertEqual(s['scan166_domestic_payment_smart_consumption_ownership']['final_repository_ci_run_id'],35915566482)
  self.assertEqual(s['scan166_domestic_payment_smart_consumption_ownership']['final_jev_run_id'],35915566528)
  self.assertEqual(s['scan167_cross_channel_trust_care_handoff']['retained_research_formations'],[])
if __name__=='__main__': unittest.main()
