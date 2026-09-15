import subprocess
import sys
import unittest
from pathlib import Path


class LiveObservationCliTests(unittest.TestCase):
    def test_builder_help_runs_from_repository_root(self):
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, "scripts/build_live_observation_fabric.py", "--help"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--jiangsu-money-flow", completed.stdout)
        self.assertIn("--xuzhou-procurement", completed.stdout)
        self.assertIn("--resource-underuse", completed.stdout)
        self.assertIn("--nbs-macro-watchlist", completed.stdout)
        self.assertIn("--pbc-jiangsu-credit", completed.stdout)
        self.assertIn("--pbc-money-flow", completed.stdout)


if __name__ == "__main__":
    unittest.main()
