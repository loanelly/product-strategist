#!/usr/bin/env python3
"""Mark decisions for review when new files match their evidence or watch terms."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {".csv", ".htm", ".html", ".json", ".md", ".txt", ".xml"}
TOKEN = re.compile(r"[\w-]+", re.UNICODE)
SOURCE_ID = re.compile(r"(?m)^\s*(?:source_id|id)\s*:\s*['\"]?([A-Za-z0-9_.:-]+)")
TAGS = re.compile(r"(?m)^\s*tags\s*:\s*(.+)$")


class RecheckError(ValueError):
    """Raised when the registry or incoming material is invalid."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RecheckError(f"Cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RecheckError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RecheckError(f"{path} must contain a JSON object")
    return value


def extract_metadata(path: Path, text: str) -> tuple[set[str], set[str]]:
    source_ids: set[str] = set()
    tags: set[str] = set()
    if path.suffix.lower() == ".json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RecheckError(f"Invalid JSON in incoming file {path}: {exc}") from exc
        if isinstance(payload, dict):
            for key in ("source_id", "id"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    source_ids.add(value.strip().casefold())
            raw_tags = payload.get("tags", [])
            if isinstance(raw_tags, list):
                tags.update(item.strip().casefold() for item in raw_tags if isinstance(item, str))
    for match in SOURCE_ID.finditer(text[:8192]):
        source_ids.add(match.group(1).casefold())
    for match in TAGS.finditer(text[:8192]):
        tags.update(
            item.strip(" '\"\t").casefold()
            for item in re.split(r"[,;]", match.group(1))
            if item.strip(" '\"\t")
        )
    return source_ids, tags


def update_registry(registry: dict[str, Any], new_dir: Path) -> dict[str, Any]:
    decisions = registry.get("decisions")
    processed = registry.get("processed_files")
    if not isinstance(decisions, list) or not isinstance(processed, dict):
        raise RecheckError("Registry must contain 'decisions' array and 'processed_files' object")
    for decision in decisions:
        if not isinstance(decision, dict) or not isinstance(decision.get("id"), str):
            raise RecheckError("Each decision must be an object with a string id")

    if not new_dir.exists():
        return {"scanned": 0, "changed_files": [], "affected_decisions": []}
    if not new_dir.is_dir():
        raise RecheckError(f"Incoming path is not a directory: {new_dir}")

    changed_files: list[str] = []
    affected: dict[str, set[str]] = {}
    new_root = new_dir.resolve()
    candidates = sorted(
        path
        for path in new_root.rglob("*")
        if path.is_file() and path.name.casefold() != "readme.md"
    )
    for path in candidates:
        if not path.resolve().is_relative_to(new_root):
            raise RecheckError(f"Incoming file resolves outside the data directory: {path}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            raise RecheckError(f"Unsupported incoming file type: {path}")
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except OSError as exc:
            raise RecheckError(f"Cannot read incoming file {path}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise RecheckError(f"Incoming file is not UTF-8 text: {path}") from exc
        relative = path.relative_to(new_root).as_posix()
        digest = hashlib.sha256(raw).hexdigest()
        previous = processed.get(relative)
        if isinstance(previous, dict) and previous.get("sha256") == digest:
            continue

        changed_files.append(relative)
        source_ids, tags = extract_metadata(path, text)
        tokens = {token.casefold() for token in TOKEN.findall(text)}
        for decision in decisions:
            if decision.get("status") in {"rejected", "superseded"}:
                continue
            reasons: list[str] = []
            refs = decision.get("source_ids", [])
            terms = decision.get("watch_terms", [])
            if not isinstance(refs, list) or not isinstance(terms, list):
                raise RecheckError(f"{decision['id']}: source_ids and watch_terms must be arrays")
            matched_sources = [
                ref for ref in refs
                if isinstance(ref, str) and ref.casefold() in source_ids
            ]
            if matched_sources:
                reasons.append("incoming material declares related source id(s): " + ", ".join(matched_sources))
            matched_terms = [
                term for term in terms
                if isinstance(term, str)
                and term.strip()
                and (
                    term.casefold() in tags
                    or set(TOKEN.findall(term.casefold())).issubset(tokens)
                )
            ]
            if matched_terms:
                reasons.append("watch term(s) found: " + ", ".join(matched_terms))
            if reasons:
                decision_id = decision["id"]
                affected.setdefault(decision_id, set()).update(reasons)
                decision["status"] = "review_required"
                existing = decision.setdefault("review_reasons", [])
                if not isinstance(existing, list):
                    raise RecheckError(f"{decision_id}: review_reasons must be an array")
                for reason in reasons:
                    if reason not in existing:
                        existing.append(reason)
        processed[relative] = {"path": relative, "sha256": digest}

    return {
        "scanned": len(candidates),
        "changed_files": changed_files,
        "affected_decisions": [
            {
                "id": decision_id,
                "claim_ids": next(
                    decision.get("claim_ids", [])
                    for decision in decisions
                    if decision["id"] == decision_id
                ),
                "reasons": sorted(reasons),
            }
            for decision_id, reasons in sorted(affected.items())
        ],
    }


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False, newline="\n"
        ) as stream:
            temporary_name = stream.name
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temporary_name, path)
    except OSError:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("state/decisions_registry.json"))
    parser.add_argument("--new-dir", type=Path, default=Path("data/new"))
    args = parser.parse_args()
    try:
        registry = read_json(args.registry)
        report = update_registry(registry, args.new_dir)
        if report["changed_files"]:
            atomic_write_json(args.registry, registry)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    except (OSError, RecheckError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
