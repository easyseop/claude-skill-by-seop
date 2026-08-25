# om-plan 확인 감사 — 실행기 전환·P0-1 반영 (2026-08-25, 새 인스턴스, 읽기 전용)

(직전 4차 PASS본의 한정 수정(87 반영) 확인 감사. 감사자 반환 원문 그대로, 판정 무수정.)

- 판정: PASS
- 핵심 이유: 한정 수정 4갈래(실행기 교체, 입력 표 customization_id 필수화+형식, 모드 표 feature 행 보강, 저장소 루트 문장의 실행기 설명)가 모두 검사기 실물과 문자 수준으로 일치하고, 이전 PASS본(4차) 대비 의도 밖 변형의 증거 0건.
  - 검사기 정합: `harness/om` 래퍼(.venv 우선→python3.14~3.11→exit 2 안내)가 SKILL.md:126 서술과 일치. feature/change의 `customization_id`·`requirement` required 강제와 검증 순서(preflight의 스키마 검증이 어댑터보다 선행)로 "없으면 `SCHEMA_INVALID`로 시작 불가" 정확(87 반례 출력과 일치). ID 형식 `^BANK-OM-[0-9]{3,}$`은 config.py:7 원문 그대로이며 어댑터 정책 귀속도 정확. block 사유 3종 전부 collectors.py:545-610 실재. `CUSTOMIZATION_ID_INVALID`도 validate_request(:300-313) 실재.
  - 훅 정합: hook_policy의 `_workflow_tail`이 `harness/om`을 직접 인식(직접 Python 호출 하위호환), marker 거부 문자열·Skill 분기 marker 생성도 7단계 서술 그대로. settings.json에 `Bash(*harness/om bootstrap*)` deny 추가 확인.
  - allowed-tools 정합: `Bash(harness/om plan *)` + `plan-resume` 별도 항목 실재, 항목 수 8개 동일.
  - 의도 밖 변형 0: 301줄 동일, `python`·`om_workflow` 잔존 0건, 앵커 76건 전수 실재(개수 동일, 실행기 관련 2건만 교체), 4차 감사 인용 문장 전건 원문 잔존, VALIDATION_BUILD 재실행분 ok:true.

## 발견 (비차단 2)
1. SKILL.md:126 "없으면 ... 종료코드 2" — `.venv` 존재+버전 미달 시에도 즉시 exit 2(PATH 우회 없음)인데 "없으면"이 "둘 다 없을 때"로만 읽힐 수 있음. 결과 서술은 참 — 다음 개정 시 한 구절 정밀화 가능.
2. §판정과 종료코드(:101)의 exit 2 설명에 래퍼 중단 경우 미추가(om-verify에는 추가됨). :126이 커버하고 판별 기준("stdout 판정 JSON 없으면 approval 아님")이 래퍼 실패에도 성립해 모순 없음 — 대칭성 차원 선택 개선.

## 확인 범위와 미확인
- 직접: 수정본 전문·래퍼·스키마·collectors(validate_request/proposal)·config.py:7·hook_policy 전문·hook_cli 분기·schema.py·preflight 검증 순서·om_workflow(argparse·exit2)·settings deny·87 전문·AUTHORING_REVIEW·4차 원문·앵커 76건 전수 스크립트 대조·VALIDATION_BUILD.
- 미확인: 4차 시점 원본 파일 부재로 바이트 diff 불가 — "변형 0"은 줄 수 동일+앵커 동수·실재+4차 인용문 전건 잔존+구 실행기 참조 0의 합성 증거. CLI·훅 실행 안 함(87 실측 기록 신뢰). 파일 무수정.
