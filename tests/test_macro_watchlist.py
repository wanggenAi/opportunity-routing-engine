import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.macro_watchlist import (
    MacroWatchItem,
    collect_nbs_watchlist,
    load_macro_watchlist,
    period_lookback,
)


class FakeAdapter:
    def dates(self, page, *, cid):
        return {"data": {"dt_all": "202608MM", "dt_name": "2026年8月"}}

    def indicators(self, page, *, cid, dt=""):
        return [
            {
                "indicator_id": "ind-1",
                "label": "测试指标",
                "unit": "%",
                "catalog_id": cid,
                "raw": {},
            }
        ]

    def fetch_values(self, page, *, cid, indicator_ids, periods=None, areas=None, show_type=1):
        return {
            "request": {
                "payload_sha256": "a" * 64,
                "fetched_at_utc": "2026-09-11T00:00:00+00:00",
            },
            "observed_row_count": 2,
            "populated_row_count": 1,
            "populated_periods": ["202607MM"],
            "latest_populated_period": "202607MM",
            "records": [
                {
                    "indicator_id": "ind-1",
                    "period_code": "202608MM",
                    "value": "",
                    "value_present": False,
                },
                {
                    "indicator_id": "ind-1",
                    "period_code": "202607MM",
                    "value": "100.8",
                    "value_present": True,
                },
            ],
            "raw": {},
        }


class MacroWatchlistTests(unittest.TestCase):
    def test_period_lookback_crosses_year_boundary(self):
        self.assertEqual(
            period_lookback("202601MM", "month", 3),
            ["202601MM", "202512MM", "202511MM"],
        )

    def test_period_lookback_quarter_and_year(self):
        self.assertEqual(
            period_lookback("202601SS", "quarter", 2),
            ["202601SS", "202504SS"],
        )
        self.assertEqual(
            period_lookback("2026YY", "year", 2),
            ["2026YY", "2025YY"],
        )

    def test_selects_latest_populated_not_latest_advertised(self):
        item = MacroWatchItem(
            signal_id="TEST",
            source_id="CN_NBS",
            page="monthData",
            cid="cid-1",
            indicator_id="ind-1",
            expected_label="测试指标",
            frequency="month",
            unit="%",
            geography="China",
            metric_kind="index",
            lookback_periods=3,
            status="ACTIVE",
        )
        result = collect_nbs_watchlist(FakeAdapter(), [item])
        signal = result["signals"][0]
        self.assertEqual(signal["status"], "AVAILABLE")
        self.assertEqual(signal["latest_advertised_period"], "202608MM")
        self.assertEqual(signal["latest_populated_period"], "202607MM")
        self.assertEqual(signal["period_lag"], 1)
        self.assertEqual(signal["value"], "100.8")

    def test_identity_drift_blocks_availability(self):
        item = MacroWatchItem(
            signal_id="TEST",
            source_id="CN_NBS",
            page="monthData",
            cid="cid-1",
            indicator_id="ind-1",
            expected_label="错误标签",
            frequency="month",
            unit="%",
            geography="China",
            metric_kind="index",
            lookback_periods=3,
            status="ACTIVE",
        )
        result = collect_nbs_watchlist(FakeAdapter(), [item])
        self.assertEqual(result["signals"][0]["status"], "LABEL_DRIFT")

    def test_watchlist_loader_is_strict(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "watch.csv"
            path.write_text(
                "signal_id,source_id,page,cid,indicator_id,expected_label,frequency,unit,geography,metric_kind,lookback_periods,status\n"
                "TEST,CN_NBS,monthData,cid-1,ind-1,测试指标,month,%,China,index,3,ACTIVE\n",
                encoding="utf-8",
            )
            items = load_macro_watchlist(path)
            self.assertEqual(items[0].lookback_periods, 3)


if __name__ == "__main__":
    unittest.main()
