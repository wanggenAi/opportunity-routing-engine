import tempfile
import unittest
from pathlib import Path

from src.requirement_bundle_registry import (
    RequirementBundleSpec,
    SQLiteRequirementBundleRegistry,
)


class RequirementBundleRegistryBoundaryTests(unittest.TestCase):
    def _spec(self, *, capabilities=("cap.a", "cap.b"), active=False):
        return RequirementBundleSpec(
            bundle_id="bundle-1",
            version=1,
            required_capabilities=capabilities,
            geography="Xuzhou",
            source_ref="opportunity:opp-1",
            rationale="bounded capability decomposition",
            active=active,
        )

    def test_list_and_tuple_are_same_immutable_version_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteRequirementBundleRegistry(Path(tmp) / "requirements.db") as registry:
                registry.register(self._spec(capabilities=["cap.a", "cap.b"], active=False))
                registry.register(self._spec(capabilities=("cap.a", "cap.b"), active=True))

                stored = registry.get("bundle-1", 1)
                self.assertIsNotNone(stored)
                self.assertEqual(tuple(stored.required_capabilities), ("cap.a", "cap.b"))
                self.assertTrue(stored.active)
                self.assertEqual(registry.active("bundle-1").version, 1)

    def test_active_selection_is_not_immutable_version_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteRequirementBundleRegistry(Path(tmp) / "requirements.db") as registry:
                registry.register(self._spec(active=True))
                registry.register(self._spec(active=False))
                self.assertTrue(registry.get("bundle-1", 1).active)

    def test_string_is_not_accepted_as_capability_sequence(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteRequirementBundleRegistry(Path(tmp) / "requirements.db") as registry:
                with self.assertRaisesRegex(ValueError, "invalid:required_capabilities"):
                    registry.register(self._spec(capabilities="cap.a"))

    def test_non_string_capability_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteRequirementBundleRegistry(Path(tmp) / "requirements.db") as registry:
                with self.assertRaisesRegex(ValueError, "missing:required_capabilities"):
                    registry.register(self._spec(capabilities=("cap.a", 7)))


if __name__ == "__main__":
    unittest.main()
