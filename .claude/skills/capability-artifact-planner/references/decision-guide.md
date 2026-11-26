# Capability Planner 결정 가이드

## 기본 상승 순서

```text
Prompt only 또는 결정적 Code
→ Skill / Reference / Script / Tool
→ deterministic Workflow 또는 bounded single Agent
→ Multi-agent
```

중간 단계를 건너뛰려면 정책·위험·규모·기준선 실패의 구체적 증거가 필요하다.

## Control mode

### `direct_response`

현재 문맥만으로 완료되고 외부 행동·장기 상태·동적 도구 선택이 없다.

### `deterministic_workflow`

코드가 단계·분기·재시도·승인·종료를 소유한다. LLM은 제한된 의미 판단 노드일 수 있다.

### `bounded_agent`

환경 피드백에 따라 다음 단계나 도구를 동적으로 선택해야 하며, turn·tool·time budget과 종료·trace가 있다.

### `multi_agent`

다음 중 하나가 실제로 필요하다.

- context isolation
- independent parallelism
- authority separation
- proven specialization
- single-agent eval failure

역할 이름이 여러 개라는 것은 근거가 아니다.

## Knowledge 선택

```text
지식 불필요
→ current context
→ static reference/direct document
→ lexical/structured retrieval
→ RAG
→ live Tool/API
```

실시간 운영 상태는 문서 RAG보다 live system of record를 우선한다.

## Code 선택

다음은 Script·Validator·Workflow 후보다.

- 같은 입력에서 재현 가능한 결과
- 대량 반복 변환
- 객관적 schema·정책 검사
- 고정 dry-run·reconciliation
- 모델이 같은 보조 코드를 반복 생성

의미 판단과 정책 결정은 결정적 코드로 위장하지 않는다.

## Agent 상승 반례

다음은 Agent 필요성 증거가 아니다.

- 작업이 중요함
- 향후 복잡해질 수 있음
- writer/reviewer/manager라는 역할 이름을 붙일 수 있음
- LLM 호출이 포함됨
- 도구가 많지만 중복 정리를 하지 않음

## 안전 override

단순성보다 다음이 우선한다.

- 비가역·고영향 write
- secret·credential
- 비신뢰 코드 실행
- 장기 상태
- tenant별 접근권한
- 의료·채용·신용·법률 등 고영향 결정

이 경우 approval·least privilege·validator·sandbox·audit·lifecycle을 강제하며, 환경이 없으면 차단한다.
