# Planner·Gate·Execution 선행 구현 복구 Work Order

## 0. 목적

현재 공식 저장소에서 누락된 다음 세 모듈의 실제 source·test·구조화 evidence를 승인된 계약에 따라 다시 생성하고 검증한다.

```text
1. Capability & Artifact Planner
2. Gate Generator M0~M3
3. Execution Artifact Generator E0~E4
```

과거 구현결과 보고서의 PASS 문장을 복사하지 않는다. 이 workstream에서 생성한 현재 source와 실제 테스트 결과만 새로운 evidence가 된다.

최종 결과는 **local contract-bound candidate**다. 실제 production permission, Host Hook 활성화, 운영 write, 별도 감사 identity, production release를 승인하지 않는다.

## 1. 수행 주체

```text
session_type: implementation
owner_role: implementation_session
branch: recovery/upstream-builders
sequence: Planner → Gate → Execution
```

한 번에 한 모듈만 구현한다. 앞 단계가 `VERIFIED_LOCAL_CANDIDATE`가 아니면 다음 모듈을 시작하지 않는다.

## 2. 입력 정본

`INPUT_MANIFEST.yaml`에 등록된 compact catalog를 공식 입력으로 사용한다.

```text
CAP_RULES_01_18.json
CAP_RULES_19_36.json
PLANNER_EVALS_01_22.json
GATE_RULES_01_40.json
GATE_RULES_41_80.json
GATE_INVARIANTS_001_085.json
GATE_EVALS_001_048.json
EXECUTION_GENERATOR_CATALOG.json
```

입력의 digest가 다르거나 ID가 누락·중복되면 `BLOCKED_FOR_SOURCE`로 중단한다. 기억, 대화 요약, 과거 보고서만으로 빠진 규칙을 추측하지 않는다.

## 3. 공통 구현 원칙

1. `OWNERSHIP.yaml.writable_paths` 밖을 수정하지 않는다.
2. `.claude/settings.json`, `.github/**`, Knowledge/RAG, Assembler 조사 경로를 수정하지 않는다.
3. 규칙·불변식·평가 ID는 입력 catalog에서 자동 추출한다.
4. source·test·evidence·report를 분리한다.
5. 자유문자 PASS, exit code 0, 파일 존재만으로 완료하지 않는다.
6. 입력·source·checker·test·evidence digest를 현재 snapshot에 결박한다.
7. 입력 또는 source 변경 시 downstream 결과를 `STALE` 처리한다.
8. 생성자와 같은 실행에서 작성한 감사 정의는 실제 독립 identity가 아니다. 별도 identity가 실행되지 않으면 `UNVERIFIED`로 기록한다.
9. 운영 enforcement가 실제로 활성화되지 않았으면 `HARD_ENFORCEMENT_UNAVAILABLE`로 둔다.
10. main 직접 수정, force push, 자동 병합을 하지 않는다.

---

# Phase P — Capability & Artifact Planner 복구

## P1. 목표

사용자의 요청·저장소 사실·정책을 받아 필요한 최소 Capability·control mode·component set을 설계하는 Planner를 구현한다. 실제 업무 Skill·Script·Tool·RAG·Agent·배포는 만들지 않는다.

정본:

```text
CAPABILITY_PLAN.yaml
```

## P2. 필수 구조

```text
.claude/skills/capability-artifact-planner/
├── SKILL.md
├── references/
│   ├── CAP_RULES.md
│   ├── RULE_COVERAGE.yaml
│   ├── decision-guide.md
│   ├── interview-guide.md
│   └── schema-guide.md
├── assets/
│   ├── REQUEST.template.md
│   ├── PROJECT_POLICY.template.yaml
│   ├── CAPABILITY_PLAN.template.yaml
│   ├── REPO_FACTS.template.json
│   └── PLANNER_EVALS.template.yaml
├── scripts/
│   ├── discover_repository.py
│   ├── init_capability_plan.py
│   ├── derive_contracts.py
│   ├── check_capability_plan.py
│   ├── audit_capability_plan.py
│   ├── planner_stop_gate.py
│   ├── install.py
│   └── run_self_tests.py
└── evals/
    ├── planner-evals.yaml
    └── mutations.yaml

.claude/agents/capability-plan-auditor.md
```

## P3. 필수 계약

- CAP-01~CAP-36 정확히 36개
- Planner EVAL-01~22 정확히 22개
- control mode:
  - `direct_response`
  - `deterministic_workflow`
  - `bounded_agent`
  - `multi_agent`
- selected/rejected component 근거·필요성 시험·소유자
- 각 Capability의 단일 `primary_owner`
- acceptance criterion의 Gate/Eval mapping
- high-risk hard control
- RAG·Agent·Multi-agent·state 조건부 필드
- repository ref·source cutoff·planner version
- upstream digest 변경 시 STALE
- machine check + blind-first audit 전 approved 금지

## P4. Planner mutation 15개

다음을 하나씩 제거·변조했을 때 반드시 실패한다.

```text
MUT-01 primary owner
MUT-02 acceptance criterion mapping
MUT-03 selected component necessity evidence
MUT-04 rejected component reason/reconsider condition
MUT-05 high-risk approval
MUT-06 write permission
MUT-07 RAG ACL
MUT-08 retrieval eval
MUT-09 Agent termination budget
MUT-10 state TTL
MUT-11 secret LLM-context prohibition
MUT-12 repository ref
MUT-13 source cutoff
MUT-14 audit attestation/current audit binding
MUT-15 input digest freshness
```

## P5. Planner 완료 검사

```text
CAP 36/36
base eval 22/22
paraphrase variants 44/44
scenario runs 66/66
mutation 15/15 detected
same-input idempotency PASS
Prompt-only request creates no downstream Skill
selected Skill creates conditional author handoff only
blind-first procedure implemented
independent identity absent → UNVERIFIED
```

증거:

```text
docs/agent-authoring/evidence/capability-planner/
├── self-test-summary.json
├── mutation-results.json
├── planner-metrics.json
├── planner-audit-result.json
├── planner-stop-gate.json
└── implementation-manifest.json
```

결과 보고서:

```text
docs/agent-authoring/CAPABILITY_ARTIFACT_PLANNER_구현결과.md
```

P단계가 실패하면 Gate를 시작하지 않는다.

---

# Phase G — Gate Generator M0~M3 복구

## G1. 목표

Planner가 확정한 위험·권한·합격 기준을 단계별 Gate 계약, 결정적 checker, 로컬 adapter, evidence로 변환한다.

하드 경계:

```text
M0 rules·schema·digest
M1 Planner→Gate compiler
M2 deterministic checker·STALE·PASS 위조 차단
M3 local path/input/tool Gate·Hook adapter·Stop gate
```

M4 exact approval, M5 durable Agent state, M6 tenant RAG, M7 production release는 실제 구현 완료로 표시하지 않는다.

## G2. 필수 구조

```text
.claude/skills/gate-generator/
├── SKILL.md
├── references/
│   ├── GATE_RULES.md
│   ├── GATE_RULE_COVERAGE.yaml
│   ├── gate-taxonomy.md
│   ├── enforcement-boundaries.md
│   ├── human-approval-contract.md
│   ├── tool-mcp-api-gates.md
│   ├── runtime-state-recovery.md
│   ├── rag-gates.md
│   └── evidence-attestation.md
├── assets/
│   ├── GATE_CONTRACT.template.yaml
│   ├── GATE_CONTRACT.schema.json
│   ├── GATE_RESULT.schema.json
│   ├── APPROVAL_REQUEST.schema.json
│   ├── APPROVAL_DECISION.schema.json
│   ├── WAIVER.template.yaml
│   └── RELEASE_MANIFEST.template.yaml
├── scripts/
│   ├── derive_gate_contract.py
│   ├── check_gate_contract.py
│   ├── discover_enforcement_inventory.py
│   ├── canonicalize_and_hash.py
│   ├── bind_phase_manifest.py
│   ├── check_traceability.py
│   ├── run_gate_evals.py
│   ├── run_gate_mutations.py
│   ├── gate_stop_gate.py
│   ├── install.py
│   └── run_self_tests.py
├── adapters/claude-code/
│   ├── pretool_gate.py
│   ├── posttool_gate.py
│   ├── stop_gate.py
│   └── settings.fragment.example.json
└── evals/
    ├── gate-evals.yaml
    ├── planner-gate-golden.yaml
    └── mutations.yaml

.claude/agents/gate-auditor.md
```

실제 `.claude/settings.json`을 수정하지 않는다.

## G3. 필수 정본

```text
GATE-01~GATE-80: 80개
I-001~I-085: 85개
GEVAL-001~GEVAL-048: 48개
Planner gate golden: 22개
```

각 Gate는 requirement/risk, implementation, test, mutation, evidence에 양방향 연결된다.

## G4. Gate critical mutation 20개

최소 다음을 포함하고 모두 killed여야 한다.

```text
GMUT-001 upstream digest 제거
GMUT-002 free-text PASS 허용
GMUT-003 fail-closed를 fail-open으로 변경
GMUT-004 mandatory Gate implementation mapping 제거
GMUT-005 high-risk approval 제거
GMUT-006 permission 제거
GMUT-007 Hook timeout을 allow로 변경
GMUT-008 malformed Hook output을 allow로 변경
GMUT-009 canonical path resolution 제거
GMUT-010 Tool namespace/version/server binding 제거
GMUT-011 RAG ACL 제거
GMUT-012 Agent termination 제거
GMUT-013 state TTL 제거
GMUT-014 approval expiry/nonce 제거
GMUT-015 idempotency payload binding 제거
GMUT-016 OUTCOME_UNKNOWN blind retry
GMUT-017 attestation subject 교체
GMUT-018 audit attestation 제거
GMUT-019 phase boundary digest 제거
GMUT-020 required test skip를 success 처리
```

## G5. Hook smoke 19개

최소 다음을 실제 adapter 입출력으로 검사한다.

```text
허용 path
repo 밖 path
traversal
symlink escape
read intent에 write tool
unknown tool
ungated allow
secret input
stale inventory
direct bypass inventory
Hook timeout
malformed handler result
missing policy
PostToolUseFailure OUTCOME_UNKNOWN
reconciliation-required
Stop literal PASS 차단
forged structured PASS 차단
STALE result 차단
current valid local result 허용
```

## G6. Gate 완료 검사

```text
Planner preflight current PASS
GATE 80/80
I 85/85
Planner golden 22/22
GEVAL 48/48 expected statuses
GMUT 20/20 killed
Hook smoke 19/19
traceability forward/reverse closed
free-text and forged PASS blocked
input/policy/checker/evidence drift → STALE
host enforcement unverified
M4~M7 HARD_ENFORCEMENT_UNAVAILABLE
independent identity absent → UNVERIFIED
```

증거:

```text
docs/agent-authoring/evidence/gate-generator/
├── self-test-summary.json
├── baseline-check.json
├── baseline-trace.json
├── planner-gate-golden-results.json
├── gate-eval-results.json
├── gate-mutation-results.json
├── hook-smoke-results.json
├── enforcement-inventory.json
├── gate-audit-result.json
└── implementation-manifest.json
```

결과 보고서:

```text
docs/agent-authoring/GATE_GENERATOR_MVP_구현결과.md
```

G단계가 실패하면 Execution을 시작하지 않는다.

---

# Phase E — Execution Artifact Generator E0~E4 복구

## E1. 목표

Planner가 선택하고 Gate가 허용한 execution component만 재사용하거나 생성한다.

```text
E0 rules·schema·state
E1 execution asset discovery·reuse
E2 Planner/Gate→Execution compiler
E3 deterministic checker·trace·STALE
E4 safe local artifact builder
```

Contract Compiler와 Artifact Builder를 분리한다. 계약 검사 전 source 생성 금지.

## E2. 필수 구조

```text
.claude/skills/execution-artifact-generator/
├── SKILL.md
├── references/
│   ├── EXEC_RULES.md
│   ├── EXEC_RULE_COVERAGE.yaml
│   ├── artifact-types.md
│   ├── runtime-selection.md
│   ├── reuse-decision.md
│   ├── io-error-recovery.md
│   ├── build-policy.md
│   └── sandbox-supply-chain.md
├── assets/
│   ├── EXECUTION_CONTRACT.template.yaml
│   ├── EXECUTION_CONTRACT.schema.json
│   ├── EXECUTION_RESULT.schema.json
│   ├── RECONCILIATION_RESULT.schema.json
│   ├── REUSE_ASSESSMENT.schema.json
│   ├── EXECUTION_TRACEABILITY.schema.json
│   ├── EXECUTION_BUILD_MANIFEST.schema.json
│   └── EXECUTION_TEST_EVIDENCE.schema.json
├── scripts/
│   ├── discover_execution_assets.py
│   ├── assess_reuse.py
│   ├── derive_execution_contract.py
│   ├── check_execution_contract.py
│   ├── check_execution_traceability.py
│   ├── scaffold_execution_artifact.py
│   ├── check_generated_artifact.py
│   ├── check_execution_result.py
│   ├── bind_execution_phase_manifest.py
│   ├── run_execution_evals.py
│   ├── run_execution_mutations.py
│   ├── execution_stop_gate.py
│   ├── install.py
│   └── run_self_tests.py
├── builders/
│   ├── registry.yaml
│   ├── no_code.py
│   ├── existing_artifact.py
│   ├── python_local.py
│   └── java_cli.py
└── evals/
    ├── execution-evals.yaml
    ├── planner-execution-golden.yaml
    └── mutations.yaml

.claude/agents/execution-artifact-auditor.md
```

## E3. 필수 정본

```text
EXEC-01~EXEC-30: 30개
EXI-001~EXI-045: 45개
EXEVAL-001~EXEVAL-026: 26개
EXMUT-001~EXMUT-010: 10개
Planner execution golden: 22개
```

## E4. 지원 경계

실제 built-in builder:

```text
no_code
existing_artifact
python_local
java_cli
```

지원되지 않은 runtime을 Python으로 대체하지 않는다.

```text
SUPPORTED_CONTRACT_ONLY
UNSUPPORTED_RUNTIME_PACK
HARD_ENFORCEMENT_UNAVAILABLE
```

생성된 코드는 비신뢰 draft이며 verified runner가 없으면 static check까지만 수행한다.

## E5. 추가 Builder 반례

최소 16개를 포함한다.

```text
no-code source 0
reuse-direct new implementation 0
thin adapter effect 확대 금지
unsupported runtime fallback 금지
source digest는 GENERATED 이후
result/test evidence는 TESTED 이후
CLI stdout 규칙의 타 artifact 오적용 금지
contract PASS 전 source 생성 차단
repo 밖 path 차단
network 차단
secret canary 차단
unverified runner dynamic execution 차단
historical evidence 재사용 차단
builder source drift → STALE
forged static PASS 차단
READY_FOR_ASSEMBLY가 production permission으로 승격되지 않음
```

## E6. Execution 완료 검사

```text
Planner/Gate preflight current PASS
EXEC 30/30
EXI 45/45
EXEVAL 26/26
EXMUT 10/10 killed
Planner execution golden 22/22
compiler idempotency PASS
Builder negative tests ≥16 all PASS
traceability physical forward/reverse closed
static binder tests current
no-code/reuse paths exact
external write/network/generated-code dynamic execution 0
independent identity absent → UNVERIFIED
READY_FOR_ASSEMBLY false unless all local conditions current
production permission false
```

증거:

```text
docs/agent-authoring/evidence/execution-artifact-generator/
├── eag-preflight.json
├── self-test-summary.json
├── planner-execution-golden-results.json
├── execution-eval-results.json
├── execution-mutation-results.json
├── builder-test-results.json
├── traceability-results.json
├── artifact-state-binder-results.json
├── execution-audit-result.json
├── execution-stop-gate.json
└── implementation-manifest.json
```

결과 보고서:

```text
docs/agent-authoring/EXECUTION_ARTIFACT_GENERATOR_MVP_구현결과.md
```

---

# 4. 상태·커밋·인수인계

작업 시작 시:

```text
CURRENT_SESSION_STATE.yaml → IN_PROGRESS / phase=P
HANDOFF_LOG.md append
```

각 phase 완료 후 논리적으로 분리된 커밋을 만든다. 권장:

```text
1. planner source
2. planner tests/evidence/report
3. gate source
4. gate tests/evidence/report
5. execution source
6. execution tests/evidence/report
```

단계 실패 시:

```text
BLOCKED_FOR_SOURCE
BLOCKED_FOR_DECISION
REENTRY_REQUIRED
```

중 하나로 상태를 바꾸고 다음 phase로 진행하지 않는다.

전체 완료 시:

```text
CURRENT_SESSION_STATE.yaml → READY_FOR_REVIEW
OUTPUT_MANIFEST.yaml에 모든 source·test·evidence·report digest 기록
HANDOFF_LOG.md에 명령·결과·한계·변경 경로 기록
Draft PR에 결과 요약
```

## 5. 최종 완료 조건

- P, G, E 세 phase 모두 현재 source에 대해 자체 테스트 PASS
- compact input catalog의 모든 ID가 source·test·evidence에 추적됨
- critical mutation survived 0
- 다른 workstream 경로 변경 0
- Knowledge/RAG·Assembler 파일 변경 0
- `.claude/settings.json`, `.github/**` 변경 0
- production enforcement·독립 identity를 거짓 주장하지 않음
- `OUTPUT_MANIFEST.yaml` current
- 상태 `READY_FOR_REVIEW`

자동 병합하지 않는다.
