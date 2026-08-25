# om-plan 독립 감사 결과 — 4차 (2026-08-25, 새 인스턴스, 읽기 전용)

(사람 승인 예외 재감사 — 결정기록: skill_develop/om_plan/24. 감사자 반환 원문 그대로 수록, 판정 무수정.)

## 종합 판정
- 판정: PASS
- 핵심 이유: 3차 차단 2건이 검사기 코드 실측과 정확히 일치하는 방식으로 해소됐다. (A) 7단계의 `STATE_ROOT`·`SESSION_ID` 출처가 `plan start` stdout JSON의 `state_root`·`session_id`로 교체됐고, 이 두 키는 `om_workflow.py`의 `start_plan_run` 반환 dict(264–270행 부근)에 실재하며 `dispatch`가 stdout으로 출력한다. `plan-resume`이 두 값을 `required=True` 인수로만 받는다는 사실(373–376행)과도 정합한다. (B) 미등록 `/om-resume` 의존이 SKILL.md에서 0건으로 제거됐고, marker 재생성 방아쇠가 `/om-plan` 재호출로 교체됐다 — `hook_cli.py` 123–133행의 PreToolUse Skill 분기가 marker 부재 시 `create_session_marker`를 호출함을 직접 확인했다(인용 줄번호까지 정확). marker 없는 직접 호출의 두 실패 경로(훅 거부 문자열, `SESSION_MARKER_INVALID`)도 `hook_cli.py`·`hook_policy.py`·`markers.py:70-86`·`resume.py`와 문자열 수준에서 일치한다. SKILL.md 7단계 ≡ `COMMAND_SPEC.yaml:267` ≡ `DESIGN_REQUIREMENTS.yaml:237`로 3파일 정합. 비차단 수정 3건도 사실과 일치하고, 기계검증 spec·build `ok:true`(수정 후 시각 01:09:52Z = 파일 mtime 10:09 KST와 정합), 필수 외부 통제 전부 실재·동작 확인, APPLY/TRANSFORM 68규칙의 targets 76건 전수 실재 확인. 차단 문제 0건.

## 설계 요구사항 집계
- 필수 요구사항: 18 / 해결: 18 (`resolved_design_requirements: 18`, `status: APPROVED`) / 미해결: 0
- 근거 없음: 0 — 수정 문장의 근거(`om_workflow.py:264-270`·`:373-376`, `hook_cli.py:123-133`, `validate.py:45-67`, 83 문서 작업 3, 지시서의 참고 저장소 읽기 전용 조항) 전부 원문 재확인, 인용 정확.
- 명세 반영 누락: 0건 신규 (3차의 `COMMAND_SPEC.inputs` 보강 1건은 #9로 Codex 단계 이월 — 이월 기록 확인)

## 규칙 집계
- 원문 규칙: 89 / 판정: 89 (APPLY 55 / TRANSFORM 13 / EXCLUDE 16 / EXTERNAL 5 — 직접 계수) / 누락 0 / 중복 0 / 미판정 0
- 반영 위치 없음: 0 — 표본 15개 요구를 넘어 68규칙의 targets `contains` 76건 전부를 스크립트로 최종 SKILL.md와 대조, 전건 실재. 의미 보존은 18건 표본(C-03·C-08·C-12·C-16·C-18·C-19·D-06·D-12·E-06·E-07·V-04·V-08·S-04·S-06·M-05·CC-02·CC-06·CC-16)으로 확인. 이번 수정 문장을 anchor로 삼는 규칙 target 0건 — coverage 표류 없음
- 미구현 필수 외부 통제: 0 — `required_for_pass:true` 6건 실재·핵심 동작 직접 확인. P-08은 `planned`·`required_for_pass:false`로 정직 표기

## 차단 문제

없음.

## 중점 항목별 판정 상세

1. **차단 A 해소 = 확인.** `plan start`는 stdout JSON에 `state_root`·`session_id`를 실제로 담고, `plan-resume`은 두 값을 필수 인수로만 받아 환경변수를 참조하지 않는다. "훅 주입 값은 CLI가 스스로 참조"라는 새 서술도 정확(`default_plan_state_root`·`select_plan_session_id`가 env를 읽는 곳은 start/check 경로뿐). 같은 세션 재호출 시 훅이 만드는 새 marker는 동일 session_id·동일 state_root 경로에 생기므로 stdout 값으로 `session_marker_path`가 그 marker를 정확히 찾는다 — 경로가 코드로 닫힌다.
2. **차단 B 해소 = 확인.** `/om-resume` 참조는 SKILL.md에서 완전 제거(잔존 2건은 COMMAND_SPEC:114·RULE_COVERAGE의 settings.json matcher 사실 기술 — 실재하는 저장소 사실이라 문제없음). 재개 전체 경로를 코드로 추적: Skill 재호출 → hook_cli.py:123-133 marker 생성 → `decide_pre_tool_use`가 미결속 marker에서 `plan-resume`을 허용 → `bind_run` → `proposal_revision_allowed`. "새 run 시작 금지, 기존 RUN_DIR" 명시도 3파일 동일.
3. **비차단 3건 = 사실 일치.** ① run-request "사람이 보호 범위 밖에서 준비"는 1단계·hook_policy Write 거부와 정합. ② `plan-validate` digest 생략 → `analysis_error`(3)는 코드로 확정(`_trusted_input_binding` issues → ANALYSIS_ERROR), CLI help 문구 원문 일치. ③ P-08 정정 정확: 83 문서 작업 3이 wiring 보강을 요구하고, 저작 지시서가 검사기 저장소 쓰기를 금지.
4. **새 모순 = 산출물·명세 체인 0건.** (설계서 잔존 낙후는 비차단 #1로 별도 — 아래)

## 시나리오 결과

정상 호출 / 필수 입력 누락 / 잘못된 입력 / 대상 부재 / 권한 부족 / 검증 실패 / 부분 변경 후 실패 / 인젝션 / 자동 발동 / 동명 충돌 / (추가) block 재개 경로 — **전부 통과** (각각 코드 실측 근거, 특히 block 재개는 marker 생성→허용→결속→재검증까지 코드로 끝까지 추적).

## 비차단 개선사항

1. 설계서(OM_PLAN_DESIGN.md) §13 7단계와 plan-validate 표현이 구 문구로 잔존 — 재저작 시 차단 B 재발 위험. 설계서 정정 또는 open_questions 등재 필요.
2. COMMAND_SPEC의 plan-validate 서술이 구 문구("verified=false...")로 남음 — SKILL.md의 정밀 표현과 불일치.
3. 7단계 재개 절차는 같은 세션 재호출을 암묵 전제 — 새 대화 재개 시 옛 session_id로 `SESSION_MARKER_INVALID` 안전 실패하나 미명시.
4. 검토결과서의 "이식 후 실기동 스모크 테스트 필수"(훅 필드명 불일치 가능성)가 AUTHORING_REVIEW 남은 위험에 미승계.
5. 3차 비차단 이월 6건(#2·#4·#5·#6·#8·#9)은 기록대로 미처리 — 이월 기록은 정직.

## 감사 범위와 미확인 사항

- 직접 검증: om_workflow.py(start 반환값·argparse·dispatch·main)·hook_cli.py·hook_policy.py·resume.py·markers.py·validate.py·settings.json(훅 4배선·deny)·test_claude_wiring.py 구조·83 작업 3·저작 지시서·검토결과서·3차 원문·VALIDATION 3종·targets 76건 전수 스크립트 대조·표본 18규칙 의미 대조.
- 미확인: CLI·훅 실행은 하지 않음(읽기 전용) / "미등록 슬래시 명령 거부"의 공식 문서 근거는 검토결과서 조사에 의존(채택된 수정은 이 주장과 무관하게 코드로 성립) / RULE_MANIFEST 전량 대조는 기계검증에 의존 / 규칙 89개 전체 의미 보존은 표본+3차에 의존 / 세션 간 재개 실패 경로는 코드 추론.
- 파일 무수정.
