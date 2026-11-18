# Product and communication strategy

## Procedure

1. Read the approved brief, `knowledge/strategy-framework.md`, research plan,
   evidence graph, and validated data/UX findings.
2. Draft `artifacts/options.md` with at least three **materially different**
   options. Always include **keep as is** and **close the direction**. For
   each include target audience/need, product approach, value, costs,
   dependencies, strongest objection, downside risk, key assumptions, and
   what evidence would disqualify it. Do not present cosmetic variations as
   distinct options.
3. Compare options against explicit decision criteria and constraints. State
   trade-offs, uncertainty, and the strongest case against the leading option.
   Do not imply that weighted scoring or fabricated precision makes a
   subjective choice objective.
4. Build `artifacts/strategy.md` with the audience and task, alternatives,
   selected direction and conscious refusals, value and economic logic, and
   the major unanswered risks. Address relevant retention, ARPU, acquisition,
   cost to serve, ecosystem effects, and cannibalization when evidence permits.
5. Add a coordinated communication strategy: audience/moment, comprehension
   or choice barrier, key message, credible proof, channel roles, and hand-off.
   Verify every promise against actual product capabilities and authoritative
   sources; qualify or omit unsupported claims.
6. Define an experiment with a falsifiable hypothesis, expected change,
   baseline/comparison, population, metric definition, sample/exposure,
   duration, owner, guardrails, and scale/iterate/stop/revisit criteria.
7. Structure every non-heading strategy line in the evidence notation in
   `AGENTS.md`; facts link to sourced fact IDs and hypotheses/forecasts remain
   distinctly labeled. Run `python scripts/validate_evidence.py`. Where
   inputs permit, run `python scripts/calc_economics.py` and cite its actual
   outputs and limitations.
8. Ask the user to review the strategy, then route accepted drafts to the
   isolated Adversarial Review Skill. Do not claim independent review when
   performed in the generation context.

## Stop for the user

Pause for approval of the shortlist before full strategy, before independent
critique, and before adopting any decision. Return to research if a key
unsupported claim or conflicting evidence could reverse the recommendation.

## Output

Deliver `artifacts/options.md` and a validated `artifacts/strategy.md` with
source traceability, objections, trade-offs, product/communication alignment,
explicit uncertainty, and a measurable experiment.
