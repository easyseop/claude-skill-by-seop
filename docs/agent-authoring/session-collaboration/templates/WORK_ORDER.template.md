# <WORKSTREAM_TITLE> Work Order

## 0. 목적

<정확한 작업 목적과 완료 범위>

## 1. 수행 주체

- session_type: `<research|implementation|review>`
- owner_role: `<role>`
- branch: `<branch>`
- draft_pr: `<number-or-pending>`

## 2. 입력 정본

`INPUT_MANIFEST.yaml`에 등록된 입력만 공식 입력으로 사용한다. 누락·digest 불일치 시 `BLOCKED_FOR_SOURCE`로 중단한다.

## 3. 수행 범위

- <scope item>

## 4. 비범위·금지

- <out-of-scope item>
- main 직접 수정
- 자동 병합·force push
- 다른 workstream writable path 수정
- 미실행 테스트·감사를 PASS로 기록

## 5. 산출물

- <required output path>

## 6. 검증 기준

- <machine-checkable criterion>

## 7. 상태 전이

```text
READY_FOR_SESSION
→ IN_PROGRESS
→ BLOCKED_FOR_SOURCE | BLOCKED_FOR_DECISION | READY_FOR_REVIEW
```

## 8. 인수인계

작업 시작·blocker·검토 요청 시 `CURRENT_SESSION_STATE.yaml`과 `HANDOFF_LOG.md`를 갱신한다.
