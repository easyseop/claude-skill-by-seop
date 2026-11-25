# 세션 간 협업 운영 규약

## 1. 목적

총괄·조사·구현·검토 세션은 서로의 비공개 대화를 직접 읽거나 보이지 않는 메시지를 주고받는다고 가정하지 않는다. GitHub 브랜치, Draft PR, 상태 파일, 인수인계 로그를 공식 통신 수단으로 사용한다.

## 2. Workstream 기본 단위

각 workstream은 반드시 다음을 가진다.

```text
전용 브랜치
Draft PR
SESSION_START_PROMPT.md
WORK_ORDER.md
CURRENT_SESSION_STATE.yaml
HANDOFF_LOG.md
INPUT_MANIFEST.yaml
OUTPUT_MANIFEST.yaml
OWNERSHIP.yaml
```

브랜치 예:

```text
research/agent-workflow-assembler
implementation/knowledge-rag-builder-k0-k6
recovery/upstream-builders
review/knowledge-rag-builder-k0-k6
```

## 3. 지시 우선순위

1. 사용자 최신 지시
2. 저장소와 작업 경로의 `AGENTS.md`
3. 해당 workstream의 `SESSION_START_PROMPT.md`
4. `WORK_ORDER.md`
5. `OWNERSHIP.yaml`
6. `CURRENT_SESSION_STATE.yaml`
7. `HANDOFF_LOG.md`
8. `INPUT_MANIFEST.yaml`에 등록된 입력
9. 기타 참고 문서

실제 source·test·구조화 evidence가 Markdown의 PASS 문장보다 우선한다.

## 4. 역할

### 4.1 총괄 세션

- 전용 브랜치와 Draft PR 생성
- 필요한 입력자료를 브랜치에 먼저 배치하고 digest 기록
- 시작 프롬프트·Work Order·상태·인수인계 파일 생성
- dependency와 일정 관리
- 상태 감시, blocker 결정, 결과 검토
- 통과·수정·재진입 판정
- 사용자 승인 없는 병합·자동 병합 금지

### 4.2 조사 세션

- 승인된 입력과 외부 1차 자료만 근거로 조사
- 공식 규격·공식 제품 문서·공식 저장소·원 논문 우선
- 현재 기능·연구 결과·설계 제안 구분
- 규칙·불변식·평가·mutation을 연속 ID로 작성
- 코드·설정·운영 리소스 변경 금지
- 결과·출처·미확인 사항을 지정 출력 경로에 기록
- `OWNERSHIP.yaml`의 writable path 밖을 수정하지 않음

### 4.3 구현 세션

- 승인된 조사·계약만 구현
- 상위 Planner·Gate·Execution·Knowledge 계약의 조용한 변경 금지
- source·test·evidence 생성 및 실제 재실행
- 범위 밖 기능은 `BLOCKED`, `UNSUPPORTED`, `HARD_ENFORCEMENT_UNAVAILABLE`로 유지
- 미실행 테스트·감사를 PASS로 기록 금지
- `OWNERSHIP.yaml`의 writable path 밖을 수정하지 않음

### 4.4 검토 세션

- source·diff·evidence·digest를 독립 검토
- 결과 보고서 문장보다 실제 실행 결과 우선
- `VERIFIED_RESEARCH`, `VERIFIED_LOCAL`, `CHANGES_REQUESTED`, `REENTRY_REQUIRED` 중 하나로 판정
- 사용자 승인 없는 병합 금지

## 5. 상태 모델

허용 상태:

```text
READY_FOR_SESSION
IN_PROGRESS
BLOCKED_FOR_SOURCE
BLOCKED_FOR_DECISION
READY_FOR_REVIEW
REVIEW_IN_PROGRESS
CHANGES_REQUESTED
VERIFIED_RESEARCH
VERIFIED_LOCAL
REENTRY_REQUIRED
DONE
```

전이:

```text
READY_FOR_SESSION
  -> IN_PROGRESS
  -> BLOCKED_FOR_SOURCE | BLOCKED_FOR_DECISION | READY_FOR_REVIEW

READY_FOR_REVIEW
  -> REVIEW_IN_PROGRESS
  -> CHANGES_REQUESTED | VERIFIED_RESEARCH | VERIFIED_LOCAL | REENTRY_REQUIRED

CHANGES_REQUESTED
  -> IN_PROGRESS
```

`VERIFIED_LOCAL`은 local contract-bound candidate 판정이며 production 승인과 동일하지 않다.

## 6. 작업 경계

각 workstream의 `OWNERSHIP.yaml`은 다음을 선언한다.

```yaml
workstream_id:
branch:
owner_role:
writable_paths: []
read_only_paths: []
forbidden_paths: []
shared_files:
  orchestrator_only: []
```

규칙:

- `writable_paths` 밖 변경은 기본 실패다.
- `read_only_paths`는 읽을 수 있지만 수정할 수 없다.
- `forbidden_paths`는 읽기·수정 모두 금지할 수 있다.
- `shared_files.orchestrator_only`는 총괄 세션만 수정한다.
- 예상 밖 변경은 완료 전에 제거하거나 `BLOCKED_FOR_DECISION`으로 전환한다.
- 다른 workstream의 브랜치·PR·상태 파일을 수정하지 않는다.

## 7. 파일 업로드와 입력 고정

총괄 세션은 시작 전에 필요한 파일을 workstream 브랜치에 올린다. 세션은 대화 첨부파일이나 임시 `/mnt/data`를 장기 정본으로 사용하지 않는다.

`INPUT_MANIFEST.yaml`에는 최소 다음을 기록한다.

```yaml
inputs:
  - id:
    path:
    sha256:
    role: source_of_truth | required_context | optional_reference
    mutable: false
```

입력 파일이 없거나 digest가 다르면 `BLOCKED_FOR_SOURCE`다. 다른 문서로 임의 대체하지 않는다.

## 8. 출력과 완료 증거

`OUTPUT_MANIFEST.yaml`에는 생성 파일, 테스트, evidence, digest, 미검증 범위를 기록한다.

```yaml
outputs:
  - path:
    sha256:
    kind: source | test | evidence | report
    status: generated | tested | audited | unverified
```

자유문자 PASS, exit code 0, 파일 존재만으로 완료하지 않는다.

## 9. 인수인계 규약

`HANDOFF_LOG.md`는 append-only다.

필수 항목:

```text
시각·작성 주체
상태
기준 commit
수행 내용
실행한 검증과 결과
blocker 또는 결정
다음 행동
```

기존 기록을 삭제·수정하지 않는다. 오류 정정은 새 항목으로 추가한다.

## 10. 일정과 dependency

총괄 세션은 `MASTER_WORKSTREAM_BOARD.yaml`에서 dependency를 관리한다.

- `ready`: 선행 입력과 브랜치가 준비됨
- `blocked`: dependency 또는 사용자 결정 대기
- `active`: 담당 세션이 작업 중
- `review`: 총괄 검토 중
- `verified`: 다음 단계에서 소비 가능

선행 workstream이 `verified`가 아니면 downstream 구현은 시작하지 않는다. 독립 조사처럼 구현 source가 불필요한 작업은 병렬 실행할 수 있다.

## 11. 병합 정책

- 모든 PR은 Draft로 시작한다.
- 세션은 자기 PR만 갱신한다.
- 자동 병합 금지.
- 총괄 검토 통과와 사용자 명시 승인 후에만 병합한다.
- main 직접 변경, force push, history rewrite 금지.
