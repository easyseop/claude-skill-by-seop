> 2차 독립 감사(skill-author-auditor 새 인스턴스) 반환 결과를 그대로 기록한다.
> 하네스가 표시 과정에서 `<`·`>`·`&`를 HTML 엔티티로 이스케이프한 것만 원문자로 되돌렸고, 판정과 내용은 수정하지 않았다.
> 이 보고서의 비차단 지적 9건을 반영한 뒤 **새 감사자 인스턴스**로 3차 감사를 수행했다. 최종 판정은 `AUDIT_REPORT.md`에 있다.

---

# om-verify 독립 감사 결과 (2차)

## 종합 판정
- 2차 판정: PASS
- 핵심 이유:
  - 원문 2종을 직접 열어 제목 단위로 계수했다. 공통 67(C-20·P-08·D-12·E-07·V-08·S-07·M-05) + Claude Code 전용 22(CC-01~22) = 89이며, manifest 89·coverage 89와 정확히 일치한다. 안티패턴 26(A-01~12 + A-CC-01~14), stage_modules 9도 실물과 일치한다. 누락·중복·미판정 0.
  - `APPLY`·`TRANSFORM` 65개 규칙의 70개 `targets[].contains` 문구를 `SKILL.md` 222줄 본문과 1건씩 대조해 전부 실재를 확인했다. 1차 이후 갱신된 P-05·S-03·CC-16의 target 문구도 실물에 있다.
  - **이번 회차 반증 대상 10건을 코드로 전수 재검증했고 결정적 반증에 실패했다.** 특히 (1) 경계 문장의 좁힘은 완화가 아니다 — `workflow.py:413-414`가 `ui_component` 부재 시 UI 게이트를 `status: verified` + `execution_status: not_configured`로 기록하므로, 좁히기 전 문장이 오히려 코드와 모순이었고 좁힌 문장은 `testruns.evaluate`(skip→`VERIFY_REQUIRED_TEST_NOT_PASS`→infra_error)·`_final_status`·skip 분기 3곳과 정합한다. 거짓 verified 구멍은 생기지 않았다. (2) 케이스 표 `failed` 행의 UI 사유는 정확하다 — `om/verify.py:288-289`가 `warn/fail/flaky/pass!=total`을 모두 `VERIFY_UI_WARN_OR_FAIL`로 올리고 `workflow.py:425`가 그 코드만 `failed`로 매핑한다. (6) 함정 2행은 `_validate_apply`의 `_file_state(snapshot) != registration_final_digest` 단일 기전만 남겨 정확하다. (7) `permissions.deny` 5항목은 검사기 저장소 `.claude/settings.json`에 실재하므로 "checker repository" 명시가 사실이다.
  - 필수 외부 통제(`required_for_pass: true`) 5경로를 직접 열어 확인했다: `om_workflow.py`(exit 매핑·analysis_error 3), `verifycore/workflow.py`(fail-closed 게이트·`VERIFY_RUN_ALREADY_EXISTS`·`controlled_names`), `pytest_runs.py`(`_BLOCKED_ENV` 6종), `result_io.py`(`os.chmod(destination, 0o444)`), `.claude/settings.json`(push·tag·docker push·kubectl apply·helm upgrade deny). CC-21의 `UserPromptExpansion`은 matcher가 `^(om-plan|om-resume)$`임을 실측했고 `state: planned` + `required_for_pass: false`로 정직하게 미구현 기록돼 있다(구현 위장 없음).
  - 기계 검증 `VALIDATION_SPEC.json`·`VALIDATION_BUILD.json` 모두 `ok: true`, errors 0, warnings 0이고 집계(89/89, 18/18)가 내 독립 계수와 일치한다. 보조 파일 미생성(references·scripts·assets·evals·README 전부 부재)과 동명 스킬 부재(검사기 저장소 `.claude/skills/om-verify/SKILL.md`, 저작 저장소 `.claude/commands/om-verify.md` 모두 부재)를 직접 확인했다.
  - 다만 1차 지적 반영 과정에서 **부분 이행 3건**과 코드 실측 정확도 결함 2건이 남았다. 어느 것도 거짓 `verified`·위험 행동·통제 미구현으로 이어지지 않아 차단으로 올리지 않았으나, 이식 전 정정 대상으로 아래에 열거한다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (전부 `RESOLVED`, `value`/`items` 비어 있지 않고 `sources`에 설계서 절 번호 + 스키마·엔진 절대경로가 연결됨. 표본 재확인: `inspect_runtime` required 8필드, `_load_waiver` 6필드·만료 검사, `escalation_required = status=="infra_error" and prior+1>=3`, `om_workflow.py:14-20` Python 3.11 게이트)
- 미해결: 0
- 근거 없음: 0 (설계서에 없는 내용을 사실처럼 보충한 항목 없음. 3번째 호출 예는 설계서 §4에 근거 문장과 함께 실재하며 §2 세 번째 사용 시점 + `DOC/83` 부록 A-3에 연결됨 — 다만 "수집된 실제 요청"이 아니라 합성 예시임은 아래 비차단 10번)
- 명세 반영 누락: 0 (18개 전부 `COMMAND_SPEC`의 purpose/scope/permissions/execution/outputs/validation/failure_handling/completion_conditions로 추적됨. `validation`만 본문 축약이며 사유 기록됨)

## 규칙 집계
- 원문 규칙: 89 (C 20 · P 8 · D 12 · E 7 · V 8 · S 7 · M 5 · CC 22)
- 판정 규칙: 89 (APPLY 42 · TRANSFORM 23 · EXCLUDE 18 · EXTERNAL 6 — 내가 재계수한 값이 작성자 주장과 일치)
- 누락: 0
- 중복: 0
- 미판정: 0
- 반영 위치 없음: 0 (70개 target 전부 `SKILL.md` 실재)
- 근거 부족 제외: 0 (EXCLUDE 18건 모두 주단계 V·부작용 등급·선택한 기술 경로에 연결된 구체 사유. "관련 없음" 수준의 사유 없음)
- 미구현 필수 외부 통제: 0

## 차단 문제
| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| — | — | 없음 | 코드·스키마 대조에서 최종 파일의 사실 주장 결정적 반증 실패, 필수 외부 통제 5경로 실물 확인, 기계 검증 2건 통과, 규칙 89/89 판정·70 target 실재 | — |

## 시나리오 결과
| 시나리오 | 판정 | 근거 |
|---|---|---|
| 1. 정상 호출 | 통과 | `SKILL.md:113-186` 5단계가 사전확인→호출→해석→보고로 이어지고, 148-151행 명령이 `om_workflow.py:400-404`의 실제 인자(`verify run REQUEST --run-dir`)와 일치 |
| 2. 필수 입력 누락 | 통과 | `SKILL.md:21-22` "If the invocation names no target, ask for the run directory or receipt path instead of guessing one." + `COMMAND_SPEC.inputs.arguments.default` |
| 3. 잘못된 입력·허용값 | 조건부 통과 | `retries≠0`(52행)·통제 환경변수(105-108행) 차단은 코드와 일치. 다만 155-158행의 "Exit 2 means the input was rejected before any run existed"는 실측과 어긋난다 — 스키마 위반·필수 필드 누락·요청 파일 부재는 모두 `PlanControlError` → `analysis_error` + **exit 3**이고, exit 2는 argparse 오류·미지원 하위명령·git 실패·Python 3.11 미만뿐이다(비차단 4번). "코드를 그대로 보고" 지침이 오판정을 막는다 |
| 4. 대상 파일·설계서 부재 | 통과 | 2단계(127-140행)가 build/fixture receipt·run-dir 부재·컨테이너 상태를 호출 전에 확인하고, 확인 불가는 62-63행에 따라 미확인 보고 |
| 5. 권한 부족 | 통과 | 64-65행 신설 문장이 도구 거부·명령 차단을 테스트 실패와 분리하고 거부된 명령명을 지목하게 한다(CC-16 충족). 1차의 조건부 통과가 해소됨 |
| 6. 검증 실패 | 통과 | 188-194 케이스 표(UI 사유 포함) + 181행 "every reason code verbatim" + 173-174행 실패 run 보존 |
| 7. 부분 변경 후 실패 | 통과 | verify는 제품 변경이 없어 롤백 대상 없음(39-40행), 부분 실행은 `skipped_due_to_stop`으로 통과 아님(171-172행), 실패 run 디렉터리를 증거로 보존 |
| 8. 외부 콘텐츠의 규칙 무시 지시 | 통과 | 55-61행이 receipt·JUnit·로그·docker·엔드포인트를 데이터로 고정하고, "skip a check, relax a threshold, or promote a WARN" 요구를 실행하지 않고 의심 항목으로 보고시키며, 신뢰 출처를 스키마·엔진·CLI로 한정 |
| 9. 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true`(부작용 명령, CC-02·A-CC-03). 미발동은 수동 전용 설계상 의도이며 description이 메뉴 식별을 돕는다 |
| 10. 기존 동명 스킬과 충돌 | 통과 | 저작·검사기 두 저장소 모두 `om-verify` 부재 실측, `.claude/commands/om-verify.md`도 부재. `name`=디렉터리명=`om-verify` 일치 |

## 비차단 개선사항

1. **입력 계약 fixture receipt 행이 엔진보다 강하게 단언한다(우선순위 최상).** `SKILL.md:89`는 6필드 "every one of them must match this run, this candidate, and the inspected container"라고 쓰지만, `om/verify.py:211-217`이 실제로 대조하는 것은 `run_id`·`candidate_sha`·`container_id`·`volume_names` 4개뿐이다. `fixture_set_digest`는 증거로 기록만 되고(`verify.py:244`) 비교 대상이 없으며, `applied_at`은 스키마 검증 외에 어떤 대조도 받지 않는다. 이는 `DOC/81`의 남은 위험 "fixture 사후 변경 미증명"과도 어긋난다. 보수 방향의 오차라 거짓 verified를 만들지는 않으나, 사람 보고에서 결속되지 않은 항목을 결속됐다고 쓰게 만들 수 있다(E-07 위반 경로). 4필드는 "must match", 나머지 2필드는 "recorded, not cross-checked"로 분리 표기할 것.
2. **`SPEC_REVIEW.md:39`가 최종 산출물과 정면으로 어긋난다.** "`allowed-tools`: `Read`·`Glob`·`Grep`과 `Bash(...)` 3종만 사전 승인한다 … **쓰기 도구는 넣지 않는다**"라고 적혀 있으나 최종 frontmatter는 `Write`와 `Bash(git status)`·`Bash(git diff)`를 포함한다. `COMMAND_SPEC.permissions.allowed_tools_policy`와 `RULE_COVERAGE.S-03.rationale`은 갱신됐는데 `판정: APPROVED`로 마감된 `SPEC_REVIEW.md`만 1차 이전 상태로 남았다. 권한 설계를 이 문서로 승인하는 사람·Codex 검토자에게 거짓 정보가 된다. 이식 전 정정 필요.
3. **1차 지적 8번(줄 수)의 반영이 절반이다.** `AUTHORING_REVIEW.md:201`은 222줄로 정정했지만 같은 문서 `:30` 「최종 프로필」은 여전히 "216줄"이다. `RULE_COVERAGE.D-08`(222줄)·실측값(222줄)과 어긋나며, 반영표의 "반영 … 이 문서" 주장이 문서 안에서 자기모순이다.
4. **exit 2 서술이 코드 실측과 다르다.** 위 시나리오 3 참조. 지시서 §5-4가 "CLI의 실제 인자·exit 의미를 코드 실측으로 기재(추측 금지)"를 명시하므로, "Exit 2 is a CLI argument or interpreter error; a rejected request file exits 3 with `analysis_error`"로 정정하면 두 문장이 하나의 사실로 합쳐진다.
5. **1차 지적 1번의 좁히기가 완료 정의에는 적용되지 않았다.** 경계 43-44행은 `skipped_due_to_stop`으로 좁혔으나 완료 정의 `SKILL.md:33-34`는 여전히 "no gate was skipped"다. `not_configured`(실행되지 않았으나 `status: verified`)를 "skipped"로 읽으면, 엔진이 `verified`를 낸 정상 run을 완료로 부르지 못하는 문면 긴장이 남는다. 4단계 검증문(171-172행)이 대상을 한정해 오판정으로 이어지지는 않는다. "no gate stopped with `skipped_due_to_stop`"으로 통일할 것.
6. **신설된 "permission stop"이 명세에 역추적되지 않는다.** `SKILL.md:64-65`는 규칙 CC-16에 근거하지만, `COMMAND_SPEC.failure_handling.states` 5종(완료/실패/검증 불가/승인 필요/조건부 완료)과 `DESIGN_REQUIREMENTS.failure_handling`에는 권한 중단 상태가 없다. 본문에만 존재하는 상태가 생겼다. 명세에 상태 1종을 추가하거나 기존 중단 상태에 귀속시킬 것.
7. **`RULE_COVERAGE.CC-16.rationale`이 실제보다 넓게 주장한다.** "조건부(UI not_configured)를 별도 상태로 두고"라고 적었지만 본문에는 조건부 완료라는 **보고 상태**가 정의돼 있지 않다. 99-101행은 조건과 판정 방식만 기술하고, 미검증 표시는 보고 템플릿의 "Unconfirmed items"로 흡수된다. 사유를 실제 반영 수준으로 낮추거나 케이스 표에 조건부 행을 추가할 것.
8. **`DESIGN_REQUIREMENTS.source_documents`의 설계서 sha256이 최신인지 확인되지 않았다.** 1차 이후 설계서 §4에 3번째 호출 예를 추가했는데, `validate_authoring.py`는 source_documents의 digest를 재검증하지 않는다(스크립트 전문 확인). 이 세션은 명령 실행 권한이 없어 해시를 계산하지 못했다. 이식 전 `init_authoring.py` 재실행 또는 해시 재계산으로 증거 사슬을 맞출 것.
9. **`Write`가 경로 무제한이다.** 요청 파일 1건 작성이라는 실제 필요에 비해 사전 승인 범위가 넓다(S-03의 "필요한 도구만 노출"). run 디렉터리 경로가 실행마다 달라 경로 한정이 어렵다는 사정은 인정되나, `COMMAND_SPEC`에 "경로 한정 불가 사유"를 한 줄 남기면 다음 개정에서 재검토 가능하다. `Edit` 미포함 결정은 본문 금지(기존 산출물 편집 금지)와 정합해 타당하다.
10. **3번째 호출 예는 수집된 실제 요청이 아니라 합성 예시다.** 지시서 「사용·비사용 조건」의 호출 예는 2건이고, 3번째는 설계서 §2의 사용 시점에서 파생한 문장이다. 근거를 §4에 명시해 은폐는 아니지만 P-01의 "실제 사용자 요청 3개 수집"을 문면대로 충족하지는 않는다. 실운용 후 실제 요청으로 교체할 것.
11. **`/om-report` 전방 참조는 여전히 실행 불가능한 대안이다(작성자 미반영, 사유 타당).** 책임 경계 유지(A-CC-11)라는 미반영 사유는 타당하고 설계서 §3·§20·`COMMAND_SPEC.open_questions`에 착수 미정이 기록돼 은폐가 아니다. 다만 본문 3·30행은 이 명령이 아직 없다는 사실을 알리지 않아, 요약 보고를 요청한 사용자가 막다른 길로 안내된다. "(not yet available)" 한 마디만 추가하면 C-19의 안전한 대안 요건과 정합한다.
12. **`cd ... && python ...` 단일 호출 미승인 결정은 은폐가 아니다.** 본문이 `cd`와 명령을 두 줄로 제시하고, `allowed-tools`는 제한이 아니라 사전 승인이므로 안전 영향이 없으며, `AUTHORING_REVIEW` 남은 위험 4에 "권한 질문 빈도만 증가"로 명시돼 있다. `Bash(git status)`/`Bash(git status *)` 이중 등록 형식은 같은 저장소 `claude-skill-author/SKILL.md:21-24`의 실제 관행과 일치한다.

## 감사 범위와 미확인 사항

- 감사한 실물: 감사 기준 `audit-rubric.md`, 원문 규칙 2종 전문, 설계서 `OM_VERIFY_DESIGN.md`, 저작 지시서, 증거 6종, 1차 감사 원문, 기계 검증 2종, 최종 `SKILL.md` 전문, 메타스킬 `validate_authoring.py`·`claude-skill-author/SKILL.md` frontmatter, 그리고 검사기 저장소의 `harness/om_workflow.py`, `verifycore/{workflow,testruns,pytest_runs,result_io,schema}.py`, `integrations/om/verify.py`, 스키마 4종, `applycore/schema.py`, `plancore/schema.py`, `tests/test_claude_wiring.py`, `.claude/settings.json`, `.claude/skills/om-apply/SKILL.md`, `CLAUDE.md`.
- 파일은 하나도 수정하지 않았다.
- 미확인 1: 이 세션에서도 `Grep`·`Glob`이 `ENOEXEC`로 사용 불가였다. 규칙 계수와 target 대조는 전부 `Read` 전문 읽기로 수동 수행했다. 파일 열거가 불가능해 보조 파일 부재는 `references`·`scripts`·`assets`·`evals`·`README.md` 5경로에 한해 확인했다. 비표준 이름 파일이 스킬 폴더에 있는지는 확인하지 못했다.
- 미확인 2: 명령 실행 권한이 없어 sha256 재계산, `claude --version = 2.1.241`, `git status --porcelain 0줄`(참고 저장소 무변경), `verify run` 실제 실행은 재확인하지 못했다. 버전 의존 필드 사용 근거는 같은 저장소 `claude-skill-author/SKILL.md`가 `disable-model-invocation`·`argument-hint`·`allowed-tools`를 실제로 쓴다는 사실로 독립 확인했다(CC-19).
- 미확인 3: `DOC/83`·`DOC/76`·`DOC/81`·`DOC/24`는 열지 않았다. 이들에 근거한 주장(부록 A 형식 요구, 리허설 실측, 남은 위험 6건, R-6)은 코드·스키마·테스트로 교차 확인 가능한 범위에서만 검증했고 문서 고유 주장은 미검증이다. 작성자도 "이 세션은 `verify run`을 실제 실행하지 않았다"고 기록했으며 나 역시 실행 검증은 하지 않았다.
- 미확인 4: `harness/tests/test_om_verify_counterexamples.py`의 OV 반례 줄 번호는 이번 회차에서 재확인하지 않았다(1차에서 확인됨). 이번 감사의 코드 대조는 엔진·CLI·스키마 원본에서 직접 수행했다.
- 감사 대상에서 제외: `.claude/skills/om-plan/`, `.claude/skill-authoring/om-plan/`, `docs/om-plan/` — 읽지도 판정하지도 않았다.
