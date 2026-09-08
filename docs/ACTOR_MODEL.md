# Actor Model

## Purpose

The Opportunity Routing Engine is actor-first. It must not assume that the person with the problem, the beneficiary, the payer, and the capability provider are the same entity.

This document defines the canonical actor-role model used across research, scoring, experiments and future code.

## 1. Actor

An `Actor` is any person, household, group, organization, institution, or resource-owning entity relevant to an opportunity.

Examples:

- student;
- graduate;
- unemployed worker;
- flexible worker;
- single young adult;
- tenant;
- parent;
- child;
- elderly person;
- caregiver;
- pet owner;
- merchant;
- skilled worker;
- farmer;
- freelancer;
- enterprise;
- manufacturer;
- school;
- community;
- government body;
- overseas buyer/consumer;
- owner of idle time, skill, equipment, inventory, vehicle, space or data.

## 2. Canonical roles

### `NEED_ACTOR`
Experiences the friction or unmet need.

### `BENEFICIARY`
Receives the solved outcome.

### `PAYER`
Provides money or other economically meaningful consideration.

### `CAPABILITY_PROVIDER`
Provides skill, labor, product, software, AI, service, equipment, information or other capability.

### `RESOURCE_OWNER`
Controls a scarce or idle resource used in the transaction.

### `SPONSOR`
Pays or subsidizes while another actor receives the value.

### `ORCHESTRATOR`
Defines requirements, routes capability, coordinates, creates trust/verification, and records outcomes.

One actor may hold multiple roles.

## 3. Common transaction patterns

### Direct C2C
```text
Individual need actor/payer
        ↓
Individual capability provider
```

### B2C
```text
Individual need actor/payer
        ↓
Business/provider capability
```

### C2B
```text
Enterprise need actor/payer
        ↓
Individual capability provider
```

### B2B
```text
Organization need actor/payer
        ↓
Organization capability provider
```

### Family-sponsored
```text
Elderly/child beneficiary
        ↑
Family-member payer
        ↓
Capability provider
```

### Institution-sponsored
```text
Resident/student/public beneficiary
        ↑
Institution payer
        ↓
Provider/network
```

### Resource exchange
```text
Actor with unmet need
        ↓
Owner of idle asset/time/space/inventory
```

### Multi-sided
```text
Need actor
   ↘
    Orchestrator / platform
   ↗        ↖
Payer      Capability provider
```

## 4. Actor record schema

Recommended minimum fields:

```text
actor_id:
actor_type:
segment:
geography:
context:
current_behavior:
constraints:
trust_requirements:
ability_to_pay:
observed_payment_behavior:
resource_or_capability:
source:
observed_at:
verification_status:
confidence:
```

Do not store unnecessary sensitive personal data.

## 5. Opportunity role map

Every promoted opportunity should include:

```text
Need actor:
Beneficiary:
Payer:
Capability provider:
Resource owner (if any):
Sponsor (if any):
Orchestrator value:
Transaction type:
```

If payer is `UNKNOWN`, the opportunity cannot advance to serious transaction testing.

## 6. Actor-first scan rule

Broad scans must not begin from only one payer type.

For Xuzhou-first research, actively look for change and friction among:

1. university students / graduates;
2. young workers / flexible workers;
3. single / renting adults;
4. parents / households;
5. elderly / caregivers / adult children;
6. pet owners;
7. value-conscious consumers;
8. skilled workers / farmers / service workers;
9. merchants / self-employed operators;
10. SMEs / manufacturers;
11. institutions / communities;
12. holders of idle personal or organizational resources.

## 7. Governing principle

**Do not ask only “who has money?” Ask “who has the need, who benefits, who loses if it stays unsolved, who can pay, and who can solve it?”**
