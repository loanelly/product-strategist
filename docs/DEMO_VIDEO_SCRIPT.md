**Язык:** Русский | [English](en/DEMO_VIDEO_SCRIPT.md)

# Сценарий демонстрационного видео (целевой тайминг: 8–9 минут)

Записывайте в Cursor или совместимой IDE, где видны
[`AGENTS.md`](../AGENTS.md), терминал, статус hooks и отдельный reviewer.
Используйте только fictional demo-проект. Не показывайте ключи, персональные
данные, закрытые файлы или утверждения о реальном продукте МегаФона.

## 0:00–0:45 — Сфера и безопасность

Откройте [`projects/demo/README.md`](../projects/demo/README.md) и скажите:
«Это вымышленный сервис облачного хранения и синтетическая таблица когорт.
Публичен только контекст Eurostat, который не является сопоставимым
benchmark trial-to-paid конверсии».

## 0:45–1:45 — Запрос и workflow

Покажите [`projects/demo/brief.md`](../projects/demo/brief.md), затем
[`AGENTS.md`](../AGENTS.md) и
[`skills/intake/SKILL.md`](../skills/intake/SKILL.md). В новом IDE-чате
вставьте:

> Read AGENTS.md and skills/intake/SKILL.md. Resume projects/demo from
> state/workflow_state.json. Summarize the saved stage, next action, fictional
> data boundary, and any human approval required. Do not repeat completed
> stages or infer real customer demand.

Покажите восстановленную контрольную точку и остановку на согласовании.
Поясните, что реальный проект не начал бы исследование до одобрения брифа
решающим человеком.

## 1:45–3:00 — Источники и evidence

Покажите [`data/source_manifest.json`](../data/source_manifest.json),
один синтетический source-файл и
[`state/evidence_graph.json`](../state/evidence_graph.json). Выполните:

```powershell
python scripts/validate_evidence.py
```

Объясните, что facts привязаны к source IDs и точным местам, а synthetic
respondent-ответы не являются доказательством спроса.

## 3:00–4:00 — Экономика

Выполните:

```powershell
python scripts/calc_economics.py data/raw/demo/economics_input.json
```

Покажите [`artifacts/economics_result.json`](../artifacts/economics_result.json).
Объясните: данные вымышлены, LTV не дисконтирован и расчёт исключает
service cost и cannibalization.

## 4:00–5:00 — Варианты и рекомендация

Покажите [`artifacts/options.md`](../artifacts/options.md) и
[`artifacts/strategy.md`](../artifacts/strategy.md). Назовите варианты
«оставить как есть», «закрыть направление», изолированное clarification
разрешений и отдельный terms/value-тест. Поясните human gates,
falsification-критерии и что 13.5% является planning target, не forecast.

## 5:00–6:00 — Независимый скептик

Покажите конфигурацию отдельного Adversarial Review и
[`artifacts/adversarial_review.md`](../artifacts/adversarial_review.md).
Объясните, что субагент не получил историю генерации: он сократил тест до
permission-only intervention, усилил условия power analysis и не допустил
публикации неподтверждённых product promises.

## 6:00–7:00 — Остановка и продолжение в новом чате

Покажите [`state/workflow_state.json`](../state/workflow_state.json).
Откройте новый IDE-чат и вставьте:

> Read AGENTS.md, the relevant decision-followup skill, and
> state/workflow_state.json. Continue from next_action only. Check for new
> material and explain which decision, if any, requires human review. Do not
> treat synthetic data as real or change an adopted decision without approval.

Покажите восстановление этапа 8 и ожидание human approval.

## 7:00–8:15 — Пересмотр по новым данным

В демо уже подготовлен fixture с 78% retention и решение помечено
`review_required`. Чтобы показать чистый до/после на временной копии реестра:

```powershell
Copy-Item state\decisions_registry.json "$env:TEMP\demo-decisions.json"
python -c "import json,os; p=os.path.join(os.environ['TEMP'],'demo-decisions.json'); d=json.load(open(p,encoding='utf-8')); d['decisions'][0]['status']='adopted'; d['decisions'][0]['review_reasons']=[]; d['processed_files']={}; json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
python scripts/recheck_decisions.py --registry "$env:TEMP\demo-decisions.json" --new-dir data/new
python -c "import json,os; print(json.load(open(os.path.join(os.environ['TEMP'],'demo-decisions.json'),encoding='utf-8'))['decisions'][0]['status'])"
```

Поясните: source-ID/watch-term match лишь ставит решение в
`review_required`; скрипт не проверяет истинность факта и не меняет решение
самостоятельно. 78% retention является синтетическим тестовым значением.

## 8:15–9:00 — Повторяемость и честные ограничения

Выполните:

```powershell
python -m unittest discover -s tests -v
```

Покажите [`artifacts/baseline/comparison.md`](../artifacts/baseline/comparison.md).
Скажите, что matched ordinary-chat baseline и provider-токены не были доступны,
поэтому никаких заявлений о реальном приросте скорости или снижении стоимости
не сделано. Поясните, как регистрировать реальные paired runs через
[`scripts/cost_tracker.py`](../scripts/cost_tracker.py).
