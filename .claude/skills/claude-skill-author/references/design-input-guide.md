# 설계 입력 가이드

## 추적 사슬

```text
SOURCE_REQUEST.md
→ SOURCE_DECISIONS.md
→ REQUIREMENT_INTAKE.yaml
→ DESIGN.md
→ DESIGN_REQUIREMENTS.yaml
→ DESIGN_AUDIT_REPORT.md + DESIGN_AUDIT_ATTESTATION.yaml
→ COMMAND_SPEC.yaml
→ SKILL.md / optional Agent.md
```

## DESIGN.md

`DESIGN_INPUT.template.md`의 표준 20개 섹션을 정확히 한 번씩 순서대로 작성한다. 빈 섹션을 두지 않는다.

- 해당 사항 없음: `없음 — <구체적인 이유>`
- 확인 불가: `미확인 — <필요한 출처 또는 행동>`
- 사용자 결정 필요: `미결정 — <질문과 영향>`

각 절차 단계에는 가능한 경우 입력·행동·산출물·검증·실패 처리를 둔다.

## REQUIREMENT_INTAKE.yaml

각 요구사항 예:

```json
{
  "id": "REQ-001",
  "type": "USER_EXPLICIT",
  "text": "코드 리뷰 중 파일을 수정하지 않는다.",
  "status": "RESOLVED",
  "blocking": true,
  "sources": [
    {"path": ".claude/skill-authoring/review/SOURCE_REQUEST.md", "anchor": "코드 리뷰 중 파일을 수정하지"}
  ],
  "design_links": ["## 11. 금지 행동"]
}
```

승인 조건:

- `USER_EXPLICIT` 요구사항 1개 이상
- 고유 `REQ-###` ID
- 모든 차단 요구와 질문 `RESOLVED`
- 모든 요구사항에 실제 근거
- 해결 요구사항마다 DESIGN 반영 위치
- 전체 상태 `APPROVED`

## DESIGN_REQUIREMENTS.yaml

18개 필수 의미 항목을 `RESOLVED`로 채우고 각 항목에 원문·결정·설계서·저장소 근거를 기록한다. DESIGN.md의 20개 섹션과 18개 의미 항목은 목적이 다르다.

- 20개 섹션: 사람이 읽는 설계 구조
- 18개 의미 항목: 검사기가 확인하는 실행 계약 입력

## 설계 감사와 digest

설계 감사자는 파일을 수정하지 않는다. PASS 보고서를 받은 뒤 `seal_attestation.py --kind design`으로 현재 원문·결정·intake·설계서·설계 요구사항 digest를 묶는다. 이후 입력이 바뀌면 기존 PASS는 재사용할 수 없다.
