import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.access_feasibility import (
    AccessEvidence,
    AccessFeasibility,
    AccessRouteKind,
    AccessState,
)
from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import SQLiteCapabilityRuleRegistry
from src.capability_verification_store import (
    CapabilityVerificationEvent,
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_store import (
    CompositionValidationEvent,
    SQLiteCompositionValidationStore,
    ValidationDimension,
    ValidationGateState,
    access_validation_event,
)
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


class CompositionValidationStoreTests(unittest.TestCase):
    def _build_callable_run(self, tmp):
        signals = SQLiteSignalLedgerStore(Path(tmp) / "signals.db")
        rules = SQLiteCapabilityRuleRegistry(Path(tmp) / "rules.db")
        graph = SQLiteCapabilityGraphStore(Path(tmp) / "graph.db")
        verification = SQLiteCapabilityVerificationStore(Path(tmp) / "cap-verification.db")
        runs = SQLiteCompositionRunStore(Path(tmp) / "runs.db")

        signals.ingest(
            SignalObservation(
                signal_id="item-1",
                source_id="sensor-a",
                observed_at=NOW,
                actor_ref="actor-a",
                geography="Xuzhou",
                raw_text="offers cap.a",
                source_url="https://example.com/item-1",
                facts=(ObservedFact("fact.cap.a", True, "observed cap.a"),),
                explicit_capabilities=(ExplicitCapability("cap.a", "explicit cap.a"),),
                availability=AvailabilityState.ADVERTISED,
                permission=PermissionState.UNKNOWN,
            )
        )
        materialization = graph.materialize_current(signals, rules, created_at=NOW)
        verification.append(
            CapabilityVerificationEvent(
                verification_id="verify-a",
                actor_ref="actor-a",
                capability_key="cap.a",
                verdict=VerificationVerdict.CONFIRMED,
                verified_at=NOW + timedelta(minutes=5),
                evidence_ref="field:verify-a",
                evidence_note="reviewed capability verification",
                geography="Xuzhou",
                availability=AvailabilityState.CONFIRMED,
                permission=PermissionState.ALLOWED,
                related_signal_refs=("sensor-a::item-1",),
            )
        )
        bundle = RequirementBundleSpec(
            bundle_id="bundle-a",
            version=1,
            required_capabilities=("cap.a",),
            geography="Xuzhou",
            source_ref="opportunity:test",
            rationale="test capability bundle",
            active=True,
        )
        run = runs.build_run(
            graph,
            bundle,
            verification_store=verification,
            materialization_id=materialization.materialization_id,
            as_of=NOW + timedelta(hours=1),
        )
        self.assertEqual(runs.hypotheses(run.run_id)[0].state, CompositionState.CALLABLE_COMPOSED)
        return signals, rules, graph, verification, runs, run

    def _event(self, run_id, dimension, value="PASS", **overrides):
        payload = dict(
            validation_id=f"{dimension.value.lower()}-{value.lower()}",
            composition_run_id=run_id,
            hypothesis_index=0,
            dimension=dimension,
            value=value,
            observed_at=NOW + timedelta(hours=2),
            evidence_ref=f"field:{dimension.value.lower()}",
            evidence_note=f"reviewed {dimension.value.lower()} evidence",
            subject_ref="counterparty-a",
            details={"reviewed": True},
        )
        payload.update(overrides)
        return CompositionValidationEvent(**payload)

    def _access(self, *, blocked=False):
        return AccessFeasibility(
            candidate_id="candidate-a",
            target_actor="counterparty-a",
            route_kind=AccessRouteKind.PUBLIC_INSTITUTIONAL_WINDOW,
            legitimate_entry_path="" if blocked else "formal public cooperation window",
            backing_leverage="formal route gives legitimate entry context",
            counterparty_reason_to_engage="bounded pilot can reduce a measured operating cost",
            counterparty_visible_surplus="lower verified operating cost if pilot succeeds",
            surplus_realization_mechanism="accepted pilot output reduces repeated manual cost",
            institutional_cover_or_referral="formal institutional route",
            status_trust_friction="counterparty protects time, reputation and authority boundaries",
            operator_credibility_assets="relevant delivery history",
            missing_credibility="",
            operator_commitment="absorb initial coordination cost",
            counterparty_commitment_requested="confirm fit and nominate the correct bounded next step",
            founder_identity_dependency="low after formal route acceptance",
            evidence=(AccessEvidence("official-window", "formal cooperation route is published"),),
        )

    def _close(self, stores):
        for store in stores:
            store.close()

    def test_append_is_idempotent_and_conflicting_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            stores = self._build_callable_run(tmp)
            signals, rules, graph, verification, runs, run = stores
            try:
                with SQLiteCompositionValidationStore(Path(tmp) / "validation.db") as ledger:
                    event = self._event(run.run_id, ValidationDimension.ACTOR_ROLE_CLARITY)
                    ledger.append(event, composition_runs=runs)
                    ledger.append(event, composition_runs=runs)
                    self.assertEqual(len(ledger.events(run.run_id, 0)), 1)
                    changed = self._event(
                        run.run_id,
                        ValidationDimension.ACTOR_ROLE_CLARITY,
                        validation_id=event.validation_id,
                        evidence_note="different evidence",
                    )
                    with self.assertRaisesRegex(ValueError, "different content"):
                        ledger.append(changed, composition_runs=runs)
            finally:
                self._close((runs, verification, graph, rules, signals))

    def test_events_are_bound_to_existing_run_and_hypothesis(self):
        with tempfile.TemporaryDirectory() as tmp:
            stores = self._build_callable_run(tmp)
            signals, rules, graph, verification, runs, run = stores
            try:
                with SQLiteCompositionValidationStore(Path(tmp) / "validation.db") as ledger:
                    with self.assertRaisesRegex(ValueError, "unknown composition_run_id"):
                        ledger.append(
                            self._event(999, ValidationDimension.ACTOR_ROLE_CLARITY),
                            composition_runs=runs,
                        )
                    with self.assertRaisesRegex(ValueError, "unknown composition hypothesis index"):
                        ledger.append(
                            self._event(
                                run.run_id,
                                ValidationDimension.ACTOR_ROLE_CLARITY,
                                hypothesis_index=99,
                            ),
                            composition_runs=runs,
                        )
            finally:
                self._close((runs, verification, graph, rules, signals))

    def test_canonical_gates_remain_independent_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            stores = self._build_callable_run(tmp)
            signals, rules, graph, verification, runs, run = stores
            try:
                with SQLiteCompositionValidationStore(Path(tmp) / "validation.db") as ledger:
                    ledger.append(
                        self._event(run.run_id, ValidationDimension.ACTOR_ROLE_CLARITY),
                        composition_runs=runs,
                    )
                    projection = ledger.projection(
                        run.run_id, 0, composition_runs=runs, as_of=NOW + timedelta(hours=3)
                    )
                    self.assertEqual(
                        projection.transaction_gates(),
                        {"G0": "PASS", "G1": "UNKNOWN", "G2": "UNKNOWN", "G3": "UNKNOWN"},
                    )
                    self.assertFalse(projection.bounded_transaction_ready)

                    for dimension in (
                        ValidationDimension.PAYER_CLARITY,
                        ValidationDimension.NEED_CONFIRMATION,
                        ValidationDimension.COUNTERPARTY_VISIBLE_SURPLUS,
                        ValidationDimension.COUNTERPARTY_CONSENT,
                        ValidationDimension.PAYER_COMMITMENT,
                        ValidationDimension.ECONOMICS,
                    ):
                        ledger.append(self._event(run.run_id, dimension), composition_runs=runs)
                    ledger.append(
                        access_validation_event(
                            validation_id="access-ready",
                            composition_run_id=run.run_id,
                            hypothesis_index=0,
                            record=self._access(),
                            observed_at=NOW + timedelta(hours=2),
                            evidence_ref="access:review",
                            evidence_note="canonical access feasibility review",
                        ),
                        composition_runs=runs,
                    )
                    ledger.append(
                        self._event(
                            run.run_id,
                            ValidationDimension.LEGAL_TRUST_SAFETY,
                            value="CONDITIONAL",
                        ),
                        composition_runs=runs,
                    )
                    projection = ledger.projection(
                        run.run_id, 0, composition_runs=runs, as_of=NOW + timedelta(hours=3)
                    )
                    self.assertEqual(
                        projection.transaction_gates(),
                        {"G0": "PASS", "G1": "PASS", "G2": "PASS", "G3": "CONDITIONAL"},
                    )
                    self.assertTrue(projection.bounded_transaction_ready)
            finally:
                self._close((runs, verification, graph, rules, signals))

    def test_access_blocked_forces_g2_fail_without_mutating_other_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            stores = self._build_callable_run(tmp)
            signals, rules, graph, verification, runs, run = stores
            try:
                with SQLiteCompositionValidationStore(Path(tmp) / "validation.db") as ledger:
                    ledger.append(
                        self._event(run.run_id, ValidationDimension.ACTOR_ROLE_CLARITY),
                        composition_runs=runs,
                    )
                    ledger.append(
                        self._event(run.run_id, ValidationDimension.PAYER_CLARITY),
                        composition_runs=runs,
                    )
                    ledger.append(
                        access_validation_event(
                            validation_id="access-blocked",
                            composition_run_id=run.run_id,
                            hypothesis_index=0,
                            record=self._access(blocked=True),
                            observed_at=NOW + timedelta(hours=2),
                            evidence_ref="access:blocked",
                            evidence_note="canonical access review found no legitimate entry path",
                        ),
                        composition_runs=runs,
                    )
                    projection = ledger.projection(
                        run.run_id, 0, composition_runs=runs, as_of=NOW + timedelta(hours=3)
                    )
                    self.assertEqual(projection.access_state, AccessState.ACCESS_BLOCKED)
                    self.assertEqual(projection.transaction_gates()["G0"], "PASS")
                    self.assertEqual(projection.transaction_gates()["G1"], "PASS")
                    self.assertEqual(projection.transaction_gates()["G2"], "FAIL")
            finally:
                self._close((runs, verification, graph, rules, signals))

    def test_later_dimension_evidence_overrides_projection_but_preserves_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            stores = self._build_callable_run(tmp)
            signals, rules, graph, verification, runs, run = stores
            try:
                with SQLiteCompositionValidationStore(Path(tmp) / "validation.db") as ledger:
                    first = self._event(
                        run.run_id,
                        ValidationDimension.PAYER_CLARITY,
                        validation_id="payer-clear-pass",
                        observed_at=NOW + timedelta(hours=2),
                    )
                    later = self._event(
                        run.run_id,
                        ValidationDimension.PAYER_CLARITY,
                        value="FAIL",
                        validation_id="payer-clear-fail",
                        observed_at=NOW + timedelta(hours=4),
                    )
                    ledger.append(first, composition_runs=runs)
                    ledger.append(later, composition_runs=runs)
                    before = ledger.projection(
                        run.run_id, 0, composition_runs=runs, as_of=NOW + timedelta(hours=3)
                    )
                    after = ledger.projection(
                        run.run_id, 0, composition_runs=runs, as_of=NOW + timedelta(hours=5)
                    )
                    self.assertEqual(before.payer_clarity, ValidationGateState.PASS)
                    self.assertEqual(after.payer_clarity, ValidationGateState.FAIL)
                    self.assertEqual(len(ledger.events(run.run_id, 0)), 2)
                    self.assertNotEqual(
                        before.evidence_snapshot_fingerprint,
                        after.evidence_snapshot_fingerprint,
                    )
            finally:
                self._close((runs, verification, graph, rules, signals))

    def test_conditional_is_only_legal_for_g3_dimension(self):
        event = CompositionValidationEvent(
            validation_id="bad-conditional",
            composition_run_id=1,
            hypothesis_index=0,
            dimension=ValidationDimension.ECONOMICS,
            value="CONDITIONAL",
            observed_at=NOW,
            evidence_ref="field:bad",
            evidence_note="not allowed here",
        )
        self.assertIn("conditional_only_allowed_for_legal_trust_safety", event.validate())


if __name__ == "__main__":
    unittest.main()
