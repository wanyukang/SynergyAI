# Report Contract

Write `report.json` even when the workflow fails. It must contain:

```json
{"input":"path/to/document.md","roles":["product_manager","software_engineer"],"max_rounds":5,"rounds_executed":1,"initial_reviews":{},"rounds":[{"round":1,"context_handoffs":[],"public_statements":[],"consensus":{}}],"final_decisions":[],"decision_map":[],"consistency_audits":[],"repair_passes":0,"errors":[],"status":"completed"}
```

Valid statuses are `completed`, `max_rounds_without_consensus`, `consistency_failed`, and `failed`. Store full initial reviews, every context handoff, every public statement, consensus results with evidence, the editor's decision map, every consistency audit, repair count, and errors. For each retry, record `phase`, `round`, `role`, `failure_type`, `invalid_fields`, and whether the repair succeeded. Store structured artifacts only; never store hidden reasoning. The CLI stream and `report.json` must contain the same validated public artifacts; a compact summary may supplement them but cannot replace them. Write `optimized.md` only for `completed` runs.
