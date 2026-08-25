# om-plan 작성 검토

근거 약어: `CHK:` = `/Users/seop/Documents/Codex/2026-07-24/sites-plugin-sites-openai-bundled/work/kb-datacatalog-upgrade-checker-om-plan-cli/`, `DOC83:` = `.../skill_develop/om_plan/83_Codex_SKILLmd_작성지시_20260824.md`, `DOC24:` = `.../skill_develop/om_plan/24_누락감사_사람결정과_기록_20260820.md`, `DOC정리:` = `.../skill_develop/공유정리/하위_om-plan_논의정리_20260821.md`, `설계서:` = `docs/om-plan/OM_PLAN_DESIGN.md`, `지시서:` = `지시서_om-plan_스킬저작_20260824.md`.

## 설계 요구사항 추적

| 설계 요구사항 | 근거 출처 | COMMAND_SPEC 반영 위치 | 최종 파일 반영 위치 | 판정 |
|---|---|---|---|---|
| `purpose` | 설계서 §1, 지시서 「목적과 결과」 | `purpose` | `## 목적` | 반영 |
| `user_outcome` | 설계서 §1, `CHK:harness/acgh/plancore/preflight.py:293-305`, `validate.py:437` | `user_outcome` | `## 목적`, `## 최종 보고 형식` | 반영 |
| `use_when` | 설계서 §2, 스키마 `mode` enum, `resume.py:51-55` | `scope.include`, `invocation.examples` | `## 사용한다` | 반영 |
| `do_not_use_when` | 설계서 §3, `CHK:.claude/skills/om-apply/SKILL.md:8-9`, `DOC83:작업 2` | `scope.exclude` | `## 사용하지 않는다` | 반영 |
| `invocation_examples` | 설계서 §4, 지시서 「호출 예」 | `invocation.examples` | frontmatter `argument-hint`, `## 입력과 인수` | 반영(예시 문장은 본문에 복사하지 않고 인수 계약으로 변환 — A-CC-12) |
| `inputs_and_defaults` | 설계서 §5, `plan-run-request.schema.json`, `om_workflow.py:65-122,321-336` | `inputs` | `## 입력과 인수`, `## 입출력 파일과 스키마`, 모드별 표, 2단계 | 반영 |
| `trusted_and_untrusted_sources` | 설계서 §6, `CHK:CLAUDE.md:17-19`, 에이전트 정의 | `inputs.trusted_sources`/`untrusted_sources` | 절대 경계 9번, `## 안전과 권한` | 반영 |
| `scope_include` | 설계서 §7 | `scope.include` | `## 사용한다`, `## 절차` | 반영 |
| `scope_exclude` | 설계서 §8 | `scope.exclude` | `## 사용하지 않는다`, 절대 경계 4번 | 반영 |
| `scope_conditional` | 설계서 §9 | `scope.conditional` | `## 판단 분기`, 5단계, 7단계 | 반영 |
| `permissions_allow` | 설계서 §10, `hook_policy.py:163-177,214-227` | `permissions.allow` | frontmatter `allowed-tools`, `## 안전과 권한` | 반영 |
| `permissions_deny` | 설계서 §11, `.claude/settings.json`, `validate.py:143,371-377,452-456` | `permissions.deny` | `## 절대 경계` 1~10번 | 반영 |
| `approval_required` | 설계서 §12, `preflight.py:311-325`, `validate.py:414-424` | `permissions.approval_required` | `## 승인이 필요한 지점` | 반영 |
| `workflow` | 설계서 §13, `DOC83:부록 A-2` | `workflow`(1차 감사 후 추가) | `## 절차` 1~8단계 + 저수준 명령 | 반영 |
| `outputs` | 설계서 §14 | `outputs`(+`outputs.skill_run_artifacts`, 1차 감사 후 추가) | `## 입출력 파일과 스키마`(upgrade 2종 포함), `## 최종 보고 형식` | 반영 |
| `validation` | 설계서 §15 | `validation` | `## 판정과 종료코드`, `## 완료 조건`, 각 단계 성공 판정 | 반영(평가 시나리오 목록 자체는 본문 밖 — V-01~V-03 EXCLUDE 사유 참조) |
| `failure_handling` | 설계서 §16, `verdict.py:9-13`, `resume.py:51-55` | `failure_handling` | `## 실패·중단·복구`, 각 단계 실패 시 | 반영 |
| `completion_conditions` | 설계서 §17, `hook_policy.py:232-240` | `completion_conditions` | `## 완료 조건` | 반영 |

미해결 설계 요구사항 0건. 근거 없는 보충 0건. `open_questions`는 4건 중 1건(CI의 exit 2 취급)이 1차 감사 후 실측으로 해소돼 본문에 기재됐고, 남은 3건은 본문에 사실로 기재하지 않고 `COMMAND_SPEC.yaml`·`SPEC_REVIEW.md`에만 남겼다.

## 최종 프로필

- 명령 이름 `/om-plan`, 설치 경로 `.claude/skills/om-plan/SKILL.md`, 작업 유형 `new`.
- 주단계 `P`, 보조단계 `R`·`V`.
- 호출 주체: 사용자 전용(`disable-model-invocation: true`).
- 부작용 등급: 로컬 쓰기(새 run 디렉터리와 `proposal/`만).
- 실행 컨텍스트: inline·동기. 서브에이전트는 upgrade의 `om-plan-official-doc-reviewer` 1회뿐.
- 최종 파일: `SKILL.md` 301줄, 보조 파일 없음.

## 규칙 집계

- 원문 규칙 89 / 판정 89 / 누락 0 / 중복 0 / 미판정 0.
- `APPLY` 55, `TRANSFORM` 13, `EXCLUDE` 16, `EXTERNAL` 5.
- 안티패턴 26 / `PASS` 21 / `NOT_APPLICABLE` 5 / 미판정 0. (`NOT_APPLICABLE`은 `A-CC-05`·`A-CC-06`·`A-CC-07`·`A-CC-08`·`A-CC-14` 다섯 건이다. 이전 기록의 20/6은 계수 오류였고 2차 감사 지적으로 정정했다.)
- 단계 모듈: `primary: P`, `secondary: [R, V]`, 세 모듈 모두 `applied: true`.

## APPLY·TRANSFORM 반영 위치

68건 전부 `RULE_COVERAGE.yaml`의 `targets`에 `{file: SKILL.md, contains: <검색 가능 문구>}` 형태로 기록했고, 각 문구가 최종 `SKILL.md`에 실제로 존재하는지 스크립트로 대조해 전부 일치를 확인했다. 대표 예:

- `C-08`(조건–행동–검증–실패) → 각 단계의 `- 호출 전 확인:` / `- 성공 판정:` / `- 실패 시:` 4단 형식. `DOC83:부록 A-2`가 요구한 형식과 같다.
- `C-19`(금지에 대안) → "**게이트 실패는 제안을 고쳐 재검증한다. 우회하지 않는다.**"
- `P-06`(결정적·재량 분리) → "검사기는 `plan check`에서 저장소를 다시 훑어 사실을 재계산하고 저장본과 대조한다."
- `D-12`(동적 사실 고정 금지) → 절대 경계 10번 "버전·ID 목록·경로를 기억으로 쓰지 않는다."
- `CC-06`(allowed-tools 오해 금지) → "`allowed-tools`는 해당 턴의 **사전 승인**이지 도구 제한이 아니다."
- `CC-14`(CLAUDE.md 관계) → 5단계가 `CHK:CLAUDE.md:7-15`의 upgrade 2차 판독 절차를 최소한으로 재명시한다. 이 스킬이 검사기 저장소로 이식된 뒤에도, `CLAUDE.md`를 읽지 않는 실행 경로에서 절차가 사라지지 않게 하기 위함이다.
- `M-05`(계획 문서에 결정·결과) → `decisions[]` 6개 필수 필드 문장과 append-only `validation-attempts` 문장.

## EXCLUDE 사유 검토

16건 모두 대상 주단계(`P`)·부작용 등급(로컬 쓰기)·입출력(계획 run 디렉터리)에 근거한 비적용 사유를 적었다. "관련 없음" 한마디로 처리한 항목은 없다. 근거 축은 세 가지다.

1. **규칙 문서를 소유하지 않음** — `C-20`·`M-01`·`M-02`·`M-03`·`M-04`·`CC-20`. om-plan의 산출물은 계획 run이고 규칙 파일 생성·개정은 금지 목록에 있다.
2. **평가·발동 축이 없음** — `V-01`·`V-02`·`V-03`·`CC-18`. `disable-model-invocation: true`라 발동 평가 대상이 존재하지 않고, 평가 시나리오는 `COMMAND_SPEC.yaml`의 `validation`에 실제로 기록했다(A-CC-12에 따라 본문에 두지 않았다).
3. **해당 기능을 쓰지 않음** — `CC-09`·`CC-10`(fork·background 미사용), `CC-11`(`!` 주입 미사용), `CC-12`(보조 파일 없음), `CC-19`(버전 의존 필드 미사용), `CC-22`(플랫 커맨드 아님). 각 항목에 "왜 쓰지 않기로 했는지"까지 적었다.

## EXTERNAL 구현 상태

| 규칙 | 유형 | 경로 | 상태 | 필수 |
|---|---|---|---|---|
| `D-09` | script | `CHK:harness/om_workflow.py`, `CHK:harness/acgh/plancore/validate.py` | implemented(실측) | 예 |
| `S-07` | permission·hook | `CHK:.claude/settings.json`, `CHK:.claude/hooks/run_om_plan_hook.sh` | implemented(실측) | 예 |
| `CC-07` | policy | `CHK:harness/acgh/plancore/hook_policy.py` | implemented(실측) | 예 |
| `CC-21` | hook | `CHK:.claude/settings.json`(4개 훅 경로) | implemented(실측) | 예 |
| `P-08` | ci | `CHK:harness/tests/test_claude_wiring.py` | **planned** | 아니오 |

`P-08`만 미구현이다. 해당 파일은 존재하지만 현재 `om-apply` SKILL.md만 단언하며(44줄), `om-plan` 단언 추가는 `DOC83:작업 3`이 Codex에게 지시한 별도 작업이다. 이 저작의 쓰기 허용 범위 밖이므로 `required_for_pass: false`, `state: planned`로 정직하게 기록했고 통과로 처리하지 않았다.

## 문장별 최종 검토

저장된 최종 파일을 다시 열어 모든 의미 문장을 검토했다. 아래는 판단이 필요했던 항목과 그 결과다.

| 파일·줄 또는 섹션 | 문장·설정 요약 | 역할 | 근거 요구사항·규칙 ID | 구체적 유지 이유 | 판정 |
|---|---|---|---|---|---|
| frontmatter `description` | 4모드 계획 run·부작용·비적용 조건 | 호출 정책 | `CC-03`·`D-02`·설계서 §1~3 | 수동 전용 메뉴에서 `/om-apply`·`/om-verify`·`/om-report`와 구분하는 유일한 단서다 | 유지 |
| frontmatter `allowed-tools` | 항목 9개(도구 6 + Bash 패턴 3) | 권한 | `S-03`·`CC-06`·`hook_policy.py:163-227` | 절차가 실제로 실행하는 것만 사전 승인한다. `Bash(*)`를 쓰지 않았다. 1차 감사 후 미사용 항목 4개를 제거했다 | 축소 후 유지 |
| `## 설치와 호출` | 디렉터리 이름이 명령 이름을 결정 | 계약 | `CC-01`·02 문서 §5.3 | 이식 대상 저장소에서 경로가 바뀌면 명령 이름도 바뀐다는 사실이 실행에 영향을 준다 | 유지 |
| 절대 경계 1번 | 판정은 검사기가 한다 | 안전 | `P-06`·`V-05`·`validate.py:501-518` | 이 문장을 빼면 에이전트가 스스로 통과를 선언할 여지가 생긴다 | 유지 |
| 절대 경계 2번 | 종료코드를 재해석하지 않는다 | 안전 | `지시서:「허용·금지」`·`DOC83:부록 A-2` | 정본 지시가 명시적으로 요구한 경계다 | 유지 |
| 절대 경계 3번 | 게이트 실패는 고쳐 재검증, 우회 아님 | 안전 | `DOC83:부록 A-2`·`C-19` | 우회 대안(매니페스트 확장)이 실제 실패 사례로 기록돼 있다 | 유지 |
| 절대 경계 7번 | `validation-attempts/` append-only | 안전 | `validate.py:371-377` | 검사기가 `ATTEMPT_APPEND_ONLY_VIOLATION`으로 실제 거부한다 | 유지 |
| 절대 경계 8번 | 사람이 주지 않은 owner 금지 | 안전 | `collectors.py:580-584` | 검사기가 block하는 실제 게이트다 | 유지 |
| `## 판정과 종료코드` 표 0행 | `plan check`는 exit 0을 내지 않는다 | 사실 | `validate.py:524-531`·`verdict.py` `EXIT_CODE` | 코드 실측 결과. 0을 기대하는 오독이 실제로 가능하므로 표와 함정에 모두 둔다 | 유지 |
| `## 판정과 종료코드` 마지막 줄 | exit 2의 두 가지 출처 구분법 | 사실 | `om_workflow.py:512-516`·`verdict.py` | `WorkflowInputError`도 2를 낸다. 1차 감사 지적대로 argparse 오류는 `입력 확인 필요`를 내지 않으므로 판정 기준을 "stdout에 판정 JSON이 없으면 approval이 아니다"로 바꿨다 | 수정 후 유지 |
| `## 판정과 종료코드` exit 2 행 | 보호된 CI는 approval을 성공으로 처리 | 사실 | `DOC83:부록 A-2`·`DOC24:Q9`·`harness/ci/om_plan_ci.py:324-325` | 1차 감사 시점에는 미실측이라 뺐으나, 이후 CI 래퍼를 직접 읽어 `ci_exit_code = 0 if verdict in {pass, approval}`을 확인했다. 정본 지시가 요구한 항목이다 | 실측 후 추가 |
| 6단계 호출 전 확인·실패 시, 알려진 함정 7번 | digest는 항상 명시한다 | 안전 | `om_workflow.py:253,287,302`·`markers.py` | 1차 감사 차단 1. 기계가 사람 검토를 강제한다는 잘못된 단언을 제거하고, 대체가 일어난다는 사실과 그래서 항상 명시해야 한다는 행동으로 바꿨다 | 수정 후 유지 |
| 「입출력 파일과 스키마」 upgrade 2행 | `official-doc-sources.yaml`·`official-doc-snapshots/` | 계약 | `doc_sources.py` `collect_document_snapshots`·`DOC83:부록 A-1` | 1차 감사 차단 2. 본문 5단계와 층2가 이 파일들을 전제하면서 이름을 적지 않았다. 스키마 파일이 없고 양식 소유가 코드라는 사실까지 적었다 | 추가 |
| 「안전과 권한」 훅 거부 문단 | 훅 거부 ≠ 게이트 실패 | 판정 | `CC-16`·`hook_policy.py` | 1차 감사가 권한 부족 시나리오를 부분 통과로 판정했다. 권한 문제를 검사 실패로 오인하지 않게 하는 문장을 추가했다 | 추가 |
| 모드별 표 `필수 입력` 열 | 모드별 필수 필드 | 계약 | `plan-run-request.schema.json` `allOf` | 스키마 실측. `pre_plan`의 `refs.candidate` 금지까지 반영 | 유지 |
| 모드별 표 `필수 산출물` 열 | 모드별 제안 산출물 | 절차 | **upgrade 9종은 `collectors.py:786-800` 코드 실측. initial·feature·change 열은 `DOC정리:§2` 설계 논의 근거** | 근거 계층이 다르다. upgrade만 검사기가 강제하고 나머지는 설계 합의다. 본문에는 각 행의 `대표 실패 게이트` 열에 코드가 실제 강제하는 것만 적어 두 계층이 섞이지 않게 했다 | 유지(근거 계층 차이를 이 표에 기록) |
| 모드별 표 `대표 실패 게이트` 열 | 코드가 내는 실제 메시지 | 사실 | `collectors.py:300-338,573-635`·`preflight.py:182-192` | 메시지 문자열을 코드에서 그대로 옮겼다 | 유지 |
| `### upgrade 3층 검증` | 층1·층2·층3 | 절차 | `DOC24:Q11`(3층 결정) + `collectors.py:802-868`(층1·층2 구현) | 사람이 확정한 결정이며 코드에 실제 구현돼 있다 | 유지 |
| 층2 마지막 문장 | ground truth 아님을 사람 보고에 옮긴다 | 안전 | `CHK:CLAUDE.md:17`·에이전트 `review_limit`·`DOC24:Q11 층2` | 정직 고지 요구가 세 곳에 있다 | 유지 |
| 2단계 호출 | `python3 harness/om_workflow.py plan start REQUEST` | 계약 | `om_workflow.py:317-327` | 인수 실측. `om-apply` SKILL.md는 `python`을 쓰지만, `om_workflow.py:14-20`이 3.11+를 요구하고 훅이 `python3.12`·`python3.11`·`python3`를 탐색하며 CI는 venv python을 쓰므로 `python3`가 더 안전하다 | 유지(패턴 이탈 근거 기록) |
| 2단계 실패 코드 목록 | 9종 오류 코드 | 사실 | `preflight.py:158-192,278,289`·`collectors.py:306-333` | 코드에서 실제 발생하는 문자열만 나열했다 | 유지 |
| 6단계 성공 판정 | exit 2 + `review_ready` + `verified: true` | 계약 | `plan-result.schema.json` `allOf`·`validate.py:414` | 스키마가 approval에 두 조건을 강제한다 | 유지 |
| 7단계 실패 코드 | `RUN_NOT_PROPOSAL_REVISABLE` 등 4종 | 사실 | `resume.py:21,26,35,53` | 코드 실측 | 유지 |
| `### 저수준 명령` | 3개 명령의 인수와 종료코드 의미 | 계약 | `om_workflow.py:338-367,404-461` | **초안 수정 이력**: 처음에는 "세 명령 모두 세션 marker 없이 실행하며 종료코드 의미가 같다"고 썼으나 실측과 달랐다. `plan-preflight`는 marker를 요구하고 종료코드 0을 내며, `plan-validate`만 marker를 다루지 않고 `plan check`와 종료코드 의미가 같다. 명령별로 분리해 수정했다 | 수정 후 유지 |
| `## 안전과 권한` 1번 | 실제 차단은 훅과 permissions | 안전 | `S-02`·`.claude/settings.json`·`run_om_plan_hook.sh` | Markdown을 보안 경계로 오인하지 않게 한다 | 유지 |
| `## 완료 조건` 상태 5종 | 완료·조건부·승인 필요·중단·검증 불가 | 판정 | `CC-16`·`V-08` | `analysis_error`를 실패가 아닌 검증 불가로 분리해야 통과 오인을 막는다 | 유지 |
| `## 알려진 함정` 6·7번 | direct-only 테스트 거짓 block, 사람 검토 건너뛰기 | 함정 | `DOC24:D-directtest`·`validate.py:45-64` | 반복 확인된 실패와 스키마가 강제하는 사실이다 | 유지 |

### 제거·외부화한 문장

- 커맨드 프로필 표(02 문서 §3.4)는 본문에 넣지 않고 `SPEC_REVIEW.md`로 외부화했다. 02 문서가 "검토 보고서에는 남기되 최종 `SKILL.md` 본문에는 필요한 항목만 반영한다"고 규정하고 `A-CC-12`가 장황한 검토 이유를 금지한다.
- 규칙 ID 매핑과 채택 이유는 본문에서 전부 뺐다(`A-CC-01`·`A-CC-12`).
- 호출 예시 문장 3개는 본문에 복사하지 않고 `argument-hint`와 `## 입력과 인수`의 인수 계약으로 변환했다. 예시 자체는 `COMMAND_SPEC.yaml`의 `invocation.examples`에 있다.
- `open_questions` 4건(판정 상태 수 표기 불일치, R-4, R-1·R-2, `.gitlab-ci.yml` exit 2 래핑 실측 미확인)은 본문에 단정 문장으로 넣지 않았다. 특히 CI가 exit 2를 성공으로 취급한다는 문구는 결정 기록에만 있고 CI 파일에서 실측하지 않았으므로 `SKILL.md`에 쓰지 않았다.

## 독립 감사 1차 결과와 조치 (2026-08-24)

1차 독립 감사 판정은 `CONDITIONAL`이었다. 차단 문제 2건과 비차단 8건을 받았고, 각 지적을 원본 코드로 직접 재확인한 뒤 조치했다. 감사 보고서는 수정하지 않았고 `AUDIT_REPORT.md`에 그대로 기록했다.

### 차단 1 (높음) — digest 미제공 시 approval 도달 가능

- **지적**: `SKILL.md`가 "digest를 주지 않으면 `approval`이 될 수 없다"고 단언하는데 `plan check`에서는 거짓이다.
- **재확인 결과: 지적이 옳다.** `om_workflow.py:253`에서 `plan start`가 `record_trusted_input_lock_digest`로 digest를 세션 marker에 기록하고, `om_workflow.py:287`에서 `plan check`가 `trusted_input_lock_digest(pair.session_marker)`로 그 값을 읽어 `302`행에서 `supplied_digest or recorded_digest`로 넘긴다. 따라서 인수를 생략해도 `verified: true`가 되어 `approval`(2)에 도달한다. 강제되는 것은 인수를 그대로 전달하는 `plan-validate`(`om_workflow.py:450-457`)뿐이다.
- **조치**: 잘못된 단언 2곳을 교정했다. 6단계 실패 시 문장과 알려진 함정 7번을 "대체가 일어나므로 `approval`까지 간다. 사람이 보관한 digest를 명시해야 검토 생략이 드러난다"로 바꾸고, 6단계 호출 전 확인에 "`--expected-input-lock-digest`를 항상 명시한다"를 추가했다. `DESIGN_REQUIREMENTS.validation`·`COMMAND_SPEC.validation`의 같은 시나리오와 설계서 §15도 함께 정정했다. `approval_required` 1항에도 "기계적으로 강제되지 않는다"는 사실을 명시했다.

### 차단 2 (중간) — 절차·런타임 출력의 명세 이관 누락과 upgrade 산출물 미기재

- **지적**: `DESIGN_REQUIREMENTS`의 `workflow`·`outputs`가 `COMMAND_SPEC.yaml`으로 이관되지 않았고, 그 결과 `official-doc-sources.yaml`·`official-doc-snapshots/`가 `SKILL.md`에 없다.
- **재확인 결과: 지적이 옳다.** 두 파일은 실제 산출물이다. `doc_sources.py`의 `collect_document_snapshots`가 `official-doc-snapshots/NN-<이름>`에 원문을 쓰고 `official-doc-sources.yaml`을 `atomic_write`한다. `preflight.py:306-308`은 비-upgrade 모드에서 이 파일을 지우고, `validate.py:496-498`과 `om_workflow.py:466-469`가 `verify_document_snapshots`로 재검증한다. `83 부록 A-1`은 본문이 언급하는 모든 입출력 파일의 양식 소유 위치를 요구하는데, 본문 5단계와 층2가 이 스냅샷을 전제하면서 파일 이름을 적지 않았다.
- **조치**: `COMMAND_SPEC.yaml`에 `workflow`(8단계 4단 계약)와 `outputs.skill_run_artifacts`(run 디렉터리 산출 9종)를 추가했다. `SKILL.md`의 「입출력 파일과 스키마」 표에 두 행을 추가하고, 스키마 파일이 없으며 양식을 `doc_sources.py`가 소유한다는 사실과 필드 목록을 실측해 적었다.

### 비차단 조치

| 항목 | 조치 |
|---|---|
| `plan-validate`가 marker를 다루지 않는다는 서술 | 재확인 결과 부정확했다. `run_validation`이 `pair_from_run`으로 `.plan-active`를 요구하고 `cleanup_pair`로 정리한다. "marker를 **인수로** 받지 않지만 `.plan-active`를 요구하고 끝나면 정리한다"로 교정했다 |
| `allowed-tools` 최소성 | 절차가 실행하지 않는 `plan-preflight`·`plan-validate`·`plan-session-start`·`git diff` 사전 승인을 제거했다. `git status *`는 2단계의 clean 확인에 실제로 쓰이므로 유지하고, 해당 단계에 `git -C <저장소> status --porcelain` 명령을 명시했다. 사전 승인 축소이지 허용 행동 축소가 아님을 본문에 적었다 |
| `Stop` 훅을 다른 세 경로와 묶어 서술 | `Stop`은 `validation-result.json` 없는 종료를 막는 다른 통제임을 분리해 적었다 |
| `S-07` 훅 경로 표기 | `settings.json`이 실제 배선한 진입점은 `.sh`다. `RULE_COVERAGE.yaml`·`SPEC_REVIEW.md`·이 문서의 표기를 `.sh`로 교정했다 |
| exit 2 구분법 | argparse 오류도 2를 내며 `입력 확인 필요`를 출력하지 않는다. "stdout에 판정 JSON이 없으면 `approval`이 아니다"로 바꿨다 |
| `83 부록 A-2`의 CI exit 2 취급 미기재 | (해소) `harness/ci/om_plan_ci.py:324`를 실측해 `ci_exit_code = 0 if verdict in {pass, approval}`와 `success-review-ready`(325행)를 확인했다. 본문 「판정과 종료코드」에 기재하고 `open_questions` 4번을 해소로 바꿨다 |
| 증거 문서의 `allowed-tools` 수치 | "6종"을 "항목 9개(도구 6 + Bash 패턴 3)"로 정정했다 |
| `CC-13` 근거 약함 | rationale을 보강하고 `argument-hint`를 두 번째 target으로 추가했다 |
| 권한 부족 시나리오 부분 통과 | 「안전과 권한」에 "훅 거부는 권한 문제이므로 게이트 실패로 보고하지 않는다"를 추가했다(`CC-16`) |

수정 후 모든 `targets` 문구를 다시 대조했다. 문구가 바뀐 `C-09`·`S-01` 2건의 target을 갱신했고, 68건 전부 최종 파일에 실재함을 재확인했다. 설계서가 바뀌었으므로 `DESIGN_REQUIREMENTS.source_documents`의 sha256도 갱신했다.

## 독립 감사 2차 결과와 조치 (2026-08-24)

2차 독립 감사(1차와 다른 새 인스턴스) 판정도 `CONDITIONAL`이었다. 1차 차단 2건은 해소됐다고 확인받았으나 **차단 3건이 새로 지적됐고, 그중 1건은 1차 조치 과정에서 내가 새로 만든 오류였다.** 각 지적을 원본 코드로 직접 재확인한 뒤 조치했다. 감사 보고서는 수정하지 않았고 `AUDIT_REPORT_ROUND2.md`에 그대로 기록했다.

### 차단 1 (높음) — 보호 세션 중 `git status`는 훅이 거부한다 (1차 조치가 만든 오류)

- **지적**: 1차 비차단 2번은 `Bash(git status *)`를 제거하라는 취지였는데, 나는 제거 대신 2단계에 `git -C <저장소> status --porcelain` 실행 지시를 새로 만들어 유지했다. 그 명령은 훅이 거부한다.
- **재확인 결과: 지적이 옳다.** `hook_cli.handle_event`의 `UserPromptSubmit` 분기가 `/om-plan`·`/om-resume`으로 시작하는 프롬프트에서 `create_session_marker`를 호출한다. 따라서 보호는 **스킬이 시작되는 순간부터** 유효하다. 이후 모든 `PreToolUse`가 `decide_pre_tool_use`를 거치는데, `git status`는 `_contains_git_mutation`이 False이고 `_workflow_action`도 None이므로 마지막 기본 거부 분기 `"only the trusted planning workflow command is allowed while protected"`에 걸린다. 게다가 이 확인은 `preflight.py`의 `WORKTREE_DIRTY`가 이미 결정적으로 수행하므로 애초에 중복이었다.
- **조치**: `allowed-tools`에서 `Bash(git status *)`를 제거하고(현재 8개 항목), 2단계 「호출 전 확인」을 "저장소 clean·run 신규·등록부 상태를 직접 확인하지 않는다. 보호 세션 중 plan 계열 외 명령은 훅에 거부되고 이 셋은 `plan start`가 결정적으로 판정한다"로 바꿨다. 설계서 §10의 허용 항목을 철회하고 그 근거 오류(`_GIT_MUTATIONS` 부재만으로 판단한 것)를 §20 미결정 사항과 `open_questions`에 정정 기록했다. `DESIGN_REQUIREMENTS.permissions_allow`·`COMMAND_SPEC.permissions.allow`도 함께 정정했다.
- **교훈**: 1차 감사의 "실제로 쓸 수 없다"는 지적을 "사용처를 만들면 된다"로 잘못 읽었다. 허용 여부의 근거는 규칙 목록의 부재가 아니라 기본 거부 구조 전체다.

### 차단 2 (높음) — `plan-resume`이 문서대로면 반드시 실패한다

- **지적**: `plan check`가 끝나면 marker 쌍이 지워지는데 7단계는 새 marker를 만드는 경로를 적지 않았고, `STATE_ROOT`·`SESSION_ID`의 출처도 없다.
- **재확인 결과: 지적이 옳다.** `run_validation`은 모든 종료 경로에서 `cleanup_pair`를 부르고 `markers.cleanup_pair`가 run marker와 session marker를 `unlink`한다. `om_workflow.py`의 `plan-resume` 분기는 `session_marker_path`로 경로만 계산하며 marker를 만들지 않고, `resume_proposal_run`의 `bind_run` → `load_session_marker`가 파일 부재 시 실패한다. 훅도 marker 부재 시 plan 계열 명령을 `"planning command requires an active session marker"`로 거부한다. `block` 재개는 「사용한다」·「판단 분기」·「실패·중단·복구」가 모두 의존하는 핵심 경로다.
- **조치**: 7단계 「호출 전 확인」에 "새 세션 marker가 필요하다. 사용자가 `/om-resume`을 새로 입력해 훅이 marker를 만들게 한다"를 넣고, marker 없이 호출했을 때의 두 실패 경로(훅 거부 / `SESSION_MARKER_INVALID`)를 적었다. 호출 블록 아래에 "`STATE_ROOT`·`SESSION_ID`는 지어내지 않는다 — 훅이 주입하는 `OM_PLAN_HOOK_STATE_ROOT`·`OM_PLAN_SESSION_ID`를 쓰고, 훅 밖이면 2단계 stdout의 `state_root`·`session_id`를 쓴다"를 추가했다. 설계서 §13 7단계와 `DESIGN_REQUIREMENTS.workflow[6]`·`COMMAND_SPEC.workflow`도 같은 내용으로 정정했다.

### 차단 3 (중간) — `run-request.yaml`의 작성 주체가 정의되지 않았다

- **지적**: 필수 입력인 요청 파일을 누가 어디에 만드는지가 없다. 절대 경계 5번은 쓰기를 `proposal/` 안으로 제한하고, 훅은 run 결속 전 모든 쓰기를 거부하므로 에이전트는 이 파일을 쓸 수 없다.
- **재확인 결과: 지적이 옳다.** `hook_policy`의 `Write`/`Edit` 분기는 `run_pair is None`이면 `"preflight has not established a run"`으로 거부하고, run 결속 후에도 `proposal/` 안으로만 허용한다. `plan start`는 요청을 run 디렉터리로 복사할 뿐 파일을 만들어 주지 않는다.
- **조치**: 1단계 입력을 "사람이 준비한 `run-request.yaml` 경로"로 바꾸고, "이 파일은 에이전트가 만들지 않는다 — 요청 파일은 사람이 보호 범위 밖에서 작성해 경로로 전달한다"를 행동에 명시했다. 실패 처리를 "필요한 값을 사용자에게 알리고 파일 작성 또는 수정을 요청한다. 추측해 채우지 않고 대신 쓰지도 않는다"로 바꿨다. 산출물도 "경로만 확정한다"로 정정했다. 설계서 §13 1단계와 `DESIGN_REQUIREMENTS.workflow[0]`도 같이 고쳤다.

### 비차단 조치

| 항목 | 조치 |
|---|---|
| `preflight-result.json` 양식 소유 위치 누락(83 A-1) | 「입출력 파일과 스키마」 표에 행을 추가했다. 스키마 파일이 없고 `preflight.py`가 양식을 소유하며 `status`·`code`·`message`·`details`를 가진다 |
| `intent_summary` 항목 누락 | `_intent_summary`가 포함하는 `change_path`·`hop_policy`를 3단계 나열에 추가했다 |
| CI exit 2 서술에 해석이 섞임 | "CI 래퍼가 `approval`을 CI 종료코드 0과 `success-review-ready`로 매핑한다"는 실측 사실과, 그 근거가 사람 결정이라는 설명을 분리했다 |
| `plan check`의 `run_dir` 선택성·`PLAN_RUN_AMBIGUOUS` 미기재 | 호출 블록 아래에 생략 가능성과 다중 run 시 중단을 적고 run 디렉터리를 명시하라고 지시했다 |
| `COMPLETED_RUN_READ_ONLY` 단정 표현 | 대화형 경로에서는 marker가 이미 지워져 `RUN_MARKER_INVALID`가 먼저 나오고 marker 복원 경로에서만 `COMPLETED_RUN_READ_ONLY`가 나온다는 사실을 「판단 분기」에 반영했다 |
| 안티패턴 집계 오류 | 실제는 `PASS` 21 / `NOT_APPLICABLE` 5다. 이 문서와 `SPEC_REVIEW.md`의 "20/6"을 정정했다. 1·2차 감사 보고서에도 같은 오류가 있었으나 감사 보고서는 수정하지 않았다 |
| 줄 수 불일치 | 실측값 301줄로 통일했다 |
| `AUTHORING_REVIEW.md`의 stale 문장 | 「남은 위험」의 "CI exit 2 미실측" 항목을 해소 상태로 갱신했다 |
| `S-03` 근거 약함 | `targets`가 `allowed-tools:` 한 줄이라 최소권한의 실질 증거로 약하다는 지적은 타당하다. 다만 이번 라운드에서는 `allowed-tools` 자체를 축소하는 실질 조치를 우선했고, 근거 문구 보강은 남은 개선사항으로 둔다 |

수정 후 모든 `targets` 문구를 다시 대조했다. 문구가 바뀐 `D-05`·`E-01`·`E-02` 3건의 target을 갱신했고(특히 `E-02`는 "실행 전 상태 확인"의 의미를 "확인 불가능한 것을 흉내내지 않고 검사기의 결정적 판정에 맡긴다"로 재해석해 rationale도 고쳤다), 68건 전부 최종 파일에 실재함을 재확인했다. 설계서가 다시 바뀌었으므로 `DESIGN_REQUIREMENTS.source_documents`의 sha256도 갱신했다.

## 기계 검사 결과

| 검사 | 명령 | 결과 | 증거 |
|---|---|---|---|
| 메타스킬 스크립트 무결성 | `python3 -m py_compile` 3개 스크립트 | 통과 | 출력 `PY_COMPILE OK` |
| spec 게이트 | `validate_authoring.py --phase spec` | 통과(exit 0) | `VALIDATION_SPEC.json`: `ok: true`, `classified_rules: 89`, `resolved_design_requirements: 18` |
| 이름 자리표시자 | `SKILL.md`의 `$` 치환 추출 | `['ARGUMENTS']`만 사용 | 미선언 명명 인수 0건 |
| 본문 길이 | 줄 수 계수 | 301줄(500줄 경고선 아래) | `C-06` 점진적 공개 기준 충족 |
| `targets` 문구 실재 | 68개 규칙의 모든 `contains` 문자열 대조 | 전부 존재 | 대조 스크립트 출력 "all snippets verified present" |
| build 게이트 | `validate_authoring.py --phase build` | 아래 "남은 위험"에 기록된 시점에 실행 | `VALIDATION_BUILD.json` |
| 참고 자료 저장소 무변경 | `git -C <검사기 저장소> status --porcelain` | 최종 보고 시점에 확인 | 최종 보고 |

## 남은 위험과 미확인

1. **`P-08` 외부 통제 미구현**: `om-plan` wiring 테스트가 아직 없다. 이 저작 범위 밖이며 `required_for_pass: false`로 기록했다. 검사기 저장소에서 추가되기 전까지는 "SKILL.md의 경계 문구가 지워져도 CI가 잡지 못하는" 상태다.
2. **모드별 필수 산출물의 근거 계층 차이**: `upgrade` 9종만 검사기가 강제하고 `initial`·`feature`·`change`의 산출물 목록은 설계 논의 근거다. 이후 검사기가 해당 게이트를 추가하면 표를 코드 근거로 승격해야 한다.
3. **[해소됨] `.gitlab-ci.yml`의 exit 2 → CI 성공 래핑**: 실측 완료. `harness/ci/om_plan_ci.py:324`가 `approval`을 CI 종료코드 0으로, 325행이 `success-review-ready`로 매핑한다. 본문에 기재했으므로 미확인 항목이 아니다.
4. **R-1·R-2(기준선 잠금)와 R-4(등록 밖 변경 커버리지 게이트)**: 검사기 쪽 미해결 항목이라 스킬이 메울 수 없다. `## 알려진 함정`의 "잘못된 `custom_baseline`으로도 `approval`이 나온다" 항목으로 사용자에게 노출했다.
5. **`python3` 인터프리터 선택**: `om-apply` SKILL.md는 `python`을 쓴다. 이식 시 검사기 저장소의 표기 통일 여부를 사람이 결정해야 한다.
6. **설치 버전 의존성 없음**: 사용한 frontmatter 5개 필드는 모두 기본 필드이며 확인한 설치 버전은 `2.1.241`이다. 버전 의존 필드를 쓰지 않아 하위 버전에서 무시될 필드가 없다.

## 4차 감사 전 수정 이력 (2026-08-25, 사람 승인 예외)

- **사람 결정**: 사용자가 2026-08-25 "고치고 한 번 더 검사받아"로 재감사 한도(2회) 예외를 승인했다. 수정 적용자는 1차 검토 세션(Claude)이며, 감사자는 아래 4차의 새 독립 인스턴스다(작성자·감사자 분리 유지).
- 차단 A: SKILL.md 7단계의 STATE_ROOT·SESSION_ID 출처를 훅 주입 환경변수(관측 불가)에서 `plan start` stdout JSON(`om_workflow.py:264-270` 실재)으로 교체. COMMAND_SPEC·DESIGN_REQUIREMENTS workflow[6] 동반 교체.
- 차단 B: `/om-resume`(미등록 명령 — 공식 문서상 파일 정의 없는 슬래시 명령은 훅 발화 전 Unknown command 거부) 의존을 제거하고, marker 재생성 방아쇠를 `/om-plan` 재호출(스킬 호출 시 `hook_cli.py:123-133` PreToolUse Skill 분기가 marker 생성)로 교체 + "새 run 시작 금지, 기존 RUN_DIR로 plan-resume" 명시. 검토결과서(docs/om-plan/검토결과_om-plan_1차_20260825.md) 근거.
- 비차단 #1: `$ARGUMENTS`→run-request 주체 충돌 해소(사람 준비 파일임을 명시). #3: `plan-validate` digest 생략 결과를 `analysis_error`(3)로 정확화(2곳 — CLI help "누락·형식 오류·불일치는 analysis_error" 근거). #7: RULE_COVERAGE P-08 사유의 83 작업3 오귀속 정정.
- 나머지 비차단 6건(#2·#4·#5·#6·#8·#9)은 Codex 2차 검토 단계로 이월.

## 4차 감사(PASS) 후 비차단 조치 (2026-08-25)

4차 감사 비차단 5건 중 감사자가 정리 권고한 3건 처리(SKILL.md 무변경):
- #1 설계서 §13 7단계·plan-validate 문구를 4차 검증본과 일치하게 정정(재저작 시 차단 B 재발 방지), source_documents sha256 갱신.
- #2 COMMAND_SPEC의 plan-validate 구 문구를 `analysis_error`(3)로 정밀화.
- #4 **남은 위험 추가**: 이식 후 실기동 스모크 테스트 필수 — 훅 필드명(`command_name` vs 공식 문서 `slash_command_name`) 불일치 가능성으로 UserPromptExpansion 우회 차단 분기가 no-op일 수 있음(검토결과서 근거). 스킬 재호출 marker 경로(PreToolUse)와 세션 간 재개(옛 session_id → SESSION_MARKER_INVALID 안전 실패)도 같은 테스트에서 확인.
- #3(세션 간 재개 한계 본문 명시)·#5(3차 이월 6건)는 Codex 단계로 이월.

## 실행기 전환·P0 반영 수정 (2026-08-25, 87 반영 — 확인 감사 대기)

- 근거: Codex P0 수정 결과(87, Claude 재검증 통과 — 276 테스트·반례 라이브 재현·훅 판정 5종 실측). 사람 결정(24): feature ID 사람 필수 기재 / 실행 래퍼 통일.
- 변경: 실행 명령을 표준 실행기 `harness/om`으로 교체(allowed-tools 패턴 포함). feature 입력 계약 반영(customization_id 필수·ID 형식·제안서 바꿔치기 block 사유) — 입력 표·모드 표. 앵커 동반 갱신, build exit 0.
