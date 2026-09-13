import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.access_feasibility import AccessEvidence, AccessFeasibility, AccessRouteKind
from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import SQLiteCapabilityRuleRegistry
from src.capability_verification_store import (
    CapabilityVerificationEvent,
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.composition_outcome_store import (
    CompositionOutcomeEvent,
    OutcomeEventType,
    SQLiteCompositionOutcomeStore,
)
from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_store import (
    CompositionValidationEvent,
    SQLiteCompositionValidationStore,
    ValidationDimension,
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


NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)
VALIDATION_TIME = NOW + timedelta(hours=2)


class CompositionOutcomeStoreTests(unittest.TestCase):
    def _build_ready_lineage(self, tmp):
        signals = SQLiteSignalLedgerStore(Path(tmp) / "signals.db")
        rules = SQLiteCapabilityRuleRegistry(Path(tmp) / "rules.db")
        graph = SQLiteCapabilityGraphStore(Path(tmp) / "graph.db")
        capability_verification = SQLiteCapabilityVerificationStore(
            Path(tmp) / "capability-verification.db"
        )
        runs = SQLiteCompositionRunStore(Path(tmp) / "runs.db")
        validations = SQLiteCompositionValidationStore(Path(tmp) / "validation.db")

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
        capability_verification.append(
            CapabilityVerificationEvent(
                verification_id="verify-a",
                actor_ref="actor-a",
                capability_key="cap.a",
                verdict=VerificationVerdict.CONFIRMED,
                verified_at=NOW + timedelta(minutes=10),
                evidence_ref="field:cap-a",
                evidence_note="capability and current availability verified",
                geography="Xuzhou",
                availability=AvailabilityState.CONFIRMED,
                permission=PermissionState.ALLOWED,
                related_signal_refs=("sensor-a::item-1",),
            )
        )
        run = runs.build_run(
            graph,
            RequirementBundleSpec(
                bundle_id="outcome-bundle",
                version=1,
                required_capabilities=("cap.a",),
                geography="Xuzhou",
                source_ref="opportunity:outcome-test",
                rationale="outcome ledger test bundle",
                active=True,
            ),
            verification_store=capability_verification,
            materialization_id=materialization.materialization_id,
            as_of=NOW + timedelta(hours=1),
        )

        def add_dimension(dimension, value="PASS"):
            validations.append(
                CompositionValidationEvent(
                    validation_id=f"validation-{dimension.value.lower()}",
                    composition_run_id=run.run_id,
                    hypothesis_index=0,
                    dimension=dimension,
                    value=value,
                    observed_at=VALIDATION_TIME,
                    evidence_ref=f"field:{dimension.value.lower()}",
                    evidence_note=f"reviewed {dimension.value.lower()} evidence",
                    subject_ref="counterparty-a",
                ),
                composition_runs=runs,
            )

        add_dimension(ValidationDimension.ACTOR_ROLE_CLARITY)
        add_dimension(ValidationDimension.PAYER_CLARITY)
        add_dimension(ValidationDimension.NEED_CONFIRMATION)
        add_dimension(ValidationDimension.COUNTERPARTY_VISIBLE_SURPLUS)
        add_dimension(ValidationDimension.COUNTERPARTY_CONSENT)
        add_dimension(ValidationDimension.PAYER_COMMITMENT)
        add_dimension(ValidationDimension.ECONOMICS)
        add_dimension(ValidationDimension.LEGAL_TRUST_SAFETY)
        validations.append(
            access_validation_event(
                validation_id="validation-access",
                composition_run_id=run.run_id,
                hypothesis_index=0,
                record=AccessFeasibility(
                    candidate_id="candidate-a",
                    target_actor="counterparty-a",
                    route_kind=AccessRouteKind.PUBLIC_INSTITUTIONAL_WINDOW,
                    legitimate_entry_path="formal cooperation window",
                    backing_leverage="formal route gives legitimate entry context",
                    counterparty_reason_to_engage="bounded pilot has a concrete cost-saving mechanism",
                    counterparty_visible_surplus="measurable operating cost reduction",
                    surplus_realization_mechanism="accepted output replaces repeated manual effort",
                    institutional_cover_or_referral="formal route",
                    status_trust_friction="counterparty protects time and authority boundaries",
                    operator_credibility_assets="relevant delivery history",
                    missing_credibility="",
                    operator_commitment="absorb initial coordination cost",
                    counterparty_commitment_requested="authorize the bounded route test",
                    founder_identity_dependency="low after route acceptance",
                    evidence=(
                        AccessEvidence(
                            "official-window",
                            "formal cooperation route is explicitly available",
                        ),
                    ),
                ),
                observed_at=VALIDATION_TIME,
                evidence_ref="field:access",
                evidence_note="canonical access feasibility reviewed",
            ),
            composition_runs=runs,
        )
        ready = validations.projection(
            run.run_id,
            0,
            composition_runs=runs,
            as_of=VALIDATION_TIME,
        )
        self.assertTrue(ready.bounded_transaction_ready)
        return (
            signals,
            rules,
            graph,
            capability_verification,
            runs,
            validations,
            run,
            ready.evidence_snapshot_fingerprint,
        )

    def _outcome(
        self,
        run_id,
        fingerprint,
        *,
        outcome_id,
        transaction_ref,
        event_type,
        observed_at,
        amount=None,
        currency=None,
    ):
        return CompositionOutcomeEvent(
            outcome_id=outcome_id,
            composition_run_id=run_id,
            hypothesis_index=0,
            transaction_ref=transaction_ref,
            event_type=event_type,
            observed_at=observed_at,
            validation_as_of=VALIDATION_TIME,
            validation_snapshot_fingerprint=fingerprint,
            evidence_ref=f"field:{outcome_id}",
            evidence_note=f"reviewed real outcome evidence for {outcome_id}",
            subject_ref="counterparty-a",
            amount=amount,
            currency=currency,
        )

    @staticmethod
    def _close(stores):
        for store in stores:
            store.close()

    def test_outcome_requires_exact_ready_validation_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            lineage = self._build_ready_lineage(tmp)
            signals, rules, graph, cap_verify, runs, validations, run, fingerprint = lineage
            try:
                with SQLiteCompositionOutcomeStore(Path(tmp) / "outcomes.db") as outcomes:
                    wrong = self._outcome(
                        run.run_id,
                        "wrong-fingerprint",
                        outcome_id="start-wrong",
                        transaction_ref="tx-1",
                        event_type=OutcomeEventType.ROUTE_TEST_STARTED,
                        observed_at=VALIDATION_TIME + timedelta(minutes=5),
                    )
                    with self.assertRaisesRegex(ValueError, "validation_snapshot_fingerprint"):
                        outcomes.append(
                            wrong,
                            composition_runs=runs,
                            validations=validations,
                        )

                    early_projection = validations.projection(
                        run.run_id,
                        0,
                        composition_runs=runs,
                        as_of=NOW + timedelta(hours=1),
                    )
                    self.assertFalse(early_projection.bounded_transaction_ready)
                    early = CompositionOutcomeEvent(
                        outcome_id="start-too-early",
                        composition_run_id=run.run_id,
                        hypothesis_index=0,
                        transaction_ref="tx-1",
                        event_type=OutcomeEventType.ROUTE_TEST_STARTED,
                        observed_at=VALIDATION_TIME + timedelta(minutes=5),
                        validation_as_of=NOW + timedelta(hours=1),
                        validation_snapshot_fingerprint=early_projection.evidence_snapshot_fingerprint,
                        evidence_ref="field:start-too-early",
                        evidence_note="attempted to bind outcome to non-ready snapshot",
                    )
                    with self.assertRaisesRegex(ValueError, "bounded_transaction_ready"):
                        outcomes.append(
                            early,
                            composition_runs=runs,
                            validations=validations,
                        )
            finally:
                self._close((validations, runs, cap_verify, graph, rules, signals))

    def test_l3_l4_l5_l6_progress_only_from_required_real_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            lineage = self._build_ready_lineage(tmp)
            signals, rules, graph, cap_verify, runs, validations, run, fingerprint = lineage
            try:
                with SQLiteCompositionOutcomeStore(Path(tmp) / "outcomes.db") as outcomes:
                    t0 = VALIDATION_TIME + timedelta(minutes=10)
                    events = [
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="tx1-signed",
                            transaction_ref="tx-1",
                            event_type=OutcomeEventType.SIGNED_TASK_OBSERVED,
                            observed_at=t0,
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="tx1-accepted",
                            transaction_ref="tx-1",
                            event_type=OutcomeEventType.DELIVERY_ACCEPTED,
                            observed_at=t0 + timedelta(minutes=10),
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="tx1-settled",
                            transaction_ref="tx-1",
                            event_type=OutcomeEventType.SETTLEMENT_OBSERVED,
                            observed_at=t0 + timedelta(minutes=20),
                            amount="1200.50",
                            currency="CNY",
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="tx2-accepted",
                            transaction_ref="tx-2",
                            event_type=OutcomeEventType.DELIVERY_ACCEPTED,
                            observed_at=t0 + timedelta(minutes=30),
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="tx2-settled",
                            transaction_ref="tx-2",
                            event_type=OutcomeEventType.SETTLEMENT_OBSERVED,
                            observed_at=t0 + timedelta(minutes=40),
                            amount="800",
                            currency="CNY",
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="tx2-replacement",
                            transaction_ref="tx-2",
                            event_type=OutcomeEventType.PROVIDER_REPLACEMENT_SUCCEEDED,
                            observed_at=t0 + timedelta(minutes=50),
                        ),
                    ]
                    for event in events:
                        outcomes.append(
                            event,
                            composition_runs=runs,
                            validations=validations,
                        )

                    l3 = outcomes.projection(
                        run.run_id, 0, as_of=t0 + timedelta(minutes=5)
                    )
                    l4 = outcomes.projection(
                        run.run_id, 0, as_of=t0 + timedelta(minutes=25)
                    )
                    l5 = outcomes.projection(
                        run.run_id, 0, as_of=t0 + timedelta(minutes=45)
                    )
                    l6 = outcomes.projection(
                        run.run_id, 0, as_of=t0 + timedelta(minutes=55)
                    )
                    self.assertEqual(l3.evidence_maturity, "L3")
                    self.assertEqual(l4.evidence_maturity, "L4")
                    self.assertEqual(l5.evidence_maturity, "L5")
                    self.assertEqual(l6.evidence_maturity, "L6")
                    self.assertEqual(l6.accepted_settled_transaction_count, 2)
                    self.assertEqual(l6.settlement_totals, {"CNY": "2000.50"})
                    self.assertTrue(l6.l6_mechanism_observed)
            finally:
                self._close((validations, runs, cap_verify, graph, rules, signals))

    def test_acceptance_and_settlement_from_different_transactions_do_not_make_l4(self):
        with tempfile.TemporaryDirectory() as tmp:
            lineage = self._build_ready_lineage(tmp)
            signals, rules, graph, cap_verify, runs, validations, run, fingerprint = lineage
            try:
                with SQLiteCompositionOutcomeStore(Path(tmp) / "outcomes.db") as outcomes:
                    t0 = VALIDATION_TIME + timedelta(minutes=10)
                    outcomes.append(
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="accept-a",
                            transaction_ref="tx-a",
                            event_type=OutcomeEventType.DELIVERY_ACCEPTED,
                            observed_at=t0,
                        ),
                        composition_runs=runs,
                        validations=validations,
                    )
                    outcomes.append(
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="settle-b",
                            transaction_ref="tx-b",
                            event_type=OutcomeEventType.SETTLEMENT_OBSERVED,
                            observed_at=t0 + timedelta(minutes=1),
                            amount="500",
                            currency="CNY",
                        ),
                        composition_runs=runs,
                        validations=validations,
                    )
                    projection = outcomes.projection(
                        run.run_id, 0, as_of=t0 + timedelta(minutes=2)
                    )
                    self.assertEqual(projection.evidence_maturity, "L0")
                    self.assertEqual(projection.accepted_settled_transaction_count, 0)
            finally:
                self._close((validations, runs, cap_verify, graph, rules, signals))

    def test_failure_evidence_is_preserved_without_erasing_prior_transaction_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            lineage = self._build_ready_lineage(tmp)
            signals, rules, graph, cap_verify, runs, validations, run, fingerprint = lineage
            try:
                with SQLiteCompositionOutcomeStore(Path(tmp) / "outcomes.db") as outcomes:
                    t0 = VALIDATION_TIME + timedelta(minutes=10)
                    for event in (
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="accepted",
                            transaction_ref="tx-1",
                            event_type=OutcomeEventType.DELIVERY_ACCEPTED,
                            observed_at=t0,
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="settled",
                            transaction_ref="tx-1",
                            event_type=OutcomeEventType.SETTLEMENT_OBSERVED,
                            observed_at=t0 + timedelta(minutes=1),
                            amount="1000",
                            currency="CNY",
                        ),
                        self._outcome(
                            run.run_id,
                            fingerprint,
                            outcome_id="later-route-failure",
                            transaction_ref="tx-2",
                            event_type=OutcomeEventType.ROUTE_FAILED,
                            observed_at=t0 + timedelta(minutes=2),
                        ),
                    ):
                        outcomes.append(
                            event,
                            composition_runs=runs,
                            validations=validations,
                        )
                    projection = outcomes.projection(
                        run.run_id, 0, as_of=t0 + timedelta(minutes=3)
                    )
                    self.assertEqual(projection.evidence_maturity, "L4")
                    self.assertEqual(projection.accepted_settled_transaction_count, 1)
                    self.assertEqual(projection.failed_transaction_count, 1)
                    self.assertEqual(projection.latest_event_type, OutcomeEventType.ROUTE_FAILED)
            finally:
                self._close((validations, runs, cap_verify, graph, rules, signals))

    def test_append_is_idempotent_and_conflicting_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            lineage = self._build_ready_lineage(tmp)
            signals, rules, graph, cap_verify, runs, validations, run, fingerprint = lineage
            try:
                with SQLiteCompositionOutcomeStore(Path(tmp) / "outcomes.db") as outcomes:
                    event = self._outcome(
                        run.run_id,
                        fingerprint,
                        outcome_id="start",
                        transaction_ref="tx-1",
                        event_type=OutcomeEventType.ROUTE_TEST_STARTED,
                        observed_at=VALIDATION_TIME + timedelta(minutes=10),
                    )
                    outcomes.append(event, composition_runs=runs, validations=validations)
                    outcomes.append(event, composition_runs=runs, validations=validations)
                    self.assertEqual(len(outcomes.events(run.run_id, 0)), 1)
                    changed = self._outcome(
                        run.run_id,
                        fingerprint,
                        outcome_id="start",
                        transaction_ref="tx-1",
                        event_type=OutcomeEventType.ROUTE_FAILED,
                        observed_at=VALIDATION_TIME + timedelta(minutes=10),
                    )
                    with self.assertRaisesRegex(ValueError, "different content"):
                        outcomes.append(
                            changed,
                            composition_runs=runs,
                            validations=validations,
                        )
            finally:
                self._close((validations, runs, cap_verify, graph, rules, signals))

    def test_settlement_requires_positive_amount_and_currency(self):
        event = CompositionOutcomeEvent(
            outcome_id="bad-settlement",
            composition_run_id=1,
            hypothesis_index=0,
            transaction_ref="tx-1",
            event_type=OutcomeEventType.SETTLEMENT_OBSERVED,
            observed_at=NOW + timedelta(hours=2),
            validation_as_of=NOW + timedelta(hours=1),
            validation_snapshot_fingerprint="abc",
            evidence_ref="field:settlement",
            evidence_note="claimed settlement without amount",
        )
        errors = event.validate()
        self.assertIn("settlement_requires_amount", errors)
        self.assertIn("settlement_requires_currency", errors)


if __name__ == "__main__":
    unittest.main()
