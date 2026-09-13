import tempfile
import unittest
from pathlib import Path

from src.capability_rule_registry import CapabilityRuleSpec, SQLiteCapabilityRuleRegistry
from src.live_resource_signals import FactCondition


class CapabilityRuleRegistryTests(unittest.TestCase):
    def _spec(self, version=1, *, active=False, capability_key="presence.local_execution"):
        return CapabilityRuleSpec(
            rule_id="local-presence",
            version=version,
            conditions=(FactCondition("offers_paid_offline_tasks", True),),
            capability_key=capability_key,
            rationale="public offline-task offer supports a local-presence hypothesis",
            active=active,
        )

    def test_rule_versions_are_append_only_and_auditable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.db"
            with SQLiteCapabilityRuleRegistry(path) as registry:
                registry.register(self._spec(version=1, active=True))
                registry.register(self._spec(version=2, active=False, capability_key="presence.local_task_execution"))
                self.assertEqual([x.version for x in registry.versions("local-presence")], [1, 2])
                self.assertTrue(registry.get("local-presence", 1).active)
                self.assertFalse(registry.get("local-presence", 2).active)

    def test_activating_new_version_deactivates_old_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityRuleRegistry(Path(tmp) / "rules.db") as registry:
                registry.register(self._spec(version=1, active=True))
                registry.register(self._spec(version=2, capability_key="presence.local_task_execution"))
                registry.activate("local-presence", 2)
                self.assertFalse(registry.get("local-presence", 1).active)
                self.assertTrue(registry.get("local-presence", 2).active)
                rules = registry.active_rules()
                self.assertEqual(len(rules), 1)
                self.assertEqual(rules[0].rule_id, "local-presence@v2")

    def test_same_version_cannot_be_silently_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityRuleRegistry(Path(tmp) / "rules.db") as registry:
                registry.register(self._spec(version=1))
                with self.assertRaisesRegex(ValueError, "different content"):
                    registry.register(self._spec(version=1, capability_key="different.capability"))

    def test_invalid_version_fails_closed(self):
        spec = self._spec(version=0)
        self.assertIn("invalid:version", spec.validate())


if __name__ == "__main__":
    unittest.main()
