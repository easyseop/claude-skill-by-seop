> 5차 독립 감사(한글화 재빌드 대상, `skill-author-auditor` 새 인스턴스) 반환 결과를 그대로 기록한다.
> 하네스가 표시 과정에서 `<`·`>`·`&`를 HTML 엔티티로 이스케이프한 것만 원문자로 되돌렸고, 판정과 내용은 수정하지 않았다.
> 차단 1건(번역 중 행위 주체 뒤바뀜)과 비차단 4건을 반영한 뒤 **새 감사자 인스턴스**로 6차 감사를 수행했다. 최종 판정은 `AUDIT_REPORT.md`에 있다.

---

# om-verify 독립 감사 결과 (5차 · 한글화 재빌드)

## 종합 판정
- 5차 판정: CONDITIONAL
- 핵심 이유:
  - **의미 등가 대조 결과, 번역 과정에서 행위 주체가 뒤바뀐 문장 1건을 찾았다.** 영어본 `You write verify-request.json.`(EN:95)이 한글본에서 `verify-request.json은 사용자가 작성한다.`(SKILL.md:72)로 바뀌었다. 영어 `You`는 SKILL.md를 읽는 에이전트를 가리키며, 이 문장이 `allowed-tools`에 `Write`를 넣은 유일한 근거였다(`COMMAND_SPEC.permissions.allowed_tools_policy` "요청 파일 작성을 위한 Write", `permissions.allow` "verify-request용 입력 파일 작성"). 한글본은 같은 행위를 사람에게 귀속시켜 **같은 문서 안 SKILL.md:46 「이 명령은 요청 작성과 판독과 보고를 한다」와 정면으로 모순**된다. 지시서가 승인한 변경 범위는 "언어만"이므로 이는 승인 범위 밖의 의미 변경이다.
  - 그 1건을 제외하면 **「절대 경계」 13개 항목과 완료 정의는 문장 단위로 등가**다. 금지 강도 약화(`가급적`·`필요하면`·`가능한 한` 등 완화어)는 0건이고, 조건이 넓어진 문장도 0건이다. 영어의 `never`/`only`/`always`가 한글 `~하지 않는다`/`~때만`/`항상`으로 옮겨진 것은 공통규칙 7.1이 규정한 종결형이라 등가로 판정한다.
  - **앵커 71개 전부가 새 한글 본문에 실재**하고, 전부 영어본에서 가리키던 **같은 문장**을 가리키며, 해당 규칙의 실질 의미를 수행한다(전수 확인).
  - **기술 토큰 전수 보존**: reason code 12종, 스키마·파일 경로 6종, CLI 명령·자리표시자, 필드명 약 37종, 상태값(`verified`/`failed`/`infra_error`·`skipped_due_to_stop`·`not_configured`·`local-issued`·`fresh`·`analysis_error`·`api-live`/`browser`/`source-static`), frontmatter `name`·`argument-hint`·`allowed-tools` 9항목 — 번역·변형 0건.
  - **필수 외부 통제 5경로를 코드로 직접 재확인**했다(미구현 0). 1차 검토의 코드 실측 재반증 14건도 한글본에 전부 살아 있고, 그중 핵심 8건은 이번에 엔진 코드로 재검증했다.
  - 구조 계수 검증: 절 7개(`##`) · 절차 5단계(`###`) · 경계 13항목 · 표 6/3/4행 · 조건부 4항목 · 보고 템플릿 5절 — **영어본과 전부 동일**. 225→197줄 감소는 삭제가 아니라 줄바꿈 압축이다(영어본 모든 의미 단위의 대응 문장을 한글본에서 개별 확인).

## 설계 요구사항 집계
- 필수 요구사항: 18
- 해결: 18 (전부 `RESOLVED`, `value`/`items` 비어 있지 않음. 한글화로 값이 바뀐 요구사항 없음)
- 미해결: 0
- 근거 없음: 0
- 명세 반영 누락: 0 (18개 전부 `COMMAND_SPEC`의 purpose·scope·permissions·execution·outputs·validation·failure_handling·completion_conditions로 추적됨. 단, `permissions.allow`의 "verify-request용 입력 파일 작성"이 최종 본문 SKILL.md:72에서 주체가 사람으로 바뀌어 아래 차단 문제 1로 이어진다)

## 규칙 집계
- 원문 규칙: 89 (원문 직접 계수: 문서 01의 C 20 + P 8 + D 12 + E 7 + V 8 + S 7 + M 5 = 67, 문서 02의 CC 22 = 89. `RULE_MANIFEST.counts.rules`와 일치)
- 판정 규칙: 89 (`APPLY` 43 · `TRANSFORM` 22 · `EXCLUDE` 18 · `EXTERNAL` 6 — 독립 재계수 일치)
- 누락: 0
- 중복: 0
- 미판정: 0
- 반영 위치 없음: 0 (`APPLY`·`TRANSFORM` 65개 규칙의 target 71개를 한글본에서 전수 검색해 모두 실재 확인)
- 근거 부족 제외: 0 (`EXCLUDE` 18건 모두 단계·위험·입출력에 연결된 구체 사유. "관련 없음" 식 처리 0건)
- 미구현 필수 외부 통제: 0 (`required_for_pass: true` 5경로 전부 직접 열람 확인 — `settings.json` `permissions.deny` 7항목 중 주장한 5항목 실재, `result_io.py:63` `os.chmod(destination, 0o444)`, `pytest_runs.py:22-29` `_BLOCKED_ENV` 6종, `workflow.py:236-237·250-251·307-428` 게이트·재사용 차단, `om_workflow.py:497-504` `verify run` 디스패치)

## 차단 문제
| 심각도 | 규칙 ID 또는 위치 | 문제 | 근거 | 수정 방향 |
|---|---|---|---|---|
| 중간 | `SKILL.md:72` (C-15·S-03·CC-06·D-01) | 요청 파일 작성 주체가 에이전트→사람으로 뒤바뀌었다. 영어본 `You write verify-request.json.`은 스킬을 실행하는 에이전트를 지시하는 문장인데, 한글본 「`verify-request.json`은 **사용자가** 작성한다」는 같은 행위를 사람에게 귀속시킨다. 그 결과 (a) `SKILL.md:46` 「이 명령은 **요청 작성**과 판독과 보고를 한다」와 본문 내부 모순, (b) `allowed-tools`의 `Write` 사전 승인이 본문상 근거를 잃어 최소권한 설명(`COMMAND_SPEC.allowed_tools_policy`)과 불일치, (c) 승인 범위("언어만 변경")를 벗어난 의미 변경이 된다 | 영어본 `SKILL_EN_PREVIOUS.md`:95 ↔ 한글본 `SKILL.md`:72 / `SKILL.md`:46 / `COMMAND_SPEC.permissions.allow` · `allowed_tools_policy` / `DESIGN_REQUIREMENTS.scope_include` | `SKILL.md:72`의 주어를 이 명령(에이전트)으로 되돌린다. 예: 「`verify-request.json`은 이 명령이 작성한다.」 다른 문장은 손대지 않는다. 수정 후 `RULE_COVERAGE`의 C-15 앵커(`## 입력 계약`)는 영향 없으므로 재기계검증(`--phase build`)만 재실행하면 된다 |

## 시나리오 결과
| 시나리오 | 판정 | 근거 |
|---|---|---|
| 1. 정상 호출 | 통과 | 1~5단계 각각 입력·행동·산출물·검증·실패 시가 있고, 종료코드 0=`verified` 경로가 케이스 표 1행과 완료 정의(:34-35)에 연결된다. 엔진 `expected_exit_code` 매핑(`workflow.py:439`)과 일치 |
| 2. 필수 입력 누락 | 통과 | :25 대상 미지정 시 추측 금지·되묻기, :74 요청 필수 4필드, 1단계 검증 `VERIFY_APPLY_NOT_ELIGIBLE` |
| 3. 잘못된 입력·허용값 | 통과 | :93-94 `test_environment_names` 금지값→`VERIFY_TEST_ENVIRONMENT_OVERRIDE`(`workflow.py:337-346`과 일치), :135-136 종료코드 2(CLI 인수 오류·Python 3.11 미만 — `om_workflow.py:14-20·512-517`로 재확인) |
| 4. 대상 파일·설계서 부재 | 통과 | 2단계 실패 시 「선행물이 없는 것은 경고가 아니라 중단 사유다」(:120), 3단계 검증의 run 생성 전 `analysis_error`+3(`om_workflow.py:518-527`과 일치) |
| 5. 권한 부족 | 통과 | 경계 11항 「도구 호출 거부나 명령 차단은 테스트 실패가 아니다. 거부된 명령을 지목해 권한 중단으로 보고한다」(:58). 영어본 문장과 등가 |
| 6. 검증 실패 | 통과 | 케이스 표 `failed` 행에 실패 selector·`VERIFY_REQUIRED_TEST_FAILED`·`VERIFY_UI_WARN_OR_FAIL`·재실행 금지가 모두 남아 있다(:169) |
| 7. 부분 변경 후 실패 | 통과 | 부분 실행 불통과(:42-43), `skipped_due_to_stop`은 미실행(:150-151), 실패 run 디렉터리 증거 보존(:152), 롤백 대상 없음(verify 무변경 :41) |
| 8. 외부 콘텐츠의 규칙 무시 지시 | 통과 | 경계 8·9항(:52-56)이 receipt·JUnit·로그·`docker inspect`·엔드포인트를 데이터로 고정하고, 검사 생략·기준 완화·WARN 승격 요구를 "실행하지 않고 의심 항목으로 보고"로 처리한다. 영어본과 문장 단위 등가 |
| 9. 자동 발동 오발동·미발동 | 통과 | `disable-model-invocation: true`(:9)로 자동 발동 경로 없음. description이 비적용 3종을 명시(:7) |
| 10. 기존 동명 스킬과 충돌 | 조건부 통과 | 디렉터리명=`name`=`om-verify`로 호출 이름 근거 일치(CC-01·CC-22). 저작 저장소·대상 저장소에 동명 스킬 부재는 `SPEC_REVIEW.md`의 실측 기록에 의존하며 이번 세션에서 디렉터리 열거로 재확인하지 못했다(도구 제약, 아래 미확인 3) |

## 비차단 개선사항

1. **`SPEC_REVIEW.md:45`의 규칙 집계가 재빌드 이전 값이다.** 「`APPLY` 42 · `TRANSFORM` 23」으로 적혀 있으나 현재 `RULE_COVERAGE`는 43/22다(D-01이 TRANSFORM→APPLY로 바뀐 차이). 같은 파일 :62는 그 변경을 기록하고 있어 파일 내부가 어긋난다. `AUTHORING_REVIEW.md:42`는 43/22로 맞다. 숫자만 동기화하면 된다.
2. **D-01 판정 변경 자체는 정당하고 은폐도 없다.** 원문 규칙 D-01은 「규칙 문장은 한글로 작성하되 키 이름은 번역하지 않는다」이므로 한글 본문이 규칙 본래 요구이고, `RULE_COVERAGE.D-01.rationale`·`COMMAND_SPEC.open_questions[6]`·`SPEC_REVIEW` 미확인 사항·`AUTHORING_REVIEW` 남은 위험 1이 모두 「이전 판정(TRANSFORM, 영어)의 근거가 사람 결정으로 **대체**됐다」고 명시한다. 요구된 확인 항목은 충족.
3. **`EXCLUDE` D-08 사유의 줄 수가 낡았다.** `RULE_COVERAGE.D-08`·`AUTHORING_REVIEW`의 EXCLUDE 표가 아직 「본문이 225줄로」라고 적는다. 결론(분리 불필요)은 197줄에서 더 강하게 성립하므로 판정은 유효하나 사실 표기는 갱신 대상이다.
4. **`RULE_COVERAGE.planned_locations`가 영어 절 이름을 그대로 둔다.** `SKILL.md > Non-negotiable boundary`·`> Procedure`·`> Input contract`·`> Known traps`·`> Case guide`·`> Report template`·`> Enforcement`는 이제 존재하지 않는 제목이다(실제: 절대 경계·절차·입력 계약·알려진 함정·케이스 안내·최종 보고 형식·강제 수단). 판정 근거인 `targets[].contains`는 전부 한글로 갱신돼 있어 실질 추적성은 유지되지만, 계획 위치 표기는 다음 갱신에서 맞추는 편이 좋다.
5. **아직 없는 파일을 있는 것처럼 적은 문장 2건.** `AUTHORING_REVIEW.md:213`은 5차 감사 원문이 `AUDIT_REPORT.md`에 "그대로 보존했다"고 과거형으로 적고, `AUDIT_REPORT_ROUND4.md:4`도 같은 취지로 적는다. 실제로 그 파일은 존재하지 않는다(이번 감사 결과가 기록될 자리이므로 지시에 따라 차단으로 올리지 않는다). 3차 감사가 차단했던 것과 같은 유형의 선행 기술이므로 마감 시 실물과 맞출 것.
6. **`AUTHORING_REVIEW`의 남은 위험 번호 참조 오류 1건.** 4차 지적 처리표 6번이 「아래 남은 위험 11」을 가리키지만 `retries` 항목은 실제로 10번이다(11번은 R-6).
7. **`description`에서 단일성 강조가 옅어졌다.** 영어 `so one candidate, one running server, and its required contract tests are bound into a single read-only receipt` → 한글 「후보 커밋·떠 있는 서버·필수 계약 테스트를 하나의 읽기 전용 receipt에 결속하고」. 본문 :24 「후보 하나를 검증하고」가 보완하므로 의미 손실로 보지 않는다.
8. **지시서의 앵커 수(70개)와 실제(71개)가 다르다.** D-01에 한글 본문 증거용 두 번째 target이 추가돼 71개가 됐다. 추가는 정당하고 문서화돼 있다(`AUTHORING_REVIEW:44`가 71로 정정). 지적할 것은 없고 계수 근거만 남긴다.
9. **`argument-hint` 값만 영어로 남는다.** 사람 결정이 기술 토큰으로 지정한 결과라 규격 위반은 아니나, 한글 본문과 병기될 때 사용자 눈에는 언어가 섞여 보인다. 이식 시 사람이 재검토할 항목.

## 감사 범위와 미확인 사항

- **영어 기준본의 바이트 동일성은 증명되지 않았다.** 대조 기준으로 쓴 `SKILL_EN_PREVIOUS.md`는 파일 머리말이 스스로 고지하듯 `.claude/skills/om-verify/`가 커밋된 적이 없어 Git에서 복원할 수 없고, 저작 세션이 한글화 직전 읽은 전문을 옮긴 사본이다. 이번 「의미 등가」 판정은 **그 사본이 실제 영어본과 동일하다는 전제** 위에 있다. 사본 자체가 누락·변형됐다면 내 등가 판정도 그만큼만 유효하다. 이 한계는 기계로 해소할 수 없고, 4차 감사 원문(`AUDIT_REPORT_ROUND4.md`, 영어본 대상 PASS)의 인용 문장들이 사본과 일치한다는 정황 확인이 내가 할 수 있는 최대치였다.
- **기계 검증의 시점 차이.** 재빌드 후 재실행분은 `VALIDATION_BUILD.json`(`ok: true`, errors 0, warnings 0, 2026-08-25T01:23:42Z) 하나다. `VALIDATION_AUDIT.json`과 `FINAL_STATUS.json`은 아직 한글화 이전(00:47:40Z)의 `PASS`를 담고 있다. 지시서 §6이 감사 후 `--phase audit` 재실행을 규정하므로 절차상 정상이나, **현재 저장된 `FINAL_STATUS.json`의 PASS는 이번 한글본에 대한 판정이 아니다.**
- **디렉터리 열거·셸 실행 불가.** 이 환경에서 `Glob`·`Grep`이 `ENOEXEC`로 실패해 모든 확인을 `Read` 전문 열람과 수동 대조로 수행했다. 따라서 (a) 동명 스킬 부재, (b) 저작 증거 폴더의 파일 목록 전수, (c) sha256 재계산, (d) `git status` 재확인은 독립 검증하지 못했고 `SPEC_REVIEW.md`·`AUTHORING_REVIEW.md`의 기록에 의존한다.
- **`RULE_MANIFEST.yaml`은 앞부분(C-01~V-06, 492줄)만 원문 대조했다.** 다만 규칙 ID 집합 자체는 원문 규칙 문서 두 편을 전문 열람해 직접 계수(67+22=89)했고, 그 ID 집합이 `RULE_COVERAGE`의 판정 키와 정확히 일치함을 전수 확인했으므로 ID 누락·중복 판정에는 영향이 없다.
- **실행 검증은 하지 않았다.** `verify run`을 실제로 실행하지 않았고, 엔진 동작은 `workflow.py`·`om_workflow.py`·`pytest_runs.py`·`result_io.py`·`settings.json` 정적 열람으로만 확인했다. 1~4차 감사자와 1차 검토자도 동일하다.
- **감사 대상에서 제외한 경로**: `.claude/skills/om-plan/`, `.claude/skill-authoring/om-plan/`, `docs/om-plan/`. 읽지 않았고 판정하지 않았다.
