import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FlowPotentialLaunchContractTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_flow_potential_requires_more_than_idle_resource(self):
        doctrine = self._read("docs/FLOW_POTENTIAL_DOCTRINE.md")
        self.assertIn("CANONICAL / LOCKED PRINCIPLE", doctrine)
        self.assertIn("IDLE / UNDERUSED RESOURCE", doctrine)
        self.assertIn("EVIDENCED VALUED OUTCOME / PAYING DEMAND", doctrine)
        self.assertIn("EVIDENCED TRANSACTION FRICTION", doctrine)
        self.assertIn("A BRIDGEABLE ROUTE", doctrine)
        self.assertIn("UNDERUSE != DEMAND", doctrine)
        self.assertIn("COMPLEMENTARITY != ROUTE", doctrine)
        self.assertIn("ROUTE != TRANSACTION", doctrine)

    def test_people_are_actors_not_inventory(self):
        doctrine = self._read("docs/FLOW_POTENTIAL_DOCTRINE.md")
        self.assertIn("A person is an `ACTOR`, not a resource inventory item", doctrine)
        self.assertIn("PERSON = ACTOR", doctrine)
        self.assertIn("TIME / SKILL / KNOWLEDGE / EXPERIENCE / TRUST / ACCESS", doctrine)
        self.assertIn("fair and transparent", doctrine)

    def test_field_truth_outranks_internal_completeness_during_launch(self):
        mission = self._read("docs/launch/FIRST_EXTERNAL_VALUE_FLOW_MISSION_2026-09-15.md")
        self.assertIn("P0 / LAUNCH MODE / ARCHITECTURE FREEZE", mission)
        self.assertIn("FIELD TRUTH > INTERNAL COMPLETENESS", mission)
        self.assertIn("within 72 hours", mission)
        self.assertIn("within 14 calendar days", mission)
        self.assertIn("ECONOMIC_COMMITMENT", mission)
        self.assertIn("SETTLED", mission)

    def test_first_value_flow_cannot_be_simulated(self):
        mission = self._read("docs/launch/FIRST_EXTERNAL_VALUE_FLOW_MISSION_2026-09-15.md")
        self.assertIn("Money may be small. It must be real", mission)
        self.assertIn("symbolic transfer", mission)
        self.assertIn("simulated transaction does not pass", mission)
        self.assertIn("FIRST_EXTERNAL_VALUE_FLOW = PASS", mission)
        self.assertIn("objective acceptance event", mission)
        self.assertIn("settlement occurred", mission)

    def test_launch_does_not_redefine_core_identity(self):
        mission = self._read("docs/launch/FIRST_EXTERNAL_VALUE_FLOW_MISSION_2026-09-15.md")
        self.assertIn("first transaction-calibration route", mission)
        self.assertIn("must not redefine the project as a generic outsourcing business", mission)
        self.assertIn("not permanent self-employment disguised as orchestration", mission)


if __name__ == "__main__":
    unittest.main()
