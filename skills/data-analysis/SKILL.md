# Data analysis and metric audit

## Procedure

1. Confirm that the input is authorized, non-sensitive, and does not contain
   personal data. Keep originals unchanged; work on a copy or read-only input.
2. Inventory file and table names, row counts, date coverage, identifiers,
   units, currencies, time zones, cohort definitions, and metric definitions.
   Report missing values, duplicates, inconsistent formats, and likely
   outliers before drawing conclusions. Do not delete outliers without a
   reasoned rule and report.
3. Check numerator, denominator, grain, period, inclusion/exclusion rules,
   missingness, sample size, survivorship, and segment mix for each metric.
   Compare like periods and cohorts; never silently mix monthly and annual,
   rates and percentages, currencies, or distinct definitions of retention,
   churn, revenue, or active users.
4. For cohort retention, document the starting cohort, eligible population,
   retained-user definition, observation window, formula, and exclusions.
   Verify calculations against the underlying rows where permitted. Do not
   say `calc_economics.py` estimates retention: it accepts an already-derived
   monthly retention rate and returns it alongside LTV/CAC/payback.
5. When economic inputs are available, prepare a JSON input with explicitly
   labeled monthly units and currency and run
   `python scripts/calc_economics.py path\to\economics-input.json`. Retain the
   input and output with the project artifacts. The script calculates LTV,
   CAC, and payback for its stated assumptions; it does not infer missing
   inputs, derive cohort rates, discount cash flows, or model cannibalization.
6. Reject calculations with missing inputs or incompatible units; do not
   fill them with zeros or typical values. List the minimum additional data
   needed and report results unavailable where necessary.
7. Separate descriptive results from causal explanations and forecasts.
   Check for seasonality, exposure changes, tracking changes, segment shifts,
   and alternative explanations. State uncertainty and falsification criteria.
8. Include reproducible formulas, input provenance, transformations,
   exclusions, comparison period, caveats, and undesirable side effects.

## Stop for the user

Stop if data authorization is uncertain, personal/sensitive data appears,
metric definitions conflict, or a missing denominator/unit could materially
change the decision. Ask for sanitized data or a definition rather than
guessing.

## Output

Return an auditable metric table plus caveats and an economics input/output
pair when calculable. Keep factual observations, hypotheses, and forecasts
distinct in the evidence graph and strategy.
