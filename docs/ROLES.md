# Roles

The skill should keep roles conceptually separate even if a single agent executes multiple steps.

## 1. Task Freezer

Purpose: turn the user's request into a frozen, reviewable task definition.

Inputs:
- user request;
- institutional requirements;
- existing outline;
- target section or chapter name.

Outputs:
- `spec.md`
- `requirements.md`

Responsibilities:
- define scope;
- record exclusions;
- define acceptance criteria;
- record unresolved conflicts.

Must not:
- start drafting before the task is frozen;
- silently fill missing requirements with guesses.

## 2. Source Curator

Purpose: build and label the approved source base.

Inputs:
- user-approved sources;
- available citations and excerpts;
- source metadata.

Outputs:
- `sources_registry.md`
- optional notes in `evidence.md`

Responsibilities:
- register sources;
- label trust level;
- mark accessibility;
- warn about weak, missing, or secondary-only evidence.

Must not:
- register inaccessible sources as fully checked;
- treat incomplete references as verified.

## 3. Outline Builder

Purpose: transform the frozen task into a structured outline.

Inputs:
- `spec.md`
- `requirements.md`
- `sources_registry.md`

Outputs:
- `outline.md`

Responsibilities:
- keep structure aligned with scope;
- make sections granular enough for claim mapping;
- avoid outline drift.

Must not:
- add major sections not justified by the task.

## 4. Drafter

Purpose: produce a controlled draft from approved materials.

Inputs:
- `spec.md`
- `requirements.md`
- `sources_registry.md`
- `outline.md`
- user notes or excerpts;
- existing draft fragments.

Outputs:
- `draft.md`
- `claim_source_map.csv`
- `quotes.md` if relevant.

Responsibilities:
- write only from approved materials;
- keep claims proportional to evidence;
- preserve terminology and logic.

Must not:
- invent support;
- pad the text with generic filler;
- rewrite the outline on the fly.

## 5. Reviewer

Purpose: independently inspect the draft in a fresh context.

Inputs:
- full task folder.

Outputs:
- `verdict.json`
- `problems.md`
- review notes in `evidence.md`.

Responsibilities:
- inspect structure;
- inspect source discipline;
- flag unsupported claims;
- flag contradictions;
- flag overstatement.

Must not:
- repair the text during review;
- ignore missing evidence because the draft sounds plausible.

## 6. Fixer

Purpose: apply targeted corrections from the reviewer.

Inputs:
- `problems.md`
- current draft artifacts.

Outputs:
- updated `draft.md`
- updated `claim_source_map.csv`
- `revision_log.md`

Responsibilities:
- fix only recorded defects;
- preserve stable sections;
- log what changed.

Must not:
- do broad stylistic rewrites without need;
- erase traceability.

## 7. Integrator

Purpose: assemble the final deliverable when the loop passes.

Inputs:
- all stable task artifacts.

Outputs:
- final reviewed section or chapter;
- final `verdict.json`.

Responsibilities:
- ensure consistency across files;
- keep the final output aligned with the frozen task.

Must not:
- introduce new claims at the end.
