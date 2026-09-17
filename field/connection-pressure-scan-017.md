# Connection Pressure Scan 017 — Evidence Acceptance Gap

Observed: 2026-09-18

## Why this matters

Earlier scans asked whether reality is legible and verifiable. This scan adds a stricter operational check:

> evidence can exist and still fail to move the next actor.

The issue is sometimes not missing expertise or missing evidence, but a mismatch between the evidence produced and the evidence schema accepted by the decision owner.

This deepens `VERIFIABILITY_TRANSFORMATION` and `BOUNDARY_TRANSLATION`; it is not a new ontology or a generic compliance-consulting thesis.

## Xuzhou event evidence

### Third-party electrical inspection did not unlock reconnection

The Xuzhou enterprise-service request stream includes an enterprise whose power was cut after the utility attributed a grid impact to enterprise electrical equipment. The enterprise then used a third-party inspection organization, which reportedly found no fault point, but the utility still had not restored power when the request was published.

Source: https://xzsme.js.cn/

`THIRD_PARTY_VERIFICATION != DECISION_OWNER_ACCEPTANCE`

The public stream does not expose the final remediation step, so no resolution is inferred.

### Imported pressure-vessel certificate existed but was unusable for registration

The same request stream includes an enterprise with six imported pressure vessels that could not be registered because the available factory inspection certificates did not satisfy domestic safety-technical-specification requirements.

Source: https://xzsme.js.cn/

`CERTIFICATE_EXISTS != ACCEPTABLE_CERTIFICATE`

### Outbound-investment state mismatch blocked bank execution

Another enterprise reported that an overseas-project transfer could not proceed because the filed/verified record did not represent the in-kind-investment structure involved in the real transaction. The enterprise sought to change the representation to monetary funds.

Source: https://xzsme.js.cn/

`REAL_TRANSACTION_STATE != FILED_STATE != BANK-ACTIONABLE_STATE`

## Why this is structural rather than anecdotal

Jiangsu's Inspection and Testing Regulation makes evidence acceptance explicitly structured: test basis, data/results, sample acquisition, authorized signer, institution seal, qualification marks and subcontracting status all matter.

2026-published national supervision results likewise show that reports can fail because they are outside recognized capability scope, use expired qualification, lack proper signing/seals, use the wrong method or cannot be supported by original records.

The national 2026 `one-list / one-database` rule further distinguishes between a test an institution may technically perform and a report that may carry formal CMA qualification effect.

Sources:
- https://www.jsrd.gov.cn/qwfb/sjfg/202510/t20251015_1221350.shtml
- https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/rkjcs/art/2026/art_3fb4543dd46e481fab1098f6aaca5e9f.html
- https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/rkjcs/art/2026/art_ea608a4306a34b8bb1f3c548a91cffa8.html

## Refined rule

### `EVIDENCE_ACCEPTANCE_GAP`

When an Actor already has a report, certificate, filing, test result or other proof but the workflow remains blocked, do **not** immediately route them to another provider.

First identify:

1. the actual decision owner;
2. the exact accepted evidence schema;
3. required provenance / qualification / standard / method;
4. identity and authorized-signature requirements;
5. chain of custody / source-data requirements;
6. cross-system state consistency;
7. the artifact used in the last successful comparable case.

Then distinguish:

`missing evidence`

from

`existing evidence not accepted`

from

`evidence accepted but decision still negative`.

These are different failure modes.

## Boundaries

This scan does **not** prove:

- demand for generic regulatory consulting;
- demand for another testing provider;
- a paid evidence-translation market;
- that any of the Xuzhou requests were ultimately solved in a particular way.

The public request stream exposes the blockage, not the final accepted artifact.

## Field truth

Two direct employer capability-proof probes are sent. Qualified human responses remain 0.

First external value flow remains unproven.

## Next search

Highest-information next evidence:

- repeated low-permission workflows where evidence exists but counterpart acceptance fails;
- the exact remediation artifact that unlocked one real event;
- current forced-external-routing events with explicit `local capability absent` evidence;
- a workflow where accepted-evidence requirements can be made legible without becoming a regulated intermediary.
