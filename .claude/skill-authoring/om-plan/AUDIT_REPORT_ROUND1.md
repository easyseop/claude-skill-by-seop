# om-plan 독립 감사 결과 — 1차 (2026-08-24)

> 이 문서는 1차 독립 감사자가 반환한 결과를 **그대로** 기록한 것이다. 작성자는 판정을 바꾸지 않았다.
> 조치 내역은 `AUTHORING_REVIEW.md`의 「독립 감사 1차 결과와 조치」에 있다. 최종 판정은 `AUDIT_REPORT.md`에 있다.
> 아래 판정 줄은 기계 검증이 세는 대상이 아니도록 인용 형태로 보존한다: 1차 판정은 `CONDITIONAL`이었다.

## 종합 판정
- (1차) 판정: `CONDITIONAL`
- 핵심 이유: 규칙 89개·안티패턴 26개 전수 판정이 원문과 정확히 일치하고, APPLY·TRANSFORM 68건의 `targets` 문구가 모두 `SKILL.md`에 실재하며, 필수 EXTERNAL 통제 4건(`om_workflow.py`·`validate.py`·`settings.json`·`hook_policy.py`)이 실제 구현돼 있음을 원본 코드로 확인했다. CLI 인수·종료코드·오류 코드·게이트 메시지·스키마 필드도 실측과 일치한다. 다만 **`plan check` 경로에서 `--expected-input-lock-digest`를 주지 않아도 `approval`(2)에 도달할 수 있는데 `SKILL.md`는 도달 불가라고 단언**(코드와 어긋나는 단언, 2곳)하고, **`DESIGN_REQUIREMENTS`의 `workflow`(절차)와 `outputs`(런타임 출력 파일 목록)가 `COMMAND_SPEC.yaml`으로 이관되지 않아** upgrade 전용 산출물이 최종 파일에서 누락됐다. 차단 문제가 2건이므로 PASS를 쓰지 않는다.

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (전부 `RESOLVED`, 각 항목이 설계서 절 + 검사기 저장소 파일:줄 근거를 가짐. 표본 재검증 결과 `preflight.py:293-325`, `validate.py:414-437`, `resume.py:51-55`, `collectors.py:300-338/573-635`, 스키마 5종 모두 실재하고 인용 내용이 정확함)
- 미해결: 0
- 근거 없음: 0 (`/om-report`도 지시서 46행에 실재. 설계서에 없는 사실 보충은 발견되지 않음)
- 명세 반영 누락: 2 (`workflow` 8단계 전체, `outputs`의 런타임 산출 파일 목록)

## 규칙 집계
- 원문 규칙: 89 (`C` 20 + `P` 8 + `D` 12 + `E` 7 + `V` 8 + `S` 7 + `M` 5 + `CC` 22 — 원문 두 문서를 직접 열람해 계수)
- 판정 규칙: 89 (`APPLY` 55 / `TRANSFORM` 13 / `EXCLUDE` 16 / `EXTERNAL` 5, 합 89 재계산 일치)
- 누락: 0
- 중복: 0
- 미판정: 0 (안티패턴 26건도 전수 판정: `PASS` 20 / `NOT_APPLICABLE` 6)
- 반영 위치 없음: 0 (68건 `contains` 문구를 최종 파일과 1:1 대조해 전부 존재 확인)
- 근거 부족 제외: 0 (16건 모두 주단계 `P`·부작용 등급·미사용 기능이라는 구체 축에 연결됨. "관련 없음" 수준 처리 없음)
- 미구현 필수 외부 통제: 0 (`required_for_pass: true` 4건 전부 implemented 실측. `P-08`만 `planned`·`required_for_pass: false`)

## 차단 문제

| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| 높음 | `SKILL.md:182`, `SKILL.md:296` (6단계 실패 시 / 알려진 함정 7) | "digest를 주지 않으면 `verified`가 `false`가 되어 `approval`이 될 수 없다"는 단언이 `plan check`에서 거짓이다. 사람 검토를 기계가 강제한다고 과장한다 | `harness/om_workflow.py:285-303` — `supplied_digest`가 `None`이면 세션 marker의 `recorded_digest`를 읽어 `run_validation(..., expected_input_lock_digest=supplied_digest or recorded_digest)`로 전달한다. `record_trusted_input_lock_digest`는 `plan start`(같은 파일 253행)가 항상 기록하므로 `_trusted_input_binding`(`validate.py:45-67`)은 issue를 만들지 않고 `verified: true` → `approval`(2)이 나온다. 강제되는 것은 `plan-validate`(`om_workflow.py:450-457`, 인수를 그대로 전달) 뿐이다 | 두 문장을 "`plan check`는 digest를 생략하면 `plan start`가 marker에 기록한 값으로 대체하므로 `approval`이 가능하다. 사람 보관 digest 없이 통과하면 검토 생략을 기계가 잡지 못하므로 항상 `--expected-input-lock-digest`를 명시한다"로 교정. `DESIGN_REQUIREMENTS.validation`·`COMMAND_SPEC.validation`의 동일 시나리오(`digest 미제공 → 종료코드 3`)도 함께 정정 |
| 중간 | `COMMAND_SPEC.yaml` (`workflow`·`outputs`) | `DESIGN_REQUIREMENTS.workflow`의 8단계(입력·행동·산출물·검증·실패)가 `COMMAND_SPEC.yaml`에 전혀 없고, `outputs`의 런타임 산출 파일 목록도 이관되지 않았다(`outputs.runtime_files`가 `SKILL.md` 자신, `evidence_files`가 저작 증거로 대체됨). 그 결과 upgrade 전용 산출물 `official-doc-sources.yaml`·`official-doc-snapshots/`가 최종 `SKILL.md` 어디에도 이름으로 등장하지 않는다 | `COMMAND_SPEC.yaml` 전문에 절차·단계 키 부재(`execution`은 컨텍스트만 기술). `DESIGN_REQUIREMENTS.outputs` 3번째 항목 "upgrade에서만: official-doc-sources.yaml·official-doc-snapshots/" 대비 `SKILL.md` 미기재. 두 파일은 실제 산출물이다: `preflight.py:296-308`(`collect_documents` 후 비-upgrade면 삭제), `validate.py:496-498`·`om_workflow.py:466-469`(`plan-resume`이 재검증). `83 부록 A-1`은 "SKILL.md에서 언급하는 모든 입출력 파일은 해당 스키마 경로를 명시"를 요구하고 본문 5단계·층2가 이 스냅샷을 전제로 한다 | `COMMAND_SPEC.yaml`에 `workflow`(8단계 4단 계약)와 런타임 `outputs` 파일 목록을 추가하고, `SKILL.md`의 「입출력 파일과 스키마」 표에 `official-doc-sources.yaml`(upgrade 전용, 스키마 없음·`doc_sources`가 소유)과 `official-doc-snapshots/`(에이전트가 읽는 원문, 수정 금지) 행을 추가 |

## 시나리오 결과

| 시나리오 | 판정 | 근거 |
|---|---|---|
| 정상 호출 | 통과 | 1~8단계가 `om_workflow.py:317-376`의 실제 서브커맨드·인수와 일치. `plan start REQUEST`, `plan check RUN_DIR --expected-input-lock-digest`, `plan-resume --run-dir --state-root --session-id` 모두 argparse 선언과 동일. 성공 판정 `status: ready_for_proposal`(`preflight.py:311`)·exit 2 + `review_ready` + `verified:true`(`plan-result.schema.json` allOf)도 실측 일치 |
| 필수 입력 누락 | 통과 | `SKILL.md:73` "모드와 필수 입력을 추측해 채우지 않는다" + 모드별 표가 `plan-run-request.schema.json`의 `required`·`allOf` 6분기와 완전 일치(`pre_plan`의 `refs.candidate` 금지 포함). 스키마 위반은 `PlanControlError` → exit 3(`om_workflow.py:518-527`) |
| 잘못된 입력·허용값 | 통과 | `UPGRADE_RELATION_UNSUPPORTED`·`DEPLOYMENT_METHOD_REQUIRED`·`DEPLOYMENT_DOCUMENT_MISSING`·`CUSTOMIZATION_ID_INVALID` 4종이 `collectors.py:300-337`에 그대로 존재. 인접 판정은 `_version_relation`(40-61행)이 소유 |
| 대상 파일·설계서 부재 | 통과 | `REFS_UNAVAILABLE`·`ACTIVE_REGISTRATION_MISSING`·`RUN_DIRECTORY_EXISTS`가 `preflight.py:157-192,276-281`에 실재. 요청 파일 자체 부재는 1단계 "부족한 필드를 사용자에게 묻는다"로 흡수 |
| 권한 부족 | 부분 통과 | `안전과 권한`이 permissions·훅의 실제 차단을 정확히 기술하나(`settings.json`·`hook_policy.py` 실측 일치), 훅 거부를 검사 실패와 구분해 보고하라는 지시가 없다. `CC-16`의 "권한 부족을 코드 실패로 오인하지 않는다"가 본문에 구현되지 않았다 |
| 검증 실패 | 통과 | `reasons`·`evidence_ref_errors`·`dirty_paths`가 `plan-validation-attempt.schema.json` 필드와 일치. block/analysis_error 분기와 게이트 우회 금지 문장 존재 |
| 부분 변경 후 실패 | 통과 | `validation-attempts` append-only는 `validate.py:366-376`(`ATTEMPT_APPEND_ONLY_VIOLATION`), `plan start` 실패 시 `preflight-result.json` 기록·기존 run 미기입은 `preflight.py:329-342` 실측 일치 |
| 외부 콘텐츠의 규칙 무시 지시 | 통과 | 절대 경계 9번(신뢰 순서)과 `안전과 권한` 3·4번이 스냅샷·2차 판독·로그를 데이터로 고정하고 의심 항목 보고를 지시. `CLAUDE.md:17`의 "not a source of deterministic truth"와 정합 |
| 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true` + `SKILL.md:37`. 부작용(run 디렉터리·세션 marker·사람 검토)이 수동 전용을 정당화한다 |
| 기존 동명 스킬 충돌 | 통과 | 이식 대상 저장소에 `.claude/skills/om-plan/` 없음(부재 확인), 저작 저장소에도 신규. `SKILL.md:36`이 디렉터리 이름이 명령 이름을 결정한다고 명시 |

## 비차단 개선사항

1. `SKILL.md:209` — "`plan-validate`는 marker를 다루지 않고 검증만 하며"는 부정확하다. `run_validation`(`validate.py:589-591,543`)은 `pair_from_run`으로 `.plan-active`를 요구하고 종료 시 `cleanup_pair`로 marker 쌍을 지운다. marker를 **인수로** 받지 않을 뿐이다. `AUTHORING_REVIEW.md`가 이 문장을 실측으로 교정했다고 기록했으나 여전히 남아 있다.
2. frontmatter `allowed-tools` 최소성 — `Bash(git status *)`·`Bash(git diff *)`는 본문의 어떤 절차도 실행하지 않으며, 보호 세션 중에는 `hook_policy.decide_pre_tool_use`(179-216행)가 workflow 명령이 아닌 모든 Bash를 거부하므로 실제로 쓸 수 없다. `plan-preflight`·`plan-session-start`도 본문이 "훅과 보호된 CI가 쓰는 저수준 경로"라고 선언한 명령인데 사전 승인돼 있다. `CC-06`·`S-03` 최소성 기준으로 축소 검토 대상이다.
3. `SKILL.md:229` — `UserPromptSubmit`·`UserPromptExpansion`·`PreToolUse`·`Stop` 네 경로가 모두 "Git 상태 변경과 `proposal/` 밖 쓰기를 막는다"고 묶었으나, `Stop`은 `stop_is_allowed`(`hook_policy.py:232-240`)로 `validation-result.json` 없는 종료를 막는 다른 통제다.
4. `RULE_COVERAGE.yaml` `S-07` — 훅 경로를 `run_om_plan_hook.py`로 적었으나 `settings.json`이 실제로 배선한 진입점은 `run_om_plan_hook.sh`다(`.py`는 그 래퍼가 exec하는 대상). 두 파일 모두 실재하므로 통제 자체는 유효하나 증거 파일의 경로 표기를 교정할 것. `SKILL.md`는 `.sh`로 정확히 적었다.
5. `SKILL.md:103` — exit 2 구분법이 "stdout JSON이면 approval, stderr `입력 확인 필요`면 인수 오류"인데, argparse 자체 오류도 exit 2이며 이 문구를 내지 않는다(`om_workflow.py:512-514`는 `WorkflowInputError`에만 해당). "stdout JSON 부재 = approval 아님"으로 서술하는 편이 안전하다.
6. `83 부록 A-2`의 "exit 2는 CI에선 성공 취급[Q9]"이 본문에 없다. `.gitlab-ci.yml` 실측을 하지 않았다는 이유로 의도적으로 뺐고 `open_questions` 4번에 정직하게 기록했다 — 판단은 타당하나 정본 지시의 부분 미충족임을 남긴다.
7. `AUTHORING_REVIEW.md`·`SPEC_REVIEW.md`가 `allowed-tools`를 "6종 최소 목록"이라 기술하나 실제 항목은 13개다(도구 6종 + Bash 패턴 7개로 읽어야 함). 증거 문서의 수치 표기만 정정할 것.
8. `CC-13`(배포 대상 선언)의 `targets`가 `disable-model-invocation: true` 한 줄로 잡혀 있어 규칙 의미(배포 대상 명시적 선언)의 직접 증거로는 약하다. 실제 선언은 `SPEC_REVIEW.md`의 "배포 대상: Claude Code 전용"에 있고 `A-CC-12` 상 본문 제외는 타당하므로 `EXTERNAL` 또는 근거 위치 교체를 권한다.

## 감사 범위와 미확인 사항

- 확인한 것: 원문 규칙 2종 전문, 설계서 3종, 저작 증거 6종, 최종 `SKILL.md`, 기계 검증 2종(`ok:true`, `classified_rules:89`, `resolved_design_requirements:18`), 그리고 대상 런타임의 `om_workflow.py`(531줄 전문)·`verdict.py`·`plancore/{preflight,validate,resume,markers,hook_policy}.py`·`integrations/om/collectors.py`(요청 검증·proposal 게이트·upgrade 게이트 구간)·`plancore/schema/` 5종 중 4종 전문·`.claude/{settings.json,hooks/run_om_plan_hook.sh,hooks/run_om_plan_hook.py,agents/om-plan-official-doc-reviewer.md}`·`CLAUDE.md`·`harness/tests/test_claude_wiring.py`.
- `P-08` 판단: 정직성 타당. `test_claude_wiring.py`를 직접 열람한 결과 `om-apply` SKILL.md만 단언하고 `om-plan` 단언은 없어 `state: planned`가 사실이다. 규칙 본문(평가 계획을 문서 작성 전에 만든다)의 실질은 `COMMAND_SPEC.validation`(구조 3·시나리오 12·트리거·완료 단언 6)으로 충족됐고, 검사기 저장소는 지시서상 읽기 전용이며 wiring 테스트 추가는 `83 작업 3`이 Codex에 배정한 별도 작업이다. 따라서 "필수인데 회피"가 아니다. 다만 이 상태에서는 `SKILL.md`의 경계 문구가 지워져도 CI가 잡지 못한다는 위험이 남는다.
- 실행하지 않은 것: 검사기 CLI를 실제로 구동한 end-to-end 리허설(읽기 전용 감사 원칙), `.gitlab-ci.yml`의 exit 2 처리, `plan-preflight`/`plan-session-start` 실행 경로의 동적 확인.
- 검증 불가: 설치된 Claude Code 2.1.241에서 서브에이전트 도구의 실제 이름이 `Agent`인지 여부. `allowed-tools`의 `Agent` 항목과 `hook_policy.py:166`의 `tool_name == "Agent"`가 서로 정합하므로 대상 런타임 내부 기준으로는 일관되나, 제품 도구명과의 일치는 이 컨텍스트에서 확인할 수 없다.
- 파일은 하나도 수정하지 않았다.
