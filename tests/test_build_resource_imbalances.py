import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_resource_imbalances import build_snapshot


class ResourceImbalanceCliTests(unittest.TestCase):
    def _write_csv(self, directory, name, fieldnames, rows):
        path = Path(directory) / name
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return str(path)

    def test_empty_inputs_produce_empty_ledger(self):
        snapshot = build_snapshot(None, None, None)
        self.assertEqual(snapshot["record_count"], 0)
        self.assertEqual(snapshot["status_counts"], {})

    def test_csv_inputs_produce_route_testable_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            needs = self._write_csv(
                directory,
                "needs.csv",
                [
                    "signal_id",
                    "capability_key",
                    "geography",
                    "need_actor",
                    "payer",
                    "evidence_state",
                    "paid_event_count",
                    "total_observed_spend_rmb",
                    "observation_period",
                    "source_ids",
                    "notes",
                ],
                [
                    {
                        "signal_id": "need-1",
                        "capability_key": "cleaning",
                        "geography": "Xuzhou",
                        "need_actor": "buyer",
                        "payer": "buyer",
                        "evidence_state": "PAID",
                        "paid_event_count": "1",
                        "total_observed_spend_rmb": "1000",
                        "observation_period": "2026-09",
                        "source_ids": "need-source;need-url",
                        "notes": "",
                    }
                ],
            )
            resources = self._write_csv(
                directory,
                "resources.csv",
                [
                    "signal_id",
                    "capability_key",
                    "geography",
                    "provider_actor",
                    "resource_state",
                    "underuse_evidence_state",
                    "available_units",
                    "observation_period",
                    "source_ids",
                    "notes",
                ],
                [
                    {
                        "signal_id": "resource-1",
                        "capability_key": "cleaning",
                        "geography": "Xuzhou",
                        "provider_actor": "provider",
                        "resource_state": "DISCOVERED",
                        "underuse_evidence_state": "OBSERVED",
                        "available_units": "2 slots/day",
                        "observation_period": "2026-09",
                        "source_ids": "resource-source",
                        "notes": "",
                    }
                ],
            )
            blockers = self._write_csv(
                directory,
                "blockers.csv",
                [
                    "signal_id",
                    "capability_key",
                    "geography",
                    "blocker_type",
                    "evidence_state",
                    "description",
                    "source_ids",
                ],
                [
                    {
                        "signal_id": "blocker-1",
                        "capability_key": "cleaning",
                        "geography": "Xuzhou",
                        "blocker_type": "TRUST_GAP",
                        "evidence_state": "OBSERVED",
                        "description": "buyer requires a trusted acceptance route",
                        "source_ids": "blocker-source",
                    }
                ],
            )
            snapshot = build_snapshot(needs, resources, blockers)
            self.assertEqual(snapshot["record_count"], 1)
            self.assertEqual(snapshot["status_counts"], {"ROUTE_TESTABLE": 1})
            self.assertEqual(snapshot["records"][0]["payer"], "buyer")


if __name__ == "__main__":
    unittest.main()
