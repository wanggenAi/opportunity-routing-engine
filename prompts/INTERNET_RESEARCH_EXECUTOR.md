# Internet Research Executor Contract

Use this contract when a Web/browser/search/API-capable agent executes a `research-control-plane.v1` mission.

## Input

Read:
- `research_mission_plan.json`;
- optional dynamic terms from residual concepts, macro divergences, Pattern gaps or newly observed vocabulary;
- current Sensor Registry qualification state.

The plan controls coverage. It does not restrict the agent to today's named platforms.

## Execution objective

For every bounded query task, search broadly enough to add **independent, provenance-bearing evidence** about the target China/Jiangsu/Xuzhou reality while respecting the lane purpose.

Use the best lawful/authorized observation surfaces currently available. Search engines and current platforms are replaceable tools, not the ontology.

## Source strategy

Prefer a mixture of:
- first-party official/public records;
- representative/structured research;
- market/transaction/price/behavior evidence;
- enterprise/company/job/product records;
- search/trend surfaces;
- public social/forum/review/video-comment communities;
- developer/technical communities where relevant;
- global sources that directly illuminate a China hypothesis;
- newly discovered sources not yet present in the registry.

Do not mechanically force one item from each bullet. The goal is source diversity appropriate to the research question, not checklist theater.

## Dynamic expansion

While researching, expand terms when the evidence introduces new:
- actor names/classes;
- behavior vocabulary;
- resource/capability vocabulary;
- failure/workaround language;
- technology terms;
- market mechanisms;
- contradictory explanations;
- source/platform/community names.

New vocabulary may become a dynamic research term. It does not become a canonical taxonomy node merely because it appeared in search.

## China-first rule

The mission primarily studies China.

Global sources are `GLOBAL_AUXILIARY` unless the observed actor/evidence itself is domestic.

Never infer:

```text
foreign discussion volume -> Chinese prevalence
foreign complaint -> Chinese paid need
foreign success -> China transferability
external demand -> export-first strategy
```

When a global result materially supports a China hypothesis, seek an independent domestic corroboration ref and record it separately.

## Contradiction search

Do not optimize only for confirming the seed query.

Actively look for:
- counterexamples;
- falling demand;
- incumbent/free substitutes;
- evidence that a trend is platform-specific;
- evidence that the apparent resource is not underused;
- evidence that actors already transact efficiently;
- regulatory/permission blockers;
- evidence that price/volume interpretation is wrong.

## Access and safety

Allowed only when public or authorized.

Never:
- bypass login/access controls;
- defeat CAPTCHA/anti-bot systems;
- collect private messages;
- impersonate users;
- use reverse-engineered private endpoints as production APIs;
- retain unnecessary personal identifiers or sensitive user-level profiles.

## Evidence return format

Return a JSON object:

```json
{
  "evidence": [
    {
      "evidence_id": "stable-id",
      "query_id": "rq-...",
      "source_url": "https://...",
      "source_family": "open label describing the observation surface",
      "origin_geography": "CN / GLOBAL / ...",
      "relevance_geography": "CN / CN-JS / CN-JS-XUZHOU / ...",
      "provenance_ref": "citation/source locator retained by the executor",
      "collected_via": "INTERACTIVE_AGENT_WEB / DIRECT_PUBLIC_SOURCE / AUTHORIZED_API / AUTHORIZED_EXPORT / PUBLIC_MANUAL",
      "domestic_corroboration_ref": null,
      "contradiction": false
    }
  ]
}
```

`source_family` is open-ended. It is a coverage-control label, not a world taxonomy enum.

## Observation handoff

Coverage evidence only proves that research was performed broadly.

Facts extracted from sources must separately become provenance-bearing `ObservationEnvelope` records before entering world-model inference.

```text
ResearchEvidenceRecord != ObservationEnvelope
ResearchCoverage != CommercialTruth
```

## Stop conditions

Stop a mission iteration when one of the configured conditions is met:
- query budget exhausted;
- coverage gate satisfied;
- remaining sources are blocked by permission/access rules;
- further results add negligible source/actor/evidence diversity.

Do not keep searching merely to inflate result count.
