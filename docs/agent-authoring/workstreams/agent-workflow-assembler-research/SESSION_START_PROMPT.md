# Agent & Workflow Assembler 조사 세션 시작 지시

너는 구현 세션이 아니라 **독립 심층조사 세션**이다.

현재 저장소가 `easyseop/claude-skill-by-seop`, 현재 브랜치가 `research/agent-workflow-assembler`인지 확인한다. 다르면 작업하지 않고 `BLOCKED_FOR_DECISION`으로 기록한다.

## 1. 읽기 순서

1. 저장소와 현재 경로의 `AGENTS.md`
2. 이 파일
3. `WORK_ORDER.md`
4. `OWNERSHIP.yaml`
5. `CURRENT_SESSION_STATE.yaml`
6. `HANDOFF_LOG.md`
7. `INPUT_MANIFEST.yaml`
8. `inputs/UPSTREAM_CONTRACT_SUMMARY.md`
9. 필요한 현재 공식 외부 자료

## 2. 시작 전 Preflight

다음을 실행·확인한다.

```text
현재 branch
현재 Git status와 diff
입력 파일 존재와 digest
OWNERSHIP writable/read-only/forbidden 경로
조사 결과 출력 경로
```

입력이 없거나 digest가 다르면 임의 자료로 대체하지 않고 `BLOCKED_FOR_SOURCE`로 전환한다.

Preflight가 통과하면:

```text
CURRENT_SESSION_STATE.yaml: IN_PROGRESS
HANDOFF_LOG.md: 시작 기록 append
```

## 3. 작업 경계

수정 허용:

```text
CURRENT_SESSION_STATE.yaml
HANDOFF_LOG.md
OUTPUT_MANIFEST.yaml
docs/agent-authoring/research-results/05_AGENT_WORKFLOW_ASSEMBLER_심층조사.md
```

다른 파일은 읽기 전용 또는 금지다. 특히 `.claude/**`, `.github/**`, 다른 workstream의 상태·evidence·결과를 수정하지 않는다.

조사 중 상위 계약 누락이나 충돌을 발견하면 해당 구현을 직접 고치지 않고 다음 중 하나를 결과에 기록한다.

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
- 코드·설정·branch·PR을 변경하지 않음

## 5. 완료 조건

- `WORK_ORDER.md`의 25개 섹션을 빠짐없이 작성
- `ASM-*`, `AINV-*`, `AEVAL-*`, `AMUT-*`를 연속 ID로 작성
- Planner 22개 Assembly golden mapping 작성
- 규칙 수·불변식 수·평가 수·mutation 수 보고
- 결론-출처 추적표와 전체 출처 포함
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

자동 병합, main 직접 변경, force push를 하지 않는다.
