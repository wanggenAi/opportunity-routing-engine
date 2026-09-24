import json
import unittest
from pathlib import Path
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(p.read_text())

class Scan169NamedRetailDisplacementTests(unittest.TestCase):
 def test_named_real_event_and_zero_retention(self):
  x=load(ROOT/'data/research_runs/attraction_scan_169.json')
  self.assertEqual(x['scan_id'],'ATTRACTION_SCAN_169')
  self.assertEqual(strategic_drift_errors(x),[])
  self.assertEqual(len(x['examined_formations']),3)
  self.assertEqual(len(x['authoritative_closures']),3)
  self.assertEqual(x['retained_research_formations'],[])
  self.assertEqual(x['high_attraction_beacons'],[])
 def test_incumbent_action_rail_and_right_disambiguation(self):
  x=load(ROOT/'data/research_runs/attraction_scan_169.json')
  rows={f['formation_id']:f for f in x['examined_formations']}
  self.assertIn('POPUPANGELS',rows['ATTRACTION_SCAN_169-F1']['decisive_action_gate_owner_state'])
  self.assertIn('CUSTOMER',rows['ATTRACTION_SCAN_169-F2']['decisive_action_gate_owner_state'])
  self.assertIn('LANDLORD',rows['ATTRACTION_SCAN_169-F3']['decisive_action_gate_owner_state'])
  for f in rows.values():
   self.assertTrue(f['discriminating_falsifier'])
   self.assertTrue(f['observed_partial_flow'])
   self.assertTrue(f['material_contradictions'])
  self.assertEqual(x['bootstrap_queue'],[])
  self.assertEqual(x['commercial_candidates'],[])
  self.assertEqual(x['active_transaction_units'],[])
  self.assertEqual(x['first_external_value_flow'],'NOT_PROVEN')
 def test_prior_merge_reconciled_and_epoch_advances(self):
  s=load(ROOT/'data/commercial_reset_state.json')
  self.assertGreaterEqual(int(s['last_completed_scan_id'].rsplit('_',1)[1]),169)
  self.assertGreaterEqual(int(s['next_scan_id'].rsplit('_',1)[1]),170)
  prev=s['scan168_asean_fragmented_ops_action_rails']
  self.assertEqual(prev['final_repository_ci_test_count'],855)
  self.assertEqual(prev['final_jev_run_id'],35949798489)
  self.assertEqual(prev['merged_pr'],483)
  self.assertEqual(s['scan169_named_retail_displacement_control_preflight']['retained_research_formations'],[])
if __name__=='__main__': unittest.main()
