---
name: claude-skill-author
description: >
  사용자의 자연어 애로사항과 통제 요구를 원문으로 보존하고, 저장소를 조사해 스킬 설계서를 만든 뒤,
  규칙 전수 판정·명세·SKILL.md 작성·선택적 Agent.md 생성·독립 감사를 수행하는 고신뢰 Claude Code 스킬 제작 하네스다.
  새 스킬 작성, 기존 스킬 개정, 설계·작성규칙 누락 감사에 사용한다.
when_to_use: >
  사용자가 /claude-skill-author로 “이 행동을 통제하는 스킬을 만들고 싶다”와 같은 자연어 요구를 명시적으로 전달할 때 사용한다.
  일반 코드 구현이나 단순 문서 작성에는 사용하지 않는다.
argument-hint: "<스킬명> [--mode full|design|spec|build|audit] [--design <경로> ...] [--agent auto|required|forbidden]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(mkdir -p *)
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/init_authoring.py *)
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py *)
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/seal_attestation.py *)
  - Bash(claude --version)
  - Bash(git status)
  - Bash(git status *)
  - Bash(git diff)
  - Bash(git diff *)
  - Agent
---

# Claude Skill Author

사용자의 자연어 요구를 **원문 보존 → 설계 → 설계 독립 감사 → 명세 → 작성 → 최종 독립 감사 → 완료 게이트** 순서로 변환한다.
기본 모드는 `full`이며 설계서가 없어도 한 번의 명시적 호출로 전체 과정을 수행한다.

## 호출

### 자연어만으로 전체 생성

```text
/claude-skill-author evidence-code-review --mode full

코드 리뷰 중 파일을 직접 수정하지 못하게 하고 싶다.
모든 지적에는 파일·줄 번호·코드 근거가 있어야 한다.
테스트를 실행하지 못했으면 통과라고 표시하지 않는다.
```

### 기존 설계서를 추가 입력으로 사용

```text
/claude-skill-author evidence-code-review --mode full \
  --design docs/review/REVIEW_POLICY.md

허용: 저장소 읽기, Git diff 확인, 로컬 테스트 실행.
금지: 코드 수정, 커밋, 푸시.
```

지원 모드:

- `design`: 원문 요구사항 보존, 설계서 작성, 설계 독립 감사까지만 수행한다.
- `spec`: 설계 PASS 후 규칙 전수 판정과 `COMMAND_SPEC.yaml` 확정까지 수행한다.
- `build`: 기존 승인 명세로 `SKILL.md`와 필요한 경우 `Agent.md`를 작성·검증한다.
- `audit`: 기존 산출물을 수정하지 않고 최종 독립 감사한다.
- `full`: `design → spec → build → audit` 전체를 수행한다. 기본값이다.

대상 Agent.md 정책:

- `--agent auto`: 독립 역할·별도 권한·별도 컨텍스트 필요성을 기준으로 자동 판정한다. 기본값이다.
- `--agent required`: 대상 업무용 Agent.md를 반드시 설계한다.
- `--agent forbidden`: 대상 업무용 Agent.md를 만들지 않는다.

## 불변 조건

1. 최초 자연어 요구를 의미 변경 없이 `SOURCE_REQUEST.md`에 보존하고 생성 후 수정하지 않는다.
2. 후속 사용자 답변과 변경 결정은 `SOURCE_DECISIONS.md`에 시간순으로 추가한다.
3. 사용자가 이미 결정한 내용을 다시 질문하지 않는다.
4. 저장소에서 확인할 수 있는 사실은 사용자에게 묻지 않고 직접 조사한다.
5. 사용자만 결정할 수 있는 차단 항목만 한 번에 묶어 질문한다.
6. `REQUIREMENT_INTAKE.yaml`에서 사용자 원문·결정·저장소 사실·안전한 기본값을 원자 요구사항으로 추적한다.
7. 설계 작성자와 설계 감사자를 분리한다.
8. 20개 설계 섹션, 18개 필수 의미 항목, 설계 감사 `PASS`와 현재 입력 digest가 모두 맞기 전에는 명세를 승인하지 않는다.
9. 모든 규칙을 최종 스킬에 넣지는 않지만 모든 규칙 ID를 정확히 한 번 판정한다.
10. design·spec 게이트가 통과하기 전에는 런타임 `SKILL.md`를 작성하지 않는다.
11. 대상 Agent.md 필요성을 `required` 또는 `not-required`로 명시적으로 판정한다.
12. `APPLY`·`TRANSFORM` 규칙은 최종 파일의 실제 반영 위치와 연결한다.
13. `EXCLUDE`에는 구체적인 비적용 이유를 적는다.
14. `EXTERNAL`에는 permission, hook, CI, script, sandbox 또는 policy의 강제 위치를 적는다.
15. 작성자와 최종 감사자를 분리한다. 감사자는 대상 파일을 수정하지 않는다.
16. 이전 PASS 이후 입력이 바뀌면 뒤 단계 상태를 `STALE`로 무효화한다.
17. 최종 감사 `PASS`, audit attestation, 기계 검증 종료코드 0이 모두 확인되기 전에는 완료로 보고하지 않는다.

## 기본 경로

- 최초 원문 요구사항: `${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>/SOURCE_REQUEST.md`
- 후속 사용자 결정: `${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>/SOURCE_DECISIONS.md`
- 요구사항 구조화: `${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>/REQUIREMENT_INTAKE.yaml`
- 단계 상태·fingerprint: `${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>/AUTHORING_STATE.yaml`
- 기본 설계서: `${CLAUDE_PROJECT_DIR}/docs/skill-designs/<스킬명>/DESIGN.md`
- 런타임 스킬: `${CLAUDE_PROJECT_DIR}/.claude/skills/<스킬명>/`
- 선택적 업무 에이전트: `${CLAUDE_PROJECT_DIR}/.claude/agents/<에이전트명>.md`
- 작성·감사 증거: `${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>/`

참조:

- 요구사항 도출: `${CLAUDE_SKILL_DIR}/references/requirements-elicitation.md`
- 설계 입력 해석: `${CLAUDE_SKILL_DIR}/references/design-input-guide.md`
- 작성 절차: `${CLAUDE_SKILL_DIR}/references/authoring-workflow.md`
- 스키마: `${CLAUDE_SKILL_DIR}/references/schemas.md`
- 감사 기준: `${CLAUDE_SKILL_DIR}/references/audit-rubric.md`
- 설계 템플릿: `${CLAUDE_SKILL_DIR}/assets/DESIGN_INPUT.template.md`
- 업무 에이전트 템플릿: `${CLAUDE_SKILL_DIR}/assets/TARGET_AGENT.template.md`

`.claude/skill-authoring/`은 Claude Code 내장 설정이 아니라 이 하네스의 감사 증거 저장소다.

# 0단계. 호출 해석과 저장소 점검

1. `$ARGUMENTS`의 첫 번째 비옵션 값을 대상 스킬명으로 해석한다.
2. 스킬명은 소문자 영문·숫자·하이픈만 허용한다.
3. `--mode`가 없으면 `full`, `--agent`가 없으면 `auto`로 둔다.
4. `--design` 경로를 수집한다. 지정하지 않으면 기본 설계서 경로를 사용한다.
5. 명령 옵션을 제외한 나머지 자연어 전체를 원문 요구사항으로 취급한다.
6. 대상 스킬명이 없거나 `design`·`spec`·`full` 모드에서 구체적인 자연어 요구와 기존 설계서가 모두 없으면 사용법을 보고한다.
7. 다음을 조사한다.
   - 적용되는 `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`
   - 기존 `.claude/skills/`, `.claude/commands/`, `.claude/agents/`
   - `.claude/settings*.json`의 permissions와 hooks
   - 같은 이름 또는 유사 책임의 기존 스킬·에이전트
   - 관련 스크립트·테스트·템플릿
   - 현재 Git 상태와 사용자 변경
   - 가능한 경우 `claude --version`
8. 기존 대상이 있으면 무조건 덮어쓰지 않고 `revise`로 분류한다.
9. 사용자 변경을 되돌리거나 대상과 무관한 파일을 수정하지 않는다.

# 1단계. 원문 요구사항 보존

`design`, `spec`, `full` 모드에서 수행한다.

1. `${CLAUDE_SKILL_DIR}/assets/SOURCE_REQUEST.template.md`를 읽는다.
2. 작성 증거 폴더를 만든다.

```bash
mkdir -p "${CLAUDE_PROJECT_DIR}/.claude/skill-authoring/<스킬명>"
```

3. 최초 실행이면 현재 호출의 자연어를 의미 변경 없이 다음 파일에 기록한다.

```text
.claude/skill-authoring/<스킬명>/SOURCE_REQUEST.md
```

4. `SOURCE_REQUEST.md`가 이미 있으면 기존 원문을 수정하지 않는다.
5. 후속 사용자 답변·변경 결정은 다음 파일에 기록 시각과 함께 추가한다.

```text
.claude/skill-authoring/<스킬명>/SOURCE_DECISIONS.md
```

6. 원문 요약과 해석 결과는 `SOURCE_REQUEST.md`가 아니라 `REQUIREMENT_INTAKE.yaml`에 기록한다.
7. 현재 호출이 기존 설계서 감사·개정 요청이면 그 현재 의도를 `SOURCE_DECISIONS.md`에 남긴다.

# 2단계. 설계서 작성과 사용자 질문 게이트

`design`, `spec`, `full` 모드에서 수행한다.

1. 다음 파일을 읽는다.
   - `${CLAUDE_SKILL_DIR}/references/requirements-elicitation.md`
   - `${CLAUDE_SKILL_DIR}/references/design-input-guide.md`
   - `${CLAUDE_SKILL_DIR}/assets/DESIGN_INPUT.template.md`
2. `SOURCE_REQUEST.md`와 `SOURCE_DECISIONS.md`를 바탕으로 `REQUIREMENT_INTAKE.yaml`을 작성한다. 각 요구사항은 고유 `REQ-###`, 유형, 상태, 차단 여부, 근거, 설계 반영 위치를 가진다.
3. 기본 설계서가 없으면 `skill-design-author`를 새 인스턴스로 호출한다.
4. 기존 설계서가 있으면 원문 요구사항과 저장소 사실을 반영해 개정이 필요한지 먼저 판정한다.
5. 설계 작성자에게 정확한 원문·템플릿·출력 경로·프로젝트 규칙 경로를 제공한다.
6. 누락 항목은 다음으로 분류한다.
   - `USER_DECISION`
   - `REPOSITORY_RESEARCH`
   - `SAFE_DEFAULT`
   - `NON_BLOCKING_UNCERTAINTY`
7. `REPOSITORY_RESEARCH`는 B 세션 또는 설계 작성자가 직접 조사한다.
8. `SAFE_DEFAULT`는 이유와 영향 범위를 설계서에 기록한다.
9. 차단되는 `USER_DECISION`만 한 번에 묶어 사용자에게 질문한다.
10. 질문에는 선택지, 권장 기본값, 선택별 영향을 포함한다. 사용자가 이미 답한 항목은 묻지 않는다.
11. 고위험 권한·운영 부작용·승인·복구 조건을 추측하지 않는다.
12. 질문 답변은 `SOURCE_DECISIONS.md`, `REQUIREMENT_INTAKE.yaml`, `DESIGN.md`에 함께 반영한다.
13. 차단 질문이 해결되지 않으면 설계 상태를 `DRAFT`로 두고 이후 단계로 넘어가지 않는다.

# 3단계. 작성 증거 초기화와 설계 독립 감사

1. 설계서와 원문 요구사항 파일이 모두 존재한 뒤 다음 명령을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/init_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --mode "<모드>" \
  --common-rules "${CLAUDE_SKILL_DIR}/references/01_LLM_스킬_하네스_MD_공통_작성규칙.md" \
  --claude-rules "${CLAUDE_SKILL_DIR}/references/02_Claude_Code_슬래시커맨드_MD_차이점_전용규칙.md" \
  --source-request ".claude/skill-authoring/<스킬명>/SOURCE_REQUEST.md" \
  --decision-document ".claude/skill-authoring/<스킬명>/SOURCE_DECISIONS.md" \
  --design "docs/skill-designs/<스킬명>/DESIGN.md"
```

추가 설계·요구사항 문서는 `--design`을 반복한다. 기존 증거를 이어서 사용할 때만 `--resume`을 사용한다.

2. `REQUIREMENT_INTAKE.yaml`의 모든 원자 요구사항을 원문·후속 결정·저장소 근거에 연결하고 `APPROVED`로 만든다.
3. `DESIGN_REQUIREMENTS.yaml`의 18개 필수 의미 항목을 설계서·원문·저장소 근거로 채운다.
4. 각 항목에 `RESOLVED`, 구체적 내용, 정확한 `sources`를 기록한다.
5. `decision_register`에 사용자 결정, 저장소 조사, 안전한 기본값, 비차단 불확실성을 구분한다.
6. `open_questions`는 구조화 객체로 기록한다. 차단 질문은 `RESOLVED`가 아니면 설계 승인을 막는다.
7. 새 `skill-design-auditor` 인스턴스를 읽기 전용으로 호출한다.
8. 감사자는 `SOURCE_REQUEST.md`, `SOURCE_DECISIONS.md`, `REQUIREMENT_INTAKE.yaml`, `DESIGN.md`를 대조하고 파일을 수정하지 않는다.
9. 감사 결과를 `DESIGN_AUDIT_REPORT.md`에 기록한다.
10. `FAIL` 또는 `CONDITIONAL`이면 설계를 보완하고 새 감사자 인스턴스로 재감사한다.
11. 설계 감사 `PASS` 후 현재 원문·결정·요구사항·설계서 digest를 감사 보고서에 묶는다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/seal_attestation.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --kind design
```

12. 다음 design 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase design
```

13. 종료코드가 0이 아니면 규칙 판정이나 스킬 작성으로 넘어가지 않는다.
14. 설계·원문·후속 결정이 바뀌면 기존 설계 감사와 이후 PASS는 무효이므로 새 감사와 검증을 수행한다.
15. `design` 모드이면 생성 파일과 검증 결과만 보고하고 종료한다.

# 4단계. 규칙 인벤토리와 실행 명세

`spec` 또는 `full` 모드에서 수행한다.

1. `RULE_MANIFEST.yaml`을 원천으로 사용한다. 규칙 ID를 기억으로 다시 작성하지 않는다.
2. 각 규칙의 제목뿐 아니라 `text` 전문을 읽는다.
3. 대상 스킬의 주단계 하나와 보조단계를 최종 사용자 결과로 판정한다.
   - `R`: 조사·이해
   - `P`: 계획·설계
   - `I`: 구현·변경
   - `V`: 검증·리뷰
   - `F`: 수정·복구
   - `O`: 배포·운영
   - `D`: 문서화·보고
   - `G`: 규칙 주입·가드레일
   - `X`: 오케스트레이션·메타
4. 모든 규칙을 `APPLY`, `TRANSFORM`, `EXCLUDE`, `EXTERNAL` 중 정확히 하나로 판정한다.
5. 승인된 설계 요구사항을 `COMMAND_SPEC.yaml`의 실행 계약으로 변환한다.
6. 대상 Agent.md 필요성을 판정한다.

Agent.md를 `required`로 판정하는 신호:

- 반복적으로 호출되는 독립 전문 역할
- 메인 세션과 다른 도구·권한 경계
- 별도 컨텍스트 격리
- 지속 메모리
- 다른 에이전트와 협업·인계
- 스킬을 특정 에이전트에서 `context: fork`로 실행할 필요

단순 슬래시 호출로 충분하면 `not-required`로 판정한다.

7. `COMMAND_SPEC.yaml`의 `agent_requirement`에 다음을 기록한다.
   - `mode`: 사용자 정책 `auto|required|forbidden`
   - `decision`: `required|not-required`
   - 판단 기준별 Boolean
   - 구체적인 이유
   - Agent 이름·경로·통합 방식·도구·권한
8. 통합 방식은 다음 중 하나다.
   - `none`
   - `skill-context-fork`
   - `agent-preloads-skill`
   - `standalone-agent`
9. 수동 전용 스킬은 Agent.md의 `skills`로 미리 로드하지 않는다. 필요하면 `skill-context-fork`를 사용한다.
10. `SPEC_REVIEW.md`에 설계 해결 현황, 단계, 권한, 호출 정책, Agent 판단, 규칙 집계를 기록한다.
11. spec 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase spec
```

12. 종료코드 0 이전에는 런타임 파일을 작성하지 않는다.
13. `spec` 모드이면 검증 결과만 보고하고 종료한다.

# 5단계. 런타임 SKILL.md와 선택적 Agent.md 작성

`build` 또는 `full` 모드에서 수행한다.

1. design·spec 검증 PASS와 `COMMAND_SPEC.status: APPROVED`를 확인한다.
2. 기존 대상 개정이면 원본과 diff를 보존하고 사용자 변경을 되돌리지 않는다.
3. 런타임 스킬은 `.claude/skills/<스킬명>/`에 작성한다.
4. 작성 증거는 런타임 폴더에 넣지 않는다.
5. 기본 산출물은 `SKILL.md`이며, 필요한 경우에만 `references/`, `scripts/`, `assets/`, `evals/`를 추가한다.
6. `SKILL.md`는 작성 규칙 문서를 다시 읽지 않아도 실행 가능한 자기완결적 계약으로 작성한다.
7. 각 단계에는 가능한 경우 입력·행동·산출물·검증·실패 처리를 둔다.
8. `allowed-tools`를 제한 목록으로 설명하지 않는다. 실제 금지는 다른 통제로 분리한다.
9. Agent.md가 `required`이면 `TARGET_AGENT.template.md`를 참고해 명세된 경로에 작성한다.
10. Agent.md에는 역할, 도구, 권한, 입력·출력, 스킬 연결, 실패·인계가 있어야 한다.
11. `skill-context-fork`이면 SKILL.md에 `context: fork`와 정확한 `agent`를 설정한다.
12. `agent-preloads-skill`이면 Agent.md의 `skills`에 대상 스킬을 넣고 대상 스킬이 수동 전용이 아닌지 확인한다.
13. 모든 `APPLY`·`TRANSFORM`에 최종 반영 파일과 검색 가능한 문구를 기록한다.
14. 모든 안티패턴을 `PASS` 또는 근거 있는 `NOT_APPLICABLE`로 판정한다.
15. 저장된 최종 SKILL.md와 Agent.md를 처음부터 다시 읽는다.
16. 모든 의미 문장을 요구사항·저장소 사실·규칙 ID에 연결한다.
17. 근거 없는 문장은 수정·제거·외부화한다.
18. `AUTHORING_REVIEW.md`에 다음 제목을 포함한다.
   - `## 규칙 집계`
   - `## Agent.md 필요성 판정`
   - `## 문장별 최종 검토`
   - `## 기계 검사 결과`
19. build 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase build
```

20. 종료코드 0 이전에는 최종 감사로 넘어가지 않는다.

# 6단계. 최종 스킬 독립 감사

`audit` 또는 `full` 모드에서 수행한다.

1. `skill-author-auditor`를 새 인스턴스로 호출한다.
2. 사용할 수 없으면 새 `general-purpose` 인스턴스에 읽기 전용 감사 프롬프트를 준다.
3. 감사 입력에는 다음을 정확히 포함한다.
   - 원문 요구사항
   - 모든 설계서
   - 설계 감사 보고서
   - `DESIGN_REQUIREMENTS.yaml`
   - 두 규칙 원문
   - `RULE_MANIFEST.yaml`
   - `COMMAND_SPEC.yaml`
   - `RULE_COVERAGE.yaml`
   - 최종 SKILL.md와 보조 파일
   - 생성된 경우 Agent.md
   - `AUTHORING_REVIEW.md`
   - 직전 기계 검증 결과
4. 감사자는 파일을 수정하지 않는다.
5. 결과를 `AUDIT_REPORT.md`에 기록한다.
6. `FAIL`이면 수정·build 재검증 후 새 감사자로 최대 2회 재감사한다.
7. 감사 `PASS` 후 현재 명세·규칙·런타임 파일·build 검증 digest를 감사 보고서에 묶는다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/seal_attestation.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --kind final
```

8. audit 검증을 실행한다.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_authoring.py \
  --project-root "${CLAUDE_PROJECT_DIR}" \
  --target "<스킬명>" \
  --phase audit
```

9. 종료코드 0이고 `AUTHORING_STATE.yaml`의 design/spec/build/audit가 모두 현재 fingerprint로 `PASS`일 때만 `FINAL_STATUS.json`을 `PASS`로 둔다.

# 7단계. 최종 보고

다음만 보고한다.

- 원문 요구사항·설계서 경로
- 설계 감사 결과
- 생성·수정한 SKILL.md와 보조 파일
- Agent.md 필요성 판정과 생성 경로
- 주단계·보조단계, 호출·컨텍스트·부작용 등급
- 설계 요구사항 해결 수
- 규칙 수, 판정 수, 누락·중복·미판정 수
- design/spec/build/audit 검증 결과와 fingerprint freshness
- 최종 독립 감사 판정
- 미구현 외부 통제와 남은 위험

`PASS`가 아니면 완료라고 표현하지 않는다.

## 금지

- 자연어 원문을 설계 요약으로 대체하거나 최초 `SOURCE_REQUEST.md`를 수정하지 않는다.
- 후속 결정을 최초 원문 파일에 섞지 않는다.
- 설계 작성자가 자기 설계를 최종 승인하지 않는다.
- 사용자가 이미 답한 사항을 다시 묻지 않는다.
- 저장소에서 확인할 수 있는 사항을 사용자에게 떠넘기지 않는다.
- 고위험 권한을 안전한 기본값으로 추측하지 않는다.
- 규칙 원문을 읽지 않고 템플릿부터 채우지 않는다.
- 모든 규칙을 최종 SKILL.md에 억지로 복사하지 않는다.
- Agent.md를 “있으면 좋아 보인다”는 이유로 만들지 않는다.
- 수동 전용 스킬을 Agent.md에 preload하지 않는다.
- 작성자가 독립 감사자를 대신하지 않는다.
- 실행하지 않은 검사와 존재하지 않는 통제를 통과로 기록하지 않는다.

