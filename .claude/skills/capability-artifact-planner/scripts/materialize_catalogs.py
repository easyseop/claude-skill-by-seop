#!/usr/bin/env python3
"""Materialize immutable planner references and eval catalogs from sealed inputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    PlannerError,
    catalog_dir,
    find_repo_root,
    load_json,
    planner_dir,
    require_exact_ids,
    sha256_file,
    write_json,
)


MUTATIONS = [
    ("MUT-01", "remove_primary_owner", "primary_owner_required"),
    ("MUT-02", "remove_acceptance_mapping", "acceptance_coverage_required"),
    ("MUT-03", "remove_selected_component_evidence", "component_evidence_required"),
    ("MUT-04", "remove_rejected_reason", "rejected_reason_required"),
    ("MUT-05", "remove_high_risk_approval", "high_risk_approval_required"),
    ("MUT-06", "remove_write_permission", "write_permission_required"),
    ("MUT-07", "remove_rag_acl", "rag_acl_required"),
    ("MUT-08", "remove_retrieval_eval", "rag_retrieval_eval_required"),
    ("MUT-09", "remove_agent_budget", "agent_budget_required"),
    ("MUT-10", "remove_state_ttl", "state_ttl_required"),
    ("MUT-11", "allow_secret_in_llm_context", "secret_context_prohibited"),
    ("MUT-12", "remove_repository_ref", "repository_ref_required"),
    ("MUT-13", "remove_source_cutoff", "source_cutoff_required"),
    ("MUT-14", "remove_audit_binding", "audit_binding_required"),
    ("MUT-15", "replace_input_digest", "input_freshness_required"),
]


def render_rules_markdown(rules: list[dict]) -> str:
    lines = [
        "# CAP 공통 규칙 정본",
        "",
        "> 이 파일은 봉인된 `CAP_RULES_01_18.json`과 `CAP_RULES_19_36.json`에서 결정적으로 생성한다.",
        "",
    ]
    for rule in rules:
        lines.extend([f"## {rule['id']} — {rule['title']}", ""])
        for key, value in rule.get("fields", {}).items():
            lines.append(f"- **{key}:** {value}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def materialize(repo_root: Path) -> dict:
    source = catalog_dir(repo_root)
    first = load_json(source / "CAP_RULES_01_18.json").get("cap_rules", [])
    second = load_json(source / "CAP_RULES_19_36.json").get("cap_rules", [])
    rules = first + second
    rule_ids = require_exact_ids(rules, "CAP", 1, 36)

    evals = load_json(source / "PLANNER_EVALS_01_22.json").get("planner_evals", [])
    eval_ids = require_exact_ids(evals, "EVAL", 1, 22)

    root = planner_dir(repo_root)
    references = root / "references"
    eval_dir = root / "evals"
    references.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    (references / "CAP_RULES.md").write_text(render_rules_markdown(rules), encoding="utf-8")
    write_json(eval_dir / "planner-evals.yaml", {"schema_version": "1.0", "planner_evals": evals})

    mutation_items = [
        {
            "id": mutation_id,
            "operation": operation,
            "expected_detector": detector,
            "expected_status": "FAIL",
            "critical": True,
        }
        for mutation_id, operation, detector in MUTATIONS
    ]
    write_json(eval_dir / "mutations.yaml", {"schema_version": "1.0", "mutations": mutation_items})

    coverage = {
        "schema_version": "1.0",
        "rules": [
            {
                "rule_id": rule_id,
                "spec_path": "references/CAP_RULES.md",
                "checker": "scripts/check_capability_plan.py",
                "eval_ids": eval_ids,
                "evidence": "docs/agent-authoring/evidence/capability-planner/self-test-summary.json",
            }
            for rule_id in rule_ids
        ],
    }
    write_json(references / "RULE_COVERAGE.yaml", coverage)

    result = {
        "status": "PASS",
        "cap_rules": len(rules),
        "planner_evals": len(evals),
        "mutations": len(mutation_items),
        "source_digests": {
            "CAP_RULES_01_18.json": sha256_file(source / "CAP_RULES_01_18.json"),
            "CAP_RULES_19_36.json": sha256_file(source / "CAP_RULES_19_36.json"),
            "PLANNER_EVALS_01_22.json": sha256_file(source / "PLANNER_EVALS_01_22.json"),
        },
        "outputs": {
            "rules": sha256_file(references / "CAP_RULES.md"),
            "coverage": sha256_file(references / "RULE_COVERAGE.yaml"),
            "evals": sha256_file(eval_dir / "planner-evals.yaml"),
            "mutations": sha256_file(eval_dir / "mutations.yaml"),
        },
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    try:
        repo_root = (args.repo_root or find_repo_root()).resolve()
        result = materialize(repo_root)
        if args.result:
            write_json(args.result, result)
        print(f"PASS CAP={result['cap_rules']} EVAL={result['planner_evals']} MUT={result['mutations']}")
        return 0
    except PlannerError as exc:
        print(f"FAIL {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
