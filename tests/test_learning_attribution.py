import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.access_feasibility import AccessEvidence, AccessFeasibility, AccessRouteKind
from src.capability_graph_store import SQLiteCapabilityGraphStore
from src.capability_rule_registry import CapabilityRuleSpec, SQLiteCapabilityRuleRegistry
from src.capability_verification_store import (
    CapabilityVerificationEvent,
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.composition_outcome_store import CompositionOutcomeEvent, OutcomeEventType, SQLiteCompositionOutcomeStore
from src.composition_run_store import SQLiteCompositionRunStore
from src.composition_validation_store import (
    CompositionValidationEvent,
    SQLiteCompositionValidationStore,
    ValidationDimension,
    access_validation_event,
)
from src.learning_attribution import (
    LinkedVerificationState,
    ReviewSignal,
    claim_verification_diagnostics,
    composition_learning_diagnostic,
    rule_verification_summaries,
    source_verification_summaries,
)
from src.live_resource_signals import (
    AvailabilityState,
    FactCondition,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_store import SQLiteSignalLedgerStore
from src.requirement_bundle_registry import RequirementBundleSpec


NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)


class LearningAttributionTests(unittest.TestCase):
    def _build_graph(self, tmp):
        signals = SQLiteSignalLedgerStore(Path(tmp) / "signals.db")
        rules = SQLiteCapabilityRuleRegistry(Path(tmp) / "rules.db")
        graph = SQLiteCapabilityGraphStore(Path(tmp) / "graph.db")
        rules.register(
            CapabilityRuleSpec(
                rule_id="rule-local-presence",
                version=1,
                conditions=(FactCondition("offers_local_task", True),),
                capability_key="presence.local_execution",
                rationale="offering a local offline task supports a local-presence hypothesis",
                active=True,
            )
        )
        for signal_id, actor_ref, source_id, observed_at in (
            ("s1", "actor-a", "source-a", NOW),
            ("s2", "actor-b", "source-a", NOW),
            ("s3", "actor-c", "source-b", NOW + timedelta(hours=1)),
        ):
            signals.ingest(
                SignalObservation(
                    signal_id=signal_id,
                    source_id=source_id,
                    observed_at=observed_at,
                    actor_ref=actor_ref,
                    geography="Xuzhou",
                    raw_text="local task",
                    source_url=f"https://example.com/{signal_id}",
                    facts=(ObservedFact("offers_local_task", True, "local task observed"),),
                    availability=AvailabilityState.ADVERTISED,
                    permission=PermissionState.UNKNOWN,
                )
            )
        materialization = graph.materialize_current(signals, rules, created_at=NOW + timedelta(hours=2))
        return signals, rules, graph, materialization

    @staticmethod
    def _close(stores):
        for store in stores:
            store.close()

    def test_exact_related_signal_ref_is_required_for_source_and_rule_learning(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._build_graph(tmp)
            verification = SQLiteCapabilityVerificationStore(Path(tmp) / "verify.db")
            try:
                verification.append(
                    CapabilityVerificationEvent(
                        verification_id="v1",
                        actor_ref="actor-a",
                        capability_key="presence.local_execution",
                        verdict=VerificationVerdict.CONFIRMED,
                        verified_at=NOW + timedelta(hours=3),
                        evidence_ref="field:v1",
                        evidence_note="actor-a capability independently confirmed",
                        geography="Xuzhou",
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                        related_signal_refs=("source-a::s1",),
                    )
                )
                verification.append(
                    CapabilityVerificationEvent(
                        verification_id="v2",
                        actor_ref="actor-b",
                        capability_key="presence.local_execution",
                        verdict=VerificationVerdict.REJECTED,
                        verified_at=NOW + timedelta(hours=3),
                        evidence_ref="field:v2",
                        evidence_note="actor-b capability independently rejected",
                        related_signal_refs=("source-a::s2",),
                    )
                )
                # Same actor/capability, but no exact source-signal linkage: must stay unresolved
                # for source/rule diagnostics.
                verification.append(
                    CapabilityVerificationEvent(
                        verification_id="v3",
                        actor_ref="actor-c",
                        capability_key="presence.local_execution",
                        verdict=VerificationVerdict.CONFIRMED,
                        verified_at=NOW + timedelta(hours=3),
                        evidence_ref="field:v3",
                        evidence_note="actor-c confirmed without linking the originating signal",
                        geography="Xuzhou",
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                        related_signal_refs=(),
                    )
                )
                diagnostics = claim_verification_diagnostics(
                    graph,
                    verification,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW + timedelta(hours=4),
                )
                states = {item.source_signal_ref: item.linked_state for item in diagnostics}
                self.assertEqual(states["source-a::s1"], LinkedVerificationState.CONFIRMED)
                self.assertEqual(states["source-a::s2"], LinkedVerificationState.REJECTED)
                self.assertEqual(states["source-b::s3"], LinkedVerificationState.UNRESOLVED)

                sources = {
                    item.lineage_id: item
                    for item in source_verification_summaries(
                        diagnostics, minimum_linked_verifications=2
                    )
                }
                self.assertEqual(sources["source-a"].confirmed_count, 1)
                self.assertEqual(sources["source-a"].rejected_count, 1)
                self.assertEqual(sources["source-a"].review_signal, ReviewSignal.MIXED_LINKED_VERIFICATION)
                self.assertEqual(sources["source-b"].unresolved_count, 1)
                self.assertEqual(sources["source-b"].review_signal, ReviewSignal.NO_LINKED_VERIFICATION)

                rule = rule_verification_summaries(
                    diagnostics, minimum_linked_verifications=2
                )[0]
                self.assertEqual(rule.lineage_id, "rule-local-presence@v1")
                self.assertEqual(rule.claim_output_count, 3)
                self.assertEqual(rule.review_signal, ReviewSignal.MIXED_LINKED_VERIFICATION)
            finally:
                self._close((verification, graph, rules, signals))

    def test_older_verification_does_not_validate_newer_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._build_graph(tmp)
            verification = SQLiteCapabilityVerificationStore(Path(tmp) / "verify.db")
            try:
                verification.append(
                    CapabilityVerificationEvent(
                        verification_id="old-v",
                        actor_ref="actor-c",
                        capability_key="presence.local_execution",
                        verdict=VerificationVerdict.CONFIRMED,
                        verified_at=NOW + timedelta(minutes=30),
                        evidence_ref="field:old",
                        evidence_note="older confirmation",
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                        related_signal_refs=("source-b::s3",),
                    )
                )
                diagnostics = claim_verification_diagnostics(
                    graph,
                    verification,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW + timedelta(hours=4),
                )
                by_ref = {item.source_signal_ref: item for item in diagnostics}
                self.assertEqual(
                    by_ref["source-b::s3"].linked_state,
                    LinkedVerificationState.UNRESOLVED,
                )
            finally:
                self._close((verification, graph, rules, signals))

    def test_low_sample_produces_review_signal_not_automatic_quality_judgment(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._build_graph(tmp)
            verification = SQLiteCapabilityVerificationStore(Path(tmp) / "verify.db")
            try:
                verification.append(
                    CapabilityVerificationEvent(
                        verification_id="v1",
                        actor_ref="actor-a",
                        capability_key="presence.local_execution",
                        verdict=VerificationVerdict.CONFIRMED,
                        verified_at=NOW + timedelta(hours=3),
                        evidence_ref="field:v1",
                        evidence_note="one linked confirmation",
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                        related_signal_refs=("source-a::s1",),
                    )
                )
                diagnostics = claim_verification_diagnostics(
                    graph,
                    verification,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW + timedelta(hours=4),
                )
                summary = source_verification_summaries(
                    diagnostics, minimum_linked_verifications=5
                )[0]
                self.assertEqual(
                    summary.review_signal,
                    ReviewSignal.INSUFFICIENT_LINKED_VERIFICATION,
                )
            finally:
                self._close((verification, graph, rules, signals))

    def test_composition_diagnostic_exposes_lineage_without_causal_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            signals, rules, graph, materialization = self._build_graph(tmp)
            verification = SQLiteCapabilityVerificationStore(Path(tmp) / "verify.db")
            runs = SQLiteCompositionRunStore(Path(tmp) / "runs.db")
            validations = SQLiteCompositionValidationStore(Path(tmp) / "validation.db")
            outcomes = SQLiteCompositionOutcomeStore(Path(tmp) / "outcomes.db")
            try:
                verification.append(
                    CapabilityVerificationEvent(
                        verification_id="v1",
                        actor_ref="actor-a",
                        capability_key="presence.local_execution",
                        verdict=VerificationVerdict.CONFIRMED,
                        verified_at=NOW + timedelta(hours=3),
                        evidence_ref="field:v1",
                        evidence_note="actor-a capability confirmed",
                        geography="Xuzhou",
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                        related_signal_refs=("source-a::s1",),
                    )
                )
                run = runs.build_run(
                    graph,
                    RequirementBundleSpec(
                        bundle_id="bundle-learning",
                        version=1,
                        required_capabilities=("presence.local_execution",),
                        geography="Xuzhou",
                        source_ref="opportunity:learning",
                        rationale="learning attribution test",
                        active=True,
                    ),
                    verification_store=verification,
                    materialization_id=materialization.materialization_id,
                    as_of=NOW + timedelta(hours=4),
                )
                # actor-a is lexically first and callable; one-actor minimal cover is hypothesis 0.
                validation_time = NOW + timedelta(hours=5)
                for dimension in (
                    ValidationDimension.ACTOR_ROLE_CLARITY,
                    ValidationDimension.PAYER_CLARITY,
                    ValidationDimension.NEED_CONFIRMATION,
                    ValidationDimension.COUNTERPARTY_VISIBLE_SURPLUS,
                    ValidationDimension.COUNTERPARTY_CONSENT,
                    ValidationDimension.PAYER_COMMITMENT,
                    ValidationDimension.ECONOMICS,
                    ValidationDimension.LEGAL_TRUST_SAFETY,
                ):
                    validations.append(
                        CompositionValidationEvent(
                            validation_id=f"val-{dimension.value.lower()}",
                            composition_run_id=run.run_id,
                            hypothesis_index=0,
                            dimension=dimension,
                            value="PASS",
                            observed_at=validation_time,
                            evidence_ref=f"field:{dimension.value.lower()}",
                            evidence_note="reviewed validation evidence",
                        ),
                        composition_runs=runs,
                    )
                validations.append(
                    access_validation_event(
                        validation_id="val-access",
                        composition_run_id=run.run_id,
                        hypothesis_index=0,
                        record=AccessFeasibility(
                            candidate_id="candidate-learning",
                            target_actor="actor-a",
                            route_kind=AccessRouteKind.PUBLIC_INSTITUTIONAL_WINDOW,
                            legitimate_entry_path="formal bounded route",
                            backing_leverage="formal route provides context",
                            counterparty_reason_to_engage="measurable bounded gain",
                            counterparty_visible_surplus="measurable bounded gain",
                            surplus_realization_mechanism="accepted output creates gain",
                            institutional_cover_or_referral="formal route",
                            status_trust_friction="bounded",
                            operator_credibility_assets="relevant history",
                            missing_credibility="",
                            operator_commitment="bounded coordination",
                            counterparty_commitment_requested="authorize bounded test",
                            founder_identity_dependency="low",
                            evidence=(AccessEvidence("route", "formal route evidenced"),),
                        ),
                        observed_at=validation_time,
                        evidence_ref="field:access",
                        evidence_note="canonical access reviewed",
                    ),
                    composition_runs=runs,
                )
                validation_projection = validations.projection(
                    run.run_id,
                    0,
                    composition_runs=runs,
                    as_of=validation_time,
                )
                self.assertTrue(validation_projection.bounded_transaction_ready)
                for outcome_id, event_type, minutes, amount, currency in (
                    ("accepted", OutcomeEventType.DELIVERY_ACCEPTED, 10, None, None),
                    ("settled", OutcomeEventType.SETTLEMENT_OBSERVED, 20, "500", "CNY"),
                ):
                    outcomes.append(
                        CompositionOutcomeEvent(
                            outcome_id=outcome_id,
                            composition_run_id=run.run_id,
                            hypothesis_index=0,
                            transaction_ref="tx-1",
                            event_type=event_type,
                            observed_at=validation_time + timedelta(minutes=minutes),
                            validation_as_of=validation_time,
                            validation_snapshot_fingerprint=validation_projection.evidence_snapshot_fingerprint,
                            evidence_ref=f"field:{outcome_id}",
                            evidence_note=f"reviewed {outcome_id}",
                            amount=amount,
                            currency=currency,
                        ),
                        composition_runs=runs,
                        validations=validations,
                    )
                diagnostic = composition_learning_diagnostic(
                    graph,
                    runs,
                    validations,
                    outcomes,
                    run_id=run.run_id,
                    hypothesis_index=0,
                    as_of=validation_time + timedelta(hours=1),
                )
                self.assertIn("source-a", diagnostic.source_ids)
                self.assertIn("rule-local-presence@v1", diagnostic.inference_rule_ids)
                self.assertTrue(diagnostic.bounded_transaction_ready)
                self.assertEqual(diagnostic.outcome_evidence_maturity, "L4")
                self.assertEqual(diagnostic.accepted_settled_transaction_count, 1)
                self.assertIn("not establish causal credit", diagnostic.truth_note)
            finally:
                self._close((outcomes, validations, runs, verification, graph, rules, signals))


if __name__ == "__main__":
    unittest.main()
