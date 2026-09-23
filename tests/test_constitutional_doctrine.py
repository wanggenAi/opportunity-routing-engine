import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConstitutionalDoctrineTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_latent_value_doctrine_is_constitutional_and_connection_discovery_first(self):
        doctrine = self._read("docs/LATENT_VALUE_DOCTRINE.md")
        self.assertIn("CONSTITUTIONAL / LOCKED", doctrine)
        self.assertIn("The system does not begin with supply and demand", doctrine)
        self.assertIn("Commercial value does not have to pre-exist the discovery", doctrine)
        self.assertIn("RESOURCE–PSYCHOLOGY DISEQUILIBRIUM", doctrine)
        self.assertIn("UNMET / UNFORMED OUTCOME", doctrine)
        self.assertIn("CONNECTION-PRESSURE EVIDENCE", doctrine)
        self.assertIn("LATENT CONNECTION HYPOTHESIS", doctrine)
        self.assertIn("Counterfactual Exchange Design is downstream", doctrine)
        self.assertIn("CONNECTION INVENTION != CONNECTION DISCOVERY", doctrine)
        self.assertIn("COMPLEMENTARITY != LATENT CONNECTION", doctrine)
        self.assertIn("UNKNOWN != PASS", doctrine)
        self.assertIn("REALITY > COGNITION > SCHEMA", doctrine)
        self.assertIn("HYPOTHESIS CARDINALITY != EPISTEMIC RIGOR", doctrine)
        self.assertIn("STATE MACHINE != REQUIRED DISCOVERY PATH", doctrine)

    def test_structural_friction_discovery_is_constitutional_and_causal(self):
        principle = self._read("docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md")
        self.assertIn("CONSTITUTIONAL / LOCKED", principle)
        self.assertIn("SURFACE PHENOMENON / SURFACE FRICTION", principle)
        self.assertIn("STRUCTURAL FRICTION", principle)
        self.assertIn("STRUCTURAL FRICTION != MISSING EDGE", principle)
        self.assertIn("OBSERVED", principle)
        self.assertIn("INFERRED", principle)
        self.assertIn("EVIDENCED_STRUCTURE", principle)
        self.assertIn("BUYER COST FIRST != CONSTITUTION", principle)
        self.assertIn("DECISIVE_UNKNOWN / PROBE_ELIGIBLE", principle)

    def test_structural_friction_principle_requires_competing_causal_descent(self):
        principle = self._read("docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md")
        self.assertIn("Causal descent is recursive, not one jump", principle)
        self.assertIn("ONE PLAUSIBLE EXPLANATION", principle)
        self.assertIn("decision-useful, falsifiable causal frontier", principle)
        self.assertIn("INTERVENTION_RELEVANT_BOUNDARY", principle)
        self.assertIn("MULTI_CAUSAL_FRONTIER", principle)
        self.assertIn("BOUND SELECTION EVIDENCE", principle)
        self.assertIn("deeper search would **not** change the next decision", principle)
        self.assertIn("Psychology is one causal sensor, not a universal gate", principle)
        self.assertIn("INFERRED STRUCTURE", principle)
        self.assertIn("MAY GUIDE EXPLORATION", principle)
        self.assertIn("Do not fabricate a competing explanation solely to satisfy a schema", principle)
        self.assertIn("Hypothesis cardinality is not epistemic rigor", principle)

    def test_latent_connection_discovery_principle_is_constitutional(self):
        principle = self._read("docs/LATENT_CONNECTION_DISCOVERY_PRINCIPLE.md")
        self.assertIn("CONSTITUTIONAL / LOCKED", principle)
        self.assertIn("Discover latent connections that reality is already trying to form", principle)
        self.assertIn("CONNECTION INVENTION", principle)
        self.assertIn("CONNECTION DISCOVERY", principle)
        self.assertIn("CONNECTION_PRESSURE", principle)
        self.assertIn("HUMAN OUTREACH != PRIMARY DISCOVERY SENSOR", principle)
        self.assertIn("The goal is not to prohibit invention", principle)
        self.assertIn("现实已经踩出来的小径", principle)

    def test_formation_principle_requires_connection_pressure_before_validation(self):
        formation = self._read("docs/LATENT_VALUE_FORMATION_BRIDGE.md")
        self.assertIn("CONSTITUTIONAL DISCOVERY PRINCIPLE / LOCKED", formation)
        self.assertIn("DEMAND DISCOVERY != LATENT VALUE FORMATION", formation)
        self.assertIn("RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM", formation)
        self.assertIn("COMPETING LATENT / UNFORMED OUTCOME HYPOTHESES", formation)
        self.assertIn("RESOURCE_STATE_MISALIGNMENT_HYPOTHESIS", formation)
        self.assertIn("STRUCTURAL_FRICTION_EVIDENCED", formation)
        self.assertIn("LATENT_CONNECTION_EVIDENCED", formation)
        self.assertIn("canonical `MISSING_EDGE`", formation)
        self.assertIn("CONNECTION-PRESSURE EVIDENCE", formation)
        self.assertIn("LATENT CONNECTION HYPOTHESIS", formation)
        self.assertIn("Latent Connection Discovery precedes Counterfactual Exchange Mechanics", formation)
        self.assertIn("COMPLEMENTARITY != LATENT_CONNECTION", formation)
        self.assertIn("HUMAN OUTREACH != PRIMARY DISCOVERY SENSOR", formation)
        self.assertIn("WILLINGNESS TO PAY != TRANSACTION", formation)

    def test_agents_makes_formation_doctrine_binding_for_future_changes(self):
        agents = self._read("AGENTS.md")
        self.assertIn("docs/LATENT_VALUE_DOCTRINE.md", agents)
        self.assertIn("docs/STRUCTURAL_FRICTION_DISCOVERY_PRINCIPLE.md", agents)
        self.assertIn("docs/LATENT_VALUE_FORMATION_BRIDGE.md", agents)
        self.assertIn("Code serves the doctrine", agents)
        self.assertIn("Architectural dependency direction — LOCKED", agents)
        self.assertIn("A procurement feed is one sensor, not the business model", agents)
        self.assertIn("NeedSignal`, `ResourceSignal` and `BlockerSignal` are downstream", agents)
        self.assertIn("RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM", agents)
        self.assertIn("Reality-first adaptive cognition", agents)
        self.assertIn("REALITY > COGNITION > SCHEMA", agents)
        self.assertIn("Do not use fixed hypothesis counts as a substitute for causal rigor", agents)

    def test_formal_truth_preserves_connection_discovery_and_fail_closed_promotion(self):
        truth = self._read("docs/FORMAL_TRUTH.md")
        self.assertIn("Actor-First Regenerative Latent-Value Formation & Orchestration Engine", truth)
        self.assertIn("infer broadly, descend causally, compare explanations, and promote conservatively", truth)
        self.assertIn("Objective Resource Exists != Commercial Value Exists", truth)
        self.assertIn("Psychology Hypothesis != Demand", truth)
        self.assertIn("Surface Phenomenon != Structural Friction", truth)
        self.assertIn("Latent Outcome Hypothesis != Evidenced Latent Outcome", truth)
        self.assertIn("One Plausible Explanation != Structural Truth", truth)
        self.assertIn("One Latent Outcome Story != Evidenced Outcome Selection", truth)
        self.assertIn("Legacy STRANDING_BARRIER == Compatibility Alias for Canonical MISSING_EDGE", truth)
        self.assertIn("Psychology Evidence != Universal Formation Gate", truth)
        self.assertIn("Structural Friction Hypothesis != Evidenced Structural Friction", truth)
        self.assertIn("Buyer Cost First != Constitution", truth)
        self.assertIn("Connection Invention != Connection Discovery", truth)
        self.assertIn("Connection Hypothesis != Connection Pressure Evidence", truth)
        self.assertIn("Need / Resource / Blocker` is the current fail-closed evidence gate", truth)
        self.assertIn("Code must remain downstream of cognition and architecture", truth)
        self.assertIn("REALITY > COGNITION > SCHEMA", truth)
        self.assertIn("Schema Conformance != Truth", truth)
        self.assertIn("Hypothesis Cardinality != Epistemic Rigor", truth)

    def test_readme_surfaces_formation_as_repository_identity(self):
        readme = self._read("README.md")
        self.assertIn("Latent-Value Formation & Orchestration Engine", readme)
        self.assertIn("Demand does not have to exist first", readme)
        self.assertIn("RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM", readme)
        self.assertIn("COMPETING LATENT / UNFORMED OUTCOME HYPOTHESES", readme)
        self.assertIn("STRUCTURAL FRICTION HYPOTHESIS", readme)
        self.assertIn("Surface friction is not the discovery endpoint", readme)
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
        self.assertIn("RESOURCE / STATE / PSYCHOLOGY DISEQUILIBRIUM", discovery)
        self.assertIn("COMPETING LATENT / UNFORMED OUTCOME HYPOTHESES", discovery)
        self.assertIn("Counterfactual Exchange Design", discovery)
        self.assertIn("outcome_selection_evidence_refs", discovery)
        self.assertIn("deeper_search_would_change_decision", discovery)
        self.assertIn("src/causal_descent.py", discovery)
        self.assertIn("LATENT_CONNECTION_EVIDENCED", discovery)
        causal = self._read("src/causal_descent.py")
        self.assertIn("ONE_PLAUSIBLE_CAUSE_NE_STRUCTURAL_TRUTH", causal)
        self.assertIn(
            "CAUSAL_DESCENT_STOPS_AT_DEEPEST_DECISION_USEFUL_FALSIFIABLE_FRONTIER",
            causal,
        )
        self.assertIn("VALUE_DISCOVERY_PRECEDES_ORCHESTRATION", self._read("src/latent_value_discovery.py"))

    def test_architecture_cannot_collapse_back_to_explicit_matching(self):
        architecture = self._read("docs/ARCHITECTURE.md")
        self.assertIn("Constitutional parent: `docs/LATENT_VALUE_DOCTRINE.md`", architecture)
        self.assertIn("ENDOWMENT / STATE / CONSTRAINTS", architecture)
        self.assertIn("LATENT VALUE HYPOTHESIS", architecture)
        self.assertIn("COMPLEMENTARY ACTOR SEARCH", architecture)
        self.assertIn("outcome_selection_evidence_refs", architecture)
        self.assertIn("deeper_search_would_change_decision", architecture)
        self.assertIn("LatentValueHypothesis != Verified Resource", architecture)
        self.assertIn("The engine is not a database of buyers and suppliers", architecture)

    def test_resource_activation_thesis_treats_actor_roles_as_non_permanent(self):
        thesis = self._read("docs/RESOURCE_ACTIVATION_THESIS.md")
        self.assertIn("Actors are not fixed sides", thesis)
        self.assertIn("NEED_ACTOR` and `RESOURCE_OWNER` are roles, not identities", thesis)
        self.assertIn("The system's job is to discover the **exchange structure**", thesis)
        self.assertIn("LATENT_VALUE_HYPOTHESIS != VERIFIED RESOURCE", thesis)

    def test_clean_slate_epoch_blocks_historical_case_inheritance(self):
        agents = self._read("AGENTS.md")
        truth = self._read("docs/FORMAL_TRUTH.md")
        reset = self._read("data/commercial_reset_state.json")
        self.assertIn("GIT HISTORY != CANDIDATE POOL", agents)
        self.assertIn("PRE-RESET CASE != ACTIVE INPUT", agents)
        self.assertIn("ATTRACTION_FIELD_V1", truth)
        self.assertIn("ATTRACTION_SCAN_001", truth)
        self.assertIn("GIT_HISTORY_ONLY_NOT_ACTIVE_INPUT", reset)



    def test_strategic_drift_prevention_is_locked_and_machine_enforced(self):
        agents = self._read("AGENTS.md")
        attraction = self._read("docs/OPPORTUNITY_ATTRACTION_FIELD.md")
        guard = self._read("src/strategic_drift_guard.py")
        self.assertIn("Strategic drift prevention — LOCKED", agents)
        self.assertIn("LOCAL GATE COMPLIANCE != STRATEGIC ALIGNMENT", agents)
        self.assertIn("Regenerative field origin gate — LOCKED", attraction)
        self.assertIn("ONE ATTRACTIVE ASSET != REGENERATIVE VALUE FIELD", attraction)
        self.assertIn("ENFORCEMENT_START_SCAN = 142", guard)
        self.assertIn("recurring_missing_edge", guard)



if __name__ == "__main__":
    unittest.main()
