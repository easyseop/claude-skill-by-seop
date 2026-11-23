# Remote Research Mode

## 목적

로컬 checkout이 조사 브랜치가 아니거나 사용자 변경이 있어도 해당 작업트리를 수정하지 않고, GitHub 커넥터와 외부 웹 조사 도구를 사용해 `research/agent-workflow-assembler` 브랜치에서 조사를 계속한다.

## 적용 조건

- 현재 로컬 checkout이 `research/agent-workflow-assembler`가 아님
- 사용자 미추적 변경이 존재
- shell의 clone/fetch/worktree가 네트워크 문제로 실패
- GitHub 커넥터로 조사 브랜치와 입력 파일을 읽고 쓸 수 있음

## 경계

- 현재 로컬 저장소·사용자 변경을 수정·stash·삭제하지 않는다.
- 코드·설정·evidence·다른 workstream을 수정하지 않는다.
- 쓰기 허용 경로는 `OWNERSHIP.yaml.writable_paths`뿐이다.
- 모든 GitHub 쓰기는 `research/agent-workflow-assembler` 브랜치를 명시한다.
- 조사 결과는 `docs/agent-authoring/research-results/05_AGENT_WORKFLOW_ASSEMBLER_심층조사.md`에만 작성한다.

## 수행 절차

1. GitHub 커넥터로 시작 지시·Work Order·Ownership·Input Manifest·상위 계약 요약을 읽는다.
2. INPUT_MANIFEST의 Git blob SHA와 현재 파일 SHA를 대조한다.
3. 공식 규격·공식 문서·공식 저장소·원 논문을 조사한다.
4. 조사 초안은 세션 scratchpad에서 작성하고, 완성된 결과만 허용 경로에 커밋한다.
5. 규칙·불변식·평가·mutation ID의 연속성·중복·누락을 검사한다.
6. OUTPUT_MANIFEST·상태·인수인계 로그를 갱신한다.

로컬 branch 불일치나 shell DNS 실패만으로 중단하지 않는다. GitHub 커넥터도 입력을 읽거나 결과를 쓸 수 없을 때만 차단한다.
