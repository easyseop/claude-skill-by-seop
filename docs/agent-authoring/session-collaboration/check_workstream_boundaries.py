#!/usr/bin/env python3
"""Enforce branch-specific workstream ownership and sealed prepared inputs."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def current_branch() -> str:
    env_branch = os.environ.get("WORKSTREAM_BRANCH") or os.environ.get("GITHUB_HEAD_REF")
    if env_branch:
        return env_branch
    return run_git("rev-parse", "--abbrev-ref", "HEAD").strip()


def changed_files(base: str | None, file_list: Path | None) -> list[str]:
    if file_list:
        return [line.strip() for line in file_list.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not base:
        base = os.environ.get("WORKSTREAM_BASE") or os.environ.get("GITHUB_BASE_REF") or "main"
    try:
        output = run_git("-c", "core.quotepath=false", "diff", "--name-only", f"origin/{base}...HEAD")
    except RuntimeError:
        output = run_git("-c", "core.quotepath=false", "diff", "--name-only", f"{base}...HEAD")
    return [line.strip() for line in output.splitlines() if line.strip()]


def matches(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def select_rule(config: dict, branch: str) -> dict | None:
    for rule in config.get("workstreams", []):
        if fnmatch.fnmatchcase(branch, rule["branch_pattern"]):
            return rule
    return None


def git_blob_sha(path: str) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(path)
    return run_git("hash-object", "--", path).strip()


def load_prepared_overrides(path: Path, branch: str) -> tuple[dict[str, str], list[str]]:
    if not path.is_file():
        return {}, []
    data = json.loads(path.read_text(encoding="utf-8"))
    prepared: dict[str, str] = {}
    applied: list[str] = []
    for item in data.get("overrides", []):
        pattern = item.get("branch_pattern")
        if pattern and fnmatch.fnmatchcase(branch, pattern):
            prepared.update(item.get("prepared_path_blobs", {}))
            applied.append(pattern)
    return prepared, applied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="docs/agent-authoring/session-collaboration/WORKSTREAM_BOUNDARIES.json",
    )
    parser.add_argument(
        "--overrides",
        default="docs/agent-authoring/session-collaboration/PREPARED_INPUT_OVERRIDES.json",
    )
    parser.add_argument("--branch")
    parser.add_argument("--base")
    parser.add_argument("--changed-files", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    branch = args.branch or current_branch()
    files = changed_files(args.base, args.changed_files)
    rule = select_rule(config, branch)
    override_prepared, applied_overrides = load_prepared_overrides(Path(args.overrides), branch)

    result = {
        "schema_version": "1.2",
        "branch": branch,
        "base": args.base,
        "status": "FAIL",
        "changed_files": files,
        "prepared_paths_verified": [],
        "prepared_override_patterns": applied_overrides,
        "violations": [],
    }

    if rule is None:
        result["violations"].append(
            {"path": None, "code": "UNKNOWN_WORKSTREAM", "message": "No branch ownership rule matched."}
        )
    else:
        writable = rule.get("writable_paths", [])
        read_only = rule.get("read_only_paths", [])
        prepared = dict(rule.get("prepared_path_blobs", {}))
        prepared.update(override_prepared)
        forbidden = config.get("global_forbidden", []) + rule.get("forbidden_paths", [])
        orchestrator_only = config.get("shared_orchestrator_only", [])
        owner_role = rule.get("owner_role")

        for path in files:
            if matches(path, forbidden):
                result["violations"].append(
                    {"path": path, "code": "FORBIDDEN_PATH", "message": "Path is explicitly forbidden."}
                )
                continue

            if matches(path, orchestrator_only) and owner_role != "orchestrator":
                result["violations"].append(
                    {
                        "path": path,
                        "code": "ORCHESTRATOR_ONLY",
                        "message": "Only the orchestrator workstream may modify this shared file.",
                    }
                )
                continue

            if path in prepared:
                try:
                    actual_sha = git_blob_sha(path)
                except (FileNotFoundError, RuntimeError) as exc:
                    result["violations"].append(
                        {
                            "path": path,
                            "code": "PREPARED_INPUT_MISSING",
                            "message": f"Prepared read-only input is missing or unreadable: {exc}",
                            "expected_blob": prepared[path],
                        }
                    )
                    continue
                if actual_sha != prepared[path]:
                    result["violations"].append(
                        {
                            "path": path,
                            "code": "PREPARED_INPUT_MODIFIED",
                            "message": "Orchestrator-prepared input differs from its sealed Git blob digest.",
                            "expected_blob": prepared[path],
                            "actual_blob": actual_sha,
                        }
                    )
                    continue
                result["prepared_paths_verified"].append(
                    {"path": path, "blob_sha": actual_sha}
                )
                continue

            if matches(path, read_only):
                result["violations"].append(
                    {"path": path, "code": "READ_ONLY_PATH", "message": "Path is input/reference only."}
                )
                continue

            if not matches(path, writable):
                result["violations"].append(
                    {
                        "path": path,
                        "code": "OUTSIDE_OWNERSHIP",
                        "message": "Changed path is outside this workstream's writable paths.",
                    }
                )

    if not result["violations"]:
        result["status"] = "PASS"

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
