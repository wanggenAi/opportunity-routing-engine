"""Fail-closed gate for the first 1-3 transaction probes of an already-evidenced field.

A live gig can validate transaction truth. It may not become the discovery ontology.
Temporary operator coordination is allowed for learning; recurring operator dependence
is not.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from src.attraction_discovery import AttractionBeaconState, AttractionDiscoveryProfile, attraction_beacon_state

class BootstrapState(str, Enum):
    FORBIDDEN="FORBIDDEN"
    PREFLIGHT_READY="PREFLIGHT_READY"
    EXECUTION_READY="EXECUTION_READY"

@dataclass(frozen=True)
class BootstrapProbe:
    explicit_task_used_as_discovery_seed: bool
    external_payment_signal_observed: bool
    bounded_output_and_acceptance: bool
    nonexpert_observation_only: bool
    lawful_access_or_permission_path: bool
    platform_team_or_delegation_path_confirmed: bool
    funded_payment_before_local_cost: bool
    optioned_replaceable_executor: bool
    executor_cost_bound: bool
    normalized_margin_positive: bool
    founder_free_labor_excluded_from_margin: bool
    target_state_requires_recurring_founder_sales: bool=False
    target_state_requires_recurring_founder_delivery: bool=False
    founder_manufactured_demand: bool=False
    specialist_certification_required: bool=False
    custody_or_shipping_required: bool=False

def bootstrap_probe_state(profile: AttractionDiscoveryProfile, probe: BootstrapProbe) -> BootstrapState:
    if attraction_beacon_state(profile) is not AttractionBeaconState.HIGH_ATTRACTION_BEACON:
        return BootstrapState.FORBIDDEN
    if probe.explicit_task_used_as_discovery_seed or probe.founder_manufactured_demand:
        return BootstrapState.FORBIDDEN
    if probe.target_state_requires_recurring_founder_sales or probe.target_state_requires_recurring_founder_delivery:
        return BootstrapState.FORBIDDEN
    if probe.specialist_certification_required or probe.custody_or_shipping_required:
        return BootstrapState.FORBIDDEN
    if not (probe.external_payment_signal_observed and probe.bounded_output_and_acceptance and probe.nonexpert_observation_only and probe.lawful_access_or_permission_path):
        return BootstrapState.FORBIDDEN
    execution_gates=(
        probe.platform_team_or_delegation_path_confirmed,
        probe.funded_payment_before_local_cost,
        probe.optioned_replaceable_executor,
        probe.executor_cost_bound,
        probe.normalized_margin_positive,
        probe.founder_free_labor_excluded_from_margin,
    )
    return BootstrapState.EXECUTION_READY if all(execution_gates) else BootstrapState.PREFLIGHT_READY
