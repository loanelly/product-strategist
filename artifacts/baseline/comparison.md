# Baseline comparison: measured demo tool phase and unmeasured chat baseline

## Measured result

Date: **2026-11-18**.

The deterministic part of the demo was rerun in a clean PowerShell process with
Python 3.12:

1. `validate_evidence.py`
2. `calc_economics.py data/raw/demo/economics_input.json`
3. `calc_economics.py data/raw/demo/q3_economics_sensitivity_input.json`
4. `recheck_decisions.py`

Measured wall time for these four CLI invocations was **364 ms** total
(0.365 s), with **4 tool/process calls**, and exit code 0 for every tool.
This does not include model reasoning, human checkpoints, source research,
subagent review, IDE startup, or initial runtime download.

For a material context-volume estimate, the selected brief, source files,
research/options/strategy/review artifacts, evidence graph, and decision
registry contain 38,662 UTF-8 characters, or roughly **9,693 content
tokens** under a 4-characters-per-token approximation. This is a text-volume
estimate, not provider-reported token usage.

## Ordinary-chat baseline

No ordinary-chat run was available from this IDE/provider session, so a
true matched baseline could not be timed or billed honestly. The repository
does not claim a speed or cost improvement.

The intended baseline format is:

| Metric | Agent demo tool phase | Ordinary chat, one request |
|---|---:|---:|
| Human requested turns | 4 deterministic CLI actions + repository workflow | 1 ordinary chat request |
| Tool/process calls | 4, measured | 0 tools in the baseline design |
| Wall time | 364 ms, measured for the four local tool calls | Not measured |
| Provider/model calls | 0 local model calls; IDE model telemetry unavailable | Not measured |
| Provider token usage | Not measured | Not measured |
| Provider cost | Not measured | Not measured |
| Repeated factual source coverage | 6/6 facts source-linked, measured | Not measured |
| Reproducible calculations | 2, executed and checked | Not measured |
| Adversarial review findings | 8, measured in the saved artifact | Not measured |
| End-to-end human elapsed time | Not measured | Not measured |

The ordinary chat arm is not treated as 0 ms or 0 cost: the values are
unknown. Provider cost and token counts must come from actual provider
telemetry, not character-count guesses.

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

## Scope limitation

This measured result covers only local deterministic tools. It does not prove
that the IDE-agent run is faster or cheaper end-to-end than ordinary chat.
The fixture-level tests prove that deterministic checks work; they do not prove
improved real-world strategy quality, lower cost, or faster completion by
themselves.
