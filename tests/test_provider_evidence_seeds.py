import csv
import tempfile
import unittest
from pathlib import Path

from src.provider_evidence_seeds import (
    ProcurementResultSeed,
    load_procurement_result_seeds,
    verify_procurement_result_seeds,
)
from src.xuzhou_procurement_results import ProcurementAward


class FakeResultAdapter:
    def __init__(self, awards_by_url=None, errors_by_url=None):
        self.awards_by_url = awards_by_url or {}
        self.errors_by_url = errors_by_url or {}
        self.urls = []

    def fetch_awards(self, url, *, fallback_title=None):
        self.urls.append(url)
        if url in self.errors_by_url:
            raise ValueError(self.errors_by_url[url])
        return self.awards_by_url.get(url, [])


def award(url, title, project_name, supplier="江苏山祥建设工程有限公司"):
    return ProcurementAward(
        source_id="XZ_GGZY_PROCUREMENT_RESULT",
        title=title,
        url=url,
        publication_date="2026-09-09",
        project_id="JSZC-TEST",
        project_name=project_name,
        buyer_actor="徐州市水务局",
        supplier_name=supplier,
        supplier_credit_code="91320312302101990G",
        supplier_address="徐州市",
        award_amount_rmb="1186000.00",
        award_amount_raw="1186000元",
        service_name=project_name,
        provenance={"payload_sha256": "f" * 64},
    )


class ProviderEvidenceSeedTests(unittest.TestCase):
    PUMP_URL = (
        "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20260909/"
        "00d7b76b-b26d-47f1-bc2e-00c7a8f7cb0d.html"
    )

    def test_matching_seed_requires_official_refetch_and_exact_reclassification(self):
        parsed = award(
            self.PUMP_URL,
            "徐州市水务局2026年度市管雨污水泵站设施维修养护市场化中标结果公告采购包2",
            "2026年度市管雨污水泵站设施维修养护市场化、市直管截污闸门维修养护",
        )
        adapter = FakeResultAdapter({self.PUMP_URL: [parsed]})
        payload = verify_procurement_result_seeds(
            [
                ProcurementResultSeed(
                    seed_id="pump",
                    url=self.PUMP_URL,
                    expected_capability_key="WATER_PUMP_STATION_MAINTENANCE",
                    discovered_via="public_web_research",
                )
            ],
            adapter=adapter,
        )
        self.assertEqual(adapter.urls, [self.PUMP_URL])
        self.assertEqual(payload["verified_seed_count"], 1)
        self.assertEqual(payload["award_count"], 1)
        self.assertEqual(payload["rejected_seed_count"], 0)
        self.assertEqual(payload["awards"][0]["supplier_name"], "江苏山祥建设工程有限公司")
        self.assertEqual(payload["awards"][0]["navigation_seed_id"], "pump")
        self.assertEqual(payload["awards"][0]["provenance"]["payload_sha256"], "f" * 64)

    def test_expected_capability_never_overrides_official_detail(self):
        parsed = award(
            self.PUMP_URL,
            "徐州市财政效能中心财政信息化服务中标公告采购包2",
            "徐州市数智化财政业务平台-财政信息化服务",
            supplier="南京中铁信息工程有限公司",
        )
        payload = verify_procurement_result_seeds(
            [
                ProcurementResultSeed(
                    seed_id="wrong-expectation",
                    url=self.PUMP_URL,
                    expected_capability_key="WATER_PUMP_STATION_MAINTENANCE",
                )
            ],
            adapter=FakeResultAdapter({self.PUMP_URL: [parsed]}),
        )
        self.assertEqual(payload["verified_seed_count"], 0)
        self.assertEqual(payload["award_count"], 0)
        self.assertEqual(payload["rejections"][0]["reason"], "OFFICIAL_DETAIL_CAPABILITY_MISMATCH")
        self.assertEqual(
            payload["rejections"][0]["observed_capability_keys"],
            ["FINANCE_DIGITAL_IT_SERVICE"],
        )

    def test_seed_without_supplier_evidence_is_rejected(self):
        payload = verify_procurement_result_seeds(
            [
                ProcurementResultSeed(
                    seed_id="void",
                    url=self.PUMP_URL,
                    expected_capability_key="WATER_PUMP_STATION_MAINTENANCE",
                )
            ],
            adapter=FakeResultAdapter({self.PUMP_URL: []}),
        )
        self.assertEqual(payload["award_count"], 0)
        self.assertEqual(
            payload["rejections"][0]["reason"],
            "OFFICIAL_DETAIL_HAS_NO_SUPPLIER_AWARD",
        )

    def test_seed_csv_rejects_non_official_or_duplicate_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seeds.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["seed_id", "url", "expected_capability_key"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "seed_id": "bad",
                        "url": "https://example.com/result.html",
                        "expected_capability_key": "WATER_PUMP_STATION_MAINTENANCE",
                    }
                )
            with self.assertRaises(ValueError):
                load_procurement_result_seeds(path)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seeds.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["seed_id", "url", "expected_capability_key"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "seed_id": "one",
                        "url": self.PUMP_URL,
                        "expected_capability_key": "WATER_PUMP_STATION_MAINTENANCE",
                    }
                )
                writer.writerow(
                    {
                        "seed_id": "two",
                        "url": self.PUMP_URL,
                        "expected_capability_key": "WATER_PUMP_STATION_MAINTENANCE",
                    }
                )
            with self.assertRaises(ValueError):
                load_procurement_result_seeds(path)


if __name__ == "__main__":
    unittest.main()
