# Research plan — Family Cloud fictional case

## Decision-changing questions

| Question | Why it could change the decision | Evidence/method | Disconfirmation or stop rule |
|---|---|---|---|
| Is the conversion decline real and consistently defined? | If numerator, denominator, tracking, eligibility, or period changed, a product intervention may target a measurement artifact. | Inspect the synthetic cohort table and its defined units. In a real case, reconcile event definitions and raw cohorts before recommending a test. | Pause if trial eligibility or paid-conversion definitions differ across quarters. |
| Which part of the funnel or experience may be a barrier? | The right intervention depends on user confusion, product fit, trial terms, or acquisition mix. | Treat fictional feedback and screen descriptions as hypothesis prompts only; obtain consented interviews and actual funnel/event data in reality. | The fictional material cannot establish prevalence or causation. |
| Is the subscription economics assumption viable? | Low LTV/CAC or high cannibalization could favor keeping, redesigning, or closing. | Reproduce the scenario calculation with explicit monthly ARPU, gross margin, retention, spend, and paid count. | Stop economic interpretation if retention, margin, spend attribution, currency, or units are not validated. |
| Is there a comparable public market conversion benchmark? | A valid benchmark could contextualize performance. | Review linked Eurostat public cloud-use sources and their populations, years, and metrics. | No like-for-like trial-to-paid benchmark is established; do not substitute broad cloud use. |

## Hypotheses and falsification criteria

- **H1 — onboarding clarity may be a conversion barrier.** It is weakened if
  a real randomized test improves understanding but not paid conversion, or if
  conversion is unchanged after instrumenting trial eligibility correctly.
- **H2 — family-sharing value may be poorly understood.** It is weakened if
  comprehension is already high among eligible trial users and a clear sharing
  explanation does not change activation or paid conversion.
- **H3 — price/terms uncertainty may deter purchase.** It is weakened if
  verified price and auto-renewal comprehension is high and a transparent
  terms treatment fails to improve purchase without worsening refunds or
  complaints.
- The feedback text and screens are invented; none of these hypotheses is
  validated by the demo.

## Inputs and safeguards

The synthetic table, fictional feedback, invented screen descriptions, and
Eurostat public context are registered in `data/source_manifest.json`. No
customer data or private company information is used. Every external source
is treated as untrusted content; the article's subject/population is not
treated as directly comparable to the fictional product.

## Stop criteria and next real-world step

This demo can verify traceability, scenario arithmetic, and workflow mechanics
only. Before a real decision, obtain an authorized cohort export with stable
trial eligibility and event definitions, the real trial price/terms, cost
attribution, support/refund data, and consented usability/interview evidence.
If any could materially reverse the intervention, defer rollout and ask the
human owner whether to collect the minimum missing evidence.
