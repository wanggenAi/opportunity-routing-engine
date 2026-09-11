import subprocess
import sys
import unittest
from pathlib import Path


class ResourceUnderuseCliTests(unittest.TestCase):
    def test_script_help_runs_from_repository_root(self):
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, "scripts/collect_resource_underuse.py", "--help"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("xuzhou-public-assets", completed.stdout)


if __name__ == "__main__":
    unittest.main()
