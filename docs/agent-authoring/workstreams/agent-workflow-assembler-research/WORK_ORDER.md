# Agent & Workflow Assembler 심층조사 Work Order

## 0. 역할과 목적

당신은 구현 세션이 아니라 독립 심층조사 세션이다. Agent Skills, Claude Code, OpenAI Agents SDK, LangGraph, MCP, 상태 머신, 워크플로 신뢰성, 패키징·배포 경계를 조사한다.

목적은 새 기능을 다시 발명하는 것이 아니다. 이미 승인된 다음 계약과 artifact만 사용해 최종 Skill·Agent·Workflow package를 조립하는 `Agent & Workflow Assembler`의 공통 규칙을 도출한다.

```text
CAPABILITY_PLAN.yaml
GATE_CONTRACT.yaml
EXECUTION_CONTRACT.yaml
KNOWLEDGE_CONTRACT.yaml / KNOWLEDGE_SPEC.yaml
검증된 Skill·Script·Validator·Tool·Reference·Agent 정의
```

Assembler는 상위 계약에 없는 component를 조용히 추가하지 않는다. 새 필요성이 발견되면 해당 단계로 재진입한다.

## 1. 필수 입력

`INPUT_MANIFEST.yaml`에 등록된 입력을 처음부터 끝까지 읽는다.

Knowledge 구현이 아직 완료되지 않았다면 research 계약 기준으로 조사하되 실제 구현 사실처럼 쓰지 않는다.

## 2. 핵심 상위 제약

1. Planner가 선택한 `control_mode`와 `selected_components`를 보존한다.
2. Gate가 요구한 hard enforcement를 Skill 문장으로 대체하지 않는다.
3. Execution Generator의 supported/unavailable runtime 경계를 보존한다.
4. Knowledge Builder의 authority·ACL·freshness·citation binding을 넓히지 않는다.
5. `SKILL.md`, `Agent.md`, Workflow, Tool, Reference, Script를 모두 만들 필요는 없다.
6. direct response나 deterministic workflow가 충분하면 Agent를 만들지 않는다.
7. Skill이 선택되지 않았으면 `claude-skill-author`를 호출하지 않는다.
8. 실제 settings/Hook 활성화는 프로젝트 owner의 별도 승인과 검증이 필요하다.
9. 새 component 필요 시 `PLANNER_REENTRY_REQUIRED`, `GATE_REENTRY_REQUIRED`, `EXECUTION_REENTRY_REQUIRED`, `KNOWLEDGE_REENTRY_REQUIRED` 중 하나를 반환한다.
10. production release와 local package assembly를 구분한다.

## 3. 반드시 조사할 영역

### A. Assembler 책임 경계

- 생성하는 것과 참조만 하는 것
- 새 코드·RAG·Tool·Agent 직접 생성 방지
- contract mismatch 재진입 기준
- source of truth와 파생 manifest 구분

### B. Control mode별 조립

```text
direct_response
deterministic_workflow
bounded_agent
multi_agent
```

각 mode의 entrypoint, 제어권, 상태, Tool·Script·Knowledge 호출, 종료, 오류, 승인, trace, package layout을 구분한다.

### C. Skill·Command·Agent 관계

- Skill only
- Skill + Script
- Skill + Reference/RAG
- Skill + Agent
- Agent의 Skill preload
- `context: fork`
- standalone Agent
- 수동 command
- model invocation 경계
- 중복 command/skill/agent 방지

Claude Code 전용 규칙과 제품 독립 규칙을 구분한다.

### D. Typed binding

component별 I/O schema, capability/AC/Gate ID, digest, status, no-evidence/conflict/outcome-unknown, version compatibility, dependency, adapter, timeout/retry, error translation을 조사한다.

### E. Context engineering

progressive disclosure, Skill body와 references 분리, subagent context isolation, 필요한 knowledge span만 전달, tool output size, state·memory, injection data-only marker, context budget, truncation, stale context, handoff summary schema를 조사한다.

### F. Tool·Execution·Knowledge binding

- low-level credential·raw DB·vector store 직접 노출 금지
- typed entrypoint
- read/write 분리
- Tool identity/version/server
- Script entrypoint/digest
- Knowledge snapshot/auth context
- Gate pre/post/completion
- result validation
- direct bypass inventory

### G. Handoff·권한·승인

original user/tenant/role binding, target permission ceiling, exact approval payload, handoff cycle, history filter evidence loss, Agent별 tools/permissions, Agent 정의와 실제 runtime 권한 차이, creator/auditor separation을 조사한다.

### H. Workflow·상태·병렬

state machine, illegal transition, checkpoint, tool_call/tool_result, branch input freeze, deterministic merge, race/conflict, lease/fencing, partial completion, retry·idempotency·compensation·reconciliation, resume stale 재검사를 조사한다.

### I. 설치·버전·마이그레이션

package manifest, dependency compatibility, relative path, install idempotency, backup, generated/user-owned 구분, settings fragment, schema migration, coexistence, rollback/uninstall, Git diff boundary, reproducible digest를 조사한다.

### J. Eval·Release

component PASS의 system PASS 오승격, E2E 정상·경계·오류·악성, no-code/no-agent/no-RAG near-miss, stale dependency, free-text PASS, Hook/permission unavailable, ACL leakage, Tool bypass, partial failure, clean-room evaluation, mutation·ablation, local assembly vs production release를 조사한다.

## 4. 필수 자료 계열

1. 공식 규격의 MUST/MUST NOT
2. 현재 공식 제품 문서
3. 공식 저장소·코드·이슈
4. 원 논문
5. 신뢰 가능한 workflow·보안·패키징 문서

필수 계열:

- Agent Skills specification, progressive disclosure, scripts, evaluation
- Claude Code Skills, commands, subagents, hooks, permissions, settings
- OpenAI Agents SDK agents, tools, handoffs, guardrails, sessions, tracing, HITL
- LangGraph workflows/agents, state, persistence, interrupts, subgraphs, deployment
- MCP architecture, tools, resources, prompts, authorization, elicitation
- durable workflow의 retry/idempotency/state
- state machine·contract testing·package manifest·supply-chain provenance
- multi-agent context isolation·handoff·merge
- stale state, orphan tool result, permission bypass, skipped gate, config drift, package overwrite, incompatible schema, partial completion 실패 사례

최신 기능은 기준일·버전·commit을 기록한다.

## 5. 필수 산출물 구조

```markdown
# Agent & Workflow Assembler 심층조사

## 0. 결론과 조사 방법
## 1. Assembler 책임·비책임
## 2. 입력 계약과 source of truth
## 3. Control mode별 assembly
## 4. Skill·Command·Agent·Workflow 결정표
## 5. Component interface와 typed binding
## 6. Context engineering·progressive disclosure
## 7. Tool·Execution·Knowledge binding
## 8. Permission·approval·handoff
## 9. State·checkpoint·parallel·recovery
## 10. Package layout·install·upgrade·rollback
## 11. Observability·evidence·attestation
## 12. Eval·mutation·ablation·release
## 13. 공통 규칙: ASM-01 ~ ASM-N
## 14. ASSEMBLY_CONTRACT.yaml 제안
## 15. 보조 스키마
## 16. 기계 불변식: AINV-001 ~ AINV-N
## 17. 평가 세트: AEVAL-001 ~ AEVAL-N
## 18. Mutation 세트: AMUT-001 ~ AMUT-N
## 19. Planner 22개 시나리오 Assembly golden mapping
## 20. Planner·Gate·Execution·Knowledge·Skill Author 연결
## 21. 우리 하네스 구현안
## 22. 단계별 구현 순서와 MVP 경계
## 23. 한계와 미확인 사항
## 24. 결론-출처 추적표
## 25. 전체 출처
```

각 규칙은 적용 조건, 행동, 검증, 실패 시, 강제 계층, 근거, 예시, 반례를 가진다.

보조 스키마:

```text
SYSTEM_MANIFEST
COMPONENT_BINDINGS
ENTRYPOINT_MANIFEST
CONTEXT_POLICY
HANDOFF_CONTRACT
STATE_MACHINE
RUNTIME_POLICY
INSTALL_MANIFEST
ASSEMBLY_RESULT
RELEASE_HANDOFF
```

## 6. 특히 답할 질문

1. 하나의 거대한 SKILL.md인가, 여러 package를 묶는 manifest인가?
2. control mode별 entrypoint와 제어권은?
3. Skill과 Agent의 책임 중복을 어떻게 검사하는가?
4. component status와 digest를 system completion에 어떻게 결박하는가?
5. Knowledge ACL과 Execution permission을 Agent가 넓히지 못하게 하는 방법은?
6. handoff 시 identity·approval·evidence 유지·재검사는?
7. context isolation과 근거 추적을 동시에 보장하는 방법은?
8. 병렬 worker의 immutable input과 deterministic merge는?
9. component 변경 후 Assembly PASS의 STALE 처리는?
10. Hook·permission 미활성 환경에서 무엇을 BLOCK하는가?
11. local assembly와 production release를 어떻게 분리하는가?
12. creator와 auditor 독립성은?
13. 불필요한 Agent·RAG·Script를 추가하지 않았음을 어떻게 검사하는가?
14. `claude-skill-author`를 언제 호출하는가?

## 7. 금지사항

- 상위 Planner에 없는 component 추가
- missing runtime를 Prompt·Skill로 대체
- 모든 시스템을 Agent/Multi-agent로 생성
- 모든 지침을 하나의 거대한 SKILL.md에 복제
- secret을 prompt·state·handoff에 포함
- Knowledge security filter를 LLM이 수정
- exit 0·문서 PASS·파일 존재만으로 system PASS
- settings fragment만으로 Hook 활성 주장
- creator와 auditor 동일 identity를 독립 감사로 주장
- production release·deployment 수행
- 출처 없는 timeout·budget·component 수를 범용 규범화

## 8. 결과 경로

조사 결과를 다음 저장소 경로에 작성한다.

```text
docs/agent-authoring/research-results/05_AGENT_WORKFLOW_ASSEMBLER_심층조사.md
```

`/mnt/data`에만 저장하지 않는다. `OUTPUT_MANIFEST.yaml`에 결과와 digest를 기록하고 상태를 `READY_FOR_REVIEW`로 바꾼다.
