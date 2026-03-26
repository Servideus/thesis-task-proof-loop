# Reference

When examples below mention `scripts/task_loop.py`, that path is relative to this skill root.
Run the script while your shell working directory is inside the target repository.

## Recommended install locations

Project skill:
- `.agents/skills/thesis-task-proof-loop/`
- `.claude/skills/thesis-task-proof-loop/`

Personal skill:
- `$HOME/.agents/skills/thesis-task-proof-loop/`
- `~/.claude/skills/thesis-task-proof-loop/`

The script writes repo-local artifacts into the current repository, not into the skill directory.

## Repo files created by `init`

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

## Commands

Initialize a task:

```bash
python scripts/task_loop.py init --task-id chapter-1 --task-text "Подготовить главу 1 дипломной работы"
```

Seed from a file:

```bash
python scripts/task_loop.py init --task-id chapter-1 --task-file docs/task.md
```

Write managed guidance into `AGENTS.md` and `CLAUDE.md`:

```bash
python scripts/task_loop.py init --task-id chapter-1 --guides both
```

Validate the artifact set:

```bash
python scripts/task_loop.py validate --task-id chapter-1
```

Summarize status and infer the next step:

```bash
python scripts/task_loop.py status --task-id chapter-1
```

## Workflow commands interpreted by the skill

The skill treats the following words as workflow commands when the user invokes it:

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

`init`, `status`, and `validate` are script-backed.
The remaining commands are role-driven workflow phases executed by the agent against the repo-local task folder.
