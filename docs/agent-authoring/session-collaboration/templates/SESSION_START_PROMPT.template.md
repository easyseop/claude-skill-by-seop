# <SESSION_TYPE> 세션 시작 지시

너는 `<SESSION_TYPE>` 세션이다. 현재 저장소와 브랜치를 확인한 뒤 이 workstream에 할당된 작업만 수행한다.

## 1. 먼저 읽을 파일

1. 저장소와 현재 경로의 `AGENTS.md`
2. 이 `SESSION_START_PROMPT.md`
3. `WORK_ORDER.md`
4. `OWNERSHIP.yaml`
5. `CURRENT_SESSION_STATE.yaml`
6. `HANDOFF_LOG.md`
7. `INPUT_MANIFEST.yaml`에 등록된 입력

## 2. 시작 전 검사

- 현재 branch가 `OWNERSHIP.yaml.branch`와 일치하는지 확인한다.
- 입력 파일 존재와 digest를 검증한다.
- 변경 전 `git status --short`, `git diff --name-only`를 확인한다.
- 다른 workstream의 파일이 이미 변경돼 있으면 건드리지 않고 blocker로 기록한다.
- 상태를 `IN_PROGRESS`로 전환하고 `HANDOFF_LOG.md`에 시작 기록을 append한다.

## 3. 범위

- `OWNERSHIP.yaml.writable_paths` 안에서만 수정한다.
- `read_only_paths`는 읽기만 한다.
- `forbidden_paths`는 수정하지 않는다.
- 상위 계약을 임의 변경하지 않는다.
- 범위 밖 필요성이 생기면 `REENTRY_REQUIRED` 또는 `BLOCKED_FOR_DECISION`을 기록한다.

## 4. 완료

- 실제 테스트·검사·evidence를 생성한다.
- `OUTPUT_MANIFEST.yaml`에 파일과 digest를 기록한다.
- 상태를 `READY_FOR_REVIEW`로 전환한다.
- `HANDOFF_LOG.md`에 수행 내용, 검증 결과, 미검증 범위, 다음 행동을 append한다.
- 자동 병합, main 직접 변경, force push를 하지 않는다.
