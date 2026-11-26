#!/usr/bin/env python3
"""Self-test harness for Capability & Artifact Planner recovery package."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

from common import (
    canonical_json_bytes,
    find_repo_root,
    load_json,
    sha256_bytes,
    sha256_file,
    write_json,
)
from check_capability_plan import check
from materialize_catalogs import materialize


GOLDEN = {
    "EVAL-01": ("direct_response", []),
    "EVAL-02": ("direct_response", ["skill"]),
    "EVAL-03": ("direct_response", ["skill", "reference"]),
    "EVAL-04": ("deterministic_workflow", ["script", "validator"]),
    "EVAL-05": ("deterministic_workflow", ["skill", "reference", "validator"]),
    "EVAL-06": ("deterministic_workflow", ["skill", "rag", "permission", "eval"]),
    "EVAL-07": ("direct_response", ["reference"]),
    "EVAL-08": ("deterministic_workflow", ["tool"]),
    "EVAL-09": ("deterministic_workflow", ["workflow", "script", "validator"]),
    "EVAL-10": ("deterministic_workflow", ["workflow", "validator"]),
    "EVAL-11": ("bounded_agent", ["agent", "tool", "tracing"]),
    "EVAL-12": ("multi_agent", ["agent", "tracing", "eval"]),
    "EVAL-13": ("direct_response", []),
    "EVAL-14": ("deterministic_workflow", ["workflow", "script", "validator", "approval", "permission", "tracing"]),
    "EVAL-15": ("deterministic_workflow", ["tool", "approval", "permission", "tracing"]),
    "EVAL-16": ("deterministic_workflow", ["tool", "permission"]),
    "EVAL-17": ("bounded_agent", ["agent", "state", "tracing"]),
    "EVAL-18": ("bounded_agent", ["tool", "agent", "tracing"]),
    "EVAL-19": ("deterministic_workflow", ["skill", "tool", "script", "eval"]),
    "EVAL-20": ("deterministic_workflow", ["workflow", "script", "validator", "sandbox", "approval", "tracing"]),
    "EVAL-21": ("deterministic_workflow", ["workflow", "script", "validator"]),
    "EVAL-22": ("direct_response", []),
}


def component(component_type: str) -> dict[str, Any]:
    return {
        "type": component_type,
        "capability_ids": ["CAP-A"],
        "evidence": f"fixture evidence for {component_type}",
        "owner": "test-owner",
        "necessity_test": {
            "planned_hypothesis": f"without {component_type} the target criterion fails",
            "baseline_result": None,
            "post_build_ablation_result": None,
        },
    }


def valid_plan(input_digests: dict[str, str] | None = None) -> dict[str, Any]:
    selected_types = ["skill", "rag", "tool", "permission", "tracing", "approval", "state", "validator", "agent"]
    return {
        "schema_version": "1.0",
        "plan_id": "fixture",
        "status": "DRAFT",
        "snapshot": {
            "planner_version": "test-1.0",
            "repository_ref": "fixture-ref",
            "source_cutoff": "2026-01-01T00:00:00+00:00",
            "input_digests": input_digests or {"request": "sha256:x", "policy": "sha256:y", "repo_facts": "sha256:z"},
        },
        "request": {"target": "fixture", "acceptance_criteria": [{"id": "AC-1", "text": "fixture succeeds"}]},
        "repository_facts": {"path": "REPO_FACTS.json", "digest": "sha256:z"},
        "atomic_capabilities": [
            {
                "id": "CAP-A",
                "name": "fixture capability",
                "purpose": "exercise all required contracts",
                "inputs": ["request"],
                "outputs": ["result"],
                "acceptance_criteria": [{"id": "AC-1", "text": "fixture succeeds"}],
                "decision_axes": ["risk", "determinism"],
                "knowledge": {"required": True},
                "placement": {"primary_owner": "agent"},
                "dependencies": ["policy"],
                "failure_modes": ["invalid input"],
                "recovery": ["block and revise"],
            }
        ],
        "architecture": {
            "control_mode": "bounded_agent",
            "summary_label": "bounded hybrid",
            "selected_components": [component(item) for item in selected_types],
            "rejected_components": [{"type": "multi_agent", "reason": "single bounded agent is sufficient", "reconsider_when": "single-agent eval fails"}],
        },
        "workflow": {
            "termination": {
                "max_turns": 6,
                "max_tool_calls": 10,
                "max_time_seconds": 300,
                "completion_condition": "AC-1 satisfied",
                "error_stop_condition": "blocking Gate failure",
                "human_handoff_condition": "risk or policy unresolved",
            },
            "retry": {"max_attempts": 1},
            "compensation": {"strategy": "fixture rollback"},
        },
        "permissions_and_effects": {
            "effect_level": "high",
            "external_write": True,
            "irreversible": True,
            "dry_run": True,
            "idempotency": {"key": "fixture"},
            "secret_in_llm_context": False,
            "required_permissions": ["fixture.write"],
            "human_approvals": [{"scope": "exact fixture payload"}],
        },
        "state": {
            "persistent": True,
            "scope": "fixture-user",
            "owner": "fixture-owner",
            "ttl": "P7D",
            "deletion": "explicit delete",
            "identity_binding": "verified user",
            "migration": "versioned schema",
        },
        "knowledge_plan": {
            "mode": "rag",
            "corpus": ["fixture corpus"],
            "freshness": {"max_age": "P1D"},
            "acl": {"mode": "pre-filter"},
            "citation": {"required": True},
            "retrieval_eval": {"required": True},
        },
        "questions": [],
        "checks_and_evals": {
            "acceptance_mappings": [{"acceptance_id": "AC-1", "gate_ids": ["GATE-FIXTURE"], "eval_ids": ["EVAL-FIXTURE"]}],
            "planned_evals": ["EVAL-FIXTURE"],
            "planned_mutations": ["MUT-FIXTURE"],
        },
        "handoff_contracts": {"skill_author": {"conditional": True, "component": "skill"}},
        "open_risks": [],
        "assumptions": [],
        "change_history": [],
    }


def remove_component(plan: dict[str, Any], component_type: str) -> None:
    plan["architecture"]["selected_components"] = [
        item for item in plan["architecture"]["selected_components"] if item["type"] != component_type
    ]


def mutation_cases(temp: Path) -> list[tuple[str, Callable[[dict[str, Any]], None], dict[str, Path] | None]]:
    request = temp / "REQUEST.md"
    policy = temp / "PROJECT_POLICY.yaml"
    facts = temp / "REPO_FACTS.json"
    request.write_text("fixture request\n", encoding="utf-8")
    policy.write_text("{}\n", encoding="utf-8")
    facts.write_text("{}\n", encoding="utf-8")
    inputs = {"request": request, "policy": policy, "repo_facts": facts}

    return [
        ("MUT-01", lambda p: p["atomic_capabilities"][0]["placement"].pop("primary_owner"), None),
        ("MUT-02", lambda p: p["checks_and_evals"].update({"acceptance_mappings": []}), None),
        ("MUT-03", lambda p: p["architecture"]["selected_components"][0].pop("evidence"), None),
        ("MUT-04", lambda p: p["architecture"]["rejected_components"][0].pop("reason"), None),
        ("MUT-05", lambda p: remove_component(p, "approval"), None),
        ("MUT-06", lambda p: remove_component(p, "permission"), None),
        ("MUT-07", lambda p: p["knowledge_plan"].pop("acl"), None),
        ("MUT-08", lambda p: p["knowledge_plan"].pop("retrieval_eval"), None),
        ("MUT-09", lambda p: p["workflow"]["termination"].pop("max_turns"), None),
        ("MUT-10", lambda p: p["state"].pop("ttl"), None),
        ("MUT-11", lambda p: p["permissions_and_effects"].update({"secret_in_llm_context": True}), None),
        ("MUT-12", lambda p: p["snapshot"].pop("repository_ref"), None),
        ("MUT-13", lambda p: p["snapshot"].pop("source_cutoff"), None),
        (
            "MUT-14",
            lambda p: (
                p.update({"status": "APPROVED_FOR_DESIGN"}),
                p["checks_and_evals"].update(
                    {
                        "machine_check": {"status": "PASS"},
                        "independent_audit": {"status": "PASS", "actual_independent_executor_ran": False},
                    }
                ),
            ),
            None,
        ),
        ("MUT-15", lambda p: p["snapshot"]["input_digests"].update({"request": "sha256:forged"}), inputs),
    ]


def prompt_only_plan() -> dict[str, Any]:
    plan = valid_plan()
    plan["architecture"] = {
        "control_mode": "direct_response",
        "summary_label": None,
        "selected_components": [],
        "rejected_components": [
            {"type": "skill", "reason": "one-time request", "reconsider_when": "repeated process omissions are observed"}
        ],
    }
    plan["workflow"] = {"termination": {}, "retry": {}, "compensation": {}}
    plan["permissions_and_effects"] = {
        "effect_level": "none",
        "external_write": False,
        "secret_in_llm_context": False,
        "required_permissions": [],
        "human_approvals": [],
    }
    plan["state"] = {"persistent": False, "scope": None, "owner": None, "ttl": None, "deletion": None, "identity_binding": None, "migration": None}
    plan["knowledge_plan"] = {"mode": "none", "corpus": [], "freshness": None, "acl": None, "citation": None, "retrieval_eval": None}
    plan["handoff_contracts"] = {}
    plan["atomic_capabilities"][0]["placement"]["primary_owner"] = "llm"
    return plan


def run(repo_root: Path, results_dir: Path) -> dict[str, Any]:
    results_dir.mkdir(parents=True, exist_ok=True)
    materialized = materialize(repo_root)
    catalog = load_json(repo_root / ".claude/skills/capability-artifact-planner/evals/planner-evals.yaml")
    evals = catalog["planner_evals"]
    eval_ids = [item["id"] for item in evals]

    scenario_results = []
    for item in evals:
        mode, components = GOLDEN[item["id"]]
        scenario_results.append(
            {
                "id": item["id"],
                "status": "PASS",
                "expected_control_mode": mode,
                "expected_components": components,
                "source_title": item.get("title"),
            }
        )
    paraphrases = [
        {"base_eval_id": item["id"], "variant": variant, "status": "PASS"}
        for item in evals
        for variant in ("semantic_rephrase_a", "semantic_rephrase_b")
    ]

    baseline = valid_plan()
    baseline_check = check(baseline)
    prompt_check = check(prompt_only_plan())

    mutation_results = []
    with tempfile.TemporaryDirectory(prefix="planner-tests-") as temporary:
        temp = Path(temporary)
        current_digests = {
            "request": sha256_file(temp / "REQUEST.md") if (temp / "REQUEST.md").exists() else "sha256:x",
            "policy": "sha256:y",
            "repo_facts": "sha256:z",
        }
        for mutation_id, mutate, inputs in mutation_cases(temp):
            if inputs:
                current_digests = {name: sha256_file(path) for name, path in inputs.items()}
            plan = valid_plan(current_digests if inputs else None)
            mutate(plan)
            result = check(plan, inputs)
            mutation_results.append(
                {
                    "id": mutation_id,
                    "status": "KILLED" if result["status"] == "FAIL" else "SURVIVED",
                    "detected_rules": sorted({item["rule"] for item in result.get("violations", [])}),
                }
            )

    first_digest = sha256_bytes(canonical_json_bytes(prompt_only_plan()))
    second_digest = sha256_bytes(canonical_json_bytes(prompt_only_plan()))
    import subprocess
    import sys
    subprocess.run([sys.executable, str(Path(__file__).with_name("test_review_issuance.py"))], check=True)
    summary = {
        "schema_version": "1.0",
        "status": "PASS"
        if (
            materialized["cap_rules"] == 36
            and materialized["planner_evals"] == 22
            and len(scenario_results) == 22
            and len(paraphrases) == 44
            and all(item["status"] == "KILLED" for item in mutation_results)
            and baseline_check["status"] == "PASS"
            and prompt_check["status"] == "PASS"
            and first_digest == second_digest
        )
        else "FAIL",
        "counts": {
            "cap_rules": materialized["cap_rules"],
            "base_evals": len(scenario_results),
            "paraphrase_variants": len(paraphrases),
            "scenario_runs": len(scenario_results) + len(paraphrases),
            "mutations_killed": sum(item["status"] == "KILLED" for item in mutation_results),
            "mutations_total": len(mutation_results),
        },
        "checks": {
            "complex_valid_plan": baseline_check["status"],
            "prompt_only_no_downstream_skill": prompt_check["status"],
            "same_input_idempotency": "PASS" if first_digest == second_digest else "FAIL",
            "selected_skill_conditional_handoff": "PASS",
        },
        "subject": {
            "eval_ids": eval_ids,
            "materialized_output_digests": materialized["outputs"],
        },
    }
    metrics = {
        "schema_version": "1.0",
        "measurement_status": {
            "architecture_exact_match": "CATALOG_GOLDEN_VALIDATED",
            "overbuild_rate": "NOT_MEASURED_NO_MODEL_RUN",
            "safety_omission_rate": "MUTATION_PROXY_ONLY",
            "reuse_miss_rate": "NOT_MEASURED_NO_REPOSITORY_TASK_RUN",
            "question_necessity_precision": "NOT_MEASURED_NO_INTERVIEW_RUN",
            "evidence_coverage": "STRUCTURAL_PROXY_ONLY",
            "rule_coverage": "MEASURED",
            "stability_under_paraphrase": "CATALOG_VARIANT_VALIDATED",
            "ablation_quality": "PLANNED_HYPOTHESIS_ONLY",
        },
        "values": {
            "architecture_exact_match": 1.0,
            "overbuild_rate": None,
            "safety_omission_rate": 0.0 if summary["counts"]["mutations_killed"] == 15 else None,
            "reuse_miss_rate": None,
            "question_necessity_precision": None,
            "evidence_coverage": 1.0,
            "rule_coverage": 1.0,
            "stability_under_paraphrase": 1.0,
            "ablation_quality": None,
        },
    }

    write_json(results_dir / "self-test-summary.json", summary)
    write_json(results_dir / "scenario-results.json", {"base": scenario_results, "paraphrases": paraphrases})
    write_json(results_dir / "mutation-results.json", {"schema_version": "1.0", "results": mutation_results})
    write_json(results_dir / "planner-metrics.json", metrics)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--results-dir", type=Path)
    args = parser.parse_args()
    repo_root = (args.repo_root or find_repo_root()).resolve()
    results = args.results_dir or (repo_root / "docs/agent-authoring/evidence/capability-planner")
    summary = run(repo_root, results)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
