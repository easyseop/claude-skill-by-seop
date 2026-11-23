# Planner·Gate·Execution 선행 구현 복구 세션 시작 지시

너는 현재 저장소의 **선행 구현 복구 담당 구현 세션**이다.

대상 저장소와 작업 브랜치:

```text
repository: easyseop/claude-skill-by-seop
branch: recovery/upstream-builders
```

로컬 checkout이 대상 브랜치가 아니거나 사용자 변경이 있어도 해당 작업트리를 건드리지 않는다. GitHub 커넥터로 대상 브랜치를 읽고 쓸 수 있으면 `REMOTE_CONNECTOR_MODE.md`에 따라 격리된 임시 작업공간에서 계속 진행한다.

## 1. 읽기 순서

1. 저장소와 현재 경로의 `AGENTS.md`
2. 이 파일
3. `REMOTE_CONNECTOR_MODE.md`
4. `WORK_ORDER.md`
5. `OWNERSHIP.yaml`
6. `CURRENT_SESSION_STATE.yaml`
7. `HANDOFF_LOG.md`
8. `INPUT_MANIFEST.yaml`
9. `inputs/*.json`
10. 공통 세션 협업 규약

## 2. 실행 모드 선택

### Local Branch Mode

현재 로컬 checkout이 `recovery/upstream-builders`이고 담당 범위 밖 변경이 없을 때 사용한다.

### Remote Connector Mode

다음 중 하나이면 사용한다.

- 현재 로컬 checkout이 `main` 또는 다른 브랜치
- 사용자 미추적 변경이 존재
- shell의 `git clone/fetch/worktree`가 DNS·네트워크 문제로 실패
- GitHub 커넥터는 대상 브랜치를 읽고 쓸 수 있음

Remote Connector Mode에서는 현재 로컬 Git 작업트리를 수정·stash·삭제하지 않는다. scratch workspace에서 구현·테스트한 뒤 검증된 파일만 GitHub 커넥터로 대상 브랜치에 쓴다.

로컬 checkout 불일치나 shell DNS 실패만으로 중단하지 않는다.

## 3. 시작 전 Preflight

- 대상 branch의 현재 head SHA 확인
- `OWNERSHIP.yaml`의 writable/read-only/forbidden 경계 확인
- `INPUT_MANIFEST.yaml`에 등록된 모든 파일 존재와 Git blob SHA 확인
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
HANDOFF_LOG.md에 실행 모드·기준 commit·검증 결과 append
```

## 4. 작업 순서

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

## 5. 담당 경계

수정 허용 경로는 `OWNERSHIP.yaml.writable_paths`뿐이다.

다음은 절대 수정하지 않는다.

```text
현재 사용자 로컬 작업트리와 미추적 파일
.claude/settings.json
.github/**
Knowledge/RAG Builder workstream
Assembler research workstream
session-collaboration 공통 작업판
main branch
```

모든 GitHub 쓰기는 `recovery/upstream-builders` 브랜치를 명시한다.

## 6. 구현·검증 원칙

- 입력 catalog에서 규칙·평가를 자동 추출한다.
- 과거 구현결과 보고서를 현재 PASS 증거로 재사용하지 않는다.
- 실제 source와 실제 테스트를 새로 만든다.
- 자유문자 PASS·exit code 0·파일 존재만으로 완료하지 않는다.
- source·checker·test·evidence digest를 결박한다.
- 변경된 subject에 오래된 evidence를 사용하지 않는다.
- 별도 감사 identity가 없으면 `UNVERIFIED`로 기록한다.
- Host Hook·sandbox·production permission이 활성화되지 않았으면 `HARD_ENFORCEMENT_UNAVAILABLE`로 기록한다.
- production DB/API write, secret 수집, 외부 배포를 수행하지 않는다.

## 7. 완료

전체 P→G→E가 통과하면:

1. 세 결과 보고서를 작성한다.
2. 세 evidence 디렉터리에 구조화 결과를 보존한다.
3. `OUTPUT_MANIFEST.yaml`에 source·test·evidence·report와 SHA-256을 기록한다.
4. 경로 경계 위반 0건을 확인한다.
5. `CURRENT_SESSION_STATE.yaml`을 `READY_FOR_REVIEW`로 변경한다.
6. `HANDOFF_LOG.md`에 커밋, 테스트 명령, 수량, 결과, 미검증 범위, 다음 행동을 append한다.
7. Draft PR에 요약을 남기되 merge하지 않는다.

중간 확인을 기다리지 말고 담당 범위 안에서 계속 진행한다. main 직접 변경, force push, 자동 병합을 하지 않는다.
