import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import CapabilityRuleSpec, SQLiteCapabilityRuleRegistry
from src.live_resource_signals import (
    AvailabilityState,
    EvidenceStatus,
    ExplicitCapability,
    FactCondition,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_ledger import TransitionKind
from src.live_signal_store import SQLiteSignalLedgerStore


NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)


class PersistentCapabilityGraphTests(unittest.TestCase):
    def _signal(
        self,
        *,
        source_id="sensor-a",
        signal_id="item-1",
        actor_ref="actor-a",
        observed_at=NOW,
        capability_key="task.local_errand",
        evidence_text="explicit local errand offer",
        fact_key="offers_paid_offline_tasks",
    ):
        return SignalObservation(
            signal_id=signal_id,
            source_id=source_id,
            observed_at=observed_at,
            actor_ref=actor_ref,
            geography="Xuzhou",
            raw_text=evidence_text,
            source_url=f"https://example.com/{source_id}/{signal_id}",
            facts=(ObservedFact(fact_key, True, evidence_text),),
            explicit_capabilities=(ExplicitCapability(capability_key, evidence_text),),
            availability=AvailabilityState.ADVERTISED,
            permission=PermissionState.UNKNOWN,
        )

    def _active_rule(self, *, version=1, capability_key="presence.local_execution"):
        return CapabilityRuleSpec(
            rule_id="local-presence",
            version=version,
            conditions=(FactCondition("offers_paid_offline_tasks"),),
            capability_key=capability_key,
            rationale=f"rule version {version}",
            active=True,
        )

    def test_materialization_persists_observed_and_inferred_claims_with_exact_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            signal_db = Path(tmp) / "signals.db"
            rule_db = Path(tmp) / "rules.db"
            graph_db = Path(tmp) / "graph.db"
            with SQLiteSignalLedgerStore(signal_db) as signals, SQLiteCapabilityRuleRegistry(
                rule_db
            ) as rules, SQLiteCapabilityGraphStore(graph_db) as graph:
                signals.ingest(self._signal())
                rules.register(self._active_rule())

                run = graph.materialize_current(signals, rules, created_at=NOW)
                claims = graph.claims(run.materialization_id)
                by_key = {claim.capability_key: claim for claim in claims}

                self.assertEqual(run.observation_count, 1)
                self.assertEqual(run.claim_count, 2)
                self.assertEqual(run.active_rule_ids, ("local-presence@v1",))
                self.assertEqual(by_key["task.local_errand"].evidence_status, EvidenceStatus.OBSERVED)
                self.assertEqual(
                    by_key["presence.local_execution"].evidence_status,
                    EvidenceStatus.INFERRED,
                )
                self.assertEqual(by_key["presence.local_execution"].source_id, "sensor-a")
                self.assertEqual(by_key["presence.local_execution"].signal_id, "item-1")
                self.assertEqual(
                    by_key["presence.local_execution"].inference_rule_id,
                    "local-presence@v1",
                )

                exported = graph.capability_claims(run.materialization_id)
                refs = {claim.source_signal_ids[0] for claim in exported}
                self.assertEqual(refs, {"sensor-a::item-1"})
                self.assertTrue(all(not claim.is_callable(NOW, timedelta(days=30)) for claim in exported))

    def test_same_rule_and_observation_snapshot_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as signals, SQLiteCapabilityRuleRegistry(
                Path(tmp) / "rules.db"
            ) as rules, SQLiteCapabilityGraphStore(Path(tmp) / "graph.db") as graph:
                signals.ingest(self._signal())
                rules.register(self._active_rule())
                first = graph.materialize_current(signals, rules, created_at=NOW)
                second = graph.materialize_current(
                    signals, rules, created_at=NOW + timedelta(hours=1)
                )
                self.assertEqual(first.materialization_id, second.materialization_id)
                self.assertEqual(graph.latest_materialization(), first)

    def test_rule_version_change_creates_new_immutable_graph_and_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as signals, SQLiteCapabilityRuleRegistry(
                Path(tmp) / "rules.db"
            ) as rules, SQLiteCapabilityGraphStore(Path(tmp) / "graph.db") as graph:
                signals.ingest(self._signal())
                rules.register(self._active_rule(version=1, capability_key="presence.local_execution"))
                before = graph.materialize_current(signals, rules, created_at=NOW)

                rules.register(
                    self._active_rule(
                        version=2,
                        capability_key="presence.local_execution.revised",
                    )
                )
                after = graph.materialize_current(
                    signals, rules, created_at=NOW + timedelta(hours=1)
                )
                diff = graph.diff(before.materialization_id, after.materialization_id)

                self.assertNotEqual(before.materialization_id, after.materialization_id)
                self.assertEqual(before.active_rule_ids, ("local-presence@v1",))
                self.assertEqual(after.active_rule_ids, ("local-presence@v2",))
                self.assertEqual(
                    {claim.capability_key for claim in diff.removed},
                    {"presence.local_execution"},
                )
                self.assertEqual(
                    {claim.capability_key for claim in diff.added},
                    {"presence.local_execution.revised"},
                )
                self.assertIn(
                    "presence.local_execution",
                    {claim.capability_key for claim in graph.claims(before.materialization_id)},
                )

    def test_out_of_order_raw_observation_is_archived_but_not_materialized_as_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as signals, SQLiteCapabilityRuleRegistry(
                Path(tmp) / "rules.db"
            ) as rules, SQLiteCapabilityGraphStore(Path(tmp) / "graph.db") as graph:
                current = self._signal(
                    observed_at=NOW + timedelta(days=2),
                    capability_key="cap.current",
                    fact_key="current_fact",
                )
                old = self._signal(
                    observed_at=NOW,
                    capability_key="cap.old",
                    fact_key="old_fact",
                )
                signals.ingest(current)
                transition = signals.ingest(old)
                self.assertEqual(transition.kind, TransitionKind.OUT_OF_ORDER)
                self.assertEqual(len(signals.observations()), 2)

                run = graph.materialize_current(signals, rules, created_at=NOW + timedelta(days=3))
                keys = {claim.capability_key for claim in graph.claims(run.materialization_id)}
                self.assertEqual(keys, {"cap.current"})

    def test_same_signal_id_from_different_sensors_has_unambiguous_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteSignalLedgerStore(Path(tmp) / "signals.db") as signals, SQLiteCapabilityRuleRegistry(
                Path(tmp) / "rules.db"
            ) as rules, SQLiteCapabilityGraphStore(Path(tmp) / "graph.db") as graph:
                signals.ingest(
                    self._signal(
                        source_id="sensor-a",
                        signal_id="item-1",
                        actor_ref="actor-a",
                        capability_key="cap.a",
                    )
                )
                signals.ingest(
                    self._signal(
                        source_id="sensor-b",
                        signal_id="item-1",
                        actor_ref="actor-b",
                        capability_key="cap.b",
                    )
                )
                run = graph.materialize_current(signals, rules, created_at=NOW)
                refs = {
                    claim.source_signal_ids[0]
                    for claim in graph.capability_claims(run.materialization_id)
                }
                self.assertEqual(refs, {"sensor-a::item-1", "sensor-b::item-1"})


if __name__ == "__main__":
    unittest.main()
