import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import SQLiteCapabilityRuleRegistry
from src.capability_verification_store import (
    CapabilityVerificationEvent,
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.composition_run_store import SQLiteCompositionRunStore
from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_store import SQLiteSignalLedgerStore
from src.requirement_bundle_registry import RequirementBundleSpec
from src.resource_composition import CompositionState


NOW = datetime(2026, 9, 13, 14, 0, tzinfo=timezone.utc)


class VerifiedCompositionRunTests(unittest.TestCase):
    def _signal(self, *, source_id, signal_id, actor_ref, capability_key):
        return SignalObservation(
            signal_id=signal_id,
            source_id=source_id,
            observed_at=NOW,
            actor_ref=actor_ref,
            geography="Xuzhou",
            raw_text=f"offers {capability_key}",
            source_url=f"https://example.com/{source_id}/{signal_id}",
            facts=(ObservedFact(f"fact.{capability_key}", True, f"observed {capability_key}"),),
            explicit_capabilities=(
                ExplicitCapability(capability_key, f"explicit {capability_key}"),
            ),
            availability=AvailabilityState.ADVERTISED,
            permission=PermissionState.UNKNOWN,
        )

    def _bundle(self):
        return RequirementBundleSpec(
            bundle_id="verified-bundle",
            version=1,
            required_capabilities=("cap.a", "cap.b"),
            geography="Xuzhou",
            source_ref="opportunity:verified-test",
            rationale="two-capability verification test",
            active=True,
        )

    def _verification(
        self,
        *,
        verification_id,
        actor_ref,
        capability_key,
        related_signal_ref,
        verdict=VerificationVerdict.CONFIRMED,
        verified_at=NOW + timedelta(hours=1),
        availability=AvailabilityState.CONFIRMED,
        permission=PermissionState.ALLOWED,
    ):
        return CapabilityVerificationEvent(
            verification_id=verification_id,
            actor_ref=actor_ref,
            capability_key=capability_key,
            verdict=verdict,
            verified_at=verified_at,
            evidence_ref=f"field-check:{verification_id}",
            evidence_note=f"reviewed field verification {verification_id}",
            geography="Xuzhou",
            availability=availability,
            permission=permission,
            related_signal_refs=(related_signal_ref,),
        )

    def _materialize(self, tmp):
        signal_store = SQLiteSignalLedgerStore(Path(tmp) / "signals.db")
        rule_store = SQLiteCapabilityRuleRegistry(Path(tmp) / "rules.db")
        graph_store = SQLiteCapabilityGraphStore(Path(tmp) / "graph.db")
        signal_store.ingest(
            self._signal(
                source_id="sensor-a",
                signal_id="item-1",
                actor_ref="actor-a",
                capability_key="cap.a",
            )
        )
        signal_store.ingest(
            self._signal(
                source_id="sensor-b",
                signal_id="item-1",
                actor_ref="actor-b",
                capability_key="cap.b",
            )
        )
        materialization = graph_store.materialize_current(
            signal_store, rule_store, created_at=NOW
        )
        return signal_store, rule_store, graph_store, materialization

    def test_composition_progresses_only_as_each_required_capability_becomes_callable(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._materialize(tmp)
            try:
                with SQLiteCapabilityVerificationStore(
                    Path(tmp) / "verification.db"
                ) as verification, SQLiteCompositionRunStore(
                    Path(tmp) / "runs.db"
                ) as runs:
                    baseline = runs.build_run(
                        graph,
                        self._bundle(),
                        materialization_id=materialization.materialization_id,
                        as_of=NOW + timedelta(hours=2),
                        created_at=NOW + timedelta(hours=2),
                    )
                    baseline_hypothesis = runs.hypotheses(baseline.run_id)[0]
                    self.assertEqual(
                        baseline_hypothesis.state,
                        CompositionState.DISCOVERED_COMPOSED,
                    )
                    self.assertEqual(baseline.verification_snapshot_fingerprint, "NONE")

                    verification.append(
                        self._verification(
                            verification_id="verify-a",
                            actor_ref="actor-a",
                            capability_key="cap.a",
                            related_signal_ref="sensor-a::item-1",
                        )
                    )
                    one_verified = runs.build_run(
                        graph,
                        self._bundle(),
                        verification_store=verification,
                        materialization_id=materialization.materialization_id,
                        as_of=NOW + timedelta(hours=2),
                        created_at=NOW + timedelta(hours=2, minutes=1),
                    )
                    one_hypothesis = runs.hypotheses(one_verified.run_id)[0]
                    self.assertEqual(
                        one_hypothesis.state,
                        CompositionState.DISCOVERED_COMPOSED,
                    )
                    self.assertNotEqual(
                        one_verified.verification_snapshot_fingerprint, "NONE"
                    )

                    verification.append(
                        self._verification(
                            verification_id="verify-b",
                            actor_ref="actor-b",
                            capability_key="cap.b",
                            related_signal_ref="sensor-b::item-1",
                        )
                    )
                    fully_verified = runs.build_run(
                        graph,
                        self._bundle(),
                        verification_store=verification,
                        materialization_id=materialization.materialization_id,
                        as_of=NOW + timedelta(hours=2),
                        created_at=NOW + timedelta(hours=2, minutes=2),
                    )
                    callable_hypothesis = runs.hypotheses(fully_verified.run_id)[0]
                    self.assertEqual(
                        callable_hypothesis.state,
                        CompositionState.CALLABLE_COMPOSED,
                    )
                    self.assertEqual(
                        set(callable_hypothesis.source_signal_ids),
                        {
                            "sensor-a::item-1",
                            "sensor-b::item-1",
                            "verification::verify-a",
                            "verification::verify-b",
                        },
                    )
                    self.assertNotEqual(baseline.run_id, one_verified.run_id)
                    self.assertNotEqual(one_verified.run_id, fully_verified.run_id)
            finally:
                graph.close()
                rules.close()
                signals.close()

    def test_rejected_capability_removes_known_stale_cover_from_verified_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._materialize(tmp)
            try:
                with SQLiteCapabilityVerificationStore(
                    Path(tmp) / "verification.db"
                ) as verification, SQLiteCompositionRunStore(
                    Path(tmp) / "runs.db"
                ) as runs:
                    verification.append(
                        self._verification(
                            verification_id="reject-b",
                            actor_ref="actor-b",
                            capability_key="cap.b",
                            related_signal_ref="sensor-b::item-1",
                            verdict=VerificationVerdict.REJECTED,
                            availability=AvailabilityState.UNKNOWN,
                            permission=PermissionState.UNKNOWN,
                        )
                    )
                    run = runs.build_run(
                        graph,
                        self._bundle(),
                        verification_store=verification,
                        materialization_id=materialization.materialization_id,
                        as_of=NOW + timedelta(hours=2),
                    )
                    self.assertEqual(run.hypothesis_count, 0)
                    self.assertEqual(runs.hypotheses(run.run_id), ())
            finally:
                graph.close()
                rules.close()
                signals.close()

    def test_future_verification_is_not_used_before_its_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._materialize(tmp)
            try:
                with SQLiteCapabilityVerificationStore(
                    Path(tmp) / "verification.db"
                ) as verification, SQLiteCompositionRunStore(
                    Path(tmp) / "runs.db"
                ) as runs:
                    future_time = NOW + timedelta(days=1)
                    verification.append(
                        self._verification(
                            verification_id="future-a",
                            actor_ref="actor-a",
                            capability_key="cap.a",
                            related_signal_ref="sensor-a::item-1",
                            verified_at=future_time,
                        )
                    )
                    verification.append(
                        self._verification(
                            verification_id="future-b",
                            actor_ref="actor-b",
                            capability_key="cap.b",
                            related_signal_ref="sensor-b::item-1",
                            verified_at=future_time,
                        )
                    )
                    before = runs.build_run(
                        graph,
                        self._bundle(),
                        verification_store=verification,
                        materialization_id=materialization.materialization_id,
                        as_of=NOW + timedelta(hours=1),
                    )
                    before_hypothesis = runs.hypotheses(before.run_id)[0]
                    self.assertEqual(
                        before_hypothesis.state,
                        CompositionState.DISCOVERED_COMPOSED,
                    )
            finally:
                graph.close()
                rules.close()
                signals.close()

    def test_existing_pre_verification_composition_db_migrates_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "legacy-runs.db"
            connection = sqlite3.connect(path)
            connection.execute(
                """
                CREATE TABLE composition_run (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    input_fingerprint TEXT NOT NULL UNIQUE,
                    materialization_id INTEGER NOT NULL,
                    graph_ruleset_fingerprint TEXT NOT NULL,
                    graph_observation_snapshot_fingerprint TEXT NOT NULL,
                    bundle_id TEXT NOT NULL,
                    bundle_version INTEGER NOT NULL,
                    bundle_source_ref TEXT NOT NULL,
                    bundle_rationale TEXT NOT NULL,
                    bundle_fingerprint TEXT NOT NULL,
                    as_of TEXT NOT NULL,
                    max_age_seconds INTEGER NOT NULL,
                    max_actors INTEGER NOT NULL,
                    max_hypotheses INTEGER NOT NULL,
                    hypothesis_count INTEGER NOT NULL
                )
                """
            )
            connection.commit()
            connection.close()

            with SQLiteCompositionRunStore(path) as migrated:
                columns = {
                    row["name"]
                    for row in migrated.connection.execute(
                        "PRAGMA table_info(composition_run)"
                    ).fetchall()
                }
                self.assertIn("verification_snapshot_fingerprint", columns)


if __name__ == "__main__":
    unittest.main()
