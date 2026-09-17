# Connection Pressure Scan 018 — Acceptance Means Receiver State Transition

Observed: 2026-09-18

## Why this scan exists

Issue #143 already distinguishes `DELIVERED` from `ACCEPTED`. This scan makes that distinction operational.

> A deliverable is not accepted merely because it arrived. Acceptance requires an observable state transition on the receiver side, under an agreed acceptance interface.

This is not new architecture. It tightens the semantics of the existing value-flow state machine.

## Cross-domain evidence

### Automotive supplier introduction

A 2026 Jiangsu-listed automotive supplier describes OEM supplier introduction as a long buyer-controlled qualification process. A potential supplier may spend six to twelve months before being admitted to the OEM supplier system. Project introduction then moves through A/B/C/D sample states, OTS and PPAP approval. Only after these buyer approvals does the product enter mass production.

Source: https://static.cninfo.com.cn/finalpage/2026-08-28/1225518017.PDF

`SAMPLE_PRODUCED != BUYER_APPROVED`

`BUYER_APPROVED -> MASS_PRODUCTION_STATE`

### Equipment procurement

A Jiangsu environmental-monitoring equipment procurement requires delivery, installation, debugging and training, but states that installation is complete only when the instrument operates normally and the buyer confirms it. Training must also continue until the user's personnel can independently operate the instrument.

Source: https://sthjj.nanjing.gov.cn/ntshjbhj/202603/t20260330_5814883.html

The value is not the installation activity. The receiver must become capable of operating the equipment.

### Inspection / remediation

2026 procurement examples for fire/electrical inspection explicitly separate initial inspection from remediation and reinspection. A first report that identifies nonconformity is not the final accepted outcome. Payment and/or final acceptance are linked to remediation, reinspection and buyer/final-recipient recognition.

Sources:
- https://www.bidcenter.com.cn/news-429967607-1.html
- https://www.ixbang.com/bid/detail/0AED0FF2FB741D0D7C9B7826AD4B9859.html

`REPORT_ISSUED != COMPLIANT_STATE`

### Technology transfer

Scan 015 already captured a Jiangsu first-use-then-pay case: the enterprise paid RMB 700,000 only after the technology achieved the expected effect, then expanded follow-on cooperation to RMB 3 million.

Reference: `JS-TECH-PAY-AFTER-EVIDENCE-045`

Observed receiver-side transitions:

`UNCERTAIN -> OBSERVED_EFFECT -> PAYMENT -> EXPANDED_COOPERATION`

## Operational rule

### `DECISION_TRANSITION_ACCEPTANCE`

Before delivery, define:

1. **blocked receiver state** — what cannot happen now?
2. **target receiver state** — what becomes possible after successful delivery?
3. **decision owner** — who has authority to enact/declare the transition?
4. **acceptance evidence** — what observable fact proves the transition?
5. **causal boundary** — can the transition reasonably be linked to this exchange?

Examples of real acceptance transitions:

- candidate may independently perform the bounded task;
- buyer admits supplier/project into production;
- machine is operational and buyer signs off;
- regulator/platform/utility removes a blocking restriction;
- buyer releases payment;
- customer signs objective acceptance;
- test result changes a real shipment/listing/investment decision.

Not acceptance:

- email delivered;
- file uploaded;
- report issued;
- code handed over;
- meeting held;
- training attended;
- no complaint received;
- counterparty silence.

## Relationship to Scan 017

Scan 017 asks:

> what evidence will the receiver accept?

Scan 018 asks:

> once accepted, what receiver state actually changes?

Together:

`DELIVERABLE`
→ `RECEIVER-ACCEPTED EVIDENCE / RESULT`
→ `DECISION OR OPERATIONAL STATE TRANSITION`

Only then should the project use `ACCEPTED`.

## Field truth

Two employer capability-proof probes have been sent. Qualified human responses remain 0.

Their current state is therefore still `SENT`, not `ACCEPTED`, regardless of delivery status.

First external value flow remains unproven.

## Next search

Prioritize:

- a real Xuzhou workflow with explicit before/after receiver state and measurable cost;
- a successful remediation artifact that unlocked a previously blocked state;
- post-acceptance settlement and repeat signal;
- any qualified human reply from the two existing employer probes.
