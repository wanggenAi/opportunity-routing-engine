"""Versioned registry for auditable capability requirement decompositions.

A registered bundle is a decomposition hypothesis for an opportunity/outcome. It is
not evidence that a payer exists, that a counterparty accepted the requirement, or
that a transaction should occur.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from src.capability_coverage import CapabilityRequirement, RequirementBundle


@dataclass(frozen=True)
class RequirementBundleSpec:
    bundle_id: str
    version: int
    required_capabilities: Sequence[str]
    geography: str
    source_ref: str
    rationale: str
    active: bool = False

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.bundle_id.strip():
            errors.append("missing:bundle_id")
        if self.version < 1:
            errors.append("invalid:version")

        keys: list[str] = []
        if isinstance(self.required_capabilities, (str, bytes)):
            errors.append("invalid:required_capabilities")
        else:
            for key in self.required_capabilities:
                if not isinstance(key, str) or not key.strip():
                    errors.append("missing:required_capabilities")
                    keys = []
                    break
                keys.append(key.strip())
            if not keys and "missing:required_capabilities" not in errors:
                errors.append("missing:required_capabilities")
            if keys and len(keys) != len(set(keys)):
                errors.append("duplicate:required_capabilities")

        if not self.source_ref.strip():
            errors.append("missing:source_ref")
        if not self.rationale.strip():
            errors.append("missing:rationale")
        return errors

    def as_bundle(self) -> RequirementBundle:
        errors = self.validate()
        if errors:
            raise ValueError("invalid requirement bundle spec: " + ",".join(errors))
        return RequirementBundle(
            bundle_id=self.bundle_id.strip(),
            geography=self.geography.strip(),
            required_capabilities=tuple(
                CapabilityRequirement(key.strip()) for key in self.required_capabilities
            ),
        )


_SCHEMA = """
CREATE TABLE IF NOT EXISTS requirement_bundle (
    bundle_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    required_capabilities_json TEXT NOT NULL,
    geography TEXT NOT NULL,
    source_ref TEXT NOT NULL,
    rationale TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (bundle_id, version)
);

CREATE INDEX IF NOT EXISTS idx_requirement_bundle_active
ON requirement_bundle(active, bundle_id, version);
"""


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _version_content(spec: RequirementBundleSpec) -> tuple[object, ...]:
    """Canonical immutable content of a bundle version, excluding active selection."""

    return (
        spec.bundle_id.strip(),
        spec.version,
        tuple(key.strip() for key in spec.required_capabilities),
        spec.geography.strip(),
        spec.source_ref.strip(),
        spec.rationale.strip(),
    )


class SQLiteRequirementBundleRegistry:
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

    def __enter__(self) -> "SQLiteRequirementBundleRegistry":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def register(self, spec: RequirementBundleSpec) -> None:
        errors = spec.validate()
        if errors:
            raise ValueError("invalid requirement bundle spec: " + ",".join(errors))

        existing = self.get(spec.bundle_id, spec.version)
        if existing is not None:
            if _version_content(existing) != _version_content(spec):
                raise ValueError("requirement bundle version already exists with different content")
            if spec.active and not existing.active:
                self.activate(spec.bundle_id.strip(), spec.version)
            return

        with self.connection:
            self.connection.execute(
                """
                INSERT INTO requirement_bundle (
                    bundle_id, version, required_capabilities_json, geography,
                    source_ref, rationale, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    spec.bundle_id.strip(),
                    spec.version,
                    _json([key.strip() for key in spec.required_capabilities]),
                    spec.geography.strip(),
                    spec.source_ref.strip(),
                    spec.rationale.strip(),
                    1 if spec.active else 0,
                ),
            )
            if spec.active:
                self.connection.execute(
                    """
                    UPDATE requirement_bundle SET active = 0
                    WHERE bundle_id = ? AND version != ?
                    """,
                    (spec.bundle_id.strip(), spec.version),
                )

    def get(self, bundle_id: str, version: int) -> RequirementBundleSpec | None:
        row = self.connection.execute(
            "SELECT * FROM requirement_bundle WHERE bundle_id = ? AND version = ?",
            (bundle_id, version),
        ).fetchone()
        if row is None:
            return None
        raw = json.loads(row["required_capabilities_json"])
        if not isinstance(raw, list) or any(not isinstance(item, str) for item in raw):
            raise ValueError("stored requirement capabilities are invalid")
        return RequirementBundleSpec(
            bundle_id=row["bundle_id"],
            version=int(row["version"]),
            required_capabilities=tuple(raw),
            geography=row["geography"],
            source_ref=row["source_ref"],
            rationale=row["rationale"],
            active=bool(row["active"]),
        )

    def versions(self, bundle_id: str) -> tuple[RequirementBundleSpec, ...]:
        rows = self.connection.execute(
            "SELECT version FROM requirement_bundle WHERE bundle_id = ? ORDER BY version",
            (bundle_id,),
        ).fetchall()
        result: list[RequirementBundleSpec] = []
        for row in rows:
            spec = self.get(bundle_id, int(row["version"]))
            if spec is None:
                raise RuntimeError("requirement bundle disappeared during read")
            result.append(spec)
        return tuple(result)

    def activate(self, bundle_id: str, version: int) -> None:
        if self.get(bundle_id, version) is None:
            raise KeyError((bundle_id, version))
        with self.connection:
            self.connection.execute(
                "UPDATE requirement_bundle SET active = 0 WHERE bundle_id = ?",
                (bundle_id,),
            )
            self.connection.execute(
                """
                UPDATE requirement_bundle SET active = 1
                WHERE bundle_id = ? AND version = ?
                """,
                (bundle_id, version),
            )

    def active(self, bundle_id: str) -> RequirementBundleSpec | None:
        row = self.connection.execute(
            """
            SELECT version FROM requirement_bundle
            WHERE bundle_id = ? AND active = 1
            ORDER BY version DESC LIMIT 1
            """,
            (bundle_id,),
        ).fetchone()
        return None if row is None else self.get(bundle_id, int(row["version"]))

    def active_specs(self) -> tuple[RequirementBundleSpec, ...]:
        rows = self.connection.execute(
            """
            SELECT bundle_id, version FROM requirement_bundle
            WHERE active = 1 ORDER BY bundle_id, version
            """
        ).fetchall()
        result: list[RequirementBundleSpec] = []
        for row in rows:
            spec = self.get(row["bundle_id"], int(row["version"]))
            if spec is None:
                raise RuntimeError("active requirement bundle disappeared during read")
            result.append(spec)
        return tuple(result)


GOVERNING_INVARIANTS = (
    "REQUIREMENT_BUNDLE_IS_DECOMPOSITION_NOT_DEMAND_TRUTH",
    "BUNDLE_CHANGE_REQUIRES_NEW_VERSION",
    "ACTIVE_BUNDLE_VERSION_IS_EXPLICIT",
    "ACTIVE_SELECTION_NE_VERSION_CONTENT",
    "BUNDLE_SOURCE_REF_IS_REQUIRED",
    "BUNDLE_RATIONALE_IS_REQUIRED",
    "BUNDLE_NE_PAYER_COMMITMENT",
    "BUNDLE_NE_TRANSACTIONABILITY",
    "UNKNOWN_NE_PASS",
)
