"""Versioned, auditable registry for capability inference rules.

Rules convert normalized observed facts into INFERRED capability claims only. The
registry is append-versioned: a changed rule receives a new version rather than
silently rewriting the historical rule that produced earlier hypotheses.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from src.live_resource_signals import CapabilityInferenceRule, FactCondition


@dataclass(frozen=True)
class CapabilityRuleSpec:
    rule_id: str
    version: int
    conditions: Sequence[FactCondition]
    capability_key: str
    rationale: str
    active: bool = False

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.rule_id.strip(): errors.append("missing:rule_id")
        if self.version < 1: errors.append("invalid:version")
        if not self.conditions: errors.append("missing:conditions")
        if any(not condition.key.strip() for condition in self.conditions): errors.append("missing:condition_key")
        if not self.capability_key.strip(): errors.append("missing:capability_key")
        if not self.rationale.strip(): errors.append("missing:rationale")
        return errors

    def as_inference_rule(self) -> CapabilityInferenceRule:
        errors = self.validate()
        if errors:
            raise ValueError("invalid rule: " + ",".join(errors))
        return CapabilityInferenceRule(
            rule_id=f"{self.rule_id.strip()}@v{self.version}",
            conditions=tuple(self.conditions),
            capability_key=self.capability_key.strip(),
            rationale=self.rationale.strip(),
        )


_SCHEMA = """
CREATE TABLE IF NOT EXISTS capability_rule (
    rule_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    capability_key TEXT NOT NULL,
    conditions_json TEXT NOT NULL,
    rationale TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (rule_id, version)
);
CREATE INDEX IF NOT EXISTS idx_capability_rule_active
ON capability_rule(active, rule_id, version);
"""


def _condition_payload(condition: FactCondition) -> dict[str, object]:
    return {"key": condition.key, "expected_value": condition.expected_value}


def _conditions_json(conditions: Sequence[FactCondition]) -> str:
    return json.dumps(
        [_condition_payload(condition) for condition in conditions],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _conditions_from_json(raw: str) -> tuple[FactCondition, ...]:
    payload = json.loads(raw)
    if not isinstance(payload, list):
        raise ValueError("stored conditions must be a list")
    result: list[FactCondition] = []
    for item in payload:
        if not isinstance(item, dict) or not isinstance(item.get("key"), str):
            raise ValueError("invalid stored condition")
        result.append(FactCondition(item["key"], item.get("expected_value", True)))
    return tuple(result)


class SQLiteCapabilityRuleRegistry:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if self.path != Path(":memory:"):
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path))
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(_SCHEMA)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteCapabilityRuleRegistry":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def register(self, spec: CapabilityRuleSpec) -> None:
        errors = spec.validate()
        if errors:
            raise ValueError("invalid rule: " + ",".join(errors))

        existing = self.get(spec.rule_id, spec.version)
        if existing is not None:
            if existing != spec:
                raise ValueError("rule version already exists with different content")
            return

        with self.connection:
            self.connection.execute(
                """
                INSERT INTO capability_rule (
                    rule_id, version, capability_key, conditions_json, rationale, active
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    spec.rule_id.strip(),
                    spec.version,
                    spec.capability_key.strip(),
                    _conditions_json(spec.conditions),
                    spec.rationale.strip(),
                    1 if spec.active else 0,
                ),
            )
            if spec.active:
                self.connection.execute(
                    """
                    UPDATE capability_rule SET active = 0
                    WHERE rule_id = ? AND version != ?
                    """,
                    (spec.rule_id.strip(), spec.version),
                )

    def get(self, rule_id: str, version: int) -> CapabilityRuleSpec | None:
        row = self.connection.execute(
            "SELECT * FROM capability_rule WHERE rule_id = ? AND version = ?",
            (rule_id, version),
        ).fetchone()
        if row is None:
            return None
        return CapabilityRuleSpec(
            rule_id=row["rule_id"],
            version=row["version"],
            conditions=_conditions_from_json(row["conditions_json"]),
            capability_key=row["capability_key"],
            rationale=row["rationale"],
            active=bool(row["active"]),
        )

    def activate(self, rule_id: str, version: int) -> None:
        if self.get(rule_id, version) is None:
            raise KeyError((rule_id, version))
        with self.connection:
            self.connection.execute("UPDATE capability_rule SET active = 0 WHERE rule_id = ?", (rule_id,))
            self.connection.execute(
                "UPDATE capability_rule SET active = 1 WHERE rule_id = ? AND version = ?",
                (rule_id, version),
            )

    def deactivate(self, rule_id: str) -> None:
        with self.connection:
            self.connection.execute("UPDATE capability_rule SET active = 0 WHERE rule_id = ?", (rule_id,))

    def versions(self, rule_id: str) -> tuple[CapabilityRuleSpec, ...]:
        rows = self.connection.execute(
            "SELECT version FROM capability_rule WHERE rule_id = ? ORDER BY version",
            (rule_id,),
        ).fetchall()
        return tuple(self.get(rule_id, row["version"]) for row in rows)

    def active_specs(self) -> tuple[CapabilityRuleSpec, ...]:
        rows = self.connection.execute(
            "SELECT rule_id, version FROM capability_rule WHERE active = 1 ORDER BY rule_id, version"
        ).fetchall()
        return tuple(self.get(row["rule_id"], row["version"]) for row in rows)

    def active_rules(self) -> tuple[CapabilityInferenceRule, ...]:
        return tuple(spec.as_inference_rule() for spec in self.active_specs())


GOVERNING_INVARIANTS = (
    "RULE_CHANGE_REQUIRES_NEW_VERSION",
    "ACTIVE_RULE_IS_EXPLICITLY_SELECTED",
    "RULE_OUTPUT_IS_INFERRED_NOT_CONFIRMED",
    "MODEL_SUGGESTED_RULE_NE_ACTIVE_RULE",
    "HISTORICAL_RULE_VERSION_MUST_REMAIN_AUDITABLE",
    "UNKNOWN_NE_PASS",
)
