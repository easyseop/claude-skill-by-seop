#!/usr/bin/env python3
"""Initialize a canonical capability plan bound to current input digests."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

from common import PlannerError, find_repo_root, load_json, planner_dir, sha256_file, write_json


def git_ref(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "UNAVAILABLE"


def initialize(
    repo_root: Path,
    target: str,
    request_path: Path,
    policy_path: Path,
    repo_facts_path: Path,
) -> dict:
    template = load_json(planner_dir(repo_root) / "assets/CAPABILITY_PLAN.template.yaml")
    template["plan_id"] = target
    template["request"]["target"] = target
    template["request"]["request_path"] = request_path.as_posix()
    template["repository_facts"]["path"] = repo_facts_path.as_posix()
    template["repository_facts"]["digest"] = sha256_file(repo_facts_path)
    template["snapshot"] = {
        "planner_version": "recovery-1.0",
        "repository_ref": git_ref(repo_root),
        "source_cutoff": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "input_digests": {
            "request": sha256_file(request_path),
            "policy": sha256_file(policy_path),
            "repo_facts": sha256_file(repo_facts_path),
        },
    }
    template["change_history"].append(
        {
            "event": "INITIALIZED",
            "at": template["snapshot"]["source_cutoff"],
            "subject_digest": None,
        }
    )
    return template


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--repo-facts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        repo_root = (args.repo_root or find_repo_root()).resolve()
        request = args.request.resolve()
        policy = args.policy.resolve()
        facts = args.repo_facts.resolve()
        for path in (request, policy, facts):
            if not path.is_file():
                raise PlannerError(f"required input is missing: {path}")
        plan = initialize(repo_root, args.target, request, policy, facts)
        write_json(args.output, plan)
        print(json.dumps({"status": "PASS", "output": args.output.as_posix()}, ensure_ascii=False))
        return 0
    except PlannerError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
