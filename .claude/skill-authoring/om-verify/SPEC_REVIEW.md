# om-verify 명세 검토

## 조사 범위

- 저작 저장소(`/Users/seop/claude-skill-by-seop`): `CLAUDE.md`·`CLAUDE.local.md`·`.claude/rules/`·`.claude/settings*.json`·`.claude/commands/` 부재를 실측했다. **init 시점(2026-08-24) 실측 기준** `.claude/skills/`에는 `claude-skill-author`만, `.claude/agents/`에는 `skill-author-auditor.md`만 있었다. 동명 `om-verify`가 없으므로 `operation`은 `new`다. (이후 이 작업이 `om-verify`를, 다른 세션이 `om-plan`을 추가했으므로 현재 목록은 다르다.)
- 대상 런타임(검사기 저장소 `/Users/seop/Documents/Codex/2026-07-24/sites-plugin-sites-openai-bundled/work/kb-datacatalog-upgrade-checker-om-plan-cli`): HEAD `82be68e733`, 브랜치 `codex/om-plan-verified-gates-20260820`, `git status --porcelain` 0줄. `CLAUDE.md`·`README.md`·`.claude/settings.json`·`.claude/skills/om-apply/SKILL.md`·`.claude/agents/`·`.claude/hooks/`를 읽었다. 여기에도 `om-verify` 스킬은 없다.
- 엔진·CLI 실측: `harness/om_workflow.py`(CLI 인자·종료코드), `harness/acgh/verifycore/{workflow,testruns,pytest_runs,result_io,schema}.py`, `harness/acgh/integrations/om/verify.py`, `harness/acgh/verifycore/schema/` 5종, `harness/acgh/applycore/schema/apply-result.schema.json`, `harness/tests/test_om_verify_counterexamples.py`, `harness/tests/test_claude_wiring.py`.
- 정본 문서: 83(부록 A) · 76 · 81 · 24.
- `claude --version` = `2.1.241 (Claude Code)`.
- 병렬 세션 관찰: init 시점 `git status --short` 출력 0줄. 타 세션의 `om-plan` 경로 변경은 관찰되지 않았고, 관찰되더라도 판정 대상이 아니다.

## 설계 입력 검토

- 필수 요구사항 수: 18
- 해결 수: 18
- 미해결 수: 0
- 설계서·호출문·저장소 근거: 설계서 `docs/om-verify/OM_VERIFY_DESIGN.md`(20개 섹션 전부 작성), 저작 지시서 `지시서_om-verify_스킬저작_20260824.md`, 내용 요구 정본 `83_Codex_SKILLmd_작성지시_20260824.md`. 모든 요구사항의 `sources`에 스키마·엔진 코드·CLI의 실측 경로를 함께 연결했다.
- 설계 입력 판정: APPROVED

## 대상 스킬 프로필

- 명령: `/om-verify`, 설치 경로 `.claude/skills/om-verify/SKILL.md`(이식 후 검사기 저장소의 같은 경로).
- 목적: `/om-apply` 인계 후보를 검사기 CLI로 실행·검증해 `verified`/`failed`/`infra_error`로 결속하고, 산출물을 바꾸지 않고 해석해 보고한다.
- 배포 대상: **Claude Code 전용**(CC-13). 근거: `disable-model-invocation`·`argument-hint`·`allowed-tools`를 사용하며, 같은 저장소의 `claude-skill-author/SKILL.md`가 동일 필드를 실제로 쓴다.
- 산출물 구조: `SKILL.md` 한 파일. `references/`·`scripts/`·`assets/`·`evals/`를 만들지 않는다(D-08·CC-12·A-CC-10).
- 본문 언어: **한글**(사람 결정 2026-08-25). 기술 토큰(reason code·파일 경로·스키마명·CLI 명령·필드명·상태값·frontmatter의 `name`·`argument-hint` 값)은 원문을 유지한다. 영어본(225줄)은 1차 검토 승인본이며 이번 재빌드는 의미 등가를 유지한 언어 변경이다.

## 단계 판정

- 주단계: **V**(검증·리뷰). 근거: 이 스킬은 요구사항을 실행 가능한 판정으로 바꾸는 것이 아니라 이미 고정된 계약 테스트를 실행하고 게이트 판정을 해석·보고한다. `V` 모듈의 필수 전용 규칙("실행하지 않은 테스트를 근거로 통과 판정하지 않는다", "양성 사례와 반례를 함께 확인한다", "판정만 하는 리뷰인지 구분한다")이 그대로 대상 행동이다.
- 보조단계: **R**(조사·이해) — 인계·receipt·컨테이너 상태를 읽기 전용으로 실측하고 확인/추론/미확인을 구분한다. **D**(문서화·보고) — 상태별 사람 보고와 고정 보고 템플릿을 만든다.
- 채택하지 않은 단계: `I`·`F`·`O`는 코드·환경을 바꾸므로 제외 범위와 정면 충돌한다. `P`는 `/om-plan`, `X`는 파이프라인 오케스트레이션(향후 `/om-report`)의 몫이다. `G`는 규칙 생성 단계라 CC-20에서 비적용으로 판정했다.

## 호출·권한·컨텍스트 결정

- 호출 정책: **수동 전용**(`disable-model-invocation: true`). 근거 CC-02·A-CC-03 — `verify run`은 호출 즉시 새 run 디렉터리를 만들고 pytest·docker 조회를 실행하는 부작용 명령이다. `user-invocable: false`는 함께 쓰지 않는다.
- 인수: 자유문 대상 지정 하나(`argument-hint`). 명명 위치 인수를 쓰지 않는다(위치 인수 3개 미만, CC-04). 대상 누락 시 추측하지 않고 되묻는다. 인수를 셸 문자열에 결합하지 않는다.
- 실행 컨텍스트: **inline**, `background: false`, 서브에이전트 없음. 근거 CC-09 — 인계 재발행·escalation·waiver 판단에 사람의 중간 결정이 필요하다.
- 부작용 등급: 중간(새 run 디렉터리 생성·테스트 실행·docker/HTTP 조회). 코드·관리파일·등록자료·기존 receipt는 불변이며 커밋·푸시·배포는 하지 않는다.
- `allowed-tools`: `Read`·`Glob`·`Grep`·`Write`와 `Bash(python harness/om_workflow.py verify run *)`·`Bash(git status)`·`Bash(git status *)`·`Bash(git diff)`·`Bash(git diff *)`를 사전 승인한다(S-03·CC-06). `Write`는 `verify-request.json`을 새로 작성해야 하므로 포함하고, `Edit`은 기존 산출물 편집이 금지 행동이므로 넣지 않는다. `Bash(*)`도 넣지 않는다. (이 항목은 1차 독립 감사 지적 5·6번을 반영해 갱신했다.) 이는 제한이 아니라 한 턴 사전 승인이며, 실제 차단은 대상 저장소 `permissions.deny`와 검사기의 fail-closed 게이트가 담당한다(CC-07·S-07).

## 규칙 판정 집계

- 원문 규칙 89개 / 판정 89개 / 누락 0 / 중복 0 / 미판정 0.
- `APPLY` 43 · `TRANSFORM` 22 · `EXCLUDE` 18 · `EXTERNAL` 6. (2026-08-25 한글화 재빌드에서 D-01이 TRANSFORM→APPLY로 바뀐 값이다.)
- 안티패턴 26개: `PASS` 21 · `NOT_APPLICABLE` 5(A-CC-05·06·07·08·14 — fork·서브에이전트·`!` 주입·플랫 커맨드를 쓰지 않기 때문).
- `EXTERNAL` 6건(D-09·V-05·S-01·S-07·CC-07·CC-21)은 모두 대상 런타임 저장소의 실재 파일을 지목한다. 이 중 CC-21의 `UserPromptExpansion` 항목만 `state: planned`(미구현)이며 `required_for_pass: false`로 두고 남은 위험으로 보고한다.

## frontmatter 결정

| 필드 | 사용 | 이유 |
|---|---|---|
| `name` | 사용 | 디렉터리명과 일치시켜 `/om-verify` 호출 이름의 근거를 만든다(CC-01·D-01). 값은 기술 토큰이므로 한글화 대상이 아니다. |
| `description` | 사용 | 수동 전용이므로 결과(3상태 receipt)·부작용(새 run 생성·계약 테스트 실행)·비적용 조건을 함께 쓴다(CC-03·D-02). 모델이 호출 판단에 쓰는 필드이므로 한글로 쓰되 `om-verify`·`verify` 등 검색 키워드를 포함한다. |
| `argument-hint` | 사용 | 대상 지정 방법을 호출 전에 보여준다(CC-04·A-CC-04). 값은 기술 토큰이므로 원문을 유지한다. |
| `disable-model-invocation` | 사용 | 부작용 명령의 자동 발동을 막는다(CC-02·A-CC-03). |
| `allowed-tools` | 사용 | 주단계에 필요한 최소 도구만 한 턴 사전 승인한다(S-03·CC-06). |
| `when_to_use`·`context`·`agent`·`background`·`user-invocable`·`disallowed-tools`·`paths` | 사용 안 함 | 실행 동작을 바꾸지 않거나(수동 전용·inline 기본값과 동일) 다음 사용자 메시지에서 해제돼 영구 차단 수단이 되지 못한다(CC-05·CC-07·A-CC-09). |

## 미확인 사항

- **[해소됨 2026-08-25]** 규칙 D-01의 "규칙 문장은 한글로 작성한다"와 이식 대상 저장소의 영어 사실이 충돌하던 항목. 사람 결정으로 **본문 언어를 한글로 통일**한다(사내 GitLab에서 한국어 조직이 직접 읽는 문서, om-plan과 일관). om-apply도 Codex 단계에서 한글화하며 `test_claude_wiring.py`의 단언 문구도 이식 시 한글로 바꾼다(Codex 작업). `RULE_COVERAGE`의 D-01 판정을 TRANSFORM(영어 예외)에서 **APPLY(한글 본문)**로 갱신했다. 더 이상 미결이 아니다.
- 대상 저장소의 `UserPromptExpansion` matcher가 `^(om-plan|om-resume)$`이라 사용자가 직접 입력한 `/om-verify` 확장은 훅 검사를 받지 않는다. 이식 시 matcher 확장 여부는 사람 결정 사항이다.
- `/om-report`(4단계) 착수, R-6(V-1~V-3 임시 확정) 재조정, 보호된 CI receipt 서명, test-agent `meta.run_id` null, GitLab CI의 verify 테스트 미실행은 모두 이 스킬 밖의 미결정 사항으로 `COMMAND_SPEC.open_questions`에 기록했다.

## 명세 판정
- 판정: APPROVED
