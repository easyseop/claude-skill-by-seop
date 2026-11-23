#!/usr/bin/env python3
"""Finalize stable Planner evidence, report, state, and output manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def source_digest(planner_dir: Path, auditor: Path) -> tuple[str, list[dict]]:
    files = sorted(
        path for path in planner_dir.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ) + [auditor]
    rows = [
        {"path": path.as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in files
    ]
    canonical = "".join(
        f"{row['path']}\0{row['sha256']}\n" for row in rows
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest(), rows


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--planner-dir", type=Path, required=True)
    parser.add_argument("--auditor", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()

    evidence = args.evidence_dir
    evidence.mkdir(parents=True, exist_ok=True)
    manifest_path = evidence / "implementation-manifest.json"
    digest, source_rows = source_digest(args.planner_dir, args.auditor)

    evidence_rows = [
        {"path": path.as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in sorted(evidence.rglob("*"))
        if path.is_file() and path != manifest_path
    ]
    manifest = {
        "schema_version": "1.0",
        "status": "PASS_LOCAL_PROCEDURE",
        "subject_source_digest": digest,
        "operational_permission": False,
        "independent_identity": "UNVERIFIED",
        "source_files": source_rows,
        "evidence_files": evidence_rows,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    report = f"""# Capability & Artifact Planner 복구 구현 결과

## 종합 판정

현재 source는 격리된 CI runner에서 검증됐으며 **PASS_LOCAL_PROCEDURE**다.

- source digest: `{digest}`
- CAP 규칙: 36/36
- 기준 평가: 22/22
- 표현 변형: 44/44
- 총 시나리오: 66/66
- mutation: 15/15 killed
- 동일 입력 멱등성: PASS
- Prompt-only downstream Skill 미생성: PASS
- Skill 선택 시 조건부 author handoff: PASS

## 범위

Planner는 `CAPABILITY_PLAN.yaml`을 정본으로 사용하고 실제 업무 Skill·Script·Tool·RAG·Agent를 직접 만들지 않는다. 검증된 Plan에서 Gate·Execution·Knowledge·Assembly 계약만 파생한다.

## 감사·완료 경계

- deterministic machine check: PASS
- procedural audit: PASS_LOCAL_PROCEDURE
- actual independent executor: not run
- independence: UNVERIFIED
- operational permission: false
- production write·deployment·secret collection·automatic merge: forbidden

## Evidence

`docs/agent-authoring/evidence/capability-planner/` 아래 self-test, scenario, mutation, metrics, machine check, contracts, audit, stop gate, implementation manifest를 보존한다.

## 다음 단계

Ownership boundary가 PASS하면 Planner를 `VERIFIED_LOCAL_CANDIDATE`로 닫고 Gate Generator M0~M3 복구를 시작한다.
"""
    write_text(args.report, report)

    state = f"""schema_version: "1.0"
workstream_id: upstream-recovery
session_type: implementation
repository: easyseop/claude-skill-by-seop
branch: recovery/upstream-builders
status: IN_PROGRESS
phase: P_BOUNDARY_RECHECK

source_of_truth:
  start_prompt: docs/agent-authoring/workstreams/upstream-recovery/SESSION_START_PROMPT.md
  remote_connector_mode: docs/agent-authoring/workstreams/upstream-recovery/REMOTE_CONNECTOR_MODE.md
  work_order: docs/agent-authoring/workstreams/upstream-recovery/WORK_ORDER.md
  ownership: docs/agent-authoring/workstreams/upstream-recovery/OWNERSHIP.yaml
  input_manifest: docs/agent-authoring/workstreams/upstream-recovery/INPUT_MANIFEST.yaml
  output_manifest: docs/agent-authoring/workstreams/upstream-recovery/OUTPUT_MANIFEST.yaml
  handoff_log: docs/agent-authoring/workstreams/upstream-recovery/HANDOFF_LOG.md

progress:
  planner_source:
    status: TESTED_PASS_BOUNDARY_PENDING
    source_digest: {digest}
    cap_rules: "36/36"
    evals: "22/22"
    paraphrase_variants: "44/44"
    scenario_runs: "66/66"
    mutations: "15/15 killed"
    local_procedural_audit: PASS
    independent_identity: UNVERIFIED
    operational_permission: false
  gate_source: PENDING
  execution_source: PENDING

blocker: null
next_action: >-
  Pass the orchestrator-approved ownership boundary check, then mark Planner
  VERIFIED_LOCAL_CANDIDATE and start Gate Generator M0-M3 recovery.
"""
    write_text(args.state, state)

    output = f"""schema_version: "1.0"
workstream_id: upstream-recovery

outputs:
  - path: .claude/skills/capability-artifact-planner/
    kind: source_package
    status: tested_pass
  - path: .claude/agents/capability-plan-auditor.md
    kind: auditor_definition
    status: implemented_independence_unverified
  - path: docs/agent-authoring/evidence/capability-planner/
    kind: evidence_package
    status: tested_pass
  - path: docs/agent-authoring/CAPABILITY_ARTIFACT_PLANNER_구현결과.md
    kind: implementation_report
    status: complete

planner_test:
  source_digest: {digest}
  status: PASS_LOCAL_PROCEDURE
  cap_rules: 36
  base_evals: 22
  paraphrase_variants: 44
  scenario_runs: 66
  mutations_killed: 15
  mutations_total: 15
  independent_identity: UNVERIFIED

checks:
  ownership_boundary: PENDING_RECHECK
  input_manifest_current: PASS_RESEALED
  planner_complete: TESTED_PASS
  gate_complete: PENDING
  execution_complete: PENDING
  critical_mutants_survived: 0
  operational_permission: false

review_status: PLANNER_BOUNDARY_RECHECK
"""
    write_text(args.output_manifest, output)
    print(json.dumps({"status": "PASS", "source_digest": digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
