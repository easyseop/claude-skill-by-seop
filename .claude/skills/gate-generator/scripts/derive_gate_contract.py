#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

from gate_engine import sha256_value, valid_contract, write_json
from gate_validation import comprehensive_check

INVARIANTS = [f"I-{n:03d}" for n in range(1, 86)]


def load_plan(path):
    data = path.read_bytes()
    plan = json.loads(data)
    for key in ("plan_id", "status"):
        if not isinstance(plan.get(key), str) or not plan[key].strip():
            raise ValueError(f"Missing Planner {key}")
    return plan, "sha256:" + hashlib.sha256(data).hexdigest()


def binding(plan, digest):
    return {"capability_plan_id": plan["plan_id"], "capability_plan_status": plan["status"],
            "capability_plan_digest": digest}


def check_current(contract, plan, digest):
    failures = {}
    if contract.get("upstream_binding") != binding(plan, digest):
        failures["I-005"] = "Planner identity, status or digest differs from current input"
    if contract.get("contract_digest") != sha256_value({k: v for k, v in contract.items() if k != "contract_digest"}):
        failures["I-005"] = "Gate contract digest mismatch"
    return comprehensive_check(contract, INVARIANTS, failures)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("capability_plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan, digest = load_plan(args.capability_plan)
    contract = valid_contract(INVARIANTS)
    contract["upstream_binding"] = binding(plan, digest)
    contract["snapshot"]["upstream_digest"] = digest
    contract.pop("contract_digest")
    contract["contract_digest"] = sha256_value(contract)
    write_json(args.output, contract)


if __name__ == "__main__":
    main()
