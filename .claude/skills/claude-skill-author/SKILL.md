---
name: claude-skill-author
description: >
  설계서와 프로젝트 규칙을 바탕으로 Claude Code용 스킬을 명세하고 작성한 뒤,
  규칙 누락·권한·인수·검증·실패 경로를 독립 감사하는 메타 스킬이다.
  새 SKILL.md 작성, 기존 스킬 개정, 작성규칙 누락 감사에 사용한다.
when_to_use: >
  사용자가 /claude-skill-author로 새 Claude Code 스킬 작성 또는 기존 스킬 개정을
  명시적으로 요청할 때 사용한다. 일반 코드 구현이나 단순 문서 작성에는 사용하지 않는다.
argument-hint: "<스킬명> [--mode full|spec|build|audit] [--design <경로> ...]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/init_authoring.py *)
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py *)
  - Bash(claude --version)
  - Bash(git status)
  - Bash(git status *)
  - Bash(git diff)
  - Bash(git diff *)
  - Agent
---

# Claude Skill Author

Claude Code용 스킬을 **명세 → 작성 → 독립 감사 → 완료 게이트** 순서로 만든다.
기본 모드는 `full`이며 한 번의 호출로 전체 과정을 수행한다.

## 호출

```text
/claude-skill-author <스킬명> --mode full --design <설계서 경로> [--design <추가 경로> ...]
```

예:

```text
/claude-skill-author omplan --mode full \
  --design docs/openmetadata/OM_PLAN_DESIGN.md \
  --design docs/openmetadata/governance_requirements.md

목적: OpenMetadata 변경 전 검증 가능한 실행계획을 작성한다.
허용: 저장소·설계서 읽기, 계획 문서 작성.
금지: 제품 코드 수정, 커밋, 푸시, 배포.
```

지원 모드:

- `full`: 명세, 작성, 독립 감사까지 수행한다. 기본값이다.
- `spec`: 규칙 전수 판정과 `COMMAND_SPEC.yaml` 확정까지만 수행한다.
- `build`: 기존 확정 명세로 런타임 스킬을 작성·검증한다.
- `audit`: 기존 산출물을 수정하지 않고 독립 감사한다.

## 불변 조건

1. 모든 규칙을 최종 스킬에 넣지는 않지만, **모든 규칙 ID를 정확히 한 번 판정한다.**
2. 목적·사용 시점·입력·범위·권한·절차·출력·검증·실패·완료 조건을 `DESIGN_REQUIREMENTS.yaml`에 구조화하고, 모든 필수 항목이 근거와 함께 해결되기 전에는 명세를 승인하지 않는다.
3. 설계 요구사항과 명세 게이트가 통과하기 전에는 런타임 `SKILL.md`를 작성하지 않는다.
4. `APPLY`·`TRANSFORM` 규칙은 최종 파일의 실제 반영 위치와 연결한다.
5. `EXCLUDE`에는 대상 단계·위험·입출력에 근거한 비적용 이유를 적는다.
6. `EXTERNAL`에는 permissions, hook, CI, script 중 기술적 강제 위치를 적는다.
7. 작성 증거는 런타임 스킬 폴더와 분리한다.
8. 작성자와 최종 감사자를 분리한다. 감사자는 대상 파일을 수정하지 않는다.
9. 감사 `PASS`와 기계 검증 종료코드 0이 모두 확인되기 전에는 완료로 보고하지 않는다.

## 경로

- 공통 규칙: `${CLAUDE_SKILL_DIR}/references/01_LLM_스킬_하네스_MD_공통_작성규칙.md`
- Claude 전용 규칙: `${CLAUDE_SKILL_DIR}/references/02_Claude_Code_슬래시커맨드_MD_차이점_전용규칙.md`
- 작성 절차: `${CLAUDE_SKILL_DIR}/references/authoring-workflow.md`
- 설계 입력 해석: `${CLAUDE_SKILL_DIR}/references/design-input-guide.md`
- 설계서 입력 템플릿: `${CLAUDE_SKILL_DIR}/assets/DESIGN_INPUT.template.md`
- 스키마 설명: `${CLAUDE_SKILL_DIR}/references/schemas.md`
- 감사 기준: `${CLAUDE_SKILL_DIR}/references/audit-rubric.md`
- 런타임 스킬: `${CLAUDE_PROJECT_DIR}/.claude/skills/<스킬명>/`
- 작성 증거: `${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>/`

`.claude/skill-authoring/`은 Claude Code의 내장 설정 디렉터리가 아니라 이 메타 스킬이 사용하는 감사 증거 저장소다.

## 0단계. 호출 해석과 사전 점검

1. `$ARGUMENTS`의 첫 번째 비옵션 값을 대상 스킬명으로 해석한다.
2. 스킬명은 소문자 영문·숫자·하이픈만 허용한다.
3. `--mode`가 없으면 `full`로 둔다.
4. `--design` 경로를 모두 수집한다. 나머지 자연어는 목적·사용·비사용 조건·허용·금지·완료 조건의 원천 요구사항으로 사용한다.
5. `${CLAUDE_SKILL_DIR}/references/design-input-guide.md`를 읽고 설계 입력의 필수 의미 항목을 확인한다.
6. 대상 스킬명이 없으면 임의 추측하지 말고 사용법을 보고한다. `spec`·`full` 모드에서는 설계서 또는 현재 호출에 명시된 목적·범위·허용·금지·완료 조건 중 하나 이상의 구체적 요구사항이 필요하다. `build`·`audit` 모드는 기존 `COMMAND_SPEC.yaml`의 설계서 목록을 사용한다.
7. 사용자가 설계서 골격 생성을 요청했거나 지정한 설계서가 아직 없다면 `${CLAUDE_SKILL_DIR}/assets/DESIGN_INPUT.template.md`를 읽어 요청 경로에 초안을 작성하고, 사용자가 채워야 할 미결정 항목을 보고한 뒤 스킬 작성은 시작하지 않는다.
8. 다음을 조사한다.
   - 적용되는 `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`
   - 기존 `.claude/skills/`, `.claude/commands/`, `.claude/agents/`
   - `.claude/settings*.json`의 permissions와 hooks
   - 같은 이름 또는 유사 책임의 기존 스킬
   - 현재 Git 상태와 사용자 변경
   - 가능한 경우 `claude --version`
9. 기존 대상이 있으면 신규 생성으로 덮어쓰지 않고 `revise` 작업으로 분류한다.
10. `${CLAUDE_SKILL_DIR}/references/authoring-workflow.md`를 읽고 이후 단계를 따른다.
11. `build`·`audit` 모드에서는 기존 작성 증거가 존재하는지 확인한 뒤 `init_authoring.py`를 `--resume`으로 실행하여 규칙 원문 변경 여부와 활성 상태를 갱신한다. 작성 증거가 없으면 새 빈 명세를 만들지 말고 해당 모드의 사전조건 실패로 보고한다.

## 1단계. 규칙 인벤토리와 명세

`spec` 또는 `full` 모드에서 수행한다.

1. 다음 명령으로 원문 규칙과 모든 판정 슬롯을 생성한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/init_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --mode "<모드>" \
  --common-rules "${CLAUDE_SKILL_DIR}/references/01_LLM_스킬_하네스_MD_공통_작성규칙.md" \
  --claude-rules "${CLAUDE_SKILL_DIR}/references/02_Claude_Code_슬래시커맨드_MD_차이점_전용규칙.md" \
  --design "<설계서 경로>"
```

설계서가 여러 개면 `--design`을 반복한다. 기존 작성 증거를 이어서 사용할 때만 `--resume`을 추가한다.

2. 생성된 `DESIGN_REQUIREMENTS.yaml`을 채운다. 설계서·현재 호출문·저장소 사실에서 목적, 사용자 결과, 사용·비사용 조건, 호출 예, 입력·기본값, 출처 경계, 포함·제외·조건부 범위, 허용·금지·승인 행동, 절차, 출력, 검증, 실패 처리, 완료 조건을 구조화한다.
3. 각 설계 요구사항에 `RESOLVED` 상태, 구체적인 `value` 또는 `items`, 정확한 `sources`를 기록한다. 해당 사항이 없으면 빈 값 대신 `없음 — <이유>`를 기록한다.
4. 해결하지 못한 항목을 추측하지 않는다. `open_questions`에 기록하고 `status: DRAFT`를 유지한다. 모든 필수 의미 항목이 해결된 경우에만 `status: APPROVED`로 바꾼다.
5. 생성된 `RULE_MANIFEST.yaml`을 원천으로 사용한다. 규칙 ID 목록을 기억으로 다시 작성하지 않는다. 각 규칙의 `title`만 보지 말고 `text` 전문을 읽은 뒤 판정한다.
6. 대상 스킬의 주단계 하나와 보조단계를 정한다.
   - `R`: 조사·이해
   - `P`: 계획·설계
   - `I`: 구현·변경
   - `V`: 검증·리뷰
   - `F`: 수정·복구
   - `O`: 배포·운영
   - `D`: 문서화·보고
   - `G`: 규칙 주입·가드레일
   - `X`: 오케스트레이션·메타
7. `RULE_COVERAGE.yaml`의 모든 규칙을 `APPLY`, `TRANSFORM`, `EXCLUDE`, `EXTERNAL` 중 정확히 하나로 판정한다.
8. 주단계와 보조단계에 해당하는 `stage_modules` 전문을 읽고 `COMMAND_SPEC.yaml`에 반영한다.
9. 승인된 `DESIGN_REQUIREMENTS.yaml`을 기준으로 `COMMAND_SPEC.yaml`을 작성한다. 설계 입력과 저장소 사실이 충돌하면 임의로 바꾸지 않고 미결정 사항으로 기록한다.
10. `SPEC_REVIEW.md`에 설계 입력 해결 현황, 주단계, 부작용, 호출 정책, frontmatter 선택, 규칙 판정 집계를 기록한다.
11. 다음 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase spec
```

12. 종료코드가 0이 아니면 `DESIGN_REQUIREMENTS.yaml`, 명세 또는 규칙 판정을 수정하고 동일 검증을 다시 실행한다.
13. `spec` 모드이면 검증 통과 상태와 생성 파일만 보고하고 종료한다.

## 2단계. 런타임 스킬 작성

`build` 또는 `full` 모드에서 수행한다.

1. `COMMAND_SPEC.yaml`의 `status`가 `APPROVED`이고 spec 검증이 통과했는지 확인한다.
2. 기존 스킬 개정이면 원본과 변경 전 diff를 보존한다. 사용자 변경을 되돌리지 않는다.
3. 런타임 파일은 `.claude/skills/<스킬명>/`에 작성한다.
4. 작성 근거·규칙 표·감사 기록은 런타임 폴더에 넣지 않는다.
5. 기본 산출물은 `SKILL.md`이며, 실제로 필요한 경우에만 `references/`, `scripts/`, `assets/`, `evals/`를 추가한다.
6. `SKILL.md`는 두 참고문서가 없어도 실행 의미를 이해할 수 있게 자기완결적으로 작성한다.
7. frontmatter에는 실제 동작을 바꾸는 필드만 둔다.
8. 각 단계는 가능한 경우 입력, 행동, 산출물, 검증, 실패 처리를 가진다.
9. `allowed-tools`를 제한 목록으로 설명하지 않는다. 실제 금지는 `disallowed-tools`, permissions, hook 또는 CI로 분리한다.
10. `RULE_COVERAGE.yaml`의 모든 `APPLY`·`TRANSFORM` 항목에 최종 반영 파일과 검색 가능한 문구를 기록한다.
11. 모든 안티패턴을 `PASS` 또는 근거가 있는 `NOT_APPLICABLE`로 판정한다.
12. 저장된 최종 파일을 다시 열어 모든 의미 문장을 검토한다.
    - 어떤 오류·누락·오해·위험을 막는가?
    - 어떤 요구사항·저장소 사실·규칙 ID가 근거인가?
    - 실행 또는 판정 가능한가?
    - 중복·충돌하지 않는가?
    - 제거하면 실제 품질이 떨어지는가?
13. 근거 없는 문장은 수정·제거·외부화한다.
14. `AUTHORING_REVIEW.md`에 최종 문장별 근거와 규칙 반영 위치를 기록한다.
15. 다음 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase build
```

16. 종료코드가 0이 아니면 감사 단계로 넘어가지 않는다.

## 3단계. 독립 감사

`audit` 또는 `full` 모드에서 수행한다.

1. 가능하면 `skill-author-auditor` 커스텀 서브에이전트를 새 인스턴스로 호출한다.
2. 해당 에이전트가 없으면 `general-purpose` 서브에이전트를 새로 호출하되, 읽기 전용 감사 프롬프트를 전달한다.
3. 감사 프롬프트에는 다음 경로를 정확히 포함한다.
   - 두 원문 규칙 문서
   - 모든 설계서
   - `DESIGN_REQUIREMENTS.yaml`
   - `RULE_MANIFEST.yaml`
   - `COMMAND_SPEC.yaml`
   - `RULE_COVERAGE.yaml`
   - 최종 `SKILL.md`와 보조 파일
   - `AUTHORING_REVIEW.md`
   - 직전 기계 검증 결과
4. 감사자는 파일을 수정하지 않고 `${CLAUDE_SKILL_DIR}/references/audit-rubric.md`의 형식으로 결과만 반환한다.
5. 반환 결과를 `AUDIT_REPORT.md`에 그대로 기록한다.
6. `FAIL`이면 발견 사항을 수정한 뒤 coverage와 리뷰 문서를 갱신하고, 기계 검증 후 **새 감사자 인스턴스**로 다시 감사한다.
7. 수정·재감사는 최대 2회 수행한다. 계속 실패하면 실패 증거와 남은 문제를 보고하고 완료로 표시하지 않는다.
8. 감사 `PASS` 후 다음 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase audit
```

9. 종료코드가 0일 때만 `FINAL_STATUS.json`의 상태를 `PASS`로 둔다.

## 4단계. 최종 보고

다음만 간결하게 보고한다.

- 생성·수정한 런타임 파일
- 작성 증거 파일
- 대상 스킬의 주단계와 보조단계
- 호출 정책, 컨텍스트, 부작용 등급
- 설계 요구사항 수와 해결 수
- 규칙 수, 판정 수, 누락·중복 수
- spec/build/audit 검증 결과
- 독립 감사 판정
- 구현되지 않은 외부 통제와 남은 위험

`PASS`가 아니면 “완료”라고 표현하지 않는다.

## 금지

- 규칙 원문을 읽지 않고 템플릿부터 채우지 않는다.
- 규칙 ID 목록을 수작업으로 새로 작성하지 않는다.
- 모든 규칙을 최종 `SKILL.md`에 억지로 복사하지 않는다.
- `EXCLUDE`를 “관련 없음” 한마디로 처리하지 않는다.
- 작성자가 독립 감사자를 대신하지 않는다.
- 감사 보고서를 수정해 판정을 바꾸지 않는다.
- 실행하지 않은 테스트와 존재하지 않는 기술적 통제를 통과로 기록하지 않는다.
- 작성 증거를 런타임 스킬 본문에 중복해 컨텍스트를 낭비하지 않는다.
