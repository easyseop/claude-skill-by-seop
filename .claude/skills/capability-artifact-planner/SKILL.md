---
name: capability-artifact-planner
description: 사용자 요구와 저장소 사실을 원자 Capability로 분해하고 가장 단순한 제어 모드와 필요한 구성요소만 선택한다. 실제 업무 코드·RAG·배포는 만들지 않고 CAPABILITY_PLAN과 downstream 계약을 작성·검사한다.
argument-hint: "<대상명> [--mode full|plan|audit] [--request REQUEST.md] [--policy PROJECT_POLICY.yaml]"
allowed-tools: Read, Grep, Glob, Bash(python3:*), Bash(git status:*), Bash(git diff:*)
---

# Capability & Artifact Planner

## 책임

이 Skill은 다음 순서만 수행한다.

```text
요청 원문 보존
→ 저장소 사실 조사
→ 원자 Capability 분해
→ 단순 기준선 작성
→ 결정적 책임 우선 배치
→ control mode와 component set 선택
→ 안전 제약 적용
→ CAPABILITY_PLAN 검사
→ 읽기 전용 감사 후보 생성
→ downstream 계약 파생
```

실제 업무용 Skill·Script·Tool·RAG·Agent·Workflow·배포를 구현하지 않는다.

## 정본

대상별 유일한 설계 정본은 다음이다.

```text
.claude/agent-system-authoring/<target>/CAPABILITY_PLAN.yaml
```

이 저장소에서는 `.yaml` 파일에 canonical JSON을 기록할 수 있다. 모든 스크립트는 이를 JSON으로 읽고 결정적으로 직렬화한다.

## 입력

필수:

- `REQUEST.md`
- `REPO_FACTS.json`
- `PROJECT_POLICY.yaml`

조건부:

- `USER_DECISIONS.yaml`
- 기존 eval·source inventory·research dossier

저장소에서 확인 가능한 사실은 사용자에게 다시 묻지 않는다. 고위험 정책, 권위 원천, 부작용 승인처럼 결과를 실제로 바꾸는 질문만 `PLANNER_QUESTIONS.yaml`에 기록한다.

## Control mode

허용값은 정확히 다음 네 가지다.

```text
direct_response
deterministic_workflow
bounded_agent
multi_agent
```

`Hybrid`는 설명용 summary label일 뿐 control mode가 아니다.

## Component

필요성이 입증된 것만 선택한다.

```text
skill, reference, script, validator, tool, rag, workflow,
agent, approval, permission, hook, sandbox, state, eval, tracing
```

Prompt-only 또는 deterministic code 기준선을 먼저 평가한다. 실패 증거 없이 Agent·RAG·Multi-agent로 상승하지 않는다.

## Hard boundary

- 객관 규칙은 code/validator/workflow에 우선 배치한다.
- 외부 write에는 permission·audit가 필요하다.
- high/critical write에는 human approval이 필요하다.
- irreversible write에는 dry-run 또는 불가 근거와 idempotency/compensation이 필요하다.
- secret는 LLM 문맥을 통과할 수 없다.
- RAG에는 corpus·freshness·ACL·citation·retrieval eval이 필요하다.
- Agent에는 turn/tool/time budget·종료·trace가 필요하다.
- Multi-agent에는 context isolation·independent parallelism·authority separation·입증된 specialization·single-agent eval failure 중 하나가 필요하다.

필수 hard enforcement를 현재 환경에서 제공할 수 없으면 `BLOCKED` 또는 `HARD_ENFORCEMENT_UNAVAILABLE`로 기록한다.

## 실행 순서

1. `scripts/materialize_catalogs.py`로 CAP 36개와 Planner eval 22개 정본을 materialize한다.
2. `scripts/discover_repository.py`로 bounded read-only 저장소 사실을 만든다.
3. `scripts/init_capability_plan.py`로 초안을 만든다.
4. 요청의 모든 목표를 원자 Capability로 분해한다.
5. 각 Capability에 primary owner를 정확히 하나 지정한다.
6. 선택·기각 component마다 근거와 재검토 조건을 기록한다.
7. `scripts/check_capability_plan.py`가 통과할 때까지 수정한다.
8. `scripts/audit_capability_plan.py`로 procedural blind-first 비교 자료를 만든다.
9. `scripts/derive_contracts.py`로 downstream 계약을 파생한다.
10. `scripts/planner_stop_gate.py`로 local handoff 가능 여부를 판정한다.

## 완료 기준

- CAP 36/36
- Planner eval 22/22
- 표현 변형 44/44
- mutation 15/15 detected
- 동일 입력 materialization·plan init 멱등성
- Prompt-only 요청은 downstream Skill을 만들지 않음
- selected Skill만 조건부 author handoff 생성
- machine check와 procedural audit 전 `approved` 금지
- 별도 감사 identity가 실제 실행되지 않으면 `UNVERIFIED`

## 금지

- `.claude/settings.json` 수정
- main 직접 수정·force push·자동 병합
- 과거 보고서의 PASS를 current evidence로 재사용
- 자유문자 PASS나 exit code 0만으로 완료 판정
- Planner가 선택하지 않은 component를 downstream에서 추가

## 독립 검토 후 설계 계획 발행

기존 Stop Gate는 절차 감사만 처리한다. 별도 발행 CLI는 고정한 DRAFT와 세 원본 입력,
기계 검사 JSON, 절차 감사 JSON, 네 가지 파생 계약, 독립 검토 원본과 발행자 서명을 받는다.

```sh
python3 scripts/planner_stop_gate.py issue --draft plan.json --request request.md --policy policy.json --facts facts.json --machine machine.json --procedural audit.json --contracts contracts --independent independent.json --signature independent.sig --output issued-plan.json
```

지원하는 출처 증명은 독립 검토자에게 별도로 귀속된 공개키로 확인하는 OpenSSL
dgst -sha256 분리 서명이다. 서명 대상은 독립 JSON 전체의 canonical_json_bytes이다.
신뢰 키는 작업 디렉터리 외부의 /etc/factory/planner-reviewers/<issuer>.pem에서만 읽는다.
검토자 이외 주체가 제어하는 키 또는 검토 JSON과 함께 전달된 키를 신뢰 목록에 등록하면 안 된다.
워크스페이스에서 키를 설치하지 않는다. 채팅 링크나 전사본만 있으면 발행은 차단된다.
출력은 신규 파일이어야 하며 설계 인계에만 유효하다.
