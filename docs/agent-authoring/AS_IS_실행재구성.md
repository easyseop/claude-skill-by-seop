# AS-IS 실행 재구성 — om-plan·om-verify 스킬 저작 과정 (실물 근거 기반)

작성일: 2026-08-28. 작성자: Claude(기록·검증 세션).
방법: 기억이 아니라 실물 확인 — 이 저장소의 git 이력·파일 mtime·증거 파일 전수 열람, 세션 기록(jsonl) 문구 검색, 패키지 ZIP 내용물 실측. 확인하지 못한 것은 마지막 절에 명시한다.
범위 주의: 실제 저작(설계서 완성→full 절차→감사)은 **이 세션이 아니라 별도의 저작 세션 2개**(om-plan용·om-verify용 병렬)가 수행했다. 본 문서는 그 세션들이 남긴 산출물·증거·git 이력으로 재구성한 것이다.

---

## 1. 입력된 사용자 요구사항 (원문 실측)

세션 기록에서 직접 확인한 사용자 원문:

- 궁극 목표: "**궁극적인 목표는 각 과정을 스킬로 만들어 정형화된 오픈메타 운영 하네스 템플릿을 만드는 것**"
- 대상 확정(교정): "**먼소리야 plan om apply omverify각각 스킬로만드는거아니었어?**" — 3종(om-plan·om-apply·om-verify) 각각 스킬화가 요구임을 확정
- 메타스킬 신뢰 확인: "**그리고 저 스킬을 만드는 스킬에대한 설계가 잘 되어있긴해?**", "**아니 스킬만드는 스킬로 만들엇잖아 각 ㅡ들을**"

세션 요약에만 남은 원문(압축으로 원문 전문 유실 — 재구성 근거는 당시 세션 요약):

- 최초 제공: "우리 스킬저장소있잖아... 이걸 설치하고... 스킬명세서와 스킬을 가지고 한번 확인해줄래?" + 메타스킬 원스톱 지시서·ZIP 경로 제공
- 이름 결정: "스킬이름은 omplan이 아니라 다른걸로 해줘" → `om-plan`
- 언어 결정: "한글로 통일하는게좋긴한데" → 한글 통일(재빌드 발생)

물적 제공물(파일 실물 확인):

- `claude-skill-author-package_20260824_v1.1.zip` (80,321B, 저장소 루트)
- `CLAUDE_원스톱_설치_설계_스킬생성_지시서_omplan_v1.1.md` — 사용자 제공 원스톱 지시서(대상 예시가 `omplan`·`docs/openmetadata/` 경로인 **다른 프로젝트용 템플릿**이었음)

**확인된 사실**: 사용자 자연어 원문을 원형 그대로 보존하는 파일(`SOURCE_REQUEST.md` 류)은 **존재하지 않는다**(전체 glob 실측 0건). 원문은 지시서로 번역된 시점부터만 파일로 추적 가능하다.

## 2. 실제 수행 순서 (git 이력 + 파일 mtime + 검증 JSON 시각 실측)

| 시각(KST) | 사건 | 근거 |
|---|---|---|
| 08-24 21:45 | 메타스킬 설치 + om-plan 저작 지시서 v1 커밋 | git `ccc3f3a` |
| 08-24 21:47 | om-verify 저작 지시서 v1 커밋 | git `cf5f571` |
| 08-24 21:52 | **지시서 v2**(자기완결·병렬 세션 대응) 커밋 — 이후 v2가 실사용본 | git `e4411cd` |
| 08-24 22:05 | 저작 세션 init 실행(규칙 인벤토리 생성) | `RULE_MANIFEST.yaml` mtime |
| 08-24 밤~08-25 오전 | 설계서 2종 작성·감사 라운드 반복 | ROUND 파일들 mtime |
| 08-25 10:22 | om-plan spec 검증 ok | `VALIDATION_SPEC.json` validated_at 01:22:06Z |
| 08-25 10:54 | om-verify spec 검증 ok | 동 01:54:42Z |
| 08-25 09:55 | Claude 1차 검토 커밋(om-verify 승인/om-plan 조건부) | git `7083db9` |
| 08-25 10:14~10:55 | 사람 결정(한글 통일) 반영 재빌드 지시·재검증 승인 | git `4c8b296`·`c4e6283` |
| 08-25 12:56 | 양쪽 build 검증 ok (한글본·87 반영 최종) | VALIDATION_BUILD 03:56:36Z |
| 08-25 13:05 | 양쪽 audit 검증 ok, `FINAL_STATUS: PASS` | VALIDATION_AUDIT·FINAL_STATUS 04:05:01Z |
| 08-25 19:25 | 산출물·증거 사슬 보존 커밋(단일) | git `9fd6f38` |

이후(이 저장소 밖): Codex 2차 검토 85(BLOCK) → 87(P0 수정·실측) → 확인 감사 PASS(본 저장소 최종 `AUDIT_REPORT.md` 2종) → 검사기 저장소 이식(90) → MR merge. 근거: skill_develop/om_plan/85·87·90 및 본 저장소 최종 감사 보고 2종.

## 3. 단계별 입력·판단·산출물

### (0) 지시서 작성 — 본 검증 세션 수행
- 입력: 사용자 원스톱 지시서 v1.1(다른 프로젝트용 템플릿) + 사용자 자연어 요구 + skill_develop 정본들.
- 판단(자체): 템플릿을 이 프로젝트에 맞게 재작성 — 대상 저장소를 검사기 저장소로 분리 지정, 참고자료 절대경로화, 병렬 세션 상호 불간섭 규칙, `--design` 3문서(설계서+지시서+83 정본) 지정.
- 산출: `지시서_om-plan_스킬저작_20260824.md`, `지시서_om-verify_스킬저작_20260824.md` (v2).

### (1) 설계서 작성 — 저작 세션 수행
- 입력: 지시서 v2 §4("full 진입 전에 이 세션이 직접 완전 작성") + `DESIGN_INPUT.template.md`(20섹션) + 검사기 저장소 실측.
- 산출: `docs/om-plan/OM_PLAN_DESIGN.md`(35.6KB)·`docs/om-verify/OM_VERIFY_DESIGN.md`(35.0KB) — 템플릿 20섹션 전 항목 실측 확인(§1 개요~§20 미결정 사항).

### (2) init → 18요구 → 89규칙 전수판정 → COMMAND_SPEC → spec
- 산출: `DESIGN_REQUIREMENTS.yaml`(source_documents 3건 **sha256 고정**, 18개 전부 RESOLVED, status: APPROVED), `RULE_MANIFEST.yaml`(104KB)·`RULE_COVERAGE.yaml`, `COMMAND_SPEC.yaml`, `SPEC_REVIEW.md`.
- 기계 판정: source_rules 89 / classified 89 / missing·unknown·duplicate 0, requirements 18/18 (VALIDATION_SPEC 실측).

### (3) SKILL.md 작성 → build → 독립 감사 → audit
- 산출: `.claude/skills/om-plan/SKILL.md`(30.4KB)·`om-verify/SKILL.md`(13.5KB), `AUTHORING_REVIEW.md` 2종, 감사 보고 om-plan 5회분·om-verify 7회분(ROUND 파일 실측).
- 감사 이력(보고서 실측): om-plan 1차 차단 2건(digest 미제공 시 approval 도달 가능 등) → 2차 차단 3건(1차 조치가 만든 오류 포함 — "보호 세션 중 git status는 훅이 거부") → 3·4차 → PASS → 87 반영 확인 감사 PASS. om-verify 1~6차 → PASS → 확인 감사 PASS.
- 한글화 진위 증명: `SKILL_EN_PREVIOUS.md`·`SKILL_EN_REVIEWER_COPY.md` 독립 사본 대조(커밋 `c4e6283` 메시지 및 파일 실물).

## 4. 사용한 파일과 명령

읽기(지시서 v2 명시 + 감사 보고 "확인 범위" 실측 합성): 검사기 저장소의 `harness/om_workflow.py`(plan 계열 6개 서브커맨드), `plancore/schema/` 5종, `.claude/skills/om-apply/SKILL.md`, `CLAUDE.md`·`README.md`, `hook_policy`·`hook_cli`·`config.py`(:7 ID 정규식)·`collectors.py`(:545-610)·`preflight.py`·`schema.py`·`settings.json` / 정본 83(부록 A)·24 결정기록·공유정리 / 메타스킬 SKILL.md + references 4종 + 템플릿.

명령(지시서 규격 + 검증 JSON으로 실행 사실 입증, **명령행 원문 로그는 미보존**): `python3 tests/run_tests.py`·`./install.sh`(08-24 설치), `python3 -m py_compile`(스크립트 3종), `init_authoring.py --project-root … --target om-plan --mode full --common-rules … --claude-rules … --design ×3`, `validate_authoring.py --phase spec|build|audit`(각 phase의 VALIDATION_*.json이 실행 증거).

## 5. 패키지 기본 기능 vs 원스톱 지시문이 추가한 부분

**패키지(ZIP 실측)가 제공**: 메타 SKILL.md(0~4단계 절차)·references 4종(design-input-guide, authoring-workflow, schemas, audit-rubric)·assets 템플릿 6종·스크립트 3종(init/validate/stop_gate)·**`.claude/agents/skill-author-auditor.md`(감사자 에이전트 정의)**·자체 테스트·install.sh.

**원스톱 지시서(v1.1)가 추가**: 설치 전 안전검토(네트워크 0·Git 쓰기 0 확인)→테스트→설치 절차, "설치 직후 슬래시 미표시여도 중단 금지, SKILL.md 직접 로딩" 우회, **0단계-7 멈춤 함정 회피**(설계서를 full 진입 전에 완성시켜 "초안만 만들고 중단" 분기를 타지 않게 함), full 연속 수행 강제와 단계 간 게이트("spec 전 SKILL 작성 금지…"), 커밋 금지, 최종 보고 형식.

**지시서 v2(본 세션 작성)가 추가**: 병렬 세션 불간섭 규칙, **89규칙 판정의 대상 저장소를 스킬 저장소가 아닌 검사기 저장소로 지정**, 참고자료 절대경로+실측 강제("CLI 인자·exit는 코드 실측, 추측 금지"), 감사 FAIL 시 새 감사자로 최대 2회, 3중 design 문서와 83 부록 A 정본 지정.

## 6. 자체 판단한 항목과 근거

- 지시서 v2로의 재작성 범위(위 5절) — 근거: v1.1은 다른 프로젝트 경로·단일 세션 전제여서 그대로 쓰면 실패.
- 설계서 20섹션의 구체 서술(승인 지점·실패 처리·반례) — 저작 세션이 검사기 실측으로 채움. 근거: DESIGN_REQUIREMENTS의 sha256 3원천 + 감사의 역방향 검증 통과.
- 규칙 89건의 APPLY/TRANSFORM/EXCLUDE/EXTERNAL 판정 — 저작 세션 판단, 단 전수판정·중복 0을 기계 검증이 강제.
- 사람에게 넘긴 항목(자체 판단하지 않음): 스킬 이름(`om-plan`), 언어(한글 통일), 최종 채택·이식 여부(3중 검토: Claude 1차 → 사용자 → Codex 2차).

## 7. 근거 없이 기본값을 둔 항목이 있었는가

- 설계 템플릿 규칙이 빈 항목을 불허(`없음 — <이유>` / `미확인 — <필요 출처>` 강제)하고, 감사 8단계가 SKILL.md의 모든 의미 문장을 요구·사실·규칙에 **역방향 연결**로 검사했다. 최종 감사 잔존은 비차단 2건(문구 정밀화 수준)뿐.
- 단, "0건"을 단정할 수는 없다 — 감사도 LLM이며, 4차 시점 원본 부재로 바이트 diff 불가 구간은 합성 증거(줄 수·앵커 동수·인용문 잔존)로 대체됐음이 감사 보고에 정직하게 기록돼 있다.

## 8. Agent.md(skill-author-auditor) — 필요 판단과 강제 여부

- **패키지 ZIP에 동봉되어 설치로 들어온 것이다**(ZIP 내부 `claude-skill-author-package/.claude/agents/skill-author-auditor.md` 실측). 작업 중 자체 판단으로 생성한 것이 **아니다**.
- 강제 수준: 원스톱 지시서의 설치 필수 파일 목록에 포함(설치 검증 대상). 다만 기계 검사(validate_authoring)가 이 파일의 존재를 강제하는지는 미확인 — 지시서 차원의 강제로 확인됨. 지시서 v2는 "없으면 general-purpose 읽기 전용" 폴백까지 규정.
- 정의 내용: 읽기 전용(tools: Read·Glob·Grep, permissionMode: plan), 독립 감사 12절차, PASS/CONDITIONAL/FAIL 판정 형식.

## 9. spec / build / audit 실제 검사 결과 (JSON 실측)

| 대상 | spec | build | audit | FINAL_STATUS |
|---|---|---|---|---|
| om-plan | ok (08-25 01:22:06Z) | ok (03:56:36Z) | ok, verdict PASS (04:05:01Z) | PASS |
| om-verify | ok (01:54:42Z) | ok (03:56:36Z) | ok, verdict PASS (04:05:01Z) | PASS |

공통 counts: source_rules 89 / classified 89 / missing 0 / unknown 0 / duplicate 0 / design_requirements 18/18. errors·warnings 전부 [].

## 10. 최종 산출물이 사용자 원문을 반영했는지 확인한 방법

1. 설계 원천 sha256 고정(DESIGN_REQUIREMENTS.source_documents 3건)
2. 설계 요구 18개 전부 RESOLVED + 전체 APPROVED
3. 규칙 89건 전수판정(누락·중복·미판정 0 — 기계 검증)
4. 독립 감사의 역방향 연결 + 앵커 전수 실재 대조(om-plan 76건·om-verify 71건)
5. 한글화는 영어 원본 독립 사본과 대조해 "번역이 원본 진위를 훼손하지 않음" 별도 증명
6. 조직 검토 3중(Claude 1차 → 사용자 결정 → Codex 2차 85/87) 후 이식

**구조적 한계**: 이 사슬의 출발점은 지시서이지 사용자 자연어 원문이 아니다. "사용자 원문 → 지시서" 번역 단계는 사람(사용자)의 검토 외에 어떤 기계·감사 장치도 거치지 않았다.

## 11. 최종 생성 파일 목록 (실측)

- 스킬: `.claude/skills/om-plan/SKILL.md`, `.claude/skills/om-verify/SKILL.md`
- 설계: `docs/om-plan/OM_PLAN_DESIGN.md`, `docs/om-verify/OM_VERIFY_DESIGN.md`
- 증거(각 대상별): DESIGN_REQUIREMENTS·RULE_MANIFEST·RULE_COVERAGE·COMMAND_SPEC·SPEC_REVIEW·AUTHORING_REVIEW·AUDIT_REPORT(+ROUND 4~6회분)·VALIDATION_{SPEC,BUILD,AUDIT}.json·FINAL_STATUS.json, om-verify 추가 2종(SKILL_EN_PREVIOUS·SKILL_EN_REVIEWER_COPY)
- 지시·검토 문서: 지시서 2종(v2)·한글화 지시서·검토요청/결과 4종·`docs/om-plan/INBOX_Claude검토_…`
- 현재 git 상태: clean(미커밋 0) — 본 재구성 문서 2건 제외. om-apply는 이 저장소 산출물이 아님(기존 영어본을 검사기 저장소에서 한글화).

## 12. 확인하지 못한 사항

1. 저작 세션 2개의 대화 로그 — 별도 세션이며 이 저장소에 없음. 명령행 원문·중간 시행착오는 재구성 불가.
2. 설계서 "최초 생성"의 정확한 시각 — 산출물이 단일 보존 커밋(9fd6f38)이라 git 이력 없음. mtime은 최종 수정 시각(08-25 10:21)만 제공.
3. 사용자 최초 메시지(ZIP·지시서 제공 메시지)의 전문 — 본 세션 컨텍스트 압축으로 원문 유실, 세션 요약으로만 남음.
4. validate_authoring이 감사자 에이전트 파일 존재를 기계적으로 강제하는지(스크립트 내부 미열람).
5. 지시서 v1 → v2 개정을 촉발한 대화의 세부.
