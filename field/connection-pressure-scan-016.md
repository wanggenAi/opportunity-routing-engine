# Connection Pressure Scan 016 — Control Continuity After Transfer

Observed: 2026-09-18

## Why this scan exists

Scan 014 established `RIGHTS_BUNDLE_COMPLETENESS`: a connected/digital asset can have physical title while debt, account, software, service or remote-control rights remain unresolved.

This scan tightens that rule:

> a transfer is not operationally complete merely because the receiver obtained the asset; it is complete only when prior actors no longer retain unauthorized superior control channels and the receiver can continue normal operation independently.

This is a refinement of existing rights/verifiability doctrine, not a new ontology and not an account-transfer business thesis.

## Real failures

### Xuzhou used EV

A buyer paid and completed vehicle title transfer, but the vehicle App/account could not be transferred because an unresolved finance/mortgage restriction remained. Remote-lock risk and impaired intelligent-control use survived the title transfer.

Source: https://szb.cnxz.com.cn/dscb/pad/con/202607/10/content_52566.html

### Jiangsu virtual account recovery

A 2026 Kunshan case involved a game account sold for money and repeatedly recovered by the original holder through password-reset / appeal channels, then resold.

Source: https://www.jsfy.gov.cn/article/107745.html

The important fact is not the game industry. It is that the transferor's recovery identity remained stronger than the transferee's apparent possession.

### Enterprise privileged access after employee exit

A 2026 Nantong case involved a former network technician retaining highest-privilege credentials after departure, remotely deleting core data and backups and disrupting enterprise operations.

Source: https://www.jsfy.gov.cn/article/106872.html

`EMPLOYMENT_EXIT != PRIVILEGE_REVOCATION`

### Platform identity / authenticated account rights

Jiangsu court material on authenticated platform accounts and stores shows that private operation/transfer agreements do not erase platform identity, certification and user-agreement constraints. Login/use possession can differ from the platform-recognized right/obligation holder.

Sources:
- https://www.jsfy.gov.cn/article/107602.html
- https://www.jsfy.gov.cn/article/107547.html

### Software right without operable software

A 2026 judicial auction of software copyright disclosed that the administrator had not taken custody of the registration certificate, software, source code or related materials and would deliver the right as-is.

Source: https://pccz.court.gov.cn/pcajxxw/pcgg/ggxq?id=2298783D79848839D85713D3DE17B896

`LEGAL_RIGHT != OPERABLE_ASSET`

## Search-rule refinement

### `CONTROL_CONTINUITY_AFTER_TRANSFER`

For any connected, digital or software-dependent asset, inspect:

1. authoritative identity / registered owner;
2. platform or OEM account binding;
3. highest-privilege administrators;
4. password reset / recovery / appeal channels;
5. remote lock/delete/control authority;
6. API, signing and encryption keys;
7. source code / executable / deployment assets;
8. data ownership and access;
9. software/service entitlement;
10. warranty, maintenance and vendor support rights.

Then ask:

> if the old owner, employee, vendor or operator disappears or becomes hostile tomorrow, can the receiver still operate the asset normally?

If not, value flow is incomplete.

### `RESIDUAL_CONTROL_CHECK`

`nominal transfer or exit`
+
`old actor retains superior technical/recovery channel`
→
`receiver control remains revocable`

This is connection-pressure evidence only when the failure is repeated/bounded and creates measurable loss, delay, downtime or dispute.

## What this does NOT prove

- It does not prove demand for an account-escrow platform.
- It does not prove demand for a generic IT-offboarding service.
- It does not prove used-EV buyers will pay for a checklist.
- It does not turn court cases into market demand.

The cases only prove that **usable control can fail to migrate even when nominal transfer appears complete**.

## Field state

Two employer capability-proof probes are currently sent; qualified human responses remain 0.

No additional employer outreach is added for volume.

First external value flow remains unproven.

## Next search

Highest-information next targets:

1. a named Xuzhou SME currently exposed to vendor/admin handover risk;
2. a connected-asset transfer where control migration creates measurable time/cost;
3. the current forced-external-routing ledger;
4. small-batch/heterogeneous material residues left after mature industrial symbiosis.
