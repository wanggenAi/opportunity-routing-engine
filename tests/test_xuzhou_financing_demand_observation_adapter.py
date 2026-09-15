import unittest

from src.xuzhou_financing_demand_observation_adapter import (
    xuzhou_financing_demand_observations,
)


class XuzhouFinancingDemandObservationAdapterTests(unittest.TestCase):
    def _payload(self):
        digest = "a" * 64
        url = "https://www.jiangsu.gov.cn/art/2025/12/15/art_33718_11693505.html"
        return {
            "source_id": "XZ_GOV_FINANCE_DEMAND",
            "evidence_kind": "SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND",
            "data_available": True,
            "event_count": 1,
            "geography": "Xuzhou",
            "truth_boundaries": [
                "DIRECT_DEMAND_EVIDENCE_IS_NEED_ONLY",
                "SCOPED_PROGRAM_IS_NOT_CITYWIDE_TOTAL",
                "SME_IS_NOT_PRIVATE_ENTERPRISE",
                "MISSING_DEMAND_IS_NOT_ZERO",
                "NO_CROSS_PROGRAM_SUM",
                "NO_CROSS_PERIOD_SUM",
                "NO_SURPLUS_RESOURCE_INFERENCE",
                "NO_OPPORTUNITY_INFERENCE",
            ],
            "events": [
                {
                    "source_id": "XZ_GOV_FINANCE_DEMAND",
                    "signal_id": "XZ_ENTERPRISE_FINANCING_DEMAND_SCOPED",
                    "evidence_role": "DIRECT_SCOPED_ENTERPRISE_FINANCING_DEMAND",
                    "geography": "Xuzhou",
                    "coverage_scope": "SCOPED_PROGRAM_OR_REPORTED_BATCH",
                    "aggregation_allowed": False,
                    "source_authority": "徐州市政府办公室",
                    "source_url": url,
                    "provenance_sha256": digest,
                    "title": "徐州以产业集群培育赋能中小企业高质量发展",
                    "publication_date": "2025-12-15",
                    "program_name": "银企同心 产融共进",
                    "actor_scope": "SME_AND_MICRO",
                    "private_enterprise_scope_explicit": False,
                    "demand_amount_cny_100m": "13.6",
                    "granted_credit_amount_cny_100m": "12.59",
                    "beneficiary_enterprises": 118,
                    "matched_text": "累计摸排融资需求13.6亿元，已授信12.59亿元，惠及118家企业。",
                }
            ],
            "provenance": {
                "detail_pages": [
                    {
                        "source_id": "XZ_GOV_FINANCE_DEMAND",
                        "url": url,
                        "payload_sha256": digest,
                        "fetched_at_utc": "2026-09-14T13:00:55.435761+00:00",
                    }
                ]
            },
        }

    def test_explicit_demand_is_state_not_flow_or_paid_need(self):
        envelope = xuzhou_financing_demand_observations(self._payload())[0]
        self.assertEqual(envelope.source_id, "XZ_GOV_FINANCE_DEMAND")
        self.assertEqual(envelope.actor_ids, ())
        claims = {claim.concept: claim for claim in envelope.claims}
        demand = claims["XZ_SCOPED_DIRECT_ENTERPRISE_FINANCING_DEMAND"]
        self.assertEqual(demand.primitive, "STATE")
        self.assertEqual(demand.value["demand_amount_cny_100m"], "13.6")
        self.assertEqual(demand.value["actor_scope"], "SME_AND_MICRO")
        self.assertFalse(demand.value["private_enterprise_scope_explicit"])
        self.assertFalse(demand.value["aggregation_allowed"])
        self.assertNotIn("PAID_NEED", claims)
        self.assertNotIn("PAYER_CONFIRMED", claims)
        self.assertTrue(all(claim.epistemic_status == "OBSERVED" for claim in envelope.claims))

    def test_granted_credit_is_state_with_payment_not_established(self):
        envelope = xuzhou_financing_demand_observations(self._payload())[0]
        claims = {claim.concept: claim for claim in envelope.claims}
        credit = claims["XZ_SCOPED_GRANTED_CREDIT_AMOUNT"]
        self.assertEqual(credit.primitive, "STATE")
        self.assertEqual(credit.value["granted_credit_amount_cny_100m"], "12.59")
        self.assertEqual(credit.value["settlement_status"], "NOT_ESTABLISHED")
        beneficiaries = claims["XZ_SCOPED_BENEFICIARY_ENTERPRISE_COUNT"]
        self.assertEqual(beneficiaries.value["beneficiary_enterprises"], 118)

    def test_event_binds_exact_text_and_detail_page_hash(self):
        envelope = xuzhou_financing_demand_observations(self._payload())[0]
        self.assertEqual(len(envelope.evidence), 1)
        evidence = envelope.evidence[0]
        self.assertIn("融资需求13.6亿元", evidence.excerpt)
        self.assertEqual(evidence.content_hash, "a" * 64)
        self.assertEqual(envelope.raw_payload_hash, "a" * 64)
        self.assertEqual(envelope.published_at, "2025-12-15T00:00:00+08:00")

    def test_hash_mismatch_fails_closed(self):
        payload = self._payload()
        payload["events"][0]["provenance_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "diverges"):
            xuzhou_financing_demand_observations(payload)

    def test_cross_program_aggregation_is_rejected(self):
        payload = self._payload()
        payload["events"][0]["aggregation_allowed"] = True
        with self.assertRaisesRegex(ValueError, "prohibit aggregation"):
            xuzhou_financing_demand_observations(payload)

    def test_sme_scope_cannot_be_relabelled_private_enterprise(self):
        payload = self._payload()
        payload["events"][0]["private_enterprise_scope_explicit"] = True
        with self.assertRaisesRegex(ValueError, "relabeled private enterprise"):
            xuzhou_financing_demand_observations(payload)

    def test_missing_truth_boundary_fails_closed(self):
        payload = self._payload()
        payload["truth_boundaries"].remove("NO_OPPORTUNITY_INFERENCE")
        with self.assertRaisesRegex(ValueError, "truth boundaries missing"):
            xuzhou_financing_demand_observations(payload)


if __name__ == "__main__":
    unittest.main()
