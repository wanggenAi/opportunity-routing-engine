"""Truth-preserving adapters from existing live artifacts into ObservationEnvelope.

These adapters translate already-collected production evidence into the source-neutral
Observation Fabric. They do not create demand, payer, payment, availability,
permission, opportunity or transaction truth.
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping, Sequence

from src.observation_fabric import EvidenceRef, ObservationEnvelope, SemanticClaim

PARSER_VERSION = "live-observation-adapters.v1"


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _sequence(value: object, field: str) -> Sequence[object]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


def _sha256(value: object, field: str) -> str:
    result = _text(value, field).lower()
    if len(result) != 64 or any(ch not in "0123456789abcdef" for ch in result):
        raise ValueError(f"{field} must be a SHA-256 hex digest")
    return result


def _stable_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()[:24]}"


def _source_actor_id(source_id: str, role: str, name: str) -> str:
    return _stable_id(f"actor:{source_id}:{role}", name)


def _provenance(value: object, field: str) -> Mapping[str, Any]:
    item = _mapping(value, field)
    _text(item.get("url"), f"{field}.url")
    _sha256(item.get("payload_sha256"), f"{field}.payload_sha256")
    _text(item.get("fetched_at_utc"), f"{field}.fetched_at_utc")
    return item


def jiangsu_money_flow_observations(payload: Mapping[str, Any]) -> tuple[ObservationEnvelope, ...]:
    """Convert one official Jiangsu release artifact into one aggregate observation."""

    if payload.get("source_id") != "JS_STATS":
        raise ValueError("unexpected Jiangsu source_id")
    if payload.get("data_available") is not True:
        raise ValueError("Jiangsu money-flow artifact has no available data")
    if payload.get("geography") != "Jiangsu":
        raise ValueError("unexpected Jiangsu geography")

    provenance = _mapping(payload.get("provenance"), "provenance")
    release_prov = _provenance(provenance.get("release"), "provenance.release")
    release_url = _text(payload.get("release_url"), "release_url")
    if release_url != release_prov["url"]:
        raise ValueError("Jiangsu release URL diverges from release provenance")
    release_hash = _sha256(release_prov.get("payload_sha256"), "provenance.release.payload_sha256")
    retrieved_at = _text(release_prov.get("fetched_at_utc"), "provenance.release.fetched_at_utc")
    metrics = _sequence(payload.get("metrics"), "metrics")
    if not metrics:
        raise ValueError("Jiangsu money-flow artifact contains no metrics")

    evidence: list[EvidenceRef] = []
    claims: list[SemanticClaim] = []
    seen_signals: set[str] = set()
    for raw_metric in metrics:
        metric = _mapping(raw_metric, "metric")
        signal_id = _text(metric.get("signal_id"), "metric.signal_id")
        if signal_id in seen_signals:
            raise ValueError(f"duplicate Jiangsu signal_id: {signal_id}")
        seen_signals.add(signal_id)
        if metric.get("source_id") != "JS_STATS":
            raise ValueError(f"metric {signal_id} has unexpected source_id")
        metric_url = _text(metric.get("source_url"), f"metric {signal_id}.source_url")
        if metric_url != release_url:
            raise ValueError(f"metric {signal_id} source URL diverges from release")
        metric_hash = _sha256(metric.get("provenance_sha256"), f"metric {signal_id}.provenance_sha256")
        if metric_hash != release_hash:
            raise ValueError(f"metric {signal_id} provenance hash diverges from release")
        kind = _text(metric.get("metric_kind"), f"metric {signal_id}.metric_kind")
        if kind == "yoy_growth":
            primitive = "CHANGE"
        elif kind == "level":
            primitive = "STATE"
        else:
            raise ValueError(f"unsupported Jiangsu metric_kind: {kind}")
        matched_text = _text(metric.get("matched_text"), f"metric {signal_id}.matched_text")
        ref_id = f"metric:{signal_id}"
        evidence.append(EvidenceRef(ref_id, release_url, matched_text, release_hash))
        claims.append(
            SemanticClaim(
                claim_id=signal_id,
                primitive=primitive,
                concept=signal_id,
                epistemic_status="OBSERVED",
                evidence_refs=(ref_id,),
                value={
                    "value": metric.get("value"),
                    "unit": metric.get("unit"),
                    "metric_kind": kind,
                    "observation_period": metric.get("observation_period") or payload.get("observation_period"),
                    "publication_date": metric.get("publication_date") or payload.get("publication_date"),
                },
                geography="CN-JS",
            )
        )

    return (
        ObservationEnvelope(
            observation_id=_stable_id("obs:JS_STATS:release", release_url),
            source_id="JS_STATS",
            source_record_id=release_url,
            source_locator=release_url,
            source_origin_geography="CN-JS",
            relevance_geographies=("CN-JS",),
            source_tier="OFFICIAL_GOVERNMENT_PRIMARY",
            observed_at=retrieved_at,
            retrieved_at=retrieved_at,
            parser_version=PARSER_VERSION,
            raw_payload_hash=release_hash,
            sampling_boundary="LATEST_OFFICIAL_JIANGSU_RELEASE_SELECTED_BY_EXISTING_ADAPTER",
            evidence=tuple(evidence),
            claims=tuple(claims),
            actor_ids=(),
            unknown_fields=("exact_publication_time",),
        ),
    )


def xuzhou_procurement_observations(payload: Mapping[str, Any]) -> tuple[ObservationEnvelope, ...]:
    """Convert recent Xuzhou procurement notices without promoting budget into payment."""

    if payload.get("source_id") != "XZ_GGZY":
        raise ValueError("unexpected Xuzhou procurement source_id")
    if int(payload.get("error_count", 0)) != 0:
        raise ValueError("Xuzhou procurement artifact contains collection errors")
    events = _sequence(payload.get("events"), "events")
    result: list[ObservationEnvelope] = []
    for raw_event in events:
        event = _mapping(raw_event, "event")
        if event.get("source_id") != "XZ_GGZY":
            raise ValueError("procurement event has unexpected source_id")
        project_id = _text(event.get("project_id"), "event.project_id")
        url = _text(event.get("url"), "event.url")
        provenance = _provenance(event.get("provenance"), f"event {project_id}.provenance")
        if provenance["url"] != url:
            raise ValueError(f"procurement event {project_id} URL diverges from provenance")
        raw_hash = _sha256(provenance.get("payload_sha256"), f"event {project_id}.payload_sha256")
        retrieved_at = _text(provenance.get("fetched_at_utc"), f"event {project_id}.fetched_at_utc")
        title = _text(event.get("title"), f"event {project_id}.title")
        project_name = _text(event.get("project_name"), f"event {project_id}.project_name")

        evidence = [EvidenceRef("notice", url, title, raw_hash)]
        claims: list[SemanticClaim] = [
            SemanticClaim(
                claim_id="procurement_notice",
                primitive="STATE",
                concept="PUBLIC_PROCUREMENT_NOTICE",
                epistemic_status="OBSERVED",
                evidence_refs=("notice",),
                value={
                    "project_id": project_id,
                    "project_name": project_name,
                    "publication_date": event.get("publication_date"),
                    "procurement_method": event.get("procurement_method"),
                    "contract_term": event.get("contract_term"),
                },
                geography="CN-JS-XZ",
            )
        ]
        budget_raw = event.get("budget_raw")
        budget_rmb = event.get("budget_rmb")
        if budget_rmb is not None:
            if not isinstance(budget_raw, str) or not budget_raw.strip():
                raise ValueError(f"procurement event {project_id} has budget without evidence text")
            evidence.append(EvidenceRef("budget", url, budget_raw.strip(), raw_hash))
            claims.append(
                SemanticClaim(
                    claim_id="declared_budget",
                    primitive="FLOW",
                    concept="DECLARED_PROCUREMENT_BUDGET",
                    epistemic_status="OBSERVED",
                    evidence_refs=("budget",),
                    value={"amount_rmb": str(budget_rmb), "raw": budget_raw.strip(), "payment_status": "NOT_ESTABLISHED"},
                    geography="CN-JS-XZ",
                )
            )
        deadline = event.get("deadline")
        if isinstance(deadline, str) and deadline.strip():
            claims.append(
                SemanticClaim(
                    claim_id="submission_deadline",
                    primitive="TIME",
                    concept="PROCUREMENT_SUBMISSION_DEADLINE",
                    epistemic_status="OBSERVED",
                    evidence_refs=("notice",),
                    value=deadline.strip(),
                    geography="CN-JS-XZ",
                )
            )
        jv = event.get("joint_venture_allowed")
        if isinstance(jv, str) and jv.strip():
            claims.append(
                SemanticClaim(
                    claim_id="joint_venture_rule",
                    primitive="CONSTRAINT",
                    concept="JOINT_VENTURE_ALLOWED_AS_STATED",
                    epistemic_status="OBSERVED",
                    evidence_refs=("notice",),
                    value=jv.strip(),
                    geography="CN-JS-XZ",
                )
            )

        result.append(
            ObservationEnvelope(
                observation_id=_stable_id("obs:XZ_GGZY:procurement", project_id, url),
                source_id="XZ_GGZY",
                source_record_id=project_id,
                source_locator=url,
                source_origin_geography="CN-JS-XZ",
                relevance_geographies=("CN-JS-XZ",),
                source_tier="OFFICIAL_GOVERNMENT_PRIMARY",
                observed_at=retrieved_at,
                retrieved_at=retrieved_at,
                parser_version=PARSER_VERSION,
                raw_payload_hash=raw_hash,
                sampling_boundary="RECENT_XUZHOU_PROCUREMENT_NOTICES_SELECTED_BY_EXISTING_ADAPTER",
                evidence=tuple(evidence),
                claims=tuple(claims),
                actor_ids=(),
                unknown_fields=("buyer_actor", "exact_publication_time", "payment_status"),
            )
        )
    return tuple(result)


def xuzhou_resource_underuse_observations(payload: Mapping[str, Any]) -> tuple[ObservationEnvelope, ...]:
    """Convert public/linked asset listings while preserving underuse uncertainty."""

    if int(payload.get("error_count", 0)) != 0:
        raise ValueError("resource-underuse artifact contains collection errors")
    listings = _sequence(payload.get("listings"), "listings")
    result: list[ObservationEnvelope] = []
    for raw_listing in listings:
        listing = _mapping(raw_listing, "listing")
        source_id = _text(listing.get("source_id"), "listing.source_id")
        url = _text(listing.get("url"), "listing.url")
        title = _text(listing.get("title"), "listing.title")

        if "detail_provenance" in listing:
            detail_prov = _provenance(listing.get("detail_provenance"), "listing.detail_provenance")
            discovery_prov = _provenance(listing.get("discovery_provenance"), "listing.discovery_provenance")
            if detail_prov["url"] != url:
                raise ValueError("linked asset detail URL diverges from provenance")
            if listing.get("source_origin_verified") is not True:
                raise ValueError("linked asset lacks verified Xuzhou source origin")
            raw_hash = _sha256(detail_prov.get("payload_sha256"), "listing.detail payload_sha256")
            retrieved_at = _text(detail_prov.get("fetched_at_utc"), "listing.detail fetched_at_utc")
            evidence = [
                EvidenceRef("listing", url, title, raw_hash),
                EvidenceRef(
                    "official_discovery",
                    _text(discovery_prov.get("url"), "listing.discovery url"),
                    "Official Xuzhou agency-list discovery path",
                    _sha256(discovery_prov.get("payload_sha256"), "listing.discovery payload_sha256"),
                ),
            ]
            source_tier = "OFFICIAL_DISCOVERY_WITH_LINKED_DETAIL"
        else:
            prov = _provenance(listing.get("provenance"), "listing.provenance")
            if prov["url"] != url:
                raise ValueError("public asset URL diverges from provenance")
            raw_hash = _sha256(prov.get("payload_sha256"), "listing.payload_sha256")
            retrieved_at = _text(prov.get("fetched_at_utc"), "listing.fetched_at_utc")
            evidence = [EvidenceRef("listing", url, title, raw_hash)]
            source_tier = "OFFICIAL_GOVERNMENT_PRIMARY"

        if listing.get("resource_state") != "DISCOVERED":
            raise ValueError("resource listing must remain DISCOVERED at observation ingress")

        owner = listing.get("owner_actor")
        actor_ids: tuple[str, ...] = ()
        actor_id: str | None = None
        if isinstance(owner, str) and owner.strip():
            actor_id = _source_actor_id(source_id, "owner_as_named", owner.strip())
            actor_ids = (actor_id,)

        record_id = str(listing.get("project_id") or listing.get("monitoring_code") or listing.get("legacy_guid") or url)
        claims: list[SemanticClaim] = [
            SemanticClaim(
                claim_id="listed_resource",
                primitive="RESOURCE",
                concept="PUBLICLY_LISTED_ASSET_OR_RIGHT",
                epistemic_status="OBSERVED",
                evidence_refs=("listing",),
                value={
                    "title": title,
                    "project_id": listing.get("project_id"),
                    "listing_mode": listing.get("listing_mode"),
                    "asking_price_rmb": listing.get("asking_price_rmb"),
                    "asking_price_raw": listing.get("asking_price_raw"),
                    "location": listing.get("location"),
                    "owner_actor_as_named": owner,
                    "publisher_actor_as_named": listing.get("publisher_actor"),
                    "resource_state": "DISCOVERED",
                },
                actor_id=actor_id,
                geography="CN-JS-XZ",
            )
        ]
        underuse_state = listing.get("underuse_evidence_state", "UNKNOWN")
        underuse_excerpt = listing.get("underuse_excerpt")
        if underuse_state == "OBSERVED":
            if not isinstance(underuse_excerpt, str) or not underuse_excerpt.strip():
                raise ValueError("OBSERVED underuse requires explicit evidence excerpt")
            evidence.append(EvidenceRef("underuse", url, underuse_excerpt.strip(), raw_hash))
            claims.append(
                SemanticClaim(
                    claim_id="explicit_underuse_state",
                    primitive="STATE",
                    concept="EXPLICIT_RESOURCE_UNDERUSE_OR_VACANCY",
                    epistemic_status="OBSERVED",
                    evidence_refs=("underuse",),
                    value={"evidence_state": "OBSERVED", "excerpt": underuse_excerpt.strip()},
                    actor_id=actor_id,
                    geography="CN-JS-XZ",
                )
            )
        elif underuse_state != "UNKNOWN":
            raise ValueError(f"unsupported underuse_evidence_state: {underuse_state}")

        if listing.get("relisting_observed") is True:
            listing_round = listing.get("listing_round")
            if not isinstance(listing_round, int) or listing_round < 2:
                raise ValueError("relisting_observed requires explicit listing_round >= 2")
            claims.append(
                SemanticClaim(
                    claim_id="relisting_change",
                    primitive="CHANGE",
                    concept="PUBLIC_LISTING_REPEATED",
                    epistemic_status="OBSERVED",
                    evidence_refs=("listing",),
                    value={"listing_round": listing_round},
                    actor_id=actor_id,
                    geography="CN-JS-XZ",
                )
            )

        result.append(
            ObservationEnvelope(
                observation_id=_stable_id(f"obs:{source_id}:resource", record_id, url),
                source_id=source_id,
                source_record_id=record_id,
                source_locator=url,
                source_origin_geography="CN-JS-XZ",
                relevance_geographies=("CN-JS-XZ",),
                source_tier=source_tier,
                observed_at=retrieved_at,
                retrieved_at=retrieved_at,
                parser_version=PARSER_VERSION,
                raw_payload_hash=raw_hash,
                sampling_boundary="RECENT_XUZHOU_ASSET_LISTINGS_SELECTED_BY_EXISTING_ADAPTER",
                evidence=tuple(evidence),
                claims=tuple(claims),
                actor_ids=actor_ids,
                unknown_fields=("current_availability", "permission", "transactionability"),
            )
        )
    return tuple(result)


GOVERNING_INVARIANTS = (
    "LIVE_ARTIFACT_TO_OBSERVATION_ONLY",
    "DECLARED_PROCUREMENT_BUDGET_NE_PAYMENT",
    "PUBLIC_LISTING_NE_CONTROL",
    "PUBLIC_LISTING_NE_CURRENT_AVAILABILITY",
    "PUBLISHER_NE_OWNER",
    "RELISTING_NE_UNDERUSE",
    "OBSERVED_UNDERUSE_REQUIRES_EXPLICIT_SOURCE_TEXT",
    "NO_PAYER_PROMOTION",
    "NO_OPPORTUNITY_PROMOTION",
    "UNKNOWN_NE_PASS",
)
