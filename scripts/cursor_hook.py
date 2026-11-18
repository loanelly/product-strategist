#!/usr/bin/env python3
"""Cursor hooks: enforce the fetch allowlist and validate edited strategies."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ALLOWED_HOSTS = (
    "megafon.ru",
    "*.megafon.ru",
    "rosstat.gov.ru",
    "data.gov.ru",
    "cbr.ru",
    "*.cbr.ru",
    "oecd.org",
    "*.oecd.org",
    "ec.europa.eu",
)


def host_allowed(hostname: str) -> bool:
    host = hostname.rstrip(".").encode("idna").decode("ascii").casefold()
    for allowed in ALLOWED_HOSTS:
        pattern = allowed.casefold()
        if pattern.startswith("*."):
            suffix = pattern[2:]
            if host.endswith("." + suffix) and host != suffix:
                return True
        elif host == pattern:
            return True
    return False


def mcp_result(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("hook_event_name") != "beforeMCPExecution":
        return {"permission": "deny", "user_message": "Unexpected MCP hook event."}
    if payload.get("mcp_server_name") != "fetch":
        return {"permission": "deny", "user_message": "Only the configured fetch MCP server is allowed."}
    raw_input = payload.get("tool_input")
    if isinstance(raw_input, str):
        try:
            tool_input = json.loads(raw_input)
        except json.JSONDecodeError:
            return {"permission": "deny", "user_message": "Malformed fetch URL parameters."}
    else:
        tool_input = raw_input
    if not isinstance(tool_input, dict) or not isinstance(tool_input.get("url"), str):
        return {"permission": "deny", "user_message": "Fetch requires a valid URL."}
    parsed = urlsplit(tool_input["url"])
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        return {"permission": "deny", "user_message": "Only public HTTP(S) URLs without credentials are allowed."}
    try:
        allowed = host_allowed(parsed.hostname)
    except UnicodeError:
        allowed = False
    if not allowed:
        return {
            "permission": "deny",
            "user_message": f"Fetch domain is not allowlisted: {parsed.hostname}",
            "agent_message": "Use only public sources from the fetch server's configured allowed-host list.",
        }
    return {"permission": "allow"}


def post_edit_result(payload: dict[str, Any], root: Path) -> dict[str, Any]:
    event = payload.get("hook_event_name")
    if event not in {"afterFileEdit", "workspaceOpen"}:
        return {}
    try:
        strategy = (root / "artifacts" / "strategy.md").resolve()
        registry = root / "state" / "decisions_registry.json"
        edited_path = payload.get("file_path")
        if event == "workspaceOpen":
            should_recheck = registry.is_file() and (root / "data" / "new").is_dir()
            should_validate = False
        elif isinstance(edited_path, str):
            edited = Path(edited_path).resolve()
            incoming = (root / "data" / "new").resolve()
            should_recheck = (
                registry.is_file()
                and edited != incoming
                and incoming in edited.parents
            )
            should_validate = edited == strategy
        else:
            return {}
        if not should_recheck and not should_validate:
            return {}
        messages: list[str] = []
        if should_recheck:
            recheck = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts" / "recheck_decisions.py"),
                    "--registry",
                    str(registry),
                    "--new-dir",
                    str(root / "data" / "new"),
                ],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                timeout=25,
            )
            recheck_output = (recheck.stdout + recheck.stderr).strip()
            if recheck.returncode:
                messages.append(f"Decision recheck failed:\n{recheck_output}")
            elif recheck_output:
                messages.append(f"Decision recheck result:\n{recheck_output}")
        if should_validate:
            validation = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts" / "validate_evidence.py"),
                    "--strategy",
                    str(strategy),
                    "--graph",
                    str(root / "state" / "evidence_graph.json"),
                ],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                timeout=25,
            )
            validation_output = (validation.stdout + validation.stderr).strip()
            messages.append(
                "Strategy evidence validation passed."
                if validation.returncode == 0
                else f"Strategy evidence validation failed; fix before presenting:\n{validation_output}"
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"additional_context": f"Automatic project check could not run: {exc}"}
    if event == "workspaceOpen":
        if messages:
            sys.stderr.write("\n".join(messages) + "\n")
        return {}
    return {"additional_context": "\n".join(messages)} if messages else {}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"Invalid Cursor hook JSON: {exc}", file=sys.stderr)
        print(json.dumps({"permission": "deny", "user_message": "Invalid hook input."}))
        return 2
    if not isinstance(payload, dict):
        print(json.dumps({"permission": "deny", "user_message": "Invalid hook input."}))
        return 2
    event = payload.get("hook_event_name")
    root = Path(__file__).resolve().parents[1]
    if event == "beforeMCPExecution":
        result = mcp_result(payload)
    else:
        result = post_edit_result(payload, root)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
