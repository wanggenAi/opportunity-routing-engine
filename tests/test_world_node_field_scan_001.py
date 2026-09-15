import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "docs" / "field" / "WORLD_NODE_FIELD_SCAN_001_XUZHOU_2026-09-16.md"


class WorldNodeFieldScan001Tests(unittest.TestCase):
    def test_selected_route_is_not_founder_cold_discovery(self):
        text = SCAN.read_text(encoding="utf-8")
        self.assertIn("PUBLIC_TECH_DEMAND_STREAM → CAPABILITY / INSTITUTION ROUTING", text)
        self.assertIn("FOUNDER_SELF-EXECUTION = NOT REQUIRED BY DESIGN", text)
        self.assertIn("Founder is **not** the motor-control engineer", text)

    def test_route_contains_heterogeneous_nodes(self):
        text = SCAN.read_text(encoding="utf-8")
        for token in [
            "DEMAND_STREAM_NODE",
            "INSTITUTION / ACCESS NODE",
            "DOMAIN_ANALYST NODE",
            "CAPABILITY_PROVIDER NODE",
            "CONTRACT / IP / ACCEPTANCE NODE",
        ]:
            self.assertIn(token, text)

    def test_public_visibility_does_not_promote_transaction_truth(self):
        text = SCAN.read_text(encoding="utf-8")
        self.assertIn("DEMAND_STREAM_VISIBLE != ECONOMIC_COMMITMENT", text)
        self.assertIn("ROUTE_VALIDATION_READY", text)
        self.assertIn("Are the public `进行中` demand records operationally current", text)

    def test_nonfounder_node_required_before_route_testable_promotion(self):
        text = SCAN.read_text(encoding="utf-8")
        self.assertIn("ONE NON-FOUNDER DOMAIN ANALYST / CAPABILITY NODE OPTIONED", text)
        self.assertIn("ONE LEGITIMATE INTRODUCTION OR SOLUTION SUBMISSION", text)
        self.assertIn("ECONOMIC / ATTRIBUTION TERMS KNOWN", text)

    def test_instrument_and_aftermarket_routes_are_not_false_promotions(self):
        text = SCAN.read_text(encoding="utf-8")
        self.assertIn("STRUCTURALLY_INTERESTING / PAYER_GAP_UNKNOWN", text)
        self.assertIn("HIGH_LONG_TERM_FIT / HIGHER_FIRST-ROUTE FRICTION", text)
        self.assertIn("STRUCTURE_VALIDATION_READY / NOT FIRST ROUTE", text)


if __name__ == "__main__":
    unittest.main()
