# Assembler 조사용 상위 계약 요약

이 문서는 Agent & Workflow Assembler 조사에 필요한 승인된 상위 원칙과 현재 구현 상태를 요약한다. 상세 사실을 새로 단정하지 않으며, 실제 구현이 없는 항목은 구현된 것으로 취급하지 않는다.

## 1. 전체 목표

사용자의 자연어 요구를 다음과 같이 변환하는 검증형 Agent System Factory를 구축한다.

```text
요구사항
→ 필요한 구성 판정
→ hard Gate 설계
→ 필요한 실행 artifact 생성
→ 필요한 Knowledge/RAG 구조 생성
→ Skill·Agent·Workflow 조립
→ 독립 평가
```

모든 downstream 생성기를 무조건 실행하지 않는다. Planner가 선택한 구성만 생성한다.

## 2. Capability & Artifact Planner

### 책임

- 자연어 목표를 원자 Capability로 분해
- `control_mode`와 `selected_components`를 분리
- 가장 단순한 기준선 우선
- Skill·Reference·Script·Validator·Tool·RAG·Agent·Workflow·Approval·Permission·Hook·Sandbox·Eval 가운데 최소 구성 선택
- 선택·기각 근거, acceptance criteria, 위험, 재검토 조건 기록

### 제어 모드

```text
direct_response
deterministic_workflow
bounded_agent
multi_agent
```

`Hybrid`는 독립 제어 모드가 아니라 선택된 조합의 설명 레이블이다.

### 핵심 경계

- 결정 가능한 부분은 Code·Validator·Workflow에 우선 배치
- 작은 안정 자료는 Reference, 최신 원장 값은 live Tool/API, 질의별 대규모·변경·ACL 자료는 증거가 있을 때만 RAG
- 단일 Agent를 먼저 평가하고 격리·병렬·권한 분리·실증된 전문화가 있을 때만 Multi-agent
- 고위험 쓰기·비밀·비신뢰 코드·장기 상태에는 하드 통제 필수
- 모든 acceptance criterion은 Gate 또는 Eval에 연결

### 정본

```text
CAPABILITY_PLAN.yaml
```

Assembler는 Planner의 control mode와 selected components를 조용히 변경하지 않는다.

## 3. Gate Generator

### 책임

Planner의 위험·권한·합격 기준을 단계별 Gate 계약과 결정적 검사로 변환한다.

```text
Intake
Design
Pre-execution
Runtime
Post-execution
Release
Long-running state
```

### 핵심 원칙

- 자유문자 PASS 금지
- PASS는 subject·policy·checker·input·trace·time·evidence digest에 결박
- Prompt·Skill은 hard enforcement가 아님
- Permission·Hook·Sandbox·Approval·CI·IAM이 실제 차단 담당
- high-risk Gate 오류는 fail-closed
- exact payload approval
- write timeout은 `OUTCOME_UNKNOWN` 가능
- retry 전 reconciliation
- Agent·Workflow·RAG 완료 Gate를 구분
- 계약↔구현↔테스트↔증거 양방향 추적

### 현재 구현 경계

과거 결과 보고 기준 M0~M3 local package는 구현됐다고 보고되었으나, 현재 공식 저장소에는 source와 evidence가 없어 복구 workstream이 필요하다.

실제 Host Hook 활성화, M4 exact approval, 운영 쓰기, durable state, tenant RAG, production Release는 승인된 적이 없다.

## 4. Execution Artifact Generator

### 책임

- 실행 artifact 필요 여부 판정
- 기존 Script·CLI·SDK·Tool·MCP 재사용 우선
- Contract Compiler와 Artifact Builder 분리
- no-code, direct reuse, thin adapter, new artifact 구분
- runtime·I/O·오류·exit·dry-run·idempotency·retry·reconciliation 계약
- Gate→artifact→source→test→evidence 추적

### 주요 상태

```text
NOT_REQUIRED
REUSE_READY
PLANNED
SCAFFOLDED
GENERATED
STATIC_CHECKED
TESTED
AUDITED
READY_FOR_ASSEMBLY
BLOCKED
HARD_ENFORCEMENT_UNAVAILABLE
UNSUPPORTED_RUNTIME_PACK
```

### 현재 구현 경계

과거 결과 보고 기준 E0~E4 local package가 구현됐다고 보고되었으나, 현재 공식 저장소에는 source와 evidence가 없어 복구 workstream이 필요하다.

verified sandbox, 실제 외부 write, durable workflow, production release는 승인되지 않았다.

## 5. Knowledge & RAG Builder

### 책임

지식이 있다는 이유만으로 RAG를 만들지 않고 최소 구조를 선택한다.

```text
no knowledge
current context
static reference
direct document
file/lexical search
structured query
vector
hybrid/rerank
graph/multi-hop
live Tool/API
long-term memory
bounded agentic retrieval
```

### 핵심 원칙

- source authority와 retrieval rank 분리
- 검색 전 ACL
- source/index/cache freshness 분리
- 삭제·정정·권한 철회를 1급 이벤트로 처리
- retrieved content는 data이며 실행 권한이 아님
- retrieval·generation·citation·security·freshness 평가 분리
- no-evidence abstention
- claim-level citation과 exact source span

### 현재 상태

심층조사와 조건부 평가는 완료됐다. K0~K6 실제 구현은 `codex/knowledge-rag-builder-k0-k6` workstream에서 진행하려 했으나 Planner·Gate·Execution source/evidence 부재로 K0에서 blocked 상태다.

Assembler 조사에서는 Knowledge Builder가 이미 구현됐다고 단정하지 않는다. 조사 계약과 제한만 사용한다.

## 6. claude-skill-author

### 책임

Planner가 Skill을 선택했을 때만 개별 Claude Skill을 고신뢰 방식으로 작성한다.

```text
자연어 원문 보존
→ 요구사항·설계
→ 규칙 전수 판정
→ spec
→ SKILL.md·references·scripts
→ build 검사
→ 독립 감사
```

Skill은 절차·지식·출력 규칙을 제공하지만 Permission·Hook·Sandbox·IAM을 대체하지 않는다.

Assembler는 Skill이 선택되지 않은 요청에서 `claude-skill-author`를 호출하지 않는다.

## 7. Assembler가 지켜야 할 상위 불변식

1. 상위 계약에 없는 component를 추가하지 않는다.
2. component 누락이나 계약 충돌을 조용히 patch하지 않고 재진입 상태로 반환한다.
3. Skill·Agent·Workflow가 같은 책임을 중복하지 않는다.
4. 제어권 소유자를 하나로 명확히 한다.
5. component PASS를 system PASS로 단순 합산하지 않는다.
6. current digest·상태·Gate·evidence를 결박한다.
7. actual runtime enforcement가 없으면 production ready를 주장하지 않는다.
8. context isolation과 evidence provenance를 함께 유지한다.
9. identity·tenant·approval·permission ceiling을 handoff마다 재검사한다.
10. local package assembly와 production release를 구분한다.

## 8. 현재 조사에서 미구현으로 취급할 항목

- 복구되지 않은 Planner·Gate·Execution actual source/evidence
- Knowledge K0~K6 actual source/evidence
- production IAM·tenant ACL·RLS/DLS
- verified sandbox·network/process isolation
- exact approval service·JIT privilege broker
- durable production workflow runtime
- trusted attestation issuer
- production deployment·release

조사 결과는 이 공백을 숨기지 않고 향후 구현·검증 필요사항으로 남긴다.
