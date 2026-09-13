import tempfile
import unittest
from pathlib import Path

from src.live_resource_signals import AvailabilityState, PermissionState
from src.live_signal_ledger import TransitionKind
from src.live_signal_store import SQLiteSignalLedgerStore
from src.resource_underuse_adapters import PublicAssetListing
from src.xuzhou_public_asset_live_sensor import signal_from_public_asset


class XuzhouPublicAssetLiveSensorTests(unittest.TestCase):
    def _listing(self, **overrides):
        payload = dict(
            source_id="XZ_GGZY",
            title="某处房屋公开招租",
            url="https://ggzy.zwb.xz.gov.cn/jyxx/003005/003005003/20260913/example.html",
            publication_date="2026-09-13",
            project_id="XZ-ASSET-001",
            listing_mode="LEASE",
            listing_round=1,
            relisting_observed=False,
            listing_start="2026-09-13",
            listing_end="2026-09-20",
            resource_state="DISCOVERED",
            underuse_evidence_state="UNKNOWN",
            underuse_excerpt=None,
            asking_price_rmb="120000.00",
            asking_price_raw="年租金底价 12 万元",
            location="徐州市",
            owner_actor="某国有单位",
            provenance={"fetched_at_utc": "2026-09-13T08:00:00+00:00"},
        )
        payload.update(overrides)
        return PublicAssetListing(**payload)

    def test_listing_becomes_advertised_signal_without_operator_permission(self):
        signal = signal_from_public_asset(self._listing())
        self.assertEqual(signal.source_id, "XZ_GGZY_PUBLIC_ASSET")
        self.assertEqual(signal.signal_id, "XZ-ASSET-001")
        self.assertEqual(signal.actor_ref, "某国有单位")
        self.assertEqual(signal.availability, AvailabilityState.ADVERTISED)
        self.assertEqual(signal.permission, PermissionState.UNKNOWN)
        self.assertEqual(signal.explicit_capabilities, ())

    def test_explicit_underuse_is_preserved_only_when_source_observed_it(self):
        observed = signal_from_public_asset(
            self._listing(
                underuse_evidence_state="OBSERVED",
                underuse_excerpt="标的状态：空置",
            )
        )
        unknown = signal_from_public_asset(self._listing())
        observed_keys = {fact.key for fact in observed.facts}
        unknown_keys = {fact.key for fact in unknown.facts}
        self.assertIn("resource.explicit_underuse_observed", observed_keys)
        self.assertNotIn("resource.explicit_underuse_observed", unknown_keys)

    def test_relisting_does_not_manufacture_underuse(self):
        signal = signal_from_public_asset(
            self._listing(listing_round=2, relisting_observed=True)
        )
        facts = {fact.key: fact.value for fact in signal.facts}
        self.assertTrue(facts["resource.relisting_observed"])
        self.assertEqual(facts["resource.underuse_evidence_state"], "UNKNOWN")
        self.assertNotIn("resource.explicit_underuse_observed", facts)

    def test_missing_owner_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "owner_actor"):
            signal_from_public_asset(self._listing(owner_actor=None))

    def test_real_sensor_signal_enters_durable_ledger_and_price_change_is_detected(self):
        first = signal_from_public_asset(self._listing())
        second = signal_from_public_asset(
            self._listing(
                asking_price_rmb="100000.00",
                asking_price_raw="年租金底价 10 万元",
                provenance={"fetched_at_utc": "2026-09-14T08:00:00+00:00"},
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as store:
                self.assertEqual(store.ingest(first).kind, TransitionKind.FIRST_SEEN)
                transition = store.ingest(second)
                self.assertEqual(transition.kind, TransitionKind.CHANGED)
                self.assertIn("facts", transition.changed_dimensions)
                current = store.get("XZ_GGZY_PUBLIC_ASSET", "XZ-ASSET-001")
                self.assertEqual(current.revision_count, 1)


if __name__ == "__main__":
    unittest.main()
