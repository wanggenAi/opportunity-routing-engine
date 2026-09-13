import json
import tempfile
import unittest
from pathlib import Path

from src.composition_outcome_intake import (
    outcome_event_from_record,
    outcome_events_from_path,
)
from src.composition_outcome_store import OutcomeEventType


class CompositionOutcomeIntakeTests(unittest.TestCase):
    def _record(self):
        return {
            "outcome_id": "outcome-1",
            "composition_run_id": 4,
            "hypothesis_index": 0,
            "transaction_ref": "tx-1",
            "event_type": "DELIVERY_ACCEPTED",
            "observed_at": "2026-09-13T21:00:00+08:00",
            "validation_as_of": "2026-09-13T20:00:00+08:00",
            "validation_snapshot_fingerprint": "abc123",
            "evidence_ref": "field:acceptance",
            "evidence_note": "counterparty accepted bounded output",
            "subject_ref": "counterparty-a",
            "details": {"acceptance_scope": "bounded test output"},
        }

    def test_atomic_outcome_record_parses(self):
        event = outcome_event_from_record(self._record())
        self.assertEqual(event.event_type, OutcomeEventType.DELIVERY_ACCEPTED)
        self.assertEqual(event.transaction_ref, "tx-1")

    def test_derived_maturity_and_gate_fields_are_rejected(self):
        for key in ("evidence_maturity", "repeatable", "G6", "L7"):
            record = self._record()
            record[key] = "PASS"
            with self.assertRaisesRegex(ValueError, "derived outcome fields are not accepted"):
                outcome_event_from_record(record)

    def test_unknown_fields_are_rejected(self):
        record = self._record()
        record["magic_success"] = True
        with self.assertRaisesRegex(ValueError, "unknown outcome fields"):
            outcome_event_from_record(record)

    def test_settlement_requires_amount_and_currency(self):
        record = self._record()
        record["event_type"] = "SETTLEMENT_OBSERVED"
        with self.assertRaisesRegex(ValueError, "settlement_requires_amount"):
            outcome_event_from_record(record)
        record["amount"] = "1200"
        with self.assertRaisesRegex(ValueError, "settlement_requires_currency"):
            outcome_event_from_record(record)
        record["currency"] = "cny"
        event = outcome_event_from_record(record)
        self.assertEqual(event.amount, "1200")
        self.assertEqual(event.currency, "cny")

    def test_non_settlement_cannot_smuggle_amount(self):
        record = self._record()
        record["amount"] = "100"
        record["currency"] = "CNY"
        with self.assertRaisesRegex(ValueError, "amount_currency_only_allowed_for_settlement"):
            outcome_event_from_record(record)

    def test_outcome_cannot_precede_validation_snapshot(self):
        record = self._record()
        record["observed_at"] = "2026-09-13T19:00:00+08:00"
        with self.assertRaisesRegex(ValueError, "outcome_cannot_precede_validation_snapshot"):
            outcome_event_from_record(record)

    def test_json_and_jsonl_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._record()
            second = self._record()
            second["outcome_id"] = "outcome-2"
            second["event_type"] = "ROUTE_FAILED"

            json_path = root / "outcomes.json"
            json_path.write_text(json.dumps([first, second]), encoding="utf-8")
            self.assertEqual(
                [event.outcome_id for event in outcome_events_from_path(json_path)],
                ["outcome-1", "outcome-2"],
            )

            jsonl_path = root / "outcomes.jsonl"
            jsonl_path.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [event.outcome_id for event in outcome_events_from_path(jsonl_path)],
                ["outcome-1", "outcome-2"],
            )


if __name__ == "__main__":
    unittest.main()
