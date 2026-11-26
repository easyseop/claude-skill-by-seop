# Codex 협업 운영 규약

## 1. 목적

이 문서는 `Knowledge & RAG Builder K0~K6` 구현에서 다음 두 세션이 GitHub를 공유 작업판으로 사용하기 위한 운영 계약이다.

- 총괄·검토 세션: 현재 ChatGPT 대화
- 구현 세션: 사용자가 생성하는 단일 Codex 세션

두 세션은 서로 직접 메시지를 주고받는다고 가정하지 않는다. 모든 공식 상태·결정·증거는 아래 브랜치와 Draft PR에 기록한다.

```text
repository: easyseop/claude-skill-by-seop
branch: codex/knowledge-rag-builder-k0-k6
```

## 2. Source of truth

우선순위는 다음과 같다.

1. 사용자 최신 지시
2. 저장소의 `AGENTS.md`
3. `docs/agent-authoring/CODEX_KNOWLEDGE_RAG_BUILDER_K0_K6_WORK_ORDER.md`
4. `docs/agent-authoring/CODEX_COLLABORATION_PROTOCOL.md`
5. `docs/agent-authoring/CURRENT_WORK_STATE.yaml`
6. PR 리뷰·`HANDOFF_LOG.md`
7. 나머지 조사·평가 문서

구현 코드, 테스트 결과, 구조화 evidence가 문서의 PASS 문장보다 우선한다.

## 3. 역할

### 3.1 Codex 구현 세션

Codex는 다음을 담당한다.

- 작업지시서에 따라 K0~K6 구현
- 전용 브랜치에서만 변경
- 자체 테스트·mutation·traceability 실행
- 구조화 evidence 보존
- 논리 단위별 커밋
- `CURRENT_WORK_STATE.yaml`과 `HANDOFF_LOG.md` 갱신
- 검토 준비가 끝나면 상태를 `READY_FOR_REVIEW`로 변경

Codex는 다음을 하지 않는다.

- `main` 직접 수정
- force push·history rewrite
- PR 자동 병합
- production RAG/index·IAM·secret·외부 write 구현
- 미실행 테스트·감사를 PASS로 기록
- 상위 Planner·Gate·Execution 계약을 임의 변경

### 3.2 총괄·검토 세션

현재 ChatGPT 대화는 다음을 담당한다.

- 브랜치·PR·변경 파일·evidence 검토
- 계약 위반·누락·과잉 구현 판정
- `PASS`, `CHANGES_REQUESTED`, `REENTRY_REQUIRED` 결정
- 필요한 경우 구체적인 수정 지시를 PR 리뷰 또는 작업 상태에 기록
- 통과 후 다음 Assembler 단계의 조사·구현 지시 준비

총괄 세션은 사용자의 명시적 승인 없이 PR을 병합하지 않는다.

## 4. 상태 모델

허용 상태:

```text
READY_FOR_CODEX
IN_PROGRESS
BLOCKED_FOR_DECISION
READY_FOR_REVIEW
CHANGES_REQUESTED
REVIEW_IN_PROGRESS
VERIFIED_LOCAL
REENTRY_REQUIRED
DONE
```

전이:

```text
READY_FOR_CODEX
  -> IN_PROGRESS
  -> BLOCKED_FOR_DECISION | READY_FOR_REVIEW

READY_FOR_REVIEW
  -> REVIEW_IN_PROGRESS
  -> CHANGES_REQUESTED | VERIFIED_LOCAL | REENTRY_REQUIRED

CHANGES_REQUESTED
  -> IN_PROGRESS
```

`VERIFIED_LOCAL`은 local contract-bound candidate에 대한 판정이며 production 승인과 동일하지 않다.

## 5. 작업 단위와 커밋

권장 커밋 분리:

1. K0 research closure·catalog·preflight
2. K1 minimality compiler·schema
3. K2 source governance
4. K3 local ingestion
5. K4 local retrieval
6. K5 security·freshness
7. K6 citation·eval·mutation·audit
8. 결과 보고서·evidence manifest

각 커밋은 빌드 또는 최소 관련 테스트를 통과해야 한다. 서로 무관한 포맷 변경이나 기존 사용자 변경을 섞지 않는다.

## 6. Codex 중간 보고 규약

Codex는 다음 상황에서만 상태를 갱신한다.

- 작업 시작
- 상위 정책 결정이 필요한 blocker 발생
- K0 preflight 실패
- 구현·테스트 완료 후 검토 요청
- 검토 지시 반영 완료

`BLOCKED_FOR_DECISION`일 때 `CURRENT_WORK_STATE.yaml`에 다음을 기록한다.

```yaml
blocker:
  id: BLOCK-...
  question: "결정이 필요한 정확한 질문"
  why_blocking: "답이 없으면 어떤 계약을 확정할 수 없는지"
  options:
    - id: option-a
      effect: "선택 시 달라지는 범위"
  safe_default: null
  affected_paths: []
```

저장소 사실로 해결할 수 있는 문제는 사용자에게 질문하지 않는다.

## 7. 검토 요청 완료 조건

Codex가 `READY_FOR_REVIEW`로 전환하려면 최소 다음이 필요하다.

```text
정확한 보강 프롬프트 coverage: unresolved missing/conflict 0
KNOW 84/84
KINV 100/100
KEVAL 64/64
KMUT 26/26 killed
Planner knowledge golden 22/22
상위 Planner·Gate·Execution preflight PASS
지원하지 않는 parser/runtime의 거짓 구현 0
critical ACL·secret·deletion·injection mutant 생존 0
traceability closed
결과 보고서와 evidence manifest 존재
```

독립 실행 identity가 없으면 감사 상태는 `UNVERIFIED`여야 한다.

## 8. 검토 결과 형식

총괄 세션은 검토 후 다음 중 하나를 기록한다.

```text
VERIFIED_LOCAL
- local contract-bound candidate 통과
- production permission 없음

CHANGES_REQUESTED
- 파일·규칙·테스트 단위의 수정 목록

REENTRY_REQUIRED
- PLANNER | GATE | EXECUTION | KNOWLEDGE 중 재진입 대상
- 현재 단계에서 조용히 보정 금지
```

## 9. 완료 후 다음 단계

Knowledge/RAG Builder가 `VERIFIED_LOCAL`이면 다음 순서로 진행한다.

```text
Agent & Workflow Assembler 심층조사 결과 검토
→ Assembler MVP 구현지시서
→ Assembler 구현
→ Independent Evaluation
→ 최상위 Agent System Author 통합
```

PR 병합은 별도 사용자 승인 후 수행한다.
