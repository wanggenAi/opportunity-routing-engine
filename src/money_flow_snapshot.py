"""Orchestrate live China → Jiangsu → Xuzhou money-flow evidence.

This snapshot is an evidence index, not an opportunity scorer. It intentionally
keeps source payloads separate and exposes unavailable dimensions as UNKNOWN.
There is no cross-source summation because the feeds differ in period, unit,
coverage and transaction meaning (for example a tender estimate is not a paid
cash flow, customs trade is not bank credit, and a scoped financing campaign is
not a citywide financing-demand total).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from src.gacc_trade_corroboration import JiangsuTradeCorroborator
from src.gacc_trade_flow import GaccTradeFlowAdapter
from src.jiangsu_money_flow import JiangsuMoneyFlowAdapter
from src.pbc_jiangsu_credit import PbcJiangsuCreditAdapter
from src.pbc_money_flow import PbcMoneyFlowAdapter
from src.pbc_regional_financing import PbcRegionalFinancingAdapter
from src.regional_adapters import XuzhouProcurementAdapter
from src.xuzhou_construction_capex import XuzhouConstructionTenderAdapter
from src.xuzhou_enterprise_funding_demand import XuzhouEnterpriseFundingDemandAdapter


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
    "CUSTOMS_PLAINTEXT_HTTP_REQUIRES_CORROBORATION",
    "CUSTOMS_CROSS_CURRENCY_VALUES_NOT_DIRECTLY_COMPARABLE",
    "XUZHOU_SPECIFIC_AREA_TRADE_IS_NOT_CITY_TOTAL",
    "PROVINCE_CORROBORATION_DOES_NOT_CORROBORATE_XUZHOU_SPECIFIC_AREA_VALUES",
    "SCOPED_ENTERPRISE_FUNDING_DEMAND_IS_NOT_CITYWIDE_TOTAL",
    "SME_IS_NOT_PRIVATE_ENTERPRISE",
    "NO_CROSS_PROGRAM_FINANCING_DEMAND_SUM",
    "NO_CROSS_PERIOD_FINANCING_DEMAND_SUM",
    "DIRECT_FUNDING_DEMAND_EVIDENCE_PROVES_NEED_ONLY",
    "MONEY_FLOW_EVIDENCE_DOES_NOT_PROVE_NEED_SURPLUS_BLOCKER",
    "NO_OPPORTUNITY_INFERENCE",
]


def _collect_customs_trade_flow() -> dict[str, Any]:
    payload = GaccTradeFlowAdapter().collect()
    return JiangsuTradeCorroborator().corroborate(payload)


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
            key="jiangsu_customs_trade_flow",
            geography="Jiangsu/XuzhouSpecificAreas",
            evidence_role="provincial_trade_flow_and_specific_area_customs_activity",
            collect=_collect_customs_trade_flow,
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
        SnapshotFeed(
            key="xuzhou_scoped_enterprise_funding_demand",
            geography="Xuzhou",
            evidence_role="scoped_direct_enterprise_financing_demand",
            collect=lambda: XuzhouEnterpriseFundingDemandAdapter().collect(),
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
        # Existing event feeds predate the explicit data_available field. A
        # successfully returned batch is AVAILABLE source evidence even when a
        # field in an individual event is missing; those fields remain None.
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

    customs = feed_map["jiangsu_customs_trade_flow"]
    customs_payload = customs.get("payload") or {}
    province_corroborated = (
        customs["status"] == "AVAILABLE"
        and customs_payload.get("corroboration_status") == "PERIOD_IDENTITY_DIRECTION_CORROBORATED"
        and (customs_payload.get("jiangsu_importer_exporter_location") or {}).get("total_ytd_usd_thousand") is not None
    )
    if province_corroborated:
        jiangsu_trade_status = "AVAILABLE"
    elif customs["status"] == "AVAILABLE":
        jiangsu_trade_status = "PARTIAL"
    else:
        jiangsu_trade_status = "UNKNOWN"

    xuzhou_location = customs_payload.get("xuzhou_importer_exporter_location")
    xuzhou_areas = customs_payload.get("xuzhou_specific_areas") or []
    if customs["status"] == "AVAILABLE" and xuzhou_location:
        xuzhou_city_trade_status = "PARTIAL"
    else:
        xuzhou_city_trade_status = "UNKNOWN"
    xuzhou_specific_area_status = (
        "PARTIAL" if customs["status"] == "AVAILABLE" and xuzhou_areas else "UNKNOWN"
    )

    funding = feed_map["xuzhou_scoped_enterprise_funding_demand"]
    funding_payload = funding.get("payload") or {}
    funding_events = funding_payload.get("events") or []
    if funding["status"] == "AVAILABLE" and funding_events:
        xuzhou_enterprise_funding_status = "PARTIAL"
    else:
        xuzhou_enterprise_funding_status = "UNKNOWN"
    explicit_private_events = [
        event
        for event in funding_events
        if event.get("actor_scope") == "PRIVATE_ENTERPRISE"
        and event.get("private_enterprise_scope_explicit") is True
    ]
    if funding["status"] == "AVAILABLE" and explicit_private_events:
        xuzhou_private_funding_status = "PARTIAL"
    else:
        xuzhou_private_funding_status = "UNKNOWN"

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
        "jiangsu_trade_flow": {
            "status": jiangsu_trade_status,
            "feeds": {"jiangsu_customs_trade_flow": customs["status"]},
            "note": (
                "GACC importer/exporter-location trade is a separate trade-flow dimension. "
                "AVAILABLE requires same-period Jiangsu HTTPS corroboration of period, geography and import/export direction; "
                "CNY and USD values are not directly compared."
            ),
        },
        "xuzhou_institutional_spend": state(
            ["xuzhou_government_procurement", "xuzhou_construction_tenders"],
            note="Public procurement and construction solicitation evidence; notices are not completed payments.",
        ),
        "xuzhou_specific_area_trade": {
            "status": xuzhou_specific_area_status,
            "feeds": {"jiangsu_customs_trade_flow": customs["status"]},
            "note": (
                "Current customs evidence may expose Xuzhou CBZ/BLC specific-area activity. "
                "It remains PARTIAL because provincial corroboration does not independently validate those area values, "
                "and specific areas are not the whole city."
            ),
        },
        "xuzhou_city_trade_flow": {
            "status": xuzhou_city_trade_status,
            "feeds": {"jiangsu_customs_trade_flow": customs["status"]},
            "note": (
                "Specific-area customs rows cannot substitute for a Xuzhou whole-city trade row. "
                "Even a future city-location row remains PARTIAL until city-scope corroboration is established."
            ),
        },
        "xuzhou_financial_balance": {
            "status": "UNKNOWN",
            "feeds": {},
            "note": "No direct live Xuzhou bank deposit/loan balance feed is connected yet.",
        },
        "xuzhou_enterprise_funding_demand": {
            "status": xuzhou_enterprise_funding_status,
            "feeds": {"xuzhou_scoped_enterprise_funding_demand": funding["status"]},
            "note": (
                "Direct financing-demand amounts reported by the Xuzhou Government Office make enterprise funding demand "
                "answerable only at PARTIAL scope when evidence is program/batch-specific. Events are not summed across "
                "programs or periods and do not establish a citywide total."
            ),
        },
        "xuzhou_private_enterprise_funding_demand": {
            "status": xuzhou_private_funding_status,
            "feeds": {"xuzhou_scoped_enterprise_funding_demand": funding["status"]},
            "note": (
                "PRIVATE-enterprise answerability requires source text to explicitly identify 民营企业/民营经济. "
                "SME, micro-enterprise or general-enterprise evidence is never relabeled as private-enterprise evidence; "
                "even explicit private events remain PARTIAL when scoped to a program/batch rather than the whole city."
            ),
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

    customs = feed_map["jiangsu_customs_trade_flow"]
    if customs["status"] == "AVAILABLE":
        payload = customs["payload"]
        result["Jiangsu"]["customs_trade_flow"] = {
            "period": payload.get("period"),
            "unit": payload.get("unit"),
            "transport_security": payload.get("transport_security"),
            "corroboration_status": payload.get("corroboration_status"),
            "corroboration": payload.get("corroboration"),
            "importer_exporter_location": payload.get("jiangsu_importer_exporter_location"),
            "scope_note": "Importer/exporter registration location; not domestic production/consumption origin-destination.",
        }
        result["Xuzhou"]["customs_specific_areas"] = {
            "period": payload.get("period"),
            "transport_security": payload.get("transport_security"),
            "province_corroboration_status": payload.get("corroboration_status"),
            "specific_area_value_corroboration": "NOT_ESTABLISHED",
            "scope": "SPECIFIC_AREAS_ONLY",
            "city_location_row": payload.get("xuzhou_importer_exporter_location"),
            "areas": payload.get("xuzhou_specific_areas", []),
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

    funding = feed_map["xuzhou_scoped_enterprise_funding_demand"]
    if funding["status"] == "AVAILABLE":
        payload = funding["payload"]
        result["Xuzhou"]["enterprise_financing_demand"] = {
            "evidence_kind": payload.get("evidence_kind"),
            "event_count": payload.get("event_count"),
            "errors": payload.get("error_count"),
            "latest_freshness": payload.get("latest_freshness"),
            "events": payload.get("events", []),
            "aggregation_policy": "NO_CROSS_PROGRAM_OR_PERIOD_SUM",
            "scope_note": (
                "Direct NEED evidence only. Every event retains its source-declared actor/program scope; "
                "scoped amounts are not a citywide total and SME evidence is not private-enterprise evidence."
            ),
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

    # Answerability currently has a fixed production contract. Tests using
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
        "schema_version": "money-flow-snapshot-v3",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "geography_path": ["China", "Jiangsu", "Xuzhou"],
        "truth_boundaries": TRUTH_BOUNDARIES,
        "status_counts": status_counts,
        "answerability": _answerability(feed_map),
        "headline_evidence": _headline_evidence(feed_map),
        "feeds": feed_map,
        "interpretation_boundary": (
            "This artifact indexes observed money-flow, trade-flow, institutional-spend and scoped direct financing-demand evidence. "
            "A direct financing-demand event establishes NEED only within its reported scope; it does not establish citywide prevalence, "
            "a surplus resource, a transaction blocker or an opportunity. Promotion still requires separately evidenced "
            "NEED + SURPLUS RESOURCE + TRANSACTION BLOCKER."
        ),
    }
