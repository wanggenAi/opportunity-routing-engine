import unittest

from src.provider_capacity_evidence import apply_provider_capacity_evidence_to_ledger
from src.resource_imbalance import BlockerSignal, NeedSignal, ResourceSignal, scan_imbalances


class ProviderCapacityEvidenceTests(unittest.TestCase):
    def _ledger(self):
        need = NeedSignal(
            signal_id="need-1",
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            need_actor="buyer",
            payer="buyer",
            evidence_state="PAID",
            paid_event_count=1,
            source_ids=("need-source",),
        )
        resource = ResourceSignal(
            signal_id="resource-1",
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            provider_actor="provider-a",
            resource_state="DISCOVERED",
            underuse_evidence_state="UNKNOWN",
            source_ids=("award-source",),
        )
        blocker = BlockerSignal(
            signal_id="blocker-1",
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            blocker_type="INFORMATION_GAP",
            evidence_state="OBSERVED",
            description="route friction",
            source_ids=("blocker-source",),
            need_signal_id="need-1",
        )
        records = scan_imbalances([need], [resource], [blocker])
        return {
            "geography": "Xuzhou",
            "signals": {
                "needs": [need.__dict__],
                "resources": [resource.__dict__],
                "blockers": [blocker.__dict__],
            },
            "records": [record.as_dict() for record in records],
            "status_counts": {"PAIR_HYPOTHESIS": 1},
            "blocking_reason_counts": {"resource underuse is not observed": 1},
            "route_testable_count": 0,
            "route_testable_records": [],
        }

    def test_provider_statement_stays_claimed_and_below_route_gate(self):
        evidence = {
            "evidence": [
                {
                    "evidence_id": "cap-1",
                    "resource_signal_id": "resource-1",
                    "provider_actor": "provider-a",
                    "capability_key": "equipment_maintenance",
                    "geography": "Xuzhou",
                    "underuse_evidence_state": "CLAIMED",
                    "evidence_basis": "PROVIDER_STATED_SPARE_CAPACITY",
                    "observation_period": "2026-09-12",
                    "source_refs": ["direct-call-note-sha256:abc"],
                }
            ]
        }
        result = apply_provider_capacity_evidence_to_ledger(self._ledger(), [evidence])
        resource = result["signals"]["resources"][0]
        self.assertEqual(resource["underuse_evidence_state"], "CLAIMED")
        self.assertEqual(result["route_testable_count"], 0)
        self.assertEqual(result["status_counts"], {"PAIR_HYPOTHESIS": 1})

    def test_authorized_schedule_can_promote_exact_resource_to_observed(self):
        evidence = {
            "evidence": [
                {
                    "evidence_id": "cap-2",
                    "resource_signal_id": "resource-1",
                    "provider_actor": "provider-a",
                    "capability_key": "equipment_maintenance",
                    "geography": "Xuzhou",
                    "underuse_evidence_state": "OBSERVED",
                    "evidence_basis": "AUTHORIZED_CAPACITY_SCHEDULE",
                    "available_units": "2 crews available 2026-09-20 to 2026-09-24",
                    "observation_period": "2026-09-12",
                    "source_refs": ["schedule-sha256:def"],
                }
            ]
        }
        result = apply_provider_capacity_evidence_to_ledger(self._ledger(), [evidence])
        resource = result["signals"]["resources"][0]
        self.assertEqual(resource["underuse_evidence_state"], "OBSERVED")
        self.assertEqual(resource["available_units"], "2 crews available 2026-09-20 to 2026-09-24")
        self.assertEqual(result["route_testable_count"], 1)
        self.assertEqual(result["status_counts"], {"ROUTE_TESTABLE": 1})

    def test_identity_mismatch_never_promotes_resource(self):
        evidence = {
            "evidence": [
                {
                    "evidence_id": "cap-3",
                    "resource_signal_id": "resource-1",
                    "provider_actor": "provider-b",
                    "capability_key": "equipment_maintenance",
                    "geography": "Xuzhou",
                    "underuse_evidence_state": "OBSERVED",
                    "evidence_basis": "VERIFIED_UNUSED_CAPACITY_RECORD",
                    "available_units": "1 unused maintenance slot",
                    "observation_period": "2026-09-12",
                    "source_refs": ["capacity-record-sha256:ghi"],
                }
            ]
        }
        result = apply_provider_capacity_evidence_to_ledger(self._ledger(), [evidence])
        self.assertEqual(result["signals"]["resources"][0]["underuse_evidence_state"], "UNKNOWN")
        self.assertEqual(result["provider_capacity_evidence"]["applied_count"], 0)
        self.assertEqual(
            result["provider_capacity_evidence"]["rejected"][0]["reason"],
            "RESOURCE_IDENTITY_MISMATCH",
        )

    def test_observed_basis_requires_available_units(self):
        evidence = {
            "evidence": [
                {
                    "evidence_id": "cap-4",
                    "resource_signal_id": "resource-1",
                    "provider_actor": "provider-a",
                    "capability_key": "equipment_maintenance",
                    "geography": "Xuzhou",
                    "underuse_evidence_state": "OBSERVED",
                    "evidence_basis": "AUTHORIZED_CAPACITY_SCHEDULE",
                    "observation_period": "2026-09-12",
                    "source_refs": ["schedule-sha256:jkl"],
                }
            ]
        }
        result = apply_provider_capacity_evidence_to_ledger(self._ledger(), [evidence])
        self.assertEqual(result["signals"]["resources"][0]["underuse_evidence_state"], "UNKNOWN")
        self.assertEqual(
            result["provider_capacity_evidence"]["rejected"][0]["reason"],
            "OBSERVED_UNDERUSE_REQUIRES_AVAILABLE_UNITS",
        )

    def test_basis_state_mismatch_is_rejected(self):
        evidence = {
            "evidence": [
                {
                    "evidence_id": "cap-5",
                    "resource_signal_id": "resource-1",
                    "provider_actor": "provider-a",
                    "capability_key": "equipment_maintenance",
                    "geography": "Xuzhou",
                    "underuse_evidence_state": "OBSERVED",
                    "evidence_basis": "PROVIDER_STATED_SPARE_CAPACITY",
                    "available_units": "2 crews",
                    "observation_period": "2026-09-12",
                    "source_refs": ["call-note-sha256:mno"],
                }
            ]
        }
        result = apply_provider_capacity_evidence_to_ledger(self._ledger(), [evidence])
        self.assertEqual(result["signals"]["resources"][0]["underuse_evidence_state"], "UNKNOWN")
        self.assertEqual(
            result["provider_capacity_evidence"]["rejected"][0]["reason"],
            "EVIDENCE_BASIS_STATE_MISMATCH",
        )


if __name__ == "__main__":
    unittest.main()
