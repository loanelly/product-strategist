# Intake: frame a decision-ready brief

## Goal

Turn an ambiguous product request into a decision question that can be
researched and acted on. Follow `AGENTS.md` and `knowledge/research-methods.md`.

## Procedure

1. Restate the request in one sentence, separating the observed symptom from
   the presumed cause.
2. Identify who owns the decision, who will use the answer, what must be
   decided, and by when.
3. Identify the desired outcome and measurable success/guardrail metrics,
   relevant segments, constraints, allowed materials, and available data.
4. Read the current `state/workflow_state.json` before resuming existing work.
   Do not ask again for information already present and still valid.
5. Ask at most **3–5 concise, decision-changing questions in total**. Prefer
   asking fewer. Ask only what changes the next research action, a safety
   boundary, or the decision. If information is unavailable, record the gap
   and proceed conditionally where safe.
6. Write or update `projects/<id>/brief.md` with the question, decision owner,
   audience, goal, deadline, success criteria, constraints, authorized inputs,
   assumptions, and unresolved questions.
7. Update `workflow_state.json` with stage 1, the completed action, next
   action, current input hashes, and the pending approval.

## Stop for the user

Do not begin evidence collection until the user confirms the problem framing,
goal, decision owner or their delegate, and material constraints. Do not ask a
question whose answer would not change the next step. Never invent authority,
access permissions, data, or success criteria.

## Output

Deliver the brief and a short list of remaining unknowns, then request approval
of the framing. Do not draft a recommendation at intake.
