import unittest
from datetime import datetime, timedelta, timezone

from src.capability_coverage import CapabilityRequirement, RequirementBundle
from src.live_resource_signals import (
    AvailabilityState,
    CapabilityClaim,
    EvidenceStatus,
    PermissionState,
)
from src.resource_composition import (
    CompositionState,
    generate_composition_hypotheses,
)


NOW = datetime(2026, 9, 13, 9, 0, tzinfo=timezone.utc)


class ResourceCompositionTests(unittest.TestCase):
    def _bundle(self, *keys, geography="Xuzhou"):
        return RequirementBundle(
            bundle_id="bundle-1",
            geography=geography,
            required_capabilities=tuple(CapabilityRequirement(key) for key in keys),
        )

    def _claim(
        self,
        actor,
        key,
        status,
        *,
        geography="Xuzhou",
        availability=AvailabilityState.UNKNOWN,
        permission=PermissionState.UNKNOWN,
        observed_at=NOW,
        source_ids=None,
    ):
        return CapabilityClaim(
            actor_ref=actor,
            capability_key=key,
            evidence_status=status,
            source_signal_ids=tuple(source_ids or (f"sig-{actor}-{key}",)),
            rationale="test evidence",
            last_observed_at=observed_at,
            geography=geography,
            availability=availability,
            permission=permission,
        )

    def test_two_actors_can_form_discovered_composition(self):
        claims = (
            self._claim("actor-a", "presence.local_execution", EvidenceStatus.OBSERVED),
            self._claim("actor-b", "evidence.capture.photo_video", EvidenceStatus.OBSERVED),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution", "evidence.capture.photo_video"),
            as_of=NOW,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].actor_refs, ("actor-a", "actor-b"))
        self.assertTrue(result[0].is_multi_actor)
        self.assertEqual(result[0].state, CompositionState.DISCOVERED_COMPOSED)

    def test_inferred_leg_keeps_composition_hypothetical(self):
        claims = (
            self._claim("actor-a", "presence.local_execution", EvidenceStatus.OBSERVED),
            self._claim("actor-b", "mobility.local", EvidenceStatus.INFERRED),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution", "mobility.local"),
            as_of=NOW,
        )
        self.assertEqual(result[0].state, CompositionState.HYPOTHESIS_COMPOSED)

    def test_fresh_confirmed_permitted_legs_can_be_callable_composition(self):
        claims = (
            self._claim(
                "actor-a",
                "presence.local_execution",
                EvidenceStatus.CONFIRMED,
                availability=AvailabilityState.CONFIRMED,
                permission=PermissionState.ALLOWED,
            ),
            self._claim(
                "actor-b",
                "mobility.local",
                EvidenceStatus.CONFIRMED,
                availability=AvailabilityState.COMMITTED,
                permission=PermissionState.ALLOWED,
            ),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution", "mobility.local"),
            as_of=NOW + timedelta(days=1),
        )
        self.assertEqual(result[0].state, CompositionState.CALLABLE_COMPOSED)
        contributions = {item.capability_key: item for item in result[0].contributions}
        self.assertEqual(
            contributions["presence.local_execution"].callable_actor_refs,
            ("actor-a",),
        )

    def test_stale_confirmation_is_discovered_not_callable(self):
        claims = (
            self._claim(
                "actor-a",
                "presence.local_execution",
                EvidenceStatus.CONFIRMED,
                availability=AvailabilityState.CONFIRMED,
                permission=PermissionState.ALLOWED,
                observed_at=NOW - timedelta(days=60),
            ),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution"),
            as_of=NOW,
            max_age=timedelta(days=30),
        )
        self.assertEqual(result[0].state, CompositionState.DISCOVERED_COMPOSED)
        self.assertEqual(result[0].contributions[0].callable_actor_refs, ())

    def test_non_minimal_superset_is_not_emitted(self):
        claims = (
            self._claim("actor-a", "presence.local_execution", EvidenceStatus.OBSERVED),
            self._claim("actor-a", "mobility.local", EvidenceStatus.OBSERVED),
            self._claim("actor-b", "mobility.local", EvidenceStatus.OBSERVED),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution", "mobility.local"),
            as_of=NOW,
        )
        self.assertEqual(tuple(item.actor_refs for item in result), (("actor-a",),))

    def test_alternative_minimal_compositions_are_preserved_without_quality_ranking(self):
        claims = (
            self._claim("actor-a", "presence.local_execution", EvidenceStatus.OBSERVED),
            self._claim("actor-a", "mobility.local", EvidenceStatus.OBSERVED),
            self._claim("actor-b", "presence.local_execution", EvidenceStatus.OBSERVED),
            self._claim("actor-c", "mobility.local", EvidenceStatus.OBSERVED),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution", "mobility.local"),
            as_of=NOW,
        )
        self.assertEqual(
            tuple(item.actor_refs for item in result),
            (("actor-a",), ("actor-b", "actor-c")),
        )

    def test_geography_mismatch_is_excluded(self):
        claims = (
            self._claim(
                "actor-a",
                "presence.local_execution",
                EvidenceStatus.OBSERVED,
                geography="Nanjing",
            ),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution", geography="Xuzhou"),
            as_of=NOW,
        )
        self.assertEqual(result, ())

    def test_actor_limit_can_block_large_composition_without_inventing_coverage(self):
        claims = (
            self._claim("actor-a", "cap.a", EvidenceStatus.OBSERVED),
            self._claim("actor-b", "cap.b", EvidenceStatus.OBSERVED),
            self._claim("actor-c", "cap.c", EvidenceStatus.OBSERVED),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("cap.a", "cap.b", "cap.c"),
            as_of=NOW,
            max_actors=2,
        )
        self.assertEqual(result, ())

    def test_source_provenance_is_aggregated(self):
        claims = (
            self._claim(
                "actor-a",
                "presence.local_execution",
                EvidenceStatus.OBSERVED,
                source_ids=("sig-2", "sig-1"),
            ),
        )
        result = generate_composition_hypotheses(
            claims,
            self._bundle("presence.local_execution"),
            as_of=NOW,
        )
        self.assertEqual(result[0].source_signal_ids, ("sig-1", "sig-2"))
        self.assertEqual(
            result[0].contributions[0].source_signal_ids,
            ("sig-1", "sig-2"),
        )

    def test_naive_datetime_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            generate_composition_hypotheses(
                (),
                self._bundle("presence.local_execution"),
                as_of=datetime(2026, 9, 13, 9, 0),
            )


if __name__ == "__main__":
    unittest.main()
