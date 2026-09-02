# Claude에게 전달할 저장소 반영·설치·공유 준비 통합 지시문

현재 Claude Code가 열린 Git 저장소에 첨부된 Claude Skill Author 공유 번들 v1.3.1(설치 엔진 v1.3.0)을 안전하게 반영하고 설치 검증까지 수행하라.

## 실행 설정

- 공유 자료 반영: `yes`
- 현재 저장소에 메타 스킬 설치: `yes`
- Git 커밋: `no`
- Git 푸시: `no`

`Git 커밋` 또는 `Git 푸시`를 `yes`로 바꾸려면 사용자가 대상 브랜치, 포함할 파일, 커밋 메시지와 원격 저장소를 명시해야 한다. 하나의 승인으로 커밋과 푸시를 동시에 승인한 것으로 해석하지 않는다.

## 첨부 또는 저장소 루트에서 찾을 파일

- `claude-skill-author-package_20260828_v1.3.zip`
- `README_KO.md`
- `BACKGROUND_AND_REFERENCES_KO.md`
- `01_CLAUDE_INSTALL_PROMPT.md`
- `02_METHOD_1_PREPARED_DESIGN_PROMPT.md`
- `03_METHOD_2_NATURAL_LANGUAGE_PROMPT.md`
- `04_CLAUDE_REPOSITORY_SETUP_AND_SHARE_PROMPT.md`
- `ATTACHMENT_MANIFEST.md`
- `BUNDLE_INFO.json`
- `SHA256SUMS.txt`

파일명이 다른 위치에 있으면 현재 저장소와 대화 첨부파일에서 정확한 경로를 확인한다. 동일 이름이 여러 개면 임의로 선택하지 않는다.

## 목표 저장 구조

```text
<저장소 루트>/
├── README_KO.md
├── BACKGROUND_AND_REFERENCES_KO.md
├── packages/
│   └── claude-skill-author-package_20260828_v1.3.zip
├── prompts/
│   ├── 01_CLAUDE_INSTALL_PROMPT.md
│   ├── 02_METHOD_1_PREPARED_DESIGN_PROMPT.md
│   ├── 03_METHOD_2_NATURAL_LANGUAGE_PROMPT.md
│   └── 04_CLAUDE_REPOSITORY_SETUP_AND_SHARE_PROMPT.md
├── ATTACHMENT_MANIFEST.md
├── BUNDLE_INFO.json
└── SHA256SUMS.txt
```

## 작업 원칙

1. `git rev-parse --show-toplevel`과 `git status --short`로 저장소 루트와 기존 사용자 변경을 확인한다.
2. 대상과 무관한 파일을 수정하거나 기존 사용자 변경을 되돌리지 않는다.
3. 같은 경로의 기존 파일이 있으면 내용을 비교한다. 무조건 덮어쓰지 말고 기존 사용자 내용 보존 또는 `.bak-<UTC시각>` 백업 방식을 선택하고 결과를 기록한다.
4. 첨부된 패키지를 재구성하거나 임의로 수정하지 않는다. 제공된 ZIP을 그대로 `packages/`에 배치한다.
5. `SHA256SUMS.txt`와 실제 파일 digest가 다르면 설치하지 않고 중단한다.
6. `.claude/settings.json`을 덮어쓰거나 Stop 훅을 자동 활성화하지 않는다.
7. 커밋·푸시·브랜치 변경·PR 생성은 이번 요청에 명시적 승인이 없는 한 수행하지 않는다.

## 1단계. 공유 자료 반영

1. 위 목표 구조를 만든다.
2. 가이드와 프롬프트 파일을 정확한 경로로 복사한다.
3. `README_KO.md` 안에서 참조하는 패키지·프롬프트 파일이 실제 존재하는지 확인한다.
4. Markdown 코드 펜스와 제목 구조가 깨지지 않았는지 검사한다.
5. 저장소 루트에 기존 `README.md` 또는 `README_KO.md`가 있으면 자동으로 대체하지 않는다. 기존 문서와 통합이 필요하면 변경안을 먼저 제시한다.

## 2단계. 패키지 보안 검토와 테스트

`packages/claude-skill-author-package_20260828_v1.3.zip`을 시스템 임시 디렉터리에 해제하고 다음을 읽는다.

- `INSTALL.md`
- `install.sh`
- `tests/run_tests.py`
- `.claude/skills/claude-skill-author/SKILL.md`
- 네 Python 스크립트
- 세 Agent 정의
- Stop 훅 예시

다음을 확인한다.

- 설치 범위가 현재 저장소의 `.claude/` 하위인가
- 기존 파일을 백업하는가
- 네트워크 호출·Git 쓰기·제품 코드 수정·자격증명 접근이 없는가
- `.claude/settings.json`을 자동 수정하지 않는가

이상이 없을 때만 패키지 디렉터리에서 실행한다.

```bash
python3 tests/run_tests.py
```

종료코드가 0이 아니면 설치하지 않는다.

## 3단계. 현재 저장소에 설치

패키지 테스트가 통과한 경우에만 패키지 디렉터리에서 다음과 동등한 설치를 수행한다.

```bash
./install.sh "$(git rev-parse --show-toplevel)"
```

설치 후 다음을 확인한다.

```text
.claude/skills/claude-skill-author/SKILL.md
.claude/agents/skill-design-author.md
.claude/agents/skill-design-auditor.md
.claude/agents/skill-author-auditor.md
.claude/settings.stop-hook.example.json
```

모든 Python 스크립트에 `python3 -m py_compile`을 실행한다.

## 4단계. 사용 경로 검증

가이드가 다음 두 경로를 모두 정확히 설명하는지 확인한다.

1. 준비된 설계서 사용

```text
/claude-skill-author <스킬명> --design <설계서>
```

2. 자연어 애로사항 사용

```text
/claude-skill-author <스킬명>
```

가이드는 `--mode full --agent auto`가 생략 시 적용되는 기본값임을 명시해야 한다.

두 경로 모두 최종 `design → spec → build → audit` 제작 엔진을 공유한다는 설명이 있어야 한다.

## 5단계. 최종 검증

```bash
git status --short
git diff -- README_KO.md BACKGROUND_AND_REFERENCES_KO.md packages prompts .claude SHA256SUMS.txt
```

다음을 보고한다.

- 반영한 공유 파일 경로
- 설치된 `.claude/` 파일 경로
- 기존 파일의 백업 또는 병합 처리
- SHA-256 검사 결과
- 패키지 테스트 결과
- Python 구문 검사 결과
- 예상 밖 변경 여부
- Claude Code 재시작 필요 여부
- 커밋·푸시를 수행하지 않았다는 확인

이번 요청에서는 예시 대상 업무 스킬을 생성하지 않는다.
## 6단계. 선택적 Git 게시

기본값은 커밋과 푸시를 수행하지 않는 것이다. `실행 설정`에서 사용자가 각각 `yes`로 명시한 경우에만 다음을 수행한다.

1. `git status --short`와 `git diff --stat`으로 포함 범위를 다시 보여준다.
2. 공유 자료와 설치 파일만 명시적으로 stage한다. `git add .`, `git add -A`, `git add --all`은 사용하지 않는다.
3. 기존 사용자 변경이나 무관한 파일을 stage하지 않는다.
4. 커밋 승인만 있으면 커밋까지만 수행한다.
5. 푸시는 별도의 명시적 승인이 있고 원격·브랜치가 확인된 경우에만 수행한다.
6. 푸시 결과를 원격 브랜치와 커밋 SHA로 검증한다.

