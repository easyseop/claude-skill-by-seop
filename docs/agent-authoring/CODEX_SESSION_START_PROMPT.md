# Codex 세션 시작 지시문

아래 내용을 새 Codex 세션에 그대로 전달한다.

```text
저장소: easyseop/claude-skill-by-seop
작업 브랜치: codex/knowledge-rag-builder-k0-k6

너는 이 저장소의 Knowledge & RAG Builder K0~K6 구현 담당 Codex다.

먼저 저장소 루트와 브랜치를 확인하고, 반드시 다음 순서로 읽어라.

1. 저장소 루트 및 하위 경로의 AGENTS.md
2. docs/agent-authoring/CODEX_COLLABORATION_PROTOCOL.md
3. docs/agent-authoring/CURRENT_WORK_STATE.yaml
4. docs/agent-authoring/HANDOFF_LOG.md
5. docs/agent-authoring/CODEX_KNOWLEDGE_RAG_BUILDER_K0_K6_WORK_ORDER.md

이번 작업의 공식 상태와 인수인계는 GitHub의 다음 두 파일로만 교환한다.

- docs/agent-authoring/CURRENT_WORK_STATE.yaml
- docs/agent-authoring/HANDOFF_LOG.md

작업 시작 직후:

1. CURRENT_WORK_STATE.yaml의 status를 IN_PROGRESS로 바꾼다.
2. HANDOFF_LOG.md에 시작 시각, 기준 commit, 이해한 범위, 예상 변경 경로를 추가한다.
3. K0 preflight부터 수행한다.
4. K0가 실패하면 K1 이후로 진행하지 말고 status를 BLOCKED_FOR_DECISION으로 바꾼다.
5. 저장소 사실로 해결할 수 있는 문제는 사용자에게 묻지 않는다.

구현 범위:

- K0 research closure·input binding
- K1 minimality compiler
- K2 source governance
- K3 제한된 local ingestion
- K4 local lexical·structured retrieval
- K5 security·freshness contract
- K6 citation·eval·mutation·procedural audit candidate

금지:

- main 직접 수정
- force push·history rewrite
- PR 자동 병합
- production RAG/index 배포
- 실제 IAM·tenant ACL·RLS/DLS 변경
- 운영 secret·credential 수집
- 외부 vector DB·embedding API·reranker 설치 또는 호출
- 운영 DB/API write
- .claude/settings.json 수정
- 실행하지 않은 테스트·감사를 PASS로 표시
- 같은 Codex 실행을 독립 감사 identity로 주장

필수 결과:

- prompt coverage unresolved 0
- KNOW 84/84
- KINV 100/100
- KEVAL 64/64
- KMUT 26/26 killed
- Planner knowledge golden 22/22
- critical mutant survived 0
- traceability closed
- unsupported parser/runtime 거짓 구현 0

완료 시:

1. docs/agent-authoring/KNOWLEDGE_RAG_BUILDER_MVP_구현결과.md를 작성한다.
2. docs/agent-authoring/evidence/knowledge-rag-builder/ 아래 구조화 evidence를 보존한다.
3. CURRENT_WORK_STATE.yaml을 READY_FOR_REVIEW로 변경한다.
4. HANDOFF_LOG.md에 커밋 목록, 테스트 명령, 결과, 미검증·unavailable 범위, 검토 요청을 추가한다.
5. Draft PR에 결과 요약을 남기되 merge하지 않는다.

자유문자 PASS, exit 0, 파일 존재만으로 완료하지 않는다. 실제 구조화 evidence와 현재 digest가 우선한다.
```
