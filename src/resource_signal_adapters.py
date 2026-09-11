"""Truth-preserving transformations from normalized source events to resource signals."""

from __future__ import annotations

from typing import Any, Mapping

from src.resource_imbalance import ResourceSignal, validate_resource


def public_asset_listing_to_resource(
    listing: Mapping[str, Any],
    *,
    signal_id: str,
    capability_key: str,
    provider_actor: str | None = None,
    geography: str = "Xuzhou",
) -> ResourceSignal:
    """Convert one normalized public asset listing into ResourceSignal evidence.

    The caller must supply `capability_key`; the transformer deliberately refuses to
    infer CapabilityUnit identity from free-form asset titles.

    The source adapter owns only these facts:
    - public listing => DISCOVERED resource state;
    - explicit idle/vacant source language => OBSERVED underuse;
    - otherwise underuse stays UNKNOWN.

    Relisting/price information is retained in notes but cannot silently manufacture
    a blocker type or upgrade underuse.
    """

    source_id = str(listing.get("source_id") or "XZ_GGZY").strip()
    source_url = str(listing.get("url") or "").strip()
    resource_state = str(listing.get("resource_state") or "").strip()
    if resource_state != "DISCOVERED":
        raise ValueError(
            "public asset listing transformer only accepts resource_state=DISCOVERED"
        )

    underuse_state = str(
        listing.get("underuse_evidence_state") or "UNKNOWN"
    ).strip()
    if underuse_state not in {"UNKNOWN", "OBSERVED"}:
        raise ValueError(
            "public asset listing underuse must be UNKNOWN or OBSERVED"
        )

    provider = (provider_actor or str(listing.get("owner_actor") or "")).strip()
    if not provider:
        raise ValueError("provider_actor or listing owner_actor is required")

    notes_parts = [
        "normalized from public property-rights listing",
        f"listing_mode={listing.get('listing_mode') or 'UNKNOWN'}",
    ]
    if listing.get("listing_round"):
        notes_parts.append(f"listing_round={listing['listing_round']}")
    if listing.get("relisting_observed"):
        notes_parts.append("relisting_observed=true")
    if listing.get("asking_price_rmb") not in (None, ""):
        notes_parts.append(f"asking_price_rmb={listing['asking_price_rmb']}")
    if listing.get("underuse_excerpt"):
        notes_parts.append(f"underuse_excerpt={listing['underuse_excerpt']}")

    source_ids = tuple(item for item in (source_id, source_url) if item)
    signal = ResourceSignal(
        signal_id=signal_id,
        capability_key=capability_key,
        geography=geography,
        provider_actor=provider,
        resource_state="DISCOVERED",
        underuse_evidence_state=underuse_state,
        available_units=None,
        observation_period=str(listing.get("publication_date") or "") or None,
        source_ids=source_ids,
        notes="; ".join(notes_parts),
    )
    validate_resource(signal)
    return signal
