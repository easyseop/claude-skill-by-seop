# Planner·Gate·Execution 선행 구현 복구 세션 시작 지시

너는 현재 저장소의 **선행 구현 복구 담당 Codex 구현 세션**이다.

현재 저장소가 `easyseop/claude-skill-by-seop`, 현재 브랜치가 `recovery/upstream-builders`인지 확인한다. 다르면 작업하지 않고 `BLOCKED_FOR_DECISION`으로 기록한다.

## 1. 읽기 순서

1. 저장소와 현재 경로의 `AGENTS.md`
2. 이 파일
3. `WORK_ORDER.md`
4. `OWNERSHIP.yaml`
5. `CURRENT_SESSION_STATE.yaml`
6. `HANDOFF_LOG.md`
7. `INPUT_MANIFEST.yaml`
8. `inputs/*.json`
9. 공통 세션 협업 규약

## 2. 시작 전 Preflight

- 현재 branch 확인
- `git status --short`, `git diff --name-only` 확인
- `OWNERSHIP.yaml`의 writable/read-only/forbidden 경계 확인
- `INPUT_MANIFEST.yaml`에 등록된 모든 파일 존재와 digest 확인
- compact catalog의 ID 수와 연속성 확인

필수 입력 수량:

```text
CAP 36
Planner EVAL 22
GATE 80
Gate invariant 85
Gate eval 48
EXEC 30
EXI 45
EXEVAL 26
EXMUT 10
```

입력 누락·digest mismatch·ID 중복/누락이 있으면 다른 자료로 임의 보완하지 않고 `BLOCKED_FOR_SOURCE`로 전환한다.

Preflight가 통과하면:

```text
CURRENT_SESSION_STATE.yaml → IN_PROGRESS, phase=P
HANDOFF_LOG.md에 시작 기록 append
```

## 3. 작업 순서

다음 순서를 바꾸지 않는다.

```text
P. Capability & Artifact Planner
→ P 자체 테스트·mutation·evidence·report
→ G. Gate Generator M0~M3
→ G 자체 테스트·mutation·Hook smoke·evidence·report
→ E. Execution Artifact Generator E0~E4
→ E 자체 테스트·mutation·builder·trace·evidence·report
```

앞 단계가 현재 source에 대해 통과하지 않으면 다음 단계로 이동하지 않는다.

## 4. 담당 경계

수정 허용 경로는 `OWNERSHIP.yaml.writable_paths`뿐이다.

읽기 전용 입력과 `claude-skill-author`를 수정하지 않는다.

다음은 절대 수정하지 않는다.

```text
.claude/settings.json
.github/**
Knowledge/RAG Builder workstream
Assembler research workstream
session-collaboration 공통 작업판
main branch
```

다른 workstream 파일이 이미 변경돼 있으면 건드리지 않고 blocker로 기록한다.

## 5. 구현·검증 원칙

- 입력 catalog에서 규칙·평가를 자동 추출한다.
- 과거 구현결과 보고서를 현재 PASS 증거로 재사용하지 않는다.
- 실제 source와 실제 테스트를 새로 만든다.
- 자유문자 PASS·exit code 0·파일 존재만으로 완료하지 않는다.
- source·checker·test·evidence digest를 결박한다.
- 변경된 subject에 오래된 evidence를 사용하지 않는다.
- 별도 감사 identity가 없으면 `UNVERIFIED`로 기록한다.
- Host Hook·sandbox·production permission이 실제로 활성화되지 않았으면 `HARD_ENFORCEMENT_UNAVAILABLE`로 기록한다.
- production DB/API write, secret 수집, 외부 배포를 수행하지 않는다.

## 6. 완료

전체 P→G→E가 통과하면:

1. 세 결과 보고서를 작성한다.
2. 세 evidence 디렉터리에 구조화 결과를 보존한다.
3. `OUTPUT_MANIFEST.yaml`에 source·test·evidence·report와 digest를 기록한다.
4. 경로 경계 검사를 실행하고 위반 0건을 확인한다.
5. `CURRENT_SESSION_STATE.yaml`을 `READY_FOR_REVIEW`로 변경한다.
6. `HANDOFF_LOG.md`에 커밋, 테스트 명령, 수량, 결과, 미검증 범위, 다음 행동을 append한다.
7. Draft PR에 요약을 남기되 merge하지 않는다.

main 직접 변경, branch 전환, force push, 자동 병합을 하지 않는다.
