# Structured Output Contract

These are executable contracts, not illustrative shapes. Every subagent response must be exactly one JSON object: no Markdown fences, prose before or after the object, comments, trailing commas, or multiple objects. Validate the object before displaying or propagating it.

## Initial Review

Use only for independent initial review. Required fields and types:

```json
{"role":"product_manager","issues":[{"id":"issue-1","severity":"high","statement":"..."}],"recommendations":[{"issue_id":"issue-1","proposal":"..."}],"open_questions":["..."]}
```

`role` must equal the assigned role. `issues`, `recommendations`, and `open_questions` are always arrays; `severity` is `high`, `medium`, or `low`; every recommendation references an issue id from the same response. Empty lists are valid.

## Public Statement

Use only for a round-table turn. Required fields and types:

```json
{"role":"software_engineer","public_statement":{"position":"...","reasons":["..."],"responses_to_others":[{"role":"product_manager","point_id":"decision-1","stance":"modify","response":"..."}],"proposals":[{"id":"decision-1","text":"...","priority":"high"}],"open_questions":["..."]}}
```

`role` must equal the assigned role. `public_statement` is an object; `position` is a non-empty string; all list fields are arrays; `priority` is `high`, `medium`, or `low`. Every required key must be present, even when its value is an empty array. Every response to another role must include `role`, `point_id`, `stance`, and `response`; `stance` is `accept`, `modify`, `reject`, or `defer`. When prior public statements exist, `responses_to_others` must identify the concrete role and point being addressed; a generic agreement sentence is insufficient.

## Consensus

Use only for the independent judge. Required fields and types:

```json
{"consensus_reached":false,"agreements":[{"topic":"...","decision":"...","supporting_roles":["..."],"evidence":[{"role":"software_engineer","point_id":"decision-1"}]}],"disagreements":[{"topic":"...","positions":[{"role":"...","position":"...","point_id":"decision-1"}],"blocking":true,"evidence":[{"role":"product_manager","point_id":"decision-1"}]}],"decisions":[{"id":"decision-1","text":"...","supporting_roles":["..."],"evidence":[{"role":"software_engineer","point_id":"decision-1"}]}],"next_questions":["..."]}
```

`consensus_reached` and every `blocking` value are booleans. All collection fields are arrays. A decision is confirmed only when it appears in `decisions`. `consensus_reached` must be false when any unresolved disagreement has `blocking: true`. Every agreement, disagreement, and decision must cite at least one concrete role/point in `evidence`; the judge cannot add a role opinion or cite a point that was not publicly emitted.

## Context Handoff

Emit this artifact before each later role receives earlier statements:

```json
{"round":1,"recipient_role":"software_engineer","visible_public_statements":[{"role":"product_manager","statement":{}}]}
```

The handoff must contain the complete validated public statements, not role names, one-line summaries, or a list of IDs. It is a human-audit artifact as well as the exact context boundary for the recipient.

## Validation and Retry

Classify failures as `empty_response`, `invalid_json`, `wrong_schema`, or `semantic_invalid`. On retry, tell the subagent the exact category and missing or invalid field, preserve the original task and viewpoint, and request only a corrected object. Never propagate or stream an invalid response.

## Editorial Rewrite

The editor returns the complete revised Markdown plus a decision map. The decision map makes it auditable that consensus changed the original requirements instead of being appended as an override.

```json
{
  "decision_map": [
    {"decision_id":"decision-1","source_sections":["2. Functional requirements"],"change":"Replaced the six-character password rule with the confirmed policy."}
  ],
  "optimized_document":"# Revised PRD\n..."
}
```

`decision_map` must contain every confirmed decision exactly once. `source_sections` and `change` are required and non-empty. `optimized_document` must be the complete document, not a patch, appendix, or list of instructions.

## Consistency Audit

```json
{
  "audit_passed": false,
  "blocking_findings":[{"id":"finding-1","category":"contradiction","sections":["2","5"],"statement":"...","repair":"..."}],
  "non_blocking_findings":[{"category":"terminology","sections":["3"],"statement":"...","repair":"..."}],
  "verified_decisions":["decision-1"],
  "unresolved_decisions":[]
}
```

`audit_passed` is true only when `blocking_findings` is empty and every confirmed decision is verified. Categories are `contradiction`, `stale_requirement`, `duplicate_rule`, `acceptance_mismatch`, `placeholder`, or `terminology`. The auditor must inspect the whole draft; it must not approve the document because a final override section claims precedence.
