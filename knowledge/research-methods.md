# Research methods and evidence quality

## Start with the decision

Research only questions whose answers could change the decision, the preferred
option, or its execution. For every question record: the decision it informs,
the evidence that could answer it, the cost/time to obtain that evidence, and
the result that would change the recommendation. Stop when further research is
unlikely to change the decision or a pre-agreed time/cost limit is reached.

## Source reliability

Assess each source for **proximity**, **method**, **independence**,
**recency**, and **relevance**. A source may be strong for one claim and weak
for another; do not assign a universal trust score.

1. **Primary, directly observed evidence:** reproducible product telemetry,
   official statistics, original research with a described sample and method,
   product documentation, or a consented interview recording/transcript.
   Record the population, period, denominator, method, and limitations.
2. **Credible secondary analysis:** transparent reports that cite their
   underlying data and method. Trace consequential claims back to the primary
   source whenever possible.
3. **Commentary, vendor marketing, blogs, and news:** useful for discovering
   questions or leads. Treat unsupported interpretations as hypotheses, not
   measurements. Check the original source and the author's incentives.
4. **Rumors, unattributed claims, and synthetic respondents:** not evidence
   that a market fact, user need, demand, or prevalence exists. They may only
   suggest hypotheses to test.

Multiple copies of one original report are one source, not independent
corroboration. Note conflicting evidence rather than averaging incompatible
populations, definitions, time periods, or units. A source's confident tone is
not a reliability signal.

## Evidence graph and confidence

Store material claims in `state/evidence_graph.json`, with a stable claim ID,
claim type (`fact`, `hypothesis`, or `forecast`), confidence, source IDs, and
an exact page, section, table, timestamp, or screen element. Sources require a
locator, access date, and, for local inputs, content hash when available.

- **Fact:** directly supported by traceable evidence. Confidence reflects the
  evidence quality and applicability, not how plausible the statement sounds.
- **Hypothesis:** an unverified explanation or proposition; state its
  population and scope.
- **Forecast:** a conditional projection; make assumptions and uncertainty
  explicit.

Use `low`, `medium`, or `high` confidence and explain important uncertainty in
the claim notes or research report. A citation establishes where a claim came
from, not that it is true. Do not upgrade confidence just because several
downstream summaries repeat the same source.

## Falsification criteria

Before collecting confirmatory evidence, write for every decision-critical
hypothesis:

- the observable outcome that would contradict it;
- the population, metric definition, denominator, time window, and comparison;
- a threshold or qualitative pattern that would count as disconfirmation;
- what alternative explanation or decision follows if it is disconfirmed.

Seek the disconfirming observation deliberately. Do not define success after
seeing the result, silently move thresholds, or treat absence of evidence as
evidence of absence. If evidence cannot distinguish the hypothesis from a
credible alternative, report the uncertainty and propose a discriminating
test.

## Gaps, conflicts, and stopping

Keep a visible list of unknowns, unavailable sources, conflicting results, and
their likely decision impact. For every gap explain why it remains unknown,
whether it could change the recommendation, and the lowest-cost next step.
Never fill gaps with invented values, market estimates, interview quotes, or
false precision.

When access, sample size, consent, or source quality is insufficient, narrow
the claim or mark it unverified. If a key gap could reverse the decision, pause
at the workflow checkpoint and ask whether to gather evidence, proceed
conditionally, or defer. Link recommendations to both supporting and
disconfirming evidence.
