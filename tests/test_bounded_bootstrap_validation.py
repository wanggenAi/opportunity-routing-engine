import unittest
from src.attraction_discovery import AttractionDiscoveryProfile,AttractionEvidence
from src.bounded_bootstrap_validation import BootstrapProbe,BootstrapState,bootstrap_probe_state

def ev(x): return (AttractionEvidence(source_id=x,claim=x),)
def profile(**o):
 v=dict(signal_id="F1",reality_pattern="field",a_actor="A",b_actor="B",candidate_bridge="bridge",
 a_voluntary_motion=3,b_voluntary_motion=3,state_dependent_value_jump=3,decision_window=3,bridge_compression=3,activation_ease=2,self_propulsion=3,operator_control=2,
 a_discoverability=3,b_discoverability=3,match_resolvability=3,action_gate_callability=2,a_population_replenishment=3,b_population_replenishment=3,recurring_connection_pressure=3,recurring_missing_edge=2,recurring_event_source=3,
 a_motion_evidence=ev("a"),b_motion_evidence=ev("b"),value_jump_evidence=ev("v"),decision_window_evidence=ev("d"),bridge_compression_evidence=ev("c"),activation_evidence=ev("act"),self_propulsion_evidence=ev("s"),operator_control_evidence=ev("o"),a_discoverability_evidence=ev("ad"),b_discoverability_evidence=ev("bd"),match_resolvability_evidence=ev("m"),action_gate_evidence=ev("g"),a_population_replenishment_evidence=ev("ar"),b_population_replenishment_evidence=ev("br"),recurring_connection_pressure_evidence=ev("p"),recurring_missing_edge_evidence=ev("e"),recurring_event_source_evidence=ev("r"))
 v.update(o); return AttractionDiscoveryProfile(**v)
def probe(**o):
 v=dict(explicit_task_used_as_discovery_seed=False,external_payment_signal_observed=True,bounded_output_and_acceptance=True,nonexpert_observation_only=True,lawful_access_or_permission_path=True,platform_team_or_delegation_path_confirmed=False,funded_payment_before_local_cost=False,optioned_replaceable_executor=False,executor_cost_bound=False,normalized_margin_positive=False,founder_free_labor_excluded_from_margin=True)
 v.update(o); return BootstrapProbe(**v)
class T(unittest.TestCase):
 def test_current_live_task_can_be_preflight_not_execution(self):
  self.assertIs(bootstrap_probe_state(profile(),probe()),BootstrapState.PREFLIGHT_READY)
 def test_gig_cannot_seed_the_formation(self):
  self.assertIs(bootstrap_probe_state(profile(),probe(explicit_task_used_as_discovery_seed=True)),BootstrapState.FORBIDDEN)
 def test_specialist_or_custody_task_is_not_first_bootstrap(self):
  self.assertIs(bootstrap_probe_state(profile(),probe(specialist_certification_required=True)),BootstrapState.FORBIDDEN)
  self.assertIs(bootstrap_probe_state(profile(),probe(custody_or_shipping_required=True)),BootstrapState.FORBIDDEN)
 def test_execution_requires_money_executor_and_margin_truth(self):
  ready=probe(platform_team_or_delegation_path_confirmed=True,funded_payment_before_local_cost=True,optioned_replaceable_executor=True,executor_cost_bound=True,normalized_margin_positive=True)
  self.assertIs(bootstrap_probe_state(profile(),ready),BootstrapState.EXECUTION_READY)
if __name__=="__main__": unittest.main()
