# 독립 감사 기준

## 설계 감사

비교:

```text
SOURCE_REQUEST.md + SOURCE_DECISIONS.md
↔ REQUIREMENT_INTAKE.yaml
↔ DESIGN.md
↔ DESIGN_REQUIREMENTS.yaml
```

검사:

- 원문 요구 누락·왜곡·반전
- 사용자 미승인 정책·권한 추가
- 허용·금지·승인 모순
- 미확인을 사실로 확정
- 20개 설계 섹션·18개 필수 의미 항목 누락
- 해결되지 않은 차단 질문
- 저장소 사실의 실제 존재

## 최종 감사

비교:

```text
원문·결정·intake·설계
→ COMMAND_SPEC
→ RULE_COVERAGE
→ SKILL.md / Agent.md
```

검사:

- APPLY·TRANSFORM 실질 반영
- EXCLUDE 근거
- EXTERNAL 실재 통제
- frontmatter·인수·권한·절차·검증·실패·완료 계약 정합성
- Agent 필요성·도구·통합 방식
- 정상·경계·오류·인젝션·부분 실패·동명 충돌
- design/spec/build fingerprint freshness

## 판정

감사 보고서에는 다음 중 정확히 한 줄만 둔다.

```text
- 판정: PASS
- 판정: CONDITIONAL
- 판정: FAIL
```

차단 문제가 하나라도 있으면 `PASS`를 사용하지 않는다. PASS 후에는 `seal_attestation.py`로 보고서를 현재 입력 digest에 묶는다.
