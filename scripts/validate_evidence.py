#!/usr/bin/env python3
"""Validate structured claims in a strategy against the evidence graph."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CLAIM_LINE = re.compile(
    r"^\s*-\s+\[(FACT|HYPOTHESIS|FORECAST)\]\s+(.+?)\s*\|\s*"
    r"evidence:\s*([A-Za-z0-9_, -]+)\s*\|\s*"
    r"confidence:\s*(low|medium|high)\s*$",
    re.IGNORECASE,
)


class ValidationError(ValueError):
    """Raised when an artifact cannot be safely validated."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValidationError(f"Cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path} must contain a JSON object")
    return value


def validate(strategy: str, graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = graph.get("sources")
    claims = graph.get("claims")
    if not isinstance(sources, list) or not isinstance(claims, list):
        return ["Evidence graph must have 'sources' and 'claims' arrays"]

    source_by_id: dict[str, dict[str, Any]] = {}
    claim_by_id: dict[str, dict[str, Any]] = {}
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str):
            errors.append("Every source must be an object with a string id")
            continue
        if source["id"] in source_by_id:
            errors.append(f"Duplicate source id: {source['id']}")
        source_by_id[source["id"]] = source

    for claim in claims:
        if not isinstance(claim, dict) or not isinstance(claim.get("id"), str):
            errors.append("Every graph claim must be an object with a string id")
            continue
        if claim["id"] in claim_by_id:
            errors.append(f"Duplicate claim id: {claim['id']}")
        claim_by_id[claim["id"]] = claim
        if claim.get("type") not in {"fact", "hypothesis", "forecast"}:
            errors.append(f"{claim['id']}: invalid or missing claim type")
        if claim.get("confidence") not in {"low", "medium", "high"}:
            errors.append(f"{claim['id']}: invalid or missing confidence")
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list) or any(not isinstance(item, str) for item in source_ids):
            errors.append(f"{claim['id']}: source_ids must be an array of strings")
            continue
        if claim.get("type") == "fact" and not source_ids:
            errors.append(f"{claim['id']}: fact has no source")
        for source_id in source_ids:
            source = source_by_id.get(source_id)
            if source is None:
                errors.append(f"{claim['id']}: unknown source id {source_id}")
            elif not isinstance(source.get("locator"), str) or not source["locator"].strip():
                errors.append(f"{claim['id']}: source {source_id} has no locator")
        if claim.get("type") == "fact" and (
            not isinstance(claim.get("exact_location"), str)
            or not claim["exact_location"].strip()
        ):
            errors.append(f"{claim['id']}: fact has no exact source location")

    claim_lines = 0
    for line_number, line in enumerate(strategy.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = CLAIM_LINE.fullmatch(line)
        if not match:
            errors.append(
                f"Line {line_number}: content must use the required "
                "[FACT]/[HYPOTHESIS]/[FORECAST] evidence format"
            )
            continue
        claim_lines += 1
        kind, text, evidence_list, confidence = match.groups()
        if not text.strip():
            errors.append(f"Line {line_number}: claim text is empty")
            continue
        evidence_ids = [item.strip() for item in evidence_list.split(",") if item.strip()]
        if not evidence_ids:
            errors.append(f"Line {line_number}: at least one evidence claim ID is required")
            continue
        expected_type = {"FACT": "fact", "HYPOTHESIS": "hypothesis", "FORECAST": "forecast"}[kind.upper()]
        for evidence_id in evidence_ids:
            claim = claim_by_id.get(evidence_id)
            if claim is None:
                errors.append(f"Line {line_number}: unknown evidence claim ID {evidence_id}")
                continue
            if claim.get("type") != expected_type:
                errors.append(
                    f"Line {line_number}: [{kind.upper()}] references "
                    f"{evidence_id} of type {claim.get('type')!r}"
                )
            if claim.get("confidence") != confidence.lower():
                errors.append(
                    f"Line {line_number}: confidence does not match graph entry {evidence_id}"
                )
            if expected_type == "fact":
                source_ids = claim.get("source_ids", [])
                if not isinstance(source_ids, list) or not source_ids:
                    errors.append(f"Line {line_number}: fact {evidence_id} has no source")
    if claim_lines == 0:
        errors.append("Strategy contains no structured claims")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", type=Path, default=Path("artifacts/strategy.md"))
    parser.add_argument("--graph", type=Path, default=Path("state/evidence_graph.json"))
    args = parser.parse_args()

    try:
        strategy = args.strategy.read_text(encoding="utf-8")
        graph = load_json(args.graph)
    except OSError as exc:
        print(f"ERROR: Cannot read {args.strategy}: {exc}", file=sys.stderr)
        return 2
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(strategy, graph)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Evidence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
