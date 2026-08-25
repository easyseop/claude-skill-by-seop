> 최종(4차) 독립 감사 — `skill-author-auditor` 새 인스턴스가 반환한 결과를 그대로 기록한다.
> 하네스가 표시 과정에서 `<`·`>`·`&`를 HTML 엔티티로 이스케이프한 것만 원문자로 되돌렸고, 판정과 내용은 수정하지 않았다.
> 회차별 원문: 1차 `AUDIT_REPORT_ROUND1.md`(PASS) · 2차 `AUDIT_REPORT_ROUND2.md`(PASS) · 3차 `AUDIT_REPORT_ROUND3.md`(CONDITIONAL) · 4차 이 문서(PASS).
> **이 문서는 영어 본문(225줄)에 대한 감사다.** 사람 결정(2026-08-25)으로 본문을 한글화한 뒤 5차 감사(`AUDIT_REPORT_ROUND5.md`, CONDITIONAL)와 6차 확인 감사(`AUDIT_REPORT.md`, PASS)를 새로 수행했다.

---

I have completed the independent verification. Findings below.

# om-verify 독립 감사 결과 (4차·최종 확인)

## 종합 판정
- 판정: PASS
- 핵심 이유:
  - **3차 차단 문제가 실제로 해소됐다.** `AUDIT_REPORT_ROUND2.md`(79줄)에 2차 감사 반환 원문이 판정·차단표·시나리오표·비차단 12건까지 그대로 보존돼 있고, `AUDIT_REPORT_ROUND1.md:3`의 인용이 `AUDIT_REPORT_ROUND2.md`로 정정돼 실제 파일과 일치한다. 인용 경로 불일치는 남아 있지 않다.
  - **줄 번호 주장 반증에 실패했다.** `AUTHORING_REVIEW.md`의 `SKILL.md:N` 표기 30개 이상을 실물과 1건씩 대조했다(C-09→147, D-05→173, V-04→174, E-03→175, E-05→181, S-02→76, CC-06→79, C-18→58, CC-16→191·102·67, CC-04→4·148, 문장별 표의 42·44-46·47·49·51·54·55·57·61·64·66·68·69-72·74-79·81-113·115-189·157-161·191-197·199-209·211-213). 전수 표본에서 어긋난 항목을 찾지 못했다. 3차 지적 1번은 구조적으로 해소됐다.
  - **`allowed-tools` 9항목 표기가 실물과 일치한다.** frontmatter 7~15행이 `Read`·`Glob`·`Grep`·`Write` + Bash 패턴 5개 = 9항목이다. `Edit`·`Bash(*)` 부재도 확인했다.
  - **3차가 지목한 `SKILL.md` 3건 수정이 코드와 일치한다.** (a) `workflow.py:250-252`가 `run.exists()` 검사를 `run.mkdir` **앞에서** 수행하므로 "before this run's directory is created"는 정확하다. (b) `om/verify.py:273-274`가 `actual_exit != 0`를 `VERIFY_UI_WARN_OR_FAIL`로 올리고 `workflow.py:425`가 그 코드만 `failed`로 매핑하므로 케이스 표 `failed` 행의 "exited non-zero"는 정확하다. (c) `workflow.py:295-296`의 `VERIFY_BUILD_DIST_DIGEST_MISSING`이 실재하므로 입력 계약 build receipt 행의 `dist_digest` 요구는 정확하다.
  - **엔진 잔여 위험이 정직하게 기록됐다.** `gitprim.GitPrimitiveError`는 `RuntimeError`(`gitprim.py:29`)이므로 `run_verify`의 `(PlanControlError, OSError, KeyError, TypeError, ValueError)` 절에도 `main`의 세 예외 절에도 걸리지 않는다. 실측으로 재현 확인했고 `AUTHORING_REVIEW` 남은 위험 4에 "스킬 문서 결함 아님 + 검사기 후속 검토"로 적혀 있다. 구현 위장이 없다.
  - **exit 2/3 서술에 회귀가 없다.** `read_data`(`plancore/schema.py:55-73`)·`_validate_request`·`VERIFY_RUN_ALREADY_EXISTS`가 모두 `PlanControlError` → `main`의 `analysis_error` + exit 3이고, exit 2는 argparse·`WorkflowInputError`·Python 3.11 미만(`om_workflow.py:14-20`)이다. `binding.pin`은 `check=False` + `BindingError(ValueError)`, `gitprim.git`은 `CalledProcessError`를 `GitPrimitiveError`로 감싸므로 verify 경로에서 `CalledProcessError→2`는 도달하지 않는다. 문장은 코드와 일치한다.
  - 완료 정의(`SKILL.md:34-36`)도 회귀가 없다. `not_configured` 게이트는 `status: verified`(`workflow.py:414`)이고 "stopped with `skipped_due_to_stop`"에 해당하지 않아 정상 run을 완료에서 배제하지 않는다.
  - 필수 외부 통제 전부 실물 확인, 기계 검증 2건 `ok: true`·errors 0·warnings 0이며 집계가 내 독립 계수와 일치한다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (전부 `RESOLVED`, `value`/`items` 비어 있지 않음. 설계서 `OM_VERIFY_DESIGN.md` 20개 절 전문과 대조해 왜곡·과장 없음을 확인했다. 표본 재실측: `inspect_runtime` required 8필드, `_load_waiver` 6필드·만료 검사, `escalation_required = infra_error and prior+1>=3`, `expected_exit_code` 매핑, `_BLOCKED_ENV` 6종, `controlled_names` 2종)
- 미해결: 0
- 근거 없음: 0 (3번째 호출 예는 설계서 §4에 파생 근거 문장과 함께 실재하며 합성 예시임이 남은 위험 7에 공개돼 있다)
- 명세 반영 누락: 0 (18개 전부 `COMMAND_SPEC`의 purpose·scope·permissions·execution·outputs·validation·failure_handling·completion_conditions로 추적된다. 2차 지적 6번의 "권한 중단" 상태도 `failure_handling.states`와 `DESIGN_REQUIREMENTS.failure_handling`에 반영돼 본문 전용 상태가 사라졌다)

## 규칙 집계
- 원문 규칙: 89 (원문 2종을 직접 열어 제목 단위 계수: C 20 · P 8 · D 12 · E 7 · V 8 · S 7 · M 5 = 67, CC-01~22 = 22)
- 판정 규칙: 89 (APPLY 42 · TRANSFORM 23 · EXCLUDE 18 · EXTERNAL 6 — 재계수 일치)
- 누락: 0
- 중복: 0
- 미판정: 0 (안티패턴 26건도 전수 판정: PASS 21 · NOT_APPLICABLE 5(A-CC-05·06·07·08·14), 사유 모두 구체적)
- 반영 위치 없음: 0 (`APPLY`·`TRANSFORM` 65건의 70개 `contains` 문구를 `SKILL.md` 225줄과 1건씩 대조해 전부 실재 확인. ID만 적고 의미가 빠진 항목 없음 — 예: C-16은 단계별 Verify 문장, S-06은 인젝션 대응 행동, CC-16은 3상태 + 권한 중단 분리로 실질 구현됨)
- 근거 부족 제외: 0 (EXCLUDE 18건은 규칙 갱신 활동 부재 5건 / 저작 단계 충족 4건 / 미선택 기술 경로 9건으로 모두 주단계 V·부작용 등급·선택 경로에 연결)
- 미구현 필수 외부 통제: 0 (`required_for_pass: true` 5경로 직접 확인: `om_workflow.py`, `verifycore/workflow.py`, `pytest_runs.py`, `result_io.py`의 `os.chmod(destination, 0o444)`, `.claude/settings.json`의 deny 7항목. CC-21의 `UserPromptExpansion`은 matcher가 `^(om-plan|om-resume)$`임을 실측했고 `planned` + `required_for_pass: false`로 정직 기록)

## 차단 문제
| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| — | — | 없음 | 3차 차단(2차 원문 미보존) 해소 확인, 3차 비차단 8건 실물 반영 확인, 코드 대조에서 사실 주장 반증 실패, 필수 외부 통제 5경로 실재, 기계 검증 2건 통과, 89/89 판정·70 target 실재 | — |

## 시나리오 결과
| 시나리오 | 판정 | 근거 |
|---|---|---|
| 1. 정상 호출 | 통과 | 5단계 절차(115-189행)가 사전확인→호출→해석→보고로 이어지고 152행 명령이 `om_workflow.py:400-404`의 실제 인자와 일치 |
| 2. 필수 입력 누락 | 통과 | 21-22행 "If the invocation names no target, ask for the run directory or receipt path instead of guessing one." + `COMMAND_SPEC.inputs.arguments.default` |
| 3. 잘못된 입력·허용값 | 통과 | 157-161행의 exit 0/1/2/3 서술이 `om_workflow.py:509-527`·`workflow.py:439`와 일치(2차·3차 정정이 유지됨). retries≠0(54행)·통제 환경변수(108-110행)도 코드와 일치 |
| 4. 대상 파일·설계서 부재 | 통과 | 2단계(129-142행)가 부작용 전에 build/fixture receipt·run-dir 부재·컨테이너 상태를 확인하고, 요청 파일 부재는 `INPUT_UNREADABLE` → analysis_error + exit 3으로 귀결 |
| 5. 권한 부족 | 통과 | 66-67행이 도구 거부·명령 차단을 테스트 실패와 분리하고 거부 명령을 지목하게 하며, `COMMAND_SPEC.failure_handling.states`에 "권한 중단"이 명세로도 존재 |
| 6. 검증 실패 | 통과 | 케이스 표 3행 + 184행 "every reason code verbatim" + 176-177행 실패 run 보존. `testruns.evaluate`의 `VERIFY_REQUIRED_TEST_FAILED`/`NOT_PASS` 분기와 정합 |
| 7. 부분 변경 후 실패 | 통과 | verify는 제품 변경이 없어 롤백 대상 없음(42행), 부분 실행은 `skipped_due_to_stop`(174-175행)으로 통과 아님, 실패 run 보존. `workflow.py`의 세 skip 분기와 일치 |
| 8. 외부 콘텐츠의 규칙 무시 지시 | 통과 | 57-63행이 receipt·JUnit·로그·docker·엔드포인트를 데이터로 고정하고 "skip a check, relax a threshold, or promote a WARN" 요구를 의심 항목 보고로 처리, 신뢰 출처를 스키마·엔진·CLI로 한정 |
| 9. 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true`(부작용 명령, CC-02·A-CC-03). description이 결과·부작용·비적용을 함께 제공해 메뉴 식별 가능 |
| 10. 기존 동명 스킬과 충돌 | 통과 | `CHK/.claude/skills/om-verify/SKILL.md`·저작 저장소 `.claude/commands/om-verify.md` 모두 "File does not exist" 실측. `name`=디렉터리명=`om-verify` |

## 비차단 개선사항

1. **`AUTHORING_REVIEW.md:200`이 아직 사실이 아닌 문장을 과거형으로 쓰고 있다(최우선).** "원문은 각각 `AUDIT_REPORT_ROUND1.md`, `AUDIT_REPORT_ROUND2.md`, `AUDIT_REPORT.md`에 그대로 보존했다"라고 적혀 있으나 `AUDIT_REPORT.md`는 현재도 rubric 템플릿(35줄, 값 미기입)이다. 이번 회차 지시에 따라 차단으로 올리지 않았지만, **이것은 3차가 차단한 것과 동일한 유형의 주장이다.** 3차·4차 원문을 실제로 기록하기 전까지 이 문장은 검증 불가 주장으로 남는다. 마감 시 3차 원문과 이번 결과를 실제로 파일에 남기고 200행의 파일 목록을 실물에 맞출 것.
2. **`COMMAND_SPEC` 안에서 3차 지적 4번이 절반만 반영됐다.** `completion_conditions[3]`(262행)에는 "승인된 waiver로 면제된 selector를 제외한"이 들어갔으나, 같은 파일 `validation.completion_assertions[3]`(220행)은 여전히 "모든 outcome이 pass이며"로 남아 있다. `workflow.py:381-389`는 waiver가 사유만 지우고 `attempt.outcome`은 `fail`로 남기므로, 두 문장 중 220행이 코드와 어긋난다. 보수적 방향의 오차라 거짓 verified를 만들지 않으나 정정이 필요하다.
3. **설계서 §17-4는 아직 waiver 조건이 없다.** `DESIGN_REQUIREMENTS.completion_conditions[3]`에 추가된 waiver 예외의 `sources`는 설계서 §17만 가리키는데, 정작 §17-4(301행)에는 "모든 `outcome`이 `pass`"만 있다. 실제 근거는 설계서 §9(waiver 조건부)와 `workflow.py:381-389`다. 근거 경로를 §9 + 코드로 보강하거나 설계서 §17을 함께 정정할 것.
4. **`AUTHORING_REVIEW.md:190`의 줄 표기 `SKILL.md:151-11`이 형식 오류다.** CLI 코드 블록은 150-153행이고 `11`은 frontmatter의 `Bash(python harness/om_workflow.py verify run *)` 행이다. 다른 모든 표기가 정확해진 만큼 이 한 항목만 남았다. `150-153 · 11`처럼 분리 표기할 것.
5. **`Write` 경로 무제한은 여전히 남은 위험이다.** 실제 필요는 요청 파일 1건 작성인데 사전 승인 범위가 전 경로다. `COMMAND_SPEC.permissions.allowed_tools_policy`에 사유와 재검토 약속이 기록돼 은폐는 아니다(S-03 최소권한 관점의 잔여 항목).
6. **`retries`가 입력 계약의 선택 필드 목록(96-98행)에 없다.** 스키마에는 `"retries": {"const": 0}`이 존재하고 본문은 경계(54행)에서만 다룬다. 의도된 축약으로 보이나, 요청 파일을 쓰는 사람이 스키마를 볼 때 혼동할 수 있다. 한 단어 추가로 해소 가능하다.
7. **기계 검증 재실행 시점은 타임스탬프로만 확인된다.** `VALIDATION_BUILD.json`의 `validated_at`이 `VALIDATION_SPEC.json`보다 늦어 3차 지적 9번의 재실행 주장과 모순되지 않지만, 셸이 없어 `SKILL.md` 최종 수정 시각과의 선후는 독립 확인하지 못했다.

## 감사 범위와 미확인 사항

- 감사한 실물: `audit-rubric.md`, 원문 규칙 2종 전문(계수용 전 구간), 설계서 `OM_VERIFY_DESIGN.md` 전문, 저작 지시서 전문, `DESIGN_REQUIREMENTS.yaml`·`RULE_MANIFEST.yaml`(헤더·ID 구간)·`COMMAND_SPEC.yaml`·`RULE_COVERAGE.yaml`·`SPEC_REVIEW.md`·`AUTHORING_REVIEW.md`·`AUDIT_REPORT_ROUND1.md`(도입부)·`AUDIT_REPORT_ROUND2.md` 전문·`AUDIT_REPORT.md`·`VALIDATION_SPEC.json`·`VALIDATION_BUILD.json`, 최종 `SKILL.md` 전문(225줄), 그리고 검사기 저장소의 `harness/om_workflow.py`(1-45, 380-532), `verifycore/{workflow,testruns,result_io,schema}.py` 전문, `verifycore/pytest_runs.py`(1-80), `integrations/om/verify.py` 전문, `acgh/gitprim.py` 전문, `acgh/binding.py` 전문, `plancore/schema.py` 전문, `plancore/paths.py`(1-60), `verifycore/schema/verify-request.schema.json`·`verify-ui-component.schema.json`, `applycore/schema/apply-result.schema.json`, `tests/test_claude_wiring.py`, `.claude/settings.json`, `.claude/hooks/run_om_plan_hook.sh`, `CLAUDE.md`.
- 파일은 하나도 수정하지 않았다.
- 미확인 1: 이 세션에서도 `Grep`·`Glob`이 `ENOEXEC`로 실패해 모든 계수·대조를 `Read` 전문 읽기로 수동 수행했다. 파일 열거가 불가능해 보조 파일 부재(`references`·`scripts`·`assets`·`evals`)는 1·2차 감사자의 확인에 의존했고 이번 회차에서 독립 재확인하지 못했다.
- 미확인 2: 셸 실행 권한이 없어 설계서 3건의 sha256 재계산, `claude --version` = 2.1.241, 참고 저장소 `git status --porcelain` 0줄, `verify run` 실제 실행을 재확인하지 못했다. 버전 의존 필드 사용 근거는 같은 저장소 `claude-skill-author/SKILL.md`가 동일 필드를 쓴다는 사실로만 간접 확인했다.
- 미확인 3: `DOC/83`·`DOC/76`·`DOC/81`·`DOC/24`는 열지 않았다(경로가 이번 감사 대상 목록 밖). 이들에 근거한 주장은 코드·스키마·설계서·CLAUDE.md로 교차 확인 가능한 범위에서만 검증했다.
- 미확인 4: `harness/tests/test_om_verify_counterexamples.py`의 OV 반례 줄 번호는 이번 회차에서 재확인하지 않았다. 대신 각 reason code를 엔진 원본에서 직접 확인했다.
- 미확인 5: 실행 검증은 하지 않았다. 1·2·3차 감사자와 작성자 모두 실행하지 않았고, 실행 근거는 리허설 문서 81의 실측치다.
- 감사 대상에서 제외: `.claude/skills/om-plan/`, `.claude/skill-authoring/om-plan/`, `docs/om-plan/` — 읽지도 판정하지도 않았다.
