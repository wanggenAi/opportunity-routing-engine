import tempfile
import unittest
from pathlib import Path

from src.live_observation_pipeline import summarize_live_store
from src.observation_store import SQLiteObservationStore


class LiveObservationSourceMonotonicityTests(unittest.TestCase):
    def test_live_summary_rejects_out_of_order_source_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "live.db") as store:
                with self.assertRaisesRegex(
                    ValueError,
                    "upstream run resolution regressed",
                ):
                    summarize_live_store(
                        store,
                        input_observation_count=1,
                        transition_counts={"OUT_OF_ORDER": 1},
                        upstream_manifest={"bootstrap": False},
                    )


if __name__ == "__main__":
    unittest.main()
