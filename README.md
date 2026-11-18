# Product Strategist — IDE agent for digital product decisions

An IDE-orchestrated research workflow that turns a product question and
authorized materials into source-linked evidence, materially different
options, a product and communication strategy, an adversarial review, and a
resumable decision record. The IDE agent orchestrates; Python 3.12 scripts are
deterministic tools only. There is no custom LLM loop.

The included Family Cloud demo uses fictional data plus limited public
Eurostat context. It describes **no real MegaFon product or customers**.

## Run in about 3 minutes

Prerequisites: Python 3.12 and an IDE agent such as Cursor, GitHub Copilot, or
Claude Code. Internet access is needed for the optional Fetch MCP server's
first start. No API key is required to run tests or deterministic tools.

1. Open this folder as a trusted workspace in your IDE. The agent should read
   `AGENTS.md` and resume at the checkpoint in `state/workflow_state.json`.
2. In Cursor, approve/install the configured `fetch` MCP server (`uvx
   mcp-server-fetch`) if public web research is wanted. Its domains are
   allowlisted in `.cursor/mcp.json` and checked again by the Cursor hook.
3. Run the tests and the demo tools:

   ```powershell
   python --version
   python -m unittest discover -s tests -v
   python scripts/validate_evidence.py
   python scripts/calc_economics.py data/raw/demo/economics_input.json
   python scripts/calc_economics.py data/raw/demo/q3_economics_sensitivity_input.json
   python scripts/recheck_decisions.py
   ```

The repository starts with `DEMO-D-001` at `review_required`:
`data/new/q3_churn_update.md` is an intentionally synthetic counterexample,
not real churn evidence. `artifacts/recheck_report.json` preserves the first
recheck result. Re-running is safe: unchanged input hashes are skipped.

## Start a new project

Ask the IDE agent to use `skills/intake/SKILL.md`, create an authorized project
brief, and pause for human approval before research. Put only permitted,
sanitized inputs in the project's `data/` area. Follow
`knowledge/source-safety.md`; do not commit secrets, personal data, or
confidential company materials. To wrap an authorized UTF-8 text source while
preserving a hash and untrusted-data boundary:

```powershell
python scripts/ingest_source.py path\to\source.txt --source-id SRC-001 --locator "file:path\to\source.txt"
```

The owner may configure optional model-provider environment variables from
`.env.example` in their IDE secret store. The repository has no default model
provider or embedded credentials; check the chosen model's pricing and log
actual tokens and cost if running a paid model.

## Architecture

```text
Cursor / Copilot / Claude Code
          |
          +-- AGENTS.md + IDE adapters + modular skills
          +-- approved human checkpoints
          +-- Fetch MCP (public allowlisted hosts; Cursor hook checks URLs)
          +-- Python 3.12 deterministic tools
          |      ingest_source / validate_evidence / calc_economics
          |      cost_tracker / recheck_decisions
          +-- state/ checkpoints, evidence graph, decision registry/log
          +-- artifacts/ strategy, review, run log, baseline report
```

`AGENTS.md` is canonical; `CLAUDE.md` and `.github/copilot-instructions.md`
are thin adapters. The separate `adversarial-reviewer` Cursor subagent gets
only the brief and finalized artifacts, not strategy-generation history.
Hooks recheck decisions on workspace open/new-data edits and validate the
strategy after edits. `recheck_decisions.py` uses source IDs/watch terms to
flag candidates, not an LLM or semantic detector; an agent/human decides
whether a conclusion actually changed.

## Skills and knowledge

Skills in `skills/` cover intake, research, synthetic respondents, UX and
multimodal audit, data analysis, strategy, adversarial review, and decision
follow-up. `knowledge/` documents source evaluation/falsification, strategy
quality, and safe handling. Synthetic respondents are hypothesis prompts
only; they cannot establish demand or prevalence.

## Python tools

- `ingest_source.py`: UTF-8 source wrapper with origin and SHA-256; source text
  remains explicitly untrusted.
- `validate_evidence.py`: checks structured strategy claims, evidence IDs,
  claim type/confidence, and source locators. Facts require exact source
  locations.
- `calc_economics.py`: reproducibly calculates monthly LTV, CAC, and payback
  only when inputs/units are explicit; it does not infer retention or model
  cannibalization.
- `recheck_decisions.py`: scans supported UTF-8 text files, stores hashes,
  and flags decisions by source-ID or watch-term matches.
- `cost_tracker.py`: aggregates manually recorded paired runs by elapsed time,
  token/cost reports, tool calls, workflow steps, evidence coverage,
  calculations, and identified risks. It does not retrieve provider billing
  data; use the actual IDE/provider usage report as the record of cost.

All scripts use only Python's standard library. Run tests with:

```powershell
python -m unittest discover -s tests -v
```

## Project map

| Path | Purpose |
|---|---|
| `AGENTS.md`, `.cursor/`, `.github/`, `CLAUDE.md` | Portable agent instructions, MCP, hooks, isolated reviewer |
| `skills/`, `knowledge/` | Reusable procedures and methods |
| `schemas/` | Contracts for evidence, checkpoint, decisions, and source manifest |
| `scripts/`, `tests/` | Deterministic tools and standard-library tests |
| `data/raw/demo/`, `projects/demo/` | Explicitly fictional demonstration inputs and brief |
| `state/`, `data/source_manifest.json` | Resumable work, evidence, decisions, source provenance |
| `artifacts/`, `docs/` | Strategy, economics, review, baseline method, submission/video documents |

## Baseline and known limits

`artifacts/baseline/comparison.md` describes a paired, reproducible comparison
against a plain chat prompt. No honest LLM-token/cost or baseline-run figures
are claimed for this repository snapshot: the IDE/provider usage report and a
matched ordinary-chat run were not available to the local scripts. Record
both actual runs before reporting efficiency as a measured result.
`docs/SUBMISSION_REPORT.md` documents the current state and restrictions.
