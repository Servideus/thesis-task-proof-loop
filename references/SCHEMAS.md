# Artifact Schemas

These are the required files for each task folder:

```text
.agents/tasks/TASK_ID/
  raw/
  spec.md
  requirements.md
  writing_profile.md
  advisor_preferences.md
  sources_registry.md
  candidate_sources.md
  outline.md
  draft.md
  claim_source_map.csv
  quotes.md
  evidence.md
  evidence.json
  feedback_log.jsonl
  feedback_digest.md
  handoff.md
  problems.md
  revision_log.md
  verdict.json
  events.jsonl
  scratchpad.md
```

## `outline.md`

Use canonical section identifiers in level-2 headings:

```text
## [S1] Название раздела
## [S1.1] Подраздел
```

The same `section_id` values must appear in `draft.md` and `claim_source_map.csv`.

## `draft.md`

Use the same canonical section identifiers as in `outline.md`.
Do not add unsupported sections in the draft without updating `outline.md`.

## `claim_source_map.csv`

Required header:

```csv
claim_id,section_id,claim_text,claim_type,source_ids,locator_if_available,direct_quote_used,evidence_strength,confidence_note,gap_flag,notes
```

Rules:
- `section_id` must exist in `outline.md` or `draft.md`
- `source_ids` must refer only to registered `source_id` values from `sources_registry.md`
- separate multiple `source_ids` with `;`
- use `gap_flag=yes` when a claim is intentionally incomplete or weakly supported

## `evidence.json`

Required top-level keys:
- `task_id`
- `generated_at`
- `artifact_timestamps`
- `overall_status`
- `acceptance_criteria`
- `quality_gates`
- `artifacts_used`
- `recommended_next_step`

Allowed overall statuses:
- `PASS`
- `PASS_WITH_WARNINGS`
- `FAIL`
- `UNKNOWN`

## `verdict.json`

Required top-level keys:
- `task_id`
- `generated_at`
- `artifact_timestamps`
- `overall_verdict`
- `acceptance_criteria`
- `quality_gates`
- `artifacts_used`
- `warnings`
- `blocking_issues`

Allowed overall verdicts:
- `PASS`
- `PASS_WITH_WARNINGS`
- `FAIL`
- `UNKNOWN`

## `feedback_log.jsonl`

Each non-empty line must be valid JSON with at least:
- `feedback_id`
- `source`
- `signal_type`
- `raw_feedback`
- `distilled_hint`
- `action_required`
- `status`

Recommended values:
- `source`: `user`, `advisor`, `verifier`, `self-check`, `tool`
- `signal_type`: `evaluative`, `directive`, `mixed`
- `status`: `open`, `applied`, `deferred`, `rejected`

Use `distilled_hint` for a concise 1-3 sentence correction direction.
Do not treat the raw feedback text as the final directive by default.

## `events.jsonl`

Each non-empty line must be valid JSON with at least:
- `timestamp`
- `event_type`
- `role`
- `summary`
- `next_step`

Use it as a lightweight observability log for long runs.

## Freshness heuristics

`status` and `validate` treat `evidence` as stale when any of these files is newer than the evidence bundle:
- `spec.md`
- `requirements.md`
- `writing_profile.md`
- `advisor_preferences.md`
- `sources_registry.md`
- `candidate_sources.md`
- `outline.md`
- `draft.md`
- `claim_source_map.csv`
- `quotes.md`
- `feedback_log.jsonl`
- `revision_log.md`

The evidence bundle is:
- `evidence.md`
- `evidence.json`
- `feedback_digest.md`

`status` and `validate` treat `verdict.json` as stale when any of these files is newer:
- `spec.md`
- `requirements.md`
- `writing_profile.md`
- `advisor_preferences.md`
- `sources_registry.md`
- `candidate_sources.md`
- `outline.md`
- `draft.md`
- `claim_source_map.csv`
- `quotes.md`
- `evidence.md`
- `evidence.json`
- `feedback_digest.md`

When `overall_status` or `overall_verdict` is not `UNKNOWN`, `generated_at` and `artifact_timestamps` should be filled.

## `problems.md`

For every non-pass acceptance criterion or quality gate, record:
- criterion id and text
- status
- why it is not proven
- minimal reproduction or inspection steps
- expected vs actual
- affected files or claims
- smallest safe fix
- corrective hint in 1-3 sentences

## Validation

Run:

```bash
python scripts/task_loop.py validate --task-id chapter-1
```

The validator checks:
- required file presence
- JSON parseability
- top-level key presence
- allowed status values
- `task_id` consistency
- canonical CSV header
- `section_id` consistency
- `source_id` consistency
- JSONL parseability for feedback and event logs
