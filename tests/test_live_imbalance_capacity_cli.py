import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LiveImbalanceCapacityCliTests(unittest.TestCase):
    def _write_json(self, directory: str, name: str, payload: dict) -> str:
        path = Path(directory) / name
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return str(path)

    def test_provider_capacity_json_updates_exact_live_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            procurement = self._write_json(
                directory,
                "procurement.json",
                {
                    "events": [
                        {
                            "source_id": "XZ_GGZY",
                            "project_id": "CURRENT-1",
                            "project_name": "泵站设施维修养护项目",
                            "title": "泵站设施维修养护采购公告",
                            "url": "https://example.test/tender/current-1",
                            "publication_date": "2026-09-12",
                            "budget_rmb": "1000000.00",
                        }
                    ]
                },
            )
            providers = self._write_json(
                directory,
                "providers.json",
                {
                    "awards": [
                        {
                            "source_id": "XZ_GGZY_PROCUREMENT_RESULT",
                            "project_id": "HIST-1",
                            "project_name": "泵站设施维修养护项目",
                            "title": "泵站设施维修养护中标结果公告",
                            "url": "https://example.test/result/hist-1",
                            "publication_date": "2026-06-01",
                            "supplier_name": "江苏某建设有限公司",
                            "supplier_credit_code": "913200000000000001",
                            "award_amount_rmb": "900000.00",
                        }
                    ]
                },
            )
            resource_signal_id = (
                "LIVE_PROVIDER::XZ_GGZY_PROCUREMENT_RESULT::HIST-1::"
                "913200000000000001::1"
            )
            capacity = self._write_json(
                directory,
                "capacity.json",
                {
                    "evidence": [
                        {
                            "evidence_id": "capacity-1",
                            "resource_signal_id": resource_signal_id,
                            "provider_actor": "江苏某建设有限公司",
                            "capability_key": "WATER_PUMP_STATION_MAINTENANCE",
                            "geography": "Xuzhou",
                            "underuse_evidence_state": "OBSERVED",
                            "evidence_basis": "AUTHORIZED_CAPACITY_SCHEDULE",
                            "available_units": "2 crews available next week",
                            "observation_period": "2026-09-12",
                            "source_refs": ["schedule-sha256:abc123"],
                        }
                    ]
                },
            )
            output = str(Path(directory) / "ledger.json")

            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_live_resource_imbalance.py",
                    "--procurement-json",
                    procurement,
                    "--provider-json",
                    providers,
                    "--provider-capacity-json",
                    capacity,
                    "--output",
                    output,
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
            ledger = json.loads(Path(output).read_text(encoding="utf-8"))
            resource = next(
                item
                for item in ledger["signals"]["resources"]
                if item["signal_id"] == resource_signal_id
            )
            self.assertEqual(resource["underuse_evidence_state"], "OBSERVED")
            self.assertEqual(resource["available_units"], "2 crews available next week")
            self.assertIn("schedule-sha256:abc123", resource["source_ids"])
            self.assertEqual(ledger["provider_capacity_evidence"]["applied_count"], 1)
            self.assertEqual(ledger["provider_capacity_evidence"]["rejected_count"], 0)
            self.assertEqual(ledger["records"][0]["status"], "PAIR_HYPOTHESIS")
            self.assertIn("need side lacks direct paid evidence", ledger["records"][0]["reasons"])
            self.assertIn("payer is not identified", ledger["records"][0]["reasons"])
            self.assertNotIn("resource underuse is not observed", ledger["records"][0]["reasons"])


if __name__ == "__main__":
    unittest.main()
