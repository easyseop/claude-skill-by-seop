# Agent & Workflow Assembler 심층조사

조사 기준일: **2026-11-26 KST** · 저장소: `easyseop/claude-skill-by-seop` · 기존 Draft PR: **#2** · 작업 브랜치: `research/agent-workflow-assembler`

## 0. 결론과 조사 방법

**Assembler는 승인된 구성의 연결·검증·패키징 경계를 명시하는 단계다.** Planner가 정한 제어 모드와 component set을 유지하고, 부족한 기능·인터페이스·권한은 소관 생성기로 재진입한다. `SKILL.md` 하나에 모든 책임을 넣거나 모든 요청을 Agent로 만들지 않는다. 이 책임 경계는 Factory의 승인 입력에서 온다. [I01], [I03]

이번 재개에서는 새 승인 입력의 **EVAL-01~EVAL-22 전체 Assembly 매핑**을 §19에 작성했다. 요청·기대 아키텍처·기대 제어 모드·기대 component set은 정본에서 그대로 가져오고, 조립 결정·entrypoint·binding·금지 구성·Gate/재진입은 연구 제안으로 표시했다. 입력의 `status: PASS` 및 paraphrase PASS를 실행 증거로 쓰지 않았다. 개별 완성 `CAPABILITY_PLAN`이 없다는 이유로 이 연구 범위를 다시 차단하지 않는다. [I02], [I04], [I05], [I08]

### 0.1 실제 수행 범위와 판정

| 구분 | 이번 결과 | 의미 |
|---|---|---|
| 실제 착수 | 기존 세션에서 `IN_PROGRESS` 기록 후 조사 | 준비 완료와 착수를 구분 |
| 입력 무결성 | 등록 입력 7/7, 봉인 대상 8/8 일치 | Git blob SHA를 실제 UTF-8 내용으로 재계산하고 head tree와 대조 |
| 정본 식별 | 두 입력의 ID 집합·제목 22/22 대응 | 정적 원본 대조이며 Planner 실행 결과 아님 |
| 연구 매핑 | §19의 22개 기록 | 승인된 기대값에 대한 Assembly 연구 출력 |
| 문서 구조 | 명시된 §0~§25, 총 26개 섹션 | Work Order의 “25개”라는 요약보다 실제 나열된 제목을 모두 보존 |
| 규칙·불변식·평가·mutation | ASM 30, AINV 24, AEVAL 30, AMUT 24 | 후속 구현·검증을 위한 명세; 설계된 평가와 mutation 실행은 `NOT_RUN` |
| 실제 런타임·외부 작업 | **0회 / NOT_RUN** | Agent 실행, DB 삭제, 발송, secret 연결, 설치, host Hook 차단, 배포를 수행하지 않음 |
| 연구 검토·운영 승인 | 검토 요청 대상 | `VERIFIED_RESEARCH`, `VERIFIED_LOCAL`, production 승인을 자체 선언하지 않음 |

문서 검증 결과: **정적 문서 대조 통과:** §0~§25 전체, 정본 22개 및 132개 source pointer, 원문·정규 기대값과 필수 9개 필드, ASM 30·AINV 24·AEVAL 30·AMUT 24의 연속 ID, 11개 YAML 제안의 파싱 및 중복 키 부재, 49개 출처 link·참조와 Markdown fence를 확인했다. 등록 입력 7개·봉인 8개의 Git blob도 재계산해 일치했다. 이는 문서·입력 검사 결과이며 AEVAL/AMUT·실제 22개 업무 실행 결과가 아니다.

### 0.2 근거의 종류

- **승인 입력 사실:** [I01]~[I12]. 입력 사용 범위와 expected 값의 권위다. 원천 provenance로 선언된 commit은 `c1710fc2d96ff0c3161231377dfeef303ab5983b`이며, 이번 세션은 승인 사본의 blob을 검증했다. 금지된 다른 workstream·evidence 원문을 새로 읽어 원천 실행을 재검증한 것은 아니다.
- **규격·제품 사실:** Agent Skills, Claude Code, OpenAI Agents SDK, LangGraph, MCP 및 상태·패키징 관련 공식 자료. 문서에 있는 기능과 Factory에서 실제 활성화된 기능을 구분한다.
- **연구 관찰:** Anthropic 연구 시스템 사례와 MAST 원 논문의 실패 분류. 특정 실험의 수치·agent 수·비용을 보편 기준으로 옮기지 않는다. [P01], [P02]
- **Assembler 연구 제안:** 이 문서의 규칙, 보조 스키마, 매핑의 추가 결정, 권한 교집합, digest 참조 방향, 설치·복구 설계. 제품이 자동 제공하거나 upstream이 개별 승인한 필드라고 주장하지 않는다.

입력 기준 head는 `e2e1628b7070e314f59f49cb03f435d47dd29abb`, 총괄 정책·할당 확인은 `42e06122d738a590fc516cccd28327de42f15743`다. 해당 입력 head의 boundary run `45529919670` 성공을 확인하고 착수했다. 입력·경계·상태 확인 뒤 쓰기는 OWNERSHIP의 네 경로에만 한정한다. [I06], [I09], [I10], [I11]

이전 로컬 초안의 동일 바이트는 복구하지 못했다. 이 브랜치의 보고서 경로 이력도 비어 있었으므로 과거 보고서의 digest·규칙 수량·검증 주장을 재사용하지 않았다. 이번 보고서는 새 승인 입력과 다시 확인한 출처로 작성한 제출본이다.

### 0.3 버전과 재현성

| 자료 계열 | 확인 기준 | 한계 |
|---|---|---|
| Agent Skills | commit `83021e2be457a9b6679148719c1f6074f0ad975e` | 규격·scripts·evaluation 원문을 고정해 읽음 |
| Claude Code | release `v2.1.332`, tag commit `eb8e6d253d0dbee6e52fb0d5fdcb72c9396fe3e8` | 제품 문서는 live/unversioned이며 release tag가 문서 전체 snapshot을 의미하지 않음 |
| OpenAI Agents Python | `v0.26.0`, commit `0ad2d63a9371a23333a95ea6878141a826c9cdda` | 문서를 해당 commit에서 대조; SDK 런타임 실행은 하지 않음 |
| LangGraph | 2026-11-26 live 공식 문서 | 설치 버전·실제 host 동작 미검증 |
| MCP | 명세 `2026-07-28` | 구버전 세션 방식·새 요청 방식 혼합 금지 |
| 공급망·상태 | SLSA v1.2, in-toto Statement v1 고정 commit, TUF v1.0.36, SCXML 2015 Recommendation, RFC 8785 | Factory에 실제 도입했다는 뜻이 아님 |

전체 URL·접근일·pin은 §25에 둔다. [S01], [S02], [S03], [C06], [O08], [M01], [D02], [D04], [D05], [D06], [D07]

## 1. Assembler 책임·비책임

**승인 입력:** 이미 선택·승인된 component만 조립한다. 새 코드·RAG·Tool·Agent를 직접 만들지 않으며 Skill이 선택되지 않으면 Skill Author를 호출하지 않는다. [I01], [I03]

**연구 제안:** Assembler의 산출물은 구성 간 연결과 적격성 판단을 담는 계약·manifest다. 다음 역할을 분리한다.

| Assembler가 작성할 것 | 참조·검증할 것 | 소관으로 돌려보낼 것 |
|---|---|---|
| entrypoint와 control owner, component binding, 상태·handoff 정책 | 승인된 plan 및 Gate/Execution/Knowledge 계약 | capability·component·제어 모드 변경 → Planner |
| package inventory, dependency/version map, 설치·검토 handoff | 기존 Skill/Script/Validator/Tool/Reference/Agent 정의와 실제 digest | 새 실행기·adapter·오류 변환 코드 → Execution |
| 전체 조합 평가 요구, 부적격·stale·unsupported 이유 | 해당 subject·version에 결박된 component evidence | hard Gate·승인·권한 정책 충돌 → Gate |
| 결과·제한·다음 단계의 구조화 기록 | 지식 출처·snapshot·ACL·citation 계약 | 검색·freshness·권한·근거 계약 변경 → Knowledge |

입출력 필드의 이름만 맞추는 rename이라도 의미·권한·오류 해석이 바뀌면 adapter 생성으로 볼 수 있다. 승인된 adapter가 이미 있는 경우에만 결박하며, 편의상 임의 wrapper를 만들지 않는다. 동일 Tool의 alias를 명확히 하는 EVAL-18에서도 실제 기능·scope가 다르면 통합 허가가 생기지 않는다.

단순 응답에는 package 자체가 불필요할 수 있다. `components=[]`는 결함이 아니며 EVAL-01·13의 정상적인 최소 구성이다. EVAL-22도 빈 구성이지만 정책 없는 구매 행동은 차단한다. component 개수와 행동 허용 여부를 별도로 판단한다. [I04], [I05]

## 2. 입력 계약과 source of truth

### 2.1 승인 입력을 읽는 순서

현재 지시·소유 경계·상태·승인 manifest를 먼저 읽고, manifest가 지정한 blob과 실제 파일 내용을 대조한다. 같은 경로라도 digest가 달라지면 새 입력이다. 과거 승인을 새 내용에 자동 적용하지 않는다. 중복 담당 여부는 공유 board와 workstream 상태를 확인한 후 착수 기록으로 남긴다. [I02], [I06], [I07], [I08], [I09]

| 이번 입력 | 역할 | 승인 범위 |
|---|---|---|
| 시작 지시·Remote Research Mode·Work Order·Ownership | 작업·수정·조사 경계 | 원격 조사 및 허용 산출물 |
| UPSTREAM_CONTRACT_SUMMARY | 상위 책임·재진입 원칙 | 고수준 계약; 현재 전체 구현의 실행 증거 아님 |
| PLANNER_EVALS_01_22.json | 요청·기대 아키텍처·판정 근거·틀린 선택 | EVAL-01~22 원문 |
| PLANNER_SCENARIO_RESULTS_22.json | `base[].id`, `source_title`, `expected_control_mode`, `expected_components` | §19 정규화 기대값만 사용; status/paraphrases는 증거에서 제외 |

**§19의 연구 입력은 충족되었다.** 개별 CAPABILITY_PLAN 전체 출력·실제 22회 trace·개별 승인 attestation은 이번 매핑의 선행 조건이 아니다. 이후 실제 package/실행/release가 exact capability ID, AC ID, Gate ID, permission, artifact digest를 요구할 때만 부족한 구체 자료를 `PLANNER_REENTRY_REQUIRED`로 반환한다. 이 경계를 현재 연구의 blocker로 되살리지 않는다. [I02], [I08]

### 2.2 정본과 파생물

정본 expected 값과 연구로 도출한 값은 서로 다른 필드에 저장한다. §19의 네 canonical 필드는 자동 추출하며, 연구 필드를 upstream 승인 필드처럼 덮어쓰지 않는다. 원문의 여러 대안과 정규화 기대 component set 사이의 차이는 설명하되 합집합으로 늘리지 않는다.

후속 구현용 source-of-truth는 승인된 계약과 immutable artifact다. SYSTEM_MANIFEST는 그것을 모아 연결한 파생물이며, 실제 실행·검토 receipt는 더 뒤에서 생성된다. static contract에 미래 결과 digest를 되써서 자기참조·순환 hash를 만들지 않는다. digest 참조 방향은 §14~15의 연구 제안이다. in-toto의 불변 subject digest 및 SLSA의 산출물·실행 provenance 연결을 참고했다. [D04], [D05]

## 3. Control mode별 assembly

아래 네 모드는 Factory 상위 계약의 분류다. 플랫폼 공통 표준 enum이라고 주장하지 않는다. LangGraph가 고정 코드 경로와 실행 중 동적으로 경로를 선택하는 agent를 구분하는 점은 이 분류의 설명에 참고할 수 있다. [I03], [L01]

| mode | entrypoint·제어권 연구안 | 상태·호출 | 종료·오류·승인 | 최소 package |
|---|---|---|---|---|
| `direct_response` | 사용자 입력에서 호스트의 단일 응답 경로 | 현재 입력과 선택된 Skill/Reference만; 자율 반복 불필요 | 답변·근거 없음·정책 질문을 구분; 외부 행동은 별도 선택 없으면 없음 | 빈 구성 또는 선택 Skill/Reference만 |
| `deterministic_workflow` | 호스트의 고정 호출 순서 또는 선택된 Workflow | 명시된 노드·I/O·조건·오류 전이; LLM은 제한된 한 노드 가능 | Validator/Gate 실패에 따라 중단; side effect의 승인·unknown·재시도 분리 | 선택된 component만. mode 이름만으로 Workflow 파일을 만들지 않음 |
| `bounded_agent` | 한 Agent가 관찰에 따라 다음 행동을 선택하고 호스트가 상한 통제 | 선택 Tool·state·trace, 범위·예산·취소 정책 | 목표 충족·예산 소진·관찰 부족·승인 대기 등 명시 | 승인된 단일 Agent 및 선택 부품 |
| `multi_agent` | coordinator가 분배·검증·합성 책임을 소유 | 각 worker 최소 context, 고정 배정, 구조화 결과 | verifier 불합격·부분 완료·충돌을 보존; 재귀·무한 handoff 방지 | 필요한 역할만, source-group 수를 동시 Agent 수로 단정하지 않음 |

정규화 기대값의 분포는 direct_response **6**, deterministic_workflow **12**, bounded_agent **3**, multi_agent **1**이다. EVAL-04/05/06/08/15/16/19에는 deterministic mode가 있지만 `workflow` component가 없다. 이 경우 설명하는 고정 제어 경로는 연구 설계이며, 실제 호스트에 존재한다거나 새 Workflow artifact를 추가할 권한을 뜻하지 않는다. [I05]

승인된 component의 내부 동작이나 기존 host 제어 경로로 충족할 수 없는 요구는 재진입 대상이다. 예를 들어 EVAL-10의 고정 큐 dispatch에 새 Tool이 필요하다고 밝혀지면 기대 set에 Tool을 조용히 넣지 않는다.

## 4. Skill·Command·Agent·Workflow 결정표

**제품 사실:** Agent Skills는 SKILL.md와 선택적 보조 자원을 정의한다. Claude Code에서는 custom command가 skills로 통합되어 있으며 기존 command 파일도 지원한다. 이 사실은 같은 capability를 Skill·Command 두 개로 복제해야 한다는 뜻이 아니다. [S01], [C01]

| 조건 | 조립 연구안 | 제외 또는 재진입 기준 |
|---|---|---|
| 반복 절차만 필요, Skill 선택 | Skill의 호출 조건·본문·출력 계약을 연결 | Agent/Hook/Script를 관습적으로 추가하지 않음 |
| Skill과 Script가 모두 선택 | Skill은 사용 절차, Script는 결정적 변환, Validator는 객관 판정 | 같은 계산·검증을 LLM 지시로 이중 구현하지 않음 |
| 안정된 자료가 선택 | Reference inventory와 버전/위치 연결 | 작은 코퍼스만으로 RAG 추가하지 않음 |
| Skill+Agent가 실제 선택 | Skill fork와 Agent preload 중 어느 쪽이 prompt·제어권을 소유하는지 선언 | 두 방식 중첩에 따른 중복 실행·context 오인 검사 |
| Agent만 선택 | standalone Agent의 정의·도구·종료 경계만 결박 | Skill Author를 호출하지 않음 |
| 수동 실행만 허용 | 사람이 시작하는 invocation 경로를 명시 | 모델 자동 호출 설정과 사람 노출 설정을 같은 것으로 취급하지 않음 |
| 고정 처리 중 LLM 판단 한 노드 | Workflow 또는 고정 호스트 경로가 제어권 유지 | LLM 사용을 이유로 agent loop 추가하지 않음 |
| 병렬 격리·검증 요구 | 승인된 multi-agent 역할과 merge 계약 | reviewer라는 이름만으로 독립 신원·권한을 검증했다고 하지 않음 |

Claude의 `context: fork`는 새 subagent에 Skill 내용을 전달하는 동작이며 현재 대화 이력을 그대로 복제하는 conversation fork와 다르다. Agent preload는 Agent 정의가 prompt를 소유한 채 Skill 내용을 시작 context에 넣는 방식이다. 누락·정책 제한으로 preload가 생략될 수 있으므로 선언과 실제 로딩을 구분해야 한다. [C01], [C02]

또한 `allowed-tools`는 Skill 호출 turn의 사전 허용이며 권한 상한이나 도구 제거 목록이 아니다. 실행 가능 Tool inventory, 실제 permission 설정, credential scope를 따로 대조한다. Claude 전용 frontmatter를 다른 host가 동일하게 강제한다고 가정하지 않는다. [C01], [C04]

## 5. Component interface와 typed binding

**연구 제안:** component의 이름만 같거나 schema가 parse된다는 이유로 호환이라고 판정하지 않는다. binding에는 artifact identity, 승인 source, content digest, 인터페이스 버전, 입력·출력 schema, 오류 의미, side-effect 종류, 런타임 적격성, 실제 evidence의 적용 범위를 연결한다. component별 통과 결과와 특정 버전 조합의 호환성은 다른 문제다. Pact의 소비자·제공자 버전 조합 검증을 참고하되 권한·업무 결과를 대신하는 검사로 쓰지 않는다. [I03], [D03]

| binding 영역 | 후속 구현에서 필요한 내용 | 생략·오해 시 위험 |
|---|---|---|
| 정체성 | artifact ID/type/version/digest, Tool server/operation, Script entrypoint | 같은 이름의 다른 Tool·다른 소스 실행 |
| 의미·형식 | I/O schema, 필수 필드, 단위·시간대·오류/빈 결과 의미 | 타입은 맞아도 단위·unknown 해석이 달라짐 |
| 권위 | plan의 capability/AC 연결, Gate policy, 허용된 호출 주체·범위 | 선언만으로 권한 확대 |
| 적격성 | READY_FOR_ASSEMBLY 등 실제 upstream 상태와 증거 subject | scaffold를 실행 적격으로 오인 |
| 실행·복구 | timeout, retry 조건, idempotency, reconciliation, 취소 | 중복 쓰기·결과 불명 은폐 |
| 지식 | source/snapshot/version, ACL·freshness·citation 계약 | 오래되거나 권한 없는 자료 사용 |

이 표는 향후 exact binding 요구다. §19에 아직 없는 capability/AC/Gate ID나 digest를 임의 생성해서 채우지 않는다. 조사 기록의 `DEFERRED_TO_IMPLEMENTATION`과 실제 실행 계약의 “필수 값 누락”을 별도 상태로 다룬다. [I02]

결과 envelope에는 정상값과 함께 `NO_EVIDENCE`, `CONFLICT`, `BLOCKED`, `ERROR`, `OUTCOME_UNKNOWN`, `CANCELLED` 같은 의미를 보존하도록 제안한다. `exit_code=0` 또는 자유문자 PASS를 업무 완료의 유일 조건으로 삼지 않는다. model tool 호출이 있었을 때만 model call ID를, 실제 transport 요청이 있었을 때만 transport request ID를 요구한다. direct response에 가짜 tool receipt를 만들지 않는다. [I01], [I03]

MCP Tool은 입력 schema와 선택적 출력 schema를 가지며 annotation은 신뢰할 수 있는 서버가 아니면 비신뢰로 다루어야 한다. Tool 이름의 유일성도 서버 내부 범위이므로 server name 문자열 하나로 전역 identity를 구성하지 않는다. **제안:** 실제 연결 대상·operation·schema/version을 결박하고, schema resolver는 승인된 로컬 참조 범위와 크기·깊이를 제한한다. 후자의 resolver 제한은 이 보고서의 설계안이다. [M02]

## 6. Context engineering·progressive disclosure

**제품 사실:** Agent Skills는 메타데이터에서 활성화된 본문, 필요한 보조 자원으로 이어지는 점진적 접근을 설명한다. Script는 선택 자원이며 기존 패키지로 충분하면 별도 scripts 디렉터리 없이 참조할 수도 있다. 이를 모든 package가 Script·Reference를 반드시 포함해야 한다는 규칙으로 바꾸지 않는다. [S01], [S02]

**연구 제안:** context는 다음 네 층으로 구성한다. 이 층은 data의 권위와 실행 권한을 혼합하지 않기 위한 설계다.

1. **고정 계약:** 목표·성공 기준·호출 가능 범위·정책 참조. 입력 정본의 digest를 유지한다.
2. **현재 단계 입력:** 해당 노드나 worker에 필요한 필드만 전달한다. 전체 사용자 이력이나 모든 도구 출력을 복제하지 않는다.
3. **근거:** 원문 위치·source version·ACL 판정·조회 시각과 필요한 span. 요약과 원문 참조를 함께 둔다.
4. **진행 기록:** 완료 항목, 미결 사항, pending call, 사용 예산, 다음 허용 전이. runtime record로 저장하며 static 계약을 수정하지 않는다.

Skill 본문에는 호출 조건·절차·예외·출력 계약을 두고, 안정 자료와 긴 예시는 references로 분리한다. 선택되지 않은 Reference component를 이런 패키징 편의 때문에 새로 추가하는 것은 허용하지 않는다. 본문의 과다 복제와 보조 파일 누락을 함께 검사한다. [I03]

Tool·retrieval 결과는 데이터로 표시하고, 그 내용이 상위 권한·승인·작업 범위를 바꾸지 못하도록 consumer boundary를 설계한다. data-only marker 자체를 injection 방어 완료로 취급하지 않는다. context budget은 host/model·과업별로 정하고 절단 시 필수 근거·pending 상태의 유실 여부를 탐지한다. 용량 초과면 요약·재조회·부분 결과로 전환하되 권한·정확한 승인 payload·미결 부작용을 삭제하지 않는다.

handoff summary에는 원 요청 참조, 담당 범위, 완료/미완료, claim→evidence 연결, conflict/no-evidence, 사용 권한·정책 버전, 남은 예산, 다음 허용 행동을 제안한다. 새 worker에게 전달할 것은 이 structured projection이며, 모든 worker가 전체 입력을 열람한다는 뜻이 아니다. 원본 evidence의 digest와 접근 범위를 별도로 보존해 isolation과 추적성을 함께 확보한다.

메모리·checkpoint는 필요한 경우에만 선택한다. EVAL-17의 state는 사용자 선호의 목적·조회·수정·삭제를 위한 것으로, 전체 대화를 무기한 저장하는 허가가 아니다. OpenAI sessions는 history를 유지하지만 session ID나 기본 SQLite 저장 자체가 사용자 인증·무결성 보증은 아니다. [I04], [I05], [O05]

## 7. Tool·Execution·Knowledge binding

**승인 입력:** Executor와 Knowledge layer의 typed entrypoint를 사용하며 raw DB credential·vector store·low-level credential을 Agent에 직접 노출하지 않는다. Knowledge의 권위·ACL·freshness·citation 계약을 넓히지 않는다. [I01], [I03]

**연구 제안:** 호출 경계에는 다음 순서를 적용한다. 실제 부품이 없으면 prompt로 흉내 내지 않고 해당 생성기로 반환한다.

| 단계 | 연결할 검사 | 실패 처리 |
|---|---|---|
| dispatch 전 | actor/tenant/task scope, artifact version/digest, schema, read/write 성격, 적용 Gate | 호출 차단·명확한 재진입 사유 |
| side effect 직전 | exact approval과 현재 payload, credential·runtime enforcement | 승인/정책/입력 변화 시 재검증; 권한 부족을 LLM 약속으로 보완하지 않음 |
| 결과 수신 | schema와 실제 outcome, source·시각·부분 처리, call/result 대응 | unknown·conflict·partial을 성공으로 바꾸지 않음 |
| 완료 전 | 업무 acceptance, 교차 component binding, evidence의 적용 subject | component 통과만으로 system 완료하지 않음 |

MCP는 2026-07-28 명세에서 self-contained stateless 요청과 요청별 capability negotiation을 정의한다. Resource는 문맥 데이터, Prompt는 템플릿, Tool은 호출 가능한 기능이다. Resource/Prompt를 읽었다고 Tool 실행 권한을 획득한 것은 아니다. HTTP authorization을 사용하는 서버의 access token은 대상 audience를 검증해야 한다. [M01], [M02], [M03], [M04], [M05]

Knowledge 결박에서는 검색 전에 원 사용자·tenant·부서의 ACL을 적용하고, source authority와 retrieval rank를 구분한다. 원문·index·cache의 freshness를 따로 추적한다. 삭제·정정·권한 철회 후 오래된 cache가 근거를 되살리지 않도록 무효화 의미를 계약으로 둔다. claim-level citation에는 정확한 문서 version·span을 보존하고, no-evidence는 abstention으로 전달한다. 이 정책은 승인된 상위 Knowledge 원칙을 Assembler 경계에 적용한 연구안이다. [I03]

대표 차이는 EVAL-03/07의 고정 Reference, EVAL-06의 ACL·citation을 갖춘 RAG, EVAL-08의 live ERP Tool, EVAL-19의 버전별 공식 문서 Tool이다. 네 경우 모두 “지식이 필요하다”는 이유로 같은 RAG architecture를 적용할 수 없다. [I04], [I05]

direct bypass inventory에는 일반 Tool 외에도 Script의 하위 호출, Skill의 inline shell, nested agent tool, state 접근 경로, 재개·관리 API를 포함하도록 제안한다. inventory는 새 component를 추가하라는 지시가 아니라 기존 경로에 Gate가 적용되는지 확인하는 자료다. OpenAI agent-level input/output guardrail이 중간의 모든 실행 경로를 덮는다고 가정하지 않는다. [C01], [O02], [O04]

## 8. Permission·approval·handoff

**연구 제안:** 유효 권한은 `원 사용자 허용 범위 ∩ 현재 과업 범위 ∩ 원 component ceiling ∩ 수신 component ceiling ∩ 현재 host/credential policy`의 교집합으로 정의한다. 이 모델은 Factory의 권한 확대 금지 원칙을 표현한 설계이며 SDK나 MCP가 모든 Agent handoff에 자동 제공하는 기능이 아니다. [I03], [M05]

exact approval은 actor·tenant·환경·실제 executor·목표·operation·정규화 payload·정책 version·만료·사용 횟수와 결박한다. 승인된 요청의 내용이 바뀌면 기존 승인을 그대로 적용하지 않는다. EVAL-14에는 SQL/조건/대상 preview와 복구 전제, EVAL-15에는 최종 수신자 집합/제목/본문/배치 범위를 포함한다. 승인 digest와 업무 idempotency key는 목적이 달라 별도 보존한다. [I03], [I04], [D01]

**제품 사실:** OpenAI handoff는 수신 agent로 제어를 이전하고 기본 history를 전달한다. manager가 제어를 유지하는 agents-as-tools와 구분해야 한다. history nesting은 redaction이 아니므로 최소 정보 전달이 필요하면 적절한 input filter와 별도 경계를 선택한다. [O01], [O03]

OpenAI `RunState` 복원은 snapshot 또는 제출자의 인증이 아니다. 서버 소유 pending 상태, reviewer 인증·인가, 저장된 call과 제출 decision의 대조, 중복 resume을 막는 원자적 consumption이 application 책임으로 문서화되어 있다. **제안:** 실제 승인 payload·policy·artifact가 바뀐 resume은 재승인을 요구하며 tool 이름 수준의 sticky approval로 고위험 exact approval을 조용히 대체하지 않는다. [O07]

| handoff 검사 | 보존할 것 | 금지할 승격 |
|---|---|---|
| identity | original user·tenant·task owner·acting agent | agent 이름을 사람 승인 identity로 사용 |
| authority | 실제 scope 교집합·승인 범위·만료 | 이전 agent가 도구를 볼 수 있었다는 이유로 수신 권한 확대 |
| evidence | claim/source digest·pending/unknown·검증 결과 | 요약에서 실패·부분 완료를 삭제 |
| control | 수신자·제어권 이전/반환·종료·cycle 상한 | 암묵적 재귀 delegation 또는 이중 control owner |
| review | creator와 reviewer의 실제 접근·권한·독립성 | 같은 실행 주체의 다른 역할 이름을 독립 attestation으로 표현 |

API key 등의 credential은 모델·chat·state·trace를 통과시키지 않는 외부 입력 경로로 연결한다. MCP form elicitation은 이런 비밀을 요청하면 안 되며 URL mode를 사용해야 한다. URL을 수락한 것과 서비스 연결이 실제 완료된 것은 다르다. EVAL-16은 이 경계를 충족하는 승인 경로를 요구하는 연구 매핑이지 자격 증명을 수집·저장한 결과가 아니다. [M06]

## 9. State·checkpoint·parallel·recovery

**연구 제안:** 상태·전이·guard·entry/exit 동작을 명시하고 허용하지 않은 전이는 차단한다. 성공 외에 blocked, failed, cancelled, partial, outcome unknown을 구분한다. 상태 머신의 명시적 전이 개념은 SCXML을 참고하지만, §15의 YAML이 SCXML 호환 실행 엔진이라는 뜻은 아니다. [D02]

| 관심사 | 조립 요구 | 반드시 구분할 것 |
|---|---|---|
| call/result | 실제 호출 ID, attempt, 결과 상태의 대응 | 미발행 call에 붙은 orphan result, retry attempt 혼합 |
| checkpoint | 입력·정책·정의 version과 실행 cursor | checkpoint 존재와 외부 쓰기 완료 |
| resume | 현재 identity·승인·artifact·지식/권한 상태 재검사 | 과거 승인·권한을 현재에 무조건 재사용 |
| retry | 재시도 가능 오류와 부작용 의미, key 재사용 정책 | 새 업무 의도와 같은 업무 재시도 |
| 취소 | 수신 확인·진행 중 호출·미결 부작용 기록 | 사용자 화면 종료와 외부 실행 중단 |
| compensation | 확인된 효과와 가능한 복구 범위 | 무조건 rollback 가능하다는 약속 |

LangGraph의 checkpoint는 외부 provider의 side effect까지 한 트랜잭션으로 포함하지 않는다. 응답 확인이 유실되면 실제 효과가 발생했을 수 있으므로 provider 상태 조회·대조가 필요하다. interrupt 재개는 노드 처음부터 다시 실행될 수 있다. 따라서 승인 이전의 비멱등 부작용, retryable 노드 안의 외부 쓰기, 재개 시 반복될 subgraph 호출을 따로 검토한다. [L02], [L03], [L05]

`OUTCOME_UNKNOWN → RECONCILE → 확인된 성공/실패/부분 결과`는 반드시 표현한다. retry를 비활성화해도 결과 불명 문제는 사라지지 않는다. provider가 업무 key를 실제로 존중하는지 검증하고 같은 key로 다른 payload를 보내는 경우를 오류로 취급하는 계약을 제안한다. reconciliation이 불가능하면 확인되지 않은 효과를 숨기지 않고 중단·사람 검토로 남긴다. [D01], [L05]

병렬 작업은 동일한 root snapshot에서 worker별 최소 입력 projection을 고정하고, 배정된 source 범위·출력 위치·schema를 분리한다. merge는 도착 순서나 마지막 쓰기에 의존하지 않고 ID 정렬·중복 처리·충돌 판정 규칙을 명시한다. EVAL-12의 12개 source group은 12개 동시 worker를 요구하지 않는다. 관측 가능한 독립성·원문 검증·merge가 핵심이다. [I04], [P01], [P02]

LangGraph의 per-invocation subgraph state와 per-thread 누적 state는 다르며, 공유 stateful subgraph를 병렬 호출하면 checkpoint namespace가 충돌할 수 있다. **제안:** 독립 연구 worker에는 호출별 격리를 우선 검토하고, 공유 writer나 stale worker가 실제로 존재하는 경로에는 lease뿐 아니라 수신 측 fencing/version check를 둔다. 단일 direct response에 불필요한 분산 locking을 요구하지 않는다. freeze·merge·fencing은 자동 runtime 보장으로 선언하지 않는다. [L04]

## 10. Package layout·install·upgrade·rollback

**연구 제안:** package는 선택된 부품을 참조하는 manifest를 중심으로 구성한다. 거대한 SKILL.md로 모든 규칙·코드·지식·권한을 복제하지 않는다. 아래는 조건부 layout 예시이며 이번 세션이 생성한 실제 설치 package 목록이 아니다. [I01], [S01]

| 후보 경로/문서 | 포함 조건 | 내용·소유 경계 |
|---|---|---|
| SYSTEM_MANIFEST, ASSEMBLY_CONTRACT | package가 필요한 조립 | immutable 계약·component digest·의존성; 자기 digest는 외부 descriptor |
| COMPONENT_BINDINGS, ENTRYPOINT_MANIFEST | 호출·참조 관계 존재 | 승인된 부품과 실제 entrypoint만 |
| SKILL.md 및 해당 references/assets | Skill이 선택되고 그 보조 자원이 승인됨 | Skill Author의 승인 산출물을 참조; 무조건 재생성하지 않음 |
| agents 정의 | Agent가 선택됨 | 역할·prompt·도구·권한 ceiling·종료; 이름만으로 독립성 주장 금지 |
| scripts/workflow 정의 | 해당 component가 선택됨 | 기존 승인 artifact를 결박; mode만으로 파일 추가 금지 |
| knowledge descriptor | 지식 component가 선택됨 | snapshot·scope·citation 참조; secret·전체 index 복제 금지 |
| settings fragment/activation request | 실제 host 설정이 필요한 경우 | 제안·검토 대상. 자동 적용하지 않고 owner 승인·활성 검증 분리 |
| eval/attestation 참조 | 해당 단계가 실제로 수행됨 | 설계된 평가와 실제 receipt를 별도 보존 |

install은 package descriptor 검증→목표 소유권·현재 digest 확인→변경안/backup→동일 대상에 적용→read-back·entrypoint 확인 순서로 제안한다. user-owned 파일은 기본적으로 보존하며 generated 파일도 이후 사용자 수정이 있으면 자동 덮어쓰지 않는다. 경로의 relative 해석·허용 root·symlink를 검사하고, check와 apply 사이 대상 교체를 막을 수 있는 원자적·identity-bound 적용 방식을 요구한다. 사전 경로 검사만으로 race가 해결됐다고 주장하지 않는다.

동일 package·입력·환경에서 install을 재실행할 때 불필요한 diff가 생기지 않도록 idempotency를 정의한다. schema migration은 원/대상 version, 호환 범위, 사용자 데이터 보존, 실패 복구를 명시한다. 기존 package와 공존할 때 Skill/Command/Agent 이름 충돌과 의존성 충돌을 확인한다. rollback/uninstall은 이번 설치가 실제로 소유·변경한 대상에만 적용하고, 설치 후 사용자 편집을 지우지 않는다.

TUF의 metadata 검증은 버전·만료·서명·snapshot 일관성을 다루지만 실제 설치 행위는 application 영역이다. 따라서 공급망 무결성 확인을 사용자 파일 보존·설정 활성·업무 rollback 성공으로 승격하지 않는다. archive 형식이 필요할 때만 별도로 extraction 경계·리소스 상한·staging을 정의하며, 패키징하지 않은 direct response에 archive installer를 만들지 않는다. [D06]

## 11. Observability·evidence·attestation

**연구 제안:** “어떤 요청이 어떤 component와 정책으로 무엇을 시도했고 실제로 무엇이 확인됐는가”를 재구성할 수 있어야 한다. request/run/parent/attempt 식별, immutable input·artifact·policy 참조, 호출·결과, 승인/거절/취소/unknown, Gate와 acceptance 판정, 시각·checker identity·한계를 연결한다. trace가 선택되지 않은 정적 응답에 새로운 tracing component를 조용히 추가하지 않는다. 필요한 증거 요구가 선택 구성으로 충족되지 않으면 재진입한다. [I01], [I03]

제품 trace는 observation이며 승인 또는 독립 attestation과 동일하지 않다. OpenAI tracing에는 민감한 generation/function 입출력이 담길 수 있고, processor는 독립 관찰자여서 앞선 redactor 실패가 뒤 exporter를 자동 차단하지 않는다. **제안:** 최소 수집·저장 범위·retention을 정하고, 필요한 경우 redaction과 전달을 application이 소유한 동일 export 경계에서 처리한다. 실패 로그에는 원문 secret을 다시 싣지 않는다. [O06]

SLSA의 build provenance는 산출물과 build definition·실행 정보·의존성을 연결하며, in-toto Statement는 불변 subject를 digest로 지칭한다. 이를 참고해 checker가 판단한 subject와 현재 package가 같은지 확인하도록 제안한다. digest만 맞아도 신뢰 발급자·정책·검토 독립성·적격성 검사가 빠지면 승인 attestation이 아니다. [D04], [D05]

| 증거 유형 | 표현할 수 있는 주장 | 표현하면 안 되는 주장 |
|---|---|---|
| 정적 기대값 catalog | 이 시나리오의 승인된 기대 mode/set | 실제 Planner/Assembler 실행 성공 |
| 이 보고서의 source/문서 검사 | 입력 일치·매핑 누락 없음·형식/참조 적합 | host enforcement·SDK run·외부 업무 완료 |
| 실제 component 테스트 receipt | 지정 component/version/조건의 결과 | 다른 version·통합 조합·production 적격 |
| 실제 조합 E2E 결과 | 지정 entrypoint·환경·권한·입력의 관측 결과 | 미실행 경로·다른 tenant·미검증 복구 보장 |
| 신뢰 발급자의 attestation | 해당 subject/policy 범위의 판정 | 별도 운영 승인·사람 merge 승인 자동 대체 |

contract와 static 정책을 먼저 고정하고, manifest는 그 digest를 모으며, 실제 실행·설치·평가 receipt가 manifest를 참조하도록 한다. receipt의 hash를 이미 고정된 contract 안에 되쓰지 않는다. workflow의 업무 반복 cycle과 digest dependency cycle은 서로 다른 개념이다. 전자는 bounded 상태 전이로 설계할 수 있어도 후자는 content-addressed 산출물 계산을 불가능하게 하므로 금지한다.

hash 대상은 정확한 바이트인지 canonical serialization인지 명시해야 한다. RFC 8785는 JSON 표현을 정규화하는 방법을 정의하지만 일반 JSON dump를 사용했다는 이유만으로 JCS 준수라고 할 수 없다. **이번 제출 보고서의 SHA-256은 UTF-8 파일 바이트 기준**이며, 승인 입력의 Git blob SHA-1과 혼동하지 않는다. manifest 자체의 digest를 자기 본문에 넣지 않는다. [D07]

## 12. Eval·mutation·ablation·release

**제품 사실:** Agent Skills 평가 지침은 실제 사용자형 prompt·expected output을 만들고 Skill 사용/미사용 또는 이전 버전을 실제로 실행해 비교하는 흐름을 설명한다. MAST는 다중 agent 실패를 체계적으로 분석한 연구이며, 그 실패 분류는 조립 평가의 위험 목록을 만드는 데 참고한다. 이 자료가 현재 Factory의 실패율·성공률을 입증하는 것은 아니다. [S03], [P02]

**연구 제안:** 평가를 네 층으로 분리한다.

| 층 | 검증할 대상 | 이번 수행 여부 |
|---|---|---|
| 입력·문서 | 승인 source digest, exact ID join, canonical field, 필수 필드·ID·schema syntax, 출처 | 실제 정적 검사 수행; §0과 manifest에 범위 기록 |
| component | 실제 Script/Tool/Skill/Knowledge의 입력·출력·권한·오류 | `NOT_RUN` |
| assembly E2E | 사용자가 실제 쓰는 entrypoint에서 정상·경계·오류·악성 경로 | `NOT_RUN` |
| 배포·운영 | 실제 host 활성·설치·복구·독립 attestation·운영 권한 | `NOT_RUN` / 승인 범위 밖 |

이번 문서의 사용자 진입점은 **기존 PR #2 → 변경 파일 → 조사 보고서 §19**다. 제출 후 같은 PR head를 다시 읽어 report bytes·digest·22개 기록·manifest 연결을 대조한다. 이 read-back 검사는 보고서 전달 경로의 검사이며, §19에 설계한 업무 entrypoint의 실행 시험이 아니다. GitHub 화면 렌더링이나 실제 Claude UI를 조작했다고 표현하지 않는다.

후속 구현 E2E에서는 각 매핑의 실제 진입점을 사용해야 한다. 예를 들어 EVAL-04는 승인 CSV 입력에서 오류 행과 결과 파일까지, EVAL-06은 서로 다른 주체의 질문에서 ACL·citation 결과까지, EVAL-14/15는 안전한 시험 환경의 preview·승인·쓰기·결과 불명·대조까지 확인한다. 문서 checker를 직접 호출한 결과를 이 사용자 경로의 성공으로 대신하지 않는다.

평가 세트에는 no-code/no-agent/no-RAG near-miss, stale dependency, orphan result, skipped Gate, permission/Hook unavailable, ACL leakage, approved payload 변조, 부분 실패, 재개·취소·replay, 설치 후 사용자 변경을 포함한다. immutable source와 별도의 평가 oracle을 유지한다. creator의 설명을 그대로 판정문으로 복사하지 않는다.

mutation은 입력·정책·binding·상태·증거를 하나씩 깨뜨려 예상 Gate가 실제로 거절하는지 보는 후속 실험 설계다. ablation은 승인된 최소 기준선과 특정 선택 component를 제거한 실험을 비교해 필요성을 평가한다. runtime 안전 통제를 제거한 실험은 격리된 시험 환경으로 제한하며 승인 없는 실운영 제거를 뜻하지 않는다. §17~18의 모든 실행 상태는 `NOT_RUN`이다.

local assembly 완료, 독립 연구 검토, local candidate 검증, production release는 각각 다른 결정이다. 이 연구는 결과를 검토 가능한 형태로 제출하며 PR을 Draft로 유지한다. 사람 merge 승인·운영 설정 활성·배포를 실행하지 않는다. [I01], [I06], [I07]

## 13. 공통 규칙: ASM-01 ~ ASM-30

다음 30개 규칙은 **Assembler 연구 제안**이다. 근거 문서의 기능 설명과 Factory에 적용할 규칙을 구분한다. `검증`은 향후 검사 방법이며, 이 절의 작성 자체는 runtime 검증이 아니다. §19의 승인된 기대값으로 작성하는 연구 매핑과 실제 package 실행·배포 승인은 별도다.

### ASM-01 — 승인 입력과 착수 주체 고정

- 적용 조건: 조사 재개 또는 입력 변경.
- 행동: 현재 head·manifest·승인 목록·담당 상태를 대조한다. 같은 작업이 실행 중이면 중복 착수하지 않는다.
- 검증: 등록 경로의 실제 digest와 승인값을 비교; AINV-001, AEVAL-001.
- 실패 시: 입력 누락·불일치는 `BLOCKED_FOR_SOURCE`; 담당 충돌은 실행하지 않고 상태 보고.
- 강제 계층: 작업 조정자, 입력 검사기, branch head 조건부 갱신.
- 근거: [I01], [I02].
- 예시: 승인된 새 Planner 2개 입력을 재검증하고 이전 source blocker를 해제.
- 반례: 오래된 manifest의 READY나 다른 담당의 착수 기록을 무시하고 시작.

### ASM-02 — mode와 component를 각각 보존

- 적용 조건: 승인된 control mode·component set 소비.
- 행동: 두 값을 독립적으로 보존한다. deterministic mode라는 이유로 Workflow artifact를 추가하지 않는다.
- 검증: 집합 동등성·mode 동등성; AINV-002, AEVAL-002.
- 실패 시: 조용히 수정하지 않고 `PLANNER_REENTRY_REQUIRED`.
- 강제 계층: contract compiler와 구성 차이 검사.
- 근거: [I01], [I03], [I05].
- 예시: EVAL-04는 script·validator만 연결.
- 반례: EVAL-08의 tool-only 기대값에 workflow·skill을 덧붙임.

### ASM-03 — 선택된 책임만 패키징

- 적용 조건: Skill·Agent·Reference·Script 배치.
- 행동: 선택된 구성에만 경로를 배정하고, Skill 선택 때만 Skill Author를 연결한다.
- 검증: 생성/참조 inventory와 Planner 구성 대조; AINV-002, AEVAL-003.
- 실패 시: 불필요한 생성 중단 및 Planner 재진입.
- 강제 계층: 생성기 dispatch와 package manifest.
- 근거: [I01], [S01], [S02].
- 예시: EVAL-01은 응답 경로만 사용하며 package component를 생성하지 않음.
- 반례: 모든 요청에 SKILL.md와 agent 파일을 생성.

### ASM-04 — §19의 승인 범위로 매핑

- 적용 조건: Planner golden 22개 연구 매핑 작성.
- 행동: 두 승인 입력을 id로 결합해 원문·정규 기대값을 보존하고, Assembler 결정은 연구 제안으로 표시한다.
- 검증: 정확한 22 ID, 1:1 행, 9개 필드, 원문 동등성; AINV-003, AEVAL-004.
- 실패 시: 누락·변조를 수정하거나 source 재진입. 전체 plan 미제공만으로 §19를 막지 않는다.
- 강제 계층: 연구 문서 구조 검사와 원문 대조.
- 근거: [I02], [I04], [I05].
- 예시: EVAL-07의 architecture 대안을 보존하고 reference-only 정규 기대값으로 조립 제안.
- 반례: 더 편한 architecture로 원문을 고치거나 새 시나리오로 대체.

### ASM-05 — 판정의 대상과 검증 수준 분리

- 적용 조건: 기대값·연구 검토·실행 결과·release 판정 기록.
- 행동: 각 판정에 scope를 기록한다. 입력 PASS를 실행 증거로 승격하지 않고 EVAL-22의 의도된 차단과 세션 blocker를 구분한다.
- 검증: verdict 출처·대상·실행 기록 확인; AINV-003, AINV-024, AEVAL-005.
- 실패 시: 잘못된 성공 주장을 철회하고 해당 검증을 `NOT_RUN` 또는 미확인으로 기록.
- 강제 계층: 결과 schema와 검토 gate.
- 근거: [I02], [I03], [S03].
- 예시: §19 매핑 완료, 시나리오 runtime 0회, EVAL-22 구매 차단 기대.
- 반례: 정적 PASS 22개를 읽고 22-run E2E 성공으로 보고.

### ASM-06 — typed binding과 adapter 재진입

- 적용 조건: component 사이 데이터·호출 연결.
- 행동: I/O schema·status·오류 의미·호환성을 확인하고 승인되지 않은 adapter나 capability를 만들지 않는다.
- 검증: 모든 edge의 producer/consumer 계약 대조; AINV-004, AINV-005, AEVAL-006.
- 실패 시: 담당 Planner·Execution·Knowledge 단계로 재진입.
- 강제 계층: schema 검사기와 contract compiler.
- 근거: [I01], [I03], [M02], [D03].
- 예시: 문자열 응답을 요구하는 consumer에 다른 구조가 오면 명시적 호환 검토.
- 반례: 데이터 손실 adapter를 몰래 삽입하거나 없는 Gate ID를 합성.

### ASM-07 — 현재 artifact에만 판정 결박

- 적용 조건: component·정책·의존성 변경 또는 재개.
- 행동: identity·version·digest·상태·검증 범위를 현재 artifact와 결박하고 영향받는 파생 판정을 STALE로 전환한다.
- 검증: dependency closure와 evidence subject 대조; AINV-006, AEVAL-007.
- 실패 시: 재검증 전 완료·실행 적격 판정 차단.
- 강제 계층: dependency resolver와 evidence gate.
- 근거: [I03], [D03], [D04], [D05].
- 예시: tool digest 변경 후 연결 manifest와 해당 평가를 재확인.
- 반례: 파일 이름이 같다는 이유로 과거 PASS 재사용.

### ASM-08 — 불변 digest 참조 그래프

- 적용 조건: contract·manifest·결과·release 자료의 digest 설계.
- 행동: 입력→계약→manifest→결과→handoff의 단방향 참조를 유지한다. 후속 receipt를 앞선 불변 문서에 되쓰기하지 않는다.
- 검증: hash 참조 DAG와 self-reference 검사; AINV-007, AEVAL-008.
- 실패 시: 순환이 없는 문서 분리·외부 descriptor로 재설계.
- 강제 계층: manifest 생성기와 digest 검사기.
- 근거: [I03], [D04], [D05], [D07]; DAG 배치는 본 연구 제안.
- 예시: static contract에는 요구 조건, 실제 승인·실행 결과는 별도 record.
- 반례: manifest가 자신과 아직 생성되지 않은 결과의 최종 hash를 포함.

### ASM-09 — entrypoint마다 제어권 명시

- 적용 조건: direct response·workflow·agent·병렬 실행 배치.
- 행동: 각 단계의 control owner와 허용 전이를 정한다. agent 호출이 있어도 상위 workflow 제어권을 자동 이전하지 않는다.
- 검증: entrypoint→owner→edge inventory; AINV-008, AEVAL-009.
- 실패 시: 이중 제어·미정의 경로를 차단하고 계약 재검토.
- 강제 계층: entrypoint manifest와 scheduler.
- 근거: [I01], [I03], [O03], [L01], [D02].
- 예시: EVAL-10의 LLM 분류 뒤 큐 선택은 고정 routing 정책 소유.
- 반례: 분류 agent가 큐 정책까지 바꾸거나 부모·자식이 같은 쓰기를 수행.

### ASM-10 — identity와 권한 교집합

- 적용 조건: tool 호출·handoff·resume.
- 행동: original user·tenant·role을 보존하고, 현재 task scope·target ceiling·host·credential·승인 범위의 교집합만 허용한다.
- 검증: 각 경계의 effective scope 대조; AINV-009, AEVAL-010.
- 실패 시: 권한 확대·identity 불명확이면 실행 거부.
- 강제 계층: host 정책, IAM/ACL, 실행 broker.
- 근거: [I03], [C04], [M05], [O07]; 교집합 모델은 연구 제안.
- 예시: read-only 조사 agent가 write 권한 credential을 받아도 쓰기 불허.
- 반례: 다른 agent나 session ID를 거치며 사용자 scope를 넓힘.

### ASM-11 — exact approval과 단일 소비

- 적용 조건: 승인 필요한 부작용과 장기 pending 작업.
- 행동: 승인에 payload·대상·executor·tenant·정책·기한을 결박하고, 저장된 pending 요청을 원자적으로 한 번 소비한다.
- 검증: payload 변조·권한 없는 reviewer·replay 시험; AINV-010, AEVAL-011.
- 실패 시: 실행 중단, 정책에 따라 새 승인 또는 reconciliation.
- 강제 계층: 신뢰된 승인 저장소와 실행 broker.
- 근거: [I03], [O07], [D01].
- 예시: EVAL-15 수신자·제목·본문 변경 시 기존 승인으로 발송하지 않음.
- 반례: 승인 문자열이나 tool-name sticky 허용만으로 다른 payload 실행.

### ASM-12 — 모든 우회 실행 경로 목록화

- 적용 조건: Tool·MCP·shell·script·subagent 연결.
- 행동: 별칭·직접 호출·hosted 경로까지 inventory에 넣고 선택된 호출 경계만 연결한다. Skill allowed-tools를 권한 상한으로 보지 않는다.
- 검증: 경로별 Gate coverage와 거부 결과; AINV-008, AEVAL-012.
- 실패 시: 미통제 side-effect 경로를 비활성화하거나 담당 단계 재진입.
- 강제 계층: host/tool dispatch와 권한 검사.
- 근거: [I03], [C01], [O02], [O04], [M02].
- 예시: EVAL-18 기존 tool 이름 정리는 승인 identity를 보존하며 새 capability를 만들지 않음.
- 반례: Guardrail 밖 shell이나 중복 alias로 같은 작업 실행.

### ASM-13 — hard enforcement의 실제 가용성

- 적용 조건: Gate가 Permission·Sandbox·Hook 등 실제 차단을 요구.
- 행동: 요구된 host·설정·실행 계층의 적용을 확인하고 문장·fragment로 대체하지 않는다.
- 검증: 동일 entrypoint에서 금지 행동·통제 오류를 실제 차단하는지 확인; AINV-011, AEVAL-013.
- 실패 시: `HARD_ENFORCEMENT_UNAVAILABLE`; 위험 작업 실행 금지.
- 강제 계층: OS sandbox, IAM, host Gate.
- 근거: [I01], [I03], [C03], [C04], [C05].
- 예시: EVAL-20에 요구된 sandbox가 없으면 수정 실행 단계 진입 불가.
- 반례: SKILL.md에 금지 문장을 썼으므로 격리가 구현됐다고 주장.

### ASM-14 — Skill 로딩도 실행 경계

- 적용 조건: inline shell·preload·Skill hooks 사용.
- 행동: 로딩 전 실행 명령과 hook 수명·등록·host 버전을 조사한다. 새 이벤트 지원을 구버전에 가정하지 않는다.
- 검증: 버전·effective 설정·실제 로딩 경로 대조; AINV-011, AEVAL-014.
- 실패 시: 통제 불가능한 로딩 실행을 제거하거나 runtime 재진입.
- 강제 계층: host version gate와 Skill 실행 dispatcher.
- 근거: [C01], [C02], [C03], [C05], [C06].
- 예시: v2.1.332 전용 inline-shell 검사 이벤트의 지원·등록을 따로 확인.
- 반례: PreToolUse나 hook 설정 조각이 모든 Skill 로딩 명령을 막는다고 가정.

### ASM-15 — 검색 이전 권한과 지식 결박

- 적용 조건: Reference·RAG·live data 연결.
- 행동: source authority·snapshot·freshness·auth context를 보존하고 검색 전에 ACL을 적용한다. LLM에 security filter 변경 권한을 주지 않는다.
- 검증: 권한 없는 source가 retrieval·cache에서 제외되는지 확인; AINV-012, AEVAL-015.
- 실패 시: Knowledge 재진입 또는 권한/근거 부족 결과.
- 강제 계층: retrieval gateway, ACL, data store.
- 근거: [I01], [I03], [M03], [M05].
- 예시: EVAL-06 부서 범위 밖 문서가 생성 model에 전달되지 않음.
- 반례: 모두 검색한 뒤 답변 단계에서만 비밀을 숨김.

### ASM-16 — 의미 있는 비성공 상태 보존

- 적용 조건: no-evidence·conflict·실패·outcome-unknown 수신.
- 행동: 상태를 성공 값으로 변환하지 않는다. 근거 없음·충돌·실행 결과 불명을 서로 구분한다.
- 검증: 상태별 terminal/재시도/재진입 전이; AINV-013, AEVAL-016.
- 실패 시: 완료 중단, 근거 재조회·정책 결정·reconciliation 중 맞는 경로 선택.
- 강제 계층: typed ResultEnvelope와 상태 머신.
- 근거: [I03], [D01], [D02].
- 예시: 재고 API timeout을 재고 0으로 바꾸지 않음.
- 반례: 비어 있는 값·exit 0·자유문자 PASS를 업무 성공으로 취급.

### ASM-17 — context 축소와 근거 보존

- 적용 조건: progressive disclosure·요약·truncation·retrieved content.
- 행동: 필요한 span만 전달하되 source·권한·불확실성 참조를 보존한다. 외부 내용은 실행 권한이 없는 데이터로 취급한다.
- 검증: 압축 전후 필수 근거와 injection 경계 확인; AINV-014, AEVAL-017.
- 실패 시: 필요한 근거를 재조회하거나 결론을 보류.
- 강제 계층: context builder와 권한 분리된 tool gateway.
- 근거: [S01], [C02], [O03], [I03].
- 예시: EVAL-12 worker 요약은 인용 span과 미확인 항목을 함께 전달.
- 반례: source의 지시문을 새 permission으로 실행하거나 인용 없이 요약만 합침.

### ASM-18 — handoff는 재검사 경계

- 적용 조건: agent 간 제어·작업·근거 이전.
- 행동: identity·승인·evidence·남은 budget을 재검사한다. static handoff policy와 매번 달라지는 runtime record를 분리한다.
- 검증: history filter 뒤 필수 연결과 대상 권한 확인; AINV-009, AINV-014, AEVAL-018.
- 실패 시: 누락된 연결 복구 전 수신 agent 실행 차단.
- 강제 계층: handoff dispatcher와 승인 broker.
- 근거: [I03], [O03], [O07], [C02].
- 예시: 민감 history를 줄여도 필요한 승인 참조와 근거 ID는 유효하게 전달.
- 반례: history nesting을 자동 redaction 또는 승인 이전으로 간주.

### ASM-19 — tool call과 결과의 정확한 대응

- 적용 조건: tool·script·workflow 결과 수신.
- 행동: 존재하는 실행 identity와 결과를 결박한다. model-call ID는 실제 model 호출 때만 요구하며 transport·실행 ID와 혼동하지 않는다.
- 검증: orphan·중복·잘못된 executor·누락 결과 탐지; AINV-005, AINV-015, AEVAL-019.
- 실패 시: 성공 보고 중단 및 관찰 가능한 실행 상태 재조정.
- 강제 계층: dispatcher, result validator, trace collector.
- 근거: [I01], [O02], [O06], [M02].
- 예시: deterministic CSV script의 실제 execution ID로 결과 연결.
- 반례: 없는 model 호출 receipt를 만들거나 다른 호출의 성공 결과를 재사용.

### ASM-20 — checkpoint 재개와 부작용 분리

- 적용 조건: interrupt·resume·replay·상태 수정.
- 행동: 재개가 node 재실행을 포함할 수 있음을 반영하고 현재 계약·권한·승인을 다시 검사한다. 부작용은 replay-safe 경계로 분리한다.
- 검증: interruption 전후 재실행 횟수와 실제 효과 대조; AINV-016, AEVAL-020.
- 실패 시: 안전한 재개 불가면 중단·reconciliation·담당 재진입.
- 강제 계층: durable runtime와 상태 저장소.
- 근거: [L02], [L03], [O07], [I03].
- 예시: 승인 대기 뒤 재개해도 발송 효과는 중복되지 않게 소비 상태 확인.
- 반례: checkpoint가 있으므로 외부 쓰기도 자동 exactly-once라고 주장.

### ASM-21 — 불명 결과는 확인 후 재시도

- 적용 조건: side-effect timeout·일부 실패·재시도.
- 행동: 동일 의도와 idempotency key를 결박하고, 결과 불명은 먼저 reconciliation한다. retry 비활성도 결과 확인 의무를 없애지 않는다.
- 검증: 지연 응답·중복 요청·키와 payload 충돌; AINV-013, AINV-017, AEVAL-021.
- 실패 시: `OUTCOME_UNKNOWN` 유지, 승인된 보상 또는 운영 인수인계.
- 강제 계층: executor, idempotency 저장소, 상태 머신.
- 근거: [I03], [D01], [L05].
- 예시: EVAL-15 일부 수신자의 발송 여부를 조회한 후 미처리분만 판단.
- 반례: timeout을 실패 확정으로 간주해 3천 명 전체 재발송.

### ASM-22 — 병렬 입력 고정과 결정적 병합

- 적용 조건: fan-out/fan-in 또는 독립 worker.
- 행동: 공통 입력 root를 고정하고 worker별 최소 권한 projection을 전달한다. 병합 순서·충돌·부분 실패 정책을 명시한다.
- 검증: 결과 도착 순서를 바꿔도 같은 입력에서 같은 병합 판정; AINV-018, AEVAL-022.
- 실패 시: 충돌·누락을 숨기지 않고 부분 완료 또는 재진입.
- 강제 계층: orchestrator, artifact store, merge validator.
- 근거: [I03], [L04], [P01], [P02]; deterministic merge는 연구 제안.
- 예시: EVAL-12 독립 출처군 결과를 원문 대조 상태와 함께 합산.
- 반례: 공유 mutable history에서 최신 도착 답변으로 다른 결과 덮어쓰기.

### ASM-23 — budget·종료·취소의 관찰 가능성

- 적용 조건: agent loop·병렬 worker·외부 실행.
- 행동: 계약에 budget 단위·scope·종료 조건을 정하고 취소 요청과 실제 종료·효과를 구분한다. 보편 timeout 숫자를 발명하지 않는다.
- 검증: 한도 초과·지연 worker·취소 후 cleanup 상태; AINV-015, AINV-019, AEVAL-023.
- 실패 시: 새 작업 중단, 미종료·결과 불명 상태를 그대로 인계.
- 강제 계층: scheduler, executor, runtime policy.
- 근거: [I01], [I03], [L05].
- 예시: EVAL-11 남은 조사 budget 소진 시 근거와 미확인 가설로 종료.
- 반례: 취소 API 반환만으로 모든 tool이 멈췄다고 기록.

### ASM-24 — 동시 소유권이 필요할 때 fencing

- 적용 조건: 재할당·동시 worker가 같은 외부 상태를 쓸 위험.
- 행동: 필요 시 lease와 단조 fencing token을 사용하고, 실제 쓰기 수신자가 오래된 소유권을 거부하게 한다.
- 검증: lease 만료 뒤 되살아난 worker의 쓰기 거부; AINV-020, AEVAL-024.
- 실패 시: 수신자 통제 없으면 동시 쓰기를 허용하지 않음.
- 강제 계층: coordinator와 side-effect 수신자.
- 근거: [I01], [I03]; 구체 fencing 설계는 본 연구 제안.
- 예시: 동일 batch를 이어받은 새 worker 이후 옛 worker 결과를 거부.
- 반례: 읽기 전용 direct response에도 불필요한 lease artifact를 강제.

### ASM-25 — 사용자 파일을 보존하는 설치

- 적용 조건: package 설치·갱신·제거.
- 행동: generated/user-owned 경로를 구분하고 path 탈출·symlink·덮어쓰기를 거부한다. 검사한 객체와 적용 대상의 identity를 결박한다.
- 검증: 재설치·경로 교체·rollback 시 사용자 파일 보존; AINV-021, AEVAL-025.
- 실패 시: 적용 전 중단하거나 정확한 설치 record로 복구.
- 강제 계층: installer와 filesystem 통제.
- 근거: [I01], [I03], [D06]; check/apply 결박은 연구 제안.
- 예시: 이미 같은 digest로 설치된 생성 파일은 idempotent 처리.
- 반례: 최종 경로 검사 한 번으로 race가 사라졌다고 하거나 사용자 설정 덮어쓰기.

### ASM-26 — 호환성·마이그레이션·rollback 계약

- 적용 조건: component/schema/runtime 버전 갱신.
- 행동: 호환 범위·상태 변환·공존·복구 경로를 명시한다. artifact rollback과 이미 발생한 외부 효과의 보상을 분리한다.
- 검증: 지원/비지원 버전 조합과 upgrade/rollback 상태 대조; AINV-006, AINV-021, AEVAL-026.
- 실패 시: unsupported 상태로 유지하고 승인된 migration 재진입.
- 강제 계층: dependency resolver, migrator, installer.
- 근거: [I01], [O07], [D03], [D06].
- 예시: pending 승인에는 원 agent/SDK 버전과 호환 재개 경로 보존.
- 반례: 최신 패키지를 덮어쓰고 오래된 state도 당연히 재개된다고 가정.

### ASM-27 — 근거·trace·민감정보 통제

- 적용 조건: trace·evaluation·attestation 저장 및 전송.
- 행동: subject·입력·정책·checker·시간·scope를 결박하고 secret을 제외한다. 실패하는 redactor 뒤로 원문이 전송되지 않게 구성한다.
- 검증: subject 교체·전송 오류·정제 실패 시험; AINV-022, AEVAL-027.
- 실패 시: 해당 증거를 인정하지 않고 전송을 중단·미확인 기록.
- 강제 계층: evidence validator와 application-owned exporter.
- 근거: [I03], [O06], [D04], [D05].
- 예시: 보고서 digest를 manifest에 기록하고 runtime trace는 별도 실행 증거로 취급.
- 반례: trace 수집 또는 서명 존재만으로 내용의 정확성과 독립성을 주장.

### ASM-28 — 실제 entrypoint와 독립성 검증

- 적용 조건: 연구 제안을 구현 검증으로 전환.
- 행동: 사용자가 호출하는 실제 entrypoint를 clean context에서 검사하고 작성자/검토자의 실질적 독립성과 권한을 확인한다.
- 검증: 정상·경계·오류·악성 경로와 reviewer identity; AINV-023, AEVAL-028.
- 실패 시: 검증 범위를 좁혀 기록하고 독립/실행 PASS 주장 금지.
- 강제 계층: 평가 harness와 검토 운영.
- 근거: [I01], [I03], [S03], [P02].
- 예시: 실제 host 호출 결과와 계약 기대값을 별도 evaluator가 대조.
- 반례: 같은 identity가 이름만 바꿔 reviewer 역할을 맡고 독립 감사라고 기록.

### ASM-29 — mutation·ablation은 실행 증거로 판정

- 적용 조건: 통제 유효성과 최소 구성을 평가.
- 행동: 제거·변조한 통제의 실패를 실제 관찰하고, 더 단순한 기준선과 비교한다. 미실행 설계는 NOT_RUN으로 둔다.
- 검증: mutant ID·실행 로그·oracle·결과 연결; AINV-023, AEVAL-029.
- 실패 시: 검출되지 않은 결함 수정·재평가; 구성 변경은 Planner 재진입.
- 강제 계층: 독립 평가와 regression gate.
- 근거: [I01], [S03], [P02].
- 예시: Agent 제거 baseline의 충분성을 평가하되 승인 구성은 임의 변경하지 않음.
- 반례: mutation 목록 개수를 그대로 검출 성공 수로 보고.

### ASM-30 — local 결과와 production 승인 분리

- 적용 조건: 조립 완료·검토·release handoff.
- 행동: local package 적격성, 연구 검토, 실제 운영 승인을 별도 상태로 관리한다. release 승인 자료는 별도 handoff에 결박한다.
- 검증: 판정 scope와 필요한 외부 승인·운영 증거 대조; AINV-024, AEVAL-030.
- 실패 시: 해당 release를 차단하고 부족한 담당 단계로 재진입.
- 강제 계층: release gate와 운영 권한 경계.
- 근거: [I01], [I03], [D03], [D04], [D05].
- 예시: 연구 보고서 READY_FOR_REVIEW, runtime NOT_RUN, production 미승인.
- 반례: component PASS 합산으로 system·production PASS를 자동 생성.

## 14. ASSEMBLY_CONTRACT.yaml 제안

`0.3-proposal`은 **연구용 계약 구조 제안**이다. `null`은 미결박 값이며, 파싱 성공은 실행 적격성 증거가 아니다. §19에는 승인된 두 입력의 1:1 매핑이면 충분하다. 향후 실행·release에 필요한 full plan, capability/acceptance/Gate ID, permission, digest가 없으면 합성하지 않고 `PLANNER_REENTRY_REQUIRED` 등으로 반환한다. [I01], [I02], [I03]

정적 artifact와 실행 기록의 digest 관계는 **상위 artifact → 정적 정책 7개 → ASSEMBLY_CONTRACT → SYSTEM_MANIFEST → 실행·평가·설치 결과 → RELEASE_HANDOFF** 순서로 제한한다. 정적 정책 7개는 COMPONENT_BINDINGS, ENTRYPOINT_MANIFEST, CONTEXT_POLICY, HANDOFF_CONTRACT, STATE_MACHINE, RUNTIME_POLICY, INSTALL_MANIFEST다. 각 단계는 이미 확정된 앞 단계의 digest만 참조한다. 후행 산출물의 논리 이름은 선언할 수 있지만 미래의 결과 digest를 앞 단계에 되쓰지 않는다. manifest 자신의 digest는 외부 descriptor에 둔다. 이 비순환 참조 설계는 immutable subject와 provenance를 바탕으로 한 **본 조사의 설계 제안**이며, SLSA/in-toto가 이 Factory 스키마를 규정한다는 뜻은 아니다. Workflow의 조건부 실행 loop와 artifact hash 순환은 서로 다른 문제다. [D04], [D05], [D07]

같은 단계 정책 사이의 component·operation 참조는 **논리 ID**이며 peer 정책 문서의 digest를 포함하지 않는다. digest reference는 이미 확정된 상위 artifact만 허용하고 정적 정책들의 최종 digest는 후행 ASSEMBLY_CONTRACT가 수집한다. 아래 `execution_entrypoint_ref`, `target_component_ref` 등은 이 논리 참조 규칙을 따른다.

```yaml
schema_kind: ASSEMBLY_CONTRACT
schema_version: "0.3-proposal"
status: PROPOSED
usage: research_contract_template
binding_profile: research_mapping
upstream_refs:
  capability_plan: null
  gate_contract: null
  execution_contract: null
  knowledge_contract: null
source_policy:
  research_mapping: use_approved_scenario_sources_with_usage_limits
  runtime_binding: require_exact_current_approved_artifact_refs
  missing_full_plan_for_runtime: PLANNER_REENTRY_REQUIRED
selection:
  control_mode: null
  selected_components: null
  permitted_mode_values:
    - direct_response
    - deterministic_workflow
    - bounded_agent
    - multi_agent
  selection_rule: preserve_planner_mode_and_component_set
policy_refs:
  component_bindings: {artifact_kind: COMPONENT_BINDINGS, digest: null}
  entrypoints: {artifact_kind: ENTRYPOINT_MANIFEST, digest: null}
  context: {artifact_kind: CONTEXT_POLICY, digest: null}
  handoff: {artifact_kind: HANDOFF_CONTRACT, digest: null}
  state_machine: {artifact_kind: STATE_MACHINE, digest: null}
  runtime: {artifact_kind: RUNTIME_POLICY, digest: null}
  installation: {artifact_kind: INSTALL_MANIFEST, digest: null}
declared_outputs:
  - {artifact_kind: SYSTEM_MANIFEST, reference_type: logical_only}
  - {artifact_kind: ASSEMBLY_RESULT, reference_type: logical_only}
  - {artifact_kind: RELEASE_HANDOFF, reference_type: logical_only}
acceptance_policy:
  one_control_owner_per_operation: true
  new_component_without_planner_approval: forbidden
  missing_required_enforcement: HARD_ENFORCEMENT_UNAVAILABLE
  unsupported_execution_target: UNSUPPORTED_RUNTIME_PACK
  current_subject_and_policy_binding: required
  implementation_readiness_from_research_mapping: forbidden
production_authorization_granted_by_contract: false
```

검사: mode·source scope·선택 집합·정책 digest/eligibility·단일 제어권·실제 강제 계층을 확인한다. runtime에 필요한 `null`은 차단하지만, 연구 mapping에 요구하지 않는 full-plan 세부 필드를 §19 blocker로 만들지 않는다. [I01], [I02]

## 15. 보조 스키마

YAML은 예시이며 완성된 JSON Schema 구현이 아니다. `*_shape`·`*_fields`는 기록 구조 설명이다. 실제 시각·cursor·승인 응답·receipt는 정적 정책 밖에서 manifest digest에 결박한다. 비밀은 기록하지 않는다. 실제 runtime·설치·release는 **NOT_RUN**, production 승인은 **false**다.

### 15.1 SYSTEM_MANIFEST — 확정된 package inventory

계약·파일 digest를 고정하고 외부 dependency와 구분한다. 같은 경로·이름만으로 이전 검증을 재사용하지 않는다. provenance의 정책·builder 신뢰도 별도로 확인한다. [D04], [D05]

```yaml
schema_kind: SYSTEM_MANIFEST
schema_version: "0.3-proposal"
status: PROPOSED
assembly_contract_ref: {digest: null}
inventory: []
inventory_item_shape:
  relative_path: null
  artifact_kind: null
  digest: null
  component_ref: null
  ownership: null
external_dependency_refs: []
entrypoint_policy_ref: {digest: null}
settings_fragment_refs: []
identity_policy:
  serialization_profile: RFC8785_when_JSON_and_profile_is_approved
  file_digests: hash_exact_file_bytes
  manifest_digest_storage: external_descriptor
  manifest_contains_own_digest: false
  include_actual_runtime_or_install_receipts: false
  missing_or_unlisted_executable: block_runtime_binding
  changed_covered_artifact: STALE
verification_requirements:
  - compare_inventory_to_actual_package
  - verify_current_contract_and_policy_digests
  - reject_path_alias_or_duplicate_entry_ambiguity
  - validate_schema_version_compatibility
```

검사: inventory 중복·누락·경로 별칭·byte digest를 확인한다. manifest 밖의 descriptor와 후행 receipt가 manifest digest를 참조한다. RFC 8785와 raw byte hash의 적용 범위를 고정한다. [D05], [D07]

### 15.2 COMPONENT_BINDINGS — 승인된 component의 연결

승인 artifact를 참조하며 새 component·adapter 생성 권한을 주지 않는다. component 유형 집합과 instance 수는 별개이므로 worker 수·endpoint·operation은 승인 세부 계획에 결박한다. [I01], [I03]

```yaml
schema_kind: COMPONENT_BINDINGS
schema_version: "0.3-proposal"
status: PROPOSED
upstream_plan_ref: null
bindings: []
binding_shape:
  component_ref: null
  component_kind: null
  source_artifact_digest: null
  source_status_evidence_ref: null
  input_schema_ref: null
  output_schema_ref: null
  error_schema_ref: null
  capability_ids: null
  acceptance_ids: null
  gate_ids: null
  execution_entrypoint_ref: null
  tool_identity: null
  knowledge_snapshot_ref: null
  permission_policy_ref: null
  compatibility_constraint: null
validation_policy:
  add_unselected_component_or_adapter: PLANNER_REENTRY_REQUIRED
  incompatible_execution_interface: EXECUTION_REENTRY_REQUIRED
  missing_required_gate_binding: GATE_REENTRY_REQUIRED
  changed_knowledge_authority_acl_or_freshness: KNOWLEDGE_REENTRY_REQUIRED
  tool_name_alone_is_identity: false
  eligibility_from_label_without_bound_evidence: forbidden
  input_validation: before_dispatch
  output_validation: envelope_then_status_specific_schema
  preserve_outcomes: [success, failed, blocked, no_evidence, conflict, outcome_unknown]
```

검사: 선택된 구성에 필요한 필드만 요구한다. 성공·실패·차단·결과 미확정은 별도 schema로 검증한다. Tool identity·operation·version/schema 변경은 같은 이름이어도 재검증한다. [I03], [M05]

### 15.3 ENTRYPOINT_MANIFEST — 사용자 진입점과 제어권

mode와 component 유형은 별개다. deterministic mode가 workflow 파일을 필수화하지 않고, direct response에도 Skill/Reference가 있을 수 있다. 새 제어 component가 필요하면 Planner로 돌아간다. [I01], [I02], [I03]

```yaml
schema_kind: ENTRYPOINT_MANIFEST
schema_version: "0.3-proposal"
status: PROPOSED
entrypoints: []
entrypoint_shape:
  exposed_name: null
  kind: null
  target_component_ref: null
  operation_ref: null
  control_owner_ref: null
  invocation_policy_ref: null
  permission_policy_ref: null
  accepted_input_schema_ref: null
  terminal_output_schema_ref: null
mode_policy:
  direct_response: caller_owned_response_without_autonomous_loop
  deterministic_workflow: fixed_dispatcher_controls_edges_and_side_effects
  bounded_agent: one_approved_agent_controls_a_bounded_tool_loop
  multi_agent: one_approved_coordinator_controls_delegation_and_merge
generation_policy:
  create_skill: only_if_selected
  create_agent: only_if_selected
  create_workflow_artifact: only_if_selected
  duplicate_command_skill_agent_responsibility: reject
trace_field_conditions:
  model_call_id: only_if_a_model_call_actually_occurs
  transport_request_id: only_if_a_transport_request_actually_occurs
  skill_preload_receipt: only_if_selected_skill_is_preloaded_by_host
  execution_record: only_if_the_entrypoint_performs_recorded_execution
```

검사: 사용자 진입점부터 dispatch·Gate를 따라가고 우회 route를 확인한다. 실제 호출이 없는 Reference·직접 응답에 model/tool call ID를 만들지 않는다.

### 15.4 CONTEXT_POLICY — 필요한 문맥과 출처의 보존

권한 있는 최소 span·상태를 전달하고 rank와 authority를 구분한다. 요약에도 claim·source·span·snapshot 연결을 유지하며 retrieved data로 지시·권한을 만들지 않는다. [I03]

```yaml
schema_kind: CONTEXT_POLICY
schema_version: "0.3-proposal"
status: PROPOSED
disclosure:
  skill_metadata: discover_when_selected
  skill_body: load_when_invoked
  reference_spans: load_only_authorized_relevant_spans
  source_authority_and_retrieval_rank: separate
context_budget:
  policy_ref: null
  universal_numeric_default: null
  overflow_action: preserve_mandatory_bindings_then_retrieve_or_stop
data_rules:
  retrieved_content_authority: data_only
  secrets_in_prompt_state_summary_or_trace: forbidden
  raw_database_access_and_secret_values: forbidden
  bearer_credentials_or_authority_bearing_handles: forbidden
  non_secret_opaque_connection_refs: allowed_with_subject_and_scope_binding
  credential_reference_grants_authority_by_itself: false
  acl_check: before_retrieval_and_before_handoff_disclosure
summary_fields:
  - original_goal_ref
  - completed_and_unresolved_work
  - exact_source_span_refs
  - source_snapshot_refs
  - uncertainty_and_conflicts
  - pending_operation_refs
  - applicable_policy_refs
staleness:
  changed_source_acl_or_snapshot: revalidate_before_reuse
  mandatory_evidence_removed_by_truncation: block_completion
```

검사: 공개 범위·권한 철회·삭제의 cache 반영·truncation 후 근거 보존을 확인한다. secret은 문맥 밖에서 처리한다. opaque라는 이름만으로 안전하다고 보지 않으며, 그 자체로 권한을 행사하는 bearer handle은 전달하지 않는다. 비밀이 아닌 연결 식별자는 서버/호스트가 원 사용자·scope를 재검사하는 조건에서만 전달한다. [I03], [M06]

### 15.5 HANDOFF_CONTRACT — 정책과 전달 기록 schema

정적 계약에는 **실제 summary·승인·비용·pending 값을 저장하지 않는다.** 별도 `handoff_runtime_record`를 manifest에 결박한다. 대상의 넓은 권한을 원 사용자의 승인으로 승격하지 않는다. [I03], [M05]

```yaml
schema_kind: HANDOFF_CONTRACT
schema_version: "0.3-proposal"
status: PROPOSED
policy:
  authority_ceiling: intersection_of_original_user_current_task_source_target_and_host_policies
  target_selection: approved_role_and_component_refs_only
  transfer_secrets: forbidden
  transfer_permission_expansion: forbidden
  recheck_current_acl_and_revocation: required
  evidence_filter_drops_required_proof: reject_handoff
  delegation_cycle_budget_ref: null
runtime_record_fields:
  always_for_handoff:
    - manifest_digest
    - original_user_ref
    - tenant_ref
    - current_task_scope_ref
    - sender_ref
    - receiver_ref
    - requested_operation_ref
    - input_and_artifact_refs
    - summary_and_pending_work
    - evidence_and_uncertainty_refs
  when_approval_required:
    - approval_record_ref
    - exact_payload_digest
    - approver_and_policy_refs
    - expiry_and_replay_guard
  when_budgeted:
    - budget_policy_ref
    - consumed_and_remaining_budget
  when_independent_review_claimed:
    - creator_identity_ref
    - reviewer_identity_and_independence_evidence_ref
runtime_record_storage: separate_append_only_handoff_records
```

검사: subject·scope·operation·현재 권한과 exact approval/replay guard를 실제 강제 지점에서 확인한다. 다른 역할명은 독립 identity의 증거가 아니며 URL 수락도 외부 완료 증거가 아니다. [M05], [M06]

### 15.6 STATE_MACHINE — 허용 전이와 결과 미확정

아래 전이는 연구 제안이며 실제 cursor·attempt·pending call은 runtime record에 둔다. checkpoint는 외부 쓰기 원자성이 아니다. interrupt 재실행 구간을 검토한다. [L03], [L05]

```yaml
schema_kind: STATE_MACHINE
schema_version: "0.3-proposal"
status: PROPOSED
applies_when: entrypoint_has_execution_or_resumable_state
states:
  - READY
  - RUNNING
  - WAITING_APPROVAL
  - WAITING_INPUT
  - OUTCOME_UNKNOWN
  - RECONCILING
  - SUCCEEDED
  - FAILED
  - BLOCKED
  - CANCELLED
  - STALE
allowed_edges:
  READY: [RUNNING, BLOCKED, STALE]
  RUNNING: [WAITING_APPROVAL, WAITING_INPUT, OUTCOME_UNKNOWN, SUCCEEDED, FAILED, BLOCKED, CANCELLED]
  WAITING_APPROVAL: [RUNNING, BLOCKED, CANCELLED, STALE]
  WAITING_INPUT: [RUNNING, BLOCKED, CANCELLED, STALE]
  OUTCOME_UNKNOWN: [RECONCILING, BLOCKED]
  RECONCILING: [SUCCEEDED, FAILED, OUTCOME_UNKNOWN, BLOCKED]
  STALE: [READY, BLOCKED]
guards:
  entering_RUNNING: current_authority_binding_and_required_gate_checks
  entering_SUCCEEDED: bound_completion_evidence_and_no_unresolved_effects
  resuming_after_pause: revalidate_changed_inputs_identity_policy_and_approval
  leaving_STALE: complete_revalidation_of_affected_bindings
  unexpected_transition: block_and_record
effect_policy:
  lost_acknowledgement: OUTCOME_UNKNOWN
  unknown_means_no_effect: false
  cancellation_clears_pending_effects: false
  compensation: separately_authorized_and_recorded_operation
operation_effect_machine:
  separate_from_task_terminal_status: true
  applies_when: an_external_operation_was_submitted_or_may_have_been_submitted
  states: [PENDING, OUTCOME_UNKNOWN, RECONCILING, CONFIRMED_SUCCESS, CONFIRMED_FAILURE, PARTIAL]
  allowed_edges:
    PENDING: [OUTCOME_UNKNOWN, CONFIRMED_SUCCESS, CONFIRMED_FAILURE, PARTIAL]
    OUTCOME_UNKNOWN: [RECONCILING]
    RECONCILING: [CONFIRMED_SUCCESS, CONFIRMED_FAILURE, PARTIAL, OUTCOME_UNKNOWN]
    PARTIAL: [RECONCILING]
  late_result_after_cancel_block_or_failure: update_effect_record_without_reopening_task
  reconciliation_authority: recheck_current_authority_for_the_existing_operation
  missing_reconciliation_authority: retain_unresolved_effect_and_handoff_for_authorized_recovery
  reconciliation_after_task_terminal: permitted_for_observation_of_existing_effect_only
  new_or_compensating_effect: require_separately_authorized_operation
  confirmed_effect_changes_cancelled_task_to_success: false
  completion_or_release_with_unresolved_effect: forbidden
runtime_record_storage: separate_state_and_operation_events
```

검사: `OUTCOME_UNKNOWN`은 retry 금지 상태에서도 reconciliation이 필요하다. 제어 작업이 CANCELLED/BLOCKED/FAILED로 끝나도 별도의 operation effect record는 유지되어 늦은 결과를 추적한다. 확인 권한이 없으면 미해결 상태를 보존해 인계하며, 권한을 재확인한 뒤 기존 효과를 대조한다. 취소된 과업을 성공으로 바꾸거나 새 쓰기를 재개하는 경로로 사용하지 않는다. cancellation은 외부 취소 증거가 아니며 미수신 result·부분 완료·budget 소진을 성공으로 합치지 않는다. [I03], [L05]

### 15.7 RUNTIME_POLICY — 실제 강제·재시도·병렬 경계

실제 host 지원과 정책 파일을 구분한다. timeout·retry·budget은 승인 계약에서 받는다. fencing은 모든 read-only 병렬 조회가 아니라 동시·재진입 writer의 mutable 효과에 조건부로 요구하는 연구 설계다. [I03], [L05]

```yaml
schema_kind: RUNTIME_POLICY
schema_version: "0.3-proposal"
status: PROPOSED
runtime_target_ref: null
enforcement:
  permission_policy_ref: null
  sandbox_policy_ref: null
  hook_policy_ref: null
  activation_receipt_required: when_selected_gate_requires_host_enforcement
  prompt_as_hard_enforcement: forbidden
  missing_required_runtime: HARD_ENFORCEMENT_UNAVAILABLE
limits:
  timeout_policy_ref: null
  retry_policy_ref: null
  budget_policy_ref: null
retry:
  side_effect_key: stable_across_retry_and_resume
  external_provider_deduplication: verify_before_relying_on_it
  reused_key_with_different_payload: reject
  unknown_outcome: reconcile_before_retry_or_compensation
parallel:
  enabled: only_if_approved_architecture_requires_it
  branch_inputs: immutable_authorized_projections_of_frozen_snapshot
  branch_outputs: separate_namespaces
  merge: declared_deterministic_reducer_with_conflict_policy
  partial_completion: explicit_incomplete_result
  mutable_write_contention: require_receiver_enforced_fencing_or_serialization
resume:
  checkpoint_scope: local_graph_state_not_external_atomic_commit
  changed_dependency_or_policy: revalidate_before_dispatch
  repeatable_pre_interrupt_code: required
  orphan_tool_result: reconcile_operation_identity_before_consumption
```

검사: 로컬 timeout과 외부 취소를 구분한다. 고정 snapshot을 worker 권한으로 투영하고 완료 순서와 무관한 reducer·충돌 처리를 적용한다. 누락·상충 근거를 숨기지 않는다.

### 15.8 INSTALL_MANIFEST — 설치 대상과 사용자 소유 파일 보호

무결성 검증·설치·host 활성화·production release는 별개다. TUF는 사용자 파일 보존까지 보장하지 않는다. settings fragment만으로 host 강제를 주장하지 않는다. [I01], [D06]

```yaml
schema_kind: INSTALL_MANIFEST
schema_version: "0.3-proposal"
status: PROPOSED
applies_when: selected_artifacts_require_installation
target_platform_ref: null
managed_paths: []
protected_user_paths: []
install_policy:
  unknown_path_ownership: block
  overwrite_user_owned_content: forbidden
  path_traversal_or_symlink_escape: reject
  duplicate_or_case_alias_destination: reject
  check_apply_identity: validated_target_handle_or_atomic_transaction
  content_changed_after_precheck: abort_and_revalidate
  file_integrity: verify_before_apply
  staging_and_extraction_limits: required_when_archive_is_used
  rerun_with_same_inputs: preserve_same_managed_result
backup_and_rollback:
  backup_before_managed_replacement: required
  restore_only_recorded_managed_targets: true
  current_content_matches_our_installed_digest: required_before_restore_or_remove
  unexpected_user_change: stop_without_overwrite
  external_side_effect_rollback: not_implied_by_file_restore
settings:
  fragment_refs: []
  activation_approval:
    required_when: owner_activation_is_needed_for_the_selected_host_configuration
    upstream_policy_ref: null
  actual_activation_record_fields:
    - subject_manifest_digest
    - owner_approval_record_ref
    - effective_host_policy_ref
    - actual_activation_receipt_ref
  actual_activation_record_storage: separate_install_or_host_record
  fragment_presence_proves_enforcement: false
schema_migration:
  compatibility_policy_ref: null
  migration_plan_ref: null
  unsupported_version: block_installation
```

검사: 정적 activation 승인 정책은 이미 확정된 상위 정책만 참조한다. 최종 manifest에 대한 실제 승인·활성 receipt는 별도 실행 기록에 저장해 digest 순환을 피한다. 최종 경로 재확인만으로 check/apply 원자성을 주장하지 않는다. rollback/uninstall은 관리 대상·현재 digest가 확인되는 범위만 다루며 외부 쓰기는 file restore로 복구되지 않는다. [D06]

### 15.9 ASSEMBLY_RESULT — 정적 검사와 실행 결과의 분리

결과는 확정 manifest를 참조한다. 문서·§19 source correspondence·runtime·E2E 판정을 분리하고 기대값 PASS를 실행 증거로 받지 않는다. [I02], [I03]

```yaml
schema_kind: ASSEMBLY_RESULT
schema_version: "0.3-proposal"
status: PROPOSED
record_template:
  manifest_ref: {digest: null}
  input_binding_refs: []
  checker_identity_ref: null
  policy_ref: null
  observed_at: null
  scope: null
  static_document_checks: UNVERIFIED
  research_mapping_checks: UNVERIFIED
  runtime_execution: NOT_RUN
  end_to_end_execution: NOT_RUN
  mutation_execution: NOT_RUN
  runtime_receipt_refs: []
  install_receipt_refs: []
  evidence_refs: []
  unresolved_effect_refs: []
  blockers: []
  limitations: []
  local_candidate_verdict: UNVERIFIED
  production_authorized: false
validation_policy:
  verdict_without_subject_policy_checker_evidence_binding: reject
  source_expectation_PASS_as_execution: reject
  component_PASS_sum_as_system_PASS: reject
  changed_manifest_dependency_or_policy: mark_affected_verdict_STALE
  independent_verification: require_actual_identity_and_procedure_evidence
  empty_required_receipts: never_imply_success
```

검사: 정적 mapping 성공과 runtime `NOT_RUN`은 양립한다. 연구 검토·미래 package 실행 적격성·production 승인은 각각 판단한다.

### 15.10 RELEASE_HANDOFF — 검토 결과와 승인 경계

계약·manifest·실제 결과를 읽는 마지막 문서이며 앞 단계에 결과 digest를 되쓰지 않는다. local candidate와 production 권한을 분리한다. [I01], [I03], [D04], [D05]

```yaml
schema_kind: RELEASE_HANDOFF
schema_version: "0.3-proposal"
status: PROPOSED
subject_manifest_ref: {digest: null}
assembly_contract_ref: {digest: null}
assembly_result_refs: []
evaluation_result_refs: []
install_and_host_receipt_refs: []
review:
  decision: NOT_REVIEWED
  reviewer_identity_ref: null
  independence_evidence_ref: null
  reviewed_scope: null
  unresolved_limitations: []
authorization:
  local_package_authorization_ref: null
  production_authorization_ref: null
  production_authorized: false
  automatic_promotion_from_research_or_local_candidate: forbidden
validation_policy:
  current_digest_and_policy_binding: required
  missing_required_evidence: block_claimed_release_scope
  unsupported_required_runtime: block_claimed_release_scope
  unresolved_external_effect: block_completion_claim
  new_capability_or_permission_need: return_to_responsible_upstream_stage
  production_action_by_research_session: forbidden
```

검사: 인수자가 동일 subject와 미검증 범위를 확인해야 한다. 승인 ref를 임의 생성하지 않는다. runtime·host 활성화·설치/rollback·외부 쓰기·독립 attestation은 **NOT_RUN 또는 UNVERIFIED**다.

## 16. 기계 불변식: AINV-001 ~ AINV-024

아래는 구현할 **predicate 제안**이다. 문서 내용의 정적 검사와 실제 runtime predicate 평가는 구분한다. nullable·조건부 필드는 해당 실행이 없는 경우 가짜 receipt로 채우지 않는다.

| ID | 검사할 불변식 | 연결 규칙 | 위반 처리 |
|---|---|---|---|
| AINV-001 | 소비 입력의 경로·실제 digest·승인 scope가 현재 manifest와 일치한다. | ASM-01 | source 차단 |
| AINV-002 | 조립 mode와 component set은 승인 기대값과 같다. mode 이름으로 artifact를 추가하지 않는다. | ASM-02, ASM-03 | Planner 재진입 |
| AINV-003 | §19는 EVAL-01~22 각각 1행, 9개 필드와 원문·정규 기대값을 보존하며 연구 결정을 구분한다. | ASM-04, ASM-05 | 매핑 수정 |
| AINV-004 | 없는 capability·Gate·permission·digest를 사실로 합성하지 않는다. §19 full-plan 부재와 향후 실행 부재를 구분한다. | ASM-04, ASM-06 | 해당 단계 재진입 |
| AINV-005 | 연결 edge는 schema·오류 의미·producer/consumer identity가 호환되고 결과가 실제 실행에 대응한다. | ASM-06, ASM-19 | 연결 차단 |
| AINV-006 | dependency version/digest/status 변경이 영향받는 판정을 STALE로 만든다. | ASM-07, ASM-26 | 재검증 |
| AINV-007 | hash 참조 그래프는 비순환이며 불변 문서에 후속 결과를 되쓰지 않는다. workflow 순환과 구분한다. | ASM-08 | 구조 수정 |
| AINV-008 | 단계별 control owner가 명확하며 모든 실제 호출·우회 경로가 inventory와 통제에 연결된다. | ASM-09, ASM-12 | 경로 차단 |
| AINV-009 | effective 권한은 원 사용자·tenant·현재 task·수신자·host·credential·승인 scope의 교집합을 넘지 않는다. | ASM-10, ASM-18 | 실행 거부 |
| AINV-010 | 승인된 payload·대상·executor·정책과 실행이 일치하며 pending 요청은 원자적으로 한 번 소비된다. | ASM-11 | 재승인/차단 |
| AINV-011 | 요구된 hard 통제의 host 지원·등록·적용이 관찰된다. prompt나 fragment는 활성 증거가 아니다. | ASM-13, ASM-14 | runtime unavailable |
| AINV-012 | Knowledge scope·authority·freshness·auth binding을 유지하며 ACL이 retrieval 전에 적용된다. | ASM-15 | Knowledge 재진입 |
| AINV-013 | no-evidence·conflict·outcome-unknown은 서로 구분되고 성공으로 축약되지 않는다. | ASM-16, ASM-21 | 완료 중단 |
| AINV-014 | context/handoff 축소 뒤에도 필수 근거·권한·불확실성을 추적하며 외부 내용은 권한이 아니다. | ASM-17, ASM-18 | 재조회/차단 |
| AINV-015 | 결과는 해당 실행과 terminal 상태에 결박된다. 취소 요청은 종료 증거가 아니며 없는 ID를 요구하지 않는다. | ASM-19, ASM-23 | 상태 조정 |
| AINV-016 | resume은 현재 계약·권한을 확인하며 node 재실행이 외부 효과 중복으로 이어지지 않는다. | ASM-20 | 재개 차단 |
| AINV-017 | 동일 의도 재시도는 idempotency 계약을 따르고 불명 효과는 재실행 전에 확인된다. | ASM-21 | reconciliation |
| AINV-018 | 병렬 입력 root가 고정되고 projection 권한·merge 순서·충돌·부분 실패 정책이 명시된다. | ASM-22 | 부분/충돌 판정 |
| AINV-019 | 적용 가능한 budget은 단위·scope·소진/취소 전이를 가지며 미종료 작업을 숨기지 않는다. | ASM-23 | 안전 종료/인계 |
| AINV-020 | 중복 소유 쓰기 위험이 있으면 수신자의 fencing/version check 또는 동등한 배타적 직렬화로 stale 쓰기를 방지한다. | ASM-24 | 동시 쓰기 차단 |
| AINV-021 | 설치·migration·rollback은 승인 경로만 변경하며 사용자 파일과 검사/적용 identity를 보존한다. | ASM-25, ASM-26 | 적용 중단/복구 |
| AINV-022 | 근거는 정확한 subject·정책·scope와 결박되고 민감정보 정제 실패 시 외부 전송되지 않는다. | ASM-27 | 근거 무효/전송 차단 |
| AINV-023 | 독립성·runtime·mutation 판정은 실제 실행과 신뢰된 identity에 근거하며 설계 수량으로 대체되지 않는다. | ASM-28, ASM-29 | NOT_RUN/미확인 |
| AINV-024 | 연구·local·production 상태는 분리되며 component 성공이나 의도된 시나리오 차단을 잘못 승격·전파하지 않는다. | ASM-05, ASM-30 | 해당 scope 차단 |

## 17. 평가 세트: AEVAL-001 ~ AEVAL-030

**모두 설계이며 `NOT_RUN`이다.** 아래는 정적·통합·runtime 평가 설계 30개이며 기대 결과는 oracle 제안이지 관찰 결과가 아니다. §19 문서 대조 검사를 별도로 실행해도 이 평가 세트 전체가 실행된 것으로 세지 않는다. 실제 실행에서는 대상 digest·host/version·입력·oracle·observed result·검증 주체를 기록한다.

| ID | 입력/경계 및 실행 방법 제안 | 기대 관찰 | 연결 | 상태 |
|---|---|---|---|---|
| AEVAL-001 | 승인 입력 1개 digest를 바꾸고 같은 resume entrypoint 호출. | 변조 입력을 소비하지 않고 source 차단. | ASM-01; AINV-001 | NOT_RUN |
| AEVAL-002 | deterministic mode, script·validator만 선택된 fixture 조립. | workflow·agent·skill artifact 추가 없음. | ASM-02; AINV-002 | NOT_RUN |
| AEVAL-003 | Skill 없는 direct/tool-only 계획을 generator dispatch에 입력. | Skill Author 미호출, 선택된 책임만 배치. | ASM-03; AINV-002 | NOT_RUN |
| AEVAL-004 | 승인 22개를 결합하되 full plan 파일은 제공하지 않음. | 연구 매핑은 가능; 원문/ID/9필드 보존, 실행 승인 주장은 없음. | ASM-04; AINV-003, AINV-004 | NOT_RUN |
| AEVAL-005 | EVAL-22의 정책 없는 구매 요청과 정적 PASS 입력. | 읽기 전용 계획 후 구매 차단; 연구 세션의 source blocker로 오판하지 않음. | ASM-05; AINV-003, AINV-024 | NOT_RUN |
| AEVAL-006 | producer와 consumer에 비호환 I/O schema 제공. | 조용한 adapter 생성 없이 지정 단계 재진입. | ASM-06; AINV-004, AINV-005 | NOT_RUN |
| AEVAL-007 | 통과했던 component digest만 갱신하고 system 결과 재조회. | 영향받는 결과 STALE, 옛 근거로 실행 불가. | ASM-07; AINV-006 | NOT_RUN |
| AEVAL-008 | contract↔manifest hash 순환과 후속 receipt 되쓰기 시도. | 순환·불변 위반 거부; workflow loop와 혼동 없음. | ASM-08; AINV-007 | NOT_RUN |
| AEVAL-009 | workflow와 nested agent가 같은 단계의 제어권을 동시에 선언. | 모호한 소유권 연결 거부, 하나의 경로를 명확히 요구. | ASM-09; AINV-008 | NOT_RUN |
| AEVAL-010 | read-only task를 더 넓은 도구/credential을 가진 agent로 handoff. | 현재 task·원 사용자 범위 유지, 확대 호출 거부. | ASM-10; AINV-009 | NOT_RUN |
| AEVAL-011 | 승인 뒤 수신자/payload 변경 및 동일 pending 요청 동시 소비. | 변경 실행 거부; 승인된 요청도 한 번만 소비. | ASM-11; AINV-010 | NOT_RUN |
| AEVAL-012 | guarded tool의 직접 shell·별칭·hosted 우회 경로로 동일 행동 시도. | 요구 통제가 모든 실제 경로에 적용되거나 경로 비활성화. | ASM-12; AINV-008 | NOT_RUN |
| AEVAL-013 | 필수 sandbox/host Gate를 제거하고 실제 사용자 entrypoint 호출. | 위험 작업 전 `HARD_ENFORCEMENT_UNAVAILABLE`. | ASM-13; AINV-011 | NOT_RUN |
| AEVAL-014 | Skill inline shell을 지원/미지원 host 및 hook 등록 실패 조건에서 호출. | 버전·경로별 실제 적용 차이를 탐지하고 fragment-only 성공 주장 없음. | ASM-14; AINV-011 | NOT_RUN |
| AEVAL-015 | ACL 밖 문서·철회 권한·stale cache를 포함한 retrieval 요청. | 권한 없는 source가 model context 전 단계에서 제외됨. | ASM-15; AINV-012 | NOT_RUN |
| AEVAL-016 | no-evidence, conflict, outcome-unknown 세 결과를 같은 consumer에 주입. | 각각 다른 의미·전이 보존; 성공 값으로 coercion 없음. | ASM-16; AINV-013 | NOT_RUN |
| AEVAL-017 | 긴 근거와 지시형 외부 문서를 함께 넣고 context를 축소. | 필수 span/불확실성 보존, 외부 지시로 권한 확대 없음. | ASM-17; AINV-014 | NOT_RUN |
| AEVAL-018 | handoff filter가 승인·근거 참조를 제거하거나 수신자 scope를 변경. | 실행 전 재검사에서 누락 탐지, 재조회/재진입. | ASM-18; AINV-009, AINV-014 | NOT_RUN |
| AEVAL-019 | orphan 결과·중복 결과·다른 executor 결과와 정상 deterministic 결과 비교. | 잘못된 대응 거부; 정상 script에 가짜 model-call ID 요구 없음. | ASM-19; AINV-005, AINV-015 | NOT_RUN |
| AEVAL-020 | side-effect 주변에서 interrupt 후 node 재실행·resume. | 재개 재검증 수행, 이미 발생한 효과 중복 방지. | ASM-20; AINV-016 | NOT_RUN |
| AEVAL-021 | 쓰기는 성공했으나 응답을 유실시킨 뒤 retry 요청. | outcome-unknown에서 확인 후 판단; 맹목적 중복 효과 없음. | ASM-21; AINV-013, AINV-017 | NOT_RUN |
| AEVAL-022 | 고정 입력의 worker 도착 순서를 변경하고 충돌·누락 branch 포함. | 순서와 무관한 병합 판정; 충돌·부분 완료를 명시. | ASM-22; AINV-018 | NOT_RUN |
| AEVAL-023 | fixture별 budget 소진 및 취소 후 지연 tool completion 발생. | 새 작업 중단, 실제 종료/효과까지 추적; 숫자는 fixture 조건으로만 사용. | ASM-23; AINV-015, AINV-019 | NOT_RUN |
| AEVAL-024 | lease 재할당 후 옛 worker가 늦게 쓰기 제출. | 수신자가 stale token을 거부; 읽기-only 사례에는 fencing을 강제하지 않음. | ASM-24; AINV-020 | NOT_RUN |
| AEVAL-025 | 재설치·사용자 파일 충돌·경로 탈출·검사 후 path 교체 시도. | 승인 파일만 변경; 검사/적용 identity 유지 또는 안전 중단. | ASM-25; AINV-021 | NOT_RUN |
| AEVAL-026 | 호환/비호환 schema의 upgrade 후 pending state 재개·rollback. | 지원 경로만 허용, 사용자 파일 보존, 외부 효과와 artifact 복구 구분. | ASM-26; AINV-006, AINV-021 | NOT_RUN |
| AEVAL-027 | evidence subject를 교체하고 trace redactor가 예외를 던지게 함. | 잘못된 근거 거부, 원문 외부 전송 없음. | ASM-27; AINV-022 | NOT_RUN |
| AEVAL-028 | 작성자와 같은 identity를 reviewer 이름으로 지정하고 실제 entrypoint 평가. | 독립성 미확인 표시; 실행 관찰과 역할 이름을 혼동하지 않음. | ASM-28; AINV-023 | NOT_RUN |
| AEVAL-029 | 통제 제거 mutant와 더 단순한 baseline을 clean context에서 각각 실행. | 관찰 결과로 검출·효용 판정; 미실행 항목은 성공 수에 제외. | ASM-29; AINV-023 | NOT_RUN |
| AEVAL-030 | 연구/정적 package 성공만으로 production 전이를 요청. | 별도 운영 증거·승인 없으면 release 거부; local 결과는 scope 유지. | ASM-30; AINV-024 | NOT_RUN |

## 18. Mutation 세트: AMUT-001 ~ AMUT-024

**아래 24개는 설계이며 모두 `NOT_RUN`; 실행·검출 수는 0이다.** 각각 통제 하나를 제거·변조한 뒤 연결 평가에서 위반을 잡는지 관찰한다. 원 구현이 없으면 mutant도 실제 생성·실행됐다고 기록하지 않는다. 실패 oracle의 적절성 역시 독립 검토 대상이다.

| ID | 변조 제안 | 반드시 탐지할 결과 | 연결 불변식 / 평가 | 상태 |
|---|---|---|---|---|
| AMUT-001 | manifest digest 비교 생략. | 바뀐 입력을 READY로 소비하는 결함. | AINV-001 / AEVAL-001 | NOT_RUN |
| AMUT-002 | mode 이름으로 workflow·agent 자동 추가. | 승인 component set 확대. | AINV-002 / AEVAL-002, AEVAL-003 | NOT_RUN |
| AMUT-003 | §19 ID 중복·누락 또는 요청 원문 교체. | 정확한 22개 1:1 대응 실패. | AINV-003 / AEVAL-004 | NOT_RUN |
| AMUT-004 | 없는 full-plan Gate/permission ID를 합성. | 연구 기대값을 실제 실행 계약으로 오승격. | AINV-004 / AEVAL-004, AEVAL-006 | NOT_RUN |
| AMUT-005 | 비호환 edge schema 검사를 제거. | 잘못된 구조를 consumer에 전달. | AINV-005 / AEVAL-006 | NOT_RUN |
| AMUT-006 | dependency 변경 후 옛 verdict 재사용. | stale 근거로 현재 artifact 승인. | AINV-006 / AEVAL-007 | NOT_RUN |
| AMUT-007 | manifest에 자기 hash나 후속 receipt 되쓰기 추가. | 순환·불변성 위반. | AINV-007 / AEVAL-008 | NOT_RUN |
| AMUT-008 | alias/직접 실행 경로를 inventory에서 누락. | 실제 우회 호출의 Gate 부재. | AINV-008 / AEVAL-009, AEVAL-012 | NOT_RUN |
| AMUT-009 | handoff 시 현재 task scope를 target 권한으로 대체. | 원 사용자 범위보다 넓은 호출. | AINV-009 / AEVAL-010 | NOT_RUN |
| AMUT-010 | exact payload 또는 atomic consume 비교 제거. | 변경 payload·중복 resume 실행. | AINV-010 / AEVAL-011 | NOT_RUN |
| AMUT-011 | host 통제를 비활성화하고 fragment만 활성 증거로 사용. | 실제 차단 없는 성공 판정. | AINV-011 / AEVAL-013, AEVAL-014 | NOT_RUN |
| AMUT-012 | ACL 검사를 retrieval 뒤로 이동. | 비인가 source가 context/cache에 노출. | AINV-012 / AEVAL-015 | NOT_RUN |
| AMUT-013 | no-evidence·conflict·unknown을 success로 치환. | 상태 의미 소실과 잘못된 완료. | AINV-013 / AEVAL-016 | NOT_RUN |
| AMUT-014 | 요약 시 source span·승인 참조 삭제. | 근거·권한을 재구성할 수 없는 handoff. | AINV-014 / AEVAL-017, AEVAL-018 | NOT_RUN |
| AMUT-015 | call/result identity 비교 제거. | orphan·중복·다른 실행 결과 수용. | AINV-015 / AEVAL-019 | NOT_RUN |
| AMUT-016 | resume 경로의 현재 계약·효과 확인 제거. | node 재실행에 따른 부작용 중복. | AINV-016 / AEVAL-020 | NOT_RUN |
| AMUT-017 | write timeout 후 reconciliation 없이 retry. | 중복 효과 또는 불명 결과의 실패 확정. | AINV-017 / AEVAL-021 | NOT_RUN |
| AMUT-018 | frozen input 대신 live state와 도착순 merge 사용. | 비결정적 합산·숨은 부분 실패. | AINV-018 / AEVAL-022 | NOT_RUN |
| AMUT-019 | 취소 요청을 terminal completion으로 기록. | 살아 있는 tool과 미확정 효과 누락. | AINV-019 / AEVAL-023 | NOT_RUN |
| AMUT-020 | fencing을 선택한 실행 경로에서 수신자의 token 검사 제거. | 재할당 뒤 stale worker 쓰기 수용. | AINV-020 / AEVAL-024 | NOT_RUN |
| AMUT-021 | user-owned 보호 또는 check/apply identity 결박 제거. | 사용자 파일 덮어쓰기·경로 교체. | AINV-021 / AEVAL-025, AEVAL-026 | NOT_RUN |
| AMUT-022 | evidence subject 비교 또는 export 정제 실패 차단 제거. | 타 artifact 근거 재사용·원문 누출. | AINV-022 / AEVAL-027 | NOT_RUN |
| AMUT-023 | 계획된 eval·mutation 항목을 실행 성공으로 집계. | 실제 run·independent identity 없는 PASS. | AINV-023 / AEVAL-028, AEVAL-029 | NOT_RUN |
| AMUT-024 | local 완료를 production 승인으로 자동 전환. | 별도 release 증거·권한 없는 승격. | AINV-024 / AEVAL-005, AEVAL-030 | NOT_RUN |

### Ablation 설계와 집계 경계

Skill·Agent·RAG·병렬화가 없는 기준선 및 이전 버전을 동일 요청·권한·근거 조건에서 비교한다. 더 단순한 기준선이 충분하다는 관찰은 Planner 재진입 자료이며, Assembler가 승인 구성 자체를 변경할 허가는 아니다. 비교에 사용한 token·시간·오류·인용·권한 지표의 정의와 실행 횟수를 기록하고 보편 예산 수치를 만들지 않는다. 이 보고서의 ablation 제안 역시 `NOT_RUN`이다.

## 19. Planner 22개 시나리오 Assembly golden mapping

### 19.1 승인 범위와 결과의 의미

2026-11-25 재봉인된 입력 manifest [I02]에 따라 EVAL-01~EVAL-22의 요청·기대 아키텍처는 [I04], 정규화된 제어 모드·구성요소는 [I05]의 `base`에서 가져왔다. 기준 input head는 `e2e1628b7070e314f59f49cb03f435d47dd29abb`다. 두 파일을 ID로 정확히 1:1 결합하며 요청·아키텍처 문자열(원문의 backtick 포함)과 구성요소 배열을 변경하지 않았다. 원문에 여러 아키텍처 대안이 있어도 이 매핑에서 조립할 구성은 승인된 정규화 기대값을 보존한다.

아래 JSON의 `mappings` 22개 레코드가 이 절의 권위 있는 매핑이다. 앞의 표는 가독성을 위한 요약이다. 각 행은 필수 9개 필드를 가지며, 4개 정본 필드와 5개 Assembler 연구제안 필드를 명시적으로 구분한다. 모든 연구제안은 설계상 필요한 연결과 차단 조건을 설명할 뿐 승인된 개별 계획 필드, 실제 runtime 존재 또는 구현 적격성의 증거가 아니다.

`research_status: MAPPED`는 승인된 기대값에 대응하는 연구 매핑을 작성했다는 뜻이다. 모든 행의 `runtime_execution: NOT_RUN`은 Planner·Assembler·외부 업무를 실행하지 않았다는 뜻이다. [I05]의 원본 `status`와 `paraphrases` 값은 입력 증거나 실행·독립 검증·개별 계획 승인 판단에 사용하지 않았다. 현재 수행 가능한 검사는 문서의 exact ID join, 원문 보존, 필수 필드 및 정적 의미 대조이다.

완성된 개별 CAPABILITY_PLAN, 22회 실행 trace, 개별 승인 attestation은 [I02]가 §19 연구 매핑의 선행 요건에서 제외한다. 향후 실제 조립·구현·release가 capability/acceptance/Gate ID, exact permission, digest 등 구체 binding을 요구하면 합성하지 않고 `PLANNER_REENTRY_REQUIRED`로 반환한다. 아래의 binding 요구는 새 component를 자동 추가한다는 뜻이 아니다.

`deterministic_workflow`는 제어 모드이며 `workflow`라는 component와 동일하지 않다. EVAL-04/05/06/08/15/16/19에는 workflow component가 없으므로 호스트의 고정 제어 경로를 연구제안으로 설명하되 새 Workflow artifact나 실제 하네스 구현을 주장하지 않는다. 같은 원칙을 Tool·Permission·State·Tracing 등 모든 미선택 component에 적용한다.

EVAL-22의 `scenario_action_status: BLOCKED_FOR_DECISION`은 구매 행동을 차단하는 해당 시나리오의 정답이다. 이 행의 연구 매핑은 완료 가능하며, 이 값을 조사 세션의 blocker로 올리지 않는다.

### 19.2 가독성용 22개 매핑 요약

| ID / 제목 | 승인 mode | 승인 components | 핵심 조립 결정 — 연구제안 |
|---|---|---|---|
| EVAL-01 · 일회성 문장 다듬기 | `direct_response` | `[]` | 현재 문맥의 문장 변환만 수행 |
| EVAL-02 · 반복 ADR 작성 규칙 | `direct_response` | `skill` | 선택된 ADR Skill만 연결 |
| EVAL-03 · 작은 안정 운영 가이드 | `direct_response` | `skill, reference` | Skill과 고정 Reference inventory 연결 |
| EVAL-04 · CSV 정규화 | `deterministic_workflow` | `script, validator` | Script→Validator 고정 경로; Skill 추가 없음 |
| EVAL-05 · 정적 DB 스키마 기반 SQL 초안 | `deterministic_workflow` | `skill, reference, validator` | SELECT 초안→SQL Validator; 실행 경로 없음 |
| EVAL-06 · 대규모 권한별 사내 규정 검색 | `deterministic_workflow` | `skill, rag, permission, eval` | ACL 선검사→RAG→근거 답변→citation eval |
| EVAL-07 · RAG near-miss | `direct_response` | `reference` | 고정 PDF·FAQ Reference만 직접 연결 |
| EVAL-08 · 현재 재고 조회 | `deterministic_workflow` | `tool` | 기존 ERP read-only Tool만 재사용 |
| EVAL-09 · 고정 야간 ETL | `deterministic_workflow` | `workflow, script, validator` | 고정 ETL Workflow와 대조·복구 연결 |
| EVAL-10 · 고정 고객 문의 라우팅 | `deterministic_workflow` | `workflow, validator` | LLM은 구조화 분류; Workflow가 고정 큐 선택 |
| EVAL-11 · 개방형 장애 조사 | `bounded_agent` | `agent, tool, tracing` | 단일 bounded Agent와 read-only Tools |
| EVAL-12 · 병렬 독립 심층조사 | `multi_agent` | `agent, tracing, eval` | 격리된 worker·verifier와 결정적 취합 |
| EVAL-13 · Multi-agent 과잉 설계 near-miss | `direct_response` | `[]` | 빈 구성의 직접 응답; 다중 Agent 없음 |
| EVAL-14 · 운영 DB 삭제 | `deterministic_workflow` | `workflow, script, validator, approval, permission, tracing` | 삭제 미리보기→exact 승인→제한 실행 |
| EVAL-15 · 메일 초안과 발송 | `deterministic_workflow` | `tool, approval, permission, tracing` | 초안과 발송 분리; 최종 payload 승인 |
| EVAL-16 · 자격 증명 연결 | `deterministic_workflow` | `tool, permission` | 비밀 입력은 out-of-band; handle만 전달 |
| EVAL-17 · 장기 개인 선호 기억 | `bounded_agent` | `agent, state, tracing` | 단일 Agent와 범위 제한 선호 state |
| EVAL-18 · 도구 중복 혼동 | `bounded_agent` | `tool, agent, tracing` | 단일 Agent 유지; 승인 Tool 표면 정리 |
| EVAL-19 · 빠르게 변하는 API 문서 | `deterministic_workflow` | `skill, tool, script, eval` | 공식 버전 문서→생성→Script tests/Eval |
| EVAL-20 · 코드 리뷰와 자동 수정 | `deterministic_workflow` | `workflow, script, validator, sandbox, approval, tracing` | 제한된 review/repair와 sandbox 검사; merge는 사람 |
| EVAL-21 · 고정 보고서 생성 배치 | `deterministic_workflow` | `workflow, script, validator` | 고정 SQL·계산·출력; LLM은 해설만 |
| EVAL-22 · 사용자 정책 결정이 빠진 결제 자동화 | `direct_response` | `[]` | 정책 질문·계획만; 구매 행동 차단 |

### 19.3 권위 있는 구조화 매핑

출처 pointer는 각각 [I04]의 `/planner_evals/{index}`, [I05]의 `/base/{index}` 안의 정확한 필드를 가리킨다. component identity·version·digest·권한 값은 해당 원본이 제공한 범위를 넘어 채우지 않았다.

```json
{
  "schema_version": "1.0-research",
  "research_scope": "WORK_ORDER_SECTION_19_RESEARCH_GOLDEN_MAPPING_ONLY",
  "input_head": "e2e1628b7070e314f59f49cb03f435d47dd29abb",
  "source_blobs": {
    "I02": {
      "path": "docs/agent-authoring/workstreams/agent-workflow-assembler-research/INPUT_MANIFEST.yaml",
      "git_blob_sha1": "3243aab3f2266a722c46e78ecd9d0d45477a8393"
    },
    "I04": {
      "path": "docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/PLANNER_EVALS_01_22.json",
      "git_blob_sha1": "8f057b4d8acbe2c250de2d821db2bf582bc3d87d"
    },
    "I05": {
      "path": "docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/PLANNER_SCENARIO_RESULTS_22.json",
      "git_blob_sha1": "9e30cf4552f0a75c1ceab5c7073c33cdafa0b364"
    }
  },
  "source_status_fields_used_as_evidence": false,
  "canonical_fields": [
    "request",
    "expected_architecture",
    "expected_control_mode",
    "expected_components"
  ],
  "assembler_proposal_fields": [
    "assembly_decision",
    "entrypoint_and_control_owner",
    "required_bindings",
    "prohibited_or_rejected_assembly",
    "gate_or_reentry_result"
  ],
  "assembler_fields_origin": "RESEARCH_PROPOSAL",
  "runtime_execution": "NOT_RUN",
  "scenario_action_status_is_session_blocker": false,
  "mappings": [
    {
      "id": "EVAL-01",
      "source_title": "일회성 문장 다듬기",
      "request": "“아래 사과 메일을 더 공손하게 고쳐줘.” 외부 파일/발송/회사 고유 규칙 없음.",
      "expected_architecture": "`Prompt only`",
      "expected_control_mode": "direct_response",
      "expected_components": [],
      "assembly_decision": "현재 입력 문장을 한 번 변환해 답변하는 직접 응답을 제안한다. 빈 구성요소 집합을 보존하고 배포 가능한 Skill·Agent·Workflow artifact를 추가하지 않는다.",
      "entrypoint_and_control_owner": "사용자 프롬프트가 entrypoint이며 제안된 호스트 단일 응답 경로가 제어권을 가진다. 별도 자율 실행 루프나 외부 호출 경로는 없다.",
      "required_bindings": [
        "원 요청과 현재 입력 문장",
        "공손한 문장으로 바꾸는 응답 범위; 외부 파일·발송·회사 고유 정책을 포함하지 않음"
      ],
      "prohibited_or_rejected_assembly": [
        "Skill·Agent·RAG 추가",
        "메일 발송 Tool 또는 별도 workflow package 생성",
        "문장 작성과 메일 발송 완료를 동일시"
      ],
      "gate_or_reentry_result": "문장 변환 범위의 직접 응답으로 매핑한다. 발송, 조직 정책, 반복 절차가 새로 요구되면 PLANNER_REENTRY_REQUIRED로 돌려보내며 이를 현재 빈 구성에 합성하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/0/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/0/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/0/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/0/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/0/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/0/expected_components"
        }
      }
    },
    {
      "id": "EVAL-02",
      "source_title": "반복 ADR 작성 규칙",
      "request": "팀이 매주 ADR을 작성하며 필수 섹션·용어·검토 순서를 자주 누락. 외부 도구 없음.",
      "expected_architecture": "`Skill only`",
      "expected_control_mode": "direct_response",
      "expected_components": [
        "skill"
      ],
      "assembly_decision": "Skill 하나의 반복 ADR 작성 절차를 직접 응답에서 사용하도록 제안한다. Skill은 절차 제공자이며 독립 Agent나 강제 실행 보장으로 취급하지 않는다.",
      "entrypoint_and_control_owner": "ADR 작성 요청 또는 수동 Skill invocation이 entrypoint다. 호스트 응답 경로가 제어권을 유지하며 Skill은 필수 섹션·용어·검토 순서를 제공한다.",
      "required_bindings": [
        "승인된 Skill 정의의 버전과 digest",
        "필수 섹션·용어·검토 순서 및 해당 작성 요청",
        "실제 Skill Author 입력·출력 계약은 구현 단계에서 결박"
      ],
      "prohibited_or_rejected_assembly": [
        "별도 Agent 또는 외부 도구 추가",
        "Hook만으로 ADR 작성 품질을 보장한다고 주장",
        "자동 제출·배포 경로 추가"
      ],
      "gate_or_reentry_result": "Skill이 선택되었으므로 Skill Author 연결 대상이다. 외부 강제 검사나 자동 제출이 새로 필요하면 PLANNER_REENTRY_REQUIRED 또는 GATE_REENTRY_REQUIRED로 반환한다. Skill 문장 자체는 hard enforcement가 아니다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/1/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/1/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/1/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/1/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/1/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/1/expected_components"
        }
      }
    },
    {
      "id": "EVAL-03",
      "source_title": "작은 안정 운영 가이드",
      "request": "버전 고정된 운영 가이드 3개와 용어집을 기반으로 답변. 문서는 분기마다 수동 갱신.",
      "expected_architecture": "`Skill + Reference`",
      "expected_control_mode": "direct_response",
      "expected_components": [
        "skill",
        "reference"
      ],
      "assembly_decision": "버전 고정 가이드 3개와 용어집을 Reference inventory로 묶고 Skill에 필요한 참조만 연결하도록 제안한다. 정적 자료에 RAG를 추가하지 않는다.",
      "entrypoint_and_control_owner": "사용자 질문이 entrypoint이며 호스트의 단일 응답 경로가 제어권을 가진다. Skill은 승인된 Reference 범위에서 답변 절차를 제공한다.",
      "required_bindings": [
        "가이드·용어집의 목록, 버전, digest",
        "답변 근거의 파일·절·문단 위치",
        "분기별 수동 갱신 후 참조 binding 재검사 조건"
      ],
      "prohibited_or_rejected_assembly": [
        "RAG 또는 검색 서버 구축",
        "승인 범위 밖 외부 자료 자동 편입",
        "모든 가이드를 거대한 Skill 본문에 중복 복제"
      ],
      "gate_or_reentry_result": "원문 범위 밖 질문에는 no-evidence를 보존한다. 문서 버전 불일치나 지식 계약 변경은 KNOWLEDGE_REENTRY_REQUIRED로 반환하며, 과거 digest의 답변을 현재 근거로 승격하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/2/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/2/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/2/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/2/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/2/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/2/expected_components"
        }
      }
    },
    {
      "id": "EVAL-04",
      "source_title": "CSV 정규화",
      "request": "정해진 컬럼명 매핑·날짜 형식·중복 제거로 CSV를 변환하고 오류 행 목록 생성.",
      "expected_architecture": "`Skill + Script + Validator 또는 Script 중심 Workflow`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "script",
        "validator"
      ],
      "assembly_decision": "정규화된 기대값의 Script와 Validator만 고정 순서로 조립하도록 제안한다. 원문에 Skill 대안이 있어도 선택 집합에는 없으므로 추가하지 않는다.",
      "entrypoint_and_control_owner": "CSV 입력에서 정규화 Script, Validator, 변환 파일·오류 행 결과로 이어지는 호스트 고정 호출 경로를 제안한다. control_mode만으로 새 Workflow artifact나 실제 동작 중인 하네스를 주장하지 않는다.",
      "required_bindings": [
        "CSV 입력 schema와 컬럼 매핑·날짜 형식·중복 제거 규칙",
        "Script·Validator identity, digest, I/O 계약",
        "오류 행 결과 schema와 누락 처리",
        "출력 경로와 기존 파일 보호 정책"
      ],
      "prohibited_or_rejected_assembly": [
        "Agent가 각 행을 임의 판단",
        "Skill·workflow component 암묵 추가",
        "오류 행을 누락한 채 exit 0만으로 완료 선언"
      ],
      "gate_or_reentry_result": "검사 실패는 명시적 오류 행·실패 결과로 보존한다. artifact 부재 또는 schema 불일치는 EXECUTION_REENTRY_REQUIRED다. 연구 매핑 작성과 실제 CSV 실행 검증을 분리한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/3/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/3/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/3/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/3/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/3/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/3/expected_components"
        }
      }
    },
    {
      "id": "EVAL-05",
      "source_title": "정적 DB 스키마 기반 SQL 초안",
      "request": "소수 테이블의 버전 고정 스키마와 예시를 보고 SELECT 초안을 만들되 실행하지 않음.",
      "expected_architecture": "`Skill + Reference + SQL Validator`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "skill",
        "reference",
        "validator"
      ],
      "assembly_decision": "Skill과 Reference를 이용한 SELECT 초안 생성 후 Validator를 거치는 고정 경로를 제안한다. DB 실행 경로를 조립하지 않는다.",
      "entrypoint_and_control_owner": "SQL 초안 요청에서 생성 노드, SQL Validator, 검토용 초안 반환으로 이어지는 호스트 고정 제어 경로를 제안한다. 별도 workflow artifact는 추가하지 않는다.",
      "required_bindings": [
        "고정 schema·예시의 버전과 digest",
        "SQL dialect, SELECT 허용 범위, 금지문 규칙",
        "Skill·Reference·Validator의 승인 정의와 I/O 계약"
      ],
      "prohibited_or_rejected_assembly": [
        "RAG·DB write Tool·autonomous Agent 추가",
        "Validator 통과 후 실제 DB 자동 실행",
        "구문 검사 결과를 실제 DB 실행 결과로 표현"
      ],
      "gate_or_reentry_result": "구문·금지문 실패 시 초안의 승인된 반환 조건에 따라 중단 또는 수정한다. 실행 요청이 추가되면 PLANNER_REENTRY_REQUIRED 및 필요한 Execution/Gate 재진입을 요구한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/4/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/4/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/4/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/4/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/4/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/4/expected_components"
        }
      }
    },
    {
      "id": "EVAL-06",
      "source_title": "대규모 권한별 사내 규정 검색",
      "request": "수만 문서, 부서별 ACL, 매일 변경, 답변에 근거 링크 필요.",
      "expected_architecture": "`Skill + RAG + ACL + citation eval`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "skill",
        "rag",
        "permission",
        "eval"
      ],
      "assembly_decision": "선택된 Skill·RAG·permission·eval을 고정 검색·답변 경로에 연결하도록 제안한다. citation eval을 포함하고 Agent나 별도 Tool component를 추가하지 않는다.",
      "entrypoint_and_control_owner": "질문과 호출 주체가 entrypoint다. 제안된 호스트 고정 경로가 권한 검사, 허용 코퍼스 retrieval, 근거 답변, citation eval의 순서를 소유한다.",
      "required_bindings": [
        "원 사용자·tenant·부서와 검색 전 ACL 정책",
        "허용 corpus/index/snapshot 및 source·index·cache freshness",
        "삭제·권한 철회 반영 상태",
        "exact source span과 claim-level citation 평가 기준"
      ],
      "prohibited_or_rejected_assembly": [
        "공개 인덱스 또는 검색 후 ACL 필터만으로 우회",
        "정적 Reference 하나로 임의 대체",
        "LLM이 ACL filter·검색 범위를 확장",
        "citation 존재만으로 권한·내용 정확성 모두 통과 처리"
      ],
      "gate_or_reentry_result": "실제 권한 강제가 없으면 HARD_ENFORCEMENT_UNAVAILABLE다. 근거·인용·신선도 부족은 no-evidence 또는 KNOWLEDGE_REENTRY_REQUIRED로 보존한다. 이번 매핑은 실제 ACL/retrieval/citation 실행 증거가 아니다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/5/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/5/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/5/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/5/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/5/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/5/expected_components"
        }
      }
    },
    {
      "id": "EVAL-07",
      "source_title": "RAG near-miss",
      "request": "한 개의 25페이지 PDF와 2페이지 FAQ로 질문에 답함. 자료 버전 고정.",
      "expected_architecture": "`Skill + Reference 또는 Prompt + attached files`",
      "expected_control_mode": "direct_response",
      "expected_components": [
        "reference"
      ],
      "assembly_decision": "정규화 기대값에 선택된 Reference만 직접 연결하는 답변을 제안한다. 원문의 Skill 대안을 자동 선택하지 않는다.",
      "entrypoint_and_control_owner": "자료가 연결된 사용자 질문이 entrypoint이며 단일 호스트 응답 경로가 제어권을 가진다.",
      "required_bindings": [
        "PDF와 FAQ의 고정 버전·digest",
        "실제 제공된 문서 범위 및 페이지·문단 위치",
        "근거 부재 시 답변 범위"
      ],
      "prohibited_or_rejected_assembly": [
        "RAG·새 Skill·Agent 추가",
        "지식베이스 구축을 선행 요건으로 만들기",
        "현재 자료 범위 밖의 내용을 근거 있는 답으로 생성"
      ],
      "gate_or_reentry_result": "문서에 근거가 없으면 abstain한다. 범위·갱신·권한 요구가 달라지면 KNOWLEDGE_REENTRY_REQUIRED 또는 PLANNER_REENTRY_REQUIRED로 반환한다. 문서 분량은 보편적인 RAG 선택 임계값이 아니다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/6/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/6/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/6/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/6/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/6/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/6/expected_components"
        }
      }
    },
    {
      "id": "EVAL-08",
      "source_title": "현재 재고 조회",
      "request": "사용자가 SKU의 지금 재고를 묻고 읽기만 수행. 기존 ERP read-only API 존재.",
      "expected_architecture": "`Skill + existing Tool/API 또는 Tool only`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "tool"
      ],
      "assembly_decision": "기존 read-only ERP Tool/API를 재사용하는 고정 호출을 제안한다. 선택되지 않은 Skill·RAG·새 MCP를 추가하지 않는다.",
      "entrypoint_and_control_owner": "SKU 입력, 정해진 재고 Tool 호출, 응답 확인, 사용자 반환의 호스트 고정 경로를 제안한다. 실제 하네스 구현 적격성은 별도 확인 대상이다.",
      "required_bindings": [
        "ERP Tool identity/version과 SKU I/O schema",
        "read-only scope와 호출 주체",
        "원장 출처·조회 시각",
        "not-found·unknown·error와 실제 재고값의 구분"
      ],
      "prohibited_or_rejected_assembly": [
        "RAG의 과거 값으로 현재 재고 대체",
        "중복 API·MCP 구현",
        "재고 변경 권한 또는 자율 Agent loop 추가"
      ],
      "gate_or_reentry_result": "live source를 읽지 못하면 현재 재고를 단정하지 않는다. Tool I/O 불일치는 EXECUTION_REENTRY_REQUIRED이며 adapter를 조용히 만들지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/7/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/7/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/7/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/7/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/7/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/7/expected_components"
        }
      }
    },
    {
      "id": "EVAL-09",
      "source_title": "고정 야간 ETL",
      "request": "매일 02시 파일 수집→schema 검사→변환→DB 적재→대조. 분기와 재시도 규칙 고정.",
      "expected_architecture": "`Deterministic Workflow + Scripts + Validators`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "workflow",
        "script",
        "validator"
      ],
      "assembly_decision": "Workflow·Scripts·Validators로 수집, schema 검사, 변환, 적재, 대조를 고정하도록 제안한다. 이번 연구는 scheduler나 실제 배치를 생성하지 않는다.",
      "entrypoint_and_control_owner": "승인된 시간·배치 이벤트가 entrypoint이며 Workflow가 단계·분기·재시도 제어권을 가진다는 설계다.",
      "required_bindings": [
        "02시의 시간대·업무일 기준 및 입력·목표 schema",
        "Script·Validator identity와 digest",
        "run ID·idempotency key·적재 대상 범위",
        "대조 기준, retry·reconciliation·복구 계약"
      ],
      "prohibited_or_rejected_assembly": [
        "Agent의 임의 경로·적재 대상·재시도 선택",
        "대조 생략",
        "write timeout 직후 blind retry",
        "미선택 Approval·Permission component 자동 추가"
      ],
      "gate_or_reentry_result": "schema·대조 실패는 다음 단계 또는 완료를 차단한다. write 결과 불명은 OUTCOME_UNKNOWN 후 reconciliation한다. 추가 hard control component가 필요하면 PLANNER_REENTRY_REQUIRED/GATE_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/8/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/8/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/8/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/8/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/8/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/8/expected_components"
        }
      }
    },
    {
      "id": "EVAL-10",
      "source_title": "고정 고객 문의 라우팅",
      "request": "정해진 6개 카테고리와 조건에 따라 부서 큐로 전달. LLM은 자유문장을 구조화 분류.",
      "expected_architecture": "`Hybrid deterministic Workflow`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "workflow",
        "validator"
      ],
      "assembly_decision": "LLM을 Workflow의 분류 노드로 제한하고 Validator와 고정 매핑이 6개 카테고리의 큐를 결정하도록 제안한다. Agent로 제어 모드를 변경하지 않는다.",
      "entrypoint_and_control_owner": "고객 문의가 entrypoint다. Workflow가 분류 호출, category 검증, 고정 큐 dispatch를 제어한다.",
      "required_bindings": [
        "6개 category enum과 category-to-queue 매핑",
        "허용 queue 식별자 및 구조화 분류 응답",
        "미분류·경계 입력 처리와 승인된 fallback",
        "dispatch 결과 schema 및 중복 방지 계약"
      ],
      "prohibited_or_rejected_assembly": [
        "LLM의 자유 텍스트 큐 주소 생성",
        "큐 생성·범위 밖 변경",
        "자율 Agent 전환",
        "새 Tool·Script component 암묵 추가"
      ],
      "gate_or_reentry_result": "enum 밖 값·불명확 응답은 dispatch 전 중단하거나 승인된 fallback으로 보낸다. 실제 queue side effect 실행 계약이 없으면 EXECUTION_REENTRY_REQUIRED/GATE_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/9/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/9/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/9/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/9/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/9/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/9/expected_components"
        }
      }
    },
    {
      "id": "EVAL-11",
      "source_title": "개방형 장애 조사",
      "request": "로그·메트릭·배포 기록을 읽고 관찰 결과에 따라 다음 진단 도구와 가설이 달라짐. 변경은 하지 않음.",
      "expected_architecture": "`Bounded single Agent + read-only Tools + trace`",
      "expected_control_mode": "bounded_agent",
      "expected_components": [
        "agent",
        "tool",
        "tracing"
      ],
      "assembly_decision": "하나의 bounded Agent가 read-only Tools와 tracing을 사용해 관찰에 따라 다음 진단을 선택하도록 제안한다. 변경 행동은 포함하지 않는다.",
      "entrypoint_and_control_owner": "장애 조사 요청이 entrypoint다. Agent가 제한된 진단 선택을 하고 호스트가 허용 도구·예산·취소·종료 경계를 강제해야 한다.",
      "required_bindings": [
        "Tool identity와 read-only scope",
        "로그·메트릭·배포 기록의 시간 범위와 출처",
        "관찰 근거와 가설의 연결",
        "승인된 budget·종료·취소 조건과 trace identity"
      ],
      "prohibited_or_rejected_assembly": [
        "무제한 조사",
        "운영 변경 Tool·권한 추가",
        "고정 선형 workflow로 승인 mode 변경",
        "프롬프트 약속을 실제 read-only 강제로 취급"
      ],
      "gate_or_reentry_result": "예산 소진·변경 필요·근거 부족을 명시해 종료한다. 실제 권한 경계가 없으면 HARD_ENFORCEMENT_UNAVAILABLE다. 추가 행동은 PLANNER_REENTRY_REQUIRED/GATE_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/10/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/10/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/10/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/10/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/10/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/10/expected_components"
        }
      }
    },
    {
      "id": "EVAL-12",
      "source_title": "병렬 독립 심층조사",
      "request": "서로 독립된 12개 공식 출처군을 조사하고, 각 결과를 별도 verifier가 원문 대조한 뒤 합산.",
      "expected_architecture": "`Multi-agent 또는 orchestrator-worker Hybrid`",
      "expected_control_mode": "multi_agent",
      "expected_components": [
        "agent",
        "tracing",
        "eval"
      ],
      "assembly_decision": "agent·tracing·eval 범위에서 coordinator, worker, verifier 역할을 제안한다. 12개 출처군을 분할하고 검증된 결과를 결정적으로 취합한다. 출처군 수를 동시 worker 수의 보편 규칙으로 만들지 않는다.",
      "entrypoint_and_control_owner": "상위 조사 요청이 entrypoint다. coordinator가 배정·취합을 소유하고 worker는 배정된 출처군을 처리하며 verifier는 주장과 원문을 대조한다.",
      "required_bindings": [
        "immutable 과업·출처군 배정과 worker별 최소 context",
        "결과 schema·원문 위치·claim provenance",
        "verifier 판정과 merge·dedup·conflict 규칙",
        "전체 budget·부분 완료·종료·취소 및 trace 연결"
      ],
      "prohibited_or_rejected_assembly": [
        "공유 대화방을 context isolation으로 취급",
        "무병합 또는 무제한 재위임",
        "역할 이름만 달리하고 독립 검증을 주장",
        "새 Tool·Workflow·State component 자동 추가"
      ],
      "gate_or_reentry_result": "미검증 부분과 상충 근거는 보존하고 완료 범위를 제한한다. 독립 verifier identity·권한·실제 runtime는 향후 별도 검증한다. exact 역할·artifact binding이 필요하면 PLANNER_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/11/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/11/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/11/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/11/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/11/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/11/expected_components"
        }
      }
    },
    {
      "id": "EVAL-13",
      "source_title": "Multi-agent 과잉 설계 near-miss",
      "request": "800자 제품 소개글 하나를 작성하고 맞춤법 검사.",
      "expected_architecture": "`Prompt only 또는 Skill + deterministic spellcheck`",
      "expected_control_mode": "direct_response",
      "expected_components": [],
      "assembly_decision": "정규화된 빈 구성에 맞춰 단일 응답으로 소개글 작성과 표기 점검을 제안한다. 원문의 대안인 Skill·deterministic spellcheck를 자동 채택하지 않는다.",
      "entrypoint_and_control_owner": "제품 소개글 작성 요청이 entrypoint이며 단일 호스트 응답 경로가 제어권을 가진다.",
      "required_bindings": [
        "원 요청의 분량·스타일·표기 기준",
        "현재 제공된 제품 사실",
        "별도 spellcheck가 실행되지 않았다는 결과 범위"
      ],
      "prohibited_or_rejected_assembly": [
        "writer/reviewer/manager 3 Agent",
        "Skill·Script·Validator 암묵 추가",
        "별도 맞춤법 프로그램을 실행한 것처럼 표현"
      ],
      "gate_or_reentry_result": "직접 응답으로 매핑한다. 결정적 spellcheck가 새 필수 요건으로 지정되면 PLANNER_REENTRY_REQUIRED이며 현재 빈 구성의 기대값을 조용히 수정하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/12/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/12/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/12/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/12/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/12/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/12/expected_components"
        }
      }
    },
    {
      "id": "EVAL-14",
      "source_title": "운영 DB 삭제",
      "request": "조건에 맞는 운영 행 삭제 요청. 대상 수를 먼저 보여주고 팀장 승인 후 실행, 롤백 가능해야 함.",
      "expected_architecture": "`Deterministic Workflow + SQL Script/Validator + Human approval + least privilege + audit`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "workflow",
        "script",
        "validator",
        "approval",
        "permission",
        "tracing"
      ],
      "assembly_decision": "Workflow·SQL Script/Validator·approval·permission·tracing으로 미리보기, 승인, 실행, 대조·복구를 분리하도록 제안한다. 실제 운영 권한이나 승인을 부여하지 않는다.",
      "entrypoint_and_control_owner": "삭제 요청, 읽기 전용 대상 산출, 팀장 승인, 고정 실행 경로를 Workflow가 제어하는 설계다.",
      "required_bindings": [
        "DB·tenant·환경, exact SQL·조건·대상집합/수와 preview snapshot",
        "승인 identity·payload digest·만료·재사용 방지",
        "least privilege와 Script·Validator identity",
        "backup·rollback의 실제 가능 범위, idempotency·대조·audit"
      ],
      "prohibited_or_rejected_assembly": [
        "Agent가 생성한 SQL 즉시 실행",
        "승인 후 SQL·대상 변경",
        "stale preview로 삭제",
        "항상 rollback 가능하다고 주장",
        "결과 불명 쓰기의 blind retry"
      ],
      "gate_or_reentry_result": "exact approval·권한·복구 전제 중 하나라도 충족하지 않으면 write 차단이다. timeout은 OUTCOME_UNKNOWN으로 보존하고 reconciliation 전 재실행하지 않는다. 누락된 exact plan은 PLANNER_REENTRY_REQUIRED, 강제 수단 부재는 HARD_ENFORCEMENT_UNAVAILABLE다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/13/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/13/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/13/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/13/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/13/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/13/expected_components"
        }
      }
    },
    {
      "id": "EVAL-15",
      "source_title": "메일 초안과 발송",
      "request": "공지 내용을 만들고 3천 명에게 메일 발송. 발송 전 최종 수신자·제목·본문 승인.",
      "expected_architecture": "`Hybrid + Tool + Human approval + batch safeguards`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "tool",
        "approval",
        "permission",
        "tracing"
      ],
      "assembly_decision": "선택된 tool·approval·permission·tracing을 사용해 초안 생성, 최종 payload 승인, 제한된 발송을 고정 단계로 분리하도록 제안한다. 별도 workflow artifact는 추가하지 않는다.",
      "entrypoint_and_control_owner": "공지 작성 요청에서 최종 수신자·제목·본문 확인, 승인, 발송 호출로 이어지는 호스트 고정 제어 경로를 제안한다. Tool이 승인 범위를 넘어 자체 확장하지 않는다.",
      "required_bindings": [
        "최종 recipient 집합·count와 제목·본문의 exact payload",
        "승인 identity·expiry·payload digest",
        "발송 Tool identity와 permission scope",
        "batch 제한·중복 방지 key·recipient별 결과·reconciliation"
      ],
      "prohibited_or_rejected_assembly": [
        "Skill만으로 자동 발송",
        "승인 뒤 수신자·제목·본문 변경",
        "실패 batch 전체 blind retry",
        "메일 발송의 무조건적 회수·rollback 보장"
      ],
      "gate_or_reentry_result": "승인 payload 불일치 시 발송을 차단한다. 부분 발송과 OUTCOME_UNKNOWN을 분리하고 실제 결과 조회·대조 후 재시도한다. exact 승인/permission 계약은 향후 Planner/Gate binding 없이는 합성하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/14/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/14/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/14/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/14/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/14/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/14/expected_components"
        }
      }
    },
    {
      "id": "EVAL-16",
      "source_title": "자격 증명 연결",
      "request": "외부 서비스 API key가 필요해 사용자가 입력해야 함.",
      "expected_architecture": "`Out-of-band secret flow + Tool/MCP; no secret in LLM context`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "tool",
        "permission"
      ],
      "assembly_decision": "선택된 Tool·permission과 승인된 out-of-band credential 절차를 연결하도록 제안한다. 모델에는 비밀 대신 credential handle과 연결 상태만 노출한다.",
      "entrypoint_and_control_owner": "서비스 연결 요청에서 호스트/서비스의 비밀 입력 경로, credential binding, Tool 연결 확인으로 이어지는 고정 경로를 제안한다.",
      "required_bindings": [
        "서비스·계정·인증 주체와 허용 scope",
        "승인된 secret 저장소·credential handle",
        "만료·회수 조건",
        "secret 없는 응답·오류·trace·handoff 정책"
      ],
      "prohibited_or_rejected_assembly": [
        "채팅·LLM context에서 API key 수집",
        "secret를 prompt·state·log·handoff에 복사",
        "비밀 입력 Tool·broker를 연구 과정에서 임의 생성"
      ],
      "gate_or_reentry_result": "안전한 out-of-band 경로가 없으면 연결·사용을 차단하고 EXECUTION_REENTRY_REQUIRED/GATE_REENTRY_REQUIRED로 반환한다. 비밀값 없이 실패 상태를 보고하며 구현된 인증 흐름이 있다고 주장하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/15/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/15/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/15/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/15/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/15/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/15/expected_components"
        }
      }
    },
    {
      "id": "EVAL-17",
      "source_title": "장기 개인 선호 기억",
      "request": "사용자의 보고서 형식 선호를 세션 간 기억하되 사용자가 조회·수정·삭제 가능해야 함.",
      "expected_architecture": "`Single Agent/Skill + scoped persistent state`",
      "expected_control_mode": "bounded_agent",
      "expected_components": [
        "agent",
        "state",
        "tracing"
      ],
      "assembly_decision": "agent·state·tracing에 맞춰 하나의 bounded Agent가 scoped persistent state를 이용하도록 제안한다. 선택되지 않은 Skill·RAG를 추가하지 않는다.",
      "entrypoint_and_control_owner": "선호 조회·수정·삭제 요청이 entrypoint다. Agent의 동작 범위와 state의 주체·접근·삭제 경계는 실제 런타임이 강제해야 한다.",
      "required_bindings": [
        "user·tenant·용도 scope와 선호 schema",
        "저장·수정 근거 및 version·충돌 정책",
        "retention·조회·삭제·권한 철회·cache 반영",
        "비민감 trace 및 승인 state entrypoint 계약"
      ],
      "prohibited_or_rejected_assembly": [
        "모든 대화 원문 무기한 저장",
        "사용자·tenant 간 선호 공유",
        "삭제한 선호를 cache에서 재활성화",
        "raw state store·credential 노출 또는 별도 Tool 암묵 추가"
      ],
      "gate_or_reentry_result": "주체 binding·삭제 의미·저장 범위가 불명확하면 state 쓰기를 차단한다. 필요한 exact state/permission 계약은 구현 단계에 확인하며 없으면 PLANNER_REENTRY_REQUIRED/GATE_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/16/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/16/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/16/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/16/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/16/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/16/expected_components"
        }
      }
    },
    {
      "id": "EVAL-18",
      "source_title": "도구 중복 혼동",
      "request": "`search_customer`, `find_customer`, `lookup_client`가 겹쳐 Agent가 오선택.",
      "expected_architecture": "`Tool consolidation/namespace; Single Agent 유지`",
      "expected_control_mode": "bounded_agent",
      "expected_components": [
        "tool",
        "agent",
        "tracing"
      ],
      "assembly_decision": "한 Agent를 유지하고 승인 Tool의 identity·namespace·설명·alias를 명확히 하는 binding을 제안한다. 통합이라는 말로 새 capability나 adapter 생성을 승인하지 않는다.",
      "entrypoint_and_control_owner": "기존 고객 조회 의도에서 bounded Agent가 중복 해소된 승인 Tool 표면을 선택하는 경로를 제안한다. Agent 수를 늘리지 않는다.",
      "required_bindings": [
        "세 이름의 실제 기능·I/O·permission scope 비교",
        "canonical Tool identity와 alias·namespace 매핑",
        "선택 근거·호환성 및 trace",
        "승인된 component 정의와 의미 동등성 확인"
      ],
      "prohibited_or_rejected_assembly": [
        "즉시 Agent 3개 분리",
        "이름 유사성만으로 권한이 다른 Tool 합치기",
        "새 통합 Tool·adapter 코드 생성",
        "통합 후 권한 범위 확대"
      ],
      "gate_or_reentry_result": "기존 승인 정의의 alias·설명 개선으로 해결 가능한지 연구 판단을 남긴다. 기능·schema·권한 변경 또는 새 adapter가 필요하면 PLANNER_REENTRY_REQUIRED/EXECUTION_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/17/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/17/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/17/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/17/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/17/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/17/expected_components"
        }
      }
    },
    {
      "id": "EVAL-19",
      "source_title": "빠르게 변하는 API 문서",
      "request": "여러 API 버전의 현재 사용법을 바탕으로 코드 생성. 문서가 주기적으로 변경.",
      "expected_architecture": "`Skill + versioned retrieval/official docs Tool + Script tests`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "skill",
        "tool",
        "script",
        "eval"
      ],
      "assembly_decision": "skill·tool·script·eval을 문서 조회, 코드 초안 생성, Script tests와 평가의 고정 경로에 연결하도록 제안한다. RAG·정적 Reference·Agent를 추가하지 않는다.",
      "entrypoint_and_control_owner": "목표 API/version을 지정한 요청이 entrypoint다. 공식 문서 Tool 조회와 생성·검사를 호스트 고정 경로가 제어한다는 설계이며 별도 workflow artifact를 추가하지 않는다.",
      "required_bindings": [
        "공식 문서 출처·API version·조회 시각·snapshot",
        "생성 대상 SDK/API version",
        "test Script identity·digest·runtime·I/O",
        "Eval 기대값과 실제 실행 결과의 별도 기록"
      ],
      "prohibited_or_rejected_assembly": [
        "정적 Skill 본문을 영구 최신 정본으로 취급",
        "API 버전 혼합",
        "미실행 Script tests를 PASS로 보고",
        "미선택 Agent·RAG·Sandbox component 자동 추가"
      ],
      "gate_or_reentry_result": "목표 버전과 문서·test runtime 불일치는 Knowledge/Execution 재진입으로 반환한다. 생성 코드 실행에 새 sandbox capability가 필요하면 PLANNER_REENTRY_REQUIRED/GATE_REENTRY_REQUIRED다. 본 매핑의 tests 실행 상태는 NOT_RUN이다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/18/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/18/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/18/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/18/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/18/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/18/expected_components"
        }
      }
    },
    {
      "id": "EVAL-20",
      "source_title": "코드 리뷰와 자동 수정",
      "request": "PR diff를 분석하고 제안 수정 후 lint/test, merge는 사람만 가능.",
      "expected_architecture": "`Hybrid: LLM review/repair + deterministic lint/test + sandbox + human merge approval`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "workflow",
        "script",
        "validator",
        "sandbox",
        "approval",
        "tracing"
      ],
      "assembly_decision": "Workflow의 제한된 LLM review/repair 노드와 Script·Validator·sandbox·approval·tracing을 연결하도록 제안한다. 의미 검토 노드가 있다는 이유로 Agent component를 추가하지 않는다.",
      "entrypoint_and_control_owner": "PR diff/base commit에서 제안 수정, sandbox lint/test, 검토 결과로 이어지는 Workflow가 제어권을 가진다. merge는 사람의 별도 단계로 남긴다.",
      "required_bindings": [
        "repo·branch·base SHA와 허용 수정 경로·diff",
        "Script·Validator identity와 실제 검사 결과",
        "sandbox·권한·network 범위",
        "사람의 merge 승인 경계 및 trace"
      ],
      "prohibited_or_rejected_assembly": [
        "LLM 자기검사만으로 합격",
        "자동 merge",
        "미실행·실패 검사 숨기기",
        "작업 중 head 변경 무시",
        "선택되지 않은 Agent·Tool 추가"
      ],
      "gate_or_reentry_result": "sandbox·scope·검사 조건 불충족 시 실행 적격이나 완료를 선언하지 않는다. 실제 hard boundary가 없으면 HARD_ENFORCEMENT_UNAVAILABLE다. 사람 승인 없는 merge는 차단하며 이번 매핑은 merge 기능을 추가하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/19/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/19/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/19/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/19/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/19/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/19/expected_components"
        }
      }
    },
    {
      "id": "EVAL-21",
      "source_title": "고정 보고서 생성 배치",
      "request": "DB 조회 SQL은 승인된 템플릿, 표 계산과 파일 출력은 코드, 해설 문단만 LLM.",
      "expected_architecture": "`Deterministic Workflow/Hybrid`",
      "expected_control_mode": "deterministic_workflow",
      "expected_components": [
        "workflow",
        "script",
        "validator"
      ],
      "assembly_decision": "Workflow·Script·Validator로 승인 SQL 템플릿 조회, 계산, 파일 출력을 담당하고 LLM을 해설 문단에만 제한하도록 제안한다.",
      "entrypoint_and_control_owner": "정해진 배치 입력에서 고정 Workflow가 제어권을 가진다. LLM이 SQL 템플릿·계산식·분기 순서를 바꾸지 않는다.",
      "required_bindings": [
        "SQL template/version과 허용 parameters·조회 scope",
        "계산식·출력 schema 및 Script·Validator identity",
        "계산값과 해설의 근거 대응",
        "파일 경로·기존 파일 보호·overwrite 정책"
      ],
      "prohibited_or_rejected_assembly": [
        "전체 과정을 Agent가 계획",
        "LLM의 SQL 템플릿 교체·계산값 수정",
        "별도 DB Tool·Skill·Tracing component 암묵 추가",
        "해설을 실제 계산 결과보다 우선"
      ],
      "gate_or_reentry_result": "schema·계산·출력 검증 실패는 완료를 차단한다. DB 호출은 승인 Script 계약 안에 결박하고 새 capability가 필요하면 PLANNER_REENTRY_REQUIRED/EXECUTION_REENTRY_REQUIRED로 반환한다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "PROPOSED_PATH_CONDITIONAL",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/20/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/20/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/20/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/20/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/20/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/20/expected_components"
        }
      }
    },
    {
      "id": "EVAL-22",
      "source_title": "사용자 정책 결정이 빠진 결제 자동화",
      "request": "“필요한 물품을 알아서 구매해줘”라고만 요청, 한도·승인자·판매자 정책 없음.",
      "expected_architecture": "`Blocked after read-only plan`",
      "expected_control_mode": "direct_response",
      "expected_components": [],
      "assembly_decision": "direct_response와 빈 구성요소 집합을 보존한다. 현재 문맥에서 읽기 전용 계획과 필요한 정책 질문만 제시하고 구매 실행 구조를 조립하지 않도록 제안한다.",
      "entrypoint_and_control_owner": "원 요청에서 호스트의 설명·확인 응답으로 종료한다. payment Agent·Tool 호출 경로를 만들지 않으며 읽기 전용 계획을 이유로 외부 Tool을 임의 호출하지 않는다.",
      "required_bindings": [
        "원 요청",
        "미결 정책 목록: 구매 한도·승인자·판매자 정책",
        "이 정책을 추정·자동 채우기하지 않는 행동 경계"
      ],
      "prohibited_or_rejected_assembly": [
        "적정 가격을 추정해 구매",
        "payment Tool·Agent·승인 서비스 자동 추가",
        "사용자 정책을 모델이 대신 결정",
        "빈 구성의 정상 직접 응답 사례와 같은 행동 허용으로 취급"
      ],
      "gate_or_reentry_result": "시나리오의 구매 행동은 BLOCKED_FOR_DECISION이다. 정책 확정 후 PLANNER_REENTRY_REQUIRED로 돌아가 새 승인 계획을 받는다. 이는 올바른 연구 매핑 결과이며 이번 조사 세션의 blocker를 뜻하지 않는다.",
      "research_status": "MAPPED",
      "runtime_execution": "NOT_RUN",
      "exact_binding": "DEFERRED_TO_IMPLEMENTATION",
      "assembler_fields_origin": "RESEARCH_PROPOSAL",
      "scenario_action_status": "BLOCKED_FOR_DECISION",
      "source_pointers": {
        "id": {
          "source": "I04",
          "pointer": "/planner_evals/21/id"
        },
        "source_title": {
          "source": "I05",
          "pointer": "/base/21/source_title"
        },
        "request": {
          "source": "I04",
          "pointer": "/planner_evals/21/fields/요청"
        },
        "expected_architecture": {
          "source": "I04",
          "pointer": "/planner_evals/21/fields/기대 아키텍처"
        },
        "expected_control_mode": {
          "source": "I05",
          "pointer": "/base/21/expected_control_mode"
        },
        "expected_components": {
          "source": "I05",
          "pointer": "/base/21/expected_components"
        }
      }
    }
  ]
}
```

## 20. Planner·Gate·Execution·Knowledge·Skill Author 연결

**연구 제안:** 생성기는 모두 무조건 호출하는 파이프라인이 아니다. Planner의 mode와 selected set이 downstream 호출 여부를 결정한다. Assembler는 승인 artifact가 도착했는지·서로 맞는지 확인하고 재진입 이유를 소관 단계에 전달한다. [I01], [I03]

| 단계 | Assembler가 소비할 것 | 호출·skip 및 재진입 |
|---|---|---|
| Planner | mode, selected components, 선택·기각 근거, capability/AC와 승인 scope | 새 component·목표·권한·정책 필요 시 `PLANNER_REENTRY_REQUIRED`; §19에서는 승인된 두 catalog 사용 |
| Gate | 적용 지점·정책·판정 schema·hard enforcement 요구·승인 payload | 고위험 경로의 누락·충돌은 `GATE_REENTRY_REQUIRED`; prompt로 통제 대체 금지 |
| Execution | 승인 Script/Validator/Tool entrypoint, I/O, runtime 적격성, error/recovery 의미 | 인터페이스/실행기/adapter 부족은 `EXECUTION_REENTRY_REQUIRED`; unsupported는 그대로 보존 |
| Knowledge | source authority·ACL·snapshot·freshness·citation·no-evidence 계약 | 필요한 지식 종류만 연결; 변경·누락은 `KNOWLEDGE_REENTRY_REQUIRED` |
| Skill Author | 선택된 개별 Skill의 승인 정의·검사 결과 | `skill`이 없으면 호출하지 않음; 전체 오케스트레이션 책임을 Skill 하나에 몰지 않음 |
| Assembler | 위 계약의 정합 조합·entrypoint·manifest·평가 요구 | 자체 코드·새 Tool/RAG 생성 권한 없음 |
| 독립 검토/평가 | 정확한 package subject·policy·실제 실행 결과와 한계 | 연구 검토, local candidate, production 판단을 분리 |

예를 들어 EVAL-08은 기존 live Tool만 선택되었으므로 Skill Author·RAG Builder를 자동 호출하지 않는다. EVAL-07은 Reference만, EVAL-04는 Script/Validator만 조립한다. EVAL-12의 verifier는 선택된 agent/eval 범위의 역할 제안이며 독립 신원 증거가 자동 생성되는 것은 아니다. [I04], [I05]

재진입 기록에는 현재 source refs, 충돌한 계약 필드, 필요한 최소 변경, 영향받는 entrypoint와 invalidated 결과를 포함하도록 제안한다. upstream을 조용히 수정한 뒤 원래 승인에 끼워 넣지 않는다. 추가 검토가 필요한 실행 의존성과 현재 연구가 끝났는지는 분리한다.

## 21. 우리 하네스 구현안

이 절은 **향후 구현안**이며 현재 실행 코드·설정·운영 자원의 변경사항이 아니다. 이번 제출은 조사 보고서·상태·로그·출력 manifest뿐이다. [I06]

### 21.1 최소 경계

하네스의 중심을 선택 보존·계약 검증·artifact 결박의 결정적 단계로 둔다. 자연어를 다시 해석해 새 component를 선택하는 두 번째 Planner를 Assembler 안에 만들지 않는다. canonical field의 파싱·ID 집합 대조·digest·버전·schema·필수 evidence 검사는 코드로 검증할 수 있는 후보이며, 미구현 항목은 요구사항으로 남긴다.

| 논리 모듈 | 입력 → 출력 | 중요한 경계 |
|---|---|---|
| 승인 입력 reader | source manifests → 고정 artifact refs | missing/mismatch를 대체 자료로 숨기지 않음 |
| selection guard | Planner mode/set → 보존된 assembly selection | 빈 set·비Agent 기준선 허용 |
| contract binder | 승인 component I/O·상태·정책 → typed binding | incompatible adapter는 새로 만들지 않음 |
| context/handoff planner | 역할·근거·권한 → 최소 projection과 전달 정책 | 새로운 memory·Tool·권한 추가 금지 |
| runtime eligibility checker | 요구 통제·actual receipts → 적격/미검증/unsupported | 파일 존재와 실제 host 활성 구분 |
| manifest packager | 고정 파일·의존성 → inventory와 외부 digest | 사용자 파일·같은 이름의 다른 artifact 보호 |
| result/review handoff | static 결과와 실제 receipt → 제한이 명시된 결과 | static mapping·runtime·release 승격 금지 |

이 모듈 분할 자체가 추가 Agent나 실행 component 7개를 만들라는 뜻은 아니다. 구현 내부 책임 분리의 제안이며, 실 구현 구조는 승인된 범위와 기존 reusable artifact를 확인한 뒤 정한다.

### 21.2 알려진 경계의 반영

승인된 UPSTREAM_CONTRACT_SUMMARY에는 과거 복구 전 상태가 포함되어 있다. 공유 board의 현재 관찰 상태는 upstream 재진입 및 downstream 검증 대기를 구분한다. 이 연구는 그 상태 파일을 근거로 구현을 완료했다고 주장하지 않으며, 다른 workstream의 실제 코드·evidence를 이번 범위에서 감사하지 않았다. **§19 연구용 승인 입력이 충분하다는 결정과 upstream 구현 검증이 완료되었다는 결정은 다르다.** [I03], [I09]

고위험 쓰기·운영 IAM·tenant ACL·검증된 sandbox·exact approval 서비스·durable production runtime·신뢰 attestation 발급은 실제 구현 및 시험 범위를 별도로 정해야 한다. `HARD_ENFORCEMENT_UNAVAILABLE` 또는 `UNSUPPORTED_RUNTIME_PACK`은 분석 결과로 보존하고, 문장형 Skill로 대체해 실행을 허용하지 않는다. [I01], [I03]

## 22. 단계별 구현 순서와 MVP 경계

아래는 연구가 제안하는 **후속 구현 순서**다. 이번 조사 세션에서 구현을 시작하거나 자동화를 생성하지 않는다. [I01], [I06]

| 단계 | 목적 | 완료 판정에 필요한 실제 근거 |
|---|---|---|
| A0 입력·선택 보존 | 승인 manifest, exact ID/selection, source scope·digest 확인 | 정상/누락/변조/중복 입력 검사와 재진입 결과 |
| A1 정적 계약·package | typed I/O·version·참조 DAG·inventory·사용자 파일 경계 | canonical serialization/byte hash, 호환/충돌/누락 검증 |
| A2 최소 비Agent 경로 | direct response와 승인된 결정적 조합부터 실제 entrypoint 검증 | EVAL-01/04/07/08/13/21 같은 최소 기준선의 실제 결과 |
| A3 Gate·권한·복구 | 실제 host 통제와 side-effect 승인·unknown·reconciliation | 안전한 시험 환경의 denied/expired/replayed approval, timeout·부분 실패 결과 |
| A4 bounded Agent | 선택된 도구·state·trace·예산·종료 검증 | EVAL-11/17/18의 실제 사용자 경로·권한·삭제·종료 관찰 |
| A5 multi-agent | 격리·분배·검증·merge·취소 검증 | EVAL-12의 source 배정, worker 결과, verifier, conflict/partial 처리 |
| A6 설치·전달·검토 | idempotent install, migration·rollback, exact subject 검토 | 사용자 파일 보존·설정 활성·entrypoint 재확인 및 독립 검토 |

MVP는 소스가 충분한 범위에서 계약 보존과 정적 결박을 검증하고 비Agent 기준선을 실제로 확인하는 수준으로 제안한다. 모든 runtime pack, multi-agent, production write를 동시에 지원하려고 범위를 넓히지 않는다. 미지원 범위는 명시적 거절과 재진입으로 유지한다.

운영 release는 A6 통과만으로 자동 승인되지 않는다. 배포 대상·운영 정책·사람 승인·실제 통제·독립 검토·현재 subject를 별도로 확인해야 한다. 이번 PR은 연구 검토용 Draft 상태를 유지하며 merge나 deployment를 수행하지 않는다.

## 23. 한계와 미확인 사항

1. **정본 22개는 기대값이다.** §19는 승인된 입력에 대응하는 연구 매핑을 완성한다. Planner를 다시 22회 실행하거나 Assembler가 외부 업무를 완료한 증거가 아니다. 원본 `PASS`와 paraphrase는 실행 판정에 사용하지 않았다. [I02], [I04], [I05]
2. **정확한 실행 binding은 별도다.** 실제 component artifact ID/digest, capability/AC/Gate ID, permission, full plan 및 runtime receipt를 이 보고서가 만들지 않는다. 이후 필요할 때 책임 단계로 재진입한다. 이는 §19 조사 blocker가 아니다. [I02], [I08]
3. **제품 기능과 Factory 가용성은 다르다.** 문서에서 Claude Hook·SDK guardrail·LangGraph checkpoint·MCP authorization을 확인했어도 이 저장소에서 활성화되었다고 증명하지 않았다. 문서의 live 버전과 설치 버전도 같다고 가정하지 않는다.
4. **실제 실행은 미수행이다.** 실제 Agent/SDK/Workflow, 22개 업무 entrypoint, DB 삭제·발송·credential 연결, 설치·rollback, host Hook 차단, mutation·ablation·E2E·production은 `NOT_RUN`이다. 제한된 문서 검사만 실제로 수행했다.
5. **교차 검토는 같은 조사 세션의 동료 검토다.** 별도 역할의 검토가 독립된 인증 신원·신뢰 attestation 발급을 증명하지 않는다. 최종 `VERIFIED_RESEARCH` 판정은 총괄/검토 절차의 몫이다.
6. **이전 보고서 원문은 재사용하지 않았다.** 안전하게 복구 가능한 동일 파일이 없어 이번 승인 입력·현재 1차자료로 다시 작성했다. 과거 규칙 수량·보고서 hash·완료 주장과 이번 제출본은 다르다.
7. **스키마는 제안이다.** YAML 파싱·필드 존재·정적 참조 검사는 실행 가능한 compiler·runtime validator·설치 transaction을 구현한 결과가 아니다. source identity·hard enforcement·정책 독립성은 후속 검증이 필요하다.
8. **보고서 전달 검사의 범위가 제한된다.** GitHub connector로 PR과 정확한 head의 파일을 다시 읽어 내용·digest·구조를 검증한다. GitHub UI의 실제 시각적 렌더링, Claude 사용자 화면, 운영 시스템의 실제 entrypoint 동작은 확인하지 않는다.

검토 중 발견한 정합성 문제는 제출 전에 수정했다. 정적 설치 정책의 실제 승인 참조는 후행 기록으로 분리했고, 취소/차단/실패 후 늦게 도착하는 외부 결과는 별도 operation effect machine에서 추적하도록 했다. bearer credential과 권한을 부여하지 않는 opaque reference를 구분했으며, fencing과 동등한 배타적 직렬화의 허용 조건 및 평가 종류의 표현을 맞췄다. 이것은 **연구 문서의 보정**이며 해당 runtime 동작의 실행 검증이 아니다.

## 24. 결론-출처 추적표

| 결론/판단 | 근거 종류·출처 | 보고서의 적용 위치 |
|---|---|---|
| mode와 selected set을 보존하고 새 기능은 재진입 | 승인 계약 [I01], [I03]; 정규화 기대값 [I05] | §1~4, ASM-02/03/06, §19 |
| 승인된 22개 입력은 §19에 충분하며 PASS는 기대값일 뿐 | 승인 범위 [I02], [I08]; 실제 catalog [I04], [I05] | §0/2/19/23, ASM-04/05 |
| Skill을 선택할 때만 Skill Author를 연결 | 승인 계약 [I01], [I03]; 규격 구조 [S01], [S02] | §4/20, ASM-03 |
| Skill fork·Agent preload·권한 설정은 서로 다름 | 현재 제품 문서 [C01], [C02], [C04], [C05] | §4/6/8, ASM-09/10/13/14 |
| Skill 로딩 명령의 통제는 host 버전·전용 event를 확인 | 제품 문서/릴리스 [C01], [C03], [C06] | §7/13, ASM-12/13/14 |
| agent-level guardrail은 모든 실행 경로의 Gate가 아님 | SDK pinned 문서 [O02], [O04] | §7/8, ASM-12/13 |
| handoff의 history·제어권·승인은 명시적으로 결박 | SDK [O01], [O03], [O07], 승인 원칙 [I03] | §8/15, ASM-10/11/18 |
| state와 trace 존재만으로 인증·무결성·독립 감사 아님 | SDK [O05], [O06], provenance [D04], [D05] | §6/11/15, ASM-05/27/28 |
| fixed workflow 안에 LLM 노드가 있어도 Agent를 추가하지 않음 | 승인 기대값 [I04], [I05], 제품 구분 [L01] | §3/19, ASM-02/09 |
| checkpoint·retry는 외부 side effect 원자성을 보장하지 않음 | LangGraph [L02], [L03], [L05], AWS [D01] | §9/15, ASM-20/21/23 |
| MCP의 데이터·Prompt·Tool·권한·secret 경계를 분리 | 날짜 고정 명세 [M01]~[M06] | §5/7/8, ASM-10/12/15/27 |
| 병렬 격리·원문 검증·merge가 필요하며 Agent 수는 별도 | 정본 EVAL-12 [I04], 제품/연구 [L04], [P01], [P02] | §6/9/19, ASM-17/22/24 |
| artifact digest는 비순환으로 결박하고 receipt는 후행 | 규격 사실 [D04], [D05], [D07]을 토대로 한 연구 설계 | §2/11/14/15, ASM-07/08 |
| 파일 무결성과 안전한 install/rollback은 구별 | TUF [D06] 및 Factory 설치 요구 [I01] | §10/15, ASM-25/26 |
| 개별 통과의 합계 대신 특정 조합·진입점·음성 경로를 평가 | 평가/계약/실패 연구 [S03], [D03], [P02], 승인 원칙 [I03] | §12/17/18, ASM-28/29 |
| local 결과와 production/merge 승인은 별도 | 승인된 작업·소유 경계 [I01], [I06], [I07] | §12/15/22/23, ASM-30 |

문서가 제시한 제품 사실과 그 사실을 바탕으로 제안한 Factory의 강제 정책은 동일하지 않다. traceability 표의 연결은 출처의 지지 범위를 표시하며, 전체 제안이 제품에서 이미 구현됐다는 인증으로 사용하지 않는다.

## 25. 전체 출처

총 **49개 출처**: 승인 입력·관리 자료 12개와 외부 1차자료 37개. 접근 기준일은 모두 **2026-11-26 KST**다. commit 또는 명세 날짜로 고정한 자료와 live 문서를 구분했다. 아래의 source ID는 본문 참조와 1:1로 대응한다. URL의 존재만이 아니라 관련 원문을 읽어 근거로 사용했으며, 제품 문서 확인을 실제 Factory runtime 실행으로 간주하지 않는다.

### 25.1 승인 입력과 관리 자료

| ID | 원문 | 버전·고정 기준 |
|---|---|---|
| I01 | [Work Order](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/WORK_ORDER.md) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I02 | [Approved Input Manifest](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/INPUT_MANIFEST.yaml) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I03 | [Upstream Contract Summary](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/UPSTREAM_CONTRACT_SUMMARY.md) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I04 | [Planner canonical request catalog](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/PLANNER_EVALS_01_22.json) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I05 | [Planner normalized expectations](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/PLANNER_SCENARIO_RESULTS_22.json) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I06 | [Ownership](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/OWNERSHIP.yaml) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I07 | [Session start](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/SESSION_START_PROMPT.md) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I08 | [Approved section 19 source decision](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/CURRENT_SESSION_STATE.yaml) | e2e1628b7070e314f59f49cb03f435d47dd29abb |
| I09 | [Orchestrator assignment board](https://github.com/easyseop/claude-skill-by-seop/blob/42e06122d738a590fc516cccd28327de42f15743/docs/agent-authoring/session-collaboration/MASTER_WORKSTREAM_BOARD.yaml) | 42e06122d738a590fc516cccd28327de42f15743 |
| I10 | [Prepared input boundary policy](https://github.com/easyseop/claude-skill-by-seop/blob/42e06122d738a590fc516cccd28327de42f15743/docs/agent-authoring/session-collaboration/WORKSTREAM_BOUNDARIES.json) | 42e06122d738a590fc516cccd28327de42f15743 |
| I11 | [Prepared input overrides](https://github.com/easyseop/claude-skill-by-seop/blob/42e06122d738a590fc516cccd28327de42f15743/docs/agent-authoring/session-collaboration/PREPARED_INPUT_OVERRIDES.json) | 42e06122d738a590fc516cccd28327de42f15743 |
| I12 | [Remote Research Mode](https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/REMOTE_RESEARCH_MODE.md) | e2e1628b7070e314f59f49cb03f435d47dd29abb |

### 25.2 Agent Skills와 Claude Code

| ID | 원문 | 버전·고정 기준 |
|---|---|---|
| S01 | [Agent Skills specification](https://agentskills.io/specification) · [고정 원문](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx) | Agent Skills commit 83021e2be457a9b6679148719c1f6074f0ad975e; Git blob `d9a2db099d905da8b879a5c6f996728073985279` |
| S02 | [Agent Skills scripts](https://agentskills.io/skill-creation/using-scripts) · [고정 원문](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/using-scripts.mdx) | Agent Skills commit 83021e2be457a9b6679148719c1f6074f0ad975e; Git blob `11ce443e9b17281305e2ac593ef155a83a38a1dd` |
| S03 | [Agent Skills evaluation](https://agentskills.io/skill-creation/evaluating-skills) · [고정 원문](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/evaluating-skills.mdx) | Agent Skills commit 83021e2be457a9b6679148719c1f6074f0ad975e; Git blob `7c90d54295be88ac40de7f19db0876cee6180c4e` |
| C01 | [Claude Code skills](https://code.claude.com/docs/en/skills) | live, unversioned; release context v2.1.332 |
| C02 | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | live, unversioned |
| C03 | [Claude Code hooks](https://code.claude.com/docs/en/hooks) | live; event/type/version conditions apply |
| C04 | [Claude Code permissions](https://code.claude.com/docs/en/permissions) | live, unversioned |
| C05 | [Claude Code settings](https://code.claude.com/docs/en/settings) | live, unversioned |
| C06 | [Claude Code release v2.1.332](https://github.com/anthropics/claude-code/releases/tag/v2.1.332) | tag commit eb8e6d253d0dbee6e52fb0d5fdcb72c9396fe3e8; published 2026-11-25 |

### 25.3 OpenAI Agents SDK와 LangGraph

| ID | 원문 | 버전·고정 기준 |
|---|---|---|
| O01 | [OpenAI Agents SDK agents](https://openai.github.io/openai-agents-python/agents/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/agents.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `c4d2adf841926d446206ca7777f4e5bc345144d1` |
| O02 | [OpenAI Agents SDK tools](https://openai.github.io/openai-agents-python/tools/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/tools.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `755892d143611dac86a7d20bd028669b4fbcf115` |
| O03 | [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/handoffs.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `05e1d10ccf53aa4ecedff2ade88371bb14c35e36` |
| O04 | [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/guardrails.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `d7dfdcbc31a0343c4c29c75e86820ac2256d418e` |
| O05 | [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/sessions/index.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `115b570da50f1a0b52ee7bc109b41f735c4de73c` |
| O06 | [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/tracing.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `7da50e985a00de8a234402cdd55dfa79885f95fd` |
| O07 | [OpenAI Agents SDK human in the loop](https://openai.github.io/openai-agents-python/human_in_the_loop/) · [고정 원문](https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/human_in_the_loop.md) | v0.26.0; 0ad2d63a9371a23333a95ea6878141a826c9cdda; Git blob `047830fdfb92eef7012af1f26b64f4f8166d1ae3` |
| O08 | [OpenAI Agents Python release v0.26.0](https://github.com/openai/openai-agents-python/releases/tag/v0.26.0) | published 2026-11-24; 0ad2d63a9371a23333a95ea6878141a826c9cdda |
| L01 | [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | live, installed runtime unverified |
| L02 | [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | live, installed runtime unverified |
| L03 | [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | live, installed runtime unverified |
| L04 | [LangGraph subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs) | live, installed runtime unverified |
| L05 | [LangGraph fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance) | live, installed runtime unverified |

### 25.4 MCP 명세

| ID | 원문 | 버전·고정 기준 |
|---|---|---|
| M01 | [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28) | 2026-07-28 |
| M02 | [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) | 2026-07-28 |
| M03 | [MCP resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) | 2026-07-28 |
| M04 | [MCP prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts) | 2026-07-28 |
| M05 | [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) | 2026-07-28; HTTP authorization scope |
| M06 | [MCP elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation) | 2026-07-28 |

### 25.5 신뢰성·상태·계약·공급망

| ID | 원문 | 버전·고정 기준 |
|---|---|---|
| D01 | [AWS retries and idempotency](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | live official design article |
| D02 | [SCXML state machine notation](https://www.w3.org/TR/2015/REC-scxml-20150901/) | W3C Recommendation 2015-09-01 |
| D03 | [Pact can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy) | live official contract-testing docs |
| D04 | [SLSA build provenance](https://slsa.dev/spec/v1.2/build-provenance) | v1.2 |
| D05 | [in-toto Statement](https://github.com/in-toto/attestation/blob/50bf01716982189898823e90586075f37cd9bb7d/spec/v1/statement.md) | Statement v1; commit 50bf01716982189898823e90586075f37cd9bb7d; blob 630f773cb530fe5989fe2dbc30e7f73239cd943a |
| D06 | [The Update Framework specification](https://theupdateframework.github.io/specification/v1.0.36/) | v1.0.36 |
| D07 | [JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html) | RFC 8785, Informational, 2020-06 |

### 25.6 Multi-agent 사례와 원 논문

| ID | 원문 | 버전·고정 기준 |
|---|---|---|
| P01 | [Anthropic multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) | official engineering case study, 2025-06-13 |
| P02 | [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657v3) | original paper, arXiv v3, 2025-10-26 |

### 25.7 재현 경계

승인 입력은 §0.2의 input head와 INPUT_MANIFEST/중앙 봉인의 Git blob에 결박했다. 공식 저장소의 고정 원문은 위 commit·blob으로 다시 확인할 수 있다. live 제품 문서는 해당 접근 시점의 내용이며 이후 변경될 수 있다. 패키지 버전의 release 확인과 문서 읽기는 설치·실행 검증을 대신하지 않는다.

이 보고서의 SHA-256은 외부 OUTPUT_MANIFEST에 기록한다. 보고서 본문에 자기 hash나 미래 제출 commit을 넣어 순환 참조를 만들지 않는다. 제출 이후 정확한 head의 전달 확인과 boundary CI는 해당 PR의 최신 head·Actions 결과로 확인해야 한다.

[I01]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/WORK_ORDER.md
[I02]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/INPUT_MANIFEST.yaml
[I03]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/UPSTREAM_CONTRACT_SUMMARY.md
[I04]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/PLANNER_EVALS_01_22.json
[I05]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/inputs/PLANNER_SCENARIO_RESULTS_22.json
[I06]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/OWNERSHIP.yaml
[I07]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/SESSION_START_PROMPT.md
[I08]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/CURRENT_SESSION_STATE.yaml
[I09]: https://github.com/easyseop/claude-skill-by-seop/blob/42e06122d738a590fc516cccd28327de42f15743/docs/agent-authoring/session-collaboration/MASTER_WORKSTREAM_BOARD.yaml
[I10]: https://github.com/easyseop/claude-skill-by-seop/blob/42e06122d738a590fc516cccd28327de42f15743/docs/agent-authoring/session-collaboration/WORKSTREAM_BOUNDARIES.json
[I11]: https://github.com/easyseop/claude-skill-by-seop/blob/42e06122d738a590fc516cccd28327de42f15743/docs/agent-authoring/session-collaboration/PREPARED_INPUT_OVERRIDES.json
[I12]: https://github.com/easyseop/claude-skill-by-seop/blob/e2e1628b7070e314f59f49cb03f435d47dd29abb/docs/agent-authoring/workstreams/agent-workflow-assembler-research/REMOTE_RESEARCH_MODE.md
[S01]: https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx
[S02]: https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/using-scripts.mdx
[S03]: https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/skill-creation/evaluating-skills.mdx
[C01]: https://code.claude.com/docs/en/skills
[C02]: https://code.claude.com/docs/en/sub-agents
[C03]: https://code.claude.com/docs/en/hooks
[C04]: https://code.claude.com/docs/en/permissions
[C05]: https://code.claude.com/docs/en/settings
[C06]: https://github.com/anthropics/claude-code/releases/tag/v2.1.332
[O01]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/agents.md
[O02]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/tools.md
[O03]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/handoffs.md
[O04]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/guardrails.md
[O05]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/sessions/index.md
[O06]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/tracing.md
[O07]: https://github.com/openai/openai-agents-python/blob/0ad2d63a9371a23333a95ea6878141a826c9cdda/docs/human_in_the_loop.md
[O08]: https://github.com/openai/openai-agents-python/releases/tag/v0.26.0
[L01]: https://docs.langchain.com/oss/python/langgraph/workflows-agents
[L02]: https://docs.langchain.com/oss/python/langgraph/persistence
[L03]: https://docs.langchain.com/oss/python/langgraph/interrupts
[L04]: https://docs.langchain.com/oss/python/langgraph/use-subgraphs
[L05]: https://docs.langchain.com/oss/python/langgraph/fault-tolerance
[M01]: https://modelcontextprotocol.io/specification/2026-07-28
[M02]: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
[M03]: https://modelcontextprotocol.io/specification/2026-07-28/server/resources
[M04]: https://modelcontextprotocol.io/specification/2026-07-28/server/prompts
[M05]: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[M06]: https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
[D01]: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
[D02]: https://www.w3.org/TR/2015/REC-scxml-20150901/
[D03]: https://docs.pact.io/pact_broker/can_i_deploy
[D04]: https://slsa.dev/spec/v1.2/build-provenance
[D05]: https://github.com/in-toto/attestation/blob/50bf01716982189898823e90586075f37cd9bb7d/spec/v1/statement.md
[D06]: https://theupdateframework.github.io/specification/v1.0.36/
[D07]: https://www.rfc-editor.org/rfc/rfc8785.html
[P01]: https://www.anthropic.com/research/multi-agent-research-system
[P02]: https://arxiv.org/abs/2503.13657v3
