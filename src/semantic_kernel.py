from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


# Stable semantic primitives. These are not a market taxonomy.
SEMANTIC_PRIMITIVES = frozenset(
    {
        "ACTOR",
        "STATE",
        "CHANGE",
        "RESOURCE",
        "CAPABILITY",
        "PERCEPTION",
        "MOTIVE",
        "BEHAVIOR",
        "FLOW",
        "CONSTRAINT",
        "FRICTION",
        "OUTCOME",
        "EVIDENCE",
        "TIME",
        "SPACE",
    }
)

EPISTEMIC_STATUSES = frozenset({"OBSERVED", "REPORTED", "INFERRED"})


@dataclass(frozen=True)
class SemanticObservation:
    observation_id: str
    primitive: str
    concept: str
    source_id: str
    observed_at: str
    evidence_refs: tuple[str, ...]
    actor_id: str | None = None
    geography: str | None = None
    epistemic_status: str = "OBSERVED"

    def __post_init__(self) -> None:
        if not self.observation_id.strip():
            raise ValueError("observation_id is required")
        if self.primitive not in SEMANTIC_PRIMITIVES:
            raise ValueError(f"unknown semantic primitive: {self.primitive}")
        if not self.concept.strip():
            raise ValueError("concept is required")
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.observed_at.strip():
            raise ValueError("observed_at is required")
        if not self.evidence_refs:
            raise ValueError("at least one evidence ref is required")
        if self.epistemic_status not in EPISTEMIC_STATUSES:
            raise ValueError(f"unsupported epistemic_status: {self.epistemic_status}")


def validate_open_concept_namespace(
    observations: Iterable[SemanticObservation],
) -> tuple[SemanticObservation, ...]:
    """Validate shape without imposing a closed domain taxonomy.

    ``concept`` is intentionally open-ended. New social behaviors, resources,
    motives, frictions and capabilities must be representable without adding an
    enum or changing core code. Canonical promotion belongs to later evidence
    gates.
    """

    result = tuple(observations)
    seen: set[str] = set()
    for item in result:
        if item.observation_id in seen:
            raise ValueError(f"duplicate observation_id: {item.observation_id}")
        seen.add(item.observation_id)
    return result
