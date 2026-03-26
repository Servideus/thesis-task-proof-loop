# thesis-task-proof-loop

Репозиторий со skill для Codex-подобных агентов, который помогает вести длинные академические задачи через repo-local workflow с явными артефактами, структурированным feedback loop и свежей проверкой.

Базовая идея:

```text
init -> freeze -> sources -> outline -> draft -> map -> evidence -> verify -> fix -> evidence -> verify
```

Цель не в том, чтобы агент писал "убедительно", а в том, чтобы он писал управляемо:
- замораживал рамку задачи
- отделял approved sources от candidate sources
- держал канонические `section_id`
- маппил содержательные claims к источникам
- логировал evaluative и directive feedback
- проверял результат в свежем контексте
- правил текст минимальными безопасными диффами

## Что изменилось в workflow

Теперь это не только набор правил, но и исполняемая инфраструктура:
- `scripts/task_loop.py` умеет `init`, `status`, `validate`
- появились строгие схемы артефактов в `references/SCHEMAS.md`
- добавлены недостающие шаблоны `outline.md`, `draft.md`, `quotes.md`
- появились `writing_profile.md` и `advisor_preferences.md`
- появились `candidate_sources.md` и `scratchpad.md` для side-turn материалов
- появились `feedback_log.jsonl`, `feedback_digest.md`, `events.jsonl`
- `verdict.json` и `evidence.json` теперь criterion-level, а не только "всё хорошо / всё плохо"

## Основные файлы skill

- `SKILL.md` — главные инструкции для агента
- `scripts/task_loop.py` — инициализация и валидация repo-local task folder
- `references/REFERENCE.md` — справка по командам и структуре
- `references/SCHEMAS.md` — схемы и правила валидации артефактов
- `references/COMMANDS.md` — command-level prompt shapes
- `references/SUBAGENTS.md` — границы ролей
- `docs/` — человеческая документация по workflow, quality gates и usage
- `templates/` — шаблоны файлов задачи

## Ожидаемая структура задачи

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

## Main-line vs side-turns

Main-line артефакты:
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

Side-turn артефакты:
- `candidate_sources.md`
- `scratchpad.md`
- `feedback_log.jsonl`
- `events.jsonl`

Правило:
- в `sources_registry.md` живут только approved sources
- в `candidate_sources.md` живут материалы, которые нельзя цитировать до одобрения
- в `feedback_log.jsonl` лежит raw next-state signal
- в `feedback_digest.md` лежит distilled hint
- в `scratchpad.md` лежат побочные идеи, которые не считаются частью задачи

## Быстрый старт

### 1. Инициализировать задачу

```bash
python scripts/task_loop.py init --task-id chapter-1 --task-text "Подготовить главу 1 дипломной работы"
```

### 2. Проверить структуру

```bash
python scripts/task_loop.py validate --task-id chapter-1
```

### 3. Посмотреть статус и следующий шаг

```bash
python scripts/task_loop.py status --task-id chapter-1
```

## Workflow commands

Skill понимает команды:
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

`init`, `status`, `validate` поддерживаются скриптом.
Остальные команды — это фазы workflow, которые агент выполняет по инструкциям из `SKILL.md` и `references/COMMANDS.md`.

## Почему здесь есть feedback loop

Репозиторий теперь использует идею next-state signals:
- user/advisor/verifier feedback несёт evaluative signal: стало лучше или хуже
- тот же feedback часто несёт directive signal: что именно нужно было сделать иначе

Поэтому workflow теперь заставляет:
1. сохранять raw feedback отдельно
2. дистиллировать короткий actionable hint
3. связывать hint с affected section / claim / file
4. явно помечать, применён ли сигнал или отложен

Это уменьшает хаос в длинных итерациях и даёт более честную историю исправлений.

## Жёсткие правила

- не выдумывать ссылки, цитаты, DOI, URL и библиографию
- не ссылаться на неутверждённые источники
- не путать candidate sources с approved sources
- не расширять драфт на шаге проверки
- не давать verifier править текст
- не делать широкий рерайт вместо точечных правок
- не сбрасывать контекст до обновления task artifacts

## Документация

- `docs/WORKFLOW.md` — полный цикл
- `docs/QUALITY_GATES.md` — критерии качества
- `docs/ROLES.md` — роли и границы ответственности
- `docs/USAGE_PROMPTS.md` — примеры запуска

## Практическая рекомендация

Этот skill работает лучше, если в репозитории уже лежат:
- план диплома или хотя бы план главы
- заметки и выписки
- файлы источников или проверяемые библиографические данные
- требования вуза и научрука

Если этого нет, workflow должен замедляться, а не фантазировать.
