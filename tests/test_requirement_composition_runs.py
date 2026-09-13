import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import SQLiteCapabilityRuleRegistry
from src.composition_run_store import SQLiteCompositionRunStore
from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_store import SQLiteSignalLedgerStore
from src.requirement_bundle_registry import (
    RequirementBundleSpec,
    SQLiteRequirementBundleRegistry,
)
from src.resource_composition import CompositionState


NOW = datetime(2026, 9, 13, 13, 0, tzinfo=timezone.utc)


class RequirementAndCompositionRunTests(unittest.TestCase):
    def _bundle(self, *, version=1, capabilities=("cap.a", "cap.b"), active=True):
        return RequirementBundleSpec(
            bundle_id="opp-1-capabilities",
            version=version,
            required_capabilities=capabilities,
            geography="Xuzhou",
            source_ref="opportunity:opp-1",
            rationale=f"decomposition version {version}",
            active=active,
        )

    def _signal(self, source_id, signal_id, actor_ref, capability_key):
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

    def test_requirement_registry_versions_are_immutable_and_activation_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.db"
            with SQLiteRequirementBundleRegistry(path) as registry:
                registry.register(self._bundle(version=1, active=True))
                registry.register(
                    self._bundle(
                        version=2,
                        capabilities=("cap.a", "cap.b", "cap.c"),
                        active=True,
                    )
                )

                versions = registry.versions("opp-1-capabilities")
                self.assertEqual(tuple(spec.version for spec in versions), (1, 2))
                self.assertFalse(versions[0].active)
                self.assertTrue(versions[1].active)
                self.assertEqual(registry.active("opp-1-capabilities").version, 2)
                self.assertEqual(versions[1].source_ref, "opportunity:opp-1")

                with self.assertRaisesRegex(ValueError, "different content"):
                    registry.register(
                        RequirementBundleSpec(
                            bundle_id="opp-1-capabilities",
                            version=2,
                            required_capabilities=("different.capability",),
                            geography="Xuzhou",
                            source_ref="opportunity:opp-1",
                            rationale="conflicting rewrite",
                            active=True,
                        )
                    )

    def test_graph_to_requirement_run_persists_discovered_multi_actor_composition(self):
        with tempfile.TemporaryDirectory() as tmp:
            signal_db = Path(tmp) / "signals.db"
            rule_db = Path(tmp) / "rules.db"
            graph_db = Path(tmp) / "graph.db"
            requirement_db = Path(tmp) / "requirements.db"
            run_db = Path(tmp) / "composition.db"

            with SQLiteSignalLedgerStore(signal_db) as signals, SQLiteCapabilityRuleRegistry(
                rule_db
            ) as rules, SQLiteCapabilityGraphStore(graph_db) as graph, SQLiteRequirementBundleRegistry(
                requirement_db
            ) as requirements, SQLiteCompositionRunStore(run_db) as runs:
                signals.ingest(self._signal("sensor-a", "item-1", "actor-a", "cap.a"))
                signals.ingest(self._signal("sensor-b", "item-1", "actor-b", "cap.b"))
                materialization = graph.materialize_current(signals, rules, created_at=NOW)

                requirements.register(self._bundle())
                spec = requirements.active("opp-1-capabilities")
                self.assertIsNotNone(spec)
                run = runs.build_run(
                    graph,
                    spec,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW,
                    created_at=NOW,
                )
                hypotheses = runs.hypotheses(run.run_id)

                self.assertEqual(run.materialization_id, materialization.materialization_id)
                self.assertEqual(run.bundle_version, 1)
                self.assertEqual(run.bundle_source_ref, "opportunity:opp-1")
                self.assertEqual(run.hypothesis_count, 1)
                self.assertEqual(hypotheses[0].actor_refs, ("actor-a", "actor-b"))
                self.assertEqual(hypotheses[0].state, CompositionState.DISCOVERED_COMPOSED)
                self.assertEqual(
                    set(hypotheses[0].source_signal_ids),
                    {"sensor-a::item-1", "sensor-b::item-1"},
                )
                self.assertNotEqual(hypotheses[0].state, CompositionState.CALLABLE_COMPOSED)

    def test_same_graph_bundle_and_parameters_are_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as signals, SQLiteCapabilityRuleRegistry(
                Path(tmp) / "rules.db"
            ) as rules, SQLiteCapabilityGraphStore(Path(tmp) / "graph.db") as graph, SQLiteCompositionRunStore(
                Path(tmp) / "composition.db"
            ) as runs:
                signals.ingest(self._signal("sensor-a", "item-1", "actor-a", "cap.a"))
                signals.ingest(self._signal("sensor-b", "item-2", "actor-b", "cap.b"))
                materialization = graph.materialize_current(signals, rules, created_at=NOW)
                spec = self._bundle()

                first = runs.build_run(
                    graph,
                    spec,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW,
                    created_at=NOW,
                )
                second = runs.build_run(
                    graph,
                    spec,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW,
                    created_at=NOW + timedelta(hours=1),
                )
                self.assertEqual(first.run_id, second.run_id)

    def test_requirement_version_change_creates_new_composition_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as signals, SQLiteCapabilityRuleRegistry(
                Path(tmp) / "rules.db"
            ) as rules, SQLiteCapabilityGraphStore(Path(tmp) / "graph.db") as graph, SQLiteCompositionRunStore(
                Path(tmp) / "composition.db"
            ) as runs:
                signals.ingest(self._signal("sensor-a", "item-1", "actor-a", "cap.a"))
                signals.ingest(self._signal("sensor-b", "item-2", "actor-b", "cap.b"))
                materialization = graph.materialize_current(signals, rules, created_at=NOW)

                v1 = runs.build_run(
                    graph,
                    self._bundle(version=1),
                    materialization_id=materialization.materialization_id,
                    as_of=NOW,
                    created_at=NOW,
                )
                v2 = runs.build_run(
                    graph,
                    self._bundle(version=2),
                    materialization_id=materialization.materialization_id,
                    as_of=NOW,
                    created_at=NOW + timedelta(minutes=1),
                )
                self.assertNotEqual(v1.run_id, v2.run_id)
                self.assertEqual(v1.bundle_version, 1)
                self.assertEqual(v2.bundle_version, 2)


if __name__ == "__main__":
    unittest.main()
