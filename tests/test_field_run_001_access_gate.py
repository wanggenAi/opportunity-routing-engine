import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELD = ROOT / "docs" / "field" / "FIELD_RUN_001_XINDIE_2026-09-15.md"
ACCESS_MISSION = ROOT / "docs" / "field" / "ACCESS_CAPITAL_MISSION_001_TECH_MANAGER_ROUTE_2026-09-15.md"
ORCHESTRATOR = ROOT / "docs" / "field" / "ORCHESTRATOR_ROLE_AND_EXTERNAL_ARCHETYPES_2026-09-15.md"
CANONICAL_ACCESS = ROOT / "docs" / "ACCESS_FEASIBILITY_GATE.md"


class FieldRun001AccessGateTests(unittest.TestCase):
    def test_field_run_does_not_confuse_public_contact_with_access(self):
        text = FIELD.read_text(encoding="utf-8")
        self.assertIn("ACCESS_BLOCKED", text)
        self.assertIn("PUBLICLY_REACHABLE = YES", text)
        self.assertIn("DIRECT FOUNDER ENTERPRISE PROBE = HOLD", text)
        self.assertIn("PUBLICLY_REACHABLE\n→ SCOUT_OR_ACCESS_PATH_DISCOVERED", text)
        self.assertIn("docs/ACCESS_FEASIBILITY_GATE.md", text)

    def test_founder_is_not_default_field_scout(self):
        text = FIELD.read_text(encoding="utf-8")
        self.assertIn("Founder/operator role boundary", text)
        self.assertIn("not the default field researcher", text)
        self.assertIn("Field Scout protocol", text)
        self.assertIn("founder_roles_performed:", text)
        self.assertIn("which_role_should_be_external_next:", text)

    def test_counterparty_surplus_and_scout_incentive_precede_task_probe(self):
        text = FIELD.read_text(encoding="utf-8")
        self.assertIn("COUNTERPART-VISIBLE SURPLUS", text)
        self.assertIn("scout_incentive:", text)
        self.assertIn("HOOK HYPOTHESIS != COUNTERPART INTEREST", text)
        self.assertIn("ALIGN THE SCOUT'S INCENTIVE", text)
        self.assertIn("CAPTURE QUALIFIED TASK TRUTH", text)

    def test_access_mission_treats_technology_manager_as_routable_capability(self):
        text = ACCESS_MISSION.read_text(encoding="utf-8")
        self.assertIn("ROUTABLE ACCESS CAPABILITY", text)
        self.assertIn("ACCESS_PROVIDER", text)
        self.assertIn("FIELD_SCOUT", text)
        self.assertIn("No certificate, training attendance, platform registration", text)
        self.assertIn("SCOUT_OPTIONED", text)
        self.assertIn("Questions 4, 5, 7 and 9 are mandatory", text)

    def test_orchestrator_contract_prevents_self_employment_collapse(self):
        text = ORCHESTRATOR.read_text(encoding="utf-8")
        self.assertIn("Orchestrator / Principal / Routing Control Plane", text)
        self.assertIn("Founder execution is therefore a **calibration exception**", text)
        self.assertIn("FIELD SCOUT / NEED DISCOVERY", text)
        self.assertIn("CAPABILITY PROVIDER / EXECUTOR", text)
        self.assertIn("A route whose economics disappear when the founder stops doing operational labor", text)
        self.assertIn("GLG", text)
        self.assertIn("Xometry", text)
        self.assertIn("Li & Fung", text)
        self.assertIn("Full Truck Alliance", text)

    def test_existing_canonical_gate_remains_parent(self):
        canonical = CANONICAL_ACCESS.read_text(encoding="utf-8")
        self.assertIn("VALUE / EXCHANGE TRUTH", canonical)
        self.assertIn("CURRENT OPERATOR ACCESS FEASIBILITY", canonical)
        self.assertIn("COUNTERPARTY VISIBLE SURPLUS", canonical)
        self.assertIn("RUNTIME_PRIVATE", (ROOT / "data" / "cycle002_access_feasibility_2026-09-12.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
