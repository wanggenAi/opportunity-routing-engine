# Capability Unit Template

Use this template whenever a recurring function is routed to a person, company, AI/software system, asset/resource owner or channel.

## Identity

```text
capability_unit_id:
transaction_id:
capability_name:
provider_id_anonymized:
provider_class:
```

## Contractible function

```text
purpose:
input:
required_output:
acceptance_criteria:
proof_required_before_assignment:
deadline_sla:
dependencies:
```

## Economics

```text
price_model:
payout_amount_or_formula:
payout_condition:
who_funds_payout:
refund_clawback_condition:
```

## Trust / risk

```text
trust_requirements:
safety_legal_boundary:
data_access_boundary:
responsibility_boundary:
```

## Replacement

```text
fallback_provider_or_route:
replacement_trigger:
maximum_rework_before_replacement:
handoff_artifacts_required:
```

## Outcome

```text
assigned_at:
delivered_at:
accepted: YES / NO / PARTIAL
revision_count:
actual_payout:
late: YES / NO
replacement_used: YES / NO
failure_reason:
reliability_learning:
```

## Rule

A skill claim is not enough. The capability unit is defined by **accepted output under explicit constraints and economics**.
