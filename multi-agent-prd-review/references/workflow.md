# Native Subagent Workflow

## Initial Review

Create one fresh subagent for each selected role. Give it the complete Markdown document, its role definition, and this instruction:

> Review the document only from your role's perspective. Return valid JSON using the initial review schema. Separate concrete issues, recommendations, and open questions. Do not decide for other roles.

The initial calls are independent and may run in parallel. When each finishes, emit its complete validated initial-review JSON in the main CLI stream under a role and phase label. Do not wait until the entire workflow ends, and do not reduce it to counts only. Require exactly one JSON object, every required key, and a top-level `role` equal to the assigned role.

## Sequential Round Table

For each round, create fresh subagents in the selected role order. Each task receives the original document, the role definition, that role's initial review, that role's own prior structured history, public statements already released earlier in this round, and the prior consensus state.

The subagent must return a complete `public_statement`. The next role receives that statement, never the prior role's private context. Keep the current round's public statements in a separate list. Before creating the next role, emit a `context_handoff` artifact listing the prior roles and their complete public statements that will be visible to it. Emit a progress event before every sequential turn and the complete validated public-statement JSON immediately after it returns. The main stream should show the position, every reason, every response, every proposal, and every open question for every role. Require exactly one JSON object, every required key, and a top-level `role` equal to the assigned role.

## Consensus Judge

After all selected roles have spoken, create a fresh judge subagent. It receives only the original document, current public statements, prior consensus state, and round number. It classifies agreements, blocking disagreements, confirmed decisions, and questions required for the next round. It must not add a new role opinion. After it returns, immediately emit the complete validated consensus JSON before creating another role subagent. Require exactly one JSON object with all five keys: `consensus_reached`, `agreements`, `disagreements`, `decisions`, and `next_questions`; every item must cite concrete role and point evidence.

## Final Document

After the judge reports consensus, create a fresh editor subagent with the original Markdown and confirmed decisions. Require a full-document rewrite that edits the original requirement locations, removes superseded statements, updates dependent sections and examples, and keeps terminology consistent. The editor must not append an override chapter, add a “source of truth” disclaimer, or leave contradictory old text in place.

The editor must produce a decision map before the document: for every confirmed decision, identify the original section(s) changed and describe the replacement. Every confirmed decision must have a mapped location; every changed acceptance criterion must agree with the revised body.

## Consistency Audit

After the editor returns, create a fresh auditor subagent. Give it only the original Markdown, confirmed decisions, and draft. Ask it to check:

- each confirmed decision is implemented at the relevant original location;
- superseded requirements, examples, and terminology are removed or updated;
- no section contradicts another section;
- acceptance criteria, flows, interfaces, and security constraints agree with the body;
- placeholders and unresolved questions are either resolved by consensus or explicitly marked as open;
- the draft does not rely on a late override section.

The auditor returns the audit schema. If it reports blocking findings, create a fresh editor with only the draft and findings, apply targeted repairs, and run the audit again. Allow at most two repair passes. Only an audit with no blocking findings can produce `optimized.md`.
