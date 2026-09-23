import json
import unittest
from pathlib import Path
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_164.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

class Scan164CrossBorderPhysicalResidualSweepTests(unittest.TestCase):
    def test_scan164_is_zero_retention_and_guard_clean(self):
        scan=load(SCAN)
        self.assertEqual(scan["scan_id"],"ATTRACTION_SCAN_164")
        self.assertEqual(strategic_drift_errors(scan),[])
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])
        self.assertEqual(len(scan["authoritative_closures"]),5)

    def test_every_residual_is_closed_by_current_incumbent_or_expert_rail(self):
        scan=load(SCAN)
        rows={x["formation_id"]:x for x in scan["examined_formations"]}
        self.assertIn("PRODUCTIZED",rows["ATTRACTION_SCAN_164-F1"]["verdict"])
        self.assertIn("PRODUCTIZED",rows["ATTRACTION_SCAN_164-F2"]["verdict"])
        self.assertIn("PROFESSIONAL_QC",rows["ATTRACTION_SCAN_164-F3"]["verdict"])
        self.assertIn("EXPERT_LEGAL_OR_QC",rows["ATTRACTION_SCAN_164-F4"]["verdict"])
        self.assertIn("CURRENT_ONE_TEAM_SERVICES",rows["ATTRACTION_SCAN_164-F5"]["verdict"])

    def test_no_bootstrap_is_authorized_after_incumbent_saturation(self):
        scan=load(SCAN)
        self.assertEqual(scan["bootstrap_queue"],[])
        self.assertEqual(scan["commercial_candidates"],[])
        self.assertEqual(scan["active_transaction_units"],[])
        self.assertEqual(scan["first_external_value_flow"],"NOT_PROVEN")
        self.assertFalse(scan["external_side_effects_performed"])

    def test_scan165_boundary_exits_generic_china_local_help_service_menu(self):
        scan=load(SCAN)
        self.assertEqual(scan["next_scan_id"],"ATTRACTION_SCAN_165")
        boundary=scan["next_search_boundary"]
        self.assertIn("LEAVE_GENERIC_CHINA_LOCAL_HELP",boundary)
        self.assertIn("EXPLICIT_PAID_TASKS_REMAIN_DOWNSTREAM_VALIDATION_ONLY",boundary)

    def test_machine_state_reconciles_scan163_and_advances_scan164(self):
        state=load(STATE)
        self.assertEqual(state["last_completed_scan_id"],"ATTRACTION_SCAN_164")
        self.assertEqual(state["next_scan_id"],"ATTRACTION_SCAN_165")
        self.assertEqual(state["active_commercial_candidates"],[])
        self.assertEqual(state["active_transaction_units"],[])
        self.assertEqual(state["first_external_value_flow"],"NOT_PROVEN")
        s163=state["scan163_cross_border_ground_truth_field"]
        self.assertEqual(s163["final_repository_ci_test_count"],836)
        self.assertEqual(s163["final_jev_next_action"],"ADVANCE_TO_NEXT_SCAN")
        self.assertEqual(s163["retained_research_formations"],[])
        s164=state["scan164_cross_border_physical_residual_sweep"]
        self.assertEqual(s164["retained_research_formations"],[])
        self.assertEqual(s164["bootstrap_queue"],[])

if __name__=="__main__":
    unittest.main()
