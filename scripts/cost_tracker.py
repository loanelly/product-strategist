#!/usr/bin/env python3
"""Record run-level cost/quality metrics and compare an agent with chat baseline."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

FIELDS = (
    "duration_seconds",
    "tokens_input",
    "tokens_output",
    "cost_usd",
    "tool_calls",
    "workflow_steps",
    "claims_total",
    "claims_sourced",
    "calculations_checked",
    "risk_findings",
)


class TrackerError(ValueError):
    """Raised for invalid metrics or log data."""


def read_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise TrackerError(f"Cannot read {path}: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TrackerError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
        if not isinstance(record, dict):
            raise TrackerError(f"{path}:{line_number} must be a JSON object")
        records.append(record)
    return records


def validate_record(record: dict[str, Any]) -> None:
    if not isinstance(record.get("scenario_id"), str) or not record["scenario_id"].strip():
        raise TrackerError("scenario_id must be a non-empty string")
    if record.get("mode") not in {"agent", "baseline"}:
        raise TrackerError("mode must be 'agent' or 'baseline'")
    if not isinstance(record.get("run_id"), str) or not record["run_id"].strip():
        raise TrackerError("run_id must be a non-empty string")
    for field in FIELDS:
        value = record.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TrackerError(f"{field} must be numeric")
        if not math.isfinite(value):
            raise TrackerError(f"{field} must be finite")
        if value < 0:
            raise TrackerError(f"{field} cannot be negative")
    if record["claims_sourced"] > record["claims_total"]:
        raise TrackerError("claims_sourced cannot exceed claims_total")
    if int(record["claims_total"]) != record["claims_total"]:
        raise TrackerError("claims_total must be a whole number")
    if int(record["claims_sourced"]) != record["claims_sourced"]:
        raise TrackerError("claims_sourced must be a whole number")
    for field in (
        "tokens_input",
        "tokens_output",
        "tool_calls",
        "workflow_steps",
        "calculations_checked",
        "risk_findings",
    ):
        if int(record[field]) != record[field]:
            raise TrackerError(f"{field} must be a whole number")


def summarize(records: list[dict[str, Any]], scenario_id: str) -> dict[str, Any]:
    selected = [record for record in records if record.get("scenario_id") == scenario_id]
    grouped = {
        mode: [record for record in selected if record.get("mode") == mode]
        for mode in ("baseline", "agent")
    }
    if not grouped["baseline"] or not grouped["agent"]:
        raise TrackerError(
            f"Scenario {scenario_id!r} needs at least one baseline and one agent run"
        )
    result: dict[str, Any] = {"scenario_id": scenario_id, "runs": {}}
    for mode, items in grouped.items():
        for item in items:
            validate_record(item)
        count = len(items)
        claims_total = sum(item["claims_total"] for item in items)
        claims_sourced = sum(item["claims_sourced"] for item in items)
        result["runs"][mode] = {
            "run_count": count,
            "mean_duration_seconds": round(sum(item["duration_seconds"] for item in items) / count, 4),
            "mean_cost_usd": round(sum(item["cost_usd"] for item in items) / count, 6),
            "mean_tokens_input": round(sum(item["tokens_input"] for item in items) / count, 2),
            "mean_tokens_output": round(sum(item["tokens_output"] for item in items) / count, 2),
            "mean_tool_calls": round(sum(item["tool_calls"] for item in items) / count, 2),
            "mean_workflow_steps": round(sum(item["workflow_steps"] for item in items) / count, 2),
            "sourced_claims": claims_sourced,
            "total_claims": claims_total,
            "sourced_claim_coverage": (
                round(claims_sourced / claims_total, 6) if claims_total else None
            ),
            "calculations_checked": sum(item["calculations_checked"] for item in items),
            "risk_findings": sum(item["risk_findings"] for item in items),
        }
    baseline = result["runs"]["baseline"]
    agent = result["runs"]["agent"]
    result["agent_vs_baseline"] = {
        "duration_reduction_percent": _reduction(
            baseline["mean_duration_seconds"], agent["mean_duration_seconds"]
        ),
        "cost_reduction_percent": _reduction(
            baseline["mean_cost_usd"], agent["mean_cost_usd"]
        ),
        "sourced_claim_coverage_delta_percentage_points": _coverage_delta(
            baseline["sourced_claim_coverage"], agent["sourced_claim_coverage"]
        ),
    }
    return result


def _reduction(baseline: float, agent: float) -> float | None:
    if baseline == 0:
        return None
    return round((baseline - agent) / baseline * 100, 2)


def _coverage_delta(baseline: float | None, agent: float | None) -> float | None:
    if baseline is None or agent is None:
        return None
    return round((agent - baseline) * 100, 2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add", help="Append one measured run")
    add_parser.add_argument("--log", type=Path, default=Path("artifacts/run_log.jsonl"))
    add_parser.add_argument("--scenario-id", required=True)
    add_parser.add_argument("--run-id", required=True)
    add_parser.add_argument("--mode", choices=("agent", "baseline"), required=True)
    for field in FIELDS:
        add_parser.add_argument(f"--{field.replace('_', '-')}", type=float, required=True)

    compare_parser = subparsers.add_parser("compare", help="Compare paired scenario runs")
    compare_parser.add_argument("--log", type=Path, default=Path("artifacts/run_log.jsonl"))
    compare_parser.add_argument("--scenario-id", required=True)
    args = parser.parse_args()
    try:
        records = read_log(args.log)
        if args.command == "add":
            record: dict[str, Any] = {
                "scenario_id": args.scenario_id,
                "run_id": args.run_id,
                "mode": args.mode,
                **{field: getattr(args, field) for field in FIELDS},
            }
            validate_record(record)
            args.log.parent.mkdir(parents=True, exist_ok=True)
            with args.log.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(json.dumps({"recorded": record}, indent=2, ensure_ascii=False))
        else:
            print(
                json.dumps(
                    summarize(records, args.scenario_id), indent=2, ensure_ascii=False
                )
            )
    except OSError as exc:
        print(f"ERROR: Cannot write {args.log}: {exc}", file=sys.stderr)
        return 2
    except TrackerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
