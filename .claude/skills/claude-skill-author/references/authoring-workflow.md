# Claude Skill Author v1.3 작성 워크플로

## 상태 전이

```text
자연어 입력
→ SOURCE_REQUEST 잠금
→ SOURCE_DECISIONS 누적
→ REQUIREMENT_INTAKE
→ DESIGN 20섹션
→ DESIGN_REQUIREMENTS 18항목
→ 독립 설계 감사 + attestation
→ design PASS
→ 규칙 전수 판정·COMMAND_SPEC
→ spec PASS
→ SKILL.md + optional Agent.md
→ build PASS
→ 독립 최종 감사 + attestation
→ audit PASS
→ FINAL_STATUS PASS
```

허용 전이:

```text
design PASS → spec
spec PASS → build
build PASS → audit
audit PASS → FINAL PASS
```

원문·결정·설계·명세·런타임 파일이 바뀌면 해당 단계와 뒤 단계 fingerprint가 stale이므로 다시 검증한다.

## 증거 디렉터리

```text
.claude/skill-authoring/<target>/
├── SOURCE_REQUEST.md
├── SOURCE_DECISIONS.md
├── REQUIREMENT_INTAKE.yaml
├── DESIGN_REQUIREMENTS.yaml
├── DESIGN_AUDIT_REPORT.md
├── DESIGN_AUDIT_ATTESTATION.yaml
├── RULE_MANIFEST.yaml
├── RULE_COVERAGE.yaml
├── COMMAND_SPEC.yaml
├── SPEC_REVIEW.md
├── AUTHORING_REVIEW.md
├── AUDIT_REPORT.md
├── AUDIT_ATTESTATION.yaml
├── AUTHORING_STATE.yaml
├── VALIDATION_DESIGN.json
├── VALIDATION_SPEC.json
├── VALIDATION_BUILD.json
├── VALIDATION_AUDIT.json
└── FINAL_STATUS.json
```

## 작성자와 감사자 분리

- B 메인 세션: 원문 캡처, 저장소 조사, 단계 조율, spec/build 수행
- `skill-design-author`: intake와 DESIGN 작성
- `skill-design-auditor`: 원문·결정 ↔ intake ↔ DESIGN 감사
- `skill-author-auditor`: 설계·명세·규칙 ↔ SKILL/Agent 최종 감사
- 검사 스크립트: 필드·digest·fingerprint·상태 전이를 결정적으로 검증

## 재개

- 최초 원문은 수정하지 않는다.
- 후속 결정은 `SOURCE_DECISIONS.md`에 추가한다.
- 기존 증거를 이어갈 때 `init_authoring.py --resume`을 사용한다.
- 입력 digest가 바뀌면 뒤 단계 PASS가 stale 처리된다.
- stale 단계부터 새 감사·검증을 수행한다.

## 감사 seal

설계 감사 PASS 후:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/seal_attestation.py \
  --project-root "${CLAUDE_PROJECT_DIR}" --target "<target>" --kind design
```

최종 감사 PASS 후:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/seal_attestation.py \
  --project-root "${CLAUDE_PROJECT_DIR}" --target "<target>" --kind final
```
