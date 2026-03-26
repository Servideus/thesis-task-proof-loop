---
name: thesis-task-proof-loop
description: Controlled repo-local workflow for long academic writing tasks such as diploma/thesis chapters, literature reviews, and research sections. Use when Codex needs to initialize or continue a task under `.agents/tasks/<TASK_ID>/`, freeze requirements, register approved sources, keep candidate sources separate, draft only from approved materials, log feedback signals, run fresh verification, and apply minimal traceable fixes.
---

# Thesis Task Proof Loop

Run this skill while your shell working directory is inside the target repository.
When examples mention `scripts/task_loop.py`, that path is relative to this skill root.

Read these references only when needed:
- `references/REFERENCE.md` for install paths, commands, and generated files
- `references/SCHEMAS.md` for artifact formats and validator expectations
- `references/COMMANDS.md` for command-specific prompt shapes
- `references/SUBAGENTS.md` for role boundaries and delegation order

## Core contract

Operate through repo-local task artifacts, not through chat memory.
Keep every working artifact inside:

```text
.agents/tasks/<TASK_ID>/
```

Use this folder as the source of truth for:
- frozen task scope
- approved source registry
- canonical section ids
- draft state
- claim-to-source traceability
- feedback signals
- evidence
- verdicts
- handoff state

## Workflow commands

Treat these words as commands when the user invokes this skill:
- `init`
- `freeze`
- `sources`
- `outline`
- `draft`
- `map`
- `evidence`
- `verify`
- `fix`
- `run`
- `status`
- `validate`

Script-backed commands:

```bash
python scripts/task_loop.py init --task-id <TASK_ID> --task-text "<task text>"
python scripts/task_loop.py status --task-id <TASK_ID>
python scripts/task_loop.py validate --task-id <TASK_ID>
```

Command inference:
- if the task folder does not exist, do `init` only and stop
- if `spec.md` is still placeholder-like, do `freeze`
- if approved sources are missing, do `sources`
- if canonical section ids are missing, do `outline`
- if the draft is missing or placeholder-like, do `draft`
- if claims are not mapped, do `map`
- if evidence is stale or `UNKNOWN`, do `evidence`
- if no fresh verdict exists, do `verify`
- if verdict is `FAIL` or `PASS_WITH_WARNINGS`, do `fix`

## Hard rules

1. Never invent citations, bibliographic fields, pages, DOI, URL, statistics, or quotes.
2. Never cite anything outside `sources_registry.md`.
3. Never silently treat `candidate_sources.md` as approved evidence.
4. Never claim to have read an unavailable source.
5. Never convert weak evidence into a strong conclusion.
6. Keep canonical `section_id` values stable across `outline.md`, `draft.md`, and `claim_source_map.csv`.
7. Log raw feedback separately from distilled instructions.
8. Run verification in a fresh session or fresh role.
9. Do not let the verifier patch the draft during verification.
10. Apply only the smallest safe fix set from `problems.md`.
11. Update artifacts before any reset or role change.
12. Stop with `FAIL` when the source base or requirements are insufficient.

## Main-line vs side-turns

Main-line artifacts:
- `spec.md`
- `requirements.md`
- `writing_profile.md`
- `advisor_preferences.md`
- `sources_registry.md`
- `outline.md`
- `draft.md`
- `claim_source_map.csv`
- `quotes.md`
- `evidence.md`
- `evidence.json`
- `feedback_digest.md`
- `handoff.md`
- `verdict.json`

Side-turn artifacts:
- `candidate_sources.md`
- `scratchpad.md`
- `feedback_log.jsonl`
- `events.jsonl`

Rules:
- keep unapproved sources in `candidate_sources.md`
- keep parking-lot ideas in `scratchpad.md`
- keep raw next-state signals in `feedback_log.jsonl`
- keep concise, reusable correction hints in `feedback_digest.md`
- keep long-run observability in `events.jsonl`

## Required artifact set

Minimum required files:
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
- `feedback_log.jsonl`
- `feedback_digest.md`
- `handoff.md`
- `problems.md`
- `revision_log.md`
- `verdict.json`
- `events.jsonl`
- `scratchpad.md`

For exact schemas, read `references/SCHEMAS.md`.

## Phase behavior

### `init`

Create the repo-local task folder and required artifacts.
Use:

```bash
python scripts/task_loop.py init --task-id <TASK_ID> --task-text "<task text>"
```

Stop after initialization unless the user explicitly asked for a later command.

### `freeze`

Fill and stabilize:
- `spec.md`
- `requirements.md`
- `writing_profile.md`
- `advisor_preferences.md`

Do not draft content during `freeze`.
Acceptance criteria must be explicit as `AC1`, `AC2`, ...

### `sources`

Register only approved sources in `sources_registry.md`.
Keep speculative or not-yet-approved materials in `candidate_sources.md`.
If a source is incomplete, mark its limits and permitted use.

### `outline`

Create `outline.md` with canonical level-2 headings:

```text
## [S1] ...
## [S1.1] ...
```

Each section should state:
- purpose
- planned claims
- allowed `source_id` values

### `draft`

Write `draft.md` only from:
- approved sources
- frozen requirements
- writing profile
- advisor preferences
- user-provided notes and excerpts

Keep section ids aligned with `outline.md`.

### `map`

Map each nontrivial claim in `claim_source_map.csv`.
If a direct quote is used, update `quotes.md`.
Do not add unsupported new claims during mapping.

### `evidence`

Refresh:
- `evidence.md`
- `evidence.json`
- `feedback_digest.md`
- `events.jsonl`

Judge acceptance criteria and quality gates independently.
Do not widen the draft on this step.

### `verify`

Run a fresh verification pass.
Read the repo-local artifacts, not the whole conversation.
Write:
- `verdict.json`
- `problems.md` when overall result is not `PASS`

The verifier must not edit production text.

### `fix`

Read only the spec, requirements, profiles, verifier output, and the necessary task files.
Reconfirm each defect before editing.
Make the smallest safe changes.
Then refresh:
- `evidence.md`
- `evidence.json`
- `revision_log.md`
- `feedback_digest.md`
- `handoff.md`
- `events.jsonl`

### `run`

Execute the loop serially:

```text
freeze -> sources -> outline -> draft -> map -> evidence -> verify -> fix(if needed) -> evidence -> verify
```

Refresh `handoff.md`, `feedback_digest.md`, and `events.jsonl` after each major phase.

## Feedback-signal policy

Treat each next-state signal as one of:
- evaluative
- directive
- mixed

For every important signal:
1. record the raw signal in `feedback_log.jsonl`
2. distill a concise actionable hint into `feedback_digest.md`
3. connect the hint to affected sections, claims, or files
4. mark whether the signal was applied, deferred, or rejected

Do not use raw feedback as the final instruction by default.
Distill it first.

## Handoff and reset policy

Before any reset or role change:
1. update touched artifacts
2. refresh `feedback_digest.md`
3. refresh `handoff.md`
4. append an event to `events.jsonl`

Reset is mandatory:
- after a full `draft -> verify -> fix` cycle
- when switching roles
- when moving to a new major section
- when the current context is polluted by stale hypotheses

Reset is not mandatory:
- inside a narrow local fix
- before the current state is written to files

## Stop conditions

Return `FAIL` when:
- approved sources are insufficient
- requirements conflict materially
- key citations cannot be grounded
- the task would require guessing instead of evidence
- the user asks for a confidence level that evidence cannot support

## Success condition

Claim success only when:
- the task matches the frozen scope
- the draft is aligned with canonical section ids
- nontrivial claims are traceable
- feedback signals are digested and either applied or explicitly deferred
- the final verifier returns `PASS` or `PASS_WITH_WARNINGS`

Before claiming the workflow is structurally ready, run:

```bash
python scripts/task_loop.py validate --task-id <TASK_ID>
```
