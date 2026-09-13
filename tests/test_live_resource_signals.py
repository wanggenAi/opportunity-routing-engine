import unittest
from datetime import datetime, timedelta, timezone

from src.capability_coverage import (
    CapabilityRequirement,
    CoverageState,
    RequirementBundle,
    evaluate_coverage,
)
from src.live_resource_signals import (
    AvailabilityState,
    CapabilityInferenceRule,
    EvidenceStatus,
    ExplicitCapability,
    FactCondition,
    ObservedFact,
    PermissionState,
    SignalObservation,
    confirm_capability,
    extract_capability_claims,
)


NOW = datetime(2026, 9, 13, 8, 0, tzinfo=timezone.utc)


class LiveResourceSignalTests(unittest.TestCase):
    def _signal(self):
        return SignalObservation(
            signal_id="sig-1",
            source_id="public-service-listing",
            observed_at=NOW,
            actor_ref="resource-node-1",
            geography="Xuzhou",
            facts=(
                ObservedFact("offers_paid_offline_tasks", True, "offers local paid help"),
                ObservedFact("local_mobility_observed", True, "offers tasks requiring local travel"),
            ),
            explicit_capabilities=(
                ExplicitCapability("task.local_errand", "explicitly offers local errand help"),
            ),
            availability=AvailabilityState.ADVERTISED,
            permission=PermissionState.UNKNOWN,
        )

    def test_signal_extracts_explicit_and_rule_based_capabilities(self):
        rules = (
            CapabilityInferenceRule(
                "r-local-presence",
                (FactCondition("offers_paid_offline_tasks"),),
                "presence.local_execution",
                "offline paid-task offer implies a hypothesis of local execution presence",
            ),
            CapabilityInferenceRule(
                "r-local-mobility",
                (FactCondition("local_mobility_observed"),),
                "mobility.local",
                "source shows willingness to perform locally mobile tasks",
            ),
            CapabilityInferenceRule(
                "r-smartphone",
                (FactCondition("smartphone_available"),),
                "capture.mobile_photo_video",
                "only infer device capture when device availability is observed",
            ),
        )
        claims = extract_capability_claims(self._signal(), rules)
        by_key = {claim.capability_key: claim for claim in claims}

        self.assertEqual(by_key["task.local_errand"].evidence_status, EvidenceStatus.OBSERVED)
        self.assertEqual(by_key["presence.local_execution"].evidence_status, EvidenceStatus.INFERRED)
        self.assertEqual(by_key["mobility.local"].evidence_status, EvidenceStatus.INFERRED)
        self.assertNotIn("capture.mobile_photo_video", by_key)

    def test_advertised_capability_is_not_callable(self):
        claim = extract_capability_claims(self._signal())[0]
        self.assertFalse(claim.is_callable(NOW + timedelta(days=1), timedelta(days=30)))

    def test_real_confirmation_can_make_capability_callable(self):
        claim = extract_capability_claims(self._signal())[0]
        confirmed = confirm_capability(
            claim,
            confirmation_signal_id="confirmation-1",
            confirmed_at=NOW + timedelta(days=1),
            availability=AvailabilityState.CONFIRMED,
            permission=PermissionState.ALLOWED,
        )
        self.assertTrue(confirmed.is_callable(NOW + timedelta(days=2), timedelta(days=30)))
        self.assertFalse(confirmed.is_callable(NOW + timedelta(days=40), timedelta(days=30)))

    def test_capability_namespace_is_open_ended(self):
        signal = self._signal()
        rule = CapabilityInferenceRule(
            "new-rule-without-enum-change",
            (FactCondition("offers_paid_offline_tasks"),),
            "future.capability.never_seen_before",
            "new capability atoms do not require an enum migration",
        )
        keys = {x.capability_key for x in extract_capability_claims(signal, (rule,))}
        self.assertIn("future.capability.never_seen_before", keys)


class CapabilityCoverageTests(unittest.TestCase):
    def _bundle(self):
        return RequirementBundle(
            bundle_id="bundle-1",
            geography="Xuzhou",
            required_capabilities=(
                CapabilityRequirement("presence.local_execution"),
                CapabilityRequirement("mobility.local"),
            ),
        )

    def _claim(self, key, status, *, availability=AvailabilityState.UNKNOWN, permission=PermissionState.UNKNOWN):
        from src.live_resource_signals import CapabilityClaim

        return CapabilityClaim(
            actor_ref=f"resource-{key}",
            capability_key=key,
            evidence_status=status,
            source_signal_ids=(f"sig-{key}",),
            rationale="test evidence",
            last_observed_at=NOW,
            geography="Xuzhou",
            availability=availability,
            permission=permission,
        )

    def test_inferred_coverage_remains_hypothesis(self):
        claims = (
            self._claim("presence.local_execution", EvidenceStatus.INFERRED),
            self._claim("mobility.local", EvidenceStatus.INFERRED),
        )
        result = evaluate_coverage(claims, self._bundle(), as_of=NOW)
        self.assertEqual(result.state, CoverageState.HYPOTHESIS_COVERED)

    def test_observed_coverage_is_discovered_not_callable(self):
        claims = (
            self._claim("presence.local_execution", EvidenceStatus.OBSERVED),
            self._claim("mobility.local", EvidenceStatus.OBSERVED),
        )
        result = evaluate_coverage(claims, self._bundle(), as_of=NOW)
        self.assertEqual(result.state, CoverageState.DISCOVERED_COVERED)
        self.assertEqual(result.callable_capabilities, ())

    def test_only_confirmed_permitted_fresh_bundle_is_callable(self):
        claims = (
            self._claim(
                "presence.local_execution",
                EvidenceStatus.CONFIRMED,
                availability=AvailabilityState.CONFIRMED,
                permission=PermissionState.ALLOWED,
            ),
            self._claim(
                "mobility.local",
                EvidenceStatus.CONFIRMED,
                availability=AvailabilityState.COMMITTED,
                permission=PermissionState.ALLOWED,
            ),
        )
        result = evaluate_coverage(claims, self._bundle(), as_of=NOW + timedelta(days=1))
        self.assertEqual(result.state, CoverageState.CALLABLE_COVERED)

    def test_geography_mismatch_fails_closed(self):
        claim = self._claim("presence.local_execution", EvidenceStatus.OBSERVED)
        bundle = RequirementBundle(
            bundle_id="other-city",
            geography="Nanjing",
            required_capabilities=(CapabilityRequirement("presence.local_execution"),),
        )
        result = evaluate_coverage((claim,), bundle, as_of=NOW)
        self.assertEqual(result.state, CoverageState.INCOMPLETE)
        self.assertEqual(result.missing_capabilities, ("presence.local_execution",))


if __name__ == "__main__":
    unittest.main()
