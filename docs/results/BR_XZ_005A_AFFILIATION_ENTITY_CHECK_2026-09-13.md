# BR-XZ-005A Affiliation Entity Check — 2026-09-13

Status: `MEDIA AFFILIATION OBSERVED / FORMAL AFFILIATION ENTITY TYPE UNRESOLVED`

## Why this check exists

The July 2026 Xuzhou case says technology manager Wang Yingping is affiliated with **Jiangsu Huaihai Technology Property Rights Exchange Center** and then uses the **CUMT Science Park Technology-Manager Office** expert/result databases.

That proves a real multi-institution operating pattern. It does **not** by itself prove that the media phrase `挂靠在江苏淮海技术产权交易中心` is identical to a current provincial `技术经理人事务所` affiliation record.

This distinction matters because the 2026 provincial rules assign social recruitment, project-cooperation affiliation, affiliation agreements and commission settlement specifically to an authorized `技术经理人事务所`.

## Current 2026 provincial rule

The 2026 Jiangsu Technology-Manager Office Management Rules define a technology-manager office as an entity established with authorization from the Jiangsu Technology Property Rights Exchange Market.

Article 9 explicitly says an office may:
- recruit technology managers from society;
- establish affiliation through project cooperation;
- sign standardized agreements;
- settle technology-transfer service commissions by agreement;
- support coordination, contracts, invoicing and settlement.

The rules also provide biennial performance evaluation and list the conditions under which office qualification may be cancelled.

Source:
- https://www.jstec.com.cn/news/202602628049695003

## 2026 support-construction list check

The April 30 / May 6, 2026 provincial notice lists 41 institutions supported to build Jiangsu Technology Property Rights Exchange Market technology-manager offices.

The two Xuzhou entries shown in that notice are:
- Xuzhou Medical University Asset Management Co., Ltd.;
- Jiangsu Normal University Science Park Co., Ltd.

The published 41-entry support-construction list does **not** show:
- Jiangsu Huaihai Technology Property Rights Exchange Center Co., Ltd.;
- Xuzhou China University of Mining and Technology National University Science Park Co., Ltd.

Source:
- https://www.jstec.com.cn/news/202612028050552446

## Why absence from that list is not a FAIL

The notice is titled a **2026 support-construction list**. It is not explicitly described as the complete register of every currently valid office.

The current management rules use periodic performance evaluation and qualification-cancellation mechanisms rather than stating that every existing office must appear on each annual support-construction list.

Therefore:

```text
NOT IN 2026 SUPPORT-CONSTRUCTION LIST
!=
PROVEN NOT CURRENTLY AUTHORIZED
```

The list creates a status ambiguity that must be resolved, not a negative verdict.

## Historical / local evidence making the ambiguity real

In 2022, Xuzhou CUMT National University Science Park Co., Ltd. appeared in the provincial **cultivation** list rather than the formally recognized list.

Source:
- https://www.jstec.com.cn/news/202234815902675344

By January 2026, the CUMT Science Park publicly reported that it had received a **2025 Jiangsu five-star technology-manager office** honor. This proves that a 2022 cultivation snapshot is not enough to infer later status.

Source:
- https://www.cumtusp.com/yuanqujianjie/1778.html

Meanwhile, July 2026 Jiangsu/Xuzhou reporting explicitly describes Wang Yingping as affiliated with the Huaihai center and separately describes her use of the CUMT Science Park office resource databases.

Source:
- https://www.zgjssw.gov.cn/shixianchuanzhen/xuzhou/202607/t20260713_8583095.shtml

## Correct interpretation

The safest current model is:

```text
OBSERVED MEDIA-LABELLED AFFILIATION TO HUAIHAI CENTER
+
OBSERVED RESOURCE USE FROM CUMT SCIENCE PARK OFFICE
+
CURRENT PROVINCIAL OFFICE RULE EXISTS
+
HUAIHAI'S EXACT CURRENT AFFILIATION ENTITY / ACCOUNT STATUS = UNKNOWN
```

Do not collapse these into one assumption.

## New first question for the manual inquiry

Before asking whether this operator can be accepted, ask:

> In the current Jiangsu system, when a technology manager is described as `挂靠在江苏淮海技术产权交易中心`, what is the formal affiliation entity and platform status? Is the affiliation contracted directly with Jiangsu Huaihai Technology Property Rights Exchange Center, through a separately authorized technology-manager office, or through another current institutional arrangement?

Then ask which exact entity signs the affiliation/project-cooperation agreement and which platform account records the relationship.

## Decision consequence

Issue #71 remains the correct gate, but its first validation is now **entity/status resolution**, followed by operator acceptance.

PASS requires a current formal route whose legal/platform entity, agreement party and operating rights can be named.

HOLD if staff only confirm that `有人挂靠` but cannot identify the current agreement entity / system relationship.

FAIL/DOWNGRADE if the media affiliation is historical, informal, employee-only, or unavailable to external individuals and no equivalent formal route exists.

## Boundary

```text
MEDIA LABEL != PROVINCIAL REGISTRY STATUS
SUPPORT-CONSTRUCTION LIST != PROVEN COMPLETE ACTIVE REGISTER
OBSERVED AFFILIATED PERSON != OPEN EXTERNAL AFFILIATION
LOCAL CENTER != AUTOMATICALLY TECHNOLOGY-MANAGER OFFICE
OFFICE RULE != HUAIHAI-SPECIFIC ACCEPTANCE
```
