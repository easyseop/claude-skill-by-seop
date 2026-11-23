---
name: execution-artifact-generator
description: Planner와 Gate가 승인한 실행 구성요소만 재사용하거나 안전한 로컬 artifact 후보로 생성·검증한다.
---

# Execution Artifact Generator

## 책임

- 실행 artifact 필요 여부를 먼저 판정한다.
- 기존 Script·CLI·SDK·Tool·MCP·표준 라이브러리를 우선 조사한다.
- 승인된 `EXECUTION_CONTRACT`에서만 source를 생성한다.
- no-code, direct reuse, Python local static candidate, Java contract-only를 구분한다.
- source·test·Gate·evidence의 정·역방향 trace를 검증한다.

## 고정 절차

1. current Planner·Gate digest와 상태를 검증한다.
2. 봉인된 `EXEC-01~30`, `EXI-001~45`, `EXEVAL-001~26`, `EXMUT-001~10`을 materialize한다.
3. bounded repository inventory와 reuse assessment를 만든다. 후보는 실행하지 않는다.
4. `execution_required`를 먼저 판정한다.
5. I/O·effect·error·retry·idempotency·reconciliation·Gate·test 계약을 source보다 먼저 검사한다.
6. `NOT_REQUIRED`와 `REUSE_DIRECT`이면 새 implementation을 만들지 않는다.
7. `python_local`은 local-pure static candidate만 생성한다. 검증된 runner가 없으면 동적 실행을 하지 않는다.
8. `java_cli`는 검증된 기존 boundary를 재사용하거나 contract-only 상태로 남긴다.
9. invariant 45개, eval 26개, mutation 10개, Planner golden 22개, builder 반례 16개 이상을 실행한다.
10. procedural audit와 Stop gate를 기록하고 evidence를 current source digest에 결박한다.

## 검증 수량

```text
EXEC 30/30
EXI 45/45
EXEVAL 26/26
EXMUT 10/10 killed
Planner execution golden 22/22
Builder negative tests >=16
```

위 수량은 등록된 `Workstream Boundary Check`의 Execution job에서 격리 실행하고 현재 source digest에 결박한다.

## 안전 경계

```text
READY_FOR_ASSEMBLY
= contract-bound local artifact package에만 사용 가능

HARD_ENFORCEMENT_UNAVAILABLE
= verified sandbox/runner, 실제 외부 write, durable runtime, production release가 없음
```

- exit 0은 결과가 방출됐다는 뜻이며 PASS가 아니다.
- `OUTCOME_UNKNOWN`은 reconciliation 전 재시도하지 않는다.
- unsupported runtime을 Python으로 대체하지 않는다.
- 생성 코드는 비신뢰 draft로 취급한다.
- 별도 감사 identity가 없으면 `UNVERIFIED`다.

## 금지

- Planner component/control mode 변경
- Gate 완화
- contract PASS 전 source 생성
- shell string·raw SQL·secret 값·floating dependency
- `.claude/settings.json` 수정
- production write·배포·자동 병합
