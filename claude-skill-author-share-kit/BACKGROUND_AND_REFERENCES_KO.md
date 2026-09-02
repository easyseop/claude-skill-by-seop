# Claude Skill Author 조사 배경과 참고자료

## 1. 시작 배경

이 프로젝트는 특정 하네스 저장소를 복제하여 만든 것이 아니다. 출발점은 “LLM 스킬·하네스용 Markdown을 작성할 때 반복적으로 지켜야 하는 공통 규칙은 무엇인가?”라는 조사 요청이었다.

조사는 다음 순서로 발전했다.

```text
여러 생태계의 공식 작성 지침과 연구 비교
→ 제품 독립 공통 작성규칙 도출
→ Claude Code 슬래시 커맨드 전용 차이 분리
→ 긴 지시문에서 발생한 규칙 누락 확인
→ 규칙 ID 전수 판정과 기계 검사 추가
→ 설계 작성자·독립 감사자·Stop 게이트 분리
→ 자연어 요구사항 수립과 설계 감사까지 확장
```

## 2. 참고자료 수

- 최초 공통 규칙 문서: **31개 번호형 근거 항목**
  - 공식 규격·제품 문서: **23개 항목**
  - 연구 논문: **8편**
- 하나의 번호에 복수 공식 문서를 묶은 경우를 개별 링크로 세면: **34개 URL**
- Claude Code 전용 차이 문서: **10개 공식 근거**
- 두 기초 문서 전체를 합쳐 중복을 제거하면: **37개 고유 URL**

## 3. 핵심 생태계

1. Agent Skills
2. OpenAI Codex
3. Claude Code
4. GitHub Copilot
5. Cursor
6. OpenHands
7. Cline
8. Roo Code
9. LangGraph
10. Microsoft AutoGen
11. CrewAI
12. Model Context Protocol

초기 탐색 범위에는 Continue와 Aider도 포함됐지만, 아래의 최종 번호형 근거 목록은 직접 연결한 공식 문서와 논문을 기준으로 한다.

## 4. 규칙 체계로 변환된 방식

공통 문서에서 67개 규칙 ID를 만들었다.

- 공통 핵심 `C-*`: 20개
- 계획 `P-*`: 8개
- 개발·작성 `D-*`: 12개
- 실행 `E-*`: 7개
- 검증 `V-*`: 8개
- 보안·규칙 주입 `S-*`: 7개
- 유지보수 `M-*`: 5개

Claude Code 전용 차이 문서에서 `CC-*` 22개를 추가해, 제작 하네스가 전수 판정하는 규칙은 총 89개가 됐다.

이 규칙들은 최종 `SKILL.md`에 모두 복사되는 것이 아니다. 각 대상 스킬에 대해 `APPLY`, `TRANSFORM`, `EXCLUDE`, `EXTERNAL` 중 하나로 반드시 판정하고, 필요한 규칙만 실행 가능한 문장·스크립트·권한·훅으로 변환한다.

## 5. 최초 공통 규칙 문서의 근거 목록

## 공식 규격·문서

1. Agent Skills, Specification  
   https://agentskills.io/specification
2. Agent Skills, Best practices for skill creators  
   https://agentskills.io/skill-creation/best-practices
3. Agent Skills, Optimizing skill descriptions  
   https://agentskills.io/skill-creation/optimizing-descriptions
4. Agent Skills, Evaluating skill output quality  
   https://agentskills.io/skill-creation/evaluating-skills
5. OpenAI Codex, Custom instructions with AGENTS.md  
   https://developers.openai.com/codex/agent-configuration/agents-md
6. OpenAI Codex, Using PLANS.md for multi-hour problem solving  
   https://developers.openai.com/cookbook/articles/codex_exec_plans
7. OpenAI Codex, Agent approvals and security  
   https://developers.openai.com/codex/agent-approvals-security
8. OpenAI Codex, Sandbox  
   https://developers.openai.com/codex/sandboxing
9. Claude Code, How Claude remembers your project  
   https://code.claude.com/docs/en/memory
10. Claude Code, Extend Claude with skills  
    https://code.claude.com/docs/en/skills
11. Claude Code, Configure permissions  
    https://code.claude.com/docs/en/permissions
12. Claude Code, Hooks  
    https://code.claude.com/docs/en/hooks
13. GitHub Copilot, Custom instructions for code review  
    https://docs.github.com/en/copilot/tutorials/customize-code-review
14. Cursor, Rules  
    https://cursor.com/docs/rules
15. OpenHands, Global Skills  
    https://docs.openhands.dev/overview/skills/public
16. Cline, Skills  
    https://docs.cline.bot/customization/skills
17. Cline, Plan and Act Mode  
    https://docs.cline.bot/core-workflows/plan-and-act
18. Cline, Memory Bank  
    https://docs.cline.bot/best-practices/memory-bank
19. Roo Code, Custom Instructions and Skills  
    https://docs.roocode.com/features/custom-instructions  
    https://docs.roocode.com/features/skills
20. LangGraph, Overview and Interrupts  
    https://docs.langchain.com/oss/python/langgraph/overview  
    https://docs.langchain.com/oss/python/langgraph/interrupts
21. Microsoft AutoGen, GraphFlow and Human-in-the-Loop  
    https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/graph-flow.html  
    https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html
22. CrewAI, Tasks and Guardrails  
    https://docs.crewai.com/en/concepts/tasks
23. Model Context Protocol, Security Best Practices  
    https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

## 논문

24. Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models  
    https://arxiv.org/abs/2210.03629
25. Wang et al., Plan-and-Solve Prompting  
    https://arxiv.org/abs/2305.04091
26. Madaan et al., Self-Refine: Iterative Refinement with Self-Feedback  
    https://arxiv.org/abs/2303.17651
27. Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning  
    https://arxiv.org/abs/2303.11366
28. Wallace et al., The Instruction Hierarchy  
    https://arxiv.org/abs/2404.13208
29. Liu et al., Lost in the Middle  
    https://arxiv.org/abs/2307.03172
30. Yang et al., SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering  
    https://arxiv.org/abs/2405.15793
31. Jimenez et al., SWE-bench  
    https://arxiv.org/abs/2310.06770

---

## 6. Claude Code 전용 차이 문서의 근거 목록

아래 10개는 Claude Code 제품 고유의 경로·frontmatter·호출·권한·훅·서브에이전트 차이를 검증하기 위해 별도로 사용한 공식 근거다. 공통 목록과 일부 중복된다.

1. Claude Code, Extend Claude with skills  
   https://code.claude.com/docs/en/skills
2. Claude Code, Extend Claude Code  
   https://code.claude.com/docs/en/features-overview
3. Claude Code, How Claude remembers your project  
   https://code.claude.com/docs/en/memory
4. Claude Code, Configure permissions  
   https://code.claude.com/docs/en/permissions
5. Claude Code, Hooks reference  
   https://code.claude.com/docs/en/hooks
6. Claude Code, Automate actions with hooks  
   https://code.claude.com/docs/en/hooks-guide
7. Claude Code, Create custom subagents  
   https://code.claude.com/docs/en/sub-agents
8. Agent Skills, Specification  
   https://agentskills.io/specification
9. Agent Skills, Best practices for skill creators  
   https://agentskills.io/skill-creation/best-practices
10. Agent Skills, Evaluating skill output quality  
    https://agentskills.io/skill-creation/evaluating-skills

---

## 7. 해석 시 주의사항

- 이 목록은 단일 공식 표준이 아니라 여러 자료에서 반복되는 원칙을 합성한 근거 집합이다.
- 제품 버전에 따라 frontmatter와 훅 동작이 바뀔 수 있으므로 실제 설치 버전과 최신 공식 문서를 우선한다.
- Markdown 규칙은 보안 경계가 아니다. 실제 금지는 permissions, hook, CI, 샌드박스, 읽기 전용 자격증명 같은 기술적 통제와 결합해야 한다.
- 연구 논문은 설계 원리를 제공하며, 특정 Claude Code 필드의 현재 동작은 공식 제품 문서를 근거로 판단한다.
