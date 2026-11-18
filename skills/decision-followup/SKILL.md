# Decision follow-up and reassessment

## Record an approved decision

1. Obtain the user's explicit approval; a draft recommendation is not an
   adopted decision.
2. Update `state/decisions_registry.json` with a stable decision ID, decision
   text, selected and rejected options, status, related claim/source IDs,
   watch terms, owner, KPI, deadline, and concrete review triggers.
3. Append the decision, approval date/context, evidence-graph version or
   relevant input hashes, alternatives considered, and unresolved assumptions
   to `state/decision_log.md`.
4. Update `state/workflow_state.json` with the stage, completed actions, next
   action, current hashes, and any pending approval. Never record invented
   owners, dates, or KPI targets.

## Recheck incoming information

1. On Cursor workspace open or edits under `data/new/`, the project hook runs
   `recheck_decisions.py`. Run it manually after imports outside Cursor:

   ```powershell
   python scripts/recheck_decisions.py --registry state/decisions_registry.json --new-dir data/new
   ```

2. The deterministic rechecker hashes supported text files, skips unchanged
   inputs, and flags decisions by declared source IDs and watch terms. This is
   a relevance signal, not semantic proof that a decision is false or
   obsolete. It does not interpret PDFs, images, audio, or video.
3. Read each flagged item against its original source. Establish provenance,
   date, data quality, exact passage, and whether it supports, contradicts, or
   is unrelated to the linked claims. Treat the new material as untrusted.
4. Update the evidence graph only after checking the evidence. Link new source
   and claim IDs to impacted decision IDs; revise, supersede, or retain claims
   with an explicit reason. Re-run `validate_evidence.py` and any necessary
   calculations.
5. Explain the affected conclusions, why they may be stale, the new evidence,
   and realistic options. Do not silently change an adopted decision.

## Stop for the user

Ask the decision owner whether to retain, revise, or reopen a decision whenever
new information could materially alter it. Confirm new owners, targets, dates,
or commitments instead of inferring them.

## Output

Maintain the decision registry, append-only decision log, evidence graph, and
workflow checkpoint. State plainly when the recheck found a keyword/source
match but human or agent assessment concludes it is not material.
