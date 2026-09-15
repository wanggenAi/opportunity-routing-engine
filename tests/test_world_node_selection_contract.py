import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODES = ROOT / "docs" / "field" / "ROUTABLE_WORLD_NODES_2026-09-16.md"
SELECT = ROOT / "docs" / "field" / "WORLD_NODE_SELECTION_CONTRACT_2026-09-16.md"


class WorldNodeSelectionContractTests(unittest.TestCase):
    def test_orchestration_unit_is_not_person_only(self):
        text = SELECT.read_text(encoding="utf-8")
        self.assertIn("The unit of orchestration is therefore not `person` or `supplier`", text)
        self.assertIn("CALLABLE NODE", text)
        self.assertIn("CONTROL / PERMISSION", text)
        self.assertIn("INTERFACE", text)
        self.assertIn("INCENTIVE", text)
        self.assertIn("ACCEPTANCE", text)

    def test_world_node_families_cover_collective_and_nonhuman_resources(self):
        text = NODES.read_text(encoding="utf-8")
        for term in [
            "GROUP / COMMUNITY",
            "ORGANIZATION / INSTITUTION",
            "PHYSICAL RESOURCE / ASSET",
            "CHANNEL / NETWORK",
            "SPACE / LOCATION",
            "EQUIPMENT / INFRASTRUCTURE",
            "INVENTORY / CAPACITY",
            "CAPITAL / BUDGET",
            "AUTHORITY / LICENSE / ACCESS RIGHT",
            "SOFTWARE / AI / API",
            "DEMAND STREAM / EVENT FLOW",
            "TRUST / REPUTATION / RELATIONSHIP",
        ]:
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
