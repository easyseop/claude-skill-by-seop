# Agent & Workflow Assembler 조사 세션 시작 지시

너는 구현 세션이 아니라 **독립 심층조사 세션**이다.

대상:

```text
repository: easyseop/claude-skill-by-seop
branch: research/agent-workflow-assembler
```

로컬 checkout이 대상 브랜치가 아니거나 사용자 변경이 있어도 해당 작업트리를 건드리지 않는다. GitHub 커넥터로 조사 브랜치를 읽고 쓸 수 있으면 `REMOTE_RESEARCH_MODE.md`에 따라 계속한다.

## 1. 읽기 순서

1. 저장소와 현재 경로의 `AGENTS.md`
2. 이 파일
3. `REMOTE_RESEARCH_MODE.md`
4. `WORK_ORDER.md`
5. `OWNERSHIP.yaml`
6. `CURRENT_SESSION_STATE.yaml`
7. `HANDOFF_LOG.md`
8. `INPUT_MANIFEST.yaml`
9. `inputs/UPSTREAM_CONTRACT_SUMMARY.md`
10. 필요한 현재 공식 외부 자료

## 2. Preflight

- GitHub의 대상 branch head 확인
- 입력 파일 존재와 Git blob SHA 확인
- `OWNERSHIP.yaml`의 writable/read-only/forbidden 경계 확인
- 조사 결과 출력 경로 확인

입력이 없거나 digest가 다르면 임의 자료로 대체하지 않고 `BLOCKED_FOR_SOURCE`로 전환한다.

로컬 branch 불일치·사용자 미추적 변경·shell DNS 실패만으로 중단하지 않는다. GitHub 커넥터로 입력을 읽고 허용 경로에 쓸 수 있으면 Remote Research Mode로 진행한다.

Preflight 통과 후:

```text
CURRENT_SESSION_STATE.yaml: IN_PROGRESS
HANDOFF_LOG.md: 실행 모드·기준 commit·시작 기록 append
```

## 3. 작업 경계

수정 허용:

```text
CURRENT_SESSION_STATE.yaml
HANDOFF_LOG.md
OUTPUT_MANIFEST.yaml
docs/agent-authoring/research-results/05_AGENT_WORKFLOW_ASSEMBLER_심층조사.md
```

다른 파일은 읽기 전용 또는 금지다. 특히 `.claude/**`, `.github/**`, 구현 source·evidence, 다른 workstream 상태·결과를 수정하지 않는다.

상위 계약 누락·충돌을 발견하면 직접 고치지 않고 다음 중 하나를 결과에 기록한다.

```text
PLANNER_REENTRY_REQUIRED
GATE_REENTRY_REQUIRED
EXECUTION_REENTRY_REQUIRED
KNOWLEDGE_REENTRY_REQUIRED
```

## 4. 조사 방식

- 공식 규격·공식 제품 문서·공식 저장소·원 논문 우선
- 현재 기능·연구 결과·설계 제안 분리
- 최신 기능은 기준일·버전·commit 기록
- Claude Code 전용 규칙과 제품 독립 규칙 분리
- 출처 없는 수치·예산·timeout을 범용 규범으로 만들지 않음
- 구현되지 않은 기능을 구현 사실처럼 쓰지 않음
- 조사 결과 외 코드·설정·branch·PR 변경 금지

## 5. 완료 조건

- `WORK_ORDER.md`의 25개 섹션 작성
- `ASM-*`, `AINV-*`, `AEVAL-*`, `AMUT-*` 연속 ID
- Planner 22개 Assembly golden mapping
- 규칙·불변식·평가·mutation 수량 보고
- 결론-출처 추적표와 전체 출처
- 미확인·실제 구현 필요사항 명시

결과 경로:

```text
docs/agent-authoring/research-results/05_AGENT_WORKFLOW_ASSEMBLER_심층조사.md
```

완료 후:

```text
OUTPUT_MANIFEST.yaml 갱신
CURRENT_SESSION_STATE.yaml: READY_FOR_REVIEW
HANDOFF_LOG.md: 결과·검증·한계·다음 행동 append
```

중간 확인을 기다리지 말고 담당 범위 안에서 계속 진행한다. 자동 병합, main 직접 변경, force push를 하지 않는다.
