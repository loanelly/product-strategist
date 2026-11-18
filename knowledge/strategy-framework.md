# Digital product and communication strategy standard

The strategy is a decision document, not a generic market overview. Complete
each section with traceable evidence IDs from `state/evidence_graph.json`.
Separate fact, hypothesis, and forecast using the required notation in
`AGENTS.md`. State gaps and assumptions next to the conclusions they affect.

## 1. Decision and diagnosis

- State the decision, decision owner, audience, goal, deadline, constraints,
  and measurable definition of success.
- Describe the observed situation and trend, including period, population,
  denominator, metric definition, comparison, and data limitations.
- Distinguish the symptom (for example, falling retention) from tested causes.
- List the decision-changing questions, strongest evidence against the current
  explanation, and the falsification criteria for key hypotheses.

## 2. Audience, need, and alternatives

- Name the target segment and the job, situation, or unmet need using evidence;
  state what is not known about representativeness.
- Include alternatives: direct competitors, substitutes, doing nothing, and
  solving the need outside the category.
- Describe the current journey and where value, friction, or abandonment occurs.
- Do not infer demand, willingness to pay, or prevalence from synthetic
  respondents or unrepresentative samples.

## 3. Materially different options

Present at least three, including **keep as is** and **close the direction**.
For each, state target user, product change, expected value, costs, risks,
dependencies, strongest objection, assumptions, and an observation that could
disqualify it. Make options genuinely distinct, not wording variants.

## 4. Product strategy and economics

- Name the selected direction and explain the options rejected or deferred.
- Connect user value to adoption, engagement, retention, revenue, cost to serve,
  and strategic fit. Draw a causal chain; do not imply correlation proves cause.
- In telecom or ecosystem contexts, state relevant effects on ARPU, retention,
  churn, acquisition, cross-product attachment, support/network costs, and
  ecosystem value. Include substitution between own products and partners.
- Estimate cannibalization explicitly: identify the existing revenue or use
  case at risk and separate transferred demand from incremental demand. If data
  is unavailable, state the gap rather than assuming zero.
- Define unit and period for every economic input. Document cohort, currency,
  gross margin, retention, customer count, CAC scope, and exclusions. Run
  `python scripts/calc_economics.py <input.json>` for supported LTV, CAC, and
  payback calculations; preserve input and output with the strategy.
- The calculator accepts a monthly retention rate; it does not derive cohort
  retention from raw events, estimate revenue, or model cannibalization. Derive
  retention only from validated cohort data with a documented formula, or
  explicitly report it as unavailable. Never treat its illustrative formula
  as a validated forecast.

## 5. Communication strategy and product truth

Specify the audience and usage/decision moment, the barrier to understanding
or choosing, one key message, proof that supports it, the call to action, and
the role of each channel along the journey. Explain what to test in each
channel and how the experience hands off to the product.

Before approving copy or a promise, verify it against current product
capabilities, eligibility, price, coverage/availability, limitations,
onboarding, and service terms using authoritative evidence. Qualify or remove
claims that cannot be substantiated. Do not imply guaranteed results,
availability, savings, compatibility, or service quality without evidence.

## 6. Experiment and decision rules

For every key uncertainty specify:

- hypothesis and falsification threshold;
- target population, eligibility, and sample or exposure requirement;
- primary metric, exact numerator/denominator, unit, period, and source;
- baseline/comparison, assignment method, duration, and analysis approach;
- guardrails and undesirable effects (e.g. churn, complaints, margin,
  cannibalization, support load, or harm to other segments);
- owner, cost, dependencies, and decision date;
- outcomes that trigger scale, iterate, stop, or revisit the strategy.

Do not promise statistical significance without an appropriate design and
adequate data. Mark directional tests and qualitative evidence as such.

## 7. Recommendation and traceability

Summarize the recommendation, why it is better than each alternative, the
largest unresolved risk, what would reverse the decision, and the immediate
human decision requested. Run `python scripts/validate_evidence.py`; resolve
all validation errors before presenting the strategy. Get human approval
before recording an adopted decision.
