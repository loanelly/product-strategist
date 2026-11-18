**Language:** [Русский](../DEMO_VIDEO_SCRIPT.md) | English

# Demo video script (target: 8–9 minutes)

Record in Cursor or a compatible IDE that can show [`AGENTS.md`](../../AGENTS.md),
terminal commands, hook status, and a separate reviewer. Use the fictional
project only. Do not show credentials, private customer data, or claim that
this is a real MegaFon product.

## 0:00–0:45 — Introduce scope and safety

Show [`projects/demo/README.md`](../../projects/demo/README.md) and say:
“This is an invented cloud-storage product and synthetic cohort data. Only
the linked Eurostat context is public, and it is not a comparable paid-
conversion benchmark.”

## 0:45–1:45 — Start at the request and workflow

Show [`projects/demo/brief.md`](../../projects/demo/brief.md), then
[`AGENTS.md`](../../AGENTS.md) and
[`skills/intake/SKILL.md`](../../skills/intake/SKILL.md). In a new IDE chat,
paste:

> Read AGENTS.md and skills/intake/SKILL.md. Resume projects/demo from
> state/workflow_state.json. Summarize the saved stage, next action, fictional
> data boundary, and any human approval required. Do not repeat completed
> stages or infer real customer demand.

Show the stage and approval boundary. Explain that an actual project would
pause for the product owner's brief approval before research.

## 1:45–3:00 — Inspect sources and evidence

Show [`data/source_manifest.json`](../../data/source_manifest.json), a source
file's synthetic provenance, and
[`state/evidence_graph.json`](../../state/evidence_graph.json). Run:

```powershell
python scripts/validate_evidence.py
```

Explain that factual claims point to source IDs/locations and synthetic
responses are not demand evidence.

## 3:00–4:00 — Reproduce economics

Run:

```powershell
python scripts/calc_economics.py data/raw/demo/economics_input.json
```

Show [`artifacts/economics_result.json`](../../artifacts/economics_result.json).
Explain it uses fictional inputs, undiscounted LTV, and excludes servicing
cost and cannibalization.

## 4:00–5:00 — Compare options and recommendation

Show [`artifacts/options.md`](../../artifacts/options.md) and
[`artifacts/strategy.md`](../../artifacts/strategy.md). Point out keep-as-is,
close, two distinct interventions, a conditional recommendation,
product-truth checks, falsification criteria, and a permission-only test.
State that the sample-size number is only a planning approximation pending
real data and statistical review.

## 5:00–6:00 — Independent challenge

Show the separate adversarial-reviewer agent configuration and
[`artifacts/adversarial_review.md`](../../artifacts/adversarial_review.md).
Explain it did not receive generation history; highlight how its challenge
narrowed the test, qualified the economics, and made power/guardrail checks
explicit.

## 6:00–7:00 — Stop and resume in a new chat

Show [`state/workflow_state.json`](../../state/workflow_state.json). Start a
fresh IDE chat and paste:

> Read AGENTS.md, the relevant decision-followup skill, and
> state/workflow_state.json. Continue from next_action only. Check for new
> material and explain which decision, if any, requires human review. Do not
> treat synthetic data as real or change an adopted decision without approval.

Show the agent recovering stage 8 and pending human approval.

## 7:00–8:15 — Demonstrate a new-data recheck

The committed demo already has the synthetic fixture registered as processed
and `DEMO-D-001` flagged for review. To show a clean before/after without
changing the repository's final state, use a temporary registry copy:

```powershell
Copy-Item state\decisions_registry.json "$env:TEMP\demo-decisions.json"
python -c "import json,os; p=os.path.join(os.environ['TEMP'],'demo-decisions.json'); d=json.load(open(p,encoding='utf-8')); d['decisions'][0]['status']='adopted'; d['decisions'][0]['review_reasons']=[]; d['processed_files']={}; json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
python scripts/recheck_decisions.py --registry "$env:TEMP\demo-decisions.json" --new-dir data/new
python -c "import json,os; print(json.load(open(os.path.join(os.environ['TEMP'],'demo-decisions.json'),encoding='utf-8'))['decisions'][0]['status'])"
```

Show the output and explain that source-ID/watch-term matches set
`review_required`; the script does not judge truth or revise the decision.
The example's 78% retention is fictional and only demonstrates that review
trigger.

## 8:15–9:00 — Wrap with reproducibility and honest limits

Run:

```powershell
python -m unittest discover -s tests -v
```

Show [`artifacts/baseline/comparison.md`](../../artifacts/baseline/comparison.md).
State that no matched chat baseline or IDE token/cost telemetry was available,
so speed/cost superiority is not claimed. Explain how to record real paired
runs with
[`scripts/cost_tracker.py`](../../scripts/cost_tracker.py) before making any
comparative claim.
