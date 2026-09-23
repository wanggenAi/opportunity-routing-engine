import json
import unittest
from pathlib import Path
from src.strategic_drift_guard import strategic_drift_errors

ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_166.json"
STATE=ROOT/"data"/"commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text())

class Scan166DomesticPaymentSmartConsumptionOwnershipTests(unittest.TestCase):
    def test_scan166_is_broad_zero_retention_and_guard_clean(self):
        scan=load(SCAN)
        self.assertEqual(scan["scan_id"],"ATTRACTION_SCAN_166")
        self.assertEqual(strategic_drift_errors(scan),[])
        self.assertEqual(scan["high_attraction_beacons"],[])
        self.assertEqual(scan["retained_research_formations"],[])
        self.assertEqual(len(scan["authoritative_closures"]),5)
        self.assertTrue(scan["drift_audit"]["broad_reality_not_inherited_from_scan165_vertical"])

    def test_each_current_state_change_has_an_owned_action_gate(self):
        scan=load(SCAN)
        rows={x["formation_id"]:x for x in scan["examined_formations"]}
        self.assertIn("MIIT_NATIONAL_COMPLAINT",rows["ATTRACTION_SCAN_166-F1"]["decisive_action_gate_owner_state"])
        self.assertIn("SHCPE",rows["ATTRACTION_SCAN_166-F2"]["decisive_action_gate_owner_state"])
        self.assertIn("SMART_HOME_PLATFORM",rows["ATTRACTION_SCAN_166-F3"]["decisive_action_gate_owner_state"])
        self.assertIn("RETAILER_AND_AUTHORIZED_RECYCLER",rows["ATTRACTION_SCAN_166-F4"]["decisive_action_gate_owner_state"])
        self.assertIn("PROFESSIONAL_FITTING_NETWORK",rows["ATTRACTION_SCAN_166-F5"]["decisive_action_gate_owner_state"])

    def test_no_bootstrap_or_commercial_promotion(self):
        scan=load(SCAN)
        self.assertEqual(scan["bootstrap_queue"],[])
        self.assertEqual(scan["commercial_candidates"],[])
        self.assertEqual(scan["active_transaction_units"],[])
        self.assertEqual(scan["first_external_value_flow"],"NOT_PROVEN")
        self.assertFalse(scan["external_side_effects_performed"])

    def test_machine_state_reconciles_scan165_and_advances_scan166(self):
        state=load(STATE)
        self.assertGreaterEqual(int(state["last_completed_scan_id"].rsplit("_",1)[1]),166)
        self.assertGreaterEqual(int(state["next_scan_id"].rsplit("_",1)[1]),167)
        s165=state["scan165_cross_customs_return_routing"]
        self.assertEqual(s165["final_repository_ci_test_count"],845)
        self.assertEqual(s165["final_jev_next_action"],"ADVANCE_TO_NEXT_SCAN")
        self.assertEqual(s165["retained_research_formations"],[])
        s166=state["scan166_domestic_payment_smart_consumption_ownership"]
        self.assertEqual(s166["retained_research_formations"],[])
        self.assertEqual(s166["bootstrap_queue"],[])

if __name__=="__main__":
    unittest.main()
