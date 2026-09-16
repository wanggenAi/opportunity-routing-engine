import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConstitutionalDoctrineTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_latent_value_doctrine_is_constitutional_and_formation_first(self):
        doctrine = self._read("docs/LATENT_VALUE_DOCTRINE.md")
        self.assertIn("CONSTITUTIONAL / LOCKED", doctrine)
        self.assertIn("The system does not begin with supply and demand", doctrine)
        self.assertIn("Commercial value does not have to pre-exist the discovery", doctrine)
        self.assertIn("RESOURCE–PSYCHOLOGY DISEQUILIBRIUM", doctrine)
        self.assertIn("UNMET / UNFORMED OUTCOME", doctrine)
        self.assertIn("COUNTERFACTUAL EXCHANGE DESIGN", doctrine)
        self.assertIn("DEMAND DISCOVERY != LATENT VALUE FORMATION", doctrine)
        self.assertIn("OBJECTIVE RESOURCE EXISTS != COMMERCIAL VALUE EXISTS", doctrine)
        self.assertIn("UNKNOWN != PASS", doctrine)

    def test_formation_principle_is_constitutional_and_upstream_of_demand(self):
        formation = self._read("docs/LATENT_VALUE_FORMATION_BRIDGE.md")
        self.assertIn("CONSTITUTIONAL DISCOVERY PRINCIPLE / LOCKED", formation)
        self.assertIn("DEMAND DISCOVERY != LATENT VALUE FORMATION", formation)
        self.assertIn("RESOURCE–PSYCHOLOGY DISEQUILIBRIUM", formation)
        self.assertIn("UNMET / UNFORMED OUTCOME HYPOTHESIS", formation)
        self.assertIn("COUNTERFACTUAL EXCHANGE DESIGN", formation)
        self.assertIn("ONLY IF REALITY SUPPORTS IT: NEW COMMERCIAL STRUCTURE", formation)
        self.assertIn("PSYCHOLOGY HYPOTHESIS != DEMAND", formation)
        self.assertIn("WILLINGNESS TO PAY != TRANSACTION", formation)

    def test_agents_makes_formation_doctrine_binding_for_future_changes(self):
        agents = self._read("AGENTS.md")
        self.assertIn("docs/LATENT_VALUE_DOCTRINE.md", agents)
        self.assertIn("docs/LATENT_VALUE_FORMATION_BRIDGE.md", agents)
        self.assertIn("Code serves the doctrine", agents)
        self.assertIn("Architectural dependency direction — LOCKED", agents)
        self.assertIn("A procurement feed is one sensor, not the business model", agents)
        self.assertIn("NeedSignal`, `ResourceSignal` and `BlockerSignal` are downstream", agents)
        self.assertIn("RESOURCE–PSYCHOLOGY DISEQUILIBRIUM", agents)
        self.assertIn("Counterfactual Exchange Design rule", agents)

    def test_formal_truth_preserves_formation_and_fail_closed_promotion(self):
        truth = self._read("docs/FORMAL_TRUTH.md")
        self.assertIn("Actor-First Regenerative Latent-Value Formation & Orchestration Engine", truth)
        self.assertIn("infer boldly and promote conservatively", truth)
        self.assertIn("Objective Resource Exists != Commercial Value Exists", truth)
        self.assertIn("Psychology Hypothesis != Demand", truth)
        self.assertIn("Counterfactual Exchange != Accepted Exchange", truth)
        self.assertIn("Need / Resource / Blocker` is the current fail-closed evidence gate", truth)
        self.assertIn("Code must remain downstream of cognition and architecture", truth)

    def test_readme_surfaces_formation_as_repository_identity(self):
        readme = self._read("README.md")
        self.assertIn("Latent-Value Formation & Orchestration Engine", readme)
        self.assertIn("Demand does not have to exist first", readme)
        self.assertIn("RESOURCE–PSYCHOLOGY DISEQUILIBRIUM", readme)
        self.assertIn("UNMET / UNFORMED OUTCOME HYPOTHESIS", readme)
        self.assertIn("COUNTERFACTUAL EXCHANGE DESIGN", readme)
        self.assertIn("Resource Imbalance Engine — downstream truth gate", readme)

    def test_psychology_is_causal_formation_input_not_pain_point_mining(self):
        psychology = self._read("docs/PSYCHOLOGY_BEHAVIOR_TRACKER.md")
        self.assertIn("CANONICAL VALUE-FORMATION SENSOR", psychology)
        self.assertIn("The real causal question", psychology)
        self.assertIn("Resource–Psychology Disequilibrium", psychology)
        self.assertIn("Contradiction is first-class signal", psychology)
        self.assertIn("UNMET / UNFORMED OUTCOME", psychology)
        self.assertIn("PSYCHOLOGY HYPOTHESIS != DEMAND", psychology)

    def test_discovery_engine_rejects_explicit_demand_as_core_identity(self):
        discovery = self._read("docs/DISCOVERY_ENGINE.md")
        self.assertIn("Latent Value Formation Radar", discovery)
        self.assertIn("Two candidate classes — do not mix them", discovery)
        self.assertIn("EXPLICIT_DEMAND_EXECUTION != CORE_LATENT_VALUE_FORMATION", discovery)
        self.assertIn("RESOURCE–PSYCHOLOGY DISEQUILIBRIUM", discovery)
        self.assertIn("UNMET / UNFORMED OUTCOME HYPOTHESIS", discovery)
        self.assertIn("Counterfactual Exchange Design", discovery)
        self.assertIn("VALUE_DISCOVERY_PRECEDES_ORCHESTRATION", self._read("src/latent_value_discovery.py"))

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

    def test_cycle_002_no_longer_ranks_existing_outsourcing_as_core(self):
        result = self._read("docs/results/DISCOVERY_CYCLE_002_PRELIMINARY_2026-09-12.md")
        money = self._read("docs/results/DISCOVERY_CYCLE_002_MONEY_CAPTURE_2026-09-12.md")
        self.assertIn("CORE LATENT-VALUE SEARCH ONLY", result)
        self.assertIn("Tacit industrial knowledge", result)
        self.assertIn("Fragmented small demand", result)
        self.assertIn("DOWNGRADED / EXPLICIT_DEMAND_EXECUTION / NOT CORE DISCOVERY", money)
        self.assertIn("A route can be profitable and still be architecturally secondary", money)


if __name__ == "__main__":
    unittest.main()
