# Claude Skill Author v1.3.1 설치·사용·공유 가이드

> 문서 번들 버전은 `v1.3.1`, 설치되는 제작 엔진은 `claude-skill-author v1.3.0`이다. 이번 개정은 엔진 변경 없이 사용법·적합 용도·조사 배경을 보강한 문서 개정본이다.

> 자연어 애로사항 또는 이미 정리된 설계서를 입력으로 받아, 요구사항 수립·독립 설계 감사·규칙 전수 판정·`SKILL.md` 작성·선택적 `Agent.md` 생성·최종 감사까지 수행하는 고신뢰 Claude Code 스킬 제작 하네스의 사용자 가이드다.


## 가장 간단한 사용법

일반 사용자는 다음 한 줄로 시작한다.

```text
/claude-skill-author <스킬명>

<만들고 싶은 스킬의 애로사항·최종 결과·허용·금지·승인 조건을 자연어로 작성>
```

옵션을 생략하면 다음 기본값을 사용한다.

```yaml
mode: full
agent: auto
```

따라서 다음 두 호출은 같은 의미다.

```text
/claude-skill-author evidence-code-review
```

```text
/claude-skill-author evidence-code-review --mode full --agent auto
```

옵션은 전체 자동 생성이 아닌 다른 흐름이 필요할 때만 명시한다.

| 목적 | 호출 방식 |
|---|---|
| 요구사항 수립부터 설계·작성·감사까지 전체 수행 | 옵션 생략 또는 `--mode full` |
| 설계서까지만 먼저 만들고 검토 | `--mode design` |
| 명세와 규칙 판정까지만 진행 | `--mode spec` |
| 승인된 명세로 파일 작성 | `--mode build` |
| 기존 결과만 독립 감사 | `--mode audit` |
| Agent 필요성을 자동 판단 | 옵션 생략 또는 `--agent auto` |
| 업무용 Agent를 반드시 생성 | `--agent required` |
| 업무용 Agent 생성을 금지 | `--agent forbidden` |

준비된 설계서를 사용할 때는 기본 호출에 `--design`만 추가한다.

```text
/claude-skill-author <스킬명> --design <설계서 경로>
```

## 1. 무엇을 설치하는가

이 패키지를 프로젝트에 설치하면 다음 구성요소가 추가된다.

| 구분 | 설치 위치 | 담당 역할 |
|---|---|---|
| 메타 스킬 | `.claude/skills/claude-skill-author/` | 자연어 또는 설계서를 실제 Claude Code 스킬로 변환한다. |
| 설계 작성자 | `.claude/agents/skill-design-author.md` | 원문 요구와 저장소 사실을 `REQUIREMENT_INTAKE.yaml`과 `DESIGN.md`로 구조화한다. |
| 설계 감사자 | `.claude/agents/skill-design-auditor.md` | 사용자 원문·후속 결정·설계서 사이의 누락, 왜곡, 임의 권한 추가를 읽기 전용으로 감사한다. |
| 최종 스킬 감사자 | `.claude/agents/skill-author-auditor.md` | 설계·명세·규칙과 최종 `SKILL.md`·선택적 `Agent.md`를 양방향으로 감사한다. |
| 검사 스크립트 | 메타 스킬의 `scripts/` | 원문 잠금, 요구사항·설계·규칙 누락, digest, 단계 상태와 최종 PASS를 기계적으로 검사한다. |
| Stop 훅 예시 | `.claude/settings.stop-hook.example.json` | 검증 전 종료를 선택적으로 차단한다. 자동 활성화되지는 않는다. |

이 하네스는 단순히 `SKILL.md` 초안을 생성하는 도구가 아니다. 다음 상태 전이를 통과시킨다.

```text
사용자 입력
→ SOURCE_REQUEST 잠금
→ 요구사항 구조화
→ DESIGN 작성
→ 독립 설계 감사
→ design PASS
→ 규칙 전수 판정·COMMAND_SPEC
→ spec PASS
→ SKILL.md + 필요 시 Agent.md
→ build PASS
→ 독립 최종 감사
→ audit PASS
→ FINAL_STATUS PASS
```

---

## 2. 사용자가 선택할 수 있는 두 가지 방법

두 방법 모두 **최종 스킬 생성 엔진은 동일**하다. 차이는 입력을 어디서 시작하느냐뿐이다.

> 아래 예시는 생략형 호출을 기본으로 사용한다. `--mode full --agent auto`를 붙여도 동일하게 동작한다. 고위험 스킬에서 사람의 명세 승인이 필요할 때만 `--mode spec`을 명시한다.

| 항목 | 방법 1. 준비된 요구사항·설계서 사용 | 방법 2. 자연어 애로사항부터 시작 |
|---|---|---|
| 시작점 | 이미 작성된 `DESIGN.md`, 정책 문서, 요구사항 문서 | “이 문제를 통제하는 스킬을 만들고 싶다”는 자연어 |
| 사용자 준비량 | 높음 | 낮음 |
| B 세션 인터뷰 | 설계서에 차단 모호성이 있을 때만 | 저장소 조사로 해결할 수 없는 사용자 결정이 빠졌을 때 |
| 적합한 상황 | 팀 합의 설계가 존재함, 기존 스킬 개정, 고위험 스킬 | 초기 아이디어, 반복 애로사항, 비개발자의 스킬 요청 |
| 최종 흐름 | 설계 감사 → spec → build → audit | 원문 보존 → 요구사항 도출·질문 → 설계 감사 → spec → build → audit |
| 생성 로직 | 동일 | 동일 |

### 방법 1 — 준비된 요구사항·설계서로 바로 생성

다음과 같은 경우에 사용한다.

- 조직 또는 프로젝트에 이미 승인된 요구사항 문서가 있다.
- 목적, 사용·비사용 조건, 입력, 권한, 절차, 검증, 실패 처리, 완료 조건이 설계서에 들어 있다.
- 기존 스킬을 새 정책에 맞게 개정한다.
- DB·배포·보안처럼 사람의 사전 설계 승인이 중요한 스킬이다.

호출 예:

```text
/claude-skill-author gated-release \
  --design docs/skill-designs/gated-release/DESIGN.md \
  --design docs/policies/release-policy.md

기존 승인 설계서와 릴리스 정책을 기준으로 생성한다.
설계서에 없는 권한 확대, 승인 생략, 운영 환경 기본값을 임의로 추가하지 않는다.
```

B 세션은 설계서를 그대로 믿지 않고 다음을 수행한다.

```text
현재 호출 원문 보존
→ 설계서·저장소 사실 대조
→ 차단 모호성만 질문
→ 독립 설계 감사
→ 기존 스킬 생성 로직 실행
```

설계서가 충분하면 질문 없이 진행한다. 설계서에 “배포 전 승인이 필요하다”고만 있고 승인 시점이나 적용 환경이 없어 안전한 제작이 불가능하면 해당 결정만 사용자에게 묻는다.

### 방법 2 — 자연어 애로사항부터 인터뷰해 생성

다음과 같은 경우에 사용한다.

- 어떤 문제가 반복되는지는 알지만 스킬 설계 문서를 작성하지 않았다.
- 목적과 금지사항 정도만 알고 있다.
- 비개발자 또는 도메인 담당자가 평범한 말로 통제 요구를 전달한다.
- B 세션이 저장소를 조사해 입력·출력·검증 절차를 설계해 주길 원한다.

호출 예:

```text
/claude-skill-author evidence-code-review

애로사항:
코드 리뷰를 요청했는데 Claude가 리뷰만 하지 않고 파일까지 수정하는 것을 막고 싶다.

최종 결과:
각 지적에 파일·줄 번호·코드 근거와 검증 상태가 포함된 리뷰 결과.

허용:
- 저장소와 테스트 읽기
- Git diff 확인
- 로컬 테스트 실행

금지:
- 코드와 테스트 수정
- 커밋·푸시
- 실행하지 않은 검사를 통과로 표시

사용자 승인 필요:
- 없음
```

B 세션은 다음을 자동으로 수행한다.

```text
최초 원문을 SOURCE_REQUEST.md에 잠금
→ 저장소와 기존 규칙 조사
→ 원자 요구사항 REQ-### 생성
→ 부족한 항목 분류
→ 사용자만 결정할 차단 항목만 묶어 질문
→ DESIGN.md 작성
→ 독립 설계 감사
→ 기존 스킬 생성 로직 실행
```

질문이 필요할 때는 다음과 같은 형식이 권장된다.

```text
현재 목적과 핵심 금지사항은 확인했습니다. 설계 확정에 필요한 항목만 결정해 주세요.

1. 기본 리뷰 범위
   - A. 현재 Git diff
   - B. 지정 파일·모듈
   - C. 전체 저장소
   - 권장 기본값: A

2. 결과 저장 방식
   - A. 대화에만 보고
   - B. Markdown 보고서 생성
   - 권장 기본값: A
```

B는 이미 답한 내용을 다시 묻지 않고, 저장소에서 확인할 수 있는 테스트 명령·파일 경로·기존 스킬은 직접 조사한다.

---

## 3. 두 방법의 사용자 시나리오

### 시나리오 A — 준비된 설계서로 검증된 릴리스 스킬 생성

### 상황

플랫폼 팀이 다음 설계서를 이미 합의했다.

```text
docs/skill-designs/gated-release/DESIGN.md
```

설계서에는 다음 내용이 있다.

- 개발·검증 환경만 지원한다.
- 배포 전에 지정 테스트가 모두 통과해야 한다.
- 운영 배포는 이 스킬의 범위에서 제외한다.
- 배포 대상, 커밋 SHA, 롤백 명령을 보고해야 한다.
- 외부 쓰기 전에 사용자 승인을 받아야 한다.

### A 세션 — 저장소별 최초 1회 설치

공유 자료의 `packages/` 경로를 유지한 채 저장소 루트에서 Claude Code를 열고, `prompts/01_CLAUDE_INSTALL_PROMPT.md` 전체를 전달한다.

설치가 끝나면 Claude Code를 종료한다.

### B 세션 — 설계서 기반 제작

같은 저장소 루트에서 새 Claude Code 세션을 연다.

```text
/claude-skill-author gated-release --mode spec --agent auto \
  --design docs/skill-designs/gated-release/DESIGN.md

설계서의 권한과 승인 경계를 완화하지 않는다.
기존 동명 스킬이 있으면 신규 생성이 아니라 개정으로 처리한다.
```

고위험 스킬이므로 먼저 `spec`까지만 수행한다. 사용자는 다음을 확인한다.

- `COMMAND_SPEC.yaml`의 대상 환경
- 허용·금지 도구
- 사용자 승인 시점
- 롤백과 부분 실패 처리
- `EXTERNAL`로 분리된 permission·hook·CI 항목

승인 후:

```text
/claude-skill-author gated-release --mode build
```

```text
/claude-skill-author gated-release --mode audit
```

### 예상 산출물

```text
.claude/skills/gated-release/SKILL.md
.claude/agents/<대상업무에이전트>.md       # 필요 판정 시만
.claude/skill-authoring/gated-release/
  ├── SOURCE_REQUEST.md
  ├── REQUIREMENT_INTAKE.yaml
  ├── DESIGN_REQUIREMENTS.yaml
  ├── DESIGN_AUDIT_REPORT.md
  ├── RULE_COVERAGE.yaml
  ├── COMMAND_SPEC.yaml
  ├── AUTHORING_REVIEW.md
  ├── AUDIT_REPORT.md
  └── FINAL_STATUS.json
```

### 실사용 세션

제작 세션을 종료하고 같은 저장소에서 새 세션을 연다.

```text
/gated-release 검증 환경에 현재 승인된 커밋을 배포할 준비 상태를 점검해줘
```

운영 배포는 설계 범위 밖이므로 실행해서는 안 된다.

---

### 시나리오 B — 애로사항 한 문장에서 읽기 전용 리뷰 스킬 생성

### 상황

사용자는 설계서가 없다. 반복되는 문제만 알고 있다.

> 코드 리뷰를 부탁하면 Claude가 파일까지 고쳐 버리고, 문제의 근거도 제대로 적지 않는다.

### A 세션 — 최초 설치

시나리오 A와 동일하다. 저장소별로 한 번만 수행한다.

### B 세션 — 자연어 입력과 인터뷰

같은 저장소 루트에서 새 Claude Code 세션을 연다.

```text
/claude-skill-author evidence-code-review

코드 리뷰 중 파일을 직접 수정하지 못하게 하는 스킬을 만들고 싶다.
모든 지적에는 파일·줄 번호·코드 근거가 있어야 한다.
테스트를 실행하지 못했으면 통과라고 표시하지 않는다.
커밋과 푸시는 금지한다.
```

B 세션은 먼저 저장소를 조사한다. 예를 들어 리뷰 범위와 테스트 실행 여부가 사용자만 결정할 항목으로 남으면 한 번에 묻는다.

사용자 답변 예:

```text
- 기본 범위는 현재 Git diff로 해줘.
- 저장소의 공식 단위 테스트 실행은 허용해.
- 결과는 우선 대화에만 보고해.
- 파일 쓰기와 자동 수정은 모두 금지해.
```

이 답변은 최초 원문을 덮어쓰지 않고 `SOURCE_DECISIONS.md`에 누적된다. 이후 B는 설계 작성·독립 설계 감사·spec·build·최종 감사를 계속한다.

### 자동 생성되는 설계서

```text
docs/skill-designs/evidence-code-review/DESIGN.md
```

### 최종 스킬

```text
.claude/skills/evidence-code-review/SKILL.md
```

단순 슬래시 실행만으로 충분하면 `--agent auto`는 대상 업무용 Agent.md를 만들지 않을 수 있다. 별도 읽기 전용 역할이나 격리 컨텍스트가 실질적으로 필요할 때만 Agent.md를 만든다.

### 실사용 세션

제작 세션을 종료하고 같은 저장소에서 새 세션을 연다.

```text
/evidence-code-review 현재 브랜치 변경사항을 검토해줘
```

기대되는 결과:

- 어떤 파일도 수정하지 않는다.
- 모든 지적에 위치와 근거를 남긴다.
- 테스트 미실행·실패·권한 부족을 통과로 바꾸지 않는다.
- 확인 범위와 미검증 항목을 구분한다.

---

## 4. B 세션은 어디까지 인터뷰하는가

B가 묻는 것은 Claude Code의 내부 작성기술이 아니라 **사용자만 결정할 수 있는 업무 정책**이다.

| B가 직접 조사·판단 | 사용자에게 확인할 수 있는 항목 |
|---|---|
| 기존 `CLAUDE.md`, 경로별 규칙 | 실제 책임 범위: 분석만 / 자동 수정까지 |
| 테스트 명령과 관련 파일 | 외부 쓰기, DB 쓰기, 배포, 삭제 허용 여부 |
| 기존 동명·유사 스킬 | 사용자 승인 시점과 승인 범위 |
| 주단계·보조단계 | 업무적으로 무엇을 완료로 볼지 |
| 규칙의 APPLY·TRANSFORM·EXCLUDE·EXTERNAL | 부분 실패와 복구 정책 |
| frontmatter와 최소 도구 | 대상 환경과 민감정보 취급 |
| `SKILL.md`·reference·script 구조 | 충돌하는 요구사항의 우선순위 |
| Agent.md 필요성 |  |

누락 항목은 네 종류로 분류한다.

```text
REPOSITORY_RESEARCH
→ 저장소에서 조사하고 질문하지 않음

SAFE_DEFAULT
→ 저위험·가역 기본값을 적용하고 근거 기록

NON_BLOCKING_UNCERTAINTY
→ 미확인으로 표시하고 진행 가능

USER_DECISION
→ 권한·운영·승인·완료에 영향을 주면 질문하고 답 전에는 차단
```

안전한 기본값의 예:

- 출력 경로 미지정 → 대화에 보고하고 파일은 쓰지 않는다.
- 수정 범위 불명확 → 읽기 전용으로 둔다.
- 테스트 명령 불명확 → 저장소 공식 명령을 찾고, 없으면 미검증으로 보고한다.
- 근거 없음 → 사실로 단정하지 않는다.

다음 항목은 안전한 기본값으로 허용하지 않는다.

- 운영 DB 쓰기
- 배포
- 파일 삭제
- 외부 전송
- 비밀정보 접근
- 비용 발생 호출
- 보안·권한 완화

> 질문을 3~5개로 묶고 선택지·권장 기본값·영향을 제시하도록 스킬에 지시되어 있다. 미해결 차단 질문의 존재는 기계 게이트가 막지만, 질문 문장의 표현 품질 전체를 별도 언어 검사기가 완전히 보증하는 것은 아니다.

---

## 5. 환경 설정

### 5.1 준비물

- Git 저장소
- Claude Code가 실행 가능한 환경
- Python 3
- Bash 환경
  - macOS·Linux: 기본 셸 사용 가능
  - Windows: WSL 또는 Git Bash 권장
- `unzip`
  - 없으면 Python 표준 라이브러리 `zipfile`로 압축을 풀 수 있다.
- 패키지 파일:

```text
claude-skill-author-package_20260828_v1.3.zip
```

별도의 Python 외부 패키지 설치를 전제로 하지 않는다. YAML 증거 파일은 검사 편의를 위해 JSON 호환 문법으로 관리된다.

### 5.2 저장소 루트 확인

```bash
git rev-parse --show-toplevel
git status --short
```

Claude Code는 `.claude/skills/` 내부가 아니라 **같은 Git 저장소 루트**에서 연다.

```bash
cd <저장소_루트>
claude
```

### 5.3 패키지 배치

```text
<저장소_루트>/
├── .git/
├── CLAUDE.md                 # 있을 수 있음
└── packages/
    └── claude-skill-author-package_20260828_v1.3.zip
```

### 5.4 A 세션에서 설치

`prompts/01_CLAUDE_INSTALL_PROMPT.md`를 Claude Code에 전달한다.

A 세션은 다음까지만 수행한다.

```text
패키지 검사
→ 패키지 자체 테스트
→ .claude/ 설치
→ Python 구문 검사
→ Git diff 확인
→ 종료
```

설치 결과는 다음과 같아야 한다.

```text
.claude/skills/claude-skill-author/
.claude/agents/skill-design-author.md
.claude/agents/skill-design-auditor.md
.claude/agents/skill-author-auditor.md
.claude/settings.stop-hook.example.json
```

패키지 자체 테스트 명령:

```bash
python3 tests/run_tests.py
```

### 5.5 새 세션에서 설치 확인

A 세션을 완전히 종료한 뒤 같은 저장소 루트에서 새 B 세션을 연다.

```text
/claude-skill-author
```

또는 `/` 메뉴에서 `claude-skill-author`가 보이는지 확인한다.

보이지 않으면 다음을 확인한다.

1. 현재 세션의 작업 디렉터리가 설치한 저장소 안인가
2. `.claude/skills/claude-skill-author/SKILL.md`가 존재하는가
3. Claude Code를 설치 후 완전히 재시작했는가

### 5.6 Stop 훅은 선택 사항

설치만으로 Stop 훅은 활성화되지 않는다.

```text
.claude/settings.stop-hook.example.json
```

필요한 경우 기존 `.claude/settings.json`의 `hooks.Stop`과 충돌·보안을 검토한 뒤 해당 항목만 수동 병합한다. 기존 설정 파일을 예시 파일로 덮어쓰지 않는다.

---

## 6. 세션 역할

| 세션 | 역할 | 실행 위치 |
|---|---|---|
| A | 저장소별 최초 설치와 설치 검증 | 저장소 루트 |
| B | 방법 1 또는 방법 2로 설계·스킬 제작·감사 | 같은 저장소 루트의 새 세션 |
| B-2 또는 C | 완성된 대상 스킬의 실제 업무 실행·스모크 테스트 | 같은 저장소 루트의 깨끗한 새 세션 |

A가 설치한 `.claude/skills/`와 `.claude/agents/`는 같은 저장소 파일시스템을 사용하는 B·C 세션에서 발견된다.

B 제작 세션에서 바로 완성 스킬을 실행할 수도 있지만, 작성 과정의 긴 컨텍스트를 제거하려면 새 B-2 또는 C 세션에서 실제 사용하는 편이 권장된다.

---

## 7. 모드와 Agent 정책

### 7.1 실행 모드

| 모드 | 범위 | 권장 상황 |
|---|---|---|
| `design` | 원문 보존·요구사항 도출·설계·설계 감사 | 설계서만 먼저 검토할 때 |
| `spec` | design 포함 + 규칙 판정·`COMMAND_SPEC.yaml` | 고위험 스킬의 명세를 사람에게 먼저 승인받을 때 |
| `build` | 승인된 명세로 런타임 파일 작성 | spec 승인 이후 |
| `audit` | 최종 읽기 전용 감사 | 기존 산출물을 별도 검토할 때 |
| `full` | design → spec → build → audit | **기본값**. 저위험·중위험 스킬 또는 충분히 명확한 요구사항 |

### 7.2 Agent.md 정책

| 옵션 | 의미 |
|---|---|
| `--agent auto` | 독립 역할·별도 권한·컨텍스트·협업 필요성을 보고 자동 판정한다. 기본값이다. |
| `--agent required` | 대상 업무용 Agent.md를 반드시 생성하도록 명세한다. |
| `--agent forbidden` | 대상 업무용 Agent.md를 만들지 않는다. |

다음 신호가 있을 때만 Agent.md가 필요할 가능성이 높다.

- 반복 호출되는 독립 전문 역할
- 메인 세션과 다른 도구 또는 권한 경계
- 별도 컨텍스트 격리
- 장기 상태나 전문 메모리
- 다른 에이전트와의 협업·인계
- 특정 Agent에서 `context: fork`로 실행할 필요

단순 `/스킬명` 호출로 충분하면 `SKILL.md`만 생성하는 것이 정상이다.

---

## 8. 생성 파일과 감사 증거

대상 런타임 파일:

```text
.claude/skills/<스킬명>/
├── SKILL.md
└── references/, scripts/, assets/, evals/   # 필요할 때만
```

선택적 업무 Agent:

```text
.claude/agents/<에이전트명>.md
```

설계서:

```text
docs/skill-designs/<스킬명>/DESIGN.md
```

감사 증거:

```text
.claude/skill-authoring/<스킬명>/
├── SOURCE_REQUEST.md
├── SOURCE_DECISIONS.md
├── REQUIREMENT_INTAKE.yaml
├── DESIGN_REQUIREMENTS.yaml
├── DESIGN_AUDIT_REPORT.md
├── DESIGN_AUDIT_ATTESTATION.yaml
├── RULE_MANIFEST.yaml
├── RULE_COVERAGE.yaml
├── COMMAND_SPEC.yaml
├── SPEC_REVIEW.md
├── AUTHORING_REVIEW.md
├── AUDIT_REPORT.md
├── AUDIT_ATTESTATION.yaml
├── AUTHORING_STATE.yaml
├── VALIDATION_DESIGN.json
├── VALIDATION_SPEC.json
├── VALIDATION_BUILD.json
├── VALIDATION_AUDIT.json
└── FINAL_STATUS.json
```

원문·후속 결정·설계·명세·런타임 파일이 변경되면 이후 단계의 기존 PASS는 `STALE`이 되며 재검증이 필요하다.

---

## 9. Git에 올려 공유할 때

권장 공유 구조:

```text
<공유 저장소>/
├── README_KO.md
├── BACKGROUND_AND_REFERENCES_KO.md
├── packages/
│   └── claude-skill-author-package_20260828_v1.3.zip
├── prompts/
│   ├── 01_CLAUDE_INSTALL_PROMPT.md
│   ├── 02_METHOD_1_PREPARED_DESIGN_PROMPT.md
│   ├── 03_METHOD_2_NATURAL_LANGUAGE_PROMPT.md
│   └── 04_CLAUDE_REPOSITORY_SETUP_AND_SHARE_PROMPT.md
└── SHA256SUMS.txt
```

프로젝트별로 생성된 다음 파일을 공유할지는 보안과 감사 목적에 따라 결정한다.

| 경로 | 공유 판단 |
|---|---|
| `.claude/skills/<스킬명>/` | 팀이 같은 스킬을 사용하려면 보통 커밋한다. |
| `.claude/agents/<에이전트명>.md` | 생성됐고 팀에서 필요하면 커밋한다. |
| `docs/skill-designs/<스킬명>/DESIGN.md` | 설계 근거 공유를 위해 권장한다. |
| `.claude/skill-authoring/<스킬명>/` | 감사 추적이 필요하면 유용하지만 원문에 민감정보가 없는지 반드시 확인한다. |
| `.claude/settings.stop-hook.example.json` | 예시로 공유할 수 있다. 실제 개인 설정을 그대로 올리지 않는다. |
| `.bak-*`, 임시 압축 해제 폴더 | 커밋하지 않는다. |

`SOURCE_REQUEST.md`와 관련 증거에는 사용자의 원문이 남기 때문에 비밀정보·개인정보·내부 경로가 포함됐는지 검토해야 한다.

---

## 10. 문제 해결

### `/claude-skill-author`가 보이지 않는다

- 설치 후 Claude Code를 완전히 재시작한다.
- 같은 저장소 루트에서 새 세션을 연다.
- `.claude/skills/claude-skill-author/SKILL.md` 존재 여부를 확인한다.

### B가 질문하고 멈췄다

`REQUIREMENT_INTAKE.yaml`의 차단 `USER_DECISION`이 해결되지 않은 상태일 가능성이 높다. 같은 B 세션에서 답한다. 답변은 `SOURCE_DECISIONS.md`에 기록되고 설계가 갱신된다.

### 기존 PASS가 `STALE`이 됐다

원문, 후속 결정, 설계서, 명세 또는 런타임 파일이 변경됐다. 변경된 단계부터 새 감사·검증을 수행하는 정상 동작이다.

### `audit`가 실패한다

`AUDIT_REPORT.md`에서 차단 항목을 확인한다. 작성자가 수정한 뒤 build 검증을 다시 하고 **새 감사자 인스턴스**로 재감사해야 한다.

### Agent.md가 생성되지 않았다

`--agent auto`에서 독립 역할·별도 권한·별도 컨텍스트가 불필요하다고 판정된 것일 수 있다. 스킬 실행에 Agent가 업무적으로 필수라면 `--agent required`로 설계하되, 필요 이유를 명시한다.

### Stop 훅이 작업 종료를 막는다

`FINAL_STATUS.json`, `AUTHORING_STATE.yaml`, 최신 validation 파일과 digest가 현재 입력과 일치하는지 확인한다. 예전 PASS 보고서를 복사하거나 입력을 바꾼 경우 다시 검증해야 한다.

---

## 11. 빠른 시작

### 최초 설치

```text
A 세션
→ prompts/01_CLAUDE_INSTALL_PROMPT.md 전달
→ 설치 PASS 확인
→ Claude Code 종료
```

### 방법 1

```text
B 새 세션
→ /claude-skill-author <스킬명> --design <설계서>
→ 차단 질문이 있으면 답변
→ FINAL_STATUS PASS
```

### 방법 2

```text
B 새 세션
→ /claude-skill-author <스킬명>
→ 애로사항·최종 결과·허용·금지·승인 필요를 자연어로 입력
→ 필요한 차단 질문만 답변
→ FINAL_STATUS PASS
```

### 실제 사용

```text
B-2 또는 C 새 세션
→ /<완성된스킬명> <실제 업무 요청>
```

---

## 12. 어떤 목적의 스킬·커맨드에 적합한가

이 하네스는 모든 사소한 편의 스킬을 만들기 위한 범용 템플릿 생성기가 아니다. **누락·권한 오용·검증 생략·잘못된 완료 판정의 비용이 큰 스킬**을 감사 가능한 방식으로 만들 때 가장 효과적이다.

### 특히 권장되는 대상

| 스킬·커맨드 목적 | 게이트가 필요한 이유 | 대표 예 |
|---|---|---|
| 계획·설계 | 요구사항, 영향 범위, 검증, 완료 조건 누락이 이후 구현 전체에 전파될 수 있음 | `/change-plan`, `/migration-plan` |
| 코드 리뷰·검증 | 일부 파일만 보고 전체 통과로 판단하거나 근거 없이 결함을 확정할 수 있음 | `/evidence-code-review`, `/verify-change` |
| 코드·설정 수정 | 무관한 파일 수정, 기존 사용자 변경 훼손, 테스트 누락 가능성 | `/safe-fix`, `/bounded-refactor` |
| 규칙·거버넌스 생성 | 잘못된 규칙이 이후 모든 세션에 반복 전파될 수 있음 | `/rule-author`, `/policy-sync` |
| 근거 기반 보고서 | 확인 사실·추론·미확인이 섞이거나 출처 없는 수치가 들어갈 수 있음 | `/evidence-report` |
| DB·마이그레이션 | 데이터 손상, 대량 변경, 롤백 실패 위험 | `/db-change-plan`, `/migration-guard` |
| 배포·릴리스·운영 | 외부 환경에 실제 부작용이 있고 승인·사후 검증·복구가 필요 | `/gated-release`, `/deploy-check` |
| 보안·권한·외부 전송 | 최소권한, 비밀정보, 승인 우회와 기술적 차단이 중요 | `/security-review`, `/external-send-guard` |
| 장기 오케스트레이션 | 단계 상태, 산출물 동결, 인수인계, 부분 실패 추적이 필요 | `/full-cycle`, `/handoff` |
| 컴플라이언스·감사 | 판정 근거와 변경 이력, 재현 가능한 증거가 필요 | `/compliance-check`, `/audit-pack` |

### 과할 수 있는 대상

다음처럼 실패 비용이 낮고 출력이 단순한 일회성 작업에는 이 하네스가 지나치게 무거울 수 있다.

- 문장 어투 변환이나 번역
- 짧은 요약
- 단순 파일명 정리
- 고정 문구·템플릿 출력
- 읽기·쓰기·외부 부작용이 없는 개인용 편의 명령

### 선택 기준

다음 질문 중 하나라도 `예`라면 이 하네스를 우선 검토한다.

- 빠지면 안 되는 규칙이나 절차가 있는가?
- 파일·코드·DB·외부 환경을 수정할 수 있는가?
- 사용자 승인 지점이 필요한가?
- 실패 후 재시도·중단·복구를 구분해야 하는가?
- 실행하지 않은 검사를 통과로 보고하면 안 되는가?
- 근거와 감사 기록을 남겨야 하는가?
- 잘못된 스킬이 다른 작업에 반복 전파될 수 있는가?

---

## 13. 조사 배경과 참고자료

이 하네스는 특정 저장소 하나를 복제해 만든 것이 아니다. 처음에는 **“LLM 스킬·하네스용 Markdown에는 어떤 공통 작성규칙이 있는가?”**라는 질문에서 시작했고, 여러 공식 문서·오픈소스 생태계·연구 논문에서 반복되는 원칙을 교차분석해 공통 규칙을 만들었다. 이후 Claude Code 슬래시 커맨드의 전용 차이를 분리하고, 실제 누락 사례를 기계 게이트와 독립 감사 구조로 바꾸면서 현재 형태로 발전했다.

### 자료 수

| 집계 기준 | 수량 |
|---|---:|
| 최초 공통 규칙 문서의 번호가 매겨진 근거 항목 | **31개** |
| 그중 공식 규격·제품 문서 항목 | **23개** |
| 그중 연구 논문 | **8편** |
| 복수 링크를 개별로 센 최초 공통 문서의 실제 URL | **34개** |
| Claude Code 전용 델타 문서의 공식 근거 | **10개** |
| 두 기초 문서 전체의 중복 제거 고유 URL | **37개** |

`31개`와 `34개`가 다른 이유는 Roo Code, LangGraph, AutoGen 항목처럼 하나의 번호 아래 두 개의 공식 문서를 함께 묶은 항목이 있기 때문이다. Claude Code 전용 델타 문서의 10개 중 다수는 공통 문서와 겹치며, 두 문서를 합쳐 중복 제거하면 37개의 고유 URL이다.

### 핵심 공식 문서·오픈소스 생태계 12개

| 생태계 | 주로 참고한 내용 |
|---|---|
| Agent Skills | `SKILL.md` 규격, description, 점진적 공개, 평가 |
| OpenAI Codex | `AGENTS.md`, 장기 실행계획, 승인·샌드박스 |
| Claude Code | Skills, 프로젝트 메모리, 권한, 훅, 서브에이전트 |
| GitHub Copilot | 저장소별 커스텀 지시와 코드 리뷰 규칙 |
| Cursor | 경로·범위 기반 Rules 구조 |
| OpenHands | 프로젝트·전역 Skills의 적용 방식 |
| Cline | Skills, Plan/Act, Memory Bank |
| Roo Code | Custom Instructions와 Skills의 역할 분리 |
| LangGraph | 상태 그래프, 중단·재개, 사람 승인 |
| Microsoft AutoGen | GraphFlow와 Human-in-the-Loop |
| CrewAI | 작업·가드레일·출력 검증 |
| Model Context Protocol | 신뢰 경계와 보안 모범사례 |

초기 탐색 범위에는 Continue와 Aider 같은 에이전트 도구도 포함됐지만, 최종 번호형 근거 목록은 위 생태계와 공식 문서 중심으로 정리했다.

### 연구 논문 8편

| 논문·연구 | 현재 설계에 반영된 핵심 |
|---|---|
| ReAct | 계획·행동·관찰 결과에 따라 다음 행동 갱신 |
| Plan-and-Solve | 복잡한 작업을 먼저 단계로 분해 |
| Self-Refine | 생성 → 피드백 → 수정 → 재검증 루프 |
| Reflexion | 실패 기록을 다음 실행과 규칙 개선에 활용 |
| Instruction Hierarchy | 외부 콘텐츠의 지시를 상위 규칙으로 승격하지 않음 |
| Lost in the Middle | 핵심 규칙을 앞에 두고 긴 상세자료를 조건부 로딩 |
| SWE-agent | 에이전트가 사용하는 인터페이스와 검증 구조의 중요성 |
| SWE-bench | 실제 저장소 과제에서 결과를 객관적으로 평가하는 관점 |

### 조사에서 현재 하네스로 발전한 과정

```text
공식 문서·오픈소스·논문 교차분석
→ 공통 작성규칙 67개(C/P/D/E/V/S/M)
→ Claude Code 전용 규칙 22개(CC)
→ 총 89개 규칙의 전수 판정 구조
→ 설계·명세·작성·감사의 단계 분리
→ 검사 스크립트와 Stop 게이트
→ 실제 성공·누락 사례 재구성
→ SOURCE_REQUEST, 요구사항 수립, 독립 설계 감사, STALE 무효화 추가
→ claude-skill-author v1.3
```

전체 근거 목록은 이 번들의 `BACKGROUND_AND_REFERENCES_KO.md`에서 확인할 수 있다.

---

## 14. 현재 보장 범위와 한계

기계 게이트가 강하게 확인하는 항목:

- 최초 원문 존재와 SHA-256 잠금
- 후속 결정 분리
- 20개 설계 섹션과 18개 필수 의미 항목
- 설계 감사 PASS와 현재 입력 digest 일치
- 규칙 누락·중복·미판정
- 명세·런타임 파일·감사 결과의 단계 상태
- 입력 변경 후 기존 PASS 무효화
- 최종 attestation과 `FINAL_STATUS.json`

LLM 의미 검토와 시나리오 평가가 담당하는 항목:

- 사용자의 애로사항을 업무적으로 올바르게 해석했는가
- 설계 절차가 실제로 유용한가
- 문장이 형식적으로만 규칙을 흉내 내지 않았는가
- 질문의 표현과 선택지가 사용자에게 충분히 이해되는가

따라서 고위험 스킬은 `spec`에서 사람의 권한·승인·복구 검토를 거치고, 완성 후 새 세션에서 드라이런 또는 비운영 스모크 테스트를 수행한다.
