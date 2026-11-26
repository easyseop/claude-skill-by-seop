# CAP 공통 규칙 정본

> 이 파일은 봉인된 `CAP_RULES_01_18.json`과 `CAP_RULES_19_36.json`에서 결정적으로 생성한다.

## CAP-01 — 가장 단순한 검증 기준선부터 시작

- **적용 조건:** 새 요청의 첫 설계 또는 기존 구조 개편.
- **행동:** Prompt only 또는 결정적 코드 기준선을 먼저 만들고, 요구를 못 충족한 실패 증거가 있을 때만 Skill·Tool·RAG·Agent·Multi-agent를 추가한다.
- **검증:** 각 상승 단계에 이전 기준선, 실패 사례, 추가 후 개선 결과가 연결되어 있는지 검사한다.
- **실패 시:** 증거가 없으면 더 단순한 단계로 되돌리고 선택 구성에서 제거한다.
- **강제 계층:** Planner + independent audit + eval gate
- **근거 자료:** [S01][S03][S07][S17]
- **예시:** 정적 정책 요약은 먼저 prompt+첨부 문서로 평가한 뒤 검색 누락이 확인될 때만 RAG를 검토한다.
- **반례:** “미래에 복잡해질 수 있으니” 처음부터 multi-agent 플랫폼을 구축한다.

## CAP-02 — 목표를 원자 Capability로 분해

- **적용 조건:** 요청에 둘 이상의 산출물·행동·판정이 섞여 있을 때.
- **행동:** 각 Capability를 입력, 출력, 성공조건, 부작용, 상태, 검증법이 독립적으로 기술되도록 분해한다.
- **검증:** 모든 Capability가 하나의 primary_owner와 하나 이상의 acceptance criterion에 매핑되는지 검사한다.
- **실패 시:** 분해되지 않으면 아키텍처 선택을 중단하고 DECOMPOSE 상태로 돌린다.
- **강제 계층:** Planner schema validator
- **근거 자료:** [S01][S25][S49]
- **예시:** “보고서 작성 후 메일 발송”을 조사·작성·검증·파일생성·승인·발송으로 분해한다.
- **반례:** 전체 요청을 `research_agent` 하나에 배치한다.

## CAP-03 — 결정적 부분을 먼저 Code에 배치

- **적용 조건:** 규칙·계산·변환·정렬·스키마 검사가 객관적으로 표현 가능할 때.
- **행동:** 해당 부분의 primary_owner를 code로 지정하고 LLM은 의미 입력 생성 또는 오류 수정에만 사용한다.
- **검증:** 동일 입력 반복 실행, unit/property test, LLM 제거 시험으로 재현성을 확인한다.
- **실패 시:** 코드화가 불가능한 의미 판단만 좁혀서 LLM에 반환한다.
- **강제 계층:** Planner + execution gate
- **근거 자료:** [S02][S08][S48][S49]
- **예시:** 날짜 유효성, 합계, YAML schema 검증은 Python validator가 수행한다.
- **반례:** LLM에게 “합계가 맞는지 다시 생각해라”라고만 한다.

## CAP-04 — Agent 정의를 제어권으로 판정

- **적용 조건:** 시스템이 Agent인지 Workflow인지 이름이 혼재할 때.
- **행동:** LLM이 다음 단계·도구·종료를 동적으로 선택하면 Agent, 코드가 경로를 소유하면 Workflow로 기록한다.
- **검증:** 실행 trace에서 다음 노드 선택 주체와 종료 주체를 확인한다.
- **실패 시:** 명칭과 실제 제어권이 다르면 architecture label을 수정한다.
- **강제 계층:** Planner + architecture auditor
- **근거 자료:** [S01][S17][S25]
- **예시:** 고정 그래프 안의 LLM 분류 노드는 Agent가 아니라 Hybrid Workflow다.
- **반례:** LLM API를 한 번 호출했다는 이유로 “agent”라고 부른다.

## CAP-05 — 예측 가능한 경로는 Workflow로 고정

- **적용 조건:** 단계와 분기를 사전에 열거할 수 있고 건너뛰면 안 되는 절차가 있을 때.
- **행동:** 코드/그래프에 상태 전이, 조건, retry, compensation, approval을 명시한다.
- **검증:** 경로 커버리지와 오류 경로 replay를 실행한다.
- **실패 시:** 열거 불가능한 하위 구간만 bounded agent로 분리한다.
- **강제 계층:** Design + workflow engine + gate
- **근거 자료:** [S01][S25][S26][S33]
- **예시:** 입력검증→초안→승인→발송을 고정하고 초안만 LLM이 생성한다.
- **반례:** 정해진 ETL 배치를 Agent가 매번 계획하게 한다.

## CAP-06 — 일회성 의미 작업은 Prompt only

- **적용 조건:** 외부 행동·재사용·장기 상태가 없고 현재 문맥으로 완료되는 요청.
- **행동:** 추가 아티팩트 없이 단일 응답 또는 구조화 출력으로 처리한다.
- **검증:** 대표·경계 프롬프트가 합격 기준을 충족하는지 확인한다.
- **실패 시:** 반복 누락은 Skill, 결정적 반복은 Script, 외부 상태는 Tool로 승격한다.
- **강제 계층:** Planner
- **근거 자료:** [S01][S17]
- **예시:** 한 번의 문장 다듬기.
- **반례:** 문장 다듬기용 영구 Agent와 DB를 만든다.

## CAP-07 — Skill은 재사용 지침 격차에만 사용

- **적용 조건:** 모델 기본 능력은 충분하지만 팀 고유 절차·용어·형식이 반복적으로 빠질 때.
- **행동:** SKILL.md에 적용 조건, 절차, 검증 루프, 출력 계약을 담고 다른 실행 책임은 분리한다.
- **검증:** with-skill/without-skill와 trigger near-miss를 비교한다.
- **실패 시:** 개선이 없으면 Skill을 만들지 않거나 더 작게 재구성한다.
- **강제 계층:** Skill author + skill eval gate
- **근거 자료:** [S05][S07][S09][S10]
- **예시:** 팀의 ADR 작성 규칙과 완료 체크리스트.
- **반례:** 모델이 이미 정확히 수행하는 단순 요약을 스킬로 포장한다.

## CAP-08 — 작고 안정적인 지식은 Reference로 고정

- **적용 조건:** 권위 자료가 소수 파일이며 버전·범위를 고정할 수 있을 때.
- **행동:** references/에 저장하고 checksum/버전/권위 순서를 기록한다.
- **검증:** 참조 링크, 버전, 누락/충돌 테스트를 수행한다.
- **실패 시:** 질의별 선택·동기화·ACL 필요가 드러날 때만 RAG로 승격한다.
- **강제 계층:** Knowledge planner + repository gate
- **근거 자료:** [S05][S06][S51]
- **예시:** 고정된 30페이지 운영 가이드와 용어집.
- **반례:** 작은 가이드에 vector DB·ingestion service를 구축한다.

## CAP-09 — RAG는 검색 필요성 증거가 있을 때만

- **적용 조건:** 대규모·변경·권한 코퍼스에서 질의별 관련 근거를 골라야 할 때.
- **행동:** 코퍼스 inventory, freshness, ACL, citation, abstention, retrieval eval을 포함한 RAG 계획을 만든다.
- **검증:** Reference 기준선 대비 검색 적중, 근거 충실성, ACL, stale-index 테스트를 분리 평가한다.
- **실패 시:** 검색 이득이 없거나 항상 같은 파일이면 Reference/live Tool로 하강한다.
- **강제 계층:** Knowledge gate + security gate + eval gate
- **근거 자료:** [S50][S51][S53]
- **예시:** 문서별 권한이 다른 수만 건의 내부 규정 검색.
- **반례:** 실시간 계좌 잔액을 과거 문서 인덱스에서 찾는다.

## CAP-10 — 반복 재발명 로직은 Script로 추출

- **적용 조건:** trace에서 같은 파싱·변환·렌더링·검증 코드를 모델이 반복 생성할 때.
- **행동:** 테스트된 script/CLI로 추출하고 안정적인 I/O와 exit code를 제공한다.
- **검증:** trace 비교, unit test, malformed input, dependency pin을 확인한다.
- **실패 시:** 일회성 로직이면 과도한 추출을 피하고, 의미 판단은 스크립트 밖에 둔다.
- **강제 계층:** Execution assembler + CI
- **근거 자료:** [S07][S08]
- **예시:** 매번 CSV 컬럼을 정규화하던 코드를 `normalize_csv.py`로 고정한다.
- **반례:** 한 번 쓰는 세 줄짜리 표현 변환마다 새 서비스 생성.

## CAP-11 — 계획과 출력은 실행 전에 Validator로 검사

- **적용 조건:** 객관적 스키마·필드·정책 규칙이 있을 때.
- **행동:** LLM이 만든 계획/인자를 먼저 deterministic validator에 통과시킨 뒤 부작용을 허용한다.
- **검증:** 유효/무효 fixture와 오류 메시지의 수정 가능성을 시험한다.
- **실패 시:** 검증 실패는 자동 수정 가능한 경우 revise loop, 고위험이면 중단한다.
- **강제 계층:** Pre-execution gate
- **근거 자료:** [S07][S21][S42]
- **예시:** PDF form field 값을 원본 필드 목록과 대조한 뒤 채운다.
- **반례:** 발송 후에야 수신자 주소 형식 오류를 확인한다.

## CAP-12 — 기존 Tool·API·MCP를 먼저 재사용

- **적용 조건:** 외부 데이터/행동 Capability가 필요할 때.
- **행동:** 저장소와 연결된 서비스에서 인증·감사·오류 계약이 검증된 경계를 먼저 찾는다.
- **검증:** 기존 경계의 기능 적합성, 권한 범위, SLA, 테스트 가능성을 기록한다.
- **실패 시:** 적합하지 않을 때만 gap을 근거로 새 wrapper/tool을 만든다.
- **강제 계층:** Repository discovery + architecture audit
- **근거 자료:** [S02][S11][S38]
- **예시:** 이미 있는 CRM MCP를 사용하고 팀 규칙만 Skill에 추가한다.
- **반례:** 같은 API용 MCP server를 프로젝트마다 새로 만든다.

## CAP-13 — 도구는 엔드포인트가 아니라 작업 단위로 설계

- **적용 조건:** API가 저수준 엔드포인트 다수를 제공할 때.
- **행동:** 사용자 목표를 완수하는 소수의 고응집 도구로 묶되, 위험이 다른 행동은 분리한다.
- **검증:** 대표 작업의 평균 연쇄 호출, 인자 오류, 도구 선택 실패를 평가한다.
- **실패 시:** 너무 큰 만능 도구는 다시 명확한 작업 경계로 분해한다.
- **강제 계층:** Tool design gate
- **근거 자료:** [S02]
- **예시:** `search_customer_context`가 필요한 검색·정규화를 내부에서 수행한다.
- **반례:** `GET /v1/x`, `GET /v1/y`를 그대로 수십 개 도구로 노출한다.

## CAP-14 — 중복 Tool을 제거하고 namespace를 사용

- **적용 조건:** 도구 수가 많거나 기능이 유사해 모델이 혼동할 때.
- **행동:** 의미 중복을 통합하고 도메인 namespace/점진적 discovery를 적용한다.
- **검증:** 도구 선택 confusion matrix와 schema token/latency를 비교한다.
- **실패 시:** 정리 후에도 도메인 라우팅이 실패할 때만 Agent 분리를 검토한다.
- **강제 계층:** Tool registry + eval gate
- **근거 자료:** [S02][S17][S19][S44][S52]
- **예시:** CRM 도구를 `crm.*`, 결제를 `billing.*`로 묶는다.
- **반례:** 같은 검색을 `find`, `lookup`, `query` 세 도구로 제공한다.

## CAP-15 — 읽기와 쓰기 도구를 분리

- **적용 조건:** 외부 시스템에서 조회와 변경이 모두 가능할 때.
- **행동:** read-only 도구와 write 도구의 이름·권한·승인·출력 계약을 분리한다.
- **검증:** 읽기 요청이 write 권한 없이 완료되는지, 모델이 write를 오선택하는지 시험한다.
- **실패 시:** 분리가 불가능하면 wrapper에서 action allowlist와 approval을 강제한다.
- **강제 계층:** Permission gate + tool runtime
- **근거 자료:** [S15][S16][S39]
- **예시:** `get_customer`와 `update_customer`를 별도 scope로 제공한다.
- **반례:** 조회용 만능 도구가 임의 SQL UPDATE도 실행한다.

## CAP-16 — 도구 계약은 모델 친화적이고 오류는 수정 가능하게

- **적용 조건:** LLM이 도구 이름·인자·결과를 해석해야 할 때.
- **행동:** 명확한 이름, 구체적 설명, 최소 스키마, 고신호 응답, pagination/filter, actionable error를 제공한다.
- **검증:** 잘못된 인자·빈 결과·부분 실패·대용량 결과에서 복구 성공률을 평가한다.
- **실패 시:** 오류가 모호하면 도구 설명/스키마를 수정하고 Agent 수를 늘리지 않는다.
- **강제 계층:** Tool design + tool eval
- **근거 자료:** [S02][S19][S48][S50]
- **예시:** “customer_id는 UUID이며 없으면 후보를 반환”을 schema/error에 명시.
- **반례:** `invalid request`만 반환한다.

## CAP-17 — 최소 권한과 Sandbox를 런타임에서 강제

- **적용 조건:** 파일·셸·네트워크·코드 실행 또는 외부 계정 접근이 있을 때.
- **행동:** 작업 디렉터리·네트워크 도메인·자원·도구 allowlist를 최소화하고 deny-by-default를 적용한다.
- **검증:** 권한 우회, 경계 밖 읽기/쓰기, 네트워크 차단, resource exhaustion을 시험한다.
- **실패 시:** 필수 작업이 막히면 정확한 최소 권한만 증거와 함께 추가한다.
- **강제 계층:** Runtime permission/sandbox gate
- **근거 자료:** [S15][S16][S38][S45]
- **예시:** 코드 생성 Agent는 임시 worktree와 제한 네트워크에서 테스트한다.
- **반례:** Skill에 “안전하게 실행”이라고 쓰고 전체 홈 디렉터리 권한을 준다.

## CAP-18 — 고영향·비가역 행동은 Human approval

- **적용 조건:** 송금·구매·외부 발송·생산 배포·삭제·법적 제출처럼 영향이 큰 행동.
- **행동:** 실행 직전 실제 대상·변경 diff·비용·권한을 보여주고 승인 토큰을 요구한다.
- **검증:** 승인 거부/취소/만료/대상 변경 후 재승인을 시험한다.
- **실패 시:** 승인자가 없거나 정보가 불충분하면 blocked로 중단한다.
- **강제 계층:** Human gate + runtime
- **근거 자료:** [S27][S39][S42]
- **예시:** 메일 초안을 보여주고 수신자·본문 확인 후 발송.
- **반례:** 사용자의 초기 “처리해줘”를 모든 후속 결제의 영구 승인으로 간주한다.

## CAP-19 — 단일 Agent를 Multi-agent보다 먼저 최대화

- **적용 조건:** 동적 실행이 필요하지만 아직 분리 근거가 없을 때.
- **행동:** 도구 통합·명확화·namespace·structured output·상태 축소 후 단일 Agent를 평가한다.
- **검증:** 분리 전후 정확도·비용·지연·복구를 같은 시나리오로 비교한다.
- **실패 시:** 단일 Agent가 합격하면 Multi-agent 후보를 기각한다.
- **강제 계층:** Architecture auditor + eval gate
- **근거 자료:** [S17][S19]
- **예시:** 지원 Agent의 겹치는 환불 도구를 정리한 뒤 재평가한다.
- **반례:** 도구가 8개라는 이유만으로 8개 Agent를 만든다.

## CAP-20 — Multi-agent는 허용된 근거를 요구

- **적용 조건:** 독립 실행 루프 둘 이상을 만들려 할 때.
- **행동:** context isolation, independent parallelism, authority separation, proven specialization 중 최소 하나와 baseline failure를 기록한다.
- **검증:** 역할별 도구·권한·문맥·출력 계약과 병합/충돌 평가를 수행한다.
- **실패 시:** 허용 근거가 없으면 single agent 또는 deterministic workflow로 하강한다.
- **강제 계층:** Planner schema + independent audit
- **근거 자료:** [S14][S17][S32][S34]
- **예시:** 서로 독립된 20개 문서를 병렬 조사하고 verifier가 근거를 재검사.
- **반례:** 짧은 글을 writer와 reviewer Agent가 서로 대화하며 토큰을 소비.

## CAP-21 — 컨텍스트 격리를 분리의 독립 근거로 인정

- **적용 조건:** 대량 검색 로그·파일 내용이 주 컨텍스트를 오염시키지만 요약만 필요할 때.
- **행동:** 읽기 전용 subagent에 탐색을 맡기고 명시적 summary schema만 반환한다.
- **검증:** 주 컨텍스트 토큰, 누락률, 원문 추적 가능성, 권한을 비교한다.
- **실패 시:** 격리 이득이 없으면 주 Agent/Workflow 노드로 통합한다.
- **강제 계층:** Context budget gate
- **근거 자료:** [S11][S14]
- **예시:** 저장소 전수 grep은 Explore subagent, 최종 설계 판단은 주 세션.
- **반례:** 작업이 작아도 “전문가 느낌”을 위해 subagent 생성.

## CAP-22 — 병렬화는 독립성과 병합 규칙이 있을 때만

- **적용 조건:** 여러 하위 작업을 동시에 실행하려 할 때.
- **행동:** 입력/상태 의존성을 분석하고 독립 작업만 병렬화하며 deterministic merge를 정의한다.
- **검증:** race, duplicate work, merge conflict, 실제 wall-clock 이득을 측정한다.
- **실패 시:** 공유 상태가 강하면 순차 workflow로 되돌린다.
- **강제 계층:** Workflow engine + eval
- **근거 자료:** [S01][S25][S33]
- **예시:** 서로 다른 출처군 검색을 병렬 수행하고 source ID로 합친다.
- **반례:** 앞 단계 결과가 필요한 세 단계를 동시에 실행한다.

## CAP-23 — 상태 범위와 수명을 최소화

- **적용 조건:** 대화/작업을 넘는 상태가 필요할 때.
- **행동:** call→run→thread→cross-thread→system-of-record 순으로 가장 짧은 scope를 선택하고 TTL·삭제·소유자를 둔다.
- **검증:** 재개, 만료, 사용자 격리, 마이그레이션, 삭제 요청, 깨진 checkpoint를 시험한다.
- **실패 시:** 필요성 없는 장기 상태는 제거하고 원장은 외부 시스템에 둔다.
- **강제 계층:** State schema + security gate
- **근거 자료:** [S28][S57]
- **예시:** 승인 대기 workflow는 thread checkpoint만 보존.
- **반례:** 모든 도구 응답을 무기한 사용자 메모리로 저장한다.

## CAP-24 — Agent loop에 종료·예산·중단 조건을 강제

- **적용 조건:** bounded agent 또는 multi-agent가 선택될 때.
- **행동:** max turns/tool calls/time/cost와 completion·error·human escalation 조건을 정의한다.
- **검증:** 무응답 도구, 반복 실패, 상호 핸드오프 loop, 부분 완료에서 종료를 시험한다.
- **실패 시:** 상한 초과 시 fail-closed 또는 인간 인계로 끝내고 자동 무한 재시도 금지.
- **강제 계층:** Runtime + eval gate
- **근거 자료:** [S04][S17][S23][S35]
- **예시:** 조사 Agent는 12 tool calls 또는 5분에서 중단하고 미완료 항목을 보고.
- **반례:** “완료될 때까지 계속”만 설정한다.

## CAP-25 — 재시도는 idempotency·보상과 함께 설계

- **적용 조건:** 외부 API·네트워크·부분 실패가 있는 Workflow/Agent.
- **행동:** 오류 유형별 retry 가능 여부, backoff, idempotency key, compensation, manual recovery를 정의한다.
- **검증:** 동일 요청 중복 실행, timeout 후 성공 여부 불명, 보상 실패를 시험한다.
- **실패 시:** 상태가 불명확한 쓰기는 자동 재시도하지 않고 조회/인간 확인으로 전환한다.
- **강제 계층:** Execution runtime + recovery gate
- **근거 자료:** [S30]
- **예시:** 결제 요청은 idempotency key로 재시도하고 결과 조회 후 결정.
- **반례:** timeout이면 같은 송금을 무조건 다시 호출한다.

## CAP-26 — 안전 규칙을 Prompt/Skill만으로 보장하지 않음

- **적용 조건:** “항상/절대/금지”가 보안·부작용에 관련될 때.
- **행동:** 규칙을 permission, hook, validator, sandbox, approval로 구현하고 Skill은 설명만 담당한다.
- **검증:** 악의적/충돌 프롬프트로 규칙 우회를 시도한다.
- **실패 시:** 런타임 강제가 없으면 고위험 Capability를 승인하지 않는다.
- **강제 계층:** Security gate
- **근거 자료:** [S11][S12][S13][S15]
- **예시:** `.env` 수정은 PreToolUse hook과 deny rule로 차단.
- **반례:** SKILL.md에만 “.env를 수정하지 마라”라고 쓴다.

## CAP-27 — 지식 최신성과 권한을 retrieval 이전에 정의

- **적용 조건:** Reference/RAG/live Tool 중 하나를 고를 때.
- **행동:** 권위 원천, 갱신 빈도, cache TTL, ACL, 삭제/정정 전파를 먼저 명시한다.
- **검증:** stale source, 권한 없는 문서, 상충 버전, 삭제 문서가 검색되는지 시험한다.
- **실패 시:** 권위/ACL을 보장할 수 없으면 답변을 중단하거나 live source로 전환한다.
- **강제 계층:** Knowledge + security gate
- **근거 자료:** [S37][S40][S44][S50][S51]
- **예시:** API 문서는 버전별 index와 sync SLA를 둔다.
- **반례:** 한 번 구축한 인덱스를 영구적으로 최신이라고 가정한다.

## CAP-28 — 관측성은 실행 경계와 위험에 비례

- **적용 조건:** Tool, Agent, Workflow, approval이 있는 운영 구성.
- **행동:** 모델 호출·도구 인자/결과·상태 전이·가드레일·승인·비용을 민감정보 제거 후 추적한다.
- **검증:** 실패 한 건을 입력부터 부작용까지 재구성할 수 있는지 확인한다.
- **실패 시:** 추적이 과도한 민감정보를 담으면 redaction/retention을 줄인다.
- **강제 계층:** Observability gate
- **근거 자료:** [S04][S22][S29]
- **예시:** handoff와 tool call에 correlation ID를 남긴다.
- **반례:** 최종 답변만 로그하고 어떤 도구가 변경했는지 남기지 않는다.

## CAP-29 — 평가는 기준선·near-miss·반례를 포함

- **적용 조건:** Skill/Tool/RAG/Agent/Planner의 선택 또는 변경.
- **행동:** positive, negative, near-miss, malformed, adversarial, recovery 사례를 단순 기준선과 비교한다.
- **검증:** 선택 정확도, 결과 품질, 안전, 비용, 지연을 분리한다.
- **실패 시:** 개선 없이 비용만 늘면 구성요소를 제거한다.
- **강제 계층:** Eval gate
- **근거 자료:** [S02][S04][S09][S10][S52][S53]
- **예시:** RAG 필요 사례와 작은 정적 문서 near-miss를 함께 평가.
- **반례:** 성공 사례 두 개만 보고 Planner를 합격시킨다.

## CAP-30 — 모든 구성요소에 ablation 필요성 시험

- **적용 조건:** architecture.selected_components에 항목을 추가할 때.
- **행동:** 구성요소를 제거/대체한 기준선과 비교하거나 안전 규정상 제거 불가 근거를 기록한다.
- **검증:** 품질·안전·비용 변화와 실패 유형을 비교한다.
- **실패 시:** load-bearing이 아니면 제거하고 plan을 갱신한다.
- **강제 계층:** Independent audit + regression eval
- **근거 자료:** [S03]
- **예시:** reviewer Agent 제거 후 테스트가 동일하면 Workflow validator로 대체.
- **반례:** 한 번 추가한 RAG/Agent를 영구 전제로 취급한다.

## CAP-31 — 질문은 아키텍처를 바꿀 때만

- **적용 조건:** 요구사항이 불완전해 인터뷰를 고려할 때.
- **행동:** 저장소 조사→안전 기본값→사용자 정책 결정→고위험 blocker 순으로 분류하고, 실제 선택을 바꾸는 질문만 묻는다.
- **검증:** 각 질문에 why_needed와 선택별 architecture delta가 있는지 검사한다.
- **실패 시:** delta가 없으면 질문을 삭제하고 assumption으로 기록한다.
- **강제 계층:** Planner interview gate
- **근거 자료:** [S42]
- **예시:** 자동 발송 여부는 권한/승인을 바꾸므로 질문한다.
- **반례:** 저장소에 명시된 Python 버전을 사용자에게 다시 묻는다.

## CAP-32 — 답 없는 고위험 결정은 중단

- **적용 조건:** 권한·승인자·데이터 분류·비가역 복구가 불명확할 때.
- **행동:** status=blocked로 전환하고 구현/실행 아티팩트 생성을 막는다.
- **검증:** blocker가 해소되기 전 downstream state transition이 불가능한지 검사한다.
- **실패 시:** 안전한 read-only 분석만 별도 범위로 허용할 수 있다.
- **강제 계층:** Human/security gate
- **근거 자료:** [S15][S27][S39][S42]
- **예시:** 운영 삭제 승인자가 없으면 변경 계획까지만 생성.
- **반례:** 모델이 적당한 승인자를 추측하고 실행한다.

## CAP-33 — 프레임워크 수명주기와 버전을 고정

- **적용 조건:** 외부 SDK/프레임워크/규격을 아키텍처에 채택할 때.
- **행동:** version/branch/commit, 유지보수 상태, migration path, adapter 경계를 기록한다.
- **검증:** 재현 설치와 차기 버전 contract test를 수행한다.
- **실패 시:** maintenance/deprecation이면 신규 채택을 재검토하고 중립 계약을 우선한다.
- **강제 계층:** Dependency/lifecycle gate
- **근거 자료:** [S01][S24][S31][S36][S54][S55][S56][S60]
- **예시:** AutoGen 패턴은 참고하되 신규 구현은 장기 지원 대안과 비교.
- **반례:** 블로그 예제의 최신 버전을 추정해 고정 없이 배포.

## CAP-34 — Handoff 경계에서 권한을 다시 검사

- **적용 조건:** Agent 간 handoff 또는 agent-as-tool이 외부 행동 권한을 바꿀 때.
- **행동:** 인자 파싱 후 부작용 전에 대상 Agent/tool의 권한과 사용자 identity를 검사한다.
- **검증:** 위조된 handoff metadata, 권한 없는 대상, history filter 누락을 시험한다.
- **실패 시:** 검사 실패는 handoff 자체를 중단하고 원 Agent/사용자에게 반환한다.
- **강제 계층:** Handoff runtime + security gate
- **근거 자료:** [S20][S21]
- **예시:** refund amount 기반 승인은 refund Agent 진입 첫 줄에서 검사.
- **반례:** 함수 도구 guardrail이 handoff에도 자동 적용된다고 가정.

## CAP-35 — 비밀은 LLM 문맥을 통과시키지 않음

- **적용 조건:** password, API key, access token, payment credential이 필요할 때.
- **행동:** secret store/environment 또는 out-of-band URL flow를 사용하고 모델에는 핸들/상태만 제공한다.
- **검증:** trace/log/prompt/tool result에서 secret pattern과 회수 가능성을 검사한다.
- **실패 시:** 안전한 경로가 없으면 기능을 blocked 처리한다.
- **강제 계층:** Secret/security gate
- **근거 자료:** [S42][S43][S45]
- **예시:** 사용자가 브라우저의 공식 도메인에서 OAuth를 완료한다.
- **반례:** 채팅에 API key를 입력하게 하고 Agent memory에 저장한다.

## CAP-36 — 핵심 결론에 출처·스냅샷·근거 등급을 연결

- **적용 조건:** 현재 기능·연구 결과·설계 제안을 함께 문서화할 때.
- **행동:** source ID, 유형, 날짜/버전/커밋을 기록하고 제안은 D 등급으로 표시한다.
- **검증:** 무출처 기능 단정, 오래된 문서, 초안 규격의 규범화 여부를 감사한다.
- **실패 시:** 근거가 없으면 추정으로 낮추거나 결론을 제거한다.
- **강제 계층:** Documentation checker + independent audit
- **근거 자료:** [S01][S36][S37][S45][S58][S59]
- **예시:** MCP 보안 초안을 “초안 권고”로 표기한다.
- **반례:** 논문 아이디어를 특정 SDK의 현재 보장 기능으로 서술한다.
