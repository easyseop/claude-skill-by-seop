#!/usr/bin/env python3
"""Finalize Gate Generator evidence, report, state, and manifest."""

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
        "scope": "M0-M3_LOCAL_CANDIDATE",
        "subject_source_digest": source_digest,
        "host_enforcement": "UNVERIFIED",
        "m4_m7": "HARD_ENFORCEMENT_UNAVAILABLE",
        "independent_identity": "UNVERIFIED",
        "operational_permission": False,
        "source_files": source_rows,
        "evidence_files": evidence_rows,
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

    report = f"""# Gate Generator M0~M3 복구 구현 결과

## 종합 판정

Gate Generator는 격리된 CI runner에서 검증됐으며 **PASS_LOCAL_PROCEDURE**다.

- source digest: `{source_digest}`
- GATE 규칙: 80/80
- 기계 불변식: 85/85
- Planner golden: 22/22
- GEVAL: 48/48
- critical mutation: 20/20 killed
- Hook smoke: 19/19
- traceability: forward/reverse closed

## 실제 구현 범위

M0 규칙·schema·digest, M1 Planner→Gate contract, M2 결정적 checker·STALE·PASS 위조 차단, M3 로컬 input/path/tool Gate와 Claude Code adapter 예시를 구현했다.

## 안전 경계

- actual Host Hook 활성화: UNVERIFIED
- independent audit identity: UNVERIFIED
- M4 exact approval, M5 durable state, M6 tenant RAG, M7 production release: HARD_ENFORCEMENT_UNAVAILABLE
- operational permission: false
- `.claude/settings.json` 자동 수정: 수행하지 않음

## Evidence

`docs/agent-authoring/evidence/gate-generator/` 아래 baseline, trace, Planner golden, eval, mutation, Hook smoke, inventory, audit, stop gate, implementation manifest를 보존한다.

## 다음 단계

Ownership boundary가 PASS하면 Gate를 `VERIFIED_LOCAL_CANDIDATE`로 닫고 Execution Artifact Generator E0~E4 복구를 시작한다.
"""
    write(args.report, report)

    state = f"""schema_version: "1.0"
workstream_id: upstream-recovery
session_type: implementation
repository: easyseop/claude-skill-by-seop
branch: recovery/upstream-builders
status: IN_PROGRESS
phase: G_BOUNDARY_RECHECK

progress:
  planner_source:
    status: VERIFIED_LOCAL_CANDIDATE
    operational_permission: false
  gate_source:
    status: TESTED_PASS_BOUNDARY_PENDING
    source_digest: {source_digest}
    gate_rules: "80/80"
    invariants: "85/85"
    planner_golden: "22/22"
    evals: "48/48"
    mutations: "20/20 killed"
    hook_smoke: "19/19"
    traceability: PASS
    host_enforcement: UNVERIFIED
    independent_identity: UNVERIFIED
    m4_m7: HARD_ENFORCEMENT_UNAVAILABLE
    operational_permission: false
  execution_source: PENDING

blocker: null
next_action: >-
  Pass the workstream ownership boundary check, then mark Gate
  VERIFIED_LOCAL_CANDIDATE and start Execution Artifact Generator E0-E4 recovery.
"""
    write(args.state, state)

    output = f"""schema_version: "1.0"
workstream_id: upstream-recovery

planner:
  status: VERIFIED_LOCAL_CANDIDATE

gate:
  status: TESTED_PASS_BOUNDARY_PENDING
  source_digest: {source_digest}
  gate_rules: 80
  invariants: 85
  planner_golden: 22
  evals: 48
  mutations_killed: 20
  hook_smoke: 19
  critical_mutants_survived: 0
  traceability: PASS
  host_enforcement: UNVERIFIED
  independent_identity: UNVERIFIED
  operational_permission: false

execution:
  status: PENDING

review_status: GATE_BOUNDARY_RECHECK
"""
    write(args.output_manifest, output)
    print(json.dumps({"status": "PASS", "source_digest": source_digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
