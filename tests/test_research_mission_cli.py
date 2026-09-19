import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ResearchMissionCLITests(unittest.TestCase):
    def test_builder_runs_as_direct_script_and_stays_calibration_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            plan = tmp_path / "plan.json"
            coverage = tmp_path / "coverage.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_research_mission.py",
                    "--mission",
                    "data/research_missions/attraction_field_broad_reality.json",
                    "--as-of-date",
                    "2026-09-19",
                    "--plan-output",
                    str(plan),
                    "--coverage-output",
                    str(coverage),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(completed.stdout.strip())
            self.assertEqual(summary["query_count"], 60)
            self.assertEqual(summary["coverage_state"], "CALIBRATION_ONLY")
            self.assertFalse(summary["broad_discovery_use_authorized"])
            self.assertTrue(plan.exists())
            self.assertTrue(coverage.exists())

            subprocess.run(
                [
                    sys.executable,
                    "scripts/validate_research_mission.py",
                    "--plan",
                    str(plan),
                    "--coverage",
                    str(coverage),
                ],
                check=True,
                capture_output=True,
                text=True,
            )


if __name__ == "__main__":
    unittest.main()
