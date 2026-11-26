#!/usr/bin/env python3
"""Deterministic core for the Gate Generator M0-M3 local candidate."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

STATUSES = {
    "PASS", "BLOCK", "FAIL", "ERROR", "STALE", "WAIVED",
    "NOT_APPLICABLE", "OUTCOME_UNKNOWN", "PLANNER_REENTRY_REQUIRED",
    "HARD_ENFORCEMENT_UNAVAILABLE",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def catalog_ids(items: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("id", "")) for item in items]


def continuous_ids(ids: list[str], prefix: str, start: int, end: int, width: int = 2) -> bool:
    expected = [f"{prefix}{number:0{width}d}" for number in range(start, end + 1)]
    return ids == expected


def valid_contract(invariant_ids: list[str]) -> dict[str, Any]:
    gates = [
        {
            "id": "G-IN-001",
            "stage": "intake",
            "blocking": True,
            "requirement_ids": ["REQ-1"],
            "risk_ids": ["RISK-1"],
            "enforcement": {"layer": "validator", "path": "scripts/gate_engine.py", "digest": "sha256:engine"},
            "test_ids": ["GEVAL-001"],
            "mutation_ids": ["GMUT-004"],
            "evidence_refs": ["evidence://baseline-check"],
        },
        {
            "id": "G-PRE-001",
            "stage": "pre_execution",
            "blocking": True,
            "requirement_ids": ["REQ-2"],
            "risk_ids": ["RISK-2"],
            "enforcement": {"layer": "hook", "path": "adapters/claude-code/pretool_gate.py", "digest": "sha256:pretool"},
            "test_ids": ["GEVAL-005", "GEVAL-014"],
            "mutation_ids": ["GMUT-007", "GMUT-009"],
            "evidence_refs": ["evidence://hook-smoke"],
        },
        {
            "id": "G-POST-001",
            "stage": "post_execution",
            "blocking": True,
            "requirement_ids": ["REQ-2"],
            "risk_ids": ["RISK-2"],
            "enforcement": {"layer": "reconciliation", "path": "adapters/claude-code/posttool_gate.py", "digest": "sha256:posttool"},
            "test_ids": ["GEVAL-027", "GEVAL-038"],
            "mutation_ids": ["GMUT-016"],
            "evidence_refs": ["evidence://reconciliation"],
        },
        {
            "id": "G-STOP-001",
            "stage": "completion",
            "blocking": True,
            "requirement_ids": ["REQ-3"],
            "risk_ids": ["RISK-3"],
            "enforcement": {"layer": "stop_gate", "path": "adapters/claude-code/stop_gate.py", "digest": "sha256:stop"},
            "test_ids": ["GEVAL-040", "GEVAL-041"],
            "mutation_ids": ["GMUT-002", "GMUT-017"],
            "evidence_refs": ["evidence://stop-gate"],
        },
    ]
    contract = {
        "schema_version": "1.0",
        "contract_id": "GATE-CONTRACT-FIXTURE",
        "status": "CHECKED_LOCAL",
        "snapshot": {
            "upstream_digest": "sha256:planner",
            "policy_digest": "sha256:policy",
            "checker_digest": "sha256:checker",
            "input_snapshot_digest": "sha256:input",
            "issued_at": "2026-11-23T00:00:00Z",
            "expires_at": "2099-01-01T00:00:00Z",
        },
        "upstream_binding": {
            "capability_plan_id": "PLAN-1",
            "capability_plan_status": "APPROVED_FOR_DESIGN",
            "capability_plan_digest": "sha256:planner",
        },
        "acceptance_criteria": [
            {"id": "AC-1", "gate_ids": ["G-IN-001"], "eval_ids": ["GEVAL-001"]},
            {"id": "AC-2", "gate_ids": ["G-PRE-001", "G-POST-001"], "eval_ids": ["GEVAL-014"]},
            {"id": "AC-3", "gate_ids": ["G-STOP-001"], "eval_ids": ["GEVAL-041"]},
        ],
        "gates": gates,
        "effects": {
            "external_write": True,
            "effect_level": "high",
            "irreversible": True,
            "pre_gate_ids": ["G-PRE-001"],
            "post_gate_ids": ["G-POST-001"],
            "recovery_gate_ids": ["G-POST-001"],
            "risk_acceptance": "human-reviewed",
            "manual_repair": "run reconciliation and escalate",
        },
        "permissions": {"default": "deny", "wildcard": False, "audit": True},
        "approval": {
            "required": True,
            "canonicalization": "JCS",
            "digest_algorithm": "SHA-256",
            "bind_fields": ["action", "tool", "resource", "tenant", "principal", "payload", "policy"],
            "expiry_seconds": 900,
            "nonce_required": True,
            "single_use": True,
            "revocation_check": True,
            "quorum": 2,
            "distinct_principals": True,
            "prevent_self_review": True,
            "batch_binding": {"item_set": True, "count": True, "limits": True},
            "jit_revoke": True,
        },
        "secrets": {"through_llm_context": False, "flow": "out_of_band"},
        "path_policy": {"canonicalize": True, "symlink_check": True, "redirect_check": True, "root": "/repo"},
        "sandbox": {
            "required": True,
            "filesystem": "repo-only",
            "network": "deny",
            "process": "isolated",
            "resources": {"cpu": 1, "memory_mb": 512, "timeout_seconds": 30},
            "secret_injection": "none",
            "unsandboxed_fallback": False,
        },
        "tools": [
            {"id": "repo.read", "namespace": "repo", "version": "1", "server": "local", "effect": "read", "schema_digest": "sha256:read-schema", "unknown_fields": "reject"},
            {"id": "repo.write", "namespace": "repo", "version": "1", "server": "local", "effect": "write", "schema_digest": "sha256:write-schema", "unknown_fields": "reject"},
        ],
        "hooks": {
            "pretool": {"event": "PreToolUse", "timing": "before", "blocking": True, "timeout_behavior": "block", "malformed_behavior": "block", "fail_policy": "closed", "async_only": False},
            "posttool": {"event": "PostToolUse", "timing": "after", "blocking": False, "timeout_behavior": "unknown", "malformed_behavior": "unknown", "fail_policy": "reconcile", "async_only": False},
            "stop": {"event": "Stop", "timing": "completion", "blocking": True, "timeout_behavior": "block", "malformed_behavior": "block", "fail_policy": "closed", "async_only": False},
        },
        "agent": {
            "enabled": True,
            "limits": {"max_turns": 12, "max_tool_calls": 20, "max_time_seconds": 300},
            "termination": "all required gates current",
            "trace": True,
            "loop_detection": True,
        },
        "state": {"persistent": True, "owner": "workflow", "identity": "principal+tenant", "ttl_seconds": 3600, "delete": True, "migration": True, "checkpoint_revalidation": ["policy", "approval", "resource", "tool_version"]},
        "runtime": {
            "tool_pairing": True,
            "parallel": {"base_digest": True, "merge_policy": "deterministic", "conflict_policy": "block"},
            "background": {"lease": True, "fencing": True, "cancel": True, "late_result": "reject"},
            "partial_completion": ["completed", "failed", "unknown", "compensated"],
            "terminal_requires_no_pending": True,
        },
        "retry": {
            "allowed_error_classes": ["rate_limit", "transient_read"],
            "max_attempts": 3,
            "max_elapsed_seconds": 30,
            "backoff": "exponential",
            "outcome_unknown_auto_retry": False,
            "conflict_policy": "refetch_replan",
        },
        "idempotency": {"required": True, "same_key_same_payload_digest": True, "non_idempotent_policy": "blocked"},
        "compensation": {"required": True, "handler": "registered", "order": "reverse", "idempotent": True, "manual_fallback": True},
        "reconciliation": {"source_of_truth": "target-system", "expected_fields": ["count", "digest"], "actual_fields": ["count", "digest"], "mismatch_status": "OUTCOME_UNKNOWN"},
        "rag": {
            "enabled": True,
            "inventory": True,
            "source_freshness": True,
            "index_freshness": True,
            "acl": {"source": "authenticated_context", "cache_scope_includes_auth": True},
            "citation": True,
            "abstention": ["NO_EVIDENCE", "CONFLICT"],
            "deletion_propagation": True,
            "chunk_metadata": ["source_digest", "version", "span", "acl", "pipeline_version"],
            "retrieval_eval": True,
            "generation_eval": True,
            "retrieved_instruction_authority": False,
        },
        "result_contract": {
            "allow_free_text_pass": False,
            "required_bindings": ["subject", "policy", "checker", "input", "trace", "time", "evidence", "issuer"],
            "allowed_statuses": sorted(STATUSES),
            "error_to_pass": False,
            "required_test_skip_success": False,
        },
        "attestation": {
            "required_for_high_risk": True,
            "subject_digest": "sha256:artifact",
            "current_artifact_digest": "sha256:artifact",
            "issuer": "trusted-ci",
            "issuer_allowlist": ["trusted-ci"],
            "predicate_type": "test-result",
            "evidence": ["evidence://tests"],
        },
        "waivers": [],
        "phase_manifest": {"digest": "sha256:phase", "stale_propagation": True},
        "implementation_inventory": [
            {"gate_id": gate["id"], "path": gate["enforcement"]["path"], "digest": gate["enforcement"]["digest"], "annotation": True}
            for gate in gates
        ],
        "tests": {
            "required_job_skip_success": False,
            "negative_mutations": True,
            "normal_error_bypass_coverage": True,
        },
        "release": {
            "protected_branch": True,
            "protected_environment": True,
            "trusted_issuer": True,
            "prevent_self_review": True,
            "rehash_before_release": True,
            "manifest": {"artifact_digest": "sha256:artifact", "gate_result_digests": ["sha256:gate-result"]},
        },
        "audit": {
            "generator_identity": "generator",
            "auditor_identity": "unverified-separate-required",
            "blind_first": True,
            "actual_independent_executor_ran": False,
            "append_only_redacted_evidence": True,
        },
        "remote_gate": {"timeout_policy": "closed", "activation_policy": "atomic", "last_known_good": True, "ttl_seconds": 300},
        "trace": {"context_is_not_authorization": True},
        "invariant_assertions": {identifier: True for identifier in invariant_ids},
    }
    contract["contract_digest"] = sha256_value({key: value for key, value in contract.items() if key != "contract_digest"})
    return contract


def _fail(failures: dict[str, str], invariant_id: str, message: str) -> None:
    failures.setdefault(invariant_id, message)


def check_contract(contract: dict[str, Any], invariant_ids: list[str]) -> dict[str, Any]:
    failures: dict[str, str] = {}
    required = ["schema_version", "contract_id", "status", "snapshot", "upstream_binding"]
    if any(not contract.get(key) for key in required):
        _fail(failures, "I-001", "required contract header missing")
    if contract.get("status") not in {"DRAFT", "CHECKED_LOCAL", "APPROVED", "BLOCKED", "STALE"}:
        _fail(failures, "I-002", "invalid contract status")
    gates = contract.get("gates", [])
    gate_ids = [gate.get("id") for gate in gates if isinstance(gate, dict)]
    if len(gate_ids) != len(set(gate_ids)) or any(not item for item in gate_ids):
        _fail(failures, "I-003", "gate IDs are missing or duplicated")
    snapshot = contract.get("snapshot", {})
    upstream = contract.get("upstream_binding", {})
    if not snapshot.get("upstream_digest") or snapshot.get("upstream_digest") != upstream.get("capability_plan_digest"):
        _fail(failures, "I-005", "upstream digest binding missing or mismatched")
    if upstream.get("capability_plan_status") not in {"APPROVED_FOR_DESIGN", "VERIFIED_LOCAL_CANDIDATE"}:
        _fail(failures, "I-006", "Planner status is not derivation-eligible")
    gate_set = set(gate_ids)
    for criterion in contract.get("acceptance_criteria", []):
        if not (set(criterion.get("gate_ids", [])) & gate_set or criterion.get("eval_ids")):
            _fail(failures, "I-008", "acceptance criterion is unmapped")
    if any(gate.get("blocking") and not gate.get("requirement_ids") and not gate.get("risk_ids") for gate in gates):
        _fail(failures, "I-009", "blocking gate is orphaned")
    effects = contract.get("effects", {})
    if effects.get("external_write"):
        if not all(effects.get(name) for name in ("pre_gate_ids", "post_gate_ids", "recovery_gate_ids")):
            _fail(failures, "I-010", "write effect lacks pre/post/recovery gates")
        if contract.get("permissions", {}).get("default") != "deny" or not contract.get("permissions", {}).get("audit"):
            _fail(failures, "I-011", "external write lacks deny permission and audit")
        if effects.get("effect_level") in {"high", "critical"} and not contract.get("approval", {}).get("required"):
            _fail(failures, "I-012", "high-risk write lacks approval")
        if effects.get("irreversible") and (not effects.get("risk_acceptance") or not effects.get("manual_repair")):
            _fail(failures, "I-013", "irreversible write lacks risk acceptance or recovery")
    if contract.get("secrets", {}).get("through_llm_context") is not False:
        _fail(failures, "I-014", "secret may enter LLM context")
    sandbox = contract.get("sandbox", {})
    if sandbox.get("required") and not all(sandbox.get(name) for name in ("filesystem", "network", "process", "resources", "secret_injection")):
        _fail(failures, "I-015", "sandbox profile incomplete")
    rag = contract.get("rag", {})
    if rag.get("enabled") and not all(rag.get(name) for name in ("inventory", "source_freshness", "index_freshness", "acl", "citation", "abstention", "retrieval_eval")):
        _fail(failures, "I-016", "RAG contract incomplete")
    agent = contract.get("agent", {})
    if agent.get("enabled") and not all(agent.get(name) for name in ("limits", "termination", "trace", "loop_detection")):
        _fail(failures, "I-017", "agent limits/termination/trace incomplete")
    state = contract.get("state", {})
    if state.get("persistent") and not all(state.get(name) for name in ("owner", "identity", "ttl_seconds", "delete", "migration", "checkpoint_revalidation")):
        _fail(failures, "I-018", "persistent state lifecycle incomplete")
    tools = contract.get("tools", [])
    effects_seen = {tool.get("effect") for tool in tools}
    if not {"read", "write"}.issubset(effects_seen):
        _fail(failures, "I-019", "read/write tools are not separated")
    if any(not tool.get("schema_digest") or tool.get("unknown_fields") != "reject" for tool in tools):
        _fail(failures, "I-020", "tool schema binding incomplete")
    if any(not all(tool.get(name) for name in ("namespace", "version", "server")) for tool in tools):
        _fail(failures, "I-021", "tool identity binding incomplete")
    hooks = contract.get("hooks", {})
    for hook in hooks.values():
        if not all(key in hook for key in ("event", "timing", "blocking", "timeout_behavior", "malformed_behavior", "fail_policy")):
            _fail(failures, "I-022", "hook semantics incomplete")
    if any(hook.get("blocking") and hook.get("async_only") for hook in hooks.values()):
        _fail(failures, "I-023", "blocking hook cannot be async-only")
    if effects.get("irreversible") and not hooks.get("pretool", {}).get("blocking"):
        _fail(failures, "I-024", "irreversible action protected only after execution")
    if contract.get("permissions", {}).get("default") != "deny" or contract.get("permissions", {}).get("wildcard"):
        _fail(failures, "I-025", "permission default is not deny")
    path_policy = contract.get("path_policy", {})
    if not all(path_policy.get(name) for name in ("canonicalize", "symlink_check", "redirect_check", "root")):
        _fail(failures, "I-026", "path canonicalization policy incomplete")
    if not sandbox.get("resources"):
        _fail(failures, "I-027", "sandbox resource limits missing")
    if sandbox.get("unsandboxed_fallback"):
        _fail(failures, "I-028", "high-risk unsandboxed fallback enabled")
    approval = contract.get("approval", {})
    if not approval.get("canonicalization") or not approval.get("digest_algorithm") or not approval.get("bind_fields"):
        _fail(failures, "I-029", "approval binding algorithm missing")
    required_bind = {"action", "tool", "resource", "tenant", "principal", "payload", "policy"}
    if not required_bind.issubset(set(approval.get("bind_fields", []))):
        _fail(failures, "I-030", "approval bind fields incomplete")
    if not all(approval.get(name) for name in ("expiry_seconds", "nonce_required", "single_use", "revocation_check")):
        _fail(failures, "I-031", "approval expiry/nonce/revocation missing")
    if effects.get("effect_level") == "critical" and (approval.get("quorum", 0) < 2 or not approval.get("distinct_principals")):
        _fail(failures, "I-032", "critical approval quorum missing")
    if effects.get("effect_level") in {"high", "critical"} and not approval.get("prevent_self_review"):
        _fail(failures, "I-033", "self-review prevention missing")
    if not all(approval.get("batch_binding", {}).get(name) for name in ("item_set", "count", "limits")):
        _fail(failures, "I-034", "batch approval binding incomplete")
    if not approval.get("jit_revoke"):
        _fail(failures, "I-035", "JIT revoke missing")
    if not contract.get("idempotency", {}).get("same_key_same_payload_digest"):
        _fail(failures, "I-036", "idempotency payload binding missing")
    retry = contract.get("retry", {})
    if retry.get("outcome_unknown_auto_retry"):
        _fail(failures, "I-037", "OUTCOME_UNKNOWN may be blindly retried")
    if not contract.get("idempotency", {}).get("required") and contract.get("idempotency", {}).get("non_idempotent_policy") != "blocked":
        _fail(failures, "I-038", "non-idempotent action not blocked")
    if not all(retry.get(name) for name in ("allowed_error_classes", "max_attempts", "max_elapsed_seconds", "backoff")):
        _fail(failures, "I-039", "retry budget incomplete")
    if retry.get("conflict_policy") != "refetch_replan":
        _fail(failures, "I-040", "conflict uses blind retry")
    compensation = contract.get("compensation", {})
    if compensation.get("required") and not all(compensation.get(name) for name in ("handler", "order", "idempotent", "manual_fallback")):
        _fail(failures, "I-041", "compensation contract incomplete")
    reconciliation = contract.get("reconciliation", {})
    if not all(reconciliation.get(name) for name in ("source_of_truth", "expected_fields", "actual_fields")):
        _fail(failures, "I-042", "reconciliation contract incomplete")
    if reconciliation.get("mismatch_status") == "PASS":
        _fail(failures, "I-043", "reconciliation mismatch maps to PASS")
    runtime = contract.get("runtime", {})
    if not runtime.get("terminal_requires_no_pending"):
        _fail(failures, "I-044", "terminal state permits pending effects")
    if not runtime.get("tool_pairing"):
        _fail(failures, "I-045", "tool call/result pairing missing")
    if not state.get("checkpoint_revalidation"):
        _fail(failures, "I-046", "checkpoint revalidation missing")
    if not all(runtime.get("parallel", {}).get(name) for name in ("base_digest", "merge_policy", "conflict_policy")):
        _fail(failures, "I-047", "parallel merge contract incomplete")
    if not all(runtime.get("background", {}).get(name) for name in ("lease", "fencing", "cancel", "late_result")):
        _fail(failures, "I-048", "background fencing contract incomplete")
    if not contract.get("phase_manifest", {}).get("digest") or not contract.get("phase_manifest", {}).get("stale_propagation"):
        _fail(failures, "I-049", "phase boundary digest/stale propagation missing")
    if set(runtime.get("partial_completion", [])) != {"completed", "failed", "unknown", "compensated"}:
        _fail(failures, "I-050", "partial completion enum incomplete")
    acl = rag.get("acl", {})
    if rag.get("enabled") and acl.get("source") != "authenticated_context":
        _fail(failures, "I-051", "RAG tenant filter not from authenticated context")
    if rag.get("enabled") and not acl.get("cache_scope_includes_auth"):
        _fail(failures, "I-052", "RAG cache omits authorization context")
    if rag.get("enabled") and not rag.get("deletion_propagation"):
        _fail(failures, "I-053", "RAG deletion propagation missing")
    if rag.get("enabled") and not {"source_digest", "version", "span", "acl", "pipeline_version"}.issubset(set(rag.get("chunk_metadata", []))):
        _fail(failures, "I-054", "RAG chunk metadata incomplete")
    if rag.get("enabled") and not (rag.get("retrieval_eval") and rag.get("generation_eval")):
        _fail(failures, "I-055", "retrieval/generation eval not separated")
    if rag.get("enabled") and not {"NO_EVIDENCE", "CONFLICT"}.issubset(set(rag.get("abstention", []))):
        _fail(failures, "I-056", "RAG abstention states missing")
    if rag.get("retrieved_instruction_authority") is not False:
        _fail(failures, "I-057", "retrieved instruction has privileged authority")
    result = contract.get("result_contract", {})
    if result.get("allow_free_text_pass"):
        _fail(failures, "I-058", "free-text PASS allowed")
    binding_fields = {"subject", "policy", "checker", "input", "trace", "time", "evidence", "issuer"}
    if not binding_fields.issubset(set(result.get("required_bindings", []))):
        _fail(failures, "I-059", "PASS binding fields incomplete")
    attestation = contract.get("attestation", {})
    if effects.get("effect_level") in {"high", "critical"} and not attestation.get("required_for_high_risk"):
        _fail(failures, "I-060", "high-risk attestation not required")
    if attestation.get("subject_digest") != attestation.get("current_artifact_digest"):
        _fail(failures, "I-061", "attestation subject mismatch")
    if attestation.get("issuer") not in attestation.get("issuer_allowlist", []) or not attestation.get("predicate_type"):
        _fail(failures, "I-062", "attestation issuer/predicate not trusted")
    if not attestation.get("evidence"):
        _fail(failures, "I-063", "test-result evidence missing")
    if not snapshot.get("issued_at") or not snapshot.get("expires_at"):
        _fail(failures, "I-064", "result freshness timestamps missing")
    if not contract.get("phase_manifest", {}).get("stale_propagation"):
        _fail(failures, "I-065", "dependency change does not propagate STALE")
    if result.get("error_to_pass"):
        _fail(failures, "I-066", "ERROR may become PASS")
    if hooks.get("pretool", {}).get("fail_policy") != "closed":
        _fail(failures, "I-067", "high-risk gate is not fail-closed")
    if contract.get("waivers"):
        for waiver in contract["waivers"]:
            if not all(waiver.get(name) for name in ("violation", "subject", "scope", "owner", "approver", "controls", "expiry")):
                _fail(failures, "I-069", "waiver contract incomplete")
            if waiver.get("converts_to_pass"):
                _fail(failures, "I-070", "waiver converts to PASS")
    inventory = contract.get("implementation_inventory", [])
    inventory_by_gate = {item.get("gate_id"): item for item in inventory}
    for gate in gates:
        implementation = inventory_by_gate.get(gate.get("id"), {})
        if not implementation.get("path") or not implementation.get("digest"):
            _fail(failures, "I-071", "required Gate implementation mapping missing")
        if not implementation.get("annotation"):
            _fail(failures, "I-072", "runtime inventory annotation missing")
        if not gate.get("test_ids"):
            _fail(failures, "I-074", "Gate lacks required tests")
        if gate.get("blocking") and not gate.get("mutation_ids"):
            _fail(failures, "I-075", "critical Gate lacks mutation test")
    if result.get("required_test_skip_success") or contract.get("tests", {}).get("required_job_skip_success"):
        _fail(failures, "I-076", "required test skip counts as success")
    release = contract.get("release", {})
    if not all(release.get(name) for name in ("protected_branch", "protected_environment", "trusted_issuer", "prevent_self_review")):
        _fail(failures, "I-077", "release protections incomplete")
    if not release.get("rehash_before_release"):
        _fail(failures, "I-078", "release does not rehash current subject")
    if not all(release.get("manifest", {}).get(name) for name in ("artifact_digest", "gate_result_digests")):
        _fail(failures, "I-079", "release manifest incomplete")
    audit = contract.get("audit", {})
    if audit.get("generator_identity") == audit.get("auditor_identity"):
        _fail(failures, "I-080", "generator and auditor identities are not separated")
    if not audit.get("blind_first"):
        _fail(failures, "I-081", "auditor is not blind-first")
    if not contract.get("trace", {}).get("context_is_not_authorization"):
        _fail(failures, "I-082", "trace context used as authorization")
    if not audit.get("append_only_redacted_evidence"):
        _fail(failures, "I-083", "evidence is not redacted/tamper-evident")
    remote = contract.get("remote_gate", {})
    if not all(remote.get(name) for name in ("timeout_policy", "activation_policy", "last_known_good", "ttl_seconds")):
        _fail(failures, "I-084", "remote Gate activation/LKG/TTL incomplete")
    if contract.get("status") == "APPROVED" and not audit.get("actual_independent_executor_ran"):
        _fail(failures, "I-085", "approved status lacks independent audit")

    asserted = contract.get("invariant_assertions", {})
    for invariant_id in invariant_ids:
        if asserted.get(invariant_id) is not True:
            _fail(failures, invariant_id, "catalog invariant assertion missing")
    results = [
        {"id": invariant_id, "status": "FAIL" if invariant_id in failures else "PASS", "message": failures.get(invariant_id)}
        for invariant_id in invariant_ids
    ]
    return {
        "schema_version": "1.0",
        "status": "FAIL" if failures else "PASS",
        "counts": {"invariants": len(invariant_ids), "passed": len(invariant_ids) - len(failures), "failed": len(failures)},
        "failures": failures,
        "results": results,
        "subject_digest": sha256_value(contract),
    }


def qualified_tool_map(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {tool["id"]: tool for tool in policy.get("tools", []) if isinstance(tool, dict) and tool.get("id")}


def pretool_gate(request: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    if not policy:
        return {"status": "BLOCK", "reason": "MISSING_POLICY"}
    if policy.get("stale"):
        return {"status": "STALE", "reason": "POLICY_STALE"}
    if request.get("handler_timeout"):
        return {"status": "BLOCK", "reason": "HOOK_TIMEOUT_FAIL_CLOSED"}
    if request.get("malformed_handler_result"):
        return {"status": "BLOCK", "reason": "MALFORMED_HANDLER_FAIL_CLOSED"}
    if not policy.get("direct_bypass_inventory_complete"):
        return {"status": "BLOCK", "reason": "DIRECT_BYPASS_INVENTORY_INCOMPLETE"}
    if request.get("secret"):
        return {"status": "BLOCK", "reason": "SECRET_INPUT"}
    path = str(request.get("path", ""))
    if path:
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or request.get("symlink_escape"):
            return {"status": "BLOCK", "reason": "PATH_OUTSIDE_ROOT"}
    tool_id = request.get("tool_id")
    tools = qualified_tool_map(policy)
    if tool_id not in tools:
        return {"status": "BLOCK", "reason": "UNKNOWN_OR_UNQUALIFIED_TOOL"}
    tool = tools[tool_id]
    if request.get("intent") == "read" and tool.get("effect") == "write":
        return {"status": "BLOCK", "reason": "WRITE_TOOL_FOR_READ_INTENT"}
    if request.get("ungated_allow"):
        return {"status": "BLOCK", "reason": "UNGATED_ALLOW_FORBIDDEN"}
    return {"status": "PASS", "reason": "PRETOOL_CURRENT", "operational_permission": False}


def posttool_gate(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("tool_failure") and result.get("effect_may_have_happened"):
        return {"status": "OUTCOME_UNKNOWN", "reason": "RECONCILIATION_REQUIRED", "retry": False}
    if result.get("reconciliation_mismatch"):
        return {"status": "OUTCOME_UNKNOWN", "reason": "RECONCILIATION_MISMATCH", "retry": False}
    return {"status": "PASS", "reason": "POSTTOOL_RECONCILED", "operational_permission": False}


def stop_gate(result: Any, expected: dict[str, str]) -> dict[str, Any]:
    if isinstance(result, str):
        return {"status": "BLOCK", "reason": "FREE_TEXT_PASS_FORBIDDEN"}
    if not isinstance(result, dict):
        return {"status": "BLOCK", "reason": "MALFORMED_RESULT"}
    required = {"status", "subject_digest", "policy_digest", "checker_digest", "input_digest", "trace_id", "evidence", "issuer"}
    if not required.issubset(result):
        return {"status": "BLOCK", "reason": "RESULT_BINDING_INCOMPLETE"}
    if result.get("status") == "STALE" or result.get("subject_digest") != expected.get("subject_digest"):
        return {"status": "STALE", "reason": "SUBJECT_STALE"}
    for field in ("policy_digest", "checker_digest", "input_digest"):
        if result.get(field) != expected.get(field):
            return {"status": "BLOCK", "reason": f"{field.upper()}_MISMATCH"}
    if result.get("issuer") not in expected.get("trusted_issuers", "").split(","):
        return {"status": "BLOCK", "reason": "UNTRUSTED_ISSUER"}
    if result.get("forged"):
        return {"status": "BLOCK", "reason": "FORGED_RESULT"}
    return {"status": "PASS_LOCAL_PROCEDURE", "reason": "CURRENT_STRUCTURED_RESULT", "operational_permission": False}


def mutate_contract(contract: dict[str, Any], mutation_id: str) -> dict[str, Any]:
    mutated = copy.deepcopy(contract)
    operations = {
        "GMUT-001": lambda c: c["snapshot"].__setitem__("upstream_digest", ""),
        "GMUT-002": lambda c: c["result_contract"].__setitem__("allow_free_text_pass", True),
        "GMUT-003": lambda c: c["hooks"]["pretool"].__setitem__("fail_policy", "open"),
        "GMUT-004": lambda c: c["implementation_inventory"][0].__setitem__("path", ""),
        "GMUT-005": lambda c: c["approval"].__setitem__("required", False),
        "GMUT-006": lambda c: c["permissions"].__setitem__("default", "allow"),
        "GMUT-007": lambda c: c["hooks"]["pretool"].__setitem__("timeout_behavior", "allow"),
        "GMUT-008": lambda c: c["hooks"]["pretool"].__setitem__("malformed_behavior", "allow"),
        "GMUT-009": lambda c: c["path_policy"].__setitem__("canonicalize", False),
        "GMUT-010": lambda c: c["tools"][0].__setitem__("namespace", ""),
        "GMUT-011": lambda c: c["rag"].__setitem__("acl", {}),
        "GMUT-012": lambda c: c["agent"].__setitem__("termination", ""),
        "GMUT-013": lambda c: c["state"].__setitem__("ttl_seconds", 0),
        "GMUT-014": lambda c: (c["approval"].__setitem__("expiry_seconds", 0), c["approval"].__setitem__("nonce_required", False)),
        "GMUT-015": lambda c: c["idempotency"].__setitem__("same_key_same_payload_digest", False),
        "GMUT-016": lambda c: c["retry"].__setitem__("outcome_unknown_auto_retry", True),
        "GMUT-017": lambda c: c["attestation"].__setitem__("subject_digest", "sha256:other"),
        "GMUT-018": lambda c: c["audit"].__setitem__("blind_first", False),
        "GMUT-019": lambda c: c["phase_manifest"].__setitem__("digest", ""),
        "GMUT-020": lambda c: c["result_contract"].__setitem__("required_test_skip_success", True),
    }
    operations[mutation_id](mutated)
    mutated["contract_digest"] = sha256_value({key: value for key, value in mutated.items() if key != "contract_digest"})
    return mutated
