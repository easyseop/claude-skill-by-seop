#!/usr/bin/env python3
"""Decide whether a plan may be handed to downstream design stages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import load_json, write_json


def decide(machine: dict, audit: dict, contracts: list[Path]) -> dict:
    missing_contracts = [path.as_posix() for path in contracts if not path.is_file()]
    machine_pass = machine.get("status") == "PASS"
    procedural_pass = audit.get("status") == "PASS_LOCAL_PROCEDURE"
    current_subject = machine.get("subject_digest") or audit.get("subject_digest")
    audit_subject = audit.get("subject_digest")
    subject_current = not current_subject or current_subject == audit_subject

    if not machine_pass:
        status = "BLOCKED"
        reason = "MACHINE_CHECK_FAILED"
    elif not procedural_pass:
        status = "BLOCKED"
        reason = "PROCEDURAL_AUDIT_FAILED"
    elif not subject_current:
        status = "STALE"
        reason = "SUBJECT_DIGEST_MISMATCH"
    elif missing_contracts:
        status = "BLOCKED"
        reason = "DOWNSTREAM_CONTRACT_MISSING"
    else:
        status = "PASS_LOCAL_PROCEDURE"
        reason = "INDEPENDENT_AUDIT_UNVERIFIED"

    return {
        "schema_version": "1.0",
        "status": status,
        "reason": reason,
        "scope": "capability_plan_and_downstream_contract_design",
        "operational_permission": False,
        "machine_check": machine_pass,
        "procedural_audit": procedural_pass,
        "independent_audit": False,
        "missing_contracts": missing_contracts,
        "permits": ["gate_design", "execution_design", "knowledge_design", "assembly_design"] if status in {"PASS_LOCAL_PROCEDURE", "APPROVED_FOR_DESIGN"} else [],
        "forbids": ["production_write", "deployment", "secret_collection", "automatic_merge"],
    }


def main() -> int:
    if sys.argv[1:2] == ["issue"]:
        from issue_reviewed_plan import main as issue_main
        return issue_main(sys.argv[2:])
    parser = argparse.ArgumentParser()
    parser.add_argument("--machine-check", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--contract", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = decide(load_json(args.machine_check), load_json(args.audit), args.contract)
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] in {"PASS_LOCAL_PROCEDURE", "APPROVED_FOR_DESIGN"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
