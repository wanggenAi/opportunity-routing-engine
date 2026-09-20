# ATTRACTION_SCAN_015-F1 — Provider Response Intake

Date: 2026-09-20  
State: `WAITING_FOR_FIRST_PROVIDER_RESPONSE`

## Purpose

Convert real provider replies into auditable Gate-A evidence without allowing sales
language or interpretation to overwrite the provider's actual words.

## Intake invariant

For every inbound provider message, preserve two layers:

```text
RAW WRITTEN PROVIDER EVIDENCE
!=
OUR DIMENSION CLASSIFICATION
```

The raw email/message ID, sender, date and relevant exact claims must remain traceable.

## R1–R8 mapping

Use the locked response rubric:

- R1 — multi-rail comparison;
- R2 — final-outcome visibility;
- R3 — non-identifying outcome retention;
- R4 — future derived statistical/routing use;
- R5 — competitor benchmarking/ranking;
- R6 — commission/settlement event;
- R7 — operator remains router/channel;
- R8 — retention/deletion/security/privacy obligations.

Do not upgrade a dimension that the provider did not actually answer.

## Response classes

### COMPATIBLE_EXPLICIT

Use only when the reply explicitly supports the decisive Wave-1 rights.

Action:
- preserve message evidence;
- classify answered dimensions;
- send Wave 2 only for missing R2/R6/R7/R8 details;
- do not pass Gate A until a second overlapping rail also qualifies.

### COMPATIBLE_BUT_INCOMPLETE

The provider answers one or more decisive rights positively but leaves others unclear.

Action:
- acknowledge;
- ask only the missing decisive question(s);
- do not resend the full questionnaire unnecessarily.

### NDA_OR_ONBOARDING_REQUIRED

The provider says rights can only be disclosed after NDA, enterprise verification or
formal partner onboarding.

Action:
- record this as `CONDITIONAL_DISCLOSURE_PATH`, not PASS and not FAIL;
- ask for exact prerequisites and whether a current agreement/template can be reviewed;
- evaluate activation friction separately.

### VAGUE_COMMERCIAL

Examples:
- "可以合作";
- "可以接";
- "后面商务谈";
- "数据都有";
- "佣金可以谈".

Action:
- keep R1/R3/R4/R5 as UNKNOWN unless explicitly answered;
- reply with the single shortest unresolved decisive question;
- do not reward vagueness by treating API availability as data-use rights.

### INCOMPATIBLE_EXPLICIT

Examples:
- no competitor comparison;
- no retention after transaction;
- data only for reconciliation;
- no use of outcomes for future routing/model;
- operator must become transaction principal.

Action:
- mark the exact affected dimension FAIL;
- do not argue with the provider;
- evaluate whether the formation survives with other rails;
- if two otherwise viable rails fail R3/R4, kill F1 current form.

### NO_RESPONSE_YET

Silence after sending.

Action:
- do not classify as FAIL;
- one concise follow-up may be used after a reasonable business interval;
- do not create recurring founder chasing as the business model.

## Follow-up templates

### Missing decisive rights

> 感谢回复。为了避免我对贵司规则理解错误，我只再确认一个最关键的问题：
> 如果订单数据已经去除姓名、手机号、地址、收款账户、IMEI/序列号等个人标识，
> 合作方是否可以长期保留“初始估价→验机价→最终成交结果/耗时”的非识别性统计记录，
> 并据此决定未来订单优先推荐给哪一家已合法授权的回收合作平台？
> 如果该用途需要写进合作协议或单独授权，也请直接告知即可。

### NDA / onboarding path

> 明白。如果这些边界只能在正式合作阶段确认，麻烦告知查看现行合作协议/数据条款前
> 需要完成哪些步骤（例如 NDA、营业执照、企业认证、商务审核），以及是否可以先获取
> 协议模板或相关条款用于可行性评估。

### Positive Wave 2 diligence

Use:
`docs/research/ATTRACTION_SCAN_015_F1_RIGHTS_INQUIRY.md`

but only ask dimensions still missing from the provider's reply.

### Explicit incompatibility

Do not persuade the provider to change policy.

Record the exact restriction and update the Gate-A matrix.

## Current response state

```text
AIHUISHOU_RESPONSE       = NONE
XIAOZHI_BEARHOME_RESPONSE = NONE
SUHUANJI_CONTACT          = UNRESOLVED
PROVIDER_RESPONSES        = 0
COMPATIBLE_WRITTEN_RAILS  = 0
GATE_A                    = PARTIAL_PASS_RIGHTS_UNKNOWN
```

No delivery-failure notice was observed immediately after Wave 1 send.

## Next action

Wait for the first actual inbound provider reply, preserve it, and classify only the
claims it contains.
