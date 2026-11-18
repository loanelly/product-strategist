# Adversarial review

## Isolation

Run this stage through the `adversarial-reviewer` subagent in a separate
context. Supply only:

- the approved brief;
- `state/evidence_graph.json`;
- `artifacts/options.md`;
- the current `artifacts/strategy.md`.

Do not pass conversation history, strategy-generation reasoning, or earlier
drafts. If the IDE cannot create an isolated subagent, stop and tell the user;
do not describe an in-context critique as independent.

## Review

Challenge the recommendation rather than improve its rhetoric. Check source
quality, unsupported factual claims, contradictory evidence, alternative
explanations, neglected options, assumptions behind economics, audience fit,
product/communication alignment, and downside risks. For each issue, cite
evidence IDs where available, state uncertainty, and name a test that could
change the decision.

Save the review to `artifacts/adversarial_review.md`. The parent agent must
address every material objection and ask the user to approve the resulting
decision.
