"""Auditable registry for deterministic capability inference rules.

Rules are data, not hidden strategy. The registry validates rule structure, preserves an
open-ended capability namespace and evaluates signals only through the same
truth-preserving inference path used by the live resource model.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from src.live_resource_signals import (
    CapabilityClaim,
    CapabilityInferenceRule,
    FactCondition,
    SignalObservation,
    extract_capability_claims,
)


SCHEMA_VERSION = 1


def validate_rule(rule: CapabilityInferenceRule) -> list[str]:
    errors: list[str] = []
    if not rule.rule_id.strip():
        errors.append("missing:rule_id")
    if not rule.capability_key.strip():
        errors.append("missing:capability_key")
    if not rule.rationale.strip():
        errors.append("missing:rationale")
    if not rule.conditions:
        errors.append("missing:conditions")
    elif any(not condition.key.strip() for condition in rule.conditions):
        errors.append("missing:condition_key")
    return errors


def rule_to_record(rule: CapabilityInferenceRule) -> dict[str, object]:
    return {
        "rule_id": rule.rule_id,
        "capability_key": rule.capability_key,
        "rationale": rule.rationale,
        "conditions": [
            {"key": condition.key, "expected_value": condition.expected_value}
            for condition in rule.conditions
        ],
    }


def rule_from_record(record: Mapping[str, object]) -> CapabilityInferenceRule:
    rule_id = record.get("rule_id")
    capability_key = record.get("capability_key")
    rationale = record.get("rationale")
    conditions_raw = record.get("conditions")

    if not isinstance(rule_id, str):
        rule_id = ""
    if not isinstance(capability_key, str):
        capability_key = ""
    if not isinstance(rationale, str):
        rationale = ""
    if not isinstance(conditions_raw, Sequence) or isinstance(conditions_raw, (str, bytes)):
        conditions_raw = ()

    conditions: list[FactCondition] = []
    for item in conditions_raw:
        if not isinstance(item, Mapping):
            raise ValueError("rule condition must be an object")
        key = item.get("key")
        if not isinstance(key, str):
            key = ""
        conditions.append(FactCondition(key=key, expected_value=item.get("expected_value", True)))

    rule = CapabilityInferenceRule(
        rule_id=rule_id,
        conditions=tuple(conditions),
        capability_key=capability_key,
        rationale=rationale,
    )
    errors = validate_rule(rule)
    if errors:
        raise ValueError("invalid capability rule: " + ",".join(errors))
    return rule


@dataclass(frozen=True)
class CapabilityRuleRegistry:
    rules: Sequence[CapabilityInferenceRule]

    def __post_init__(self) -> None:
        ids: set[str] = set()
        for rule in self.rules:
            errors = validate_rule(rule)
            if errors:
                raise ValueError("invalid capability rule: " + ",".join(errors))
            key = rule.rule_id.strip()
            if key in ids:
                raise ValueError(f"duplicate capability rule_id: {key}")
            ids.add(key)

    def infer(self, signal: SignalObservation) -> list[CapabilityClaim]:
        return extract_capability_claims(signal, tuple(self.rules))

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": SCHEMA_VERSION,
            "rules": [rule_to_record(rule) for rule in self.rules],
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "CapabilityRuleRegistry":
        if payload.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("unsupported capability rule schema_version")
        raw_rules = payload.get("rules")
        if not isinstance(raw_rules, list):
            raise ValueError("capability rules must be an array")
        return cls(tuple(rule_from_record(item) for item in raw_rules if isinstance(item, Mapping)))

    @classmethod
    def load_json(cls, path: str | Path) -> "CapabilityRuleRegistry":
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read capability rule registry: {path}") from exc
        if not isinstance(payload, Mapping):
            raise ValueError("capability rule registry root must be an object")
        return cls.from_mapping(payload)


GOVERNING_INVARIANTS = (
    "RULE_REGISTRY_IS_AUDITABLE_DATA",
    "CAPABILITY_NAMESPACE_IS_OPEN_ENDED",
    "RULE_MATCH_NE_CAPABILITY_CONFIRMATION",
    "MODEL_SUGGESTION_NE_CANONICAL_RULE",
    "RULE_CHANGE_REQUIRES_REVIEWABLE_DIFF",
    "UNKNOWN_NE_PASS",
)
