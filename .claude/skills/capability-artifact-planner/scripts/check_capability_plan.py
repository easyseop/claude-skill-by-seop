#!/usr/bin/env python3
"""Deterministic validation for CAPABILITY_PLAN canonical JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import PlannerError, load_json, sha256_file, write_json


CONTROL_MODES = {"direct_response", "deterministic_workflow", "bounded_agent", "multi_agent"}
OWNERS = {"llm", "code", "knowledge", "tool", "agent", "human"}
COMPONENTS = {
    "skill",
    "reference",
    "script",
    "validator",
    "tool",
    "rag",
    "workflow",
    "agent",
    "approval",
    "permission",
    "hook",
    "sandbox",
    "state",
    "eval",
    "tracing",
}
HIGH_EFFECTS = {"high", "critical"}


def violation(rule: str, path: str, message: str, remediation: str, blocking: bool = True) -> dict[str, Any]:
    return {
        "rule": rule,
        "path": path,
        "message": message,
        "blocking": blocking,
        "remediation": remediation,
    }


def selected_component_map(plan: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    selected = plan.get("architecture", {}).get("selected_components", [])
    for item in selected if isinstance(selected, list) else []:
        if isinstance(item, str):
            item = {"type": item}
        if not isinstance(item, dict):
            continue
        result.setdefault(str(item.get("type", "")), []).append(item)
    return result


def check(plan: dict[str, Any], current_inputs: dict[str, Path] | None = None) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for key in (
        "schema_version",
        "plan_id",
        "status",
        "snapshot",
        "request",
        "atomic_capabilities",
        "architecture",
        "permissions_and_effects",
        "state",
        "knowledge_plan",
        "checks_and_evals",
        "handoff_contracts",
    ):
        if key not in plan:
            errors.append(violation("SCHEMA", key, "required top-level field is missing", f"add `{key}`"))

    snapshot = plan.get("snapshot", {})
    for key in ("planner_version", "repository_ref", "source_cutoff", "input_digests"):
        if not snapshot.get(key):
            errors.append(violation("CAP-36", f"snapshot.{key}", "snapshot binding is missing", "record current value and digest"))

    if current_inputs:
        expected = snapshot.get("input_digests", {})
        for name, path in current_inputs.items():
            current = sha256_file(path)
            if expected.get(name) != current:
                errors.append(
                    violation(
                        "CAP-36",
                        f"snapshot.input_digests.{name}",
                        f"input is stale: expected={expected.get(name)} current={current}",
                        "regenerate the plan from current inputs",
                    )
                )

    capabilities = plan.get("atomic_capabilities", [])
    if not isinstance(capabilities, list):
        errors.append(violation("CAP-02", "atomic_capabilities", "must be a list", "use a list of atomic capability objects"))
        capabilities = []
    ids: list[str] = []
    acceptance_ids: set[str] = set()
    for index, cap in enumerate(capabilities):
        path = f"atomic_capabilities[{index}]"
        if not isinstance(cap, dict):
            errors.append(violation("CAP-02", path, "capability must be an object", "replace with a structured object"))
            continue
        cap_id = str(cap.get("id", ""))
        if not cap_id:
            errors.append(violation("CAP-02", f"{path}.id", "capability id is required", "assign a stable id"))
        elif cap_id in ids:
            errors.append(violation("CAP-02", f"{path}.id", f"duplicate capability id {cap_id}", "use unique stable ids"))
        ids.append(cap_id)
        for field in ("name", "purpose", "inputs", "outputs", "failure_modes", "recovery"):
            if field not in cap or cap.get(field) in (None, "", []):
                errors.append(violation("CAP-02", f"{path}.{field}", "atomic capability field is empty", "describe the field explicitly"))
        placement = cap.get("placement", {})
        owner = placement.get("primary_owner") if isinstance(placement, dict) else None
        if owner not in OWNERS:
            errors.append(
                violation(
                    "CAP-02",
                    f"{path}.placement.primary_owner",
                    f"exactly one valid primary owner is required; got {owner!r}",
                    f"choose one of {sorted(OWNERS)}",
                )
            )
        acs = cap.get("acceptance_criteria", [])
        if not isinstance(acs, list) or not acs:
            errors.append(violation("CAP-02", f"{path}.acceptance_criteria", "at least one criterion is required", "add objective criteria"))
        else:
            for ac in acs:
                ac_id = ac.get("id") if isinstance(ac, dict) else ac
                if ac_id:
                    acceptance_ids.add(str(ac_id))

    mode = plan.get("architecture", {}).get("control_mode")
    if mode not in CONTROL_MODES:
        errors.append(violation("CAP-04", "architecture.control_mode", f"invalid control mode: {mode!r}", f"choose one of {sorted(CONTROL_MODES)}"))

    components = selected_component_map(plan)
    selected = plan.get("architecture", {}).get("selected_components", [])
    for index, raw in enumerate(selected if isinstance(selected, list) else []):
        item = {"type": raw} if isinstance(raw, str) else raw
        path = f"architecture.selected_components[{index}]"
        if not isinstance(item, dict) or item.get("type") not in COMPONENTS:
            errors.append(violation("CAP-01", f"{path}.type", "unknown component type", f"choose one of {sorted(COMPONENTS)}"))
            continue
        for key in ("capability_ids", "evidence", "owner", "necessity_test"):
            if not item.get(key):
                errors.append(violation("CAP-01", f"{path}.{key}", "selected component lacks necessity evidence", "record capability use, owner, evidence, and necessity hypothesis"))
        necessity = item.get("necessity_test", {})
        if isinstance(necessity, dict) and not necessity.get("planned_hypothesis"):
            errors.append(violation("CAP-01", f"{path}.necessity_test.planned_hypothesis", "planned ablation hypothesis is missing", "state what fails without the component"))

    rejected = plan.get("architecture", {}).get("rejected_components", [])
    for index, item in enumerate(rejected if isinstance(rejected, list) else []):
        path = f"architecture.rejected_components[{index}]"
        if not isinstance(item, dict) or not item.get("type"):
            errors.append(violation("CAP-01", path, "rejected component type is missing", "record rejected type"))
            continue
        if not item.get("reason") or not item.get("reconsider_when"):
            errors.append(violation("CAP-01", path, "rejected component needs reason and reconsider condition", "add both fields"))

    mappings = plan.get("checks_and_evals", {}).get("acceptance_mappings", [])
    mapped: set[str] = set()
    for mapping in mappings if isinstance(mappings, list) else []:
        if isinstance(mapping, dict) and mapping.get("acceptance_id"):
            if mapping.get("gate_ids") or mapping.get("eval_ids"):
                mapped.add(str(mapping["acceptance_id"]))
    missing_ac = sorted(acceptance_ids - mapped)
    if missing_ac:
        errors.append(violation("CAP-29", "checks_and_evals.acceptance_mappings", f"unmapped acceptance criteria: {missing_ac}", "map every criterion to a Gate or Eval"))

    workflow = plan.get("workflow", {})
    if mode in {"bounded_agent", "multi_agent"}:
        termination = workflow.get("termination", {})
        for key in ("max_turns", "max_tool_calls", "max_time_seconds", "completion_condition", "error_stop_condition", "human_handoff_condition"):
            if not termination.get(key):
                errors.append(violation("CAP-24", f"workflow.termination.{key}", "bounded agent termination field is missing", "set an explicit finite value or condition"))
        if "tracing" not in components:
            errors.append(violation("CAP-28", "architecture.selected_components", "Agent mode requires tracing", "select tracing and bind evidence"))
    if mode == "multi_agent":
        evidence = plan.get("architecture", {}).get("multi_agent_evidence", [])
        allowed = {"context_isolation", "independent_parallelism", "authority_separation", "proven_specialization", "single_agent_eval_failure"}
        if not isinstance(evidence, list) or not allowed.intersection(evidence):
            errors.append(violation("CAP-20", "architecture.multi_agent_evidence", "multi-agent lacks allowed separation evidence", f"provide one of {sorted(allowed)}"))

    effects = plan.get("permissions_and_effects", {})
    effect_level = effects.get("effect_level", "none")
    external_write = bool(effects.get("external_write"))
    if effects.get("secret_in_llm_context") is not False:
        errors.append(violation("CAP-35", "permissions_and_effects.secret_in_llm_context", "secret may not enter LLM context", "set false and define out-of-band secret flow"))
    if external_write:
        for required in ("tool", "permission", "tracing"):
            if required not in components:
                errors.append(violation("CAP-17", "architecture.selected_components", f"external write requires {required}", f"select and bind {required}"))
        if effect_level in HIGH_EFFECTS and "approval" not in components:
            errors.append(violation("CAP-18", "architecture.selected_components", "high/critical write requires human approval", "add exact-payload approval"))
        if effects.get("irreversible"):
            dry_run = effects.get("dry_run")
            no_dry_run_reason = effects.get("dry_run_unavailable_reason")
            if not dry_run and not no_dry_run_reason:
                errors.append(violation("CAP-32", "permissions_and_effects.dry_run", "irreversible write requires dry-run or reason", "add dry-run or explicit impossibility reason"))
            if not effects.get("idempotency") and not effects.get("compensation"):
                errors.append(violation("CAP-25", "permissions_and_effects", "irreversible write lacks idempotency or compensation", "define recovery semantics"))

    knowledge = plan.get("knowledge_plan", {})
    if "rag" in components or knowledge.get("mode") == "rag":
        for key in ("corpus", "freshness", "acl", "citation", "retrieval_eval"):
            if not knowledge.get(key):
                errors.append(violation("CAP-27", f"knowledge_plan.{key}", "RAG field is required", "define current corpus and enforcement/eval contract"))

    state = plan.get("state", {})
    if state.get("persistent") or "state" in components:
        for key in ("scope", "owner", "ttl", "deletion", "identity_binding", "migration"):
            if not state.get(key):
                errors.append(violation("CAP-31", f"state.{key}", "persistent state contract is incomplete", "define lifecycle and identity semantics"))

    handoff = plan.get("handoff_contracts", {})
    skill_selected = "skill" in components
    author_handoff = handoff.get("skill_author") if isinstance(handoff, dict) else None
    if skill_selected and not author_handoff:
        errors.append(violation("CAP-07", "handoff_contracts.skill_author", "selected Skill lacks conditional author handoff", "add handoff without executing it in Planner"))
    if not skill_selected and author_handoff:
        errors.append(violation("CAP-06", "handoff_contracts.skill_author", "Prompt/no-skill plan must not call Skill Author", "remove the handoff"))

    status = str(plan.get("status", "DRAFT"))
    if status in {"APPROVED", "APPROVED_FOR_DESIGN"}:
        machine = plan.get("checks_and_evals", {}).get("machine_check", {})
        audit = plan.get("checks_and_evals", {}).get("independent_audit", {})
        if machine.get("status") != "PASS":
            errors.append(violation("CAP-33", "checks_and_evals.machine_check.status", "approved plan lacks current machine PASS", "run checker and bind current subject"))
        if audit.get("status") != "PASS" or audit.get("actual_independent_executor_ran") is not True:
            errors.append(violation("CAP-33", "checks_and_evals.independent_audit", "approved plan lacks actual independent audit", "run a distinct read-only auditor or lower status"))

    for item in selected if isinstance(selected, list) else []:
        if isinstance(item, dict):
            for cap_id in item.get("capability_ids", []):
                if cap_id not in ids:
                    errors.append(violation("CAP-02", "architecture.selected_components.capability_ids", f"unknown capability reference {cap_id}", "reference an existing capability"))

    target = errors if errors else warnings
    if not capabilities:
        target.append(violation("CAP-02", "atomic_capabilities", "plan has no capabilities", "decompose the request", blocking=not bool(errors)))

    return {
        "schema_version": "1.0",
        "status": "FAIL" if errors else "PASS",
        "summary": {
            "blocking_violations": len(errors),
            "warnings": len(warnings),
            "capabilities": len(capabilities),
            "acceptance_criteria": len(acceptance_ids),
            "selected_component_types": sorted(components),
        },
        "violations": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--repo-facts", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        plan = load_json(args.plan)
        inputs = None
        if args.request or args.policy or args.repo_facts:
            if not all((args.request, args.policy, args.repo_facts)):
                raise PlannerError("--request, --policy, and --repo-facts must be supplied together")
            inputs = {"request": args.request, "policy": args.policy, "repo_facts": args.repo_facts}
        result = check(plan, inputs)
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "PASS" else 2
    except PlannerError as exc:
        result = {"schema_version": "1.0", "status": "ERROR", "error": str(exc)}
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
