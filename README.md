# claude-skill-by-seop

Claude Code에서 쓰는 스킬 모음. 대화 보조용 경량 스킬 3종과, 통제형 스킬을 만드는 제작 하네스 1종.

## 설치

```bash
git clone https://github.com/easyseop/claude-skill-by-seop.git
cp -r claude-skill-by-seop/skills/<스킬명> ~/.claude/skills/   # 개인용
# 또는 프로젝트의 .claude/skills/ 에 복사
```

## 스킬 목록

| 스킬 | 한 줄 용도 | 상세 |
|---|---|---|
| **[claude-skill-author](.claude/skills/claude-skill-author/README.md)** | 통제·게이트형 스킬을 자연어로 만들어 주는 제작 하네스 (Python 3.11+ 필요) | [README](.claude/skills/claude-skill-author/README.md) · [SKILL](.claude/skills/claude-skill-author/SKILL.md) |
| [two-track-report](skills/two-track-report/SKILL.md) | 결과를 두 갈래로 — 사용자 눈높이 보고 + 협업 에이전트용 파일 분리 | [SKILL](skills/two-track-report/SKILL.md) |
| [plain-report](skills/plain-report/SKILL.md) | 기술용어 뒤에 "즉, ~입니다" 의역을 붙이는 보고 형식 | [SKILL](skills/plain-report/SKILL.md) |
| [reader-doubt-check](skills/reader-doubt-check/SKILL.md) | 문장을 내놓기 전 독자 의문 7종으로 자기검토 | [SKILL](skills/reader-doubt-check/SKILL.md) |

> **claude-skill-author**는 다른 셋과 성격이 다르다 — 복사만으로 쓰는 경량 스킬이 아니라, 저장소에 설치해 "AI 행동을 통제하는 스킬"을 만들어 내는 제작 도구다. 설치·환경·사용법·알려진 한계는 [전용 README](.claude/skills/claude-skill-author/README.md)를 볼 것.
>
> ⚠️ **오해 주의**: 이 도구는 `SKILL.md`(마크다운)를 만들어 줄 뿐, 규칙을 실제로 막는 **런타임 검사기는 만들지 않는다.** 진짜 하드 차단이 필요하면 검사기를 별도로 개발한 뒤 SKILL.md로 엮어야 한다 — [자세히](.claude/skills/claude-skill-author/README.md#️-무엇을-만들어-주고-무엇은-안-만드는가-오해-방지--필독).
