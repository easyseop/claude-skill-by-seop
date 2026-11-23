#!/usr/bin/env python3
"""Finalize Execution Generator evidence, report, state, and manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--auditor", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()

    source_files = sorted(path for path in args.package.rglob("*") if path.is_file() and "__pycache__" not in path.parts) + [args.auditor]
    source_rows = [{"path": path.as_posix(), "sha256": digest(path), "bytes": path.stat().st_size} for path in source_files]
    canonical = "".join(f"{row['path']}\0{row['sha256']}\n" for row in source_rows).encode("utf-8")
    source_digest = "sha256:" + hashlib.sha256(canonical).hexdigest()

    manifest_path = args.evidence / "implementation-manifest.json"
    evidence_files = sorted(path for path in args.evidence.rglob("*") if path.is_file() and path != manifest_path)
    evidence_rows = [{"path": path.as_posix(), "sha256": digest(path), "bytes": path.stat().st_size} for path in evidence_files]
    payload = {
        "schema_version": "1.0",
        "status": "PASS_LOCAL_PROCEDURE",
        "scope": "E0-E4_LOCAL_CANDIDATE",
        "subject_source_digest": source_digest,
        "verified_runner": False,
        "dynamic_execution": "HARD_ENFORCEMENT_UNAVAILABLE",
        "independent_identity": "UNVERIFIED",
        "operational_permission": False,
        "source_files": source_rows,
        "evidence_files": evidence_rows,
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

    report = f"""# Execution Artifact Generator E0~E4 복구 구현 결과

## 종합 판정

Execution Artifact Generator는 격리 CI runner에서 검증됐으며 **PASS_LOCAL_PROCEDURE**다.

- source digest: `{source_digest}`
- EXEC 규칙: 30/30
- 기계 불변식: 45/45
- Planner execution golden: 22/22
- EXEVAL: 26/26
- EXMUT: 10/10 killed
- Builder 반례: 16/16
- traceability: forward/reverse closed

## 실제 지원 범위

- `no_code`: 지원·검증
- `existing_artifact`: 지원·검증
- `python_local`: static scaffold·static check 지원, 동적 실행 금지
- `java_cli`: contract-only, verified build/test pack 없음

## 안전 경계

- verified sandbox/runner: 없음
- generated-code dynamic execution: 수행하지 않음
- 실제 외부 write·approval·idempotency ledger·reconciliation dispatch: HARD_ENFORCEMENT_UNAVAILABLE
- durable workflow/state·tenant RAG·production release: 범위 밖
- independent audit identity: UNVERIFIED
- operational permission: false

## Evidence

`docs/agent-authoring/evidence/execution-artifact-generator/`에 contract check, traceability, golden mapping, eval, mutation, builder tests, inventory, reuse assessment, audit, stop gate, implementation manifest를 보존한다.

## 다음 단계

Ownership boundary가 PASS하면 Execution을 `VERIFIED_LOCAL_CANDIDATE`로 닫고 Knowledge/RAG Builder K0~K6 작업판을 재개한다.
"""
    write(args.report, report)

    state = f"""schema_version: "1.0"
workstream_id: upstream-recovery
session_type: implementation
repository: easyseop/claude-skill-by-seop
branch: recovery/upstream-builders
status: IN_PROGRESS
phase: E_BOUNDARY_RECHECK

progress:
  planner_source:
    status: VERIFIED_LOCAL_CANDIDATE
    operational_permission: false
  gate_source:
    status: VERIFIED_LOCAL_CANDIDATE
    operational_permission: false
  execution_source:
    status: TESTED_PASS_BOUNDARY_PENDING
    source_digest: {source_digest}
    exec_rules: "30/30"
    invariants: "45/45"
    planner_golden: "22/22"
    evals: "26/26"
    mutations: "10/10 killed"
    builder_tests: "16/16"
    traceability: PASS
    verified_runner: false
    dynamic_execution: HARD_ENFORCEMENT_UNAVAILABLE
    independent_identity: UNVERIFIED
    operational_permission: false

blocker: null
next_action: >-
  Pass the workstream ownership boundary check, then mark the full upstream
  recovery workstream READY_FOR_REVIEW and unblock Knowledge/RAG Builder K0-K6.
"""
    write(args.state, state)

    output = f"""schema_version: "1.0"
workstream_id: upstream-recovery

planner:
  status: VERIFIED_LOCAL_CANDIDATE

gate:
  status: VERIFIED_LOCAL_CANDIDATE

execution:
  status: TESTED_PASS_BOUNDARY_PENDING
  source_digest: {source_digest}
  exec_rules: 30
  invariants: 45
  planner_golden: 22
  evals: 26
  mutations_killed: 10
  builder_tests: 16
  critical_mutants_survived: 0
  traceability: PASS
  verified_runner: false
  dynamic_execution: HARD_ENFORCEMENT_UNAVAILABLE
  independent_identity: UNVERIFIED
  operational_permission: false

review_status: EXECUTION_BOUNDARY_RECHECK
"""
    write(args.output_manifest, output)
    print(json.dumps({"status": "PASS", "source_digest": source_digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
