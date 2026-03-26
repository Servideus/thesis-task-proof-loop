# Рабочий цикл

## Общая схема

```text
init -> freeze -> sources -> outline -> draft -> map -> evidence -> verify -> fix -> evidence -> verify
```

Где:
- `init` создаёт repo-local task folder
- `freeze` стабилизирует рамку задачи
- `sources` отделяет approved sources от candidate sources
- `outline` создаёт канонические section ids
- `draft` пишет текст
- `map` приземляет claims на источники
- `evidence` собирает доказательства и digest feedback signals
- `verify` делает свежую проверку
- `fix` вносит минимальные исправления

## 1. Инициализировать или переиспользовать задачу

Работай внутри:

```text
.agents/tasks/<TASK_ID>/
```

Если папки задачи нет:

```bash
python scripts/task_loop.py init --task-id <TASK_ID> --task-text "<task text>"
```

`init` создаёт обязательные артефакты и `raw/`.
После `init` можно запускать `validate` и `status`.

## 2. Заморозить задачу

Заполни:
- `spec.md`
- `requirements.md`
- `writing_profile.md`
- `advisor_preferences.md`

До перехода дальше должны быть зафиксированы:
- границы раздела или главы
- non-goals
- AC1, AC2, ...
- требования оформления
- требования по стилю письма
- требования научрука, если они известны

Не начинай писать `draft.md`, пока заморозка не завершена.

## 3. Зафиксировать approved sources

Заполни:
- `sources_registry.md`
- `candidate_sources.md`, если есть спорные или непроверенные материалы

Разделяй:
- сильные approved sources
- слабые background sources
- неполные или частично доступные материалы
- candidate sources, которые ещё нельзя использовать как доказательную опору

Правило:
- `sources_registry.md` можно цитировать
- `candidate_sources.md` нельзя цитировать до переноса в approved

## 4. Построить канонический outline

Создай `outline.md` с `section_id` в заголовках:

```text
## [S1] ...
## [S1.1] ...
```

Каждый section должен содержать:
- цель
- planned claims
- разрешённые `source_id`

Эти `section_id` затем обязаны совпадать в `draft.md` и `claim_source_map.csv`.

## 5. Написать драфт

Создай или обнови `draft.md`.

Используй только:
- approved sources
- замороженные требования
- writing profile
- advisor preferences
- пользовательские заметки и выписки

Различай:
- факт
- интерпретацию
- вывод

Если опора слабая, ослабляй утверждение или помечай пробел явно.

## 6. Связать claims с источниками

Создай или обнови:
- `claim_source_map.csv`
- `quotes.md`, если использованы прямые цитаты

Каждое нетривиальное утверждение должно иметь:
- `claim_id`
- `section_id`
- `source_id` или несколько `source_id`
- локатор, только если он реально доступен

## 7. Собрать evidence и feedback digest

Создай или обнови:
- `evidence.md`
- `evidence.json`
- `feedback_digest.md`
- `events.jsonl`

На этом шаге:
- оцени AC по отдельности
- оцени quality gates по отдельности
- кратко зафиксируй риски и пробелы
- запиши рекомендуемый следующий шаг

## 8. Обработать next-state signals

Каждый значимый user / advisor / verifier signal должен пройти через два слоя:

1. raw log в `feedback_log.jsonl`
2. distilled hint в `feedback_digest.md`

Классифицируй сигнал как:
- `evaluative`
- `directive`
- `mixed`

Не используй raw feedback как финальную инструкцию без дистилляции.

## 9. Подготовить handoff

Перед reset или сменой роли обнови:
- затронутые артефакты
- `feedback_digest.md`
- `handoff.md`
- `events.jsonl`

В `handoff.md` зафиксируй:
- что стабильно
- что спорно
- какие signals уже применены
- что делать следующему агенту
- что нельзя трогать без причины

## 10. Провести fresh verification

Создай или обнови:
- `verdict.json`
- `problems.md`

Проверяющий читает task artifacts, а не длинную историю сообщений.
Проверяющий не правит `draft.md` во время проверки.

Проверка должна смотреть минимум на:
- соответствие scope
- соответствие outline
- дисциплину по источникам
- полноту claim mapping
- правдоподобие локаторов и цитат
- логику
- alignment с `writing_profile.md` и `advisor_preferences.md`
- усвоение feedback signals

## 11. Внести точечные правки

Если verdict не `PASS`, исправляющий:
- читает `problems.md`
- подтверждает каждый дефект
- вносит минимальные правки
- обновляет `revision_log.md`
- обновляет `evidence.md` и `evidence.json`
- обновляет `feedback_digest.md`, `handoff.md`, `events.jsonl`

Широкий рерайт запрещён без отдельной причины.

## 12. Повторять или остановиться

Повторяй цикл до одного из исходов:
- `PASS`
- `PASS_WITH_WARNINGS`
- честный `FAIL`

## Когда нужен обязательный reset

Сбрасывай контекст обязательно:
- при смене роли
- после итерации `draft -> verify -> fix`
- при переходе к новой крупной главе или разделу
- когда контекст засорён старыми версиями и спорящими гипотезами

Не сбрасывай контекст:
- внутри короткой локальной правки
- пока текущее состояние не выгружено в task artifacts

## Условия остановки

Возвращай `FAIL`, если:
- approved sources недостаточны
- требования конфликтуют
- ключевые цитаты или ссылки нельзя приземлить
- задача требует догадок вместо доказательств
- пользователь требует уверенности, которую источники не поддерживают

## Проверка структуры

Перед заявлением, что workflow в порядке, запускай:

```bash
python scripts/task_loop.py validate --task-id <TASK_ID>
python scripts/task_loop.py status --task-id <TASK_ID>
```
