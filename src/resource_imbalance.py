"""Evidence-gated Resource Imbalance Engine.

The engine pairs verified need-side evidence with verified resource-side evidence
without allowing one-sided observations to masquerade as opportunities.

Key invariants:
- paid demand != resource availability;
- resource existence != under-utilisation;
- DISCOVERED != OPTIONED;
- UNKNOWN != PASS;
- a paired hypothesis is not a transaction-ready opportunity;
- ROUTE_TESTABLE means only that a bounded real-world route test is justified.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, Mapping, Sequence


NEED_EVIDENCE_STATES = {"UNKNOWN", "OBSERVED", "PAID", "REPEATED_PAID"}
RESOURCE_STATES = {"HYPOTHETICAL", "DISCOVERED", "OPTIONED", "OWNED"}
UNDERUSE_EVIDENCE_STATES = {"UNKNOWN", "CLAIMED", "OBSERVED", "MEASURED"}
BLOCKER_EVIDENCE_STATES = {"UNKNOWN", "CLAIMED", "OBSERVED", "MEASURED"}

BLOCKER_TYPES = {
    "DEMAND_GAP",
    "CAPABILITY_GAP",
    "PRICE_GAP",
    "TRUST_GAP",
    "INFORMATION_GAP",
    "GEOGRAPHY_GAP",
    "TIME_GAP",
    "COORDINATION_GAP",
    "PAYER_SHIFT",
    "TECHNOLOGY_SHIFT",
}

STATUSES = {
    "NEED_ONLY",
    "RESOURCE_ONLY",
    "PAIR_HYPOTHESIS",
    "ROUTE_TESTABLE",
}

_NEED_RANK = {"UNKNOWN": 0, "OBSERVED": 1, "PAID": 2, "REPEATED_PAID": 3}
_RESOURCE_RANK = {"HYPOTHETICAL": 0, "DISCOVERED": 1, "OPTIONED": 2, "OWNED": 3}
_UNDERUSE_RANK = {"UNKNOWN": 0, "CLAIMED": 1, "OBSERVED": 2, "MEASURED": 3}
_BLOCKER_RANK = {"UNKNOWN": 0, "CLAIMED": 1, "OBSERVED": 2, "MEASURED": 3}


@dataclass(frozen=True)
class NeedSignal:
    signal_id: str
    capability_key: str
    geography: str
    need_actor: str
    payer: str | None
    evidence_state: str
    paid_event_count: int = 0
    total_observed_spend_rmb: str | None = None
    observation_period: str | None = None
    source_ids: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class ResourceSignal:
    signal_id: str
    capability_key: str
    geography: str
    provider_actor: str
    resource_state: str
    underuse_evidence_state: str
    available_units: str | None = None
    observation_period: str | None = None
    source_ids: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class BlockerSignal:
    signal_id: str
    capability_key: str
    geography: str
    blocker_type: str
    evidence_state: str
    description: str
    source_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ImbalanceRecord:
    record_id: str
    capability_key: str
    geography: str
    status: str
    need_signal_id: str | None
    resource_signal_id: str | None
    blocker_signal_id: str | None
    payer: str | None
    need_evidence_state: str | None
    resource_state: str | None
    underuse_evidence_state: str | None
    blocker_type: str | None
    blocker_evidence_state: str | None
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reasons"] = list(self.reasons)
        return data


def _required_text(name: str, value: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{name} must not be empty")
    return text


def _validate_decimal(name: str, value: str | None) -> None:
    if value is None or str(value).strip() == "":
        return
    try:
        parsed = Decimal(str(value).replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"{name} must be numeric when supplied") from exc
    if parsed < 0:
        raise ValueError(f"{name} must not be negative")


def validate_need(signal: NeedSignal) -> None:
    _required_text("signal_id", signal.signal_id)
    _required_text("capability_key", signal.capability_key)
    _required_text("geography", signal.geography)
    _required_text("need_actor", signal.need_actor)
    if signal.payer is not None and not str(signal.payer).strip():
        raise ValueError("payer must be null or non-empty")
    if signal.evidence_state not in NEED_EVIDENCE_STATES:
        raise ValueError(f"invalid need evidence_state: {signal.evidence_state}")
    if not isinstance(signal.paid_event_count, int) or signal.paid_event_count < 0:
        raise ValueError("paid_event_count must be a non-negative integer")
    if signal.evidence_state == "PAID" and signal.paid_event_count < 1:
        raise ValueError("PAID need evidence requires at least one paid event")
    if signal.evidence_state == "REPEATED_PAID" and signal.paid_event_count < 2:
        raise ValueError("REPEATED_PAID need evidence requires at least two paid events")
    if signal.evidence_state in {"PAID", "REPEATED_PAID"} and not signal.payer:
        raise ValueError("paid need evidence requires an identified payer")
    if signal.evidence_state != "UNKNOWN" and not signal.source_ids:
        raise ValueError("observed need evidence requires source_ids")
    _validate_decimal("total_observed_spend_rmb", signal.total_observed_spend_rmb)


def validate_resource(signal: ResourceSignal) -> None:
    _required_text("signal_id", signal.signal_id)
    _required_text("capability_key", signal.capability_key)
    _required_text("geography", signal.geography)
    _required_text("provider_actor", signal.provider_actor)
    if signal.resource_state not in RESOURCE_STATES:
        raise ValueError(f"invalid resource_state: {signal.resource_state}")
    if signal.underuse_evidence_state not in UNDERUSE_EVIDENCE_STATES:
        raise ValueError(
            f"invalid underuse_evidence_state: {signal.underuse_evidence_state}"
        )
    if signal.resource_state != "HYPOTHETICAL" and not signal.source_ids:
        raise ValueError("verified resource state requires source_ids")
    if signal.underuse_evidence_state in {"OBSERVED", "MEASURED"} and not signal.source_ids:
        raise ValueError("observed underuse requires source_ids")


def validate_blocker(signal: BlockerSignal) -> None:
    _required_text("signal_id", signal.signal_id)
    _required_text("capability_key", signal.capability_key)
    _required_text("geography", signal.geography)
    _required_text("description", signal.description)
    if signal.blocker_type not in BLOCKER_TYPES:
        raise ValueError(f"invalid blocker_type: {signal.blocker_type}")
    if signal.evidence_state not in BLOCKER_EVIDENCE_STATES:
        raise ValueError(f"invalid blocker evidence_state: {signal.evidence_state}")
    if signal.evidence_state in {"OBSERVED", "MEASURED"} and not signal.source_ids:
        raise ValueError("observed blocker evidence requires source_ids")


def _pair_key(capability_key: str, geography: str) -> tuple[str, str]:
    return (capability_key.strip().lower(), geography.strip().lower())


def _best_blocker(
    blockers: Sequence[BlockerSignal], capability_key: str, geography: str
) -> BlockerSignal | None:
    compatible = [
        blocker
        for blocker in blockers
        if _pair_key(blocker.capability_key, blocker.geography)
        == _pair_key(capability_key, geography)
    ]
    if not compatible:
        return None
    return max(compatible, key=lambda item: _BLOCKER_RANK[item.evidence_state])


def evaluate_pair(
    need: NeedSignal,
    resource: ResourceSignal,
    blocker: BlockerSignal | None = None,
    *,
    record_id: str | None = None,
) -> ImbalanceRecord:
    """Classify one exact capability/geography pair.

    V1 deliberately requires exact capability and geography identity. Cross-region
    routing and ontology expansion must be explicit later rather than inferred here.
    """

    validate_need(need)
    validate_resource(resource)
    if blocker is not None:
        validate_blocker(blocker)

    if _pair_key(need.capability_key, need.geography) != _pair_key(
        resource.capability_key, resource.geography
    ):
        raise ValueError("need/resource capability and geography must match exactly")
    if blocker is not None and _pair_key(blocker.capability_key, blocker.geography) != _pair_key(
        need.capability_key, need.geography
    ):
        raise ValueError("blocker must match the same capability and geography")

    reasons: list[str] = []
    route_testable = True

    if _NEED_RANK[need.evidence_state] < _NEED_RANK["PAID"]:
        route_testable = False
        reasons.append("need side lacks direct paid evidence")
    if not need.payer:
        route_testable = False
        reasons.append("payer is not identified")
    if _RESOURCE_RANK[resource.resource_state] < _RESOURCE_RANK["DISCOVERED"]:
        route_testable = False
        reasons.append("resource remains hypothetical")
    if _UNDERUSE_RANK[resource.underuse_evidence_state] < _UNDERUSE_RANK["OBSERVED"]:
        route_testable = False
        reasons.append("resource underuse is not observed")
    if blocker is None:
        route_testable = False
        reasons.append("transaction blocker is not identified")
    elif _BLOCKER_RANK[blocker.evidence_state] < _BLOCKER_RANK["OBSERVED"]:
        route_testable = False
        reasons.append("transaction blocker is not observed")

    if route_testable:
        status = "ROUTE_TESTABLE"
        reasons.append(
            "paid need + identified payer + discovered resource + observed underuse + observed blocker"
        )
    else:
        status = "PAIR_HYPOTHESIS"

    return ImbalanceRecord(
        record_id=record_id or f"PAIR::{need.signal_id}::{resource.signal_id}",
        capability_key=need.capability_key,
        geography=need.geography,
        status=status,
        need_signal_id=need.signal_id,
        resource_signal_id=resource.signal_id,
        blocker_signal_id=blocker.signal_id if blocker else None,
        payer=need.payer,
        need_evidence_state=need.evidence_state,
        resource_state=resource.resource_state,
        underuse_evidence_state=resource.underuse_evidence_state,
        blocker_type=blocker.blocker_type if blocker else None,
        blocker_evidence_state=blocker.evidence_state if blocker else None,
        reasons=tuple(reasons),
    )


def scan_imbalances(
    needs: Iterable[NeedSignal],
    resources: Iterable[ResourceSignal],
    blockers: Iterable[BlockerSignal] = (),
    *,
    max_pairs_per_need: int = 5,
) -> list[ImbalanceRecord]:
    """Create a bounded imbalance ledger without manufacturing missing sides.

    `max_pairs_per_need` limits emitted pair records only. A resource that shares an
    exact key with any need is never relabelled RESOURCE_ONLY merely because it fell
    outside that output bound.
    """

    if not isinstance(max_pairs_per_need, int) or max_pairs_per_need <= 0:
        raise ValueError("max_pairs_per_need must be a positive integer")

    need_list = list(needs)
    resource_list = list(resources)
    blocker_list = list(blockers)
    for need in need_list:
        validate_need(need)
    for resource in resource_list:
        validate_resource(resource)
    for blocker in blocker_list:
        validate_blocker(blocker)

    resources_by_key: dict[tuple[str, str], list[ResourceSignal]] = {}
    for resource in resource_list:
        resources_by_key.setdefault(
            _pair_key(resource.capability_key, resource.geography), []
        ).append(resource)

    need_keys = {
        _pair_key(need.capability_key, need.geography)
        for need in need_list
    }
    result: list[ImbalanceRecord] = []

    for need in need_list:
        key = _pair_key(need.capability_key, need.geography)
        all_matches = resources_by_key.get(key, [])
        if not all_matches:
            result.append(
                ImbalanceRecord(
                    record_id=f"NEED::{need.signal_id}",
                    capability_key=need.capability_key,
                    geography=need.geography,
                    status="NEED_ONLY",
                    need_signal_id=need.signal_id,
                    resource_signal_id=None,
                    blocker_signal_id=None,
                    payer=need.payer,
                    need_evidence_state=need.evidence_state,
                    resource_state=None,
                    underuse_evidence_state=None,
                    blocker_type=None,
                    blocker_evidence_state=None,
                    reasons=(
                        "verified need exists but no matching resource signal is present",
                    ),
                )
            )
            continue

        blocker = _best_blocker(blocker_list, need.capability_key, need.geography)
        for resource in all_matches[:max_pairs_per_need]:
            result.append(evaluate_pair(need, resource, blocker))

    for resource in resource_list:
        key = _pair_key(resource.capability_key, resource.geography)
        if key in need_keys:
            continue
        result.append(
            ImbalanceRecord(
                record_id=f"RESOURCE::{resource.signal_id}",
                capability_key=resource.capability_key,
                geography=resource.geography,
                status="RESOURCE_ONLY",
                need_signal_id=None,
                resource_signal_id=resource.signal_id,
                blocker_signal_id=None,
                payer=None,
                need_evidence_state=None,
                resource_state=resource.resource_state,
                underuse_evidence_state=resource.underuse_evidence_state,
                blocker_type=None,
                blocker_evidence_state=None,
                reasons=(
                    "verified resource exists but no matching need signal is present",
                ),
            )
        )

    return result


def procurement_event_to_need(
    event: Mapping[str, Any],
    *,
    signal_id: str,
    capability_key: str,
    need_actor: str,
    payer: str,
    geography: str = "Xuzhou",
) -> NeedSignal:
    """Normalize explicit procurement settlement evidence into a PAID need.

    This compatibility helper is intentionally strict. A tender notice, published
    budget, award/result, or signed contract is insufficient. Callers must provide
    an explicit ``settlement_proven=True`` flag, a settled amount, an identified
    payer, and a source URL. Exact-project lifecycle code should normally be used
    instead so project identity and provenance stay auditable.
    """

    if event.get("settlement_proven") is not True:
        raise ValueError(
            "procurement PAID normalization requires explicit settlement_proven evidence"
        )
    settled_amount = event.get("settled_amount_rmb")
    if settled_amount in (None, ""):
        raise ValueError("procurement PAID normalization requires settled_amount_rmb")
    if not str(payer or "").strip():
        raise ValueError("procurement PAID normalization requires an identified payer")

    source_id = str(event.get("source_id") or "XZ_GGZY").strip()
    source_url = str(event.get("url") or "").strip()
    if not source_url:
        raise ValueError("procurement PAID normalization requires a source URL")
    source_refs = tuple(item for item in (source_id, source_url) if item)
    need = NeedSignal(
        signal_id=signal_id,
        capability_key=capability_key,
        geography=geography,
        need_actor=need_actor,
        payer=payer,
        evidence_state="PAID",
        paid_event_count=1,
        total_observed_spend_rmb=str(settled_amount),
        observation_period=str(
            event.get("settlement_date") or event.get("publication_date") or ""
        )
        or None,
        source_ids=source_refs,
        notes=(
            "normalized from explicit procurement settlement evidence; "
            "no supply-side claim implied"
        ),
    )
    validate_need(need)
    return need
