import unittest

from src.resource_signal_adapters import public_asset_listing_to_resource


class PublicAssetResourceSignalTests(unittest.TestCase):
    def test_explicit_idle_listing_becomes_observed_resource_signal(self):
        listing = {
            "source_id": "XZ_GGZY",
            "url": "https://ggzy.zwb.xz.gov.cn/example",
            "publication_date": "2026-08-20",
            "owner_actor": "江苏宁通投资发展集团有限公司",
            "resource_state": "DISCOVERED",
            "underuse_evidence_state": "OBSERVED",
            "underuse_excerpt": "房屋现状 标的状态 空置",
            "listing_mode": "LEASE",
            "listing_round": 1,
            "relisting_observed": False,
            "asking_price_rmb": "893792.00",
        }
        signal = public_asset_listing_to_resource(
            listing,
            signal_id="resource-1",
            capability_key="industrial_space",
        )
        self.assertEqual(signal.resource_state, "DISCOVERED")
        self.assertEqual(signal.underuse_evidence_state, "OBSERVED")
        self.assertEqual(signal.provider_actor, "江苏宁通投资发展集团有限公司")
        self.assertIn("underuse_excerpt=", signal.notes)

    def test_relisting_without_idle_language_stays_unknown_underuse(self):
        listing = {
            "source_id": "XZ_GGZY",
            "url": "https://ggzy.zwb.xz.gov.cn/example2",
            "publication_date": "2026-08-28",
            "owner_actor": "resource owner",
            "resource_state": "DISCOVERED",
            "underuse_evidence_state": "UNKNOWN",
            "underuse_excerpt": None,
            "listing_mode": "LEASE",
            "listing_round": 3,
            "relisting_observed": True,
            "asking_price_rmb": "10000.00",
        }
        signal = public_asset_listing_to_resource(
            listing,
            signal_id="resource-2",
            capability_key="commercial_space",
        )
        self.assertEqual(signal.underuse_evidence_state, "UNKNOWN")
        self.assertIn("relisting_observed=true", signal.notes)

    def test_transformer_refuses_source_promotion_beyond_discovered(self):
        listing = {
            "source_id": "XZ_GGZY",
            "url": "https://ggzy.zwb.xz.gov.cn/example3",
            "owner_actor": "resource owner",
            "resource_state": "OPTIONED",
            "underuse_evidence_state": "OBSERVED",
        }
        with self.assertRaisesRegex(ValueError, "only accepts resource_state=DISCOVERED"):
            public_asset_listing_to_resource(
                listing,
                signal_id="resource-3",
                capability_key="asset",
            )

    def test_capability_identity_remains_caller_supplied(self):
        listing = {
            "source_id": "XZ_GGZY",
            "url": "https://ggzy.zwb.xz.gov.cn/example4",
            "owner_actor": "resource owner",
            "resource_state": "DISCOVERED",
            "underuse_evidence_state": "UNKNOWN",
        }
        signal = public_asset_listing_to_resource(
            listing,
            signal_id="resource-4",
            capability_key="caller_defined_capability",
        )
        self.assertEqual(signal.capability_key, "caller_defined_capability")


if __name__ == "__main__":
    unittest.main()
