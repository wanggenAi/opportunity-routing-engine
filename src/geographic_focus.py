from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FocusPolicy:
    primary_market: str
    execution_geographies: tuple[str, ...]
    global_observation_enabled: bool = True
    cross_border_mode: str = "EXCEPTION_ONLY"

    def __post_init__(self) -> None:
        if not self.primary_market.strip():
            raise ValueError("primary_market is required")
        if not self.execution_geographies:
            raise ValueError("execution_geographies are required")
        if self.cross_border_mode not in {"EXCEPTION_ONLY", "DISABLED"}:
            raise ValueError("unsupported cross_border_mode")


def china_focus_policy() -> FocusPolicy:
    return FocusPolicy(
        primary_market="CN",
        execution_geographies=("CN", "CN-JS", "CN-JS-XZ"),
        global_observation_enabled=True,
        cross_border_mode="EXCEPTION_ONLY",
    )


def classify_signal_focus(signal: dict, policy: FocusPolicy | None = None) -> dict:
    """Classify a signal by research relevance without confusing source geography
    with target-market priority.

    Foreign/global information may inform China research, but it cannot become a
    domestic fact or an execution candidate merely because it is salient abroad.
    Cross-border opportunities remain exceptional and require explicit evidence.
    """

    policy = policy or china_focus_policy()
    signal_id = str(signal.get("signal_id") or "").strip()
    origin = str(signal.get("origin_geography") or "").strip()
    evidence_refs = tuple(signal.get("evidence_refs") or ())
    if not signal_id:
        raise ValueError("signal_id is required")
    if not origin:
        raise ValueError("origin_geography is required")
    if not evidence_refs:
        raise ValueError("evidence_refs are required")

    domestic_geographies = set(policy.execution_geographies)
    if origin in domestic_geographies or origin.startswith(f"{policy.primary_market}-"):
        lane = "DOMESTIC_PRIMARY"
        action = "ANALYZE_WITH_DOMESTIC_BEHAVIOR_AND_MONEY"
    elif not policy.global_observation_enabled:
        lane = "OUT_OF_SCOPE"
        action = "IGNORE_FOR_PRIMARY_RESEARCH"
    elif not signal.get("china_relevance_evidence"):
        lane = "GLOBAL_UNBOUND"
        action = "HOLD_UNTIL_CHINA_RELATION_IS_EVIDENCED"
    elif signal.get("domestic_corroboration_evidence"):
        lane = "GLOBAL_AUXILIARY_CORROBORATED"
        action = "USE_AS_AUXILIARY_INPUT_TO_DOMESTIC_HYPOTHESIS"
    else:
        lane = "GLOBAL_AUXILIARY"
        action = "GENERATE_TRANSFER_HYPOTHESIS_ONLY"

    cross_border_exception = False
    if (
        policy.cross_border_mode == "EXCEPTION_ONLY"
        and origin not in domestic_geographies
        and signal.get("cross_border_direct_transaction_evidence")
        and signal.get("domestic_execution_evidence")
        and signal.get("china_relevance_evidence")
    ):
        cross_border_exception = True

    return {
        "signal_id": signal_id,
        "lane": lane,
        "next_action": action,
        "primary_market": policy.primary_market,
        "execution_geographies": list(policy.execution_geographies),
        "cross_border_mode": policy.cross_border_mode,
        "cross_border_exception_candidate": cross_border_exception,
        "truth_boundaries": [
            "GLOBAL_SALIENCE_IS_NOT_DOMESTIC_PREVALENCE",
            "FOREIGN_TREND_IS_NOT_CHINA_DEMAND",
            "TRANSFER_HYPOTHESIS_REQUIRES_DOMESTIC_CORROBORATION",
            "CROSS_BORDER_IS_NOT_PRIMARY_STRATEGY",
        ],
    }
