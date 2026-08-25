# om-plan 명세 검토

## 조사 범위

- 저작 저장소 `/Users/seop/claude-skill-by-seop`: `git status --short` 비어 있음(2026-08-24), `CLAUDE.md`·`CLAUDE.local.md`·`.claude/rules/` 없음, `.claude/settings.json` 없음(`.claude/settings.stop-hook.example.json`만 존재), `.claude/skills/`에 `claude-skill-author`만 있고 `om-plan`은 없음 — 신규 생성이 맞다. `.claude/agents/skill-author-auditor.md` 존재.
- 대상 런타임(검사기 저장소) `/Users/seop/Documents/Codex/2026-07-24/sites-plugin-sites-openai-bundled/work/kb-datacatalog-upgrade-checker-om-plan-cli/`:
  - `harness/om_workflow.py` 531줄 — 서브커맨드·인수·종료코드 실측.
  - `harness/acgh/verdict.py` — `EXIT_CODE = {pass:0, block:1, approval:2, analysis_error:3}` 실측.
  - `harness/acgh/plancore/{preflight,validate,resume,paths,errors,hook_policy}.py` — 산출 파일·게이트·재개 조건·훅 정책 실측.
  - `harness/acgh/integrations/om/collectors.py` — 4모드 사실 수집과 proposal 게이트(upgrade 9종 산출물·path-remap 커버리지·독립 판독) 실측.
  - `harness/acgh/plancore/schema/` 5종 — 입출력 정본 실측.
  - `.claude/{settings.json,hooks/,agents/,skills/om-apply/SKILL.md}`, `CLAUDE.md`, `README.md`, `harness/tests/test_claude_wiring.py` 실측.
- 정본·결정 문서: `83_Codex_SKILLmd_작성지시_20260824.md`(부록 A), `24_누락감사_사람결정과_기록_20260820.md`(Q9·Q11·R-1~R-6·D-directtest), `하위_om-plan_논의정리_20260821.md`.
- 설치 Claude Code 버전: `claude --version` = `2.1.241 (Claude Code)`.
- 메타스킬 무결성: 필수 파일 전부 존재, `init_authoring.py`·`validate_authoring.py`·`stop_gate.py` `python3 -m py_compile` 통과. 재설치 불필요.

## 설계 입력 검토

- 필수 요구사항 수: 18
- 해결 수: 18
- 미해결 수: 0
- 설계서·호출문·저장소 근거: 설계서 `docs/om-plan/OM_PLAN_DESIGN.md`(20개 섹션 전부 작성), 저작 지시서 `지시서_om-plan_스킬저작_20260824.md`, 정본 지시 `83_Codex_SKILLmd_작성지시_20260824.md`. 모든 항목에 검사기 저장소의 파일:줄 근거를 연결했다.
- 설계 입력 판정: APPROVED

## 대상 스킬 프로필

- 명령 이름: `/om-plan`
- 주단계: `P`(계획·설계)
- 보조단계: `R`(조사·이해), `V`(검증·리뷰)
- 사용자 관점 결과: 검사기가 검증한 계획 run 디렉터리 하나와, 그 `validation-result.json`의 판정을 재해석 없이 옮긴 보고.
- 호출 주체: 사용자 전용
- 부작용 등급: 로컬 쓰기(새 run 디렉터리와 `proposal/` 문서만)
- 실행 컨텍스트: inline
- 동기·백그라운드: 동기
- 입력 형식: 자유문 `$ARGUMENTS` + 확정된 `run-request.yaml`
- 출력 형식: 5개 섹션 고정 보고
- 완료 조건: 5개(설계서 17절)
- 승인 지점: 4개(intent_review, approval 후 검토, 입력 변경, missing_requirements 처리)
- 복구 수단: `block`은 `plan-resume`, 그 밖은 새 run
- 배포 대상: Claude Code 전용

## 단계 판정

주단계를 `P`로 정한 근거는 최종 사용자가 얻는 핵심 결과가 "실행 전 계획"이라는 점이다(02 문서 §3.2 "결과가 실행 전 계획이면 `P`"). 검사기가 저장소를 훑어 사실을 수집하는 부분은 `R`, `plan check`로 게이트를 판정하는 부분은 `V`이지만 둘 다 계획을 성립시키기 위한 보조다. 실제 파일 변경(`I`)과 배포(`O`)는 `/om-apply`·`/om-verify`가 소유하므로 보조단계로도 넣지 않았다.

02 문서 §7.2 `P` 모듈의 필수 전용 규칙 6개를 모두 반영했다: 계획 단계에서 소스 파일을 수정하지 않음, 사용자 관점 결과와 완료 계약을 먼저 씀, 포함·제외·가정·미확인 구분, 실제 저장소 파일과 명령 조사, 단계마다 검증·실패 처리·복구, 계획이 승인 전제임을 표시.

## 호출·권한·컨텍스트 결정

- 호출: 수동 전용(`disable-model-invocation: true`). 근거 — `plan start`는 새 run 디렉터리 생성·세션 marker 결속·사람 intent_review 요구라는 부작용을 만든다(`preflight.py:293-325`). 02 문서 CC-02가 "되돌리기 어렵거나 상태를 만드는 작업은 수동 호출 전용을 우선 검토"하라고 요구한다. `user-invocable: false`는 쓰지 않는다 — 사용자가 직접 실행해야 하는 커맨드이기 때문이다.
- 컨텍스트: inline. `plan start` 이후 사람이 `intent_summary`를 확인하고 `input_lock_digest`를 보관해야 다음 단계로 갈 수 있어(`preflight.py:311-325`) 대화 중간의 사람 판단이 필수다. CC-09가 "사용자의 중간 판단이 자주 필요하면 fork를 피하라"고 규정한다.
- 서브에이전트: upgrade 모드에서만 `om-plan-official-doc-reviewer`(읽기 전용)를 1회 호출한다. 훅 정책이 보호 중 이 에이전트만 허용한다(`hook_policy.py:166-177`).
- 권한: `allowed-tools`에 항목 9개만 둔다 — Read·Glob·Grep·Write·Edit·Agent 6개 도구와 Bash 패턴 3개(`plan *`·`plan-resume *`·`git status *`). 독립 감사 1차 지적에 따라 절차가 실행하지 않는 `plan-preflight`·`plan-validate`·`plan-session-start`·`git diff` 사전 승인을 제거했다(S-03·CC-06 최소성). 이는 허용 행동을 줄인 것이 아니라 사전 승인을 줄인 것이며, 필요하면 일반 권한 절차로 실행한다. 실제 차단은 검사기 저장소의 `permissions.deny`와 PreToolUse 훅이 담당한다(CC-06·CC-07 분리).

## 규칙 판정 집계

- 원문 규칙: 89 (`C-*` 20, `P-*` 8, `D-*` 12, `E-*` 7, `V-*` 8, `S-*` 7, `M-*` 5, `CC-*` 22)
- 판정: 89 (누락 0, 중복 0, 미판정 0)
- `APPLY` 55 / `TRANSFORM` 13 / `EXCLUDE` 16 / `EXTERNAL` 5
- 안티패턴: 26 판정 (`PASS` 21, `NOT_APPLICABLE` 5 — `A-CC-05`·`A-CC-06`은 fork·Explore/Plan 미사용, `A-CC-07`·`A-CC-08`은 `!` 주입 미사용, `A-CC-14`는 플랫 커맨드 미사용에 근거)
- `EXTERNAL` 5건과 통제 위치: `P-08`(wiring 테스트, planned), `D-09`(`om_workflow.py`·`validate.py`, implemented), `S-07`(`.claude/settings.json`·`run_om_plan_hook.sh`, implemented), `CC-07`(`hook_policy.py`, implemented), `CC-21`(`.claude/settings.json`의 4개 훅 경로, implemented)

## frontmatter 결정

| 필드 | 값 | 유지 이유 | 대안 검토 |
|---|---|---|---|
| `name` | `om-plan` | 디렉터리명과 일치시켜 `/om-plan`을 확정한다(D-01·CC-01). | 생략 시 디렉터리명이 그대로 쓰이나, 이식 대상 저장소에서 이름 근거를 명시적으로 남기려고 유지한다. |
| `description` | 4모드 계획 run + 비적용 조건 | 수동 전용 커맨드의 메뉴 식별과 다른 om 스킬과의 구분에 필요하다(CC-03·D-02). | 없음 — 필수. |
| `argument-hint` | `<모드 또는 요청 설명>` | 인수 계약을 호출 시점에 보여준다(CC-04). | `arguments` 명명 인수는 위치 인수가 셋 이상일 때만 권장되며 이 커맨드는 자유문 하나라 쓰지 않는다. |
| `disable-model-invocation` | `true` | 부작용 있는 커맨드의 자동 발동을 막는다(CC-02·A-CC-03). | `user-invocable: false`는 반대 방향이라 부적합. 둘 다 켜면 호출 불가 상태가 되므로 쓰지 않는다. |
| `allowed-tools` | 항목 9개(도구 6 + Bash 패턴 3) | 절차가 실제로 실행하는 것만 해당 턴에 사전 승인한다(S-03·CC-06). | `Bash(*)` 광범위 허용은 CC-06이 금지한다. 저수준 명령과 `git diff`는 절차가 쓰지 않아 사전 승인에서 뺐다. |

사용하지 않은 필드와 이유: `when_to_use`(description으로 충분하고 합산 길이 제한이 있다), `context`·`agent`·`background`(fork 미사용), `hooks`(훅은 검사기 저장소가 소유), `paths`(수동 전용이라 경로 자동 발동이 무의미), `model`·`effort`(세션 설정을 존중), `metadata`·`license`·`compatibility`(실행 동작을 바꾸지 않음). 버전 의존 필드를 하나도 쓰지 않았으므로 설치 버전 2.1.241에서 동작이 달라질 요소가 없다(CC-19).

## 미확인 사항

`COMMAND_SPEC.yaml`의 `open_questions` 4건과 동일하다.

1. 판정 상태 수 표기 불일치 — 배경 문서는 5가지, 코드 enum은 4가지, 계획 검증 경로는 3가지만 산출. 스킬 본문은 저장소 사실을 따른다. 결정 주체: 사람.
2. R-4 등록 밖 변경 커버리지 게이트가 `/om-plan`에 자동 배선되지 않음. 결정 주체: 사람(Q21).
3. R-1·R-2 기준선 잠금(`custom_baseline` 신뢰) 미해결. 결정 주체: 사람(verify 착수·apply 개방 시).
4. **[해소됨]** `.gitlab-ci.yml`의 exit 2 → CI 성공 래핑을 실측했다. `harness/ci/om_plan_ci.py:324`가 `approval`을 CI 종료코드 0으로 매핑한다. 본문에 기재했다.

## 명세 판정
- 판정: APPROVED
