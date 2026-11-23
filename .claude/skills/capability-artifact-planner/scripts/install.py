#!/usr/bin/env python3
"""Idempotent local package verification and catalog materialization."""

from __future__ import annotations

import argparse
import json
import py_compile
from pathlib import Path

from common import PlannerError, find_repo_root, planner_dir, sha256_file, write_json
from materialize_catalogs import materialize


REQUIRED = [
    "SKILL.md",
    "references/decision-guide.md",
    "references/interview-guide.md",
    "references/schema-guide.md",
    "assets/REQUEST.template.md",
    "assets/PROJECT_POLICY.template.yaml",
    "assets/CAPABILITY_PLAN.template.yaml",
    "assets/REPO_FACTS.template.json",
    "assets/PLANNER_EVALS.template.yaml",
    "scripts/common.py",
    "scripts/materialize_catalogs.py",
    "scripts/discover_repository.py",
    "scripts/init_capability_plan.py",
    "scripts/check_capability_plan.py",
    "scripts/derive_contracts.py",
    "scripts/audit_capability_plan.py",
    "scripts/planner_stop_gate.py",
    "scripts/run_self_tests.py",
]


def verify(repo_root: Path) -> dict:
    root = planner_dir(repo_root)
    missing = [item for item in REQUIRED if not (root / item).is_file()]
    if missing:
        raise PlannerError(f"missing planner package files: {missing}")

    compiled = []
    for path in sorted((root / "scripts").glob("*.py")):
        py_compile.compile(str(path), doraise=True)
        compiled.append(path.relative_to(repo_root).as_posix())

    catalog = materialize(repo_root)
    files = {
        path.relative_to(repo_root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }
    return {
        "schema_version": "1.0",
        "status": "PASS",
        "required_files": len(REQUIRED),
        "compiled_python": compiled,
        "catalog": catalog,
        "file_digests": files,
        "settings_modified": False,
        "operational_permission": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        repo_root = (args.repo_root or find_repo_root()).resolve()
        result = verify(repo_root)
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (PlannerError, py_compile.PyCompileError) as exc:
        result = {"schema_version": "1.0", "status": "FAIL", "error": str(exc)}
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
