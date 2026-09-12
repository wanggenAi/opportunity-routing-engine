import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConstitutionalDoctrineTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_latent_value_doctrine_is_constitutional_and_actor_first(self):
        doctrine = self._read("docs/LATENT_VALUE_DOCTRINE.md")
        self.assertIn("CONSTITUTIONAL / LOCKED", doctrine)
        self.assertIn("The system does not begin with supply and demand", doctrine)
        self.assertIn("LATENT_VALUE_HYPOTHESIS", doctrine)
        self.assertIn("COMPLEMENTARY_ACTOR", doctrine)
        self.assertIn("A source adapter is an **observer**, not the strategy", doctrine)
        self.assertIn("WORLD MODEL / DOCTRINE", doctrine)
        self.assertIn("POTENTIAL VALUE != PROVEN VALUE", doctrine)
        self.assertIn("UNKNOWN != PASS", doctrine)

    def test_agents_makes_doctrine_binding_for_future_changes(self):
        agents = self._read("AGENTS.md")
        self.assertIn("docs/LATENT_VALUE_DOCTRINE.md", agents)
        self.assertIn("Code serves the doctrine", agents)
        self.assertIn("Architectural dependency direction — LOCKED", agents)
        self.assertIn("A procurement feed is one sensor, not the business model", agents)
        self.assertIn("NeedSignal`, `ResourceSignal` and `BlockerSignal` are evidence projections", agents)

    def test_formal_truth_preserves_broad_discovery_and_fail_closed_promotion(self):
        truth = self._read("docs/FORMAL_TRUTH.md")
        self.assertIn("Actor-First Regenerative Latent-Value Orchestration Engine", truth)
        self.assertIn("The engine must **discover boldly and promote conservatively**", truth)
        self.assertIn("Potential Value != Proven Value", truth)
        self.assertIn("Complementarity != Transactionability", truth)
        self.assertIn("Need / Resource / Blocker` is the current fail-closed evidence gate", truth)
        self.assertIn("Code must remain downstream of cognition and architecture", truth)

    def test_architecture_cannot_collapse_back_to_explicit_matching(self):
        architecture = self._read("docs/ARCHITECTURE.md")
        self.assertIn("Constitutional parent: `docs/LATENT_VALUE_DOCTRINE.md`", architecture)
        self.assertIn("ENDOWMENT / STATE / CONSTRAINTS", architecture)
        self.assertIn("LATENT VALUE HYPOTHESIS", architecture)
        self.assertIn("COMPLEMENTARY ACTOR SEARCH", architecture)
        self.assertIn("LatentValueHypothesis != Verified Resource", architecture)
        self.assertIn("The engine is not a database of buyers and suppliers", architecture)

    def test_resource_activation_thesis_treats_actor_roles_as_non_permanent(self):
        thesis = self._read("docs/RESOURCE_ACTIVATION_THESIS.md")
        self.assertIn("Actors are not fixed sides", thesis)
        self.assertIn("NEED_ACTOR` and `RESOURCE_OWNER` are roles, not identities", thesis)
        self.assertIn("The system's job is to discover the **exchange structure**", thesis)
        self.assertIn("LATENT_VALUE_HYPOTHESIS != VERIFIED RESOURCE", thesis)


if __name__ == "__main__":
    unittest.main()
