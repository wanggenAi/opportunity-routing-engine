import unittest

from src.resource_imbalance import (
    BlockerSignal,
    NeedSignal,
    ResourceSignal,
    evaluate_pair,
    procurement_event_to_need,
    scan_imbalances,
)


class ResourceImbalanceTests(unittest.TestCase):
    def _paid_need(self, signal_id="need-1"):
        return NeedSignal(
            signal_id=signal_id,
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            need_actor="industrial buyer",
            payer="industrial buyer",
            evidence_state="PAID",
            paid_event_count=1,
            total_observed_spend_rmb="200000",
            source_ids=("source-need",),
        )

    def _observed_resource(self, signal_id="resource-1", state="DISCOVERED"):
        return ResourceSignal(
            signal_id=signal_id,
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            provider_actor="maintenance team",
            resource_state=state,
            underuse_evidence_state="OBSERVED",
            source_ids=("source-resource",),
        )

    def _observed_blocker(self):
        return BlockerSignal(
            signal_id="blocker-1",
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            blocker_type="INFORMATION_GAP",
            evidence_state="OBSERVED",
            description="buyers and spare-capacity providers do not share a trusted route",
            source_ids=("source-blocker",),
        )

    def test_need_without_resource_stays_need_only(self):
        records = scan_imbalances([self._paid_need()], [], [])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].status, "NEED_ONLY")
        self.assertIsNone(records[0].resource_signal_id)

    def test_resource_without_need_stays_resource_only(self):
        records = scan_imbalances([], [self._observed_resource()], [])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].status, "RESOURCE_ONLY")
        self.assertIsNone(records[0].need_signal_id)

    def test_pair_without_observed_blocker_is_only_hypothesis(self):
        result = evaluate_pair(self._paid_need(), self._observed_resource())
        self.assertEqual(result.status, "PAIR_HYPOTHESIS")
        self.assertIn("transaction blocker is not identified", result.reasons)

    def test_claimed_underuse_cannot_become_route_testable(self):
        resource = ResourceSignal(
            signal_id="resource-claimed",
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            provider_actor="maintenance team",
            resource_state="DISCOVERED",
            underuse_evidence_state="CLAIMED",
            source_ids=("source-resource",),
        )
        result = evaluate_pair(self._paid_need(), resource, self._observed_blocker())
        self.assertEqual(result.status, "PAIR_HYPOTHESIS")
        self.assertIn("resource underuse is not observed", result.reasons)

    def test_observed_need_without_payment_cannot_become_route_testable(self):
        need = NeedSignal(
            signal_id="need-observed",
            capability_key="equipment_maintenance",
            geography="Xuzhou",
            need_actor="industrial buyer",
            payer=None,
            evidence_state="OBSERVED",
            source_ids=("source-need",),
        )
        result = evaluate_pair(need, self._observed_resource(), self._observed_blocker())
        self.assertEqual(result.status, "PAIR_HYPOTHESIS")
        self.assertIn("need side lacks direct paid evidence", result.reasons)
        self.assertIn("payer is not identified", result.reasons)

    def test_paid_need_plus_observed_underuse_and_blocker_is_route_testable(self):
        result = evaluate_pair(
            self._paid_need(), self._observed_resource(), self._observed_blocker()
        )
        self.assertEqual(result.status, "ROUTE_TESTABLE")
        self.assertEqual(result.blocker_type, "INFORMATION_GAP")

    def test_discovered_is_enough_for_bounded_route_test_not_transaction_claim(self):
        result = evaluate_pair(
            self._paid_need(),
            self._observed_resource(state="DISCOVERED"),
            self._observed_blocker(),
        )
        self.assertEqual(result.status, "ROUTE_TESTABLE")
        self.assertEqual(result.resource_state, "DISCOVERED")
        self.assertNotEqual(result.resource_state, "OPTIONED")

    def test_exact_capability_and_geography_match_is_required(self):
        resource = ResourceSignal(
            signal_id="resource-other",
            capability_key="equipment_maintenance",
            geography="Jiangsu",
            provider_actor="maintenance team",
            resource_state="DISCOVERED",
            underuse_evidence_state="OBSERVED",
            source_ids=("source-resource",),
        )
        with self.assertRaisesRegex(ValueError, "must match exactly"):
            evaluate_pair(self._paid_need(), resource)

    def test_scan_pairs_matching_signals_and_keeps_unmatched_resource(self):
        extra = ResourceSignal(
            signal_id="resource-data",
            capability_key="data_cleaning",
            geography="Xuzhou",
            provider_actor="graduate team",
            resource_state="DISCOVERED",
            underuse_evidence_state="OBSERVED",
            source_ids=("source-data",),
        )
        records = scan_imbalances(
            [self._paid_need()],
            [self._observed_resource(), extra],
            [self._observed_blocker()],
        )
        statuses = {record.record_id: record.status for record in records}
        self.assertEqual(statuses["PAIR::need-1::resource-1"], "ROUTE_TESTABLE")
        self.assertEqual(statuses["RESOURCE::resource-data"], "RESOURCE_ONLY")

    def test_pair_limit_never_turns_matching_resource_into_resource_only(self):
        resource_1 = self._observed_resource("resource-1")
        resource_2 = self._observed_resource("resource-2")
        records = scan_imbalances(
            [self._paid_need()],
            [resource_1, resource_2],
            [self._observed_blocker()],
            max_pairs_per_need=1,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].record_id, "PAIR::need-1::resource-1")
        self.assertFalse(
            any(record.record_id == "RESOURCE::resource-2" for record in records)
        )

    def test_paid_state_requires_real_payer_and_event_count(self):
        bad = NeedSignal(
            signal_id="bad",
            capability_key="maintenance",
            geography="Xuzhou",
            need_actor="buyer",
            payer=None,
            evidence_state="PAID",
            paid_event_count=0,
            source_ids=("source",),
        )
        with self.assertRaises(ValueError):
            scan_imbalances([bad], [], [])

    def test_procurement_normalization_creates_only_need_side_evidence(self):
        event = {
            "source_id": "XZ_GGZY",
            "url": "https://example.invalid/procurement/1",
            "budget_rmb": "350000.00",
            "publication_date": "2026-09-11",
        }
        need = procurement_event_to_need(
            event,
            signal_id="xz-proc-1",
            capability_key="facility_operations",
            need_actor="public institution",
            payer="public institution",
        )
        self.assertEqual(need.evidence_state, "PAID")
        self.assertEqual(need.total_observed_spend_rmb, "350000.00")
        records = scan_imbalances([need], [], [])
        self.assertEqual(records[0].status, "NEED_ONLY")


if __name__ == "__main__":
    unittest.main()
