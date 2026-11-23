#!/usr/bin/env python3
"""Supplemental semantic validation for Gate contracts."""

from __future__ import annotations

from typing import Any

from gate_engine import check_contract


def comprehensive_check(contract: dict[str, Any], invariant_ids: list[str]) -> dict[str, Any]:
    result = check_contract(contract, invariant_ids)
    failures = dict(result.get("failures", {}))
    pretool = contract.get("hooks", {}).get("pretool", {})
    stop = contract.get("hooks", {}).get("stop", {})
    if pretool.get("timeout_behavior") != "block":
        failures.setdefault("I-022", "high-risk PreToolUse timeout must block")
        failures.setdefault("I-067", "high-risk timeout is not fail-closed")
    if pretool.get("malformed_behavior") != "block":
        failures.setdefault("I-022", "malformed PreToolUse result must block")
        failures.setdefault("I-067", "malformed high-risk hook is not fail-closed")
    if stop.get("timeout_behavior") != "block" or stop.get("malformed_behavior") != "block":
        failures.setdefault("I-022", "Stop hook timeout/malformed behavior must block")
    if contract.get("status") == "APPROVED" and not contract.get("audit", {}).get("actual_independent_executor_ran"):
        failures.setdefault("I-085", "approved status requires actual independent audit")
    results = [
        {"id": invariant_id, "status": "FAIL" if invariant_id in failures else "PASS", "message": failures.get(invariant_id)}
        for invariant_id in invariant_ids
    ]
    result["failures"] = failures
    result["results"] = results
    result["status"] = "FAIL" if failures else "PASS"
    result["counts"] = {
        "invariants": len(invariant_ids),
        "passed": len(invariant_ids) - len(failures),
        "failed": len(failures),
    }
    return result
