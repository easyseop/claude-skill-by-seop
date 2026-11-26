#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from derive_execution_contract import INVARIANTS, read_inputs
from execution_engine import check_contract, read_json, sha256_value, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--planner", type=Path, required=True)
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        contract = read_json(args.contract)
        planner, plan_digest, gate_digest = read_inputs(args.planner, args.gate)
        failures = {}
        if contract.get("planner_binding") != planner:
            failures["EXI-003"] = "Planner identity or architecture mismatch"
        if contract.get("snapshot", {}).get("gate_digest") != gate_digest:
            failures["EXI-002"] = "Gate digest stale"
        if contract.get("contract_digest") != sha256_value({k: v for k, v in contract.items() if k != "contract_digest"}):
            failures["EXI-001"] = "Execution contract digest mismatch"
        result = check_contract(contract, INVARIANTS, planner_digest=plan_digest, binding_failures=failures)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        result = {"status": "FAIL", "failures": {"EXI-002": str(exc)}}
    if args.output:
        write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
