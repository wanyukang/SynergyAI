---
name: multi-agent-prd-review
description: Review a Markdown PRD with isolated Codex subagents for product, engineering, UX, security, and QA perspectives, then produce an optimized document and an auditable report.
---

# Multi-Agent PRD Review

Use this skill for a user-requested multi-perspective review or optimization of a Markdown PRD. This is a native Codex workflow: use fresh subagents for role work and the current Codex model. Do not call an external LLM API, request provider tokens, or implement role calls in a script.

Read [references/roles.md](references/roles.md), [references/workflow.md](references/workflow.md), [references/schemas.md](references/schemas.md), and [references/reporting.md](references/reporting.md) before starting.

## Inputs

- Read the user-provided Markdown document completely.
- Default roles: `product_manager`, `software_engineer`, `ux_designer`.
- Optional roles: `security_privacy`, `qa_engineer`.
- Default maximum discussion rounds: 5. Accept an explicitly requested value from 1 through 15.
- Preserve the user's output directory; otherwise use `review-output/` beside the input document.

## Execution

1. Parse the document, selected roles, and maximum rounds. Report invalid paths, empty documents, unknown roles, or out-of-range rounds before creating subagents.
2. Create one fresh subagent per selected role for independent initial review. These calls may run in parallel. Pass only the original document and that role's definition.
3. Collect and validate each role's structured initial review. Immediately stream the complete structured review to the main CLI as a labeled role artifact. Initial reviews are evidence for the discussion, not the final discussion result.
4. Run each discussion round as a strict sequential round table in the selected role order. Create a fresh subagent for each turn and pass only the original document, that role's own structured history, the previous consensus state, and public statements already released in the current round.
5. Create a fresh consensus judge after every round. Pass only the original document, current public statements, previous consensus, and round number.
6. Stop early when `consensus_reached` is true. Stop at the configured maximum when it is false. Never invent agreement to reach the document phase.
7. If consensus is reached, create a full-document editorial rewrite from the original Markdown and confirmed `decisions`. Apply each decision at the location of the affected requirement, remove or replace superseded wording, and preserve only structure that remains logically valid.
8. Create a fresh consistency-auditor subagent to compare the draft against the original document and confirmed decisions. It must identify contradictions, duplicate requirements, stale examples, unresolved placeholders, and acceptance criteria that no longer match the body.
9. If the auditor finds blocking issues, send only its structured findings and the draft to a fresh editor for targeted repair, then audit again. Write the final document only after the audit passes.
10. Always write `report.json`; write `optimized.md` only after consensus and a passing consistency audit.

The workflow must complete at least one full discussion round after initial review. Do not replace the round table with a single disagreement summary. On every role return, stream the complete validated public artifact, including `position`, `reasons`, `responses_to_others`, `proposals`, and `open_questions`. On every judge return, stream the complete validated consensus artifact, including agreements, disagreements, decisions, and next questions. During final editing and auditing, stream the draft status, audit findings, repair count, and final consistency status.

## Visible Progress

Keep the workflow visible in the main Codex CLI stream. Before every subagent call, emit a short progress line containing the phase, round, role, and action. Immediately after it returns, emit the complete validated artifact. After each judge call, emit the complete validated consensus artifact and whether another round will run. After the workflow ends, emit the final status and artifact paths.

Use this format:

```text
[PRD Review] Phase: initial review | Role: Product Manager | starting
[PRD Review] Phase: initial review | Role: Product Manager | completed; issues=4; recommendations=3
[PRD Review] Round 1/5 | Role: Software Engineer | public position: adopt async validation
[PRD Review] Round 1/5 | Judge | consensus=false; agreements=2; blocking_disagreements=1; next=round 2
[PRD Review] Final edit | decision_map=7 entries | draft ready
[PRD Review] Consistency audit | passed=false | blocking_findings=2 | repair_pass=1
[PRD Review] Completed | status=completed | optimized=review-output/optimized.md | report=review-output/report.json
```

Stream validated structured artifacts in full, enclosed by explicit start/end markers with phase, round, role, and artifact type labels. Before each later role call, stream a complete `context_handoff` artifact showing exactly which prior public statements are being passed to that role. Do not print hidden reasoning, private history, full prompts, secrets, or unvalidated raw responses. These are progress events in the main conversation; the Skill cannot guarantee token-by-token streaming of a subagent's internal generation.

Use this envelope:

```text
[PRD Review][artifact:start][phase=round][round=1][role=software_engineer][type=public_statement]
{one validated JSON object}
[PRD Review][artifact:end][phase=round][round=1][role=software_engineer][type=public_statement]
```

## Context Boundary

Subagents receive explicit task payloads. Keep role histories private; propagate only validated `public_statement` objects. Do not pass the parent conversation, another role's private history, hidden reasoning, or the full report into a role subagent. Do not record hidden reasoning in artifacts.

## Failure Handling

If a subagent fails or returns invalid structure, classify the failure as `empty_response`, `invalid_json`, `wrong_schema`, or `semantic_invalid`. Retry that task once with the same bounded input and an explicit correction containing the exact missing or invalid field. Preserve the original viewpoint; the retry is a format repair, not a new analysis. Never stream or propagate the invalid response. If the consistency audit fails twice after targeted repair, stop with `status: consistency_failed` and retain the draft and audit findings in the report; do not present the draft as final. If a discussion subagent still fails, stop the affected phase and write an intermediate report with `status: failed`. If the maximum rounds end without consensus, write `status: max_rounds_without_consensus` and retain all public statements; do not write an optimized document.
