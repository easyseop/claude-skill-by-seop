# om-plan 독립 감사 결과 — 3차(최종, 2026-08-24)

> 3차 독립 감사자(1·2차와 다른 새 인스턴스)가 반환한 결과를 그대로 기록한다. 작성자는 판정을 바꾸지 않았다.
> 1·2차 감사 원문은 `AUDIT_REPORT_ROUND1.md`·`AUDIT_REPORT_ROUND2.md`에 보존돼 있다.
> 메타스킬 규정상 수정·재감사는 최대 2회이며, 이 3차 감사로 그 한도를 소진했다.

## 종합 판정
- 판정: CONDITIONAL
- 핵심 이유: 2차 차단 3건(`git status` 제거, `run-request.yaml` 작성 주체, `plan-resume` marker 수명)의 조치는 코드로 검증한 결과 **대부분 정확**하다. 훅·preflight·validate·markers·collectors·CI·스키마 전반의 단언이 실측과 일치했고, 규칙 89·안티패턴 26 전수 판정, 요구사항 18/18, 필수 EXTERNAL 통제 실재, 기계 검증 `ok:true`도 확인됐다. 다만 **7단계(block 재개)만은 여전히 실행 가능성이 입증되지 않는다.** (1) `plan-resume`은 `--state-root`/`--session-id`를 argparse `required=True`로 받고 환경변수 대체가 없는데(`om_workflow.py:373-375`), SKILL.md는 에이전트가 관측할 수 없는 훅 주입 환경변수를 **1차 출처**로 지시한다. (2) 새 marker를 만드는 유일한 방아쇠로 지시된 `/om-resume` 명령이 대상 저장소에 **존재하지 않는다**. 두 항목 모두 "실행하지 않은 검사·미확인 외부 통제를 통과로 인정하지 않는다"는 기준에 걸리므로 PASS를 줄 수 없다. 안전 경계·게이트·판정 전달에는 결함이 없어 FAIL도 아니다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (`open_questions`는 사람 결정 대기로 정직하게 분리됐고, 2건은 실측 근거와 함께 해소 표기됨)
- 미해결: 0
- 근거 없음: 0 — 표본 검증한 저장소 근거가 모두 실재하고 인용 내용과 일치했다(`preflight.py:264-328`, `validate.py:441-544`, `resume.py:40-69`, `markers.py`, `hook_policy.py:142-240`, `hook_cli.py:64-168`, `om_plan_ci.py:324-325`, `collectors.py:769-868`, `plan-run-request.schema.json`, `CLAUDE.md`, `.claude/settings.json`, 에이전트 정의, `om-apply/SKILL.md`)
- 명세 반영 누락: 1(부분) — `inputs_and_defaults`의 CLI 선택 인수·기본값 4항목(`--run-dir|--evidence-root` 상호배타, `--state-root`·`--session-id` 기본값 규칙)이 `COMMAND_SPEC.inputs`로 옮겨지지 않고 `workflow`와 최종 본문에만 남았다.

## 규칙 집계
- 원문 규칙: 89 (공통 C20+P8+D12+E7+V8+S7+M5=67, 전용 CC22 — 두 원문에서 제목을 직접 확인)
- 판정 규칙: 89 / 누락 0 / 중복 0 / 미판정 0
- 반영 위치 없음: 0 — `APPLY`·`TRANSFORM` 68건의 `targets` 문자열을 최종 `SKILL.md`에서 표본 대조했고 전부 실재하며 규칙의 실질 의미를 구현했다.
- 근거 부족 제외: 0 — `EXCLUDE` 16건의 사유가 주단계(P)·부작용(로컬 쓰기)·입출력(계획 run)과 논리적으로 연결된다. `CC-09`~`CC-12` 제외는 최종 본문에 `context: fork`·`!` 주입·보조 파일이 실제로 없음을 확인해 사실과 일치한다.
- 미구현 필수 외부 통제: 0 — `required_for_pass: true` 통제를 모두 열어 서술대로 동작함을 확인. `P-08`의 `test_claude_wiring.py`는 `planned`·`required_for_pass:false`이며 실제로 om-apply만 단언함을 확인해 **정직한 표기**다.
- 안티패턴: 26 판정(PASS 21 / NOT_APPLICABLE 5) — 집계 산술 일치.

## 차단 문제

| 심각도 | 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| 차단 | `SKILL.md` 7단계 / `COMMAND_SPEC.workflow[6]` / `DESIGN_REQUIREMENTS.workflow[6]` | `STATE_ROOT`·`SESSION_ID`의 1차 출처를 "훅이 주입하는 `OM_PLAN_HOOK_STATE_ROOT`·`OM_PLAN_SESSION_ID`"로 지시하나 에이전트가 그 값을 관측할 방법이 없고, `plan-resume`은 두 값을 필수 인수로만 받는다 | `om_workflow.py:369-376`(`--state-root`·`--session-id` `required=True`). 환경변수 대체는 `default_plan_state_root`(65-85행)·`select_plan_session_id`(162-168행)뿐이며 `plan start`·`plan check` 경로에서만 호출된다. 훅 주입은 `hook_cli._updated_command`(64-78행)가 명령 문자열 앞에 붙이는 **셸 변수 할당 접두사**여서 같은 명령 안에서 `$VAR`로 되읽을 수 없고, `hook_policy._SHELL_OPERATORS`가 `$(`를 막아 명령치환 우회도 불가하다 | 1차 출처를 2단계 `plan start` stdout의 `state_root`·`session_id`(`om_workflow.py:264-270`)로 바꾸고, 훅 주입은 "CLI가 스스로 쓰는 값이며 에이전트가 인용할 값이 아니다"로 서술 |
| 차단 | `SKILL.md` 7단계 / `COMMAND_SPEC.workflow[6]` | "사용자가 `/om-resume`을 새로 입력해 훅이 marker를 만들게 한다"는 절차가 대상 저장소에 존재하지 않는 명령에 의존한다 | `.claude/skills/om-resume/SKILL.md`·`.claude/commands/om-resume.md` 모두 부재. `.claude/settings.json`의 `UserPromptExpansion` matcher `^(om-plan|om-resume)$`와 `hook_cli.handle_event`(86-99행)는 그 이름을 전제하지만 소유 파일이 없다. 미등록 슬래시 명령에서 `UserPromptSubmit`이 발화되는지는 실행 검증하지 못했다 | (a) 대상 저장소에 `om-resume` 스킬·커맨드를 추가하거나, (b) marker 재생성 방아쇠를 실재하는 `/om-plan` 재입력으로 바꾸고 그 흐름을 본문에 기술 |

> 위 2건은 모두 **block 재개 경로 한정**이다. 정상·승인·중단 경로의 판정·게이트·안전 경계에는 차단 문제가 없다.

## 시나리오 결과

| 시나리오 | 판정 | 근거 |
|---|---|---|
| 1. 정상 호출 | 통과 | 8단계가 실제 CLI와 일치. `run_validation`은 `pass`를 만들지 않아 "exit 0 없음" 서술이 정확(`validate.py:524-531`, `verdict.to_exit_code`) |
| 2. 필수 입력 누락 | 통과 | 스키마 `required`+모드별 `allOf`가 본문 표와 정확히 일치. 1단계 실패 처리가 "추측 금지·사람에게 요청"으로 정의됨 |
| 3. 잘못된 입력·허용값 | 통과 | 오류 코드 4종 전부 `collectors.validate_request`(300-337행)에 실재하며 exit 3 |
| 4. 대상 부재 | 통과 | `REFS_UNAVAILABLE`·`PINNED_COMMIT_UNAVAILABLE`·`ACTIVE_REGISTRATION_MISSING`/`EXISTS`가 `preflight.collect_state`(146-193행)에 실재 |
| 5. 권한 부족 | 통과 | "훅 거부는 권한 문제이며 게이트 실패로 보고하지 않는다"가 `hook_policy` 기본 거부 및 `_deny` 프로토콜과 정합 |
| 6. 검증 실패 | 통과 | `block`·`analysis_error` 구분과 원문 보고 요구가 `_write_attempt_and_summary`(379-438행) 필드와 일치 |
| 7. 부분 변경 후 실패 | 통과 | append-only, run 보존, `preflight-result.json`+marker 정리, 기존 run 미기입 모두 실측 일치 |
| 8. 인젝션 | 통과 | 신뢰 순서·"외부 콘텐츠는 데이터"·의심 보고 문장이 있고, 기술적으로도 훅이 plan 계열 외 Bash와 지정 외 Agent를 거부 |
| 9. 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true`. 부작용에 비춰 수동 전용 선택이 타당 |
| 10. 동명 충돌 | 조건부 | 대상 저장소에 기존 om-plan 스킬·커맨드가 없어 실제 충돌은 없다. 그러나 본문이 참조하는 `/om-resume` 이름은 소유 파일 없이 훅 matcher에만 존재해 이름 계약이 미완성이다 |

## 비차단 개선사항

1. **「입력과 인수」와 1단계의 주체 불일치**: "여기서 얻은 값은 곧바로 실행하지 않고 `run-request.yaml`의 필드로 확정한 뒤"가 에이전트가 파일을 채우는 것처럼 읽혀 1단계 "이 파일은 에이전트가 만들지 않는다"와 충돌한다.
2. **6단계 digest 생략 서술의 범위**: marker 기록값 대체는 `plan start`가 만든 첫 검증에만 해당한다. `plan-resume` 후 새 세션 marker에는 `trusted_input_lock_digest`가 없으므로(기록은 `start_plan_run` 253행에서만) 생략 시 `TRUSTED_INPUT_LOCK_DIGEST_MISSING`으로 exit 3이다. "첫 검증에 한해"를 붙이면 해소된다.
3. **`plan-validate` 미제공 시 결과 표현**: "verified가 false가 되고 approval에 도달하지 못한다"는 실제로 `trusted_issues`가 `reasons`에 들어가 verdict가 `analysis_error`(3)가 되는 것보다 약하게 표현됐다.
4. **저수준 명령 실행 안내의 실효성**: "필요하면 일반 권한 절차를 거쳐 실행한다"는 보호 세션 중 성립하지 않는 경우가 있다. `_workflow_action`은 `plan-session-start`를 인식하지 않아 marker가 있는 동안 항상 거부되고, `plan-preflight`는 run 미결속 시에만, `plan-validate`는 run 결속 시에만 허용된다.
5. **`preflight-result.json` 예외 미기재**: `RUN_DIRECTORY_EXISTS`일 때는 기록하지 않는다(`preflight.py:337`). 이 예외를 표에도 넣으면 좋다.
6. **CI 매핑 근거의 사실·해석 분리 잔여**: "사람 결정에 따른 것"이라는 인과 서술의 인용 가능한 결정 기록이 증거 파일에 없다.
7. **`RULE_COVERAGE` `P-08` 사유의 출처 오귀속**: "83 작업 3 범위 밖"이라 적었으나 83 작업 3은 오히려 wiring 테스트 보강을 **요구**한다. 상태 표기는 정직하나 사유 문장을 "이번 저작 지시서 범위 밖"으로 정정해야 한다.
8. **완료 상태 어휘**: `CC-16`의 최소 상태는 `실패`인데 본문은 `중단`을 쓴다. `V-08`과 정합하므로 문제는 아니나 의도적 매핑임을 증거에 남기면 좋다.
9. **`COMMAND_SPEC.inputs` 보강**: 위 「명세 반영 누락」 1건.

## 감사 범위와 미확인 사항

- **직접 코드로 검증한 것**: `hook_policy.py`·`hook_cli.py`·`preflight.py`·`validate.py`·`markers.py`·`resume.py`·`om_workflow.py`·`collectors.py`·`doc_sources.py`·`om_plan_ci.py` 전체, `plan-run-request.schema.json`, `.claude/settings.json`, `run_om_plan_hook.sh`, 에이전트 정의, `om-apply/SKILL.md`, `CLAUDE.md`, `test_claude_wiring.py`.
- **83 부록 A 충족**: A-1 통과(9종 입출력 파일 전부에 스키마 경로 또는 양식 소유 코드를 명시했고 필드가 실측과 일치). A-2 통과(8단계 모두 4단 체크, exit 의미·CI 성공 취급·게이트별 판독법·재검증 원칙 포함). A-3 통과(4모드 표, upgrade 3층 검증, `path-remap` 커버리지 규칙이 `collectors.py:769-833`과 문자열까지 일치). A-4 부분 통과(개선 6번 참조).
- **미확인**: (1) 이 환경에서 `Glob`·`Grep`이 계속 `ENOEXEC`로 실패해 직접 경로 읽기만으로 조사했다. `om-resume` 소유 파일이 사용자 수준(`~/.claude/`)이나 플러그인 경로에 있을 가능성을 배제하지 못했다. (2) 미등록 슬래시 명령 입력 시 Claude Code가 `UserPromptSubmit` 훅을 발화하는지 실행 검증하지 못했다 — 차단 2번의 실제 영향 크기는 이 동작에 좌우된다. (3) 공통 규칙 원문의 안티패턴 절은 직접 열람하지 않고 총계에서 역산했다. (4) `RULE_MANIFEST.yaml`은 일부만 열람하고 나머지는 원문 제목 열거로 대조했다. (5) `AUTHORING_REVIEW.md`·`SPEC_REVIEW.md`·1·2차 감사 보고서는 감사 원칙에 따라 근거로 사용하지 않았고 열람하지 않았다. (6) 설계서 원문 대조는 `DESIGN_REQUIREMENTS`의 저장소 근거 검증으로 갈음했다. (7) CLI를 실제로 실행하지 않았다(읽기 전용 감사).
- 파일은 하나도 수정하지 않았다.
