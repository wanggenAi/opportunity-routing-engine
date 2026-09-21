# Attraction Scan 063 — Persistent workaround after incumbent adoption

**As of:** 2026-09-21  
**Epoch:** `ATTRACTION_FIELD_V1`  
**Result:** 0 commercial promotions, 0 new retained research formations, `FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN`.

## Purpose

Scans 061 and 062 established that buyer-side workaround evidence is a strong pain sensor but weak white-space evidence by itself. Scan 063 raises the observation floor: each formation begins with a buyer already using, paying for, or having tried a relevant incumbent while the workaround persists.

```text
ACTIVE / PAID INCUMBENT
+ PERSISTENT BUYER WORKAROUND
→ ISOLATE RESIDUAL EDGE
→ CHECK CURRENT NATIVE ROADMAP / MIGRATION
→ CHECK PARTNER ECOSYSTEM
→ CHECK WHETHER RESIDUAL IS CONFIGURATION / DATA / GOVERNANCE / HUMAN JUDGMENT
→ FAIL CLOSED
```

## Examined formations

### 063-F1 — Salesforce/Outlook activity capture residual
A current Salesforce buyer reports cycling through native Outlook integration, Einstein Activity Capture, Cirrus Insight, BCC and other plugins, then testing middleware because automatic inbound/outbound logging, matching and reportability still do not line up cleanly.

Salesforce is actively migrating EAC to **Sync Email as Salesforce Activity**, storing captured email in standard Activity/EmailMessage records usable by standard reports, workflows, APIs and customizable matching flows.

**Verdict:** DEMOTED — powerful residual signal, but the platform is actively absorbing the exact gap and third-party integration supply is already mature.

### 063-F2 — Jira Advanced Plans portfolio capacity shadow Excel
A PMO using Jira Data Center Advanced Roadmaps says it rebuilds quarterly capacity rollups in Excel because mixed structures across many projects cause trust to deteriorate rapidly.

Jira Plans already owns cross-team capacity, dependencies, scenarios and program-board planning, and Atlassian documents practical limits and configuration requirements around teams/work sources/plan size.

**Verdict:** DEMOTED — residual is configuration, scale and data-trust/portfolio-judgment rather than a distinct external machine control asset.

### 063-F3 — Workday Financials Excel reporting residual
Current Workday Financials practitioners describe recurring period-end manual effort and control friction around Excel-oriented reporting.

Workday's own OfficeConnect is an Excel add-in that directly queries Workday financial-model data and refreshes reports inside Excel.

**Verdict:** DEMOTED — the official platform already owns the Excel bridge; residual value is security/configuration and finance-modeling judgment.

### 063-F4 — ServiceNow role-aware guidance maintenance
A current ServiceNow administrator manually maintains guidance whenever forms and workflows change; role-specific views make static guidance brittle, and the administrator has already rejected Guided Tours as insufficient.

ServiceNow's 2026 Dynamic Guidance explicitly targets real-time, contextual in-workflow help and complements Guided Tours. External digital-adoption tools also target role-aware overlays.

**Verdict:** DEMOTED — native roadmap and external adoption-tool ecosystem are actively absorbing the edge; remaining work includes OCM and instance-specific configuration.

### 063-F5 — Epic Cogito ad-hoc SQL → Excel analyst layer
A current analyst at a large Epic health system reports spending much of the job querying Epic reporting stores in SQL and exporting results to Excel for clinicians and finance users despite Cogito/Caboodle/Clarity certification.

Epic's Cogito stack already includes Reporting Workbench, Radar and SlicerDicer self-service analytics, and current health systems provide end-user training around these tools.

**Verdict:** DEMOTED — residual is complex semantics, governance, access and bespoke analysis, not a normalized founder-independent machine layer.

### 063-F6 — OPERA Cloud front-desk check-in deferral
A current OPERA Cloud front-desk user says busy-period walk-in check-in takes enough clicks that they create placeholder reservations and temporarily record ID details in a text editor, then backfill later. Their IT team is willing to expose API keys.

Oracle already provides configurable check-in steps, preregistration, partner ID scanning, OHIP REST APIs and prebuilt contactless check-in integration recipes. Canary and other mature partners integrate mobile check-in with OPERA.

**Verdict:** DEMOTED — exact native and partner surfaces already occupy the control layer.

## Method conclusion

Scan 063 confirms that **post-incumbent residual evidence is materially stronger** than generic spreadsheet/workaround evidence. It reveals genuine gaps that survived real purchasing and adoption.

But it also exposes a new distinction:

```text
PERSISTENT RESIDUAL AFTER INCUMBENT
!=
DURABLE EXTERNAL WHITE SPACE

TEMPORARY PRODUCT DEFICIENCY
+ ACTIVE NATIVE ROADMAP / PARTNER ECOSYSTEM
→ LIKELY ABSORPTION
```

The next evidence escalation should therefore be economic rather than another abstract mechanism. Scan 064 will search for buyers who pay an incumbent **and separately keep paying an external recurring workaround for the same outcome**. Parallel spend is stronger evidence that the residual itself carries willingness to pay.

The residual must still survive incumbent/roadmap preflight and remain digital or delegatable; expert consulting, configuration, physical capture, organizational change management and one-off migration work still fail closed.

## Sources

- Salesforce buyer residual: https://www.reddit.com/r/salesforce/comments/1syz3x8/salesforce_outlook_in_2026_is_anyone_actually/
- Salesforce EAC migration/current activity storage: https://help.salesforce.com/s/articleView?id=004633781&language=en_US&type=1
- Jira buyer residual: https://www.reddit.com/r/AIDeveloperNews/comments/1v7xa33/anyone_moved_portfolio_planning_off_jira_without/
- Jira Plans: https://www.atlassian.com/software/jira/guides/advanced-roadmaps/overview
- Jira plan limits: https://support.atlassian.com/jira-software-cloud/docs/limits-on-plan-size-in-advanced-roadmaps/
- Workday buyer residual: https://www.reddit.com/r/workday/comments/1vtn322/unpopular_opinion_workday_financials_doesnt_need/
- Workday OfficeConnect: https://doc.workday.com/admin-guide/ko-kr/financial-management/-0/officeconnect-/uvy1645571165544.html?toc=2.20.5
- ServiceNow buyer residual: https://www.reddit.com/r/servicenow/comments/1vz588t/what_tools_do_you_recommend_to_drive_servicenow/
- ServiceNow Dynamic Guidance: https://www.servicenow.com/community/servicenow-ai-platform-blog/platform-academy-january-27th-2025-go-from-zero-to-hero/bc-p/3554091
- Epic analyst residual: https://www.reddit.com/r/healthIT/comments/1uj0br6/question_from_newer_epic_analyst/
- Epic Cogito tools: https://health.ucdavis.edu/data/tools.html
- Epic SlicerDicer: https://medicine.yale.edu/ybic/research-informatics-office/data-resources-services/self-service-tools/slicerdicer/
- OPERA buyer workaround: https://www.reddit.com/r/askhotels/comments/1swzz5j/check_in_automation/
- OPERA preregistration: https://docs.oracle.com/en/industries/hospitality/opera-cloud/26.2/ocsuh/c_booking_reservations_pre_register_arrival_reservations.htm
- Oracle OHIP: https://www.oracle.com/hospitality/integration-platform/
- Canary OPERA integration: https://www.canarytechnologies.com/integrations/oracle-and-canary-partnership
