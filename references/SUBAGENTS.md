# Subagents

Use role separation even if the platform does not support literal child agents.

## Preferred roles

- `task-freezer`
- `source-curator`
- `outline-builder`
- `section-drafter`
- `signal-distiller`
- `task-verifier`
- `task-fixer`
- `task-integrator`

## Role boundaries

### `task-freezer`

Purpose:
- freeze `spec.md` and `requirements.md`

Hard boundaries:
- may read profiles and source metadata
- must not write `draft.md`
- must not write `verdict.json`

### `source-curator`

Purpose:
- curate `sources_registry.md`
- separate approved from candidate sources

Hard boundaries:
- may write `candidate_sources.md`
- must not silently promote a candidate source into approved use

### `outline-builder`

Purpose:
- build `outline.md` with canonical section ids

Hard boundaries:
- section ids must be stable
- must not write the full draft

### `section-drafter`

Purpose:
- write or refine `draft.md`
- keep the draft aligned with outline ids and approved sources

Hard boundaries:
- must not cite unapproved sources
- must not backfill fake locators

### `signal-distiller`

Purpose:
- turn raw feedback into structured next-state signals
- update `feedback_log.jsonl` and `feedback_digest.md`

Hard boundaries:
- treat raw feedback as noisy by default
- distill concise correction hints
- classify signals as evaluative, directive, or mixed

### `task-verifier`

Purpose:
- run a fresh verification pass

Hard boundaries:
- must not edit `draft.md`
- must write `verdict.json`
- must write `problems.md` when the verdict is not `PASS`

### `task-fixer`

Purpose:
- repair only what the verifier proved or flagged

Hard boundaries:
- must reconfirm each problem before editing
- must keep already-passing areas stable
- must refresh evidence artifacts after changes

### `task-integrator`

Purpose:
- produce the final coherent package after the loop has converged

Hard boundaries:
- must not introduce unsupported new claims
- must ensure `handoff.md`, `evidence.json`, and `verdict.json` agree

## Delegation pattern

Keep delegation depth flat:

1. run `init` if needed
2. use one role at a time
3. refresh task artifacts before any reset
4. keep verification fresh

For long tasks, prefer:

1. `task-freezer`
2. `source-curator`
3. `outline-builder`
4. `section-drafter`
5. `signal-distiller`
6. `task-verifier`
7. `task-fixer`
8. `task-verifier`
