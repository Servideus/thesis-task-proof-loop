# Workflow

## Loop

```text
freeze -> source lock -> outline -> draft -> claim map -> review -> targeted fix -> review again
```

## 1. Initialize or reuse a task

Create a stable task id and work inside:

```text
.agents/tasks/<TASK_ID>/
```

If the task already exists, inspect its current status before editing files.

## 2. Freeze the task

Create `spec.md` and `requirements.md`.

Before moving on, make sure these are explicit:
- target section;
- scope;
- exclusions;
- formatting rules;
- acceptance criteria.

## 3. Lock approved sources

Create `sources_registry.md`.

Separate stronger sources from weaker background material. Mark inaccessible or partially checked items clearly.

Do not rely on unregistered sources.

## 4. Build the outline

Create `outline.md`.

The outline should be detailed enough for later source mapping.

## 5. Draft from approved materials

Create `draft.md`.

Keep factual support separate from interpretation. Stay inside the frozen outline.

## 6. Map claims to sources

Create `claim_source_map.csv`.

Track every substantive claim.

## 7. Review

Create `evidence.md` and `verdict.json`.

The review should check:
- scope alignment;
- source discipline;
- unsupported claims;
- logical continuity;
- formatting drift.

## 8. Apply targeted fixes

If needed, write issues into `problems.md`, apply only targeted corrections, and record the changes in `revision_log.md`.

## 9. Repeat or stop

Repeat until:
- PASS;
- PASS_WITH_WARNINGS;
- or FAIL because the evidence base or requirements are not good enough.

## Stop conditions

Return FAIL when:
- requirements conflict;
- essential sources are missing;
- citations cannot be grounded;
- the task would require guesswork.

## Practical guidance

- Small reliable steps beat giant rewrites.
- The reviewer should be stricter than the drafter.
- Stable text should stay stable unless a real defect requires change.
- Traceability matters more than polish.
