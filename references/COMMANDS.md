# Commands

Use these command shapes when the user invokes the skill.
Treat the first workflow word after the skill name as the command.

## `init`

Goal:
- create `.agents/tasks/TASK_ID/`
- seed required artifacts
- stop after initialization

Prompt shape:

```text
Используй $thesis-task-proof-loop init для TASK_ID <TASK_ID> в этом репозитории.
Если папки задачи ещё нет, создай её и сиди в ней.
Сначала запусти:
python scripts/task_loop.py init --task-id <TASK_ID> --task-text "<исходная формулировка задачи>"
После этого коротко сообщи, какие артефакты созданы, и остановись.
```

## `freeze`

Goal:
- fill `spec.md` and `requirements.md`
- freeze acceptance criteria and non-goals
- stop if the task is still ambiguous

Prompt shape:

```text
Используй $thesis-task-proof-loop freeze для существующей папки задачи <TASK_ID>.
Прочитай spec.md, requirements.md, writing_profile.md, advisor_preferences.md и исходную задачу.
Заполни и заморозь:
- цель
- границы
- non-goals
- AC1, AC2, ...
- обязательные требования вуза и пользователя
Не пиши draft.md на этом шаге.
```

## `sources`

Goal:
- register approved sources in `sources_registry.md`
- park unapproved or speculative materials in `candidate_sources.md`

Prompt shape:

```text
Используй $thesis-task-proof-loop sources для <TASK_ID>.
Разрешено обновлять только sources_registry.md, candidate_sources.md, evidence.md, feedback_digest.md и handoff.md.
Не ссылайся на source_id, которого нет в sources_registry.md.
Если источник недоступен или сомнителен, пометь это явно.
```

## `outline`

Goal:
- create `outline.md` with canonical section ids

Prompt shape:

```text
Используй $thesis-task-proof-loop outline для <TASK_ID>.
Построй outline.md с каноническими section_id вида [S1], [S1.1], ...
Для каждого раздела укажи:
- цель
- planned claims
- разрешённые source_id
Не начинай писать полный текст раздела.
```

## `draft`

Goal:
- update `draft.md`
- keep section ids aligned with the outline

Prompt shape:

```text
Используй $thesis-task-proof-loop draft для <TASK_ID>.
Пиши только по утверждённым источникам, профилю письма и замороженным требованиям.
Сохраняй section_id из outline.md.
Если доказательств мало, ослабляй формулировку или оставляй явную пометку о пробеле.
```

## `map`

Goal:
- update `claim_source_map.csv`
- update `quotes.md` when direct quotes are used

Prompt shape:

```text
Используй $thesis-task-proof-loop map для <TASK_ID>.
Сопоставь каждое нетривиальное утверждение из draft.md с source_id в claim_source_map.csv.
Если использована прямая цитата, обнови quotes.md.
Не добавляй новые содержательные утверждения на этом шаге.
```

## `evidence`

Goal:
- refresh `evidence.md`, `evidence.json`, `feedback_digest.md`, `events.jsonl`
- do not widen production text

Prompt shape:

```text
Используй $thesis-task-proof-loop evidence для <TASK_ID>.
Не переписывай широко draft.md.
Оцени каждый AC и каждый ключевой quality gate отдельно.
Собери факты, риски, пробелы и рекомендуемый следующий шаг.
```

## `verify`

Goal:
- run a fresh-session verification
- write `verdict.json` and `problems.md`

Prompt shape:

```text
Используй $thesis-task-proof-loop verify для <TASK_ID>.
Это должна быть свежая проверка.
Читай только repo-local artifacts, а не длинную историю сообщений.
Не чини текст во время проверки.
Запиши verdict.json и problems.md.
```

## `fix`

Goal:
- apply the smallest safe fix set from `problems.md`
- refresh evidence artifacts after the fix

Prompt shape:

```text
Используй $thesis-task-proof-loop fix для <TASK_ID>.
Прочитай только spec.md, requirements.md, writing_profile.md, advisor_preferences.md, verdict.json, problems.md и нужные файлы задачи.
Подтверди каждый дефект перед правкой.
Внеси минимальные изменения.
После правок обнови evidence.md, evidence.json, revision_log.md, feedback_digest.md, handoff.md и events.jsonl.
Не подписывай финальный PASS самостоятельно.
```

## `run`

Goal:
- execute the full loop serially

Prompt shape:

```text
Используй $thesis-task-proof-loop run для <TASK_ID>.
Если папки задачи нет, сначала выполни init и остановись.
Иначе пройди по шагам:
freeze -> sources -> outline -> draft -> map -> evidence -> verify -> fix(if needed) -> evidence -> verify
После каждого крупного шага обновляй handoff.md, feedback_digest.md и events.jsonl.
```

## `status`

Command:

```bash
python scripts/task_loop.py status --task-id <TASK_ID>
```

## `validate`

Command:

```bash
python scripts/task_loop.py validate --task-id <TASK_ID>
```
