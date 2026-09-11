"""Orchestrate live China → Jiangsu → Xuzhou money-flow evidence.

This snapshot is an evidence index, not an opportunity scorer.  It intentionally
keeps source payloads separate and exposes unavailable dimensions as UNKNOWN.
There is no cross-source summation because the feeds differ in period, unit,
coverage and transaction meaning (for example a tender estimate is not a paid
cash flow).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from src.jiangsu_money_flow import JiangsuMoneyFlowAdapter
from src.pbc_jiangsu_credit import PbcJiangsuCreditAdapter
from src.pbc_money_flow import PbcMoneyFlowAdapter
from src.pbc_regional_financing import PbcRegionalFinancingAdapter
from src.regional_adapters import XuzhouProcurementAdapter
from src.xuzhou_construction_capex import XuzhouConstructionTenderAdapter


Collector = Callable[[], dict[str, Any]]


@dataclass(frozen=True)
class SnapshotFeed:
    key: str
    geography: str
    evidence_role: str
    collect: Collector


TRUTH_BOUNDARIES = [
    "MISSING_STAYS_UNKNOWN",
    "SOURCE_ERROR_NEVER_BECOMES_PASS",
    "NO_CROSS_SOURCE_SUM",
    "NO_TENDER_SUM_WITHOUT_PROJECT_DEDUP",
    "TENDER_NOTICE_IS_NOT_COMPLETED_PAYMENT",
    "PROCUREMENT_NOTICE_IS_NOT_COMPLETED_PAYMENT",
    "MONEY_FLOW_EVIDENCE_DOES_NOT_PROVE_NEED_SURPLUS_BLOCKER",
    "NO_OPPORTUNITY_INFERENCE",
]


def default_feeds() -> list[SnapshotFeed]:
    return [
        SnapshotFeed(
            key="china_pbc_financial_statistics",
            geography="China",
            evidence_role="national_money_credit_liquidity",
            collect=lambda: PbcMoneyFlowAdapter().collect_latest(),
        ),
        SnapshotFeed(
            key="jiangsu_pbc_regional_social_financing",
            geography="Jiangsu",
            evidence_role="provincial_social_financing_flow",
            collect=lambda: PbcRegionalFinancingAdapter().collect_region(region="江苏"),
        ),
        SnapshotFeed(
            key="jiangsu_pbc_credit_deposit",
            geography="Jiangsu",
            evidence_role="provincial_deposit_loan_levels",
            collect=lambda: PbcJiangsuCreditAdapter().collect(),
        ),
        SnapshotFeed(
            key="jiangsu_stats_economic_operation",
            geography="Jiangsu",
            evidence_role="provincial_investment_consumption_finance_corroboration",
            collect=lambda: JiangsuMoneyFlowAdapter().collect(),
        ),
        SnapshotFeed(
            key="xuzhou_government_procurement",
            geography="Xuzhou",
            evidence_role="institutional_purchase_demand",
            collect=lambda: XuzhouProcurementAdapter().collect_recent_events(limit=10),
        ),
        SnapshotFeed(
            key="xuzhou_construction_tenders",
            geography="Xuzhou",
            evidence_role="local_construction_capex_solicitation",
            collect=lambda: XuzhouConstructionTenderAdapter().collect_recent_events(limit=10),
        ),
    ]


def _safe_collect(feed: SnapshotFeed) -> dict[str, Any]:
    try:
        payload = feed.collect()
    except Exception as exc:
        return {
            "key": feed.key,
            "geography": feed.geography,
            "evidence_role": feed.evidence_role,
            "status": "ERROR",
            "data_available": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "payload": None,
        }

    available = payload.get("data_available")
    if available is False:
        status = "UNAVAILABLE"
    else:
        # Existing event feeds predate the explicit data_available field.  A
        # successfully returned batch is AVAILABLE evidence even when a field in
        # an individual event is missing; those fields remain None in the payload.
        status = "AVAILABLE"
    return {
        "key": feed.key,
        "geography": feed.geography,
        "evidence_role": feed.evidence_role,
        "status": status,
        "data_available": status == "AVAILABLE",
        "error_type": None,
        "error": None,
        "payload": payload,
    }


def _answerability(feed_map: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    def state(keys: list[str], *, note: str) -> dict[str, Any]:
        statuses = {key: feed_map[key]["status"] for key in keys}
        if all(value == "AVAILABLE" for value in statuses.values()):
            value = "AVAILABLE"
        elif any(value == "AVAILABLE" for value in statuses.values()):
            value = "PARTIAL"
        else:
            value = "UNKNOWN"
        return {"status": value, "feeds": statuses, "note": note}

    return {
        "china_money_flow": state(
            ["china_pbc_financial_statistics"],
            note="National monetary, credit and social-financing release evidence.",
        ),
        "jiangsu_money_flow": state(
            [
                "jiangsu_pbc_regional_social_financing",
                "jiangsu_pbc_credit_deposit",
                "jiangsu_stats_economic_operation",
            ],
            note="Provincial financing, bank-balance and investment/consumption evidence; sources corroborate but are not additive.",
        ),
        "xuzhou_institutional_spend": state(
            ["xuzhou_government_procurement", "xuzhou_construction_tenders"],
            note="Public procurement and construction solicitation evidence; notices are not completed payments.",
        ),
        "xuzhou_financial_balance": {
            "status": "UNKNOWN",
            "feeds": {},
            "note": "No direct live Xuzhou bank deposit/loan balance feed is connected yet.",
        },
        "xuzhou_private_enterprise_funding_demand": {
            "status": "UNKNOWN",
            "feeds": {},
            "note": "Tender/procurement activity cannot substitute for direct enterprise financing-demand evidence.",
        },
    }


def _headline_evidence(feed_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Expose mechanically selected facts without combining or scoring them."""
    result: dict[str, Any] = {"China": {}, "Jiangsu": {}, "Xuzhou": {}}

    national = feed_map["china_pbc_financial_statistics"]
    if national["status"] == "AVAILABLE":
        payload = national["payload"]
        result["China"]["pbc_release"] = {
            "title": payload.get("latest_release", {}).get("title"),
            "release_date": payload.get("latest_release", {}).get("release_date"),
            "metrics": payload.get("latest_release", {}).get("metrics", {}),
            "freshness": payload.get("freshness"),
        }

    regional = feed_map["jiangsu_pbc_regional_social_financing"]
    if regional["status"] == "AVAILABLE":
        payload = regional["payload"]
        result["Jiangsu"]["regional_social_financing"] = {
            "table_title": payload.get("table_title"),
            "release_date": payload.get("release_date"),
            "observation": payload.get("region_observation"),
        }

    credit = feed_map["jiangsu_pbc_credit_deposit"]
    if credit["status"] == "AVAILABLE":
        payload = credit["payload"]
        result["Jiangsu"]["credit_deposit"] = {
            "table_title": payload.get("table_title"),
            "observation_period": payload.get("observation_period"),
            "release_date": payload.get("release_date"),
            "metrics": payload.get("observation", {}).get("metrics", {}),
            "freshness": payload.get("freshness"),
        }

    js_stats = feed_map["jiangsu_stats_economic_operation"]
    if js_stats["status"] == "AVAILABLE":
        payload = js_stats["payload"]
        result["Jiangsu"]["economic_operation"] = {
            "release_title": payload.get("release_title"),
            "publication_date": payload.get("publication_date"),
            "observation_period": payload.get("observation_period"),
            "metrics": payload.get("metrics", []),
            "freshness": payload.get("freshness"),
        }

    procurement = feed_map["xuzhou_government_procurement"]
    if procurement["status"] == "AVAILABLE":
        payload = procurement["payload"]
        result["Xuzhou"]["government_procurement"] = {
            "discovered": payload.get("discovery", {}).get("item_count"),
            "parsed_events": payload.get("event_count"),
            "errors": payload.get("error_count"),
            "events": payload.get("events", []),
        }

    construction = feed_map["xuzhou_construction_tenders"]
    if construction["status"] == "AVAILABLE":
        payload = construction["payload"]
        result["Xuzhou"]["construction_tenders"] = {
            "discovered": payload.get("discovery", {}).get("item_count"),
            "parsed_events": payload.get("event_count"),
            "errors": payload.get("error_count"),
            "amount_evidence_count": payload.get("amount_evidence_count"),
            "funding_evidence_count": payload.get("funding_evidence_count"),
            "reissue_count": payload.get("reissue_count"),
            "events": payload.get("events", []),
            "aggregation_policy": payload.get("aggregation_policy"),
        }

    return result


def collect_money_flow_snapshot(
    *, feeds: list[SnapshotFeed] | None = None
) -> dict[str, Any]:
    selected = feeds or default_feeds()
    if not selected:
        raise ValueError("money-flow snapshot requires at least one feed")
    keys = [feed.key for feed in selected]
    if len(keys) != len(set(keys)):
        raise ValueError("money-flow snapshot feed keys must be unique")

    collected = [_safe_collect(feed) for feed in selected]
    feed_map = {item["key"]: item for item in collected}

    # Answerability currently has a fixed production contract.  Tests using
    # injected subsets still need all keys represented explicitly as UNKNOWN.
    for feed in default_feeds():
        feed_map.setdefault(
            feed.key,
            {
                "key": feed.key,
                "geography": feed.geography,
                "evidence_role": feed.evidence_role,
                "status": "NOT_RUN",
                "data_available": False,
                "error_type": None,
                "error": None,
                "payload": None,
            },
        )

    status_counts = {
        status: sum(1 for item in feed_map.values() if item["status"] == status)
        for status in ("AVAILABLE", "UNAVAILABLE", "ERROR", "NOT_RUN")
    }
    return {
        "schema_version": "money-flow-snapshot-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "geography_path": ["China", "Jiangsu", "Xuzhou"],
        "truth_boundaries": TRUTH_BOUNDARIES,
        "status_counts": status_counts,
        "answerability": _answerability(feed_map),
        "headline_evidence": _headline_evidence(feed_map),
        "feeds": feed_map,
        "interpretation_boundary": (
            "This artifact indexes observed money-flow and institutional-spend evidence. "
            "It does not infer an opportunity. Promotion still requires separately evidenced "
            "NEED + SURPLUS RESOURCE + TRANSACTION BLOCKER."
        ),
    }
