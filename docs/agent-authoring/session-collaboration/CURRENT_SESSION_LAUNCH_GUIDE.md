# 현재 세션 실행 안내

## 1. 구현 세션

저장소:

```text
easyseop/claude-skill-by-seop
```

브랜치:

```text
recovery/upstream-builders
```

구현 세션에 전달할 문장:

```text
현재 저장소와 브랜치를 확인한 뒤
`docs/agent-authoring/workstreams/upstream-recovery/SESSION_START_PROMPT.md`를
최상위 시작 지시로 읽고 그대로 수행해.

`OWNERSHIP.yaml`에 선언된 담당 경로 밖은 수정하지 말고,
Planner → Gate → Execution 순서를 바꾸지 마.
main 수정, 브랜치 전환, force push, 자동 병합은 하지 마.
```

공식 작업판: Draft PR #4

현재 Knowledge/RAG PR #1은 `BLOCKED_FOR_SOURCE`이며, 복구 workstream이 검토 통과할 때까지 작업하지 않는다.

## 2. 조사 세션

저장소:

```text
easyseop/claude-skill-by-seop
```

브랜치:

```text
research/agent-workflow-assembler
```

조사 세션에 전달할 문장:

```text
현재 저장소와 브랜치를 확인한 뒤
`docs/agent-authoring/workstreams/agent-workflow-assembler-research/SESSION_START_PROMPT.md`를
최상위 시작 지시로 읽고 그대로 수행해.

`OWNERSHIP.yaml`에 선언된 조사 결과·상태·로그 경로만 수정하고,
코드·설정·evidence·다른 workstream은 건드리지 마.
main 수정, 브랜치 전환, force push, 자동 병합은 하지 마.
```

공식 작업판: Draft PR #2

## 3. 공통 규칙

- 한 세션은 한 active workstream만 담당한다.
- 시작 프롬프트·Work Order·입력은 총괄 세션이 브랜치에 미리 배치한다.
- 준비된 입력은 blob digest로 봉인된다.
- 담당 경로 밖 변경은 GitHub `Workstream Boundary Check`에서 실패한다.
- 세션 간 공식 통신은 상태 파일·인수인계 로그·Draft PR로 한다.
- 자동 병합하지 않는다.
