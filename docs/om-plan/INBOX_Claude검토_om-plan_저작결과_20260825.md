# [Claude 검토 요청] om-plan 스킬 저작 결과 — 인수인계

- 작성일: 2026-08-25
- 작성 세션: `claude-skill-author` full 모드로 `om-plan` 저작을 수행한 세션
- 수신: 다른 Claude 세션(1차 검토). 이 검토 후 Codex 검토가 예정돼 있다.
- 저작 지시서: `/Users/seop/claude-skill-by-seop/지시서_om-plan_스킬저작_20260824.md`
- **[해소됨 2026-08-25]** 아래 CONDITIONAL은 처리 완료 — 1차 검토(docs/om-plan/검토결과_om-plan_1차_20260825.md)로 차단 2건 수정 방향 확정, 사람 승인 예외 4차 감사 **PASS**, FINAL_STATUS PASS. 이력 보존을 위해 본문은 원문 유지.
- **당시 상태: `CONDITIONAL` — 완료 아님.** 독립 감사 3회 모두 PASS를 받지 못했고, 메타스킬이 정한 재감사 한도(최대 2회)를 소진했다.
- **커밋·푸시하지 않았다.** 모든 산출물은 워킹트리에 untracked 상태로 있다.

---

## 1. 이 문서 하나로 검토가 가능하도록 하는 전제

검토자는 아래 경로를 직접 열어 확인한다. 이 문서의 주장을 그대로 믿지 말 것.

### 저작 산출물 (이 저장소 `/Users/seop/claude-skill-by-seop`)

| 구분 | 경로 |
|---|---|
| 런타임 스킬 | `.claude/skills/om-plan/SKILL.md` (301줄) |
| 설계서 | `docs/om-plan/OM_PLAN_DESIGN.md` |
| 설계 요구사항 | `.claude/skill-authoring/om-plan/DESIGN_REQUIREMENTS.yaml` |
| 규칙 원문 인벤토리 | `.claude/skill-authoring/om-plan/RULE_MANIFEST.yaml` |
| 규칙 전수 판정 | `.claude/skill-authoring/om-plan/RULE_COVERAGE.yaml` |
| 실행 계약 명세 | `.claude/skill-authoring/om-plan/COMMAND_SPEC.yaml` |
| 명세 검토 | `.claude/skill-authoring/om-plan/SPEC_REVIEW.md` |
| 작성 검토(문장별 근거·감사 조치 이력) | `.claude/skill-authoring/om-plan/AUTHORING_REVIEW.md` |
| 감사 1차 원문 | `.claude/skill-authoring/om-plan/AUDIT_REPORT_ROUND1.md` |
| 감사 2차 원문 | `.claude/skill-authoring/om-plan/AUDIT_REPORT_ROUND2.md` |
| 감사 3차(최종) 원문 | `.claude/skill-authoring/om-plan/AUDIT_REPORT.md` |
| 기계 검증 결과 | `.claude/skill-authoring/om-plan/VALIDATION_{SPEC,BUILD,AUDIT}.json` |

### 대상 런타임 (읽기 전용, 절대 쓰지 말 것)

`/Users/seop/Documents/Codex/2026-07-24/sites-plugin-sites-openai-bundled/work/kb-datacatalog-upgrade-checker-om-plan-cli/`
브랜치 `codex/om-plan-verified-gates-20260820`, HEAD `82be68e733`. 이 저작 중 변경 0건(`git status --porcelain` 비어 있음).

### 내용 정본

`/Users/seop/Documents/Codex/2026-07-24/sites-plugin-sites-openai-bundled/skill_develop/om_plan/83_Codex_SKILLmd_작성지시_20260824.md` (부록 A가 SKILL.md 내용 요구의 정본)

---

## 2. 기계 검증 상태

| 게이트 | 결과 | 파일 |
|---|---|---|
| spec | exit 0, `ok: true` | `VALIDATION_SPEC.json` |
| build | exit 0, `ok: true` | `VALIDATION_BUILD.json` |
| audit | **exit 1**, `errors: ["independent audit is not PASS: CONDITIONAL"]` | `VALIDATION_AUDIT.json` |
| `FINAL_STATUS.json` | **생성되지 않음** | — |

집계: 원문 규칙 89개 전수 판정(APPLY 55 / TRANSFORM 13 / EXCLUDE 16 / EXTERNAL 5), 누락·중복·미판정 0. 안티패턴 26개 판정(PASS 21 / NOT_APPLICABLE 5). 설계 요구사항 18개 전부 RESOLVED, 상태 APPROVED. 주단계 `P`, 보조단계 `R`·`V`.

3차 감사가 확인한 것: 규칙 전수 판정 일치, `APPLY`·`TRANSFORM` 68건의 `targets` 문구가 `SKILL.md`에 실재하며 규칙의 실질 의미를 구현, `EXCLUDE` 16건 사유의 논리적 연결, 필수 `EXTERNAL` 통제 실재, 83 부록 A-1/A-2/A-3 충족.

---

## 3. 검토 최우선 항목 — 남은 차단 문제 2건

두 건 모두 **`block` 재개(7단계) 경로 한정**이다. 정상·승인·중단 경로의 판정·게이트·안전 경계에는 차단 문제가 없다.
두 건 모두 저작 세션이 검사기 코드로 직접 재확인했고, 감사 지적이 옳다고 판단했다.

### 차단 A — `plan-resume`의 `--state-root`·`--session-id` 출처가 관측 불가능한 값으로 지정됨

- **위치**: `.claude/skills/om-plan/SKILL.md:193`, `COMMAND_SPEC.yaml`의 `workflow[6]`, `DESIGN_REQUIREMENTS.yaml`의 `requirements.workflow.items[6]`
- **현재 문구**: "훅이 허용한 plan 계열 명령 앞에 `OM_PLAN_HOOK_STATE_ROOT`와 `OM_PLAN_SESSION_ID`를 주입하므로 그 값을 쓴다. 훅을 거치지 않는 환경에서는 2단계 stdout의 `state_root`·`session_id`를 쓴다."
- **결함**: 훅 주입값을 1차 출처로 지시하는데 에이전트가 그 값을 읽을 수 없다.
- **근거(재현 없이 코드로 확인 가능)**:
  - `harness/om_workflow.py:373-375` — `plan-resume`의 `--run-dir`·`--state-root`·`--session-id`가 모두 `required=True`. 환경변수 대체 경로가 없다.
  - 환경변수 대체는 `default_plan_state_root`(`om_workflow.py:65-85`)와 `select_plan_session_id`(`om_workflow.py:162-168`)에만 있고, 이 둘은 `plan start`·`plan check` 경로에서만 호출된다.
  - `harness/acgh/plancore/hook_cli.py:64-78`(`_updated_command`) — 훅은 명령 문자열 **앞에 셸 변수 할당 접두사**(`OM_PLAN_SESSION_ID=... OM_PLAN_HOOK_STATE_ROOT=... <원래 명령>`)를 붙인다. 셸은 명령을 실행하기 전에 `$VAR`를 확장하므로, 같은 명령 안에서 그 값을 되읽을 수 없다.
  - `harness/acgh/plancore/hook_policy.py`의 `_SHELL_OPERATORS`가 `$(`를 차단하므로 명령치환 우회도 불가능하다.
- **수정안**: `SKILL.md:193`을 아래로 교체한다.

  ```text
  `STATE_ROOT`와 `SESSION_ID`는 지어내지 않는다. 2단계 `plan start`의 stdout JSON에 있는 `state_root`·`session_id` 값을 그대로 쓴다.
  훅이 명령 앞에 붙이는 `OM_PLAN_HOOK_STATE_ROOT`·`OM_PLAN_SESSION_ID`는 CLI가 스스로 참조하는 값이며 이 문서에서 인용할 값이 아니다.
  ```

  근거: `harness/om_workflow.py:264-270`이 `plan start` 반환값에 `"state_root"`·`"session_id"`를 담는다.
- **동반 수정**: `COMMAND_SPEC.yaml`의 `workflow[6]`과 `DESIGN_REQUIREMENTS.yaml`의 `requirements.workflow.items[6]`에서 같은 문장을 교체한다. 수정 후 `RULE_COVERAGE.yaml`의 `targets` 문구 재대조와 spec·build 게이트 재실행이 필요하다.

### 차단 B — `/om-resume` 명령이 대상 저장소에 존재하지 않는다

- **위치**: `.claude/skills/om-plan/SKILL.md:186`, 같은 `workflow[6]`
- **현재 문구**: "사용자가 `/om-resume`을 새로 입력해 훅이 marker를 만들게 한다."
- **결함**: 실재하지 않는 슬래시 명령에 절차가 의존한다.
- **근거**:
  - 대상 저장소에 `.claude/commands/` 디렉터리 자체가 없다.
  - `.claude/skills/` 하위에는 `om-apply` 하나뿐이다(`om-resume` 부재).
  - 그럼에도 `.claude/settings.json`의 `UserPromptExpansion` matcher는 `^(om-plan|om-resume)$`이고, `harness/acgh/plancore/hook_cli.py:86-99`의 `UserPromptSubmit` 분기는 프롬프트가 `/om-plan` 또는 `/om-resume`으로 시작하면 `create_session_marker`를 호출한다. 즉 훅은 그 이름을 전제하지만 소유 파일이 없다.
- **미확인(검토자가 판단해야 할 지점)**: 등록되지 않은 슬래시 명령을 사용자가 입력했을 때 Claude Code가 `UserPromptSubmit` 훅을 발화하는지 실행 검증하지 못했다. 발화한다면 `/om-resume`은 "등록된 명령"이 아니라 "훅이 인식하는 프롬프트 접두사"로 동작하므로 절차 자체는 성립하고, 이 항목은 문서 표현 문제로 격하된다. 발화하지 않는다면 `block` 재개 경로가 실제로 막힌다.
- **수정안(둘 중 택일 — 위 미확인 사항의 결론에 따라 결정)**:
  - (a) 훅이 발화한다면: `SKILL.md:186`을 "사용자가 `/om-resume`으로 시작하는 프롬프트를 새로 입력한다. 이는 등록된 슬래시 명령이 아니라 `UserPromptSubmit` 훅이 인식하는 접두사이며, 훅이 세션 marker를 만든다"로 바꾼다.
  - (b) 발화하지 않는다면: marker 재생성 방아쇠를 실재하는 `/om-plan` 재입력으로 바꾸고 그때의 `SESSION_ALREADY_ACTIVE`·중복 run 처리 흐름을 본문에 기술하거나, 대상 저장소에 `om-resume` 스킬을 추가하는 별도 작업으로 분리한다.

---

## 4. 미구현 외부 통제 1건

- `RULE_COVERAGE.yaml`의 `P-08` — `harness/tests/test_claude_wiring.py`가 `om-apply`의 SKILL.md만 단언하고 `om-plan` 단언이 없다. `state: planned`, `required_for_pass: false`로 기록했고 통과 처리하지 않았다. 3차 감사도 이 표기를 "정직하다"고 확인했다.
- **남는 위험**: 현재 상태에서는 `SKILL.md`의 핵심 경계 문구가 삭제돼도 CI가 잡지 못한다.
- **참고**: wiring 테스트 보강은 `83_Codex_SKILLmd_작성지시_20260824.md`의 「작업 3」이 Codex에 배정한 작업이며, 이 저작 지시서의 쓰기 허용 범위(대상 저장소 읽기 전용) 밖이다.
- **동반 정정 필요(3차 감사 비차단 7번)**: `RULE_COVERAGE.yaml`의 `P-08` 사유 문장이 "83 작업 3 범위 밖"이라고 적혀 있으나, 83 작업 3은 오히려 그 보강을 **요구**한다. "이번 저작 지시서 범위 밖"으로 정정해야 한다.

---

## 5. 비차단 개선사항 9건

3차 감사가 남긴 목록이 `AUDIT_REPORT.md`의 「비차단 개선사항」에 그대로 있다. 요지만 적는다.

1. 「입력과 인수」의 "`run-request.yaml`의 필드로 확정한 뒤"가 1단계의 "이 파일은 에이전트가 만들지 않는다"와 주체 충돌.
2. 6단계 digest 생략 서술은 `plan start`가 만든 **첫 검증**에만 해당. `plan-resume` 후 새 marker에는 `trusted_input_lock_digest`가 없어 생략 시 exit 3.
3. `plan-validate` 미제공 시 결과는 실제로 `analysis_error`(3)인데 본문 표현이 약함.
4. 저수준 명령의 "일반 권한 절차로 실행" 안내가 보호 세션 중 성립하지 않는 경우가 있음(`_workflow_action`이 `plan-session-start`를 인식하지 않음).
5. `preflight-result.json`은 `RUN_DIRECTORY_EXISTS`일 때 기록되지 않는 예외가 표에 없음.
6. CI 매핑의 인과 서술("사람 결정에 따른 것")에 인용 가능한 결정 기록이 증거 파일에 없음.
7. `P-08` 사유 출처 오귀속(위 4절).
8. 완료 상태 어휘가 `CC-16`의 `실패` 대신 `중단`. `V-08`과는 정합.
9. `COMMAND_SPEC.inputs`에 CLI 선택 인수·기본값 4항목 미이관.

---

## 6. 저작 과정에서 확인한 중요 사실 (검토 시 참고)

이 항목들은 코드 실측 결과이며 `SKILL.md`에 이미 반영돼 있다. 검토자가 반대 결론을 내린다면 그 근거를 명시해 주기 바란다.

1. **`plan check`는 종료코드 0을 내지 않는다.** `harness/acgh/plancore/validate.py:524-531`의 검증 경로는 `APPROVAL`·`BLOCK`·`ANALYSIS_ERROR`만 만든다. 성공 상태는 exit 2(`approval` / `review_ready`)다.
2. **`plan check`는 `--expected-input-lock-digest`를 생략해도 `approval`에 도달한다.** `harness/om_workflow.py:253`에서 `plan start`가 digest를 세션 marker에 기록하고, `:287`·`:302`에서 `plan check`가 그 값으로 대체한다. 따라서 사람 검토를 기계가 강제하지 않는다. 이 사실 때문에 절차가 "항상 명시한다"를 요구한다. (강제되는 것은 저수준 `plan-validate`뿐.)
3. **보호 세션 중에는 `git status`조차 실행할 수 없다.** `hook_cli.handle_event`가 `/om-plan` 프롬프트에서 marker를 만들고, 이후 `hook_policy.decide_pre_tool_use`가 plan 계열 workflow 명령이 아닌 모든 Bash를 기본 거부한다. 저장소 clean 여부는 `plan start`의 `WORKTREE_DIRTY`가 판정한다.
4. **`run-request.yaml`은 에이전트가 만들 수 없다.** run 결속 전 모든 Write가 거부되고, 결속 후에도 `proposal/` 안으로만 허용된다. 사람이 보호 범위 밖에서 준비해 경로로 전달해야 한다.
5. **보호된 CI는 exit 2를 성공으로 취급한다.** `harness/ci/om_plan_ci.py:324`가 `ci_exit_code = 0 if verdict in {"pass", "approval"}`, `:325`가 `success-review-ready`로 매핑한다.
6. **upgrade 필수 산출물 9종과 3층 검증**은 `harness/acgh/integrations/om/collectors.py:769-868`에 구현돼 있으며, `path-remap` 커버리지와 `doc-code-crosscheck` 연결이 층1(결정적 강제)이다.

---

## 7. 검토자에게 요청하는 판단

1. **차단 A의 수정안이 옳은가.** `plan start` stdout의 `state_root`·`session_id`를 1차 출처로 삼는 것이 실제 실행 흐름에서 성립하는지 확인해 달라.
2. **차단 B의 미확인 사항을 결정해 달라.** 등록되지 않은 슬래시 명령에서 `UserPromptSubmit` 훅이 발화하는가. 이에 따라 수정안 (a)/(b)가 갈린다. 사용자 수준 설정(`~/.claude/`)이나 플러그인에 `om-resume`이 존재하는지도 함께 확인이 필요하다.
3. **재감사 한도 처리.** 메타스킬 규정상 수정·재감사는 최대 2회이며 이미 소진했다. 차단 2건을 수정한 뒤 4차 감사를 돌릴지, 아니면 `CONDITIONAL` 상태 그대로 Codex 검토로 넘길지 사람 결정이 필요하다.
4. **비차단 9건과 `P-08` 사유 정정**을 이번에 함께 처리할지, Codex 단계로 미룰지.

---

## 8. 안전 확인 (이 저작 세션이 지킨 것)

- 검사기 저장소 변경 0건. 정본 문서 폴더 변경 0건(mtime 검사로도 확인).
- 커밋·푸시·브랜치 변경 없음.
- 쓰기는 `docs/om-plan/`, `.claude/skills/om-plan/`, `.claude/skill-authoring/om-plan/`에만 했다. 예외로 메타스킬 스크립트가 공용 `.claude/skill-authoring/.active.json`을 갱신하는데, 이는 지시서가 실행하라고 지정한 `init_authoring.py`·`validate_authoring.py`의 정상 동작이다.
- 같은 저장소에서 다른 세션이 `om-verify`를 병렬 저작 중인 것을 관찰했다. 해당 경로(`.claude/skills/om-verify/`, `.claude/skill-authoring/om-verify/`)는 읽지도 고치지도 판정하지도 않았다.
- 감사 보고서 3건은 반환된 원문 그대로 기록했고 판정을 바꾸지 않았다.
