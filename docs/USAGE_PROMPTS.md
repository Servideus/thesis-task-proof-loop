# Usage Prompts

## Default prompt

```text
Spawn subagents. Use $thesis-task-proof-loop to continue the task described below in this repository.
Reuse the matching task if it already exists; otherwise initialize it first.
Follow the skill strictly:
- freeze the task;
- lock approved sources;
- build or confirm the outline;
- draft only from approved materials;
- map substantive claims to sources;
- review in a fresh context;
- apply only targeted fixes;
- stop with FAIL if the evidence base is insufficient.
```

## Prompt for building a section from approved materials

```text
Spawn subagents. Use $thesis-task-proof-loop in this repository.
Task: prepare a structured section from the approved outline, notes, and sources already present here.
Requirements:
- do not use unapproved sources;
- do not invent bibliographic data;
- keep all runtime artifacts under .agents/tasks/<TASK_ID>/;
- produce draft.md, claim_source_map.csv, evidence.md, and verdict.json.
```

## Prompt for review only

```text
Use $thesis-task-proof-loop in review mode for the existing task folder.
Do not rewrite the section broadly.
Check quality gates, update evidence.md, write verdict.json, and list concrete defects in problems.md.
```

## Prompt for targeted revision

```text
Use $thesis-task-proof-loop in fix mode for the existing task folder.
Read problems.md and apply only targeted corrections.
Update revision_log.md and rerun review.
```
