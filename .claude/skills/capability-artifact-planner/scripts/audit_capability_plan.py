#!/usr/bin/env python3
"""Create a read-only procedural audit record for a capability plan.

This script never claims an independent identity. A separate session may replace the
procedural result with an attested independent audit bound to the same subject digest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import canonical_json_bytes, load_json, sha256_bytes, write_json
from check_capability_plan import check


def audit(plan: dict[str, Any]) -> dict[str, Any]:
    machine = check(plan)
    capabilities = plan.get("atomic_capabilities", [])
    selected = plan.get("architecture", {}).get("selected_components", [])
    capability_ids = [item.get("id") for item in capabilities if isinstance(item, dict)]
    selected_types = sorted(
        item if isinstance(item, str) else str(item.get("type", ""))
        for item in selected
    )
    findings: list[dict[str, Any]] = []
    if machine["status"] != "PASS":
        findings.append(
            {
                "severity": "blocking",
                "code": "MACHINE_CHECK_FAILED",
                "message": "procedural audit cannot pass while deterministic validation fails",
                "related_rules": sorted({item["rule"] for item in machine.get("violations", [])}),
            }
        )
    if not capability_ids:
        findings.append(
            {
                "severity": "blocking",
                "code": "NO_CAPABILITIES",
                "message": "request has not been decomposed into atomic capabilities",
            }
        )
    if selected_types and not plan.get("architecture", {}).get("rejected_components"):
        findings.append(
            {
                "severity": "non_blocking",
                "code": "NO_REJECTED_ALTERNATIVES",
                "message": "selected architecture has no documented rejected alternatives",
            }
        )

    subject_digest = sha256_bytes(canonical_json_bytes(plan))
    blocking = sum(1 for item in findings if item["severity"] == "blocking")
    return {
        "schema_version": "1.0",
        "audit_type": "procedural_blind_first_candidate",
        "subject_digest": subject_digest,
        "status": "PASS_LOCAL_PROCEDURE" if blocking == 0 else "FAIL",
        "blocking_disagreements": blocking,
        "findings": findings,
        "independence": {
            "actual_independent_executor_ran": False,
            "independence_status": "UNVERIFIED",
            "attestation": False,
            "note": "A distinct read-only session must audit request/repo/policy before reading planner rationale.",
        },
        "observed": {
            "capability_ids": capability_ids,
            "selected_component_types": selected_types,
            "control_mode": plan.get("architecture", {}).get("control_mode"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = load_json(args.plan)
    result = audit(plan)
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "PASS_LOCAL_PROCEDURE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
