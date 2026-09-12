import unittest

from scripts.build_live_resource_imbalance import _blocker_from_mapping
from src.procurement_lifecycle import _blocker_from_dict
from src.resource_imbalance import (
    BlockerSignal,
    NeedSignal,
    ResourceSignal,
    evaluate_pair,
    scan_imbalances,
)


class BlockerNeedScopeTests(unittest.TestCase):
    def _need(self, signal_id: str) -> NeedSignal:
        return NeedSignal(
            signal_id=signal_id,
            capability_key="shared_capability",
            geography="Xuzhou",
            need_actor="buyer",
            payer="payer",
            evidence_state="PAID",
            paid_event_count=1,
            source_ids=("need-source",),
        )

    def _resource(self) -> ResourceSignal:
        return ResourceSignal(
            signal_id="resource-1",
            capability_key="shared_capability",
            geography="Xuzhou",
            provider_actor="provider",
            resource_state="DISCOVERED",
            underuse_evidence_state="OBSERVED",
            source_ids=("resource-source",),
        )

    def _scoped_blocker(self, need_signal_id: str) -> BlockerSignal:
        return BlockerSignal(
            signal_id=f"blocker::{need_signal_id}",
            capability_key="shared_capability",
            geography="Xuzhou",
            blocker_type="CAPABILITY_GAP",
            evidence_state="OBSERVED",
            description="exact transaction qualification constraint",
            source_ids=("blocker-source",),
            need_signal_id=need_signal_id,
        )

    def test_scoped_blocker_cannot_cross_between_same_capability_needs(self):
        need_a = self._need("need-a")
        need_b = self._need("need-b")
        records = scan_imbalances(
            [need_a, need_b],
            [self._resource()],
            [self._scoped_blocker("need-a")],
        )
        by_need = {record.need_signal_id: record for record in records}
        self.assertEqual(by_need["need-a"].status, "ROUTE_TESTABLE")
        self.assertEqual(by_need["need-a"].blocker_signal_id, "blocker::need-a")
        self.assertEqual(by_need["need-b"].status, "PAIR_HYPOTHESIS")
        self.assertIsNone(by_need["need-b"].blocker_signal_id)
        self.assertIn("transaction blocker is not identified", by_need["need-b"].reasons)

    def test_evaluate_pair_rejects_wrong_scoped_blocker(self):
        with self.assertRaisesRegex(ValueError, "exact need signal"):
            evaluate_pair(
                self._need("need-b"),
                self._resource(),
                self._scoped_blocker("need-a"),
            )

    def test_unscoped_market_blocker_remains_capability_wide(self):
        blocker = BlockerSignal(
            signal_id="market-blocker",
            capability_key="shared_capability",
            geography="Xuzhou",
            blocker_type="INFORMATION_GAP",
            evidence_state="OBSERVED",
            description="market-wide route information gap",
            source_ids=("market-source",),
        )
        records = scan_imbalances(
            [self._need("need-a"), self._need("need-b")],
            [self._resource()],
            [blocker],
        )
        self.assertTrue(all(record.status == "ROUTE_TESTABLE" for record in records))
        self.assertTrue(all(record.blocker_signal_id == "market-blocker" for record in records))

    def test_exact_scoped_blocker_wins_over_equal_rank_unscoped_blocker(self):
        unscoped = BlockerSignal(
            signal_id="market-blocker",
            capability_key="shared_capability",
            geography="Xuzhou",
            blocker_type="INFORMATION_GAP",
            evidence_state="OBSERVED",
            description="market-wide route information gap",
            source_ids=("market-source",),
        )
        record = scan_imbalances(
            [self._need("need-a")],
            [self._resource()],
            [unscoped, self._scoped_blocker("need-a")],
        )[0]
        self.assertEqual(record.blocker_signal_id, "blocker::need-a")

    def test_json_loader_preserves_need_scope(self):
        blocker = _blocker_from_mapping(
            {
                "signal_id": "blocker-a",
                "capability_key": "shared_capability",
                "geography": "Xuzhou",
                "blocker_type": "CAPABILITY_GAP",
                "evidence_state": "OBSERVED",
                "description": "constraint",
                "source_ids": ["source"],
                "need_signal_id": "need-a",
            }
        )
        self.assertEqual(blocker.need_signal_id, "need-a")

    def test_lifecycle_reconstruction_preserves_need_scope(self):
        blocker = _blocker_from_dict(
            {
                "signal_id": "blocker-a",
                "capability_key": "shared_capability",
                "geography": "Xuzhou",
                "blocker_type": "CAPABILITY_GAP",
                "evidence_state": "OBSERVED",
                "description": "constraint",
                "source_ids": ["source"],
                "need_signal_id": "need-a",
            }
        )
        self.assertEqual(blocker.need_signal_id, "need-a")


if __name__ == "__main__":
    unittest.main()
