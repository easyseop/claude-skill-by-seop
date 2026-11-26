#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

from execution_engine import sha256_value, valid_contract, write_json

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "gate-generator" / "scripts"))
from derive_gate_contract import check_current, load_plan

INVARIANTS = [f"EXI-{n:03d}" for n in range(1, 46)]


def read_inputs(planner_path, gate_path):
    plan, plan_digest = load_plan(planner_path)
    data = gate_path.read_bytes()
    gate = json.loads(data)
    checked = check_current(gate, plan, plan_digest)
    if checked["status"] != "PASS":
        raise ValueError(f"Invalid upstream Gate: {checked['failures']}")
    architecture = plan["architecture"]
    mode = architecture["control_mode"]
    components = [item["type"] for item in architecture["selected_components"]]
    if mode not in {"direct_response", "deterministic_workflow", "bounded_agent", "multi_agent"} or not all(isinstance(c, str) and c for c in components):
        raise ValueError("Invalid Planner architecture")
    planner = {"plan_id": plan["plan_id"], "control_mode": mode, "current_control_mode": mode,
               "selected_components": components, "current_selected_components": components,
               "reentry_required": False}
    return planner, plan_digest, "sha256:" + hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("planner", type=Path)
    parser.add_argument("gate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        planner, plan_digest, gate_digest = read_inputs(args.planner, args.gate)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"{exc}\n")
    contract = valid_contract(INVARIANTS)
    contract["planner_binding"] = planner
    contract["snapshot"].update(planner_digest=plan_digest, gate_digest=gate_digest)
    contract.pop("contract_digest")
    contract["contract_digest"] = sha256_value(contract)
    write_json(args.output, contract)


if __name__ == "__main__":
    main()
