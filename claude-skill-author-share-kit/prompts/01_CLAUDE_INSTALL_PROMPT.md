# A 세션용 Claude Skill Author v1.3 안전 설치 지시문

현재 Claude Code가 열린 Git 저장소에 `claude-skill-author` v1.3을 설치하고 설치 결과만 검증하라. 이번 세션에서는 대상 업무 스킬을 만들지 않는다.

## 패키지 위치

다음 두 후보만 순서대로 확인한다.

1. `packages/claude-skill-author-package_20260828_v1.3.zip`
2. `claude-skill-author-package_20260828_v1.3.zip`

정확히 하나가 있으면 사용한다. 둘 다 있으면 SHA-256이 같은지 확인하고, 다르면 임의로 선택하지 않고 중단한다. 둘 다 없으면 저장소 전체나 인터넷을 추측 검색하지 말고 누락 경로를 보고한다.

## 작업 원칙

- 기존 사용자 변경을 되돌리지 않는다.
- 커밋·푸시·브랜치 변경·PR 생성은 하지 않는다.
- `.claude/settings.json`을 수정하거나 Stop 훅을 자동 활성화하지 않는다.
- 패키지 테스트가 실패하면 설치하지 않는다.
- 예상하지 못한 네트워크 호출, 자격증명 접근, 제품 코드 수정 또는 파괴적 명령이 있으면 중단한다.

## 수행 순서

1. 저장소 루트와 현재 변경을 확인한다.

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"
git status --short
```

2. 패키지 ZIP을 시스템 임시 디렉터리에 해제한다. `unzip`이 없으면 Python 표준 라이브러리 `zipfile`을 사용하고 외부 패키지는 설치하지 않는다.

3. 설치 전에 다음을 처음부터 끝까지 읽는다.

```text
INSTALL.md
install.sh
tests/run_tests.py
.claude/skills/claude-skill-author/SKILL.md
.claude/skills/claude-skill-author/scripts/init_authoring.py
.claude/skills/claude-skill-author/scripts/validate_authoring.py
.claude/skills/claude-skill-author/scripts/seal_attestation.py
.claude/skills/claude-skill-author/scripts/stop_gate.py
.claude/agents/skill-design-author.md
.claude/agents/skill-design-auditor.md
.claude/agents/skill-author-auditor.md
.claude/settings.stop-hook.example.json
```

4. 다음을 확인한다.

- 설치 대상이 현재 저장소의 `.claude/` 하위로 제한되는가
- 기존 파일을 `.bak-<UTC시각>`으로 백업하는가
- 네트워크·Git 쓰기·제품 코드 수정·자격증명 접근이 없는가
- `.claude/settings.json`을 자동 수정하지 않는가

5. 이상이 없을 때만 패키지 디렉터리에서 실행한다.

```bash
python3 tests/run_tests.py
```

6. 테스트 종료코드가 0일 때만 설치한다.

```bash
chmod +x install.sh
./install.sh "$PROJECT_ROOT"
```

7. 설치 후 다음 파일이 존재하는지 확인한다.

```text
.claude/skills/claude-skill-author/SKILL.md
.claude/agents/skill-design-author.md
.claude/agents/skill-design-auditor.md
.claude/agents/skill-author-auditor.md
.claude/settings.stop-hook.example.json
```

8. 설치된 네 Python 스크립트에 `python3 -m py_compile`을 실행한다.

9. 최종 변경 범위를 확인한다.

```bash
git status --short
git diff -- .claude
```

## 최종 보고

다음만 보고한다.

- 설치 성공 또는 실패
- 사용한 패키지 경로와 SHA-256
- 패키지 자체 테스트 결과
- 생성·백업된 경로
- Python 구문 검사 결과
- 예상 밖 변경 여부
- Claude Code 새 세션 시작 필요 여부

이번 요청에서는 `/claude-skill-author`를 실행하여 다른 스킬을 생성하지 않는다.
