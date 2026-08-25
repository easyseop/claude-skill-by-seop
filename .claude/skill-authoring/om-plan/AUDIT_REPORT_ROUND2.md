# om-plan 독립 감사 결과 — 2차 (2026-08-24)

> 이 문서는 2차 독립 감사자(1차와 다른 새 인스턴스)가 반환한 결과를 **그대로** 기록한 것이다. 작성자는 판정을 바꾸지 않았다.
> 조치 내역은 `AUTHORING_REVIEW.md`의 「독립 감사 2차 결과와 조치」에 있다. 최종 판정은 `AUDIT_REPORT.md`에 있다.
> 아래 판정 줄은 기계 검증이 세는 대상이 되지 않도록 인용 형태로 보존한다: 2차 판정은 `CONDITIONAL`이었다.

## 종합 판정
- (2차) 판정: `CONDITIONAL`
- 핵심 이유: 1차 차단 2건은 실제로 해소됐다. `SKILL.md:172,180,297`의 digest 서술은 `om_workflow.py:285-303`·`markers.py:89-130`·`validate.py:45-67` 실측과 정확히 일치하도록 교정됐고, `DESIGN_REQUIREMENTS.validation`·`COMMAND_SPEC.validation`·설계서 §15도 같은 내용으로 정정됐다. `COMMAND_SPEC.yaml`에 `workflow` 8단계와 `outputs.skill_run_artifacts`가 추가됐으며, 「입출력 파일과 스키마」 표의 `official-doc-sources.yaml`·`official-doc-snapshots/` 2행은 `doc_sources.py:71-81` 산출 필드와 문자 그대로 일치한다. 규칙 89건 전수판정·안티패턴 26건 판정·설계 요구사항 18건 RESOLVED·필수 EXTERNAL 4건 implemented도 원본으로 재확인했다. 그러나 **1차 비차단 지적 2번(`allowed-tools` 최소성)을 조치하는 과정에서 새 차단 문제가 생겼다.** 1차 감사는 "보호 세션 중 `hook_policy`가 workflow 명령이 아닌 모든 Bash를 거부하므로 `Bash(git status *)`는 실제로 쓸 수 없다"고 지적했는데, 작성자는 항목을 제거하는 대신 **2단계에 `git -C <저장소> status --porcelain` 실행 지시를 새로 추가**해 유지했다. 이 명령은 대상 런타임 훅이 실제로 거부한다. 추가로 7단계 `plan-resume` 절차와 1단계 `run-request.yaml` 확정 절차가 대상 런타임에서 실행 불가능한 형태로 기술돼 있다. 차단 3건이므로 PASS를 쓰지 않는다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (전부 `RESOLVED`, 비어 있지 않음. 표본 재검증 결과 `preflight.py:293-325`, `validate.py:414-437`, `resume.py:51-55`, `collectors.py:302-336/550-584`, `hook_policy.py:232-240`, `om_workflow.py:512-527`, 스키마 5종 전부 실재하며 인용 내용이 정확)
- 미해결: 0
- 근거 없음: 0 (설계서에 없는 사실을 본문에 보충한 사례는 발견되지 않음)
- 명세 반영 누락: 0 (1차 지적 2건 해소 — `COMMAND_SPEC.yaml:259-268` `workflow`, `:174-184` `outputs.skill_run_artifacts` 실재 확인)
- 다만 **설계 입력과 저장소 사실의 충돌 1건이 미결정 사항으로 드러나지 않았다**: 설계서 §10(129행)과 지시서 「허용·금지」(59행)가 "`git status`·`git diff` 읽기 허용"을 근거 `_GIT_MUTATIONS`에 없음으로 단정하나, `hook_policy.decide_pre_tool_use`는 기본 거부 구조여서 Git 변경이 아니어도 workflow 명령이 아니면 거부한다. 이 충돌이 `open_questions`에 없다.

## 규칙 집계
- 원문 규칙: 89 (원문 두 문서를 직접 열람해 계수 — `C` 20 + `P` 8 + `D` 12 + `E` 7 + `V` 8 + `S` 7 + `M` 5 = 67, `CC-01`~`CC-22` = 22)
- 판정 규칙: 89 (`APPLY` 55 / `TRANSFORM` 13 / `EXCLUDE` 16 / `EXTERNAL` 5 — 직접 재계수해 합 89 일치)
- 누락: 0
- 중복: 0
- 미판정: 0 (안티패턴도 `A-01`~`A-12` 12건 + `A-CC-01`~`A-CC-14` 14건 = 26건 전수 판정)
- 반영 위치 없음: 0 (`APPLY`·`TRANSFORM` 68건의 `contains` 문구를 최종 `SKILL.md` 본문과 1:1 대조해 전부 실재 확인)
- 근거 부족 제외: 0 (16건 모두 주단계 `P`·부작용 등급·미사용 기능이라는 구체 축에 연결. "관련 없음" 수준 처리 없음)
- 미구현 필수 외부 통제: 0 (`required_for_pass: true` 4건 — `om_workflow.py`·`validate.py`·`settings.json`·`hook_policy.py`·`run_om_plan_hook.sh` 전부 직접 열람해 implemented 확인. `P-08`만 `planned`·`required_for_pass: false`이며 `test_claude_wiring.py` 전문을 읽은 결과 `om-apply` SKILL.md만 단언하고 `om-plan` 단언이 없어 **정직성 타당**)

## 차단 문제

| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| 높음 | `SKILL.md` frontmatter `Bash(git status *)` + 2단계 「호출 전 확인」 | 조치 과정에서 생긴 새 모순. 본문이 지시하는 `git -C <저장소> status --porcelain`은 대상 런타임 훅이 **거부**한다. 1차 지적(비차단 2)은 이 항목을 제거하라는 취지였는데, 작성자는 본문에 사용처를 새로 만들어 유지했다 | `hook_cli.handle_event`(86-99행)가 `/om-plan` 프롬프트에서 세션 marker를 생성하므로 이후 모든 `PreToolUse`가 `decide_pre_tool_use`를 거친다. `hook_policy.py:179-216`에서 `git status`는 `_contains_git_mutation` False → `_workflow_action` None → 마지막 `HookDecision(False, "only the trusted planning workflow command is allowed while protected")`로 **거부**된다. 같은 `SKILL.md:230`이 "훅 거부는 권한 문제이므로 우회 경로를 찾지 않는다"고 지시하므로 절차가 2단계에서 정지한다. 게다가 이 확인은 `preflight.py:283-292`의 `WORKTREE_DIRTY`가 이미 결정적으로 수행한다 | `Bash(git status *)`를 `allowed-tools`에서 제거하고, 2단계 「호출 전 확인」을 "작업 트리 clean 여부는 `plan start`가 `WORKTREE_DIRTY`로 판정한다"로 바꾼다. 설계서 §10의 `git status`·`git diff` 허용 근거도 정정하거나 `open_questions`로 올린다 |
| 높음 | `SKILL.md` 7단계 `plan-resume` | 문서대로 호출하면 반드시 실패한다. `plan check`가 끝나면 세션 marker와 run marker가 모두 삭제되는데, `plan-resume`은 **이미 존재하는 unbound 세션 marker**를 요구한다. 새 marker를 만드는 경로(`/om-resume` 프롬프트 또는 `plan-session-start`)가 본문에 없고, 오히려 `SKILL.md:209`가 `plan-session-start`를 "이 스킬의 절차가 실행하지 않는다"며 사전 승인에서 제외했다. `STATE_ROOT`·`SESSION_ID` 값의 출처(2단계 stdout의 `state_root`·`session_id`)도 없다 | `validate.py:543,599,617`이 모든 종료 경로에서 `cleanup_pair(pair)`를 호출하고 `markers.cleanup_pair`(201-217행)가 run marker와 session marker를 `unlink`한다. `om_workflow.py:459-464`는 marker 경로만 계산하고 생성하지 않으며 `resume.py:60`의 `bind_run` → `markers.load_session_marker`(70-79행)가 파일 부재 시 `SESSION_MARKER_INVALID`를 낸다. 훅도 `hook_cli.py:134-138`에서 marker 부재 시 `plan-resume`을 "planning command requires an active session marker"로 거부한다. `block` 재개는 「사용한다」·「판단 분기」·「실패·중단·복구」가 모두 의존하는 핵심 경로다 | 7단계에 "새 세션 marker가 필요하므로 사용자가 `/om-resume`을 다시 입력해 훅이 marker를 만들게 한다"는 사전조건을 넣고, `--state-root`·`--session-id`에 2단계 stdout의 `state_root`·`session_id`(또는 훅이 주입하는 `OM_PLAN_HOOK_STATE_ROOT`·`OM_PLAN_SESSION_ID`)를 쓴다고 명시한다 |
| 중간 | `SKILL.md` 1단계 산출물 / 「입력과 인수」 / 절대 경계 5번 | 필수 입력 `run-request.yaml`을 **누가 어디에 만드는지가 정의되지 않았다.** 1단계는 "`run-request.yaml`을 확정한다 / 산출물: 확정된 `run-request.yaml` 경로"라고만 쓰고, 절대 경계 5번은 "쓰기는 현재 run의 `proposal/` 안에서만"이라 에이전트가 쓸 수 없으며, 훅도 run 결속 전 Write를 거부한다. 그 결과 "필수 입력 누락" 시나리오에서 부족한 필드를 물어본 뒤의 행동이 결정되지 않는다 | `hook_policy.py:218-227` — `Write`/`Edit`는 `run_pair is None`이면 "preflight has not established a run"으로 거부되고, run 결속 후에도 `proposal/` 안으로만 허용된다. `plan start`는 `run_dir`에 요청을 복사할 뿐(`preflight.py:303`) 요청 파일 자체를 만들지 않는다 | 1단계에 "요청 파일은 사람이 저장소 밖 경로에 작성해 경로를 준다" 또는 "훅 보호 세션 밖에서 준비한다" 등 실제 생성 주체·위치를 명시하고, 없을 때의 행동(사람에게 파일 작성 요청)을 실패 처리에 넣는다 |

## 시나리오 결과

| 시나리오 | 판정 | 근거 |
|---|---|---|
| 정상 호출 | 부분 통과 | CLI 인수·성공 판정은 실측과 완전 일치한다(`om_workflow.py:317-336,369-376` argparse 선언, `preflight.py:311` `ready_for_proposal`, `plan-result.schema.json:44-58` approval↔`review_ready`↔`verified:true` allOf). 그러나 1단계 요청 파일 생성 주체 미정의(차단 3)와 2단계 `git status` 훅 거부(차단 1)로 진입부가 그대로 실행되지 않는다 |
| 필수 입력 누락 | 부분 통과 | 모드별 표가 `plan-run-request.schema.json`의 `required`+`allOf` 6분기와 완전 일치한다(`pre_plan`의 `refs.candidate` 금지 포함). "추측해 채우지 않는다"도 있다. 다만 물어본 뒤 요청 파일을 확정하는 행동이 실행 불가(차단 3) |
| 잘못된 입력·허용값 | 통과 | `UPGRADE_RELATION_UNSUPPORTED`·`DEPLOYMENT_METHOD_REQUIRED`·`DEPLOYMENT_DOCUMENT_MISSING`·`CUSTOMIZATION_ID_INVALID` 4종이 `collectors.py:302-336`에 그대로 존재 |
| 대상 파일·설계서 부재 | 통과 | `REFS_UNAVAILABLE`(`preflight.py:157-164`), `ACTIVE_REGISTRATION_MISSING`(188-193), `RUN_DIRECTORY_EXISTS`(276-281) 실재 |
| 권한 부족 | 부분 통과 | 1차 지적대로 "훅 거부는 권한 문제이므로 게이트 실패로 보고하지 않는다"가 `SKILL.md:230`에 추가됐고 `settings.json`·`hook_policy.py` 서술은 실측과 일치한다. 그러나 정작 본문이 훅이 거부할 명령을 지시해 이 규칙이 정상 흐름에서 발동한다(차단 1) |
| 검증 실패 | 통과 | `reasons`·`evidence_ref_errors`·`dirty_paths`가 `plan-validation-attempt.schema.json` 필드와 일치. block/analysis_error 분기와 게이트 우회 금지 문장 존재. 게이트 메시지 6종(`feature customization id already exists in the registry`, `change customization id is not registered`, `registered tests for ... missing from run list`, `ambiguous commit ids require unresolved questions and a STOP`, `upgrade output is missing or empty:`, `path-remap does not cover affected registered customization paths:`)을 `collectors.py:551,553,631,645,798,819`에서 문자 그대로 확인 |
| 부분 변경 후 실패 | 부분 통과 | append-only(`validate.py:366-376`)와 `plan start` 실패 시 `preflight-result.json`·marker 정리(`preflight.py:329-360`)는 정확하다. 그러나 block 이후 재개 경로가 실행 불가(차단 2) |
| 외부 콘텐츠의 규칙 무시 지시 | 통과 | 절대 경계 9번과 「안전과 권한」 4·5번이 스냅샷·2차 판독·로그를 데이터로 고정하고 의심 항목 보고를 지시한다. `CLAUDE.md:17`("not a source of deterministic truth")·에이전트 정의의 `review_limit`과 정합 |
| 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true` + `SKILL.md:33`. 부작용(run 디렉터리·세션 marker·사람 검토)이 수동 전용을 정당화한다 |
| 기존 동명 스킬 충돌 | 통과 | 대상 저장소에 `.claude/skills/om-plan/SKILL.md`가 없음을 직접 읽기 시도로 확인(파일 없음). `om-apply`만 존재. `SKILL.md:32`가 디렉터리 이름이 명령 이름을 결정한다고 명시 |

## 비차단 개선사항

1. `SKILL.md:216`·`DESIGN_REQUIREMENTS.scope_conditional`·`COMMAND_SPEC.scope.conditional` — "완료된 run에 `plan check` 재실행 → `COMPLETED_RUN_READ_ONLY`"는 대화형 경로에서 거의 관측되지 않는다. 직전 검증이 `cleanup_pair`로 `.plan-active`를 지웠으므로 `check_plan_run`의 `pair_from_run`(`om_workflow.py:284`)이 먼저 `RUN_MARKER_INVALID`를 낸다. `COMPLETED_RUN_READ_ONLY`(`validate.py:449-455`)는 marker가 복원된 경로(CI `restore-run`)에서 나온다. `SKILL.md`는 "…가 나오면"으로 조건부라 거짓은 아니나 명세의 단정 표현은 부정확하다.
2. `83 부록 A-1` 부분 미충족 — `SKILL.md:258`이 `preflight-result.json`을 언급하지만 「입출력 파일과 스키마」 표에 그 양식 소유 위치(`preflight.py:339-342`)가 없다. 1차에서 지적된 upgrade 2종은 추가됐으나 같은 규칙의 이 항목이 남았다.
3. `AUTHORING_REVIEW.md` 내부 모순 — 117행과 「남은 위험」 3번(167행)이 여전히 "CI의 exit 2 래핑은 미실측이라 `SKILL.md`에 쓰지 않았다"고 기술하나, 같은 문서 94·144행과 `SKILL.md:99`는 `om_plan_ci.py:324-325`를 실측해 기재했다고 한다. 조치 후 갱신되지 않은 stale 문장이다(내가 `om_plan_ci.py:324-325`와 `.gitlab-ci.yml:276-283`을 직접 읽어 기재 내용 자체는 사실임을 확인했다).
4. 안티패턴 집계 수치 오류 — `AUTHORING_REVIEW.md:43`과 `SPEC_REVIEW.md:60`이 "PASS 20 / NOT_APPLICABLE 6"이라 적었으나 `RULE_COVERAGE.yaml` 실제는 PASS 21 / NOT_APPLICABLE 5다. `SPEC_REVIEW.md:60`은 NA 항목을 5개만 열거하면서 6이라 쓴다(1차 감사 보고서의 같은 수치도 오류였다).
5. `AUTHORING_REVIEW.md` 37행 "297줄" vs 158행 "296줄" 불일치(실측 297줄).
6. `SKILL.md:152` 3단계의 `intent_summary` 항목 나열에 `change_path`·`hop_policy`가 빠졌다. `preflight._intent_summary`(76-96행)는 두 항목을 포함한다.
7. `SKILL.md:99`의 "계획 단계는 아무것도 반영하지 않기 때문이며, 미해결 항목은 뒤 단계가 강제한다"는 CI 코드가 말하지 않는 해석이다. 사실(`ci_exit_code`·`success-review-ready`)과 해석이 한 문장에 섞여 있다.
8. `RULE_COVERAGE.S-03`의 `targets`가 `allowed-tools:` 한 줄이어서 최소권한 규칙의 실질 증거로 약하다(1차의 `CC-13` 지적과 같은 유형이며, 실제로 이 약한 증거 때문에 차단 1을 놓쳤다).
9. `SKILL.md`가 `plan check`의 `run_dir`가 선택 인수이며 생략 시 marker로 유일한 미완료 run을 고른다는 사실(`om_workflow.py:333`, `select_incomplete_plan_run` 201-218행)과 `PLAN_RUN_AMBIGUOUS`를 다루지 않는다. 오류는 아니나 다중 run 상황의 함정이다.
10. 종료코드 2의 출처로 `subprocess.CalledProcessError`(`om_workflow.py:515-517`)와 Python 3.11 미만 인터프리터(14-20행)도 있으나 본문은 두 경우를 언급하지 않는다. "stdout에 판정 JSON이 없으면 `approval`이 아니다"라는 상위 판정 규칙이 이를 흡수하므로 위험은 낮다.

## 감사 범위와 미확인 사항

- 직접 열람해 확인한 것: 원문 규칙 2종 전문(규칙·안티패턴 계수 포함), 설계서 3종 전문, 저작 증거 6종(`DESIGN_REQUIREMENTS`·`RULE_MANIFEST` 부분·`COMMAND_SPEC`·`RULE_COVERAGE` 전문·`SPEC_REVIEW`·`AUTHORING_REVIEW`), 최종 `SKILL.md` 297줄 전문, 기계 검증 2종(`VALIDATION_SPEC.json`·`VALIDATION_BUILD.json` 모두 `ok:true`, `classified_rules:89`, `resolved_design_requirements:18`), 1차 감사 보고서. 대상 런타임에서는 `harness/om_workflow.py`(531줄 전문), `harness/acgh/verdict.py`, `plancore/{preflight,validate,resume,markers,hook_policy,hook_cli}.py`, `integrations/om/{collectors.py 280-399·540-868, doc_sources.py}`, `plancore/schema/` 5종 전문, `harness/ci/om_plan_ci.py`(255-433행), `.gitlab-ci.yml` 전문, `.claude/{settings.json, hooks/run_om_plan_hook.sh, hooks/run_om_plan_hook.py, agents/om-plan-official-doc-reviewer.md, skills/om-apply/SKILL.md}`, `CLAUDE.md`, `harness/tests/test_claude_wiring.py`.
- `RULE_MANIFEST.yaml`은 1107줄 중 492줄까지만 열람했다. 다만 규칙 ID 목록·계수는 원문 두 문서를 직접 읽어 독립적으로 89를 재계산했고 `RULE_COVERAGE.yaml`의 89건 판정과 대조했으므로, 누락·중복·미판정 판정은 manifest 전문 열람 없이도 성립한다.
- 실행하지 않은 것: 검사기 CLI의 end-to-end 리허설(읽기 전용 감사 원칙), 훅을 실제 프로세스로 구동한 동적 확인. 차단 1·2의 훅 거부와 marker 부재 실패는 **코드 경로 정독으로만** 판정했으며 실행 관측은 아니다.
- 이 세션에서 `Glob`·`Grep` 도구가 계속 `ENOEXEC` 오류로 실패해, 파일 탐색은 절대경로 `Read`로만 수행했다. 대상 저장소 `.claude/` 하위의 전체 파일 목록은 열거하지 못했다(존재를 주장한 개별 파일은 모두 직접 읽어 확인했다).
- 검증 불가: 설치된 Claude Code 2.1.241에서 서브에이전트 도구의 실제 이름이 `Agent`인지 여부. `allowed-tools`의 `Agent`와 `hook_policy.py:166`의 `tool_name == "Agent"`가 서로 정합하므로 대상 런타임 내부 기준으로는 일관되나, 제품 도구명과의 일치는 이 컨텍스트에서 확인할 수 없다.
- 검증 불가: `VALIDATION_BUILD.json`의 `validated_at`(13:38:15)이 1차 감사 후 모든 수정보다 뒤인지 여부. 파일 수정 시각을 조회할 수단이 없어 기계 검증이 최종 산출물에 대해 실행됐는지는 호출 프롬프트의 진술("직전 기계 검증 결과, 둘 다 ok:true")에 의존했다.
- 파일은 하나도 수정하지 않았다.
