import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELD = ROOT / "docs" / "field" / "FIELD_RUN_001_XINDIE_2026-09-15.md"
ACCESS_MISSION = ROOT / "docs" / "field" / "ACCESS_CAPITAL_MISSION_001_TECH_MANAGER_ROUTE_2026-09-15.md"
CANONICAL_ACCESS = ROOT / "docs" / "ACCESS_FEASIBILITY_GATE.md"


class FieldRun001AccessGateTests(unittest.TestCase):
    def test_field_run_does_not_confuse_public_contact_with_access(self):
        text = FIELD.read_text(encoding="utf-8")
        self.assertIn("ACCESS_BLOCKED", text)
        self.assertIn("PUBLICLY_REACHABLE = YES", text)
        self.assertIn("DIRECT ENTERPRISE PROBE = HOLD", text)
        self.assertIn("PUBLICLY_REACHABLE\n→ INTRODUCTION_READY", text)
        self.assertIn("docs/ACCESS_FEASIBILITY_GATE.md", text)

    def test_operator_profile_remains_runtime_private(self):
        text = FIELD.read_text(encoding="utf-8")
        self.assertIn("RUNTIME_PRIVATE / NOT COMMITTED", text)
        self.assertIn("RUNTIME_PRIVATE_NOT_COMMITTED", text)

    def test_counterparty_surplus_precedes_task_probe(self):
        text = FIELD.read_text(encoding="utf-8")
        self.assertIn("COUNTERPART-VISIBLE SURPLUS", text)
        self.assertIn("HOOK HYPOTHESIS != COUNTERPART INTEREST", text)
        self.assertIn("EARN CONVERSATION PERMISSION", text)
        self.assertIn("THEN ASK FOR TASK TRUTH", text)

    def test_access_mission_requires_operational_role_not_certificate(self):
        text = ACCESS_MISSION.read_text(encoding="utf-8")
        self.assertIn("ACCESS_CAPITAL_OPERATIONAL", text)
        self.assertIn("No certificate, training attendance or platform registration alone", text)
        self.assertIn("SUPERVISED_CASE_ASSIGNED", text)
        self.assertIn("FORMAL_INTRODUCTION_GRANTED", text)
        self.assertIn("Question 8 is mandatory", text)

    def test_existing_canonical_gate_remains_parent(self):
        canonical = CANONICAL_ACCESS.read_text(encoding="utf-8")
        self.assertIn("VALUE / EXCHANGE TRUTH", canonical)
        self.assertIn("CURRENT OPERATOR ACCESS FEASIBILITY", canonical)
        self.assertIn("COUNTERPARTY VISIBLE SURPLUS", canonical)
        self.assertIn("RUNTIME_PRIVATE", (ROOT / "data" / "cycle002_access_feasibility_2026-09-12.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
