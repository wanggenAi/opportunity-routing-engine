import hashlib
import unittest

from src.questmobile_research_observation_adapter import (
    questmobile_public_research_observations,
)


def payload():
    excerpt = "QuestMobile数据显示，示例全国样本行为发生变化。"
    excerpt_hash = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
    page_hash = "a" * 64
    return {
        "schema_version": "questmobile-public-research.v1",
        "source_id": "QM",
        "data_available": True,
        "collection_scope": "LATEST_PUBLIC_RESEARCH_REPORTS_ONLY",
        "report_limit": 5,
        "report_count": 2,
        "text_finding_count": 1,
        "reports": [
            {
                "source_id": "QM",
                "report_id": "2099761859812982785",
                "title": "QuestMobile 示例公开研究报告",
                "publication_date": "2026-09-15",
                "source_authority": "QuestMobile研究院",
                "category_text": "旅游服务",
                "finding_evidence_state": "TEXT_FINDINGS_OBSERVED",
                "finding_count": 1,
                "findings": [
                    {
                        "finding_id": "2099761859812982785:1",
                        "attribution": "QuestMobile",
                        "excerpt": excerpt,
                        "excerpt_sha256": excerpt_hash,
                    }
                ],
                "source_url": "https://www.questmobile.com.cn/research/report/2099761859812982785/",
                "provenance_sha256": page_hash,
                "provenance": {
                    "source_id": "QM",
                    "url": "https://www.questmobile.com.cn/research/report/2099761859812982785/",
                    "payload_sha256": page_hash,
                    "fetched_at_utc": "2026-09-15T12:03:00+00:00",
                },
            },
            {
                "source_id": "QM",
                "report_id": "2090000000000000000",
                "title": "QuestMobile 图片型公开研究报告",
                "publication_date": "2026-09-01",
                "source_authority": "QuestMobile研究院",
                "category_text": None,
                "finding_evidence_state": "NO_TEXT_FINDING",
                "finding_count": 0,
                "findings": [],
                "source_url": "https://www.questmobile.com.cn/research/report/2090000000000000000/",
                "provenance_sha256": "b" * 64,
                "provenance": {
                    "source_id": "QM",
                    "url": "https://www.questmobile.com.cn/research/report/2090000000000000000/",
                    "payload_sha256": "b" * 64,
                    "fetched_at_utc": "2026-09-15T12:03:00+00:00",
                },
            },
        ],
        "truth_boundaries": [
            "PUBLIC_REPORT_PAGE_ONLY",
            "NO_LOGIN_OR_PAID_DATABASE",
            "NO_OCR_OR_IMAGE_METRIC_EXTRACTION",
            "NO_TEXT_FINDING_NE_ZERO",
            "RESEARCH_REPORT_NE_CURRENT_LOCAL_REALITY",
            "REPORTED_SAMPLE_OR_PANEL_NE_CENSUS",
            "RESEARCH_FINDING_NE_PAID_DEMAND",
            "RESEARCH_FINDING_NE_PAYER",
            "RESEARCH_FINDING_NE_PAYMENT",
            "RESEARCH_FINDING_NE_OPPORTUNITY",
            "EXACT_EXCERPT_REQUIRED",
            "UNKNOWN_NE_PASS",
        ],
    }


class QuestMobileResearchObservationAdapterTests(unittest.TestCase):
    def test_text_findings_become_cn_only_evidence_claims(self):
        envelopes = questmobile_public_research_observations(payload())
        self.assertEqual(len(envelopes), 1)
        envelope = envelopes[0]
        self.assertEqual(envelope.source_id, "QM")
        self.assertEqual(envelope.source_origin_geography, "CN")
        self.assertEqual(envelope.relevance_geographies, ("CN",))
        self.assertEqual(envelope.actor_ids, ())
        self.assertIn("xuzhou_applicability", envelope.unknown_fields)
        self.assertEqual(len(envelope.claims), 1)
        claim = envelope.claims[0]
        self.assertEqual(claim.primitive, "EVIDENCE")
        self.assertEqual(claim.concept, "PUBLIC_RESEARCH_FINDING_EXCERPT")
        self.assertEqual(claim.epistemic_status, "OBSERVED")
        self.assertEqual(claim.geography, "CN")
        self.assertEqual(claim.value["representativeness_status"], "NOT_ESTABLISHED_FROM_PUBLIC_PAGE")
        self.assertEqual(claim.value["current_local_reality_status"], "NOT_ESTABLISHED")
        self.assertEqual(claim.value["paid_demand_status"], "NOT_ESTABLISHED")

    def test_image_only_report_is_not_promoted_to_observation(self):
        envelopes = questmobile_public_research_observations(payload())
        ids = {item.source_record_id for item in envelopes}
        self.assertNotIn("questmobile-report:2090000000000000000", ids)

    def test_exact_excerpt_is_the_evidence_not_a_parsed_numeric_fact(self):
        envelope = questmobile_public_research_observations(payload())[0]
        excerpt = payload()["reports"][0]["findings"][0]["excerpt"]
        self.assertEqual(envelope.evidence[0].excerpt, excerpt)
        self.assertEqual(envelope.claims[0].primitive, "EVIDENCE")
        self.assertNotIn("market_size", envelope.claims[0].value)
        self.assertNotIn("demand", envelope.claims[0].value)

    def test_excerpt_hash_tampering_fails_closed(self):
        item = payload()
        item["reports"][0]["findings"][0]["excerpt_sha256"] = "c" * 64
        with self.assertRaisesRegex(ValueError, "excerpt hash mismatch"):
            questmobile_public_research_observations(item)

    def test_page_provenance_tampering_fails_closed(self):
        item = payload()
        item["reports"][0]["provenance"]["payload_sha256"] = "c" * 64
        with self.assertRaisesRegex(ValueError, "provenance hash"):
            questmobile_public_research_observations(item)

    def test_no_local_geography_can_be_manufactured(self):
        envelope = questmobile_public_research_observations(payload())[0]
        self.assertNotIn("CN-JS", envelope.relevance_geographies)
        self.assertNotIn("CN-JS-XZ", envelope.relevance_geographies)
        self.assertTrue(all(claim.geography == "CN" for claim in envelope.claims))

    def test_declared_finding_count_must_match_adapted_findings(self):
        item = payload()
        item["text_finding_count"] = 2
        with self.assertRaisesRegex(ValueError, "declared text_finding_count"):
            questmobile_public_research_observations(item)


if __name__ == "__main__":
    unittest.main()
