import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROUTABLE_WORLD_NODES.md"


class RoutableWorldNodesTests(unittest.TestCase):
    def test_world_is_not_reduced_to_people(self):
        text = DOC.read_text(encoding="utf-8")
        for term in [
            "PERSON / INDIVIDUAL",
            "GROUP / COMMUNITY",
            "ORGANIZATION / INSTITUTION",
            "PHYSICAL RESOURCE / ASSET",
            "CHANNEL / NETWORK",
            "INFORMATION / DATA SOURCE",
            "EQUIPMENT / INFRASTRUCTURE",
            "CAPITAL / BUDGET",
            "SOFTWARE / AI / API",
        ]:
            self.assertIn(term, text)

    def test_existence_is_not_control(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("EXISTS\n!=\nOBSERVED\n!=\nACCESSIBLE\n!=\nOPTIONED\n!=\nCONTROLLED\n!=\nTRANSACTIONABLE", text)

    def test_collective_structure_is_first_class(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("GROUP VALUE != SUM(INDIVIDUAL VALUE)", text)
        self.assertIn("ORGANIZATION CAPABILITY != EMPLOYEE CAPABILITY", text)

    def test_non_human_sensors_are_allowed(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("EQUIPMENT TELEMETRY", text)
        self.assertIn("PROCUREMENT FEED", text)
        self.assertIn("SOFTWARE / AI AGENT", text)


if __name__ == "__main__":
    unittest.main()
