"""Map Xuzhou official public-asset evidence into neutral live signals.

This adapter is intentionally conservative. It carries explicit listing facts into
``SignalObservation`` and marks the resource as ADVERTISED, while leaving operator
permission/control UNKNOWN. It does not manufacture low-level capabilities.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Mapping, Sequence

from src.live_resource_signals import (
    AvailabilityState,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.resource_underuse_adapters import PublicAssetListing


def _observation_time(listing: PublicAssetListing) -> datetime:
    raw = listing.provenance.get("fetched_at_utc")
    if isinstance(raw, str) and raw.strip():
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if value.tzinfo is not None:
            return value
    return datetime.now(timezone.utc)


def _fact(key: str, value: object, evidence_text: str) -> ObservedFact:
    return ObservedFact(key=key, value=value, evidence_text=evidence_text)


def signal_from_public_asset(listing: PublicAssetListing) -> SignalObservation:
    """Convert one parsed official listing without adding unsupported capabilities."""

    if not listing.owner_actor or not listing.owner_actor.strip():
        raise ValueError("owner_actor is required for actor-linked live signal")

    stable_id = (listing.project_id or listing.url).strip()
    if not stable_id:
        raise ValueError("project_id or url is required for stable signal identity")

    facts: list[ObservedFact] = [
        _fact("resource.publicly_listed", True, listing.title),
        _fact("resource.listing_mode", listing.listing_mode, listing.title),
        _fact("resource.owner_actor", listing.owner_actor.strip(), listing.owner_actor.strip()),
        _fact("resource.relisting_observed", listing.relisting_observed, listing.title),
        _fact(
            "resource.underuse_evidence_state",
            listing.underuse_evidence_state,
            listing.underuse_excerpt or "source parser found no explicit idle/vacant phrase",
        ),
    ]

    optional = (
        ("resource.project_id", listing.project_id, listing.project_id),
        ("resource.publication_date", listing.publication_date, listing.publication_date),
        ("resource.listing_round", listing.listing_round, str(listing.listing_round) if listing.listing_round is not None else None),
        ("resource.asking_price_rmb", listing.asking_price_rmb, listing.asking_price_raw or listing.asking_price_rmb),
        ("resource.location", listing.location, listing.location),
        ("resource.listing_start", listing.listing_start, listing.listing_start),
        ("resource.listing_end", listing.listing_end, listing.listing_end),
    )
    for key, value, evidence in optional:
        if value is not None and evidence is not None and str(evidence).strip():
            facts.append(_fact(key, value, str(evidence).strip()))

    if listing.underuse_evidence_state == "OBSERVED" and listing.underuse_excerpt:
        facts.append(_fact("resource.explicit_underuse_observed", True, listing.underuse_excerpt))

    raw_parts = [listing.title]
    if listing.underuse_excerpt:
        raw_parts.append(listing.underuse_excerpt)
    if listing.asking_price_raw:
        raw_parts.append(listing.asking_price_raw)

    return SignalObservation(
        signal_id=stable_id,
        source_id="XZ_GGZY_PUBLIC_ASSET",
        observed_at=_observation_time(listing),
        actor_ref=listing.owner_actor.strip(),
        geography="Xuzhou",
        raw_text=" | ".join(raw_parts),
        source_url=listing.url,
        facts=tuple(facts),
        explicit_capabilities=(),
        availability=AvailabilityState.ADVERTISED,
        permission=PermissionState.UNKNOWN,
    )


def signals_from_collected_payload(payload: Mapping[str, object]) -> tuple[SignalObservation, ...]:
    """Convert ``XuzhouPublicAssetAdapter.collect_recent`` output into live signals."""

    raw = payload.get("listings", [])
    if not isinstance(raw, list):
        raise ValueError("payload listings must be a list")

    signals: list[SignalObservation] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("listing record must be an object")
        listing = PublicAssetListing(**dict(item))
        signals.append(signal_from_public_asset(listing))
    return tuple(signals)


GOVERNING_INVARIANTS = (
    "OFFICIAL_LISTING_FACT_NE_LOW_LEVEL_CAPABILITY",
    "PUBLICLY_ADVERTISED_RESOURCE_NE_OPERATOR_CONTROL",
    "UNDERUSE_UNKNOWN_NE_UNDERUSE_OBSERVED",
    "RELISTING_NE_UNDERUSE",
    "SOURCE_ADAPTER_IS_OBSERVER_NOT_STRATEGY",
    "UNKNOWN_NE_PASS",
)
