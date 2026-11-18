# Product Strategist — Family Cloud Demo Case Pack

**Назначение:** единый читаемый пакет для финальной демонстрации жюри.

**Статус данных:** полностью синтетический демонстрационный кейс и ограниченный публичный контекст Eurostat.
**Проектные ссылки:** [бриф](brief.md) · [исходные данные](../../data/raw/demo/) · [граф доказательств](../../state/evidence_graph.json) · [стратегия](../../artifacts/strategy.md) · [критика](../../artifacts/adversarial_review.md)

---

## 1. Исходный бриф

### Решение

Нужно решить, стоит ли фиктивному оператору тестировать изменения trial-to-paid onboarding для облачного хранилища, оставить текущий опыт или остановить направление.

### Контекст

Синтетическая funnel-таблица показывает conversion из бесплатного триала в оплату на уровне 18% в Q1 и 11% в Q4. Все числа вымышлены. Это не результат МегаФона, не реальная конверсия и не доказательство рыночного спроса.

### ЛПР и аудитория

- Решает: вымышленный Head of Digital Products.
- Получатели: продукт, growth, finance, customer support и коммуникационная команда.
- Срок: принять решение о начале ограниченной валидации после проверки evidence и guardrails.

### Цель

- Проверить гипотезы о разнице между синтетическими Q1 и Q4.
- Предложить обратимый следующий шаг только при наличии реальной возможности проверить его.
- Основная демонстрационная метрика: paid conversions / eligible trial starters.

### Защитные метрики

- 30-дневный paid retention.
- Refund/cancellation.
- Complaints и support contacts.
- Gross contribution margin.
- Cannibalization существующих тарифов хранения.

### Границы

Используются только синтетические демонстрационные файлы и публичный контекст Eurostat. Нет закрытых данных МегаФона, персональных данных, реальных интервью или закрытых материалов. Описания экранов не являются снимками реального интерфейса.

---

## 2. Сводка источников и проверки

| ID | Тип | Материал | Что подтверждает | Ограничение |
|---|---|---|---|---|
| DEMO-FUNNEL | Таблица | [funnel_metrics.csv](../../data/raw/demo/funnel_metrics.csv) | Содержит синтетические значения Q1–Q4 и вычисляемые economics assumptions | Не является реальной телеметрией |
| DEMO-FEEDBACK | Текст | [user_feedback.md](../../data/raw/demo/user_feedback.md) | Сценарии возможных барьеров: sharing, trial terms и differentiation | Вымышленные фрагменты; не спрос и не prevalence |
| DEMO-UX | Описание | [onboarding_screens.md](../../data/raw/demo/onboarding_screens.md) | Пропущены trial length, price, renewal и permission boundary | Реального интерфейса не показывали |
| DEMO-BENCH | Публичный контекст | [market_benchmark.md](../../data/raw/demo/market_benchmark.md) | Объясняет пределы публичных Eurostat-ссылок | Не benchmark trial-to-paid |
| EUROSTAT-ARTICLE | Публичная статья | [Eurostat digital economy and society](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Digital_economy_and_society_statistics_-_households_and_individuals) | Широкий контекст цифрового использования в ЕС | Популяция, годы и вопросы не сопоставимы |
| EUROSTAT-CLOUD-DATA | Публичный dataset | [Eurostat isoc_cicci_use](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_cicci_use?lang=en) | Официально обозначен период 2014–2020 | Не цена, не paid conversion, не demand для текущего кейса |
| DEMO-Q3-UPDATE | Синтетический update | [q3_churn_update.md](../../data/new/q3_churn_update.md) | Контрпример к допущению retention=88% | Тестовый триггер пересмотра решения |

Полный реестр с хешами: [source_manifest.json](../../data/source_manifest.json).

Граф фактов и гипотез: [evidence_graph.json](../../state/evidence_graph.json).
Проверка свидетельств прошла успешно: **Evidence validation passed**; 6 из 6 фактических утверждений стратегии связаны с графом доказательств.

### Проверенные факты

- В синтетической таблице Q1 = 18%, Q4 = 11%.
- Разница составляет 7 процентных пунктов, а не доказанная причинная динамика.
- Eurostat cloud dataset ограничен периодом 2014–2020 и не является конкурентным benchmark для trial-to-paid.
- В исходном наборе нет реальной UX-сессии и реального интервью.
- Новая synthetic retention update противоречит допущению 88% и переводит решение в `review_required`.

### Решение, не принятое на основе демо

Агент не утверждает, что real customers confused, real retention падает или реальная компания должна изменить продукт. Все выводы остаются гипотезами до настоящих authorized данных.

---

## 3. Четыре варианта решения

### Вариант A — оставить как есть

- Валидировать tracking, eligibility и offer exposure.
- Не менять UI или коммуникации.
- **Плюс:** минимизирует риск интервенции против ложного decline.
- **Возражение:** реальная исправимая ошибка онбординга может продолжать снижать конверсию.
- **Решающее опровержение:** подтверждённый барьер и безопасный адресуемый тест с достаточным value.

### Вариант B — закрыть направление

- Прекратить feature investment/acquisition и подготовить безопасный wind-down или migration.
- **Плюс:** ограничивает усилия при устойчиво отрицательной economics.
- **Главное возражение:** демо не содержит validated lifetime value, cannibalization, demand или customer obligations.
- **Решающее опровержение:** verified positive incremental contribution, retention или ecosystem value.

### Вариант C — разъяснить sharing permissions

- Изолированно показать границы видимости отдельных файлов и семейного sharing.
- Не менять storage-value copy, price, trial terms или traffic mix.
- **Плюс:** проверяет конкретный comprehension barrier.
- **Главное возражение:** synthetic feedback не доказывает реальный barrier.
- **Решающее опровержение:** comprehension растёт, но paid conversion, activation и guardrails не улучшаются.

### Вариант D — сделать trial terms и value явными

- До подтверждения отобразить verified trial length, renewal date, price, cancellation и ограничения.
- **Плюс:** проверяет uncertainty по billing и renewal.
- **Главное возражение:** disclosure может увеличивать отток или связывать разные механизмы в одном тесте.
- **Решающее опровержение:** gain в conversion не удерживается или ухудшаются refunds, complaints и margin.

**Итог отборочного шага:** вариант A — безопасное текущее действие; вариант C — единственная изолированная check-гипотеза для gated test; вариант D требует отдельного верифицированного теста; вариант B сохраняется при подтверждённо отрицательной economics.

Полный текст вариантов: [options.md](../../artifacts/options.md).

---

## 4. Продуктовая стратегия

### Рекомендованное направление

Не запускать изменение в production на основании демо. Сначала проверить реальное tracking и доказать конкретный sharing-comprehension barrier. Только при подтверждении гипотезы провести account-randomized trial, который меняет **только permission boundary copy**.

### Целевая аудитория и задача

Лица, решающие, подходит ли им совместное облачное хранилище для конкретной задачи backup/share. До пользовательского исследования нельзя утверждать, что они испытывают этот barrier.

### Осознанные отказы

- Не менять billing/price без отдельного решения.
- Не объединять family sharing и storage-value messaging в одну интервенцию.
- Не масштабировать по uplift самого synthetic test target.
- Не закрывать направление по отсутствию демо-фактов.

### Связь пользы и экономики

Переменные для реальной валидации:

- Incremental ARPU.
- Paid and free retention.
- Gross margin.
- CAC attribution.
- Service/support costs.
- Attach rate в ecosystem.
- Cannibalization существующих storage/partner offers.

Без этих данных экономический вывод считается scenario analysis, а не инвестиционным решением.

---

## 5. Коммуникационная стратегия

### Аудитория и момент

Потенциальный trial starter перед подтверждением онбординга или платежных условий.

### Проверяемый barrier

Неясно, какие файлы доступны family members и что происходит после trial.

### Ключевое сообщение

> «Вы можете выбрать, какие файлы и папки отправить семейству».

Сообщение разрешено к показу только после проверки реального permission model, privacy rules и legal review.

### Подтверждение

UI должен буквально показывать scope sharing, recipients и способ изменения доступа. Trial length, renewal, price и cancellation должны раскрываться отдельно и точно соответствовать billing terms.

### Роль каналов

- Product screen: объяснение permission boundary.
- Trial confirmation: verified billing terms.
- Lifecycle notification: напоминание только о подтвержденной ценности и действии по cancellation.
- Support: ответы на фактически поддерживаемые вопросы.

Никакая рекламная формулировка не должна обещать storage coverage, family behavior или savings, пока это не подтверждено authority sources.

---

## 6. Экономика

### Базовый сценарий

Входы: monthly ARPU 199 RUB, gross margin 65%, monthly retention 88%, acquisition spend 1,320,000 RUB, новых paid customers 1,320.

Результат от [`calc_economics.py`](../../scripts/calc_economics.py):

| Метрика | Значение |
|---|---:|
| LTV | 1 077.916667 RUB |
| CAC | 1 000 RUB |
| Payback | 7.730963 months |

Полный output: [economics_result.json](../../artifacts/economics_result.json).

Расчёт является undiscounted и использует constant monthly survival rate. Он не включает support/cloud cost и не моделирует cannibalization.

### Чувствительность при 78% retention

При сохранении всех прочих значений и снижении monthly retention до 78%:

| Метрика | Значение |
|---|---:|
| LTV | 587.954545 RUB |
| CAC | 1 000 RUB |
| Итог | LTV ниже CAC |

Полный output: [q3_economics_result.json](../../artifacts/q3_economics_result.json). Сценарий соответствует synthetic trigger [`q3_churn_update.md`](../../data/new/q3_churn_update.md).

### Экономический вывод

Решение о scale/stop принимается только по verified incremental contribution. До этого числа относятся к unit-economics check, а не к реальной рентабельности сервиса.

---

## 7. План A/B-теста

### Гипотеза

Уточнение границы family-sharing permission улучшит comprehension и может улучшить paid conversion среди eligible trial starters.

### Критерий опровержения

Гипотеза H1 ослабляется, если comprehension уже высокая и clarification treatment не улучшает paid conversion или activation относительно control.

### Дизайн

- Unit randomization: account-level, с дедупликацией.
- Split: 1:1.
- Control: действующий screen.
- Treatment: один permission-boundary clarification.
- Fixed variables: storage-value copy, price, eligibility, trial terms, traffic mix.
- Enrollment: 4 недели для предварительного planning.
- Paid-conversion window: pre-defined с 30-дневной maturation.
- Retention: минимум 30 дней для paid retention.

### Planning target

- Baseline: 11.0% (fictional Q4).
- Illustrative target: 13.5%.
- Two-sided alpha: 0.05.
- Power: 80%.
- Normal approximation suggests ~2,700 users per arm.
- Для реального запуска требуется verified power calculation, sample exclusions и attrition assumptions.

Числа не являются прогнозом реального uplift.

### Основная метрика

Paid conversions / eligible randomized trial-starting accounts в pre-defined window.

### Guardrails

- 30-дневный paid retention.
- Refunds/cancellations.
- Complaints.
- Support contacts.
- Gross contribution.
- Cannibalization.
- Comprehension or privacy misunderstanding.

### Pre-registration

До запуска установить:

- eligibility и exclusion rules;
- account deduplication и cross-device handling;
- baseline balance checks;
- maturity and data-quality window;
- stop/roll-back thresholds;
- no-peeking rule;
- ownership and review schedule.

### Решение по результату

- **Scale:** pre-registered primary uplift positive, guardrails stable, verified economics positive.
- **Iterate:** comprehension improved but conversion not decided or guardrails inconclusive.
- **Stop:** quality/data errors, comprehension worsened, complaints/refunds worsen, economics negative.
- **Reopen:** новая информация меняет eligible population, product capability or privacy promise.

---

## 8. Итог Adversarial Review

Независимый skeptic получил только brief, evidence graph, options и draft strategy. Он не получил историю генерации.

Обнаружены и внесены в финальную стратегию следующие правки:

1. Фиксированное 7-пп изменение нельзя интерпретировать как proven decline.
2. Fictional feedback нельзя считать demand evidence.
3. 13.5% и 3,000 users per arm исключены из статуса verified forecast.
4. Option C отделён от storage-value messaging.
5. Добавлены account-level randomization, cross-device, balance, maturity и stopping rules.
6. “You control…” не публикуется до product/privacy/legal verification.
7. LTV/CAC остаётся assumption scenario и не подтверждает реальную economics.
8. Новая retention update является триггером пересмотра, не доказательством false decision.

Полный текст критики: [adversarial_review.md](../../artifacts/adversarial_review.md).

---

## 9. Финальное решение демо

Для демонстрации принято условное решение:

> Сначала проверить instrumentation и реальную product truth. Если реальный barrier clarity подтверждён, запустить изолированный account-randomized test permission copy; без этого rollout не разрешён.

Решение зафиксировано в реестре: [decisions_registry.json](../../state/decisions_registry.json). Текущий статус: `review_required` из-за synthetic Q3 retention update.

Владельцем в демо указан fictional role, а не реальное лицо. Любой real experiment, release или customer contact требует отдельного human approval.

---

## 10. Пакет проверки жюри

Проверьте по этому порядку:

1. Запустите тесты: `python -m unittest discover -s tests -v`.
2. Проверьте evidence: `python scripts/validate_evidence.py`.
3. Пересчитайте economics: `python scripts/calc_economics.py data/raw/demo/economics_input.json`.
4. Пересчитайте sensitivity: `python scripts/calc_economics.py data/raw/demo/q3_economics_sensitivity_input.json`.
5. Проверьте recheck: `python scripts/recheck_decisions.py`.
6. Посмотрите обоснование измерений: [comparison.md](../../artifacts/baseline/comparison.md).

Полный технический отчёт: [SUBMISSION_REPORT.md](../../docs/SUBMISSION_REPORT.md).

Сценарий демонстрационного видео: [DEMO_VIDEO_SCRIPT.md](../../docs/DEMO_VIDEO_SCRIPT.md).
