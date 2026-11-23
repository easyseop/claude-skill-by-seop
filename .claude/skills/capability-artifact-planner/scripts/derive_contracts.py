#!/usr/bin/env python3
"""Derive downstream handoff contracts without implementing downstream artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import PlannerError, canonical_json_bytes, load_json, sha256_bytes, write_json
from check_capability_plan import check


def component_types(plan: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for item in plan.get("architecture", {}).get("selected_components", []):
        result.add(item if isinstance(item, str) else str(item.get("type", "")))
    return result


def derive(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    validation = check(plan)
    if validation["status"] != "PASS":
        raise PlannerError("cannot derive contracts from an invalid plan")

    plan_digest = sha256_bytes(canonical_json_bytes(plan))
    components = component_types(plan)
    capabilities = plan.get("atomic_capabilities", [])
    acceptance = plan.get("checks_and_evals", {}).get("acceptance_mappings", [])
    common = {
        "schema_version": "1.0",
        "upstream_plan_id": plan.get("plan_id"),
        "upstream_plan_digest": plan_digest,
        "control_mode": plan.get("architecture", {}).get("control_mode"),
        "capability_ids": [item.get("id") for item in capabilities],
        "acceptance_mappings": acceptance,
        "operational_permission": False,
    }

    contracts: dict[str, dict[str, Any]] = {}
    contracts["GATE_CONTRACT.yaml"] = {
        **common,
        "required": bool(components.intersection({"validator", "approval", "permission", "hook", "sandbox", "eval", "tracing"})),
        "effect_contract": plan.get("permissions_and_effects", {}),
        "state_contract": plan.get("state", {}),
        "status": "PLANNED",
    }
    contracts["EXECUTION_CONTRACT.yaml"] = {
        **common,
        "required": bool(components.intersection({"script", "validator", "tool", "workflow"})),
        "selected_components": sorted(components.intersection({"script", "validator", "tool", "workflow"})),
        "workflow": plan.get("workflow", {}),
        "status": "PLANNED",
    }
    contracts["KNOWLEDGE_CONTRACT.yaml"] = {
        **common,
        "required": bool(components.intersection({"reference", "rag"})) or plan.get("knowledge_plan", {}).get("mode") not in {None, "none"},
        "selected_components": sorted(components.intersection({"reference", "rag"})),
        "knowledge_plan": plan.get("knowledge_plan", {}),
        "status": "PLANNED",
    }
    contracts["ASSEMBLY_CONTRACT.yaml"] = {
        **common,
        "required": True,
        "selected_components": sorted(components),
        "skill_author_handoff": plan.get("handoff_contracts", {}).get("skill_author"),
        "status": "PLANNED",
    }
    return contracts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        plan = load_json(args.plan)
        contracts = derive(plan)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, value in contracts.items():
            write_json(args.output_dir / name, value)
        print(json.dumps({"status": "PASS", "contracts": sorted(contracts)}, ensure_ascii=False))
        return 0
    except PlannerError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
