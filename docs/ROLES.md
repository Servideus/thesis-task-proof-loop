# Роли

Даже если весь цикл делает один агент, роли должны быть концептуально разделены.

## 1. Замораживатель задачи

Входы:
- запрос пользователя
- требования вуза
- требования научрука
- существующий план

Выходы:
- `spec.md`
- `requirements.md`
- при необходимости `writing_profile.md`
- при необходимости `advisor_preferences.md`

Обязанности:
- определить scope
- определить non-goals
- зафиксировать AC
- зафиксировать обязательные ограничения

Нельзя:
- писать `draft.md`
- молча догадываться за пользователя

## 2. Куратор источников

Входы:
- утверждённые пользователем материалы
- библиографические данные
- заметки и выписки

Выходы:
- `sources_registry.md`
- `candidate_sources.md`

Обязанности:
- отделять approved sources от candidate sources
- отмечать уровень доверия и доступность полного текста
- ограничивать допустимое использование слабых источников

Нельзя:
- молча повышать candidate source до approved
- считать неполную ссылку проверенной ссылкой

## 3. Построитель outline

Входы:
- `spec.md`
- `requirements.md`
- `sources_registry.md`
- профили письма

Выходы:
- `outline.md`

Обязанности:
- строить канонические `section_id`
- задавать planned claims
- прикреплять допустимые `source_id`

Нельзя:
- добавлять крупные разделы вне scope
- ломать стабильность `section_id` без причины

## 4. Драфтер

Входы:
- `spec.md`
- `requirements.md`
- `writing_profile.md`
- `advisor_preferences.md`
- `sources_registry.md`
- `outline.md`

Выходы:
- `draft.md`

Обязанности:
- писать только по approved materials
- держать термины и логику
- соотносить текст с outline ids

Нельзя:
- использовать candidate sources
- выдумывать локаторы
- подменять слабую опору сильным выводом

## 5. Маппер claims

Входы:
- `draft.md`
- `sources_registry.md`
- `outline.md`

Выходы:
- `claim_source_map.csv`
- `quotes.md`

Обязанности:
- связать нетривиальные claims с `source_id`
- отмечать локаторы только если они реально доступны

Нельзя:
- добавлять новые claims вместо mapping
- прятать пробелы в доказательствах

## 6. Дистиллятор сигналов

Входы:
- raw user feedback
- advisor comments
- verifier remarks
- self-check observations

Выходы:
- `feedback_log.jsonl`
- `feedback_digest.md`

Обязанности:
- классифицировать signal как evaluative / directive / mixed
- сохранять raw feedback отдельно от distilled hint
- формировать короткие actionable hints

Нельзя:
- считать raw feedback готовой инструкцией без фильтрации
- терять связь с affected section / claim / file

## 7. Проверяющий

Входы:
- вся папка задачи

Выходы:
- `verdict.json`
- `problems.md`
- при необходимости заметки в `evidence.md`

Обязанности:
- проверять AC и quality gates
- проверять scope, sources, traceability, logic, profiles, feedback assimilation

Нельзя:
- чинить текст прямо во время проверки
- игнорировать отсутствие доказательств только потому, что текст звучит уверенно

## 8. Исправляющий

Входы:
- `problems.md`
- `verdict.json`
- необходимые task artifacts

Выходы:
- обновлённый `draft.md`
- обновлённый `claim_source_map.csv`
- `revision_log.md`
- обновлённые evidence/handoff artifacts

Обязанности:
- подтверждать каждый дефект перед правкой
- вносить минимальные изменения
- не ломать уже стабильные куски

Нельзя:
- делать широкий stylistic rewrite без необходимости
- забывать обновить evidence после правок

## 9. Интегратор

Входы:
- все стабильные артефакты задачи

Выходы:
- финальный согласованный пакет

Обязанности:
- синхронизировать handoff, evidence, verdict и draft
- следить, чтобы финальные claims жили в main-line files

Нельзя:
- добавлять новые содержательные утверждения в самом конце
