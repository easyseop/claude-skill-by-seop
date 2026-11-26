---
name: gate-generator
description: 승인된 Capability Plan을 단계별 Gate 계약, 결정적 검사, 로컬 Hook adapter, 평가·mutation·evidence로 변환한다.
---

# Gate Generator

## 사용 조건

Capability Planner가 `CAPABILITY_PLAN`과 downstream `GATE_CONTRACT` 요구를 승인했고, 위험·권한·부작용·합격 기준을 실제 차단 규칙으로 변환해야 할 때 사용한다.

## 사용하지 않는 조건

- Planner의 control mode나 component set을 새로 결정할 때
- 실제 production IAM·DB 권한·Hook 설정을 활성화할 때
- M4 exact approval, M5 durable state, M6 tenant RAG, M7 production release를 구현할 때
- Prompt 문장만으로 hard enforcement를 대체할 때

## 고정 절차

1. 상위 Planner source·evidence digest와 현재 상태를 확인한다.
2. 봉인된 `GATE-01~80`, `I-001~85`, `GEVAL-001~48` catalog를 materialize한다.
3. `GATE_CONTRACT`를 생성하고 acceptance criterion·risk·side effect를 Gate에 양방향 연결한다.
4. 결정적 checker로 schema, digest, permission, approval, Hook, retry, RAG, state, result binding을 검사한다.
5. PreToolUse·PostToolUse·Stop adapter를 로컬 candidate로 검증한다.
6. Planner golden 22개, GEVAL 48개, mutation 20개, Hook smoke 19개를 실행한다.
7. traceability와 stale propagation을 검사한다.
8. read-only blind-first 감사 절차를 기록한다. 별도 identity가 실제 실행되지 않으면 `UNVERIFIED`다.
9. 구조화 evidence와 source digest를 결박한다.
10. `PASS_LOCAL_PROCEDURE`까지만 허용한다. Host enforcement가 없으면 운영 권한은 false다.

## 검증 수량

```text
GATE 80/80
I 85/85
Planner golden 22/22
GEVAL 48/48
GMUT 20/20 killed
Hook smoke 19/19
```

위 수량은 현재 source와 구조화 evidence에 결박되어야 하며, 하나라도 누락되면 Gate 단계는 완료되지 않는다. 검증은 등록된 `Workstream Boundary Check`의 Gate job에서 격리 실행한다.

## 상태 경계

```text
PASS_LOCAL_PROCEDURE
= M0~M3 로컬 계약·checker·adapter·평가가 current source에 대해 검증됨

HARD_ENFORCEMENT_UNAVAILABLE
= 실제 Host Hook, trusted approval, tenant IAM, production release가 없음
```

자유문자 `PASS`, exit code 0, 파일 존재는 완료 증거가 아니다.

## 금지

- `.claude/settings.json` 자동 수정
- main 직접 수정·자동 병합
- 검증되지 않은 runtime을 활성화했다고 주장
- ERROR·STALE·WAIVED·OUTCOME_UNKNOWN을 PASS로 승격
- 생성자와 같은 실행을 독립 감사라고 주장
