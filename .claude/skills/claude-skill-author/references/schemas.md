# 작성 증거 스키마 v1.3

모든 `.yaml` 파일은 Python 표준 라이브러리로 검증할 수 있도록 JSON 호환 YAML, 즉 유효한 JSON 문법으로 저장한다.

## SOURCE_REQUEST.md

최초 사용자 자연어의 불변 원형이다. 생성 후 수정하지 않는다. `AUTHORING_STATE.yaml.source_request_lock`에 경로·SHA-256·잠금 시각을 기록한다.

## SOURCE_DECISIONS.md

최초 요청 이후의 사용자 답변·변경 결정을 시간순으로 추가한다. 기존 기록을 덮어쓰지 않는다. 변경 시 design 이후 단계는 stale 처리한다.

## REQUIREMENT_INTAKE.yaml

```json
{
  "schema_version": "1.3",
  "target_skill": "example",
  "source_request_documents": [{"path": ".../SOURCE_REQUEST.md", "sha256": "...", "type": "source_request"}],
  "decision_documents": [{"path": ".../SOURCE_DECISIONS.md", "sha256": "...", "type": "source_decision"}],
  "requirements": [
    {
      "id": "REQ-001",
      "type": "USER_EXPLICIT",
      "text": "파일을 수정하지 않는다.",
      "status": "RESOLVED",
      "blocking": true,
      "sources": [{"path": ".claude/skill-authoring/example/SOURCE_REQUEST.md", "anchor": "파일을 수정하지"}],
      "design_links": ["## 11. 금지 행동"]
    }
  ],
  "open_questions": [],
  "summary": {},
  "status": "APPROVED"
}
```

가능한 `type`:

- `USER_EXPLICIT`
- `USER_DECISION`
- `REPOSITORY_FACT`
- `SAFE_DEFAULT`
- `PROPOSAL`
- `NON_BLOCKING_UNCERTAINTY`

## DESIGN_REQUIREMENTS.yaml

```json
{
  "schema_version": "1.3",
  "target_skill": "example",
  "primary_design_document": "docs/skill-designs/example/DESIGN.md",
  "source_documents": [{"path": "...", "sha256": "...", "type": "design"}],
  "source_request_documents": [{"path": "...", "sha256": "...", "type": "source_request"}],
  "decision_documents": [{"path": "...", "sha256": "...", "type": "source_decision"}],
  "requirement_intake_document": ".claude/skill-authoring/example/REQUIREMENT_INTAKE.yaml",
  "requirements": {},
  "decision_register": {},
  "open_questions": [],
  "status": "APPROVED"
}
```

필수 의미 항목은 `purpose`, `user_outcome`, `use_when`, `do_not_use_when`, `invocation_examples`, `inputs_and_defaults`, `trusted_and_untrusted_sources`, `scope_include`, `scope_exclude`, `scope_conditional`, `permissions_allow`, `permissions_deny`, `approval_required`, `workflow`, `outputs`, `validation`, `failure_handling`, `completion_conditions`다.

## DESIGN_AUDIT_ATTESTATION.yaml

독립 설계 감사 PASS를 정확한 입력 digest에 묶는다.

```json
{
  "schema_version": "1.3",
  "target_skill": "example",
  "audit_kind": "design",
  "auditor_role": "skill-design-auditor",
  "verdict": "PASS",
  "inputs": [{"path": "...", "sha256": "...", "role": "source-request", "kind": "file"}],
  "input_fingerprint": "...",
  "report": {"path": ".../DESIGN_AUDIT_REPORT.md", "sha256": "...", "role": "audit-report", "kind": "file"},
  "attested_at": "..."
}
```

## RULE_MANIFEST.yaml / RULE_COVERAGE.yaml

원문 규칙에서 manifest를 자동 생성한다. Coverage는 각 규칙을 `APPLY`, `TRANSFORM`, `EXCLUDE`, `EXTERNAL` 중 하나로 판정한다.

## COMMAND_SPEC.yaml

필수 최상위 필드:

- `target_skill`, `artifact_type`, `operation`, `purpose`, `user_outcome`
- `primary_stage`, `secondary_stages`
- `invocation`, `inputs`, `scope`, `side_effect_level`, `permissions`
- `execution`, `outputs`, `validation`, `failure_handling`
- `completion_conditions`, `agent_requirement`, `status`

`inputs`에는 승인된 design, source request, decision, requirement intake 경로가 모두 포함돼야 한다.

## AUTHORING_STATE.yaml

```json
{
  "schema_version": "1.3",
  "target_skill": "example",
  "mode": "full",
  "source_request_lock": {"path": "...", "sha256": "...", "locked_at": "..."},
  "phases": {
    "design": {"status": "PASS", "fingerprint": "..."},
    "spec": {"status": "PASS", "fingerprint": "..."},
    "build": {"status": "PASS", "fingerprint": "..."},
    "audit": {"status": "PASS", "fingerprint": "..."}
  }
}
```

상위 입력이 바뀌면 뒤 단계는 `STALE`이 되며 이전 PASS를 재사용할 수 없다.

## AUDIT_ATTESTATION.yaml

최종 감사 PASS를 명세·규칙·런타임 파일·build 검증 digest에 묶는다. `AUDIT_REPORT.md`만 수정하거나 옛 PASS 보고서를 복사하면 audit 검증이 실패해야 한다.

## FINAL_STATUS.json

모든 단계가 현재 fingerprint로 PASS일 때만 생성한다. 네 단계 fingerprint와 validation 파일 목록을 포함한다.
