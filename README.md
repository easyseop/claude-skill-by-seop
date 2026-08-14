# claude-skill-by-seop

Claude Code에서 쓰는 개인 스킬 모음.

## 설치

원하는 스킬 폴더를 `~/.claude/skills/`에 복사하면 끝.

```bash
git clone https://github.com/easyseop/claude-skill-by-seop.git
cp -r claude-skill-by-seop/skills/two-track-report ~/.claude/skills/
```

프로젝트 단위로 쓰려면 해당 저장소의 `.claude/skills/`에 복사한다.

## 스킬 목록

| 스킬 | 용도 |
|---|---|
| [two-track-report](skills/two-track-report/SKILL.md) | 기술 작업 결과를 두 갈래로 전달 — 사용자에게는 비개발자 눈높이 보고, 기술 상세는 협업 에이전트(코덱스 등)가 읽을 파일로. 검토 결과 보고·에이전트 간 인수인계에 사용 |
| [plain-report](skills/plain-report/SKILL.md) | 기술용어는 유지하되 각 핵심 뒤에 "즉, ~입니다" 의역을 붙이는 보고 형식. 진척 보고·결과 요약에 사용 |
| [reader-doubt-check](skills/reader-doubt-check/SKILL.md) | 문장을 내놓기 전 독자 의문 7종("이게 무슨 말이야?"·"그거 진짜야?" 등)으로 자기검토. 발표자료·보고서·설명문 작성 시 사용 |

## two-track-report 요약

**같은 내용을 두 번, 받는 쪽에 맞게 다르게 쓴다.**

- **① 사용자 보고** (대화): 문서를 하나도 안 읽은 사람 기준. 결론 먼저, 정확한 비유 허용, 기술용어 뒤엔 "즉, ~입니다" 의역. 결정에 필요한 건 여기 다 있어야 한다.
- **② 에이전트 파일** (저장소 안): 추가 질문 없이 실행 가능한 수준 — 근거 위치·재현 방법·구체적 수정안. 대화에서 나온 결정은 파일에 소급 반영. 실행에 필요한 건 여기 다 있어야 한다.
- 사용자가 용어를 하나하나 되묻기 시작하면 ①이 실패했다는 신호 — 다시 풀어 설명하고, 구체화된 내용은 ②에 반영한다.
