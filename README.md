[Инструкция на русском языке здесь](README.ru.md).

# thesis-task-proof-loop

An agent skill and repository-local workflow for long-form academic writing. Task scope, approved sources, drafts and verification evidence live in explicit files. Claims are mapped to sources, feedback is recorded, and verification happens in a fresh context.

## Workflow

```text
init -> freeze -> sources -> outline -> draft -> map -> evidence -> verify -> fix -> evidence -> verify
```

The workflow freezes scope, separates approved and candidate sources, preserves section IDs, maps claims to sources and records feedback. Revisions should be small and tied to the evidence or feedback that prompted them.

## Setup and quick start

Use the repository's [SKILL.md](SKILL.md) as the agent instructions. The Python helper initializes task folders, validates artifact structure and reports status:

```sh
python scripts/task_loop.py init --task-id chapter-1 --task-text "Prepare chapter 1 of the thesis"
python scripts/task_loop.py validate --task-id chapter-1
python scripts/task_loop.py status --task-id chapter-1
```

Only `init`, `status` and `validate` are implemented as helper commands. The other workflow phases are agent actions described in `SKILL.md` and [references/COMMANDS.md](references/COMMANDS.md). Structural validation does not establish that a claim is true.

## Repository layout

| Path | Purpose |
|---|---|
| `SKILL.md` | Main agent instructions |
| `scripts/task_loop.py` | Task initialization and structural validation |
| `references/REFERENCE.md` | Command and artifact reference |
| `references/SCHEMAS.md` | Artifact schemas and validation rules |
| `references/COMMANDS.md` | Prompts for workflow phases |
| `references/SUBAGENTS.md` | Role boundaries |
| `docs/` | Workflow, quality gates, roles and usage |
| `templates/` | Task file templates |

## Task artifacts

```text
.agents/tasks/<TASK_ID>/
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

Main-line artifacts are the specification, requirements, writing/advisor preferences, approved source registry, outline, draft, claim map, quotes, evidence, feedback digest, handoff and verdict. Candidate sources, scratchpad, raw feedback and events are side-turn material.

`sources_registry.md` contains approved sources only. Candidate sources cannot be cited until approved. `feedback_log.jsonl` records raw feedback; `feedback_digest.md` records actionable hints; `scratchpad.md` holds ideas outside the accepted task. Evidence and verdicts are recorded per criterion.

## Feedback and revision

Feedback can evaluate the previous result and direct the next change. Preserve the original feedback, extract a short actionable hint, link it to the affected section/claim/file and mark it as applied or deferred. Keep the revision history instead of replacing it with a general success statement.

## Rules and limitations

- Do not invent links, quotations, DOI values or bibliographic details.
- Cite approved sources only; keep candidates separate.
- Do not expand the draft during verification or let the verifier edit it.
- Apply targeted revisions instead of broad rewrites.
- Update task artifacts before resetting context.

Provide a chapter outline, notes, accessible sources and institutional/advisor requirements when available. Missing evidence should slow the workflow rather than produce unsupported text.

## Further documentation

- [Complete workflow](docs/WORKFLOW.md)
- [Quality gates](docs/QUALITY_GATES.md)
- [Roles](docs/ROLES.md)
- [Usage prompts](docs/USAGE_PROMPTS.md)

This repository packages a workflow and structural helper; factual verification still requires checking the actual sources.
