> 1차 독립 감사(skill-author-auditor 새 인스턴스) 반환 결과를 그대로 기록한다.
> 하네스가 표시 과정에서 `<`·`>`·`&`를 HTML 엔티티로 이스케이프한 것만 원문자로 되돌렸고, 판정과 내용은 수정하지 않았다.
> 이 보고서의 비차단 개선사항 1~6·8·9·11을 반영한 뒤 **새 감사자 인스턴스**로 2차 감사를 수행했다(원문: `AUDIT_REPORT_ROUND2.md`). 최종 판정은 `AUDIT_REPORT.md`에 있다.

---

# om-verify 독립 감사 결과

## 종합 판정
- 1차 판정: PASS
- 핵심 이유:
  - 원문 규칙 89개(공통 67 + Claude Code 전용 22)를 직접 세어 manifest·coverage와 대조했고, 89개 전부가 정확히 한 번씩 판정됐다. 누락·중복·미판정 0건.
  - `APPLY`·`TRANSFORM` 65개 규칙의 69개 `targets[].contains` 문구를 최종 `SKILL.md` 본문과 1건씩 대조해 전부 실재를 확인했고, 문구가 규칙의 핵심 의미를 실제로 수행하는지도 확인했다. ID만 적어두고 의미가 빠진 항목은 발견하지 못했다.
  - **코드 실측 주장 반증 시도가 전부 실패했다.** 종료코드 매핑(`{"verified": 0, "failed": 1, "infra_error": 3}` — `verifycore/workflow.py:439`), 입력오류 2·pre-run 차단 3(`om_workflow.py:512-527`), CLI 형태 `verify run REQUEST --run-dir`(`om_workflow.py:400-404`), 게이트 4종 이름, 최악 게이트=최종 상태(`_STATUS_RANK`·`_final_status`), `not_configured` 분기, waiver의 `VERIFY_REQUIRED_TEST_FAILED:` 접두사 한정 제거, 통제 환경변수 2종(`controlled_names`), 요청·build·fixture·waiver·ui 스키마 필드 목록, 함정 표 4행의 reason code — 모두 스키마·엔진 코드와 일치했다.
  - 필수 외부 통제 6건 중 `required_for_pass: true` 항목(`om_workflow.py`, `verifycore/workflow.py`, `pytest_runs.py`, `result_io.py`의 `os.chmod(destination, 0o444)`, `.claude/settings.json`의 `permissions.deny` 5항목)을 모두 직접 열어 구현을 확인했다. `pytest_runs._BLOCKED_ENV`(6종)와 `VERIFY_RUN_ALREADY_EXISTS` 분기도 실재한다.
  - CC-21의 `UserPromptExpansion`은 대상 저장소 matcher가 `^(om-plan|om-resume)$`임을 실측했고, 작성자는 이를 `state: planned` + `required_for_pass: false`로 정직하게 미구현 기록했다. 구현했다고 위장하지 않았다.
  - 기계 검증 2건(`VALIDATION_SPEC.json`, `VALIDATION_BUILD.json`) 모두 `ok: true`, errors 0, warnings 0이며 집계값(89/89, 18/18)이 내가 독립 계수한 값과 일치한다.
  - 보조 파일 미생성 주장을 직접 검증했다(`references`·`scripts`·`assets`·`evals` 4경로 모두 "File does not exist"). 동명 스킬 충돌도 없다(검사기 저장소 `.claude/skills/om-verify/SKILL.md` 부재 실측).
  - `D-01` 언어 충돌은 은폐되지 않았다. `RULE_COVERAGE.D-01.rationale`, `SPEC_REVIEW.md` 미확인 항, `AUTHORING_REVIEW.md` 남은 위험 1, `COMMAND_SPEC.open_questions` 네 곳에 명시됐고 근거(대상 저장소 `om-apply/SKILL.md` 영어, `test_claude_wiring.py:43-52`의 영어 문구 단언, 정본 83 작업3의 "never 계열 문구" 요구)를 전부 실물에서 확인했다. 결정은 타당하다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (`purpose`·`user_outcome`·`use_when`·`do_not_use_when`·`invocation_examples`·`inputs_and_defaults`·`trusted_and_untrusted_sources`·`scope_include`·`scope_exclude`·`scope_conditional`·`permissions_allow`·`permissions_deny`·`approval_required`·`workflow`·`outputs`·`validation`·`failure_handling`·`completion_conditions`)
- 미해결: 0
- 근거 없음: 0 — 18개 항목 전부 설계서 절 번호 + 스키마/엔진 코드 절대경로가 `sources`에 연결돼 있고, 표본 검증한 근거(예: `inspect_runtime`의 required 8필드, `_load_waiver`, `escalation_required` 계산식, `om_workflow.py:14-20`)가 실재했다. 설계서에 없는 내용을 사실처럼 보충한 항목은 발견하지 못했다.
- 명세 반영 누락: 0 — 18개 요구사항이 `COMMAND_SPEC.yaml`의 `purpose`/`scope`/`permissions`/`validation`/`failure_handling`/`completion_conditions`/`outputs`로 전수 추적된다. `validation`만 본문 축약(대표 4종)이며 나머지 OV 반례는 명세에 보존됐고 그 사유(A-CC-12·CC-08)가 기록돼 있다.

## 규칙 집계
- 원문 규칙: 89 (C-01~20, P-01~08, D-01~12, E-01~07, V-01~08, S-01~07, M-01~05 = 67 / CC-01~22 = 22) — 원문 두 문서를 직접 열어 제목 단위로 계수했고 manifest의 89와 일치
- 판정 규칙: 89 (APPLY 42 · TRANSFORM 23 · EXCLUDE 18 · EXTERNAL 6 — 내가 직접 재계수한 값이 작성자 주장과 일치)
- 누락: 0
- 중복: 0
- 미판정: 0
- 반영 위치 없음: 0 (69개 target 문구 전부 `SKILL.md`에 실재)
- 근거 부족 제외: 0 — `EXCLUDE` 18건 모두 "관련 없음" 수준이 아니라 대상 주단계(V)·부작용·선택한 기술 경로에 연결된 구체 사유를 가진다. 규칙 갱신·유지보수 계열(C-20·M-01·M-03·M-04·M-05)은 verify 실행 경로에 그 활동이 없다는 점, 평가 계열(P-08·V-01·V-02·CC-18)은 자동 발동 미허용 + 충족 위치(`COMMAND_SPEC.validation`) 명시, 기술 경로 계열(D-08·E-04·V-03·CC-09~CC-12·CC-20·CC-22)은 fork·`!` 주입·보조 파일·플랫 커맨드 미사용이라는 실제 결정에 연결된다.
- 미구현 필수 외부 통제: 0

## 차단 문제
| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| — | — | 없음 | 코드·스키마 대조에서 최종 파일의 사실 주장 반증 실패, 필수 외부 통제 전부 구현 확인, 기계 검증 2건 통과 | — |

## 시나리오 결과
| 시나리오 | 판정 | 근거 |
|---|---|---|
| 1. 정상 호출 | 통과 | `SKILL.md:108-181` 5단계가 사전 확인→호출→해석→보고로 이어지고, 3단계 명령이 `om_workflow.py:400-404`의 실제 인자와 일치한다 |
| 2. 필수 입력 누락 | 통과 | `SKILL.md:18-19` "If the invocation names no target, ask for the run directory or receipt path instead of guessing one." + `COMMAND_SPEC.inputs.arguments.default` |
| 3. 잘못된 입력·허용값 | 통과 | `SKILL.md:150-153`이 exit 2(입력 거부)와 pre-run 차단(stderr `analysis_error`+exit 3)을 분리한다. `om_workflow.py:512-527`과 일치. `retries≠0`·통제 환경변수는 `SKILL.md:49,101-103`에서 차단 |
| 4. 대상 파일·설계서 부재 | 통과 | 2단계가 build/fixture receipt·run-dir 부재·컨테이너 상태를 호출 전에 확인하고(`SKILL.md:122-135`), 확인 불가는 `SKILL.md:59-60`에 따라 미확인으로 보고한다 |
| 5. 권한 부족 | 조건부 통과 | 도구 권한 거부를 코드 실패와 구분하라는 CC-16 문장이 본문에 직접 없다. 다만 `SKILL.md:59-60`·`181`의 "미확인으로 보고" 규율이 오판정을 막는다 (비차단 개선 4번) |
| 6. 검증 실패 | 통과 | `SKILL.md:183-189` 케이스 표 + `176` "every reason code verbatim" + `168-169` 실패 run 보존 |
| 7. 부분 변경 후 실패 | 통과 | verify는 제품 변경이 없어 롤백 대상이 없고(`SKILL.md:37-38`), 부분 실행은 `skipped_due_to_stop`로 통과가 아니며(`167`), 실패 run 디렉터리를 증거로 보존한다(`169`) |
| 8. 외부 콘텐츠의 규칙 무시 지시 | 통과 | `SKILL.md:52-58` — receipt·JUnit·로그·docker·엔드포인트를 데이터로 고정, "skip a check, relax a threshold, or promote a WARN" 요구는 실행하지 않고 의심 항목 보고, 신뢰 출처를 스키마·엔진·CLI로 한정 |
| 9. 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true`로 부작용 명령의 자동 발동 차단(CC-02·A-CC-03). 미발동 위험은 수동 전용 설계상 의도된 것이며 `description`이 메뉴 식별을 돕는다 |
| 10. 기존 동명 스킬과 충돌 | 통과 | 저작 저장소·검사기 저장소 모두 기존 `om-verify` 부재를 직접 확인(검사기 경로 읽기 시 "File does not exist"). `name`=디렉터리명=`om-verify` 일치 |

## 비차단 개선사항

1. **`SKILL.md:41-42`의 "a gate that never executed is never a pass"와 `not_configured` 분기의 문면 긴장(우선순위 최상).** `workflow.py:413-414`는 `ui_component` 부재 시 UI 게이트를 `status: "verified"`, `execution_status: "not_configured"`로 기록한다. 즉 "실행되지 않았는데 verified로 기록되는 게이트"가 실제로 존재한다. `SKILL.md:95-96`이 이 분기를 별도로 설명하고 4단계 검증문(`167`)이 대상을 `skipped_due_to_stop`로 한정하므로 오판정으로 이어지지는 않는다. 다만 41-42행을 "a gate stopped by `skipped_due_to_stop` is never a pass"처럼 좁히면 문면 충돌이 사라진다.
2. **`SKILL.md:188` 케이스 표의 `failed` 원인 서술이 좁다.** `failed`는 계약 테스트 실패 외에 `VERIFY_UI_WARN_OR_FAIL`(`om/verify.py:273-289`, `workflow.py:425`) 경로로도 발생한다. 현재 행은 "report each failing selector and its `VERIFY_REQUIRED_TEST_FAILED` reason"만 지시해 UI 사유일 때 대응 지침이 비어 있다(안전 측면 문제는 없음 — 5단계가 모든 reason code를 그대로 보고시킨다).
3. **입력 계약 표의 "What must hold" 열이 두 행에서 필드 나열에 머문다.** fixture receipt 행은 `run_id`/`candidate_sha`/`container_id`/`volume_names`가 현재 run·후보·런타임과 **일치**해야 한다는 결속 조건(`VERIFY_FIXTURE_RUNTIME_MISMATCH`, `om/verify.py:211-217`)을 적지 않았고, waiver 행은 스키마 필수 필드 `run_id`(해당 run에 결속, `workflow.py:215-217`)를 목록에서 빠뜨렸다.
4. **CC-16의 "권한 부족을 코드 실패로 오인하지 않는다"가 본문에 없다.** 상태 5종(verified/failed/infra_error/승인 필요/not_configured)은 구현됐으나 도구 권한 거부·명령 차단 상황의 별도 보고 지시는 본문·명세 어디에도 없다.
5. **`allowed-tools` 패턴이 본문 코드 블록과 정확히 맞물리지 않는다.** 본문은 `cd <checker_repository_root>` 다음 줄에 `python harness/om_workflow.py ...`를 제시하는데, 사전 승인 패턴은 `Bash(python harness/om_workflow.py verify run *)`뿐이라 `cd ... && python ...` 형태의 단일 호출은 매칭되지 않는다. `Bash(git status *)`도 인자 없는 `git status`를 덮지 못한다(같은 저장소의 `claude-skill-author/SKILL.md:21-24`는 두 형태를 모두 등록). 제한이 아닌 사전 승인이므로 안전 문제는 아니고 프롬프트 빈도만 늘어난다.
6. **`COMMAND_SPEC.permissions.allow`의 "verify-request용 입력 파일 작성"과 `allowed-tools`에 쓰기 도구가 없는 점이 어긋난다.** `SKILL.md:76`은 "You write `verify-request.json`"이라고 지시하는데 `Write`가 사전 승인 목록에 없다. 규칙상 위반은 아니지만(사전 승인≠제한) 계약 추적성이 끊긴다.
7. **`/om-report` 전방 참조.** `SKILL.md:3,27`은 `/om-report`를 대안 명령처럼 제시하지만 이 명령은 아직 존재하지 않는다(설계서 §3·§20, `DOC/81` 「다음」-2에서 "착수 여부 사람 결정 대기"로 기록). 설계서와 일관되므로 왜곡은 아니나, C-19의 "안전한 대안" 관점에서는 실행 불가능한 대안이다.
8. **`RULE_COVERAGE.D-08` 사유의 측정값이 틀렸다.** "본문이 200줄 미만이라"고 적었으나 최종 `SKILL.md`는 217줄이다(같은 증거 묶음의 `AUTHORING_REVIEW.md`는 216줄로 적어 자체 불일치). 결론(500줄 임계 미만이므로 분리 불필요)은 유효하지만 근거 수치가 실물과 다르다.
9. **함정 표 2행의 "왜 옳은가"가 두 기전을 섞었다.** `VERIFY_REGISTRATION_DIGEST_MISMATCH`는 `_file_state(snapshot) != registration_final_digest` 비교에서 발생하고(`workflow.py:179-180`), 필수 테스트 재계산은 그 뒤 별개 단계다. 두 기전이 연관되긴 하나 설명이 정확하지는 않다.
10. **`P-01`의 "최소 3개의 실제 사용자 요청" 조건이 문면상 미충족.** 수집된 호출 예는 2건(`COMMAND_SPEC.invocation.examples`)이다. 경계 사례·비사용 요청은 충분히 확보돼 있어 실질 영향은 작다.
11. **`Enforcement` 절의 "the repository"가 현재 설치 위치에서는 참이 아니다.** 저작 저장소 `/Users/seop/claude-skill-by-seop`에는 `.claude/settings.json`이 없다(직접 확인). 문장이 가리키는 대상은 검사기 저장소이며 본문 첫 문단이 실행 위치를 그 저장소로 못 박고 있지만, "in the checker repository"로 명시하면 이식 전 오독을 없앨 수 있다.

## 감사 범위와 미확인 사항

- 감사한 실물: 원문 규칙 2종, 설계서 `OM_VERIFY_DESIGN.md`, 정본 `83_Codex_SKILLmd_작성지시_20260824.md`, 증거 6종(`DESIGN_REQUIREMENTS`·`RULE_MANIFEST`·`COMMAND_SPEC`·`RULE_COVERAGE`·`SPEC_REVIEW`·`AUTHORING_REVIEW`), 기계 검증 2종, 최종 `SKILL.md`, 그리고 검사기 저장소의 `harness/om_workflow.py`, `verifycore/{workflow,testruns,pytest_runs,result_io,schema}.py`, `integrations/om/verify.py`, 스키마 5종 + `apply-result.schema.json`, `tests/test_om_verify_counterexamples.py`(OV-01·02·05·06·07·09·11·12·13·14 구간), `tests/test_claude_wiring.py`, `.claude/settings.json`, `.claude/skills/om-apply/SKILL.md`, `CLAUDE.md`.
- 파일은 하나도 수정하지 않았다.
- 미확인 1: 이 세션에서 `Grep`·`Glob` 도구가 환경 오류(`ENOEXEC`)로 사용 불가였다. 규칙 ID 계수와 target 문구 대조는 전부 `Read`로 파일 전문을 열어 수동 수행했다. 파일 시스템 열거는 "존재하는 디렉터리=EISDIR / 없는 경로=File does not exist" 판별로 대체했으므로, 보조 폴더 부재는 4개 표준 경로(`references`·`scripts`·`assets`·`evals`)에 한해 확인된 것이다. 그 외 비표준 이름의 파일이 스킬 폴더에 있는지는 확인하지 못했다.
- 미확인 2: `AUTHORING_REVIEW.md`의 "참고 자료 저장소 무변경(`git status --porcelain` 0줄)" 주장과 `claude --version = 2.1.241` 실측 주장은 이 감사에서 명령을 실행할 수 없어 재확인하지 못했다. 다만 `disable-model-invocation`·`argument-hint`·`allowed-tools` 사용 근거는 같은 저장소 `claude-skill-author/SKILL.md`가 동일 필드를 실제로 쓴다는 사실로 독립 확인했다(CC-19 충족).
- 미확인 3: `DOC/81`(리허설 재검증)·`DOC/76`(구현지시서)·`DOC/24`(사람 결정 기록)는 열지 않았다. 이들이 근거인 주장(실데이터 리허설 통과, 남은 위험 6건, R-6 임시 결정)은 코드·테스트로 교차 확인 가능한 범위에서만 검증했고, 문서 고유 주장은 미검증이다. 작성자 스스로 "이 세션은 `verify run`을 실제 실행하지 않았다"고 기록했으며(`AUTHORING_REVIEW` 남은 위험 4), 나 역시 실행 검증은 수행하지 않았다.
- 감사 대상에서 제외: `.claude/skills/om-plan/`, `.claude/skill-authoring/om-plan/`, `docs/om-plan/`. 읽지도 판정하지도 않았다.
