# Промпты для запуска

## Базовый `run`

```text
Создай субагентов. Используй $thesis-task-proof-loop run для TASK_ID chapter-1 в этом репозитории.
Если папки задачи нет, сначала выполни init и остановись.
Иначе пройди цикл:
freeze -> sources -> outline -> draft -> map -> evidence -> verify -> fix(if needed) -> evidence -> verify.

Строго соблюдай:
- approved sources живут только в sources_registry.md;
- candidate sources живут только в candidate_sources.md;
- канонические section_id должны совпадать в outline.md, draft.md и claim_source_map.csv;
- raw feedback логируется в feedback_log.jsonl;
- distilled hints фиксируются в feedback_digest.md;
- verifier работает в свежем контексте и не правит текст;
- fixer делает только минимальные правки;
- перед reset обновляй handoff.md и events.jsonl.
```

## `init`

```text
Используй $thesis-task-proof-loop init для TASK_ID chapter-1 в этом репозитории.
Сначала запусти:
python scripts/task_loop.py init --task-id chapter-1 --task-text "Подготовить главу 1 дипломной работы"
После этого кратко перечисли созданные артефакты и остановись.
```

## `freeze`

```text
Используй $thesis-task-proof-loop freeze для TASK_ID chapter-1.
Прочитай spec.md, requirements.md, writing_profile.md, advisor_preferences.md и исходную задачу.
Заморозь scope, non-goals и acceptance criteria.
Не пиши draft.md на этом шаге.
```

## `sources`

```text
Используй $thesis-task-proof-loop sources для TASK_ID chapter-1.
Утверждённые источники заноси в sources_registry.md.
Непроверенные или спорные источники заноси в candidate_sources.md.
Не цитируй candidate sources.
```

## `outline`

```text
Используй $thesis-task-proof-loop outline для TASK_ID chapter-1.
Построй outline.md с section_id вида [S1], [S1.1], ...
Для каждого раздела укажи цель, planned claims и разрешённые source_id.
```

## `draft`

```text
Используй $thesis-task-proof-loop draft для TASK_ID chapter-1.
Пиши только по approved sources, writing_profile.md, advisor_preferences.md и outline.md.
Не выходи за замороженный scope.
```

## `map`

```text
Используй $thesis-task-proof-loop map для TASK_ID chapter-1.
Обнови claim_source_map.csv и quotes.md.
Каждое нетривиальное утверждение должно получить claim_id, section_id и source_id.
```

## `verify`

```text
Используй $thesis-task-proof-loop verify для TASK_ID chapter-1.
Это свежая проверка.
Прочитай repo-local artifacts, а не длинную историю диалога.
Обнови verdict.json и problems.md.
Не правь draft.md.
```

## `fix`

```text
Используй $thesis-task-proof-loop fix для TASK_ID chapter-1.
Прочитай problems.md и verdict.json.
Подтверди каждый дефект.
Внеси минимальные правки и обнови revision_log.md, evidence.md, evidence.json, feedback_digest.md, handoff.md и events.jsonl.
```

## Только проверить структуру

```text
Используй $thesis-task-proof-loop validate для TASK_ID chapter-1.
Запусти:
python scripts/task_loop.py validate --task-id chapter-1
python scripts/task_loop.py status --task-id chapter-1
И сообщи, что сломано в структуре артефактов.
```
