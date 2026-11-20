# 세션 협업 프레임워크

이 디렉터리는 총괄 세션, 조사 세션, 구현 세션, 검토 세션이 GitHub를 공용 작업판으로 사용하기 위한 공통 규약과 템플릿을 제공한다.

## 기본 원칙

세션들은 서로의 비공개 대화를 직접 읽거나 보이지 않는 메시지를 주고받는다고 가정하지 않는다. 공식 통신은 다음 파일과 Draft PR을 통해서만 수행한다.

```text
SESSION_START_PROMPT.md
WORK_ORDER.md
CURRENT_SESSION_STATE.yaml
HANDOFF_LOG.md
INPUT_MANIFEST.yaml
OUTPUT_MANIFEST.yaml
Draft PR
```

## 세션 유형

- `research`: 외부 조사·규칙 추출·설계안 작성. 코드 구현 금지.
- `implementation`: 승인된 조사·계약을 실제 source·test·evidence로 구현.
- `review`: diff·evidence·결과 보고서를 독립 검토. 구현 수정은 별도 지시가 있을 때만.

## 사용자 역할

사용자는 세션을 열고 해당 브랜치의 `SESSION_START_PROMPT.md`를 읽으라고 한 번 전달한다. 필요한 입력자료, 상태 파일, 인수인계 파일은 총괄 세션이 미리 브랜치에 배치한다.

## 총괄 세션 역할

1. 다음 workstream과 세션 유형을 결정한다.
2. 전용 브랜치와 Draft PR을 만든다.
3. 필요한 입력 문서와 digest를 업로드한다.
4. 시작 프롬프트·Work Order·상태·인수인계 파일을 생성한다.
5. 상태를 감시하고 blocker·검토·다음 단계를 기록한다.
6. 자동 병합하지 않는다.

세부 규약은 `SESSION_COLLABORATION_PROTOCOL.md`를 따른다.
