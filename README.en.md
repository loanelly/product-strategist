<img src=".github/5732-fotor-bg-remover-20261118211536.png" align="right" width="180px">


# Product Strategist

**Language:**  <a href="https://github.com/loanelly/product-strategist/blob/main/README.en.md"><img src="https://github.com/loanelly/EntropyShield/blob/main/img/Flags/EN1.png" height="21" align="center"/></a> <a href="https://github.com/loanelly/product-strategist/blob/main/README.md"><img src="https://github.com/loanelly/EntropyShield/blob/main/img/Flags/result.png" height="26" align="center"/></a>

# AI agent for digital product decisions

**Product Strategist** turns an ambiguous product request and a set of authorized materials into a verifiable picture of the situation, materially distinct options, aligned product and communication strategies, independent criticism, and a resumable decision record.

The orchestrator is an agent inside Cursor, GitHub Copilot, Claude Code, or another compatible IDE. Python scripts perform deterministic validation, calculation, and registry work: they do not create a custom LLM loop.

The repository includes a **Family Cloud** demonstration built from synthetic data and limited public Eurostat context. It is explicitly unrelated to real MegaFon products, customers, or confidential data.

## What the agent does

- Clarifies the decision, decision owner, goal, audience, constraints, and success criteria.
- Collects facts from documents, tables, public web sources, and interface descriptions.
- Separates facts, hypotheses, and forecasts and maintains an evidence graph with citations and confidence.
- Recommends at least three materially different options, including **keep as is** and **close the direction**.
- Produces aligned product and communication strategies with a validation plan and guardrails.
- Runs an isolated adversarial review and records the decision, owner, KPI, deadline, and review triggers.
- Saves checkpoints and resumes in a new chat or IDE without repeating completed work.
- Flags decisions affected by new evidence and moves them to `review_required`.

## Architecture

```text
Cursor / GitHub Copilot / Claude Code
                  |
                  +-- AGENTS.md and IDE adapters
                  +-- Modular Skills and knowledge
                  +-- Human-in-the-loop checkpoints
                  +-- Fetch MCP and domain allowlist
                  +-- Deterministic Python 3.12 CLI
                  |      ingest_source / validate_evidence
                  |      calc_economics / recheck_decisions
                  |      cost_tracker
                  +-- state/ and evidence graph
                  +-- artifacts/ and decision log
```

Canonical rules live in [`AGENTS.md`](AGENTS.md). IDE adapters are [`.cursor/rules/agent.mdc`](.cursor/rules/agent.mdc), [`.github/copilot-instructions.md`](.github/copilot-instructions.md), and [`CLAUDE.md`](CLAUDE.md).

Reusable procedures are in [`skills/`](skills/), methodology in [`knowledge/`](knowledge/), and project state/results are separated between [`state/`](state/) and [`artifacts/`](artifacts/). The full file map is described in the [submission report](docs/SUBMISSION_REPORT.md).

### Current repository map

```text
.cursor/
  agents/adversarial-reviewer.md
  hooks.json
  mcp.json
  rules/agent.mdc
.github/
  copilot-instructions.md
artifacts/
  baseline/comparison.md
  adversarial_review.md
  economics_result.json
  options.md
  q3_economics_result.json
  recheck_report.json
  research_plan.md
  run_log.jsonl
  strategy.md
data/
  new/README.md
  new/q3_churn_update.md
  raw/demo/
    economics_input.json
    funnel_metrics.csv
    market_benchmark.md
    onboarding_screens.md
    q3_economics_sensitivity_input.json
    user_feedback.md
  source_manifest.json
docs/
  DEMO_VIDEO_SCRIPT.md
  SUBMISSION_REPORT.md
  en/
    DEMO_VIDEO_SCRIPT.md
    SUBMISSION_REPORT.md
knowledge/
  research-methods.md
  source-safety.md
  strategy-framework.md
projects/
  demo/
    DEMO_CASE_PACK.md
    README.md
    brief.md
schemas/
  decisions-registry.schema.json
  evidence.schema.json
  source-manifest.schema.json
  workflow-state.schema.json
scripts/
  calc_economics.py
  cost_tracker.py
  cursor_hook.py
  ingest_source.py
  recheck_decisions.py
  validate_evidence.py
skills/
  adversarial-review/SKILL.md
  data-analysis/SKILL.md
  decision-followup/SKILL.md
  intake/SKILL.md
  research/SKILL.md
  strategy/SKILL.md
  synthetic-respondents/SKILL.md
  ux-multimodal-audit/SKILL.md
state/
  decision_log.md
  decisions_registry.json
  evidence_graph.json
  workflow_state.json
tests/
  test_tools.py
AGENTS.md
CLAUDE.md
README.md
README.en.md
.env.example
.gitignore
```

IDE-specific and temporary directories (`.idea/`, `.vscode/`, `__pycache__/`, `.pytest_cache/`) are excluded from publication through [`.gitignore`](.gitignore).

### MCP and hooks

- [`.cursor/mcp.json`](.cursor/mcp.json) configures the standard Fetch MCP server and approved public domains.
- [`.cursor/hooks.json`](.cursor/hooks.json) validates strategy edits and rechecks decisions on workspace open or new-data edits.
- External content is treated as untrusted data. Isolation rules are documented in [`knowledge/source-safety.md`](knowledge/source-safety.md), and inputs can be wrapped with [`scripts/ingest_source.py`](scripts/ingest_source.py).

### Independent review

The adversarial-review stage uses a separate subagent with restricted context: it receives only the brief, evidence graph, options, and strategy. Generation history is not supplied. Configuration: [`.cursor/agents/adversarial-reviewer.md`](.cursor/agents/adversarial-reviewer.md). Procedure: [`skills/adversarial-review/SKILL.md`](skills/adversarial-review/SKILL.md).

## 3-minute quick start

**Requirements:** Python 3.12 and Cursor, GitHub Copilot, Claude Code, or a compatible IDE. Tests and deterministic tools do not require a model API or paid service.

1. Open the repository folder as a trusted workspace.
2. In Cursor, configure the Fetch MCP server from [`.cursor/mcp.json`](.cursor/mcp.json) if public web research is needed.
3. Run the checks and demo:

```powershell
python --version
python -m unittest discover -s tests -v
python scripts/validate_evidence.py
python scripts/calc_economics.py data/raw/demo/economics_input.json
python scripts/calc_economics.py data/raw/demo/q3_economics_sensitivity_input.json
python scripts/recheck_decisions.py
```

The demo decision `DEMO-D-001` starts in review state. The synthetic fixture [`data/new/q3_churn_update.md`](data/new/q3_churn_update.md) contradicts the constant-retention assumption and should change decision status only after human and agent review.

Optional environment variable names are listed in [`.env.example`](.env.example). Real credentials must never be committed; use your IDE or shell secret store.

## Family Cloud demo

The fictional cloud-storage service for mobile-operator subscribers is shown with an illustrative decline in trial-to-paid conversion from 18% to 11% in a synthetic funnel table.

The synthetic data and boundaries are documented in [`projects/demo/README.md`](projects/demo/README.md):

- [`data/raw/demo/funnel_metrics.csv`](data/raw/demo/funnel_metrics.csv) — synthetic cohort table;
- [`data/raw/demo/user_feedback.md`](data/raw/demo/user_feedback.md) — fictional feedback fragments;
- [`data/raw/demo/onboarding_screens.md`](data/raw/demo/onboarding_screens.md) — invented onboarding descriptions;
- [`data/raw/demo/market_benchmark.md`](data/raw/demo/market_benchmark.md) — public Eurostat context;
- [`data/raw/demo/economics_input.json`](data/raw/demo/economics_input.json) — explicitly labeled scenario assumptions;
- [`data/raw/demo/q3_economics_sensitivity_input.json`](data/raw/demo/q3_economics_sensitivity_input.json) — retention sensitivity scenario.

Key artifacts:

- Brief: [`projects/demo/brief.md`](projects/demo/brief.md)
- Research plan: [`artifacts/research_plan.md`](artifacts/research_plan.md)
- Evidence graph: [`state/evidence_graph.json`](state/evidence_graph.json)
- Options: [`artifacts/options.md`](artifacts/options.md)
- Strategy: [`artifacts/strategy.md`](artifacts/strategy.md)
- Adversarial review: [`artifacts/adversarial_review.md`](artifacts/adversarial_review.md)
- Economics: [`artifacts/economics_result.json`](artifacts/economics_result.json)
- Retention-risk sensitivity: [`artifacts/q3_economics_result.json`](artifacts/q3_economics_result.json)
- Decision registry: [`state/decisions_registry.json`](state/decisions_registry.json)
- Decision log: [`state/decision_log.md`](state/decision_log.md)

The demo does not prove real demand, retention, ARPU, or interface effectiveness. It verifies the end-to-end workflow, reproducible arithmetic, claim tracing, and decision reassessment.

## Tools

- [`scripts/ingest_source.py`](scripts/ingest_source.py) — UTF-8 source packaging with provenance and SHA-256;
- [`scripts/validate_evidence.py`](scripts/validate_evidence.py) — fact, evidence-ID, confidence, and source-locator validation;
- [`scripts/calc_economics.py`](scripts/calc_economics.py) — LTV, CAC, and payback with explicit units and periods;
- [`scripts/recheck_decisions.py`](scripts/recheck_decisions.py) — hashing and source/relevance checks for new material;
- [`scripts/cost_tracker.py`](scripts/cost_tracker.py) — paired measurement of time, tokens, cost, steps, and quality.

All scripts use only the Python 3.12 standard library.

```powershell
python -m unittest discover -s tests -v
```

The suite currently contains 19 tests. Cost tracker supports `add` and `compare`; the paired-run protocol and measured local demo phase are documented in [`artifacts/baseline/comparison.md`](artifacts/baseline/comparison.md).

## Resuming work

The agent first reads [`state/workflow_state.json`](state/workflow_state.json), verifies saved hashes, and continues only unfinished work. Decisions live in [`state/decisions_registry.json`](state/decisions_registry.json), while changes are appended to [`state/decision_log.md`](state/decision_log.md).

When a file is added under [`data/new/`](data/new/), either the hook or `recheck_decisions.py` is run. The script flags affected decisions; it does not change one without evidence review and human/agent assessment.

## Knowledge and validation

- [`knowledge/research-methods.md`](knowledge/research-methods.md) — source reliability, unknowns, and falsification criteria;
- [`knowledge/strategy-framework.md`](knowledge/strategy-framework.md) — product and communication strategy, retention, ARPU, cannibalization, and experiment planning;
- [`knowledge/source-safety.md`](knowledge/source-safety.md) — prompt injection, personal data, secrets, and confidential company data;
- [`schemas/`](schemas/) — JSON schemas for evidence, checkpoints, decisions, and the source manifest.

## Comparison with ordinary chat

[`artifacts/baseline/comparison.md`](artifacts/baseline/comparison.md) defines a paired protocol for measuring time, cost, steps, and quality. The repository does not invent comparison figures: actual IDE billing telemetry and a matched plain-chat baseline were unavailable.

`cost_tracker.py` does not retrieve provider billing automatically. A credible report requires actual tokens and cost for every measured run.

## Submission documentation

- Unified demo case pack: [`projects/demo/DEMO_CASE_PACK.md`](projects/demo/DEMO_CASE_PACK.md)
- Baseline comparison: [`artifacts/baseline/comparison.md`](artifacts/baseline/comparison.md)
- Full architecture and limitation report: [`docs/en/SUBMISSION_REPORT.md`](docs/en/SUBMISSION_REPORT.md)
- Demo video script under 10 minutes: [`docs/en/DEMO_VIDEO_SCRIPT.md`](docs/en/DEMO_VIDEO_SCRIPT.md)
- Russian submission report: [`docs/SUBMISSION_REPORT.md`](docs/SUBMISSION_REPORT.md)
- Russian video script: [`docs/DEMO_VIDEO_SCRIPT.md`](docs/DEMO_VIDEO_SCRIPT.md)
- Run journal: [`artifacts/run_log.jsonl`](artifacts/run_log.jsonl)
- Russian version: [README.md](README.md)
