<img src="img/logo/logo.png" align="right" width="150px">


# EntropyShield

**Language:**  <a href="https://github.com/loanelly/EntropyShield/blob/main/README.md"><img src="https://github.com/loanelly/EntropyShield/blob/main/img/Flags/EN1.png" height="21" align="center"/></a> <a href="https://github.com/loanelly/EntropyShield/blob/main/README_RU.md"><img src="https://github.com/loanelly/EntropyShield/blob/main/img/Flags/result.png" height="26" align="center"/></a>


**Язык:** Русский | [English](README.en.md)

# Product Strategist — ИИ-агент для решений цифровых продуктов

**Product Strategist** превращает неоднозначный запрос руководителя продукта и набор разрешённых материалов в проверяемую картину ситуации, несколько содержательно разных вариантов, согласованные продуктовую и коммуникационную стратегии, независимую критику и возобновляемое решение.

Оркестратором является агент внутри Cursor, GitHub Copilot, Claude Code или совместимой IDE. Python-скрипты выполняют детерминированные проверки, расчёты и реестры: они не создают собственный LLM-цикл.

В репозитории реализован демонстрационный кейс **Family Cloud** на синтетических данных и ограниченном публичном контексте Eurostat. Кейс явно не относится к реальным продуктам, заказчикам или данным МегаФона.

## Что умеет агент

- Уточняет решение, ЛПР, цель, аудиторию, ограничения и критерии успеха.
- Собирает факты из документов, таблиц, публичных веб-источников и описаний интерфейсов.
- Отделяет факты, гипотезы и прогнозы и ведёт граф доказательств с ссылками и уверенностью.
- Предлагает минимум три содержательно разные позиции, включая **«оставить как есть»** и **«закрыть направление»**.
- Формирует согласованные продуктовую и коммуникационную стратегии с планом проверки и защитными метриками.
- Запускает изолированную независимую критику и фиксирует решение, владельца, KPI, сроки и триггеры пересмотра.
- Сохраняет контрольную точку и продолжает работу в новом чате или IDE без повторения выполненных шагов.
- При появлении новых данных определяет затронутые решения и переводит их в статус `review_required`.

## Архитектура

```text
Cursor / GitHub Copilot / Claude Code
                  |
                  +-- AGENTS.md и адаптеры IDE
                  +-- Модульные Skills и знания
                  +-- Human-in-the-loop на ключевых выборах
                  +-- Fetch MCP и allowlist доменов
                  +-- Детерминированные Python 3.12 CLI
                  |      ingest_source / validate_evidence
                  |      calc_economics / recheck_decisions
                  |      cost_tracker
                  +-- state/ и evidence graph
                  +-- artifacts/ и журнал решений
```

Постоянные правила находятся в [`AGENTS.md`](AGENTS.md). Адаптеры для IDE: [`.cursor/rules/agent.mdc`](.cursor/rules/agent.mdc), [`.github/copilot-instructions.md`](.github/copilot-instructions.md) и [`CLAUDE.md`](CLAUDE.md).

Процедуры вынесены в [`skills/`](skills/), методическая база — в [`knowledge/`](knowledge/), а состояния и результаты разделены по [`state/`](state/) и [`artifacts/`](artifacts/). Подробная схема файлов описана в [отчёте для жюри](docs/SUBMISSION_REPORT.md).

### Актуальная карта репозитория

```text
.cursor/
  agents/adversarial-reviewer.md
  hooks.json
  mcp.json
  rules/agent.mdc
.github/
  copilot-instructions.md
artifacts/
  baseline/comparison.md
  adversarial_review.md
  economics_result.json
  options.md
  q3_economics_result.json
  recheck_report.json
  research_plan.md
  run_log.jsonl
  strategy.md
data/
  new/README.md
  new/q3_churn_update.md
  raw/demo/
    economics_input.json
    funnel_metrics.csv
    market_benchmark.md
    onboarding_screens.md
    q3_economics_sensitivity_input.json
    user_feedback.md
  source_manifest.json
docs/
  DEMO_VIDEO_SCRIPT.md
  SUBMISSION_REPORT.md
  en/
    DEMO_VIDEO_SCRIPT.md
    SUBMISSION_REPORT.md
knowledge/
  research-methods.md
  source-safety.md
  strategy-framework.md
projects/
  demo/
    DEMO_CASE_PACK.md
    README.md
    brief.md
schemas/
  decisions-registry.schema.json
  evidence.schema.json
  source-manifest.schema.json
  workflow-state.schema.json
scripts/
  calc_economics.py
  cost_tracker.py
  cursor_hook.py
  ingest_source.py
  recheck_decisions.py
  validate_evidence.py
skills/
  adversarial-review/SKILL.md
  data-analysis/SKILL.md
  decision-followup/SKILL.md
  intake/SKILL.md
  research/SKILL.md
  strategy/SKILL.md
  synthetic-respondents/SKILL.md
  ux-multimodal-audit/SKILL.md
state/
  decision_log.md
  decisions_registry.json
  evidence_graph.json
  workflow_state.json
tests/
  test_tools.py
AGENTS.md
CLAUDE.md
README.md
README.en.md
.env.example
.gitignore
```

Встроенные папки IDE и временные каталоги (`.idea/`, `.vscode/`, `__pycache__/`, `.pytest_cache/`) исключены из публикации через [`.gitignore`](.gitignore).

### MCP и Hooks

- [`.cursor/mcp.json`](.cursor/mcp.json) подключает стандартный MCP-сервер Fetch и разрешённые публичные домены.
- [`.cursor/hooks.json`](.cursor/hooks.json) автоматически запускает проверки после редактирования стратегии и перепроверяет решения при открытии workspace или появлении новых файлов.
- Внешний контент считается недоверенными данными. Правила изолируются в [`knowledge/source-safety.md`](knowledge/source-safety.md), а источник оборачивается скриптом [`scripts/ingest_source.py`](scripts/ingest_source.py).

### Независимая критика

Этап adversarial review запускается отдельным субагентом с ограниченным контекстом: ему передаются только бриф, граф доказательств, варианты и стратегия. История генерации не передаётся. Конфигурация: [`.cursor/agents/adversarial-reviewer.md`](.cursor/agents/adversarial-reviewer.md), процедура: [`skills/adversarial-review/SKILL.md`](skills/adversarial-review/SKILL.md).

## Быстрый старт за 3 минуты

**Требования:** Python 3.12 и Cursor, GitHub Copilot, Claude Code или совместимая IDE. Для тестов и детерминированных скриптов API-модель и платные сервисы не нужны.

1. Откройте папку репозитория как доверенный workspace.
2. В Cursor настройте Fetch MCP из [`.cursor/mcp.json`](.cursor/mcp.json), если нужен публичный веб-поиск.
3. Запустите проверку и демо:

```powershell
python --version
python -m unittest discover -s tests -v
python scripts/validate_evidence.py
python scripts/calc_economics.py data/raw/demo/economics_input.json
python scripts/calc_economics.py data/raw/demo/q3_economics_sensitivity_input.json
python scripts/recheck_decisions.py
```

На старте демо решение `DEMO-D-001` находится на пересмотре. Новый синтетический файл [`data/new/q3_churn_update.md`](data/new/q3_churn_update.md) опровергает допущение о постоянном удержании и должен менять статус решения только после проверки человеком.

Дополнительные переменные окружения перечислены в [`.env.example`](.env.example). Реальные ключи не хранятся в репозитории и задаются только через локальные секретные хранилища IDE или оболочки.

## Демо-кейс Family Cloud

Фиктивный сервис облачного хранения для абонентов мобильного оператора столкнулся с падением trial-to-paid конверсии в синтетической таблице с 18% до 11%.

Исходные данные и границы подробно описаны в [`projects/demo/README.md`](projects/demo/README.md):

- [`data/raw/demo/funnel_metrics.csv`](data/raw/demo/funnel_metrics.csv) — синтетическая таблица когорт;
- [`data/raw/demo/user_feedback.md`](data/raw/demo/user_feedback.md) — вымышленные фрагменты отзывов;
- [`data/raw/demo/onboarding_screens.md`](data/raw/demo/onboarding_screens.md) — описания вымышленного онбординга;
- [`data/raw/demo/market_benchmark.md`](data/raw/demo/market_benchmark.md) — контекст публичных данных Eurostat;
- [`data/raw/demo/economics_input.json`](data/raw/demo/economics_input.json) — явно помеченные сценарные допущения;
- [`data/raw/demo/q3_economics_sensitivity_input.json`](data/raw/demo/q3_economics_sensitivity_input.json) — проверка чувствительности к снижению retention.

Ключевые артефакты:

- Бриф: [`projects/demo/brief.md`](projects/demo/brief.md)
- План исследования: [`artifacts/research_plan.md`](artifacts/research_plan.md)
- Граф доказательств: [`state/evidence_graph.json`](state/evidence_graph.json)
- Варианты решений: [`artifacts/options.md`](artifacts/options.md)
- Стратегия: [`artifacts/strategy.md`](artifacts/strategy.md)
- Независимая критика: [`artifacts/adversarial_review.md`](artifacts/adversarial_review.md)
- Экономика: [`artifacts/economics_result.json`](artifacts/economics_result.json)
- Проверка по новому риску: [`artifacts/q3_economics_result.json`](artifacts/q3_economics_result.json)
- Реестр решения: [`state/decisions_registry.json`](state/decisions_registry.json)
- Журнал решений: [`state/decision_log.md`](state/decision_log.md)

Демо не доказывает реальный спрос, retention, ARPU или эффективность интерфейса. Оно проверяет сквозной workflow, воспроизводимость расчёта, цитирование фактов и автоматический пересмотр решений.

## Инструменты

- [`scripts/ingest_source.py`](scripts/ingest_source.py) — упаковка UTF-8 источника с provenance и SHA-256;
- [`scripts/validate_evidence.py`](scripts/validate_evidence.py) — проверка фактов, evidence IDs, уверенности и точных локаторов;
- [`scripts/calc_economics.py`](scripts/calc_economics.py) — расчёт LTV, CAC и срока окупаемости при явных единицах и периодах;
- [`scripts/recheck_decisions.py`](scripts/recheck_decisions.py) — хеширование и поиск связанных новых данных;
- [`scripts/cost_tracker.py`](scripts/cost_tracker.py) — сравнительный учёт времени, токенов, стоимости, шагов и качества.

Все скрипты используют только стандартную библиотеку Python 3.12.

```powershell
python -m unittest discover -s tests -v
```

На текущий момент набор содержит 19 автотестов. Cost tracker работает в режимах `add` и `compare`; подробный протокол парного замера и измеренная локальная фаза демо находятся в [`artifacts/baseline/comparison.md`](artifacts/baseline/comparison.md).

## Продолжение работы

Агент сначала читает [`state/workflow_state.json`](state/workflow_state.json), сверяет сохранённые хеши и продолжает только незавершённое действие. Решения хранятся в [`state/decisions_registry.json`](state/decisions_registry.json), а изменения протоколируются в [`state/decision_log.md`](state/decision_log.md).

При добавлении нового файла в [`data/new/`](data/new/) запускается хук или команда `recheck_decisions.py`. Скрипт отмечает затронутые решения, но не меняет их без человеко-читаемой и агентской оценки новых данных.

## Схема знаний и проверок

- [`knowledge/research-methods.md`](knowledge/research-methods.md) — надёжность источников, пробелы и falsification-критерии;
- [`knowledge/strategy-framework.md`](knowledge/strategy-framework.md) — продуктовая и коммуникационная стратегия, retention, ARPU, cannibalization и plan experiment;
- [`knowledge/source-safety.md`](knowledge/source-safety.md) — prompt injection, ПДн, секреты и закрытые данные;
- [`schemas/`](schemas/) — JSON-схемы графа доказательств, checkpoint, реестра решений и манифеста.

## Сравнение с обычным чатом

[`artifacts/baseline/comparison.md`](artifacts/baseline/comparison.md) описывает протокол парного измерения времени, стоимости, шагов и качества. В репозитории не представлены вымышленные цифры сравнения: реально доступные IDE-телеметрия и matched plain-chat baseline отсутствовали.

`cost_tracker.py` не получает биллинг провайдера автоматически. Для честного отчёта нужно добавить фактические токены и стоимость каждого measured-run.

## Документация для сдачи 

- Единый пакет демо-кейса: [`projects/demo/DEMO_CASE_PACK.md`](projects/demo/DEMO_CASE_PACK.md)
- Baseline-сравнение: [`artifacts/baseline/comparison.md`](artifacts/baseline/comparison.md)
- Полный отчёт по архитектуре и ограничениям: [`docs/SUBMISSION_REPORT.md`](docs/SUBMISSION_REPORT.md)
- Сценарий видеодемонстрации до 10 минут: [`docs/DEMO_VIDEO_SCRIPT.md`](docs/DEMO_VIDEO_SCRIPT.md)
- Английский отчёт и сценарий: [`docs/en/SUBMISSION_REPORT.md`](docs/en/SUBMISSION_REPORT.md), [`docs/en/DEMO_VIDEO_SCRIPT.md`](docs/en/DEMO_VIDEO_SCRIPT.md)
- Журнал реального запуска: [`artifacts/run_log.jsonl`](artifacts/run_log.jsonl)
- English version: [README.en.md](README.en.md)
