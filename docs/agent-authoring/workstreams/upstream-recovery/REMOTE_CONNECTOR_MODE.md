# Remote Connector Mode

## 목적

로컬 checkout이 `main`이거나 사용자 미추적 변경이 있어도 해당 작업트리를 수정하지 않고, GitHub 커넥터와 격리된 임시 작업공간으로 `recovery/upstream-builders` 브랜치의 작업을 계속한다.

이 모드는 shell의 `github.com` DNS 실패와 무관하게 GitHub 커넥터가 대상 브랜치를 읽고 쓸 수 있을 때 사용한다.

## 적용 조건

다음 중 하나이면 Remote Connector Mode를 선택한다.

- 현재 로컬 checkout이 대상 브랜치가 아님
- 현재 작업트리에 담당 범위 밖 사용자 변경이 있음
- `git clone`, `git fetch`, `git worktree`가 네트워크 문제로 불가능함
- GitHub 커넥터로 대상 브랜치의 파일 읽기·쓰기가 가능함

## 하드 경계

- 현재 로컬 저장소와 사용자 미추적 파일을 수정·삭제·stash하지 않는다.
- `main`에 쓰지 않는다.
- 모든 GitHub 쓰기는 `recovery/upstream-builders` 브랜치를 명시한다.
- `OWNERSHIP.yaml.writable_paths` 밖을 쓰지 않는다.
- `.claude/settings.json`, `.github/**`, Knowledge/RAG, Assembler 조사 경로를 수정하지 않는다.
- 별도 독립 감사 identity가 실제로 실행되지 않았으면 `UNVERIFIED`로 기록한다.

## 수행 절차

1. GitHub 커넥터에서 다음을 직접 읽는다.
   - `SESSION_START_PROMPT.md`
   - `WORK_ORDER.md`
   - `OWNERSHIP.yaml`
   - `INPUT_MANIFEST.yaml`
   - `inputs/*.json`
   - 현재 브랜치 head SHA
2. `INPUT_MANIFEST.yaml`의 Git blob SHA와 실제 입력 blob SHA를 대조한다.
3. `/tmp` 또는 세션의 격리 임시 디렉터리에 빈 scratch workspace를 만든다.
4. 필요한 입력 파일만 scratch workspace에 복사한다. 현재 로컬 Git 작업트리를 입력으로 사용하지 않는다.
5. scratch workspace에서 Planner → Gate → Execution 순서로 source·tests·evidence를 생성하고 테스트한다.
6. 각 단계가 통과할 때마다 생성 파일의 SHA-256과 테스트 결과를 구조화 evidence로 남긴다.
7. 검증된 파일만 GitHub 커넥터로 `recovery/upstream-builders` 브랜치에 커밋한다.
8. 커밋 직후 GitHub에서 다시 읽어 파일 digest와 경로 범위를 검증한다.
9. `CURRENT_SESSION_STATE.yaml`, `HANDOFF_LOG.md`, `OUTPUT_MANIFEST.yaml`을 갱신한다.

## 진행 순서

```text
P. Capability Planner
→ 실제 테스트·mutation·evidence
→ G. Gate Generator M0~M3
→ 실제 테스트·mutation·Hook smoke·evidence
→ E. Execution Artifact Generator E0~E4
→ 실제 테스트·mutation·builder·trace·evidence
```

앞 단계가 current source에 대해 통과하기 전에는 다음 단계로 이동하지 않는다.

## 차단 조건

다음 경우에만 `BLOCKED_FOR_SOURCE` 또는 `BLOCKED_FOR_DECISION`으로 멈춘다.

- GitHub 커넥터도 대상 브랜치를 읽거나 쓸 수 없음
- sealed input blob SHA 불일치
- catalog ID 누락·중복·손상
- ownership 경계 안에서 필수 산출물을 만들 수 없음
- 사용자 정책 결정 없이는 고위험 계약을 확정할 수 없음

단순히 로컬 checkout이 `main`이거나 shell DNS가 실패한다는 이유만으로 멈추지 않는다.

## 완료 판정

Remote Connector Mode에서 생성한 결과도 Work Order의 모든 수량·mutation·trace·evidence 기준을 동일하게 충족해야 한다. 자유문자 PASS, 파일 존재, exit code 0만으로 완료하지 않는다.
