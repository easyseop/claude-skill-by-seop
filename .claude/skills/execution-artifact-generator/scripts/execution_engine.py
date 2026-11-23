#!/usr/bin/env python3
"""Deterministic core for Execution Artifact Generator E0-E4."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

EXIT_REGISTRY = {
    "RESULT_EMITTED": 0,
    "INVALID_INPUT": 2,
    "GATE_BLOCKED": 3,
    "DEPENDENCY_EXHAUSTED": 4,
    "RUNNER_ERROR": 5,
    "OUTCOME_UNKNOWN": 6,
}
SUPPORTED_BUILDERS = {"no_code", "existing_artifact", "python_local", "java_cli"}
TERMINAL_UNAVAILABLE = {
    "HARD_ENFORCEMENT_UNAVAILABLE",
    "UNSUPPORTED_RUNTIME_PACK",
    "BLOCKED_PENDING_REPO_FACTS",
    "PLANNER_REENTRY_REQUIRED",
    "GATE_REENTRY_REQUIRED",
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


def continuous_ids(ids: list[str], prefix: str, start: int, end: int, width: int) -> bool:
    return ids == [f"{prefix}{number:0{width}d}" for number in range(start, end + 1)]


def valid_contract(invariant_ids: list[str]) -> dict[str, Any]:
    artifact = {
        "id": "ART-001",
        "kind": "cli_script",
        "primary_responsibility": "normalize a bounded CSV fixture",
        "owner": "execution-generator",
        "acceptance_ids": ["AC-EXEC-1"],
        "necessity_test": {"baseline": "prompt-only fails deterministic rows", "expected_gain": "stable transform"},
        "reuse_assessment": {"status": "NEW_ARTIFACT_JUSTIFIED", "inventory_complete": True, "candidates": [], "gap": "no compatible existing artifact"},
        "runtime": {"language": "python", "version": "3.11", "repository_fact": "pyproject/test runner present", "compatible": True},
        "builder": "python_local",
        "implementation_state": "TESTED",
        "path": "generated/normalize_csv.py",
        "entrypoint": ["python", "generated/normalize_csv.py"],
        "input_schema_digest": "sha256:input-schema",
        "output_schema_digest": "sha256:output-schema",
        "unknown_fields": "reject",
        "stdout_policy": "one-json-document",
        "diagnostics_channel": "stderr",
        "effect_class": "write",
        "pre_effect_gate_ids": ["G-PRE-001"],
        "post_effect_gate_ids": ["G-POST-001"],
        "permission_scopes": ["read", "write", "reconcile"],
        "dry_run": {"same_validation": True, "writer_called": False, "target_fingerprint": "sha256:target"},
        "apply": {"recheck_target_fingerprint": True, "recheck_gate": True, "recheck_plan": True},
        "idempotency": {"required": True, "scope": "tenant+operation", "payload_digest_bound": True, "same_key_different_payload": "reject"},
        "retry": {"policy_owned": True, "max_attempts": 3, "max_elapsed_seconds": 30, "retryable": ["rate_limit"], "outcome_unknown_auto_retry": False},
        "reconciliation": {"source_of_truth": "target-system", "expected_fields": ["count", "digest"], "actual_fields": ["count", "digest"], "result_schema_digest": "sha256:reconcile-schema"},
        "compensation": {"registered": True, "manual_repair": "escalate with target id", "idempotent": True},
        "shell": {"mode": "argv", "shell": False, "fixed_executable": True, "cwd_allowlist": ["repo"], "env_allowlist": ["PATH"]},
        "sql": {"raw_strings": False, "values_bound": True, "identifier_allowlist": True, "autocommit": False},
        "path_policy": {"canonicalize": True, "root": "generated", "symlink_check": True},
        "secret_policy": {"references_only": True, "value_fields": False, "cli_args": False, "logs": False, "build_args": False},
        "dependency": {"lock_digest": "sha256:lock", "toolchain_digest": "sha256:toolchain", "image_digest": "sha256:no-image-local", "floating": False},
        "supply_chain": {"sbom_required": False, "provenance_required": False, "artifact_digest": "sha256:artifact"},
        "sandbox": {"required": True, "verified": False, "status": "HARD_ENFORCEMENT_UNAVAILABLE", "inventory_digest": "sha256:sandbox-inventory"},
        "egress": {"required": False, "allowlist": [], "enforcer_verified": False},
        "source_digest": "sha256:source",
        "test_evidence": {
            "artifact_digest": "sha256:artifact",
            "test_digest": "sha256:test",
            "runner_digest": "sha256:runner",
            "environment_digest": "sha256:env",
            "result_digest": "sha256:result",
            "self_digest": "sha256:evidence",
            "historical": False,
            "executed": True,
        },
        "audit": {"blind_first": True, "auditor_identity": "unverified-separate-required", "actual_independent_executor_ran": False, "evidence": ["evidence://execution-audit"]},
    }
    contract = {
        "schema_version": "1.0",
        "contract_id": "EXECUTION-CONTRACT-FIXTURE",
        "status": "READY_FOR_BUILD",
        "snapshot": {
            "planner_digest": "sha256:planner",
            "gate_digest": "sha256:gate",
            "checker_digest": "sha256:checker",
            "inventory_digest": "sha256:inventory",
            "input_digest": "sha256:input",
            "schema_digest": "sha256:contract-schema",
            "source_digest": "sha256:source",
            "lock_digest": "sha256:lock",
            "toolchain_digest": "sha256:toolchain",
            "test_digest": "sha256:test",
            "runtime_digest": "sha256:runtime",
        },
        "planner_binding": {"control_mode": "deterministic_workflow", "selected_components": ["script", "validator"], "current_control_mode": "deterministic_workflow", "current_selected_components": ["script", "validator"], "reentry_required": False},
        "gate_binding": {"required_gate_ids": ["G-PRE-001", "G-POST-001"], "catalog_gate_ids": ["G-PRE-001", "G-POST-001"], "checker_digest": "sha256:gate-checker", "current_status": "PASS_LOCAL_PROCEDURE"},
        "decision": {"execution_required": True, "disposition": "NEW_ARTIFACT_JUSTIFIED", "reason": "deterministic repeated transform"},
        "repository_facts": {"complete_bounded": True, "supported_runtimes": ["python:3.11", "java:17"], "existing_entrypoints": [], "lockfiles": ["pyproject.lock"], "test_runners": ["python"]},
        "artifacts": [artifact],
        "exit_registry": EXIT_REGISTRY,
        "control_flow": {"uses_error_codes": True, "uses_error_text": False, "free_text_pass": False, "exit_zero_is_pass": False},
        "permissions": {"default": "deny", "separated": ["read", "write", "reconcile", "release"], "wildcard": False},
        "stale_dependencies": ["planner", "gate", "source", "lock", "toolchain", "schema", "inventory", "input", "test", "runtime"],
        "traceability": {
            "forward": [{"acceptance_id": "AC-EXEC-1", "artifact_id": "ART-001", "gate_ids": ["G-PRE-001", "G-POST-001"], "entrypoint": "generated/normalize_csv.py", "test_ids": ["EXEVAL-002"], "mutation_ids": ["EXMUT-003"], "evidence": ["evidence://execution-test"]}],
            "reverse": [{"entrypoint": "generated/normalize_csv.py", "artifact_id": "ART-001", "gate_ids": ["G-PRE-001", "G-POST-001"], "acceptance_ids": ["AC-EXEC-1"]}],
            "known_entrypoints": ["generated/normalize_csv.py"],
        },
        "result_contract": {"statuses": ["NOT_REQUIRED", "REUSE_READY", "STATIC_CHECKED", "TESTED", "BLOCKED", "STALE", "OUTCOME_UNKNOWN", "HARD_ENFORCEMENT_UNAVAILABLE", "UNSUPPORTED_RUNTIME_PACK", "PLANNER_REENTRY_REQUIRED", "GATE_REENTRY_REQUIRED"], "gate_statuses_not_pass": ["ERROR", "STALE", "OUTCOME_UNKNOWN", "WAIVED"], "free_text_pass": False},
        "runtime_boundary": {"verified_runner": False, "dynamic_execution_permitted": False, "local_pure_static_check": True, "operational_permission": False},
        "invariant_assertions": {identifier: True for identifier in invariant_ids},
    }
    contract["contract_digest"] = sha256_value({key: value for key, value in contract.items() if key != "contract_digest"})
    return contract


def fail(failures: dict[str, str], invariant_id: str, message: str) -> None:
    failures.setdefault(invariant_id, message)


def check_contract(contract: dict[str, Any], invariant_ids: list[str]) -> dict[str, Any]:
    failures: dict[str, str] = {}
    for key in ("schema_version", "contract_id", "status", "snapshot", "planner_binding", "gate_binding", "decision", "artifacts"):
        if not contract.get(key):
            fail(failures, "EXI-001", f"missing {key}")
    snapshot = contract.get("snapshot", {})
    if snapshot.get("planner_digest") != "sha256:planner":
        fail(failures, "EXI-002", "Planner digest stale")
    planner = contract.get("planner_binding", {})
    if planner.get("control_mode") != planner.get("current_control_mode") or planner.get("selected_components") != planner.get("current_selected_components"):
        fail(failures, "EXI-003", "Planner architecture mismatch")
    artifacts = contract.get("artifacts", [])
    if contract.get("decision", {}).get("execution_required") is False and artifacts:
        fail(failures, "EXI-004", "no-code decision contains executable")
    if planner.get("reentry_required") and contract.get("status") in {"READY_FOR_BUILD", "TESTED", "READY_FOR_ASSEMBLY"}:
        fail(failures, "EXI-005", "Planner reentry cannot be ready")
    gate = contract.get("gate_binding", {})
    gate_catalog = set(gate.get("catalog_gate_ids", []))
    known_entrypoints = set(contract.get("traceability", {}).get("known_entrypoints", []))
    reverse_entrypoints = {item.get("entrypoint") for item in contract.get("traceability", {}).get("reverse", [])}
    for artifact in artifacts:
        path = artifact.get("path")
        if artifact.get("reuse_assessment", {}).get("status") == "NEW_ARTIFACT_JUSTIFIED" and not artifact.get("reuse_assessment", {}).get("inventory_complete"):
            fail(failures, "EXI-006", "new artifact lacks reuse inventory")
        if not artifact.get("necessity_test") or not artifact.get("owner") or not artifact.get("acceptance_ids"):
            fail(failures, "EXI-007", "artifact necessity/owner/acceptance missing")
        if artifact.get("implementation_state") == "NOT_REQUIRED" and (artifact.get("entrypoint") or artifact.get("effect_class") not in (None, "none")):
            fail(failures, "EXI-008", "not-required artifact has executable/effect")
        if not artifact.get("runtime", {}).get("compatible"):
            fail(failures, "EXI-009", "runtime incompatible with repository facts")
        if not artifact.get("input_schema_digest") or not artifact.get("output_schema_digest"):
            fail(failures, "EXI-010", "schema digest missing")
        if artifact.get("unknown_fields") != "reject":
            fail(failures, "EXI-011", "unknown fields accepted")
        if artifact.get("kind") == "cli_script" and artifact.get("stdout_policy") != "one-json-document":
            fail(failures, "EXI-012", "CLI stdout contract invalid")
        if contract.get("exit_registry") != EXIT_REGISTRY:
            fail(failures, "EXI-013", "exit registry drift")
        if contract.get("control_flow", {}).get("uses_error_text"):
            fail(failures, "EXI-014", "error text drives control flow")
        if artifact.get("effect_class") not in {"none", "read", "write", "reconcile", "release"}:
            fail(failures, "EXI-015", "invalid effect class")
        if artifact.get("effect_class") == "write":
            if not artifact.get("pre_effect_gate_ids") or "write" not in artifact.get("permission_scopes", []):
                fail(failures, "EXI-016", "write lacks pre-effect Gate/permission")
            if artifact.get("dry_run", {}).get("writer_called") is not False:
                fail(failures, "EXI-017", "dry-run called writer")
            if not artifact.get("apply", {}).get("recheck_target_fingerprint"):
                fail(failures, "EXI-018", "apply lacks target fingerprint recheck")
        idem = artifact.get("idempotency", {})
        if artifact.get("effect_class") == "write" and not all(idem.get(name) for name in ("required", "scope", "payload_digest_bound")):
            fail(failures, "EXI-019", "idempotency scope/payload binding missing")
        if idem.get("same_key_different_payload") != "reject":
            fail(failures, "EXI-020", "same key/different payload accepted")
        if artifact.get("retry", {}).get("outcome_unknown_auto_retry"):
            fail(failures, "EXI-021", "unknown outcome auto retry enabled")
        reconciliation = artifact.get("reconciliation", {})
        if artifact.get("effect_class") == "write" and not all(reconciliation.get(name) for name in ("source_of_truth", "expected_fields", "actual_fields")):
            fail(failures, "EXI-022", "reconciliation incomplete")
        compensation = artifact.get("compensation", {})
        if artifact.get("effect_class") == "write" and not (compensation.get("registered") or compensation.get("manual_repair")):
            fail(failures, "EXI-023", "compensation/manual repair missing")
        if not set(artifact.get("pre_effect_gate_ids", []) + artifact.get("post_effect_gate_ids", [])).issubset(gate_catalog):
            fail(failures, "EXI-024", "unknown Gate reference")
        if not gate.get("checker_digest"):
            fail(failures, "EXI-025", "Gate checker digest missing")
        if set(contract.get("stale_dependencies", [])) != {"planner", "gate", "source", "lock", "toolchain", "schema", "inventory", "input", "test", "runtime"}:
            fail(failures, "EXI-026", "stale dependency coverage incomplete")
        control = contract.get("control_flow", {})
        if control.get("free_text_pass") or control.get("exit_zero_is_pass"):
            fail(failures, "EXI-027", "free-text/exit-zero treated as attestation")
        if set(contract.get("result_contract", {}).get("gate_statuses_not_pass", [])) != {"ERROR", "STALE", "OUTCOME_UNKNOWN", "WAIVED"}:
            fail(failures, "EXI-028", "non-pass Gate statuses may be promoted")
        if not all(artifact.get("path_policy", {}).get(name) for name in ("canonicalize", "root", "symlink_check")):
            fail(failures, "EXI-029", "path canonicalization incomplete")
        shell = artifact.get("shell", {})
        sql = artifact.get("sql", {})
        if shell.get("mode") != "argv" or shell.get("shell") is not False or sql.get("raw_strings"):
            fail(failures, "EXI-030", "raw shell/SQL route exists")
        if not {"read", "write", "reconcile"}.issubset(set(artifact.get("permission_scopes", []))):
            fail(failures, "EXI-031", "permission scopes not separated")
        secret = artifact.get("secret_policy", {})
        if not secret.get("references_only") or any(secret.get(name) for name in ("value_fields", "cli_args", "logs", "build_args")):
            fail(failures, "EXI-032", "secret value may leak")
        sandbox = artifact.get("sandbox", {})
        if sandbox.get("verified") and not sandbox.get("inventory_digest"):
            fail(failures, "EXI-033", "verified sandbox lacks inventory")
        if artifact.get("egress", {}).get("required") and not artifact.get("egress", {}).get("enforcer_verified"):
            fail(failures, "EXI-034", "egress allowlist lacks enforcer")
        if not sandbox.get("verified") and sandbox.get("status") != "HARD_ENFORCEMENT_UNAVAILABLE":
            fail(failures, "EXI-035", "unverified sandbox represented as available")
        dependency = artifact.get("dependency", {})
        if not all(dependency.get(name) for name in ("lock_digest", "toolchain_digest", "image_digest")):
            fail(failures, "EXI-036", "dependency/toolchain/image digest missing")
        if dependency.get("floating"):
            fail(failures, "EXI-037", "floating dependency/image")
        supply = artifact.get("supply_chain", {})
        if supply.get("sbom_required") and not supply.get("sbom_digest"):
            fail(failures, "EXI-038", "required SBOM missing")
        evidence = artifact.get("test_evidence", {})
        if artifact.get("implementation_state") in {"TESTED", "READY_FOR_ASSEMBLY"} and not all(evidence.get(name) for name in ("artifact_digest", "test_digest", "runner_digest", "environment_digest", "result_digest", "self_digest")):
            fail(failures, "EXI-039", "test evidence binding incomplete")
        if evidence.get("historical"):
            fail(failures, "EXI-040", "historical evidence reused")
        entry = artifact.get("entrypoint", [])
        entry_path = entry[-1] if isinstance(entry, list) and entry else None
        if entry_path and entry_path not in known_entrypoints:
            fail(failures, "EXI-041", "entrypoint not inventoried")
        if entry_path and entry_path not in reverse_entrypoints:
            fail(failures, "EXI-042", "orphan entrypoint")
        if artifact.get("effect_class") == "write" and not artifact.get("pre_effect_gate_ids") and artifact.get("post_effect_gate_ids"):
            fail(failures, "EXI-043", "post-only control for write")
        if artifact.get("audit", {}).get("blind_first") is not True or not artifact.get("audit", {}).get("auditor_identity") or not artifact.get("audit", {}).get("evidence"):
            fail(failures, "EXI-045", "audit order/identity/evidence incomplete")
    assertions = contract.get("invariant_assertions", {})
    for identifier in invariant_ids:
        if assertions.get(identifier) is not True:
            fail(failures, identifier, "catalog assertion missing")
    results = [{"id": identifier, "status": "FAIL" if identifier in failures else "PASS", "message": failures.get(identifier)} for identifier in invariant_ids]
    return {
        "schema_version": "1.0",
        "status": "FAIL" if failures else "PASS",
        "counts": {"invariants": len(invariant_ids), "passed": len(invariant_ids) - len(failures), "failed": len(failures)},
        "failures": failures,
        "results": results,
        "subject_digest": sha256_value(contract),
    }


def decide_execution(request: dict[str, Any], repository_facts: dict[str, Any]) -> dict[str, Any]:
    components = set(request.get("selected_components", []))
    if not components.intersection({"script", "tool", "workflow", "validator"}):
        return {"execution_required": False, "disposition": "NOT_REQUIRED", "builder": "no_code", "source_files": []}
    candidates = repository_facts.get("candidates", [])
    compatible = [candidate for candidate in candidates if candidate.get("compatible") and candidate.get("effect") == request.get("effect", "read")]
    if compatible:
        return {"execution_required": True, "disposition": "REUSE_DIRECT", "builder": "existing_artifact", "candidate": compatible[0], "source_files": []}
    runtime = request.get("runtime")
    supported = set(repository_facts.get("supported_runtimes", []))
    if runtime == "python" and "python" in supported:
        return {"execution_required": True, "disposition": "NEW_ARTIFACT_JUSTIFIED", "builder": "python_local", "dynamic_execution": False}
    if runtime == "java" and "java" in supported:
        return {"execution_required": True, "disposition": "SUPPORTED_CONTRACT_ONLY", "builder": "java_cli", "status": "HARD_ENFORCEMENT_UNAVAILABLE"}
    return {"execution_required": True, "disposition": "UNSUPPORTED_RUNTIME_PACK", "builder": None, "status": "UNSUPPORTED_RUNTIME_PACK"}


def validate_generated_source(source: str, output_path: str) -> dict[str, Any]:
    if PurePosixPath(output_path).is_absolute() or ".." in PurePosixPath(output_path).parts:
        return {"status": "BLOCKED", "reason": "OUTPUT_PATH_OUTSIDE_ROOT"}
    forbidden = [r"shell\s*=\s*True", r"subprocess\.(run|Popen)\(\s*['\"]", r"os\.system\(", r"requests\.", r"AKIA[0-9A-Z]{16}", r"BEGIN PRIVATE KEY", r"\blatest\b"]
    for pattern in forbidden:
        if re.search(pattern, source):
            return {"status": "BLOCKED", "reason": f"FORBIDDEN_PATTERN:{pattern}"}
    return {"status": "STATIC_CHECKED", "source_digest": "sha256:" + hashlib.sha256(source.encode()).hexdigest()}


def scaffold_python_local(output_root: Path, relative_path: str, contract_status: str) -> dict[str, Any]:
    if contract_status != "READY_FOR_BUILD":
        return {"status": "BLOCKED", "reason": "CONTRACT_NOT_READY"}
    pure = PurePosixPath(relative_path)
    if pure.is_absolute() or ".." in pure.parts:
        return {"status": "BLOCKED", "reason": "OUTPUT_PATH_OUTSIDE_ROOT"}
    path = output_root / Path(*pure.parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    source = '''#!/usr/bin/env python3
from __future__ import annotations
import json, sys

def main() -> int:
    payload=json.load(sys.stdin)
    result={"schema_version":"1.0","status":"RESULT_EMITTED","rows":payload.get("rows",[]),"operational_permission":False}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
'''
    check = validate_generated_source(source, relative_path)
    if check["status"] != "STATIC_CHECKED":
        return check
    path.write_text(source, encoding="utf-8")
    return {"status": "STATIC_CHECKED", "path": path.as_posix(), "source_digest": sha256_file(path), "dynamic_execution": "HARD_ENFORCEMENT_UNAVAILABLE"}


def mutate_contract(contract: dict[str, Any], mutation_id: str) -> dict[str, Any]:
    mutated = copy.deepcopy(contract)
    artifact = mutated["artifacts"][0]
    operations = {
        "EXMUT-001": lambda: mutated["planner_binding"].__setitem__("current_selected_components", ["tool"]),
        "EXMUT-002": lambda: mutated["decision"].__setitem__("execution_required", False),
        "EXMUT-003": lambda: artifact.__setitem__("pre_effect_gate_ids", []),
        "EXMUT-004": lambda: artifact.__setitem__("unknown_fields", "allow"),
        "EXMUT-005": lambda: artifact["path_policy"].__setitem__("canonicalize", False),
        "EXMUT-006": lambda: artifact["shell"].update({"mode": "string", "shell": True}),
        "EXMUT-007": lambda: artifact["retry"].__setitem__("outcome_unknown_auto_retry", True),
        "EXMUT-008": lambda: artifact["apply"].__setitem__("recheck_target_fingerprint", False),
        "EXMUT-009": lambda: artifact["dependency"].update({"lock_digest": "", "floating": True}),
        "EXMUT-010": lambda: artifact["test_evidence"].update({"historical": True, "executed": False}),
    }
    operations[mutation_id]()
    mutated["contract_digest"] = sha256_value({key: value for key, value in mutated.items() if key != "contract_digest"})
    return mutated
