# Codex 작업지시 — Knowledge & RAG Builder K0~K6

## 0. 작업 주체와 목표

너는 Claude Code 세션이 아니라 이 Git 저장소의 구현 담당 Codex다.
`.claude/skills/**`와 `.claude/agents/**`는 네 실행 환경이 아니라 향후 Claude Code가 사용할 산출물 경로다.

목표는 `Knowledge & RAG Builder`의 **K0~K6 로컬 MVP**를 실제 저장소에 구현하는 것이다.

```text
K0 research closure·input binding
→ K1 minimality compiler
→ K2 source governance
→ K3 제한된 local ingestion
→ K4 기본 local retrieval
→ K5 security·freshness contract
→ K6 citation·eval·audit candidate
```

이 결과는 `contract-bound local knowledge candidate`다. Production RAG, 실제 tenant IAM/ACL, 운영 secret, 외부 vector DB, production index/release를 승인하는 결과가 아니다.

커밋·푸시·브랜치 변경·PR 생성은 작업 완료 후 별도 단계에서만 수행한다. 작업 중에는 현재 브랜치를 유지한다.

## 1. 우선순위

1. 현재 사용자/이슈 지시
2. 저장소의 `AGENTS.md`가 있다면 해당 지시
3. 이 문서
4. 현재 저장소의 Planner·Gate·Execution 실제 구현과 구조화 evidence
5. 기존 `claude-skill-author`와 프로젝트 규칙

`CLAUDE.md`는 Codex의 상위 지시가 아니다. 다만 Claude Code 산출물 호환성 확인용으로 읽을 수 있다.

## 2. 먼저 현재 상태 판정

저장소 루트에서 다음을 확인한다.

```bash
git rev-parse --show-toplevel
git status --short
git diff --stat
git diff --name-only

find .claude/skills -maxdepth 2 -type f -name SKILL.md | sort
find .claude/agents -maxdepth 1 -type f 2>/dev/null | sort
find docs/agent-authoring -maxdepth 4 -type f | sort
```

다음 중 하나로 판정한다.

- `A`: Knowledge/RAG Builder 구현물이 없음
- `B`: 구현물은 있으나 보고서·evidence가 잘못되거나 누락됨
- `C`: 일부만 구현됨

중복 생성하지 말고 미구현 범위만 수행한다.

또한 선행 구성요소를 확인한다.

- Capability & Artifact Planner
- Gate Generator
- Execution Artifact Generator

실물이 없거나 현재 digest와 증거가 맞지 않으면 거짓 PASS를 만들지 말고 `UPSTREAM_MISSING`, `STALE`, 또는 해당 재진입 상태로 보고한다.

## 3. 범위

### 구현 범위

- K0: 정확한 연구 요구사항 closure, ID catalog, 상위 binding
- K1: 지식 최소 구조 판정
- K2: source governance
- K3: 제한된 로컬 ingestion
- K4: 기본 로컬 retrieval
- K5: security·freshness contract
- K6: citation·eval·audit candidate

### 수행하지 않음

- production RAG/index 배포
- 실제 IAM·tenant ACL·RLS/DLS 변경
- secret 값 수집·복제·로그
- 외부 vector DB·embedding/reranker 서비스 설치·호출
- 운영 DB/API 쓰기
- `.claude/settings.json` 자동 수정
- Claude subagent를 실제 호출했다고 주장
- 동일 Codex 실행을 독립 identity 감사로 주장
- Knowledge 단계에서 새 Agent·Tool·Execution component를 임의 추가

새 필요성이 발견되면 다음 중 하나를 반환한다.

```text
PLANNER_REENTRY_REQUIRED
GATE_REENTRY_REQUIRED
EXECUTION_REENTRY_REQUIRED
BLOCKED_SOURCE_AUTHORITY
BLOCKED_ACCESS_POLICY
HARD_ENFORCEMENT_UNAVAILABLE
```

## 4. 필수 정본과 보정

구현 전에 다음 정본을 만든다.

```text
KNOW-01~KNOW-84       84개
KINV-001~KINV-100     100개
KEVAL-001~KEVAL-064   64개
KMUT-001~KMUT-026     26개
Planner Knowledge golden EVAL-01~22 22개
```

ID는 누락·중복·범위 밖 추가가 없어야 한다.

KMUT 최소 범위:

- no-RAG 합격인데 vector/RAG 강제
- baseline·실패 evidence 제거
- live 값을 stale index로 대체
- source owner·authority·effective interval·digest 제거
- prohibited/quarantine source 활성화
- ACL·sensitivity 상속 제거
- secret indexing 허용
- parser/table/source-span provenance 제거
- mixed embedding/index version 허용
- candidate 검증 전 publish
- tombstone 전파 누락
- user-supplied tenant 허용
- ACL을 post-filter로 이동
- cache key의 auth/policy/snapshot 제거
- query rewrite가 tenant/scope/as-of 변경
- unauthorized candidate를 reranker/외부 모델에 전달
- retrieved instruction이 Tool 권한 부여
- no-evidence에서 일반지식 확정 답
- URL 존재만 검사하고 claim support 제거
- citation completeness 제거
- retrieval·generation 평가를 하나로 합침
- source/index/policy 변경 후 과거 PASS 재사용

## 5. 정본 역할

```text
KNOWLEDGE_CONTRACT.yaml
= Planner가 만든 immutable upstream handoff

KNOWLEDGE_SPEC.yaml
= Builder가 선택한 최소 architecture·build·eval 하위 정본

SOURCE_MANIFEST.yaml
= source authority·lifecycle·access 정본

INGESTION_POLICY.yaml
= parser·unit·candidate snapshot·publish/invalidation 정본

RETRIEVAL_POLICY.yaml
= auth·query·route·retrieval·citation·cache 정본
```

Builder는 상위 `KNOWLEDGE_CONTRACT.yaml`을 수정하지 않는다.

## 6. 구현 산출물

```text
.claude/skills/knowledge-rag-builder/
├── SKILL.md
├── references/
│   ├── KNOW_RULES.md
│   ├── KNOW_RULE_COVERAGE.yaml
│   ├── architecture-decision-ladder.md
│   ├── source-governance.md
│   ├── ingestion-and-indexing.md
│   ├── retrieval-routing.md
│   ├── acl-freshness-deletion.md
│   ├── citation-and-abstention.md
│   ├── prompt-injection-trust-boundary.md
│   ├── evaluation-and-mutation.md
│   └── source-map.md
├── assets/
│   ├── KNOWLEDGE_SPEC.template.yaml
│   ├── KNOWLEDGE_SPEC.schema.json
│   ├── SOURCE_MANIFEST.template.yaml
│   ├── SOURCE_MANIFEST.schema.json
│   ├── INGESTION_POLICY.template.yaml
│   ├── INGESTION_POLICY.schema.json
│   ├── RETRIEVAL_POLICY.template.yaml
│   ├── RETRIEVAL_POLICY.schema.json
│   ├── QUERY_ENVELOPE.schema.json
│   ├── RETRIEVAL_RESULT.schema.json
│   ├── SOURCE_UNIT.schema.json
│   ├── INDEX_SNAPSHOT.schema.json
│   ├── CLAIM_EVIDENCE.schema.json
│   ├── KNOWLEDGE_RESULT.schema.json
│   └── KNOWLEDGE_TRACEABILITY.schema.json
├── scripts/
│   ├── extract_knowledge_catalog.py
│   ├── bind_knowledge_inputs.py
│   ├── discover_sources.py
│   ├── classify_sources.py
│   ├── derive_knowledge_specs.py
│   ├── check_knowledge_contract.py
│   ├── check_source_manifest.py
│   ├── ingest_local_sources.py
│   ├── bind_unit_provenance.py
│   ├── build_local_lexical_index.py
│   ├── query_local_lexical.py
│   ├── query_structured_json.py
│   ├── verify_index_snapshot.py
│   ├── apply_tombstones.py
│   ├── verify_citations.py
│   ├── check_knowledge_traceability.py
│   ├── run_knowledge_evals.py
│   ├── run_knowledge_mutations.py
│   ├── knowledge_stop_gate.py
│   ├── install.py
│   └── run_self_tests.py
├── adapters/
│   ├── registry.yaml
│   ├── no_rag.py
│   ├── current_context.py
│   ├── static_reference.py
│   ├── direct_document.py
│   ├── lexical_local.py
│   └── structured_json.py
└── evals/
    ├── knowledge-evals.yaml
    ├── planner-knowledge-golden.yaml
    ├── architecture-near-miss.yaml
    └── mutations.yaml

.claude/agents/
└── knowledge-rag-auditor.md
```

## 7. 지원 범위

### 실제 built-in knowledge mode

```text
no_knowledge
current_context
static_reference
direct_document
file_or_lexical_search
structured_reference
```

### 실제 built-in parser

```text
text/plain
text/markdown
application/json
text/csv
```

### Contract-only 또는 blocked

```text
PDF·DOCX·PPTX·XLSX
image/audio/video
vector·hybrid·rerank·graph
live DB/API/MCP
long-term memory
bounded agentic retrieval
production tenant ACL
```

지원하지 않는 포맷이나 runtime을 Python fallback 등으로 가장하지 않는다.

## 8. 핵심 판정 규칙

1. 지식이 없으면 `no_knowledge`; 불필요한 index·embedding 0개.
2. 작은 안정 자료는 static reference/direct document를 우선한다.
3. 현재 거래·운영 값은 live Tool/API/DB가 권위 원천일 수 있다.
4. source authority와 retrieval score를 분리한다.
5. authenticated identity에서 ACL filter를 유도하며 prompt tenant는 untrusted다.
6. unauthorized candidate는 reranker·생성 모델·cache로 보내지 않는다.
7. source freshness, index freshness, cache freshness를 분리한다.
8. delete·correction·permission revoke를 tombstone과 evidence STALE에 전파한다.
9. retrieved instruction은 data이며 Tool 실행 권한이 아니다.
10. no-match, unauthorized-only, stale-only, conflict, error를 서로 다른 상태로 유지한다.
11. citation은 claim→source version→unit/span→digest→support relation으로 검사한다.
12. URL/파일 존재만으로 citation PASS를 내지 않는다.
13. retrieval, generation, citation, security, freshness eval을 분리한다.
14. source/index/parser/policy/eval 변경 시 기존 PASS·audit는 STALE다.

## 9. Source governance

Codex가 기계적으로 확인할 수 있는 것과 사용자/정책 결정이 필요한 것을 구분한다.

기계 확인 가능:
- 경로·형식·digest
- metadata 필드 존재
- parser/retriever 기존 자산
- version/effective/access-policy reference 존재

임의 확정 금지:
- authoritative source
- 법적 효력·라이선스 적합성
- retention·PII 처리 근거
- tenant/role 접근정책
- 충돌 우선순위

미결정 고위험 항목은 질문 또는 blocked로 남긴다.

## 10. Local ingestion·retrieval

- network 없음
- secret 없음
- 허용 경로만
- bounded bytes/records/time
- raw/canonical digest
- deterministic source unit ID
- source line/record/span locator
- parent ACL·sensitivity 상속
- candidate snapshot은 active production index가 아님

`lexical_local`은 로컬 결정적 검색 후보일 뿐 기업 검색엔진과 동일 성능을 주장하지 않는다.

## 11. Eval·mutation·audit

필수 결과:

```text
KNOW 84/84
KINV 100/100
KEVAL 64/64
KMUT 26/26 killed
Planner Knowledge golden 22/22
```

Critical mutation 생존 0건.

`knowledge-rag-auditor.md`는 future Claude Code용 읽기 전용 blind-first 정의다. 실제 별도 identity가 실행되지 않았다면 다음을 기록한다.

```text
actual_independent_executor_ran: false
independence_status: UNVERIFIED
attestation: false
```

동일 Codex 프로세스의 재검토를 독립 감사로 과장하지 않는다.

## 12. 증거와 완료

구조화 증거:

```text
docs/agent-authoring/evidence/knowledge-rag-builder/
```

최종 구현 결과:

```text
docs/agent-authoring/KNOWLEDGE_RAG_BUILDER_MVP_구현결과.md
```

로컬 완료 상태는 다음처럼 분리한다.

```yaml
local_candidate:
  status: PASS_LOCAL_PROCEDURE
  scope: contract_bound_local_knowledge_candidate

assembler_design_handoff:
  permitted: true

operational_assembly:
  permitted: false
  status: HARD_ENFORCEMENT_UNAVAILABLE
```

다음을 모두 충족해야 K0~K6 완료다.

- KNOW 84/84, KINV 100/100, KEVAL 64/64, KMUT 26/26 killed
- Planner golden 22/22
- Planner/Gate/Execution preflight current
- no-RAG 경로의 불필요 artifact 0
- 지원 parser/retrieval만 실제 구현
- source authority·ACL 미정의 거짓 PASS 0
- ACL·secret·삭제·injection critical mutation 생존 0
- citation support·completeness 검사
- 양방향 traceability 폐쇄
- 별도 audit identity 미실행 시 UNVERIFIED
- production index·IAM·write·secret operation 0

최종 응답에는 구현 파일, 테스트 결과, blocked/unavailable 항목, evidence 경로, Git 변경 범위를 요약한다.
