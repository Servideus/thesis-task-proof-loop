# thesis-task-proof-loop

A repository for a Codex-style skill that helps with **academic writing workflows** through a controlled loop of planning, source control, drafting from approved materials, review, and minimal revision.

## Purpose

This repository contains rules, roles, templates, and usage prompts for a disciplined research-writing loop:

**freeze requirements -> lock approved sources -> draft from approved materials -> map claims to sources -> fresh review -> minimal fixes -> re-review**

The goal is to support academic writing with traceability and source discipline.

## What the skill should help with

- freeze the scope of a chapter or section;
- organize approved sources;
- draft from user-provided requirements, notes, and approved sources;
- map substantive claims to sources;
- review structure, logic, and citation discipline;
- apply minimal revisions instead of rewriting everything.

## What it must never do

- invent citations;
- pretend to have read inaccessible sources;
- fabricate quotations, page numbers, DOI, or URLs;
- silently drift away from the approved outline.

## Main files

- `SKILL.md` - main operational instructions for the agent.
- `docs/ROLES.md` - role definitions and responsibilities.
- `docs/WORKFLOW.md` - end-to-end loop and stop conditions.
- `docs/QUALITY_GATES.md` - acceptance criteria and review checklist.
- `docs/USAGE_PROMPTS.md` - prompts to invoke the skill from Codex.
- `templates/` - templates for runtime task artifacts.

## Expected runtime artifacts in the target repository

```text
.agents/tasks/<TASK_ID>/
  spec.md
  requirements.md
  sources_registry.md
  outline.md
  draft.md
  claim_source_map.csv
  evidence.md
  problems.md
  revision_log.md
  verdict.json
```

## Recommended usage

Use this repository as a skill source for Codex. The skill should be invoked inside the target research-writing repository and should create runtime files under `.agents/tasks/<TASK_ID>/`.

See `docs/USAGE_PROMPTS.md` for examples.
