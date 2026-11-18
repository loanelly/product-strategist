# Baseline comparison: measurement protocol and current result

## Status

**A matched ordinary-chat baseline has not been run.** This workspace has no
configured model credentials or provider billing telemetry, and the IDE agent's
token/cost details are not exposed to these deterministic scripts. Reporting
invented durations, token counts, costs, or a chat-only quality score would be
misleading. Current comparison values are therefore marked **not measured**,
not zero.

## Run protocol before making comparative claims

1. Select one fixed brief and the same authorized source files for both arms.
   Record file hashes, the exact prompt, model/provider/version, date, and
   allowed tools.
2. **Plain-chat baseline:** use a normal chat with no repository workflow,
   scripts, or MCP; ask for the same decision output. Record wall time including
   human follow-up, all prompt/output tokens, provider cost, number of user/AI
   steps, and any manual rework.
3. **IDE-agent arm:** start from the same brief/material hashes; follow the
   repository workflow. Record wall time including human checkpoints, actual
   provider token/cost telemetry, tool calls, and rework. Do not count
   deterministic local scripts as free human time.
4. Score both outputs using a blind, identical checklist: fraction of
   decision-relevant factual claims with a valid source and exact location;
   successful reproducible economics check; material options (including
   keep/close), strong counterarguments, communication/product truth,
   falsification criteria, guardrails, and major risks. Two reviewers should
   adjudicate disputed rubric items before comparing.
5. Repeat with at least three representative tasks before generalizing. Report
   median and range, model/tool versions, human time, and limitations; do not
   generalize from one synthetic demo.

For each paired run, record the measured values with
`cost_tracker.py add --scenario-id <same-id> --run-id <unique-id> --mode
baseline|agent` and all required metric flags. Then run
`cost_tracker.py compare --scenario-id <same-id>`. Tokens/cost must come from
actual provider reporting, not character-count estimates. Claims coverage is
the number of material factual claims with valid source links divided by all
material factual claims. Record separately how many calculations were checked
and material risks identified.

## Current demonstration observations

| Metric | IDE-agent artifacts | Plain-chat baseline |
|---|---|---|
| Workflow steps | Eight stages defined; all eight demo artifacts were prepared | Not measured |
| Sourced factual claims | `validate_evidence.py` passed; all 6/6 factual lines have graph claim IDs, confidence, and source locators | Not measured |
| Economic calculations | Two synthetic scenarios executed with `calc_economics.py`; base and 78% retention sensitivity are in `artifacts/economics_result.json` and `artifacts/q3_economics_result.json` | Not measured |
| Material risks identified | Eight material challenges from the isolated adversarial review; see `artifacts/adversarial_review.md` | Not measured |
| Recheck behavior | `recheck_decisions.py` flags the synthetic retention counterexample and records its hash | Not measured |
| Model/tool token count | Not available from this IDE session | Not measured |
| Provider/tool cost | Not available; not assumed to be zero | Not measured |
| End-to-end human elapsed time | Not measured consistently by the repository | Not measured |
| Comparative speed or quality gain | **Not established** | **Not established** |

The fixture-level tests prove the deterministic checks work on their test
cases; they do not prove improved real-world strategy quality, lower cost, or
faster completion than a human or ordinary chat.
