# 작성 증거 스키마

모든 `.yaml` 파일은 Python 표준 라이브러리만으로 검증할 수 있도록 **JSON 호환 YAML**, 즉 유효한 JSON 문법으로 저장한다. JSON은 YAML 1.2의 부분집합이다.


## DESIGN_REQUIREMENTS.yaml

설계서·현재 호출문·저장소 사실에서 추출한 요구사항을 구조화한다. `COMMAND_SPEC.yaml`보다 먼저 승인한다.

```json
{
  "schema_version": "1.0",
  "target_skill": "example",
  "source_documents": [
    {"path": "docs/example.md", "sha256": "..."}
  ],
  "requirements": {
    "purpose": {
      "status": "RESOLVED",
      "value": "구현 전 검증 가능한 계획을 작성한다.",
      "sources": ["docs/example.md#목적"]
    },
    "use_when": {
      "status": "RESOLVED",
      "items": ["다중 파일 변경 계획 요청"],
      "sources": ["docs/example.md#사용-시점"]
    }
  },
  "open_questions": [],
  "status": "APPROVED"
}
```

필수 의미 항목은 `purpose`, `user_outcome`, `use_when`, `do_not_use_when`, `invocation_examples`, `inputs_and_defaults`, `trusted_and_untrusted_sources`, `scope_include`, `scope_exclude`, `scope_conditional`, `permissions_allow`, `permissions_deny`, `approval_required`, `workflow`, `outputs`, `validation`, `failure_handling`, `completion_conditions`다.

각 항목은 다음 조건을 만족해야 한다.

- `status: RESOLVED`
- 비어 있지 않은 `value` 또는 `items`
- 하나 이상의 `sources`
- 해당 사항이 없으면 `없음 — <이유>`를 명시

모든 필수 항목이 해결된 경우에만 최상위 `status`를 `APPROVED`로 둔다.

## RULE_MANIFEST.yaml

원문에서 자동 생성한다. 직접 수정하지 않는다.

핵심 필드:

```json
{
  "schema_version": "1.0",
  "source_documents": [],
  "counts": {
    "rules": 0,
    "anti_patterns": 0,
    "stage_modules": 0
  },
  "rules": [],
  "anti_patterns": [],
  "stage_modules": {}
}
```

각 규칙은 `id`, `title`, `category`, `source_file`, `start_line`, `end_line`, `text`를 가진다.

## RULE_COVERAGE.yaml

```json
{
  "target_skill": "example",
  "rules": {
    "C-01": {
      "status": "UNCLASSIFIED",
      "rationale": "",
      "planned_locations": [],
      "targets": [],
      "external_controls": []
    }
  },
  "anti_patterns": {
    "A-01": {
      "status": "UNCHECKED",
      "evidence": ""
    }
  },
  "stage_modules": {
    "primary": "",
    "secondary": [],
    "applied": {}
  }
}
```

최종 `targets` 형식:

```json
{
  "file": "SKILL.md",
  "contains": "검증이 통과한 경우에만 완료로 판정한다."
}
```

외부 통제 형식:

```json
{
  "type": "hook",
  "path": ".claude/settings.json",
  "state": "implemented",
  "required_for_pass": true,
  "description": "배포 명령 전 승인 토큰을 검사한다."
}
```

## COMMAND_SPEC.yaml

필수 최상위 필드:

- `target_skill`
- `artifact_type`
- `operation`
- `purpose`
- `user_outcome`
- `primary_stage`
- `secondary_stages`
- `invocation`
- `inputs`
- `scope`
- `side_effect_level`
- `permissions`
- `execution`
- `outputs`
- `validation`
- `failure_handling`
- `completion_conditions`
- `status`

`status`는 명세 검토 후 `APPROVED`로 바꾼다.

## 감사 판정

`AUDIT_REPORT.md`에는 다음 줄이 정확히 하나 있어야 한다.

```text
- 판정: PASS
```

가능한 값은 `PASS`, `CONDITIONAL`, `FAIL`이다.
