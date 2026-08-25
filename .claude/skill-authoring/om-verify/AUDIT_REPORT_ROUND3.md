> 3차 독립 감사(skill-author-auditor 새 인스턴스) 반환 결과를 그대로 기록한다.
> 하네스가 표시 과정에서 `<`·`>`·`&`를 HTML 엔티티로 이스케이프한 것만 원문자로 되돌렸고, 판정과 내용은 수정하지 않았다.
> 이 회차는 유일하게 차단 문제를 냈다(2차 감사 원문 미보존). 차단 1건 + 비차단 8건을 반영한 뒤 **새 감사자 인스턴스**로 4차 감사를 수행했다. 최종 판정은 `AUDIT_REPORT.md`에 있다.

---

# om-verify 독립 감사 결과 (3차·최종)

## 종합 판정
- 3차 판정: CONDITIONAL
- 핵심 이유:
  - 최종 `SKILL.md`(225줄) 자체에서는 차단 결함을 찾지 못했다. 이번 회차에 지목된 반증 대상 8건(완료 정의·exit 2/3 서술·fixture 대조 필드·`/om-report` 부재·권한 중단 역추적·SPEC_REVIEW 정합·줄 수·CC-16/D-08/S-03 사유)을 코드·스키마·설정 원본과 1건씩 대조했고 **전부 실물과 일치**했다. 반증 시도는 모두 실패했다.
  - 규칙 89개 전수 판정(누락·중복·미판정 0), `APPLY`·`TRANSFORM` 65건의 target 70개 전부 `SKILL.md`에 실재, 안티패턴 26건 전수 판정, 필수 `EXTERNAL` 통제 5경로 전부 실측 구현 확인, 기계 검증 2건 `ok: true`.
  - 그러나 **증거 묶음에 검증 불가한 인용이 남아 있다**. `AUTHORING_REVIEW.md:224`와 `AUDIT_REPORT_ROUND1.md:3`이 2차 감사 판정의 소재지로 `AUDIT_REPORT.md`를 지목하지만, 그 파일은 **빈 rubric 템플릿**(`- 판정: PASS | CONDITIONAL | FAIL` 그대로)이고 폴더 어디에도 2차 기록이 없다. 감사 원칙 1·5(주장을 사실로 간주하지 않는다 / 실행하지 않은 검사를 통과로 인정하지 않는다)에 따라 이 상태로는 `PASS`를 쓸 수 없다. 수정 범위는 문서 1건이며 `SKILL.md` 변경은 필요 없다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (`DESIGN_REQUIREMENTS.status: APPROVED`, 전 항목 `RESOLVED`·비어 있지 않음)
- 미해결: 0
- 근거 없음: 0 — 표본 재확인한 근거가 모두 실재했다. `verify-request.schema.json` required 4필드, `inspect_runtime` required 8필드, `verify-fixture-receipt.schema.json` 6필드, `_load_waiver` 6필드, `escalation_required = status=="infra_error" and prior+1>=3`, `om_workflow.py:14-20`(Python 3.11 게이트), `.claude/settings.json` deny 5항목, `test_om_verify_counterexamples.py:158·430·435`(행 번호까지 일치), `CLAUDE.md`의 "may hand off only `static_consistent_awaiting_verify` to `/om-verify`".
- 명세 반영 누락: 0 — 18항이 `COMMAND_SPEC`의 purpose/scope/permissions/execution/outputs/validation/failure_handling/completion_conditions로 전수 추적된다. 2차 신설 항목인 **권한 중단**도 `DESIGN_REQUIREMENTS.failure_handling` → `COMMAND_SPEC.failure_handling.non_retryable`·`states` → `SKILL.md:66-67`로 완전 역추적된다.
- `validation`만 본문 축약(대표 거부 4종)이며 사유(A-CC-12·CC-08)가 기록돼 있다.

## 규칙 집계
- 원문 규칙: 89 — 두 원문 문서를 직접 열어 제목 단위로 계수했다. manifest 89와 정확히 일치하고 ID·제목·행 범위도 원문과 일치한다. 안티패턴 26, stage_modules 9도 일치.
- 판정 규칙: 89 (APPLY 42 · TRANSFORM 23 · EXCLUDE 18 · EXTERNAL 6 — 독립 재계수 일치)
- 누락: 0 / 중복: 0 / 미판정: 0
- 반영 위치 없음: 0 — 70개 `targets[].contains`를 `SKILL.md` 전문과 1건씩 대조해 전부 실재를 확인했고, 문구가 규칙의 실질 의미를 실제로 수행한다.
- 근거 부족 제외: 0 — `EXCLUDE` 18건은 (1) 규칙 갱신·유지보수 계열, (2) 저작 단계에서 충족한 평가 계열, (3) 선택하지 않은 기술 경로로, 모두 주단계 V·부작용 등급·실제 설계 결정에 연결된다.
- 미구현 필수 외부 통제: 0 — `required_for_pass: true` 5경로를 직접 열어 확인했다. CC-21의 `UserPromptExpansion`은 matcher가 `^(om-plan|om-resume)$`임을 실측했고 `planned`·`required_for_pass: false`로 정직하게 기록돼 있다.

## 차단 문제
| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| 중 | `AUTHORING_REVIEW.md:224`, `AUDIT_REPORT_ROUND1.md:3` (감사 원칙 1·5) | 2차 독립 감사 판정("PASS, 차단 0건, 비차단 12건")의 소재지로 `AUDIT_REPORT.md`를 인용하지만 그 파일은 빈 rubric 템플릿이다. `AUDIT_REPORT_ROUND2.md`도 없다. 증거 묶음만으로는 2차 감사 수행·판정을 확인할 수 없다 | `AUDIT_REPORT.md` 전문 35줄이 rubric 원본 템플릿과 동일. 1차는 원문이 보존돼 대조 가능하나 2차는 대응 파일이 없음 | 2차 감사 반환 원문을 1차와 같은 방식으로 기록하고 두 인용 경로를 실제 파일에 맞춘다. 기록할 원문이 남아 있지 않으면 "2차 감사 원문 미보존, 요약만 존재"로 문구를 낮춰 적는다. `SKILL.md` 수정은 불필요 |

## 시나리오 결과
| 시나리오 | 판정 | 근거 |
|---|---|---|
| 1. 정상 호출 | 통과 | `SKILL.md:115-189` 5단계. 3단계 명령이 `om_workflow.py:395-404`의 실제 인자와 일치 |
| 2. 필수 입력 누락 | 통과 | `SKILL.md:21-22` + `COMMAND_SPEC.inputs.arguments.default` |
| 3. 잘못된 입력·허용값 | 통과 | `SKILL.md:157-161`이 exit 2(argparse·Python<3.11)와 pre-run 차단(stderr `analysis_error` + exit 3)을 분리한다. `read_data`→`PlanControlError(INPUT_UNREADABLE)`, `_validate_request`, `run.exists()`가 모두 `main`에서 3으로 매핑됨을 확인. verify 경로에서 exit 2를 낼 다른 경로는 도달 불가 |
| 4. 대상 파일·설계서 부재 | 통과 | 2단계(`SKILL.md:129-142`)가 호출 전에 확인하고, 확인 불가는 미확인 보고 |
| 5. 권한 부족 | 통과 | `SKILL.md:66-67` 권한 중단 문장(1차 지적 4번 해소) |
| 6. 검증 실패 | 통과 | 케이스 표 + 모든 reason code 축자 보고 + 실패 run 보존 |
| 7. 부분 변경 후 실패 | 통과 | 제품 변경 없음, `skipped_due_to_stop`은 통과 불가, 실패 run 보존. 엔진 3분기와 `_final_status`가 강제 |
| 8. 외부 콘텐츠의 규칙 무시 지시 | 통과 | `SKILL.md:57-63` 데이터 고정·의심 항목 보고·신뢰 출처 한정·endpoint 보조 교차확인 |
| 9. 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true` |
| 10. 기존 동명 스킬과 충돌 | 통과 | 양 저장소 `om-verify` 부재 실측. `/om-report`도 양쪽 부재이므로 `SKILL.md:30`의 "not yet available"은 사실 |

### 이번 회차 반증 대상별 결과
1. **완료 정의(34-36)** — 완화 아님. `_final_status`가 게이트 status의 최댓값이고 `skipped_due_to_stop` 게이트는 항상 `status: infra_error`이므로 `status == verified`는 `failed`·`infra_error`·`skipped_due_to_stop` 조합을 논리적으로 배제한다. `not_configured`만 `status: verified`로 남는데 이는 101-103에 별도 고지돼 있고 44-46·174-175와 모순되지 않는다.
2. **exit 2/3 서술(157-161)** — 코드와 정확히 일치. 다만 "before the run directory exists" 표현은 비차단 5번 참조.
3. **입력 계약 fixture 행(91)** — `inspect_runtime`이 대조하는 fixture payload 필드는 정확히 4개이고 `fixture_set_digest`는 기록만, `applied_at`은 전혀 사용되지 않는다. 요청의 `fixture_digest`와 혼동하지 않고 "running server" 행에 별도 배치했다. 정확.
4. **`/om-report, not yet available`** — 양 저장소 부재 실측, 사실.
5. **권한 중단 역추적** — 3단 전부 존재, 완결.
6. **SPEC_REVIEW allowed-tools 서술(39행)** — 최종 frontmatter와 일치. 2차 지적 2번 해소됨.
7. **줄 수** — 실측 225줄로 통일됨. 2차 지적 3번 해소됨.
8. **CC-16·D-08·S-03 사유** — D-08·S-03은 과장 없음. CC-16만 경미한 과장(비차단 3번).
9. **설계서 sha256 3건** — 셸 실행 수단이 없어 **미확인**.
10. **미반영 2건** — 10번(3번째 호출 예 합성)은 설계서 §4가 파생 근거를 명시하므로 은폐 아님. 12번(`cd && python` 미승인)은 CC-06 사실에 부합하며 남은 위험으로 고지돼 은폐 아님. 두 건 모두 사유 타당.

## 비차단 개선사항

1. **`AUTHORING_REVIEW.md`의 줄 번호가 여러 곳에서 현재 파일과 어긋난다.** 「독립 감사 반영」·「2차 독립 감사 반영」 표와 「설계 요구사항 추적」·「문장별 최종 검토」의 여러 항목이 마지막 편집 이전 기준이다. 규칙 문서가 "최종 파일 수정 후 문장별 검토를 다시 실행한다"고 요구하므로 일괄 재계산이 필요하다.
2. **`allowed-tools` 항목 수 표기 오류.** "6항목"·"6+4 목록"이라고 적었으나 실제 frontmatter 항목은 9개다. 1·2차가 반복 지적한 계수 오류와 같은 계열이므로 함께 정정할 것.
3. **`RULE_COVERAGE.CC-16` 사유가 아직 한 뼘 넓다.** "승인 필요(escalation_required)를 케이스 표에서 별도 상태로 두고"라고 적었으나 케이스 표는 3행이고 escalation은 `infra_error` 행 안의 조건절이다.
4. **`COMMAND_SPEC` 내부 긴장 1건.** `completion_conditions` 4번은 "모든 `outcome`이 `pass`"를 요구하지만 `scope.conditional`의 waiver 분기는 실패한 selector가 있어도 `verified`가 되는 경로를 허용한다. 명세 문장을 "waiver가 없는 경우"로 조건화하면 모순이 사라진다.
5. **`SKILL.md:159-160` 문면.** "every stop that happens before the run directory exists, such as `VERIFY_RUN_ALREADY_EXISTS`"는 그 코드가 디렉터리가 **이미 존재**해서 나는 것이므로 자기모순처럼 읽힌다. "before the run directory is created"로 다듬으면 된다.
6. **엔진 잔여 위험(스킬 문서 결함 아님).** `gitprim.GitPrimitiveError`는 `RuntimeError`라서 `run_verify`의 예외 절에도 `main`의 세 예외 절에도 걸리지 않는다. 후보 저장소의 git 조회가 실패하면 receipt 없이 traceback과 함께 종료코드 1이 날 수 있다. 남은 위험 목록에 한 줄 추가할 가치가 있다.
7. **`SKILL.md:196` `failed` 행 보강 여지.** UI 경로의 `VERIFY_UI_WARN_OR_FAIL`은 WARN/fail/flaky/부분 실행 외에 `actual_exit != 0`에서도 발생한다.
8. **`SKILL.md:90` build receipt 행 보강 여지.** 엔진은 `dist_digest` 존재도 요구한다(`VERIFY_BUILD_DIST_DIGEST_MISSING`).
9. **기계 검증 타임스탬프.** `VALIDATION_BUILD.json`은 편집 이전 실행분이다. 집계 대상은 편집으로 바뀌지 않아 결론은 유지되지만, 산출물 확정 후 `--phase build`를 한 번 더 돌려 타임스탬프를 맞추는 편이 안전하다.

## 감사 범위와 미확인 사항

- 감사한 실물: 원문 규칙 2종 전문, 설계서 2종, 증거 8종, 기계 검증 2종, 최종 `SKILL.md` 전문, 검사기 저장소의 `harness/om_workflow.py`·`verifycore/{workflow,testruns,pytest_runs,result_io}.py`·`integrations/om/verify.py`·`plancore/{schema,paths}.py`·`gitprim.py`·`binding.py`·스키마·`tests/test_om_verify_counterexamples.py`(표본 3구간)·`tests/test_claude_wiring.py`·`.claude/settings.json`·`.claude/hooks/run_om_plan_hook.sh`·`CLAUDE.md`.
- 파일은 하나도 수정하지 않았다.
- 미확인 1: 셸 실행 수단이 없어 `DESIGN_REQUIREMENTS.source_documents`의 sha256 3건을 재계산하지 못했다. 같은 이유로 `claude --version`, 참고 저장소 `git status --porcelain` 0줄도 재확인하지 못했다.
- 미확인 2: `Grep`·`Glob`이 `ENOEXEC`로 실패해 파일 열거를 하지 못했다. 보조 파일 부재는 표준 4경로 확인으로 대체했다.
- 미확인 3: `DOC/76`·`DOC/81`·`DOC/24`와 정본 `83`은 열지 않았다.
- 미확인 4: `verify run`을 실제 실행하지 않았다.
- 감사 대상 제외: `.claude/skills/om-plan/`, `.claude/skill-authoring/om-plan/`, `docs/om-plan/`.
- 판정 근거 요약: 차단 1건(증거 문서 인용 불일치)만 해소하면 `SKILL.md`·규칙 판정·외부 통제·기계 검증 측면에서는 `PASS` 요건을 이미 충족한다.
