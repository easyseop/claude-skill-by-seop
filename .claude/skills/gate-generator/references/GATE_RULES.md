# Gate 공통 규칙

이 파일은 봉인된 Gate 조사 catalog에서 생성된다.

## GATE-01 — 단계별 작은 Gate로 분해

- **적용 조건:** 둘 이상의 수명주기 경계 또는 서로 다른 실패 효과가 있을 때.
- **행동:** Intake·Design·Pre-execution·Runtime·Post-execution·Release·Long-running Gate를 분리하고 공통 contract로 조합한다.
- **검증:** 각 Gate가 하나의 주 enforcement point·owner·failure effect를 가지는지 검사한다.
- **실패 시:** 여러 경계를 한 boolean으로 합치면 분해 후 재작성한다.
- **강제 계층:** Contract compiler + stage runner.
- **근거:** [S10][S36][S47].
- **예시:** 입력 schema와 Release provenance를 서로 다른 Gate로 둔다.
- **반례:** `check-all.sh` 하나가 모든 실패를 exit 1로만 반환한다.

## GATE-02 — 상위 계약을 source of truth로 고정

- **적용 조건:** Gate를 Planner 결과에서 파생할 때.
- **행동:** `CAPABILITY_PLAN.yaml` digest와 schema version을 `GATE_CONTRACT.yaml`에 binding하고 파생 파일은 역편집하지 않는다.
- **검증:** 모든 gate requirement가 upstream path/CAP/acceptance id에 추적되는지 검사한다.
- **실패 시:** binding 부재나 역방향 불일치는 STALE/BLOCK한다.
- **강제 계층:** Contract validator + CI.
- **근거:** [S01][S02].
- **예시:** GATE-DELETE-01이 side_effect 항목과 AC-07을 참조한다.
- **반례:** Gate 문서에만 승인 필요라고 추가하고 Planner에는 반영하지 않는다.

## GATE-03 — 판정 상태를 분리

- **적용 조건:** Gate 결과를 저장·집계할 때.
- **행동:** PASS/BLOCK/FAIL/ERROR/STALE/WAIVED/NOT_APPLICABLE/OUTCOME_UNKNOWN을 구분한다.
- **검증:** enum, 허용 전이, 집계 우선순위를 검사한다.
- **실패 시:** unknown 문자열 또는 ERROR→PASS 변환은 차단한다.
- **강제 계층:** Result schema + aggregator.
- **근거:** [S36][S38].
- **예시:** 정책 엔진 장애는 GATE_ERROR로 남긴다.
- **반례:** 모든 문제를 FAIL로 뭉개고 자동 retry한다.

## GATE-04 — 하드 안전 Gate를 점수보다 우선

- **적용 조건:** 비가역·민감·권한·Release 조건이 있을 때.
- **행동:** 평균 품질 점수와 무관하게 필요한 approval/IAM/sandbox/ACL/attestation을 강제한다.
- **검증:** risk→mandatory gate mapping이 존재하고 제거되지 않았는지 검사한다.
- **실패 시:** 필수 hard gate 누락은 즉시 BLOCK한다.
- **강제 계층:** Planner/Gate checker + runtime.
- **근거:** [S01][S02][S64][S66].
- **예시:** 답변 품질 99점이어도 송금 승인이 없으면 차단한다.
- **반례:** 여러 soft metric 평균이 높아 권한 누락을 통과시킨다.

## GATE-05 — Deny-by-default

- **적용 조건:** 허용 범위를 명시적으로 열거할 수 있는 실행.
- **행동:** resource/action/path/tool/network는 명시적 allow만 허용하고 미지정은 deny한다.
- **검증:** wildcard·empty ACL·fallback allow를 mutation test한다.
- **실패 시:** 미분류 요청은 BLOCK 또는 read-only degraded로만 전환한다.
- **강제 계층:** Permission/IAM/policy/sandbox.
- **근거:** [S03][S27][S64].
- **예시:** 허용 DB schema 두 개만 role에 부여한다.
- **반례:** 규칙에 없는 tool은 모델 판단으로 실행한다.

## GATE-06 — Planner 아키텍처를 조용히 바꾸지 않음

- **적용 조건:** Gate 설계 중 상위 구성 오류를 발견할 때.
- **행동:** `PLANNER_REENTRY_REQUIRED`와 영향 capability를 기록하고 해당 downstream만 blocked한다.
- **검증:** Gate가 새 Agent/RAG/Tool을 몰래 추가하지 않았는지 diff 검사한다.
- **실패 시:** 아키텍처 변경이 필요하면 Planner를 supersede하고 재승인한다.
- **강제 계층:** Gate generator + independent audit.
- **근거:** [S01][S02].
- **예시:** 실제 write endpoint 발견 시 Planner의 external_effect를 재평가 요청한다.
- **반례:** Gate YAML에 새 멀티에이전트를 추가해 문제를 덮는다.

## GATE-07 — 생성자와 승인자를 분리

- **적용 조건:** Gate 생성·검사·Release 승인.
- **행동:** Generator, deterministic checker, blind-first auditor, human/release approver의 identity·권한을 분리한다.
- **검증:** self-review·동일 credential·동일 write 권한 여부를 검사한다.
- **실패 시:** 독립성 미충족 시 audit/approval을 무효화한다.
- **강제 계층:** IAM + CI environment + audit process.
- **근거:** [S02][S44].
- **예시:** Gate 작성자는 결과를 만들지만 prod Release reviewer가 될 수 없다.
- **반례:** Generator가 자기 JSON에 `approved:true`를 기록한다.

## GATE-08 — 자유문자 PASS 금지

- **적용 조건:** Gate 결과가 downstream을 해제할 때.
- **행동:** 구조화 result와 subject/policy/checker digest·evidence·issuer를 요구한다.
- **검증:** PASS 문자열만 있거나 필수 binding이 비면 실패한다.
- **실패 시:** 결과를 ERROR/BLOCK하고 재실행한다.
- **강제 계층:** Result validator + attestation verifier.
- **근거:** [S38][S39][S40][S41].
- **예시:** 서명된 test-result predicate가 artifact digest를 가리킨다.
- **반례:** README에 '모든 테스트 PASS'를 써서 Release한다.

## GATE-09 — Acceptance criterion 양방향 추적

- **적용 조건:** 합격 기준이 존재할 때.
- **행동:** 각 AC가 하나 이상의 Gate/Eval에, 각 blocking Gate가 하나 이상의 requirement/risk에 연결되게 한다.
- **검증:** uncovered AC와 orphan Gate를 모두 탐지한다.
- **실패 시:** coverage가 닫히기 전 Design/Release를 막는다.
- **강제 계층:** Contract checker + CI.
- **근거:** [S01][S69].
- **예시:** AC-03→GATE-OUT-02→test_output_schema→evidence URI.
- **반례:** 테스트는 많지만 어떤 요구를 검증하는지 모른다.

## GATE-10 — 닫힌 입력 스키마

- **적용 조건:** machine-consumed input 또는 tool args.
- **행동:** required/type/enum/range/unknown-field/duplicate-key 규칙을 명시하고 가능한 경우 closed object로 검증한다.
- **검증:** schema validator와 property-based boundary test를 실행한다.
- **실패 시:** 위반은 실행 전 BLOCK하고 field path를 반환한다.
- **강제 계층:** Validator.
- **근거:** [S27][S34][S51].
- **예시:** 예상하지 않은 `admin:true` 필드를 거부한다.
- **반례:** 알 수 없는 필드를 조용히 downstream API에 전달한다.

## GATE-11 — 입력 trust·data classification

- **적용 조건:** user/LLM/retrieved/tool input이 섞일 때.
- **행동:** 각 입력 source와 trust, sensitivity, tenant, retention을 라벨링한다.
- **검증:** unclassified input이 privileged sink로 흐르는지 검사한다.
- **실패 시:** 미분류 민감 입력은 BLOCK 또는 격리한다.
- **강제 계층:** Intake validator + data policy.
- **근거:** [S64][S65].
- **예시:** retrieved 문서는 `untrusted_data`로 실행 경로와 분리한다.
- **반례:** 공식 URL에서 왔다는 이유로 명령으로 실행한다.

## GATE-12 — 보수적 safe default

- **적용 조건:** 사용자 정책은 없지만 안전한 축소가 가능한 경우.
- **행동:** write→read-only/dry-run, broad→narrow, auto→explicit, secret→out-of-band를 적용하고 assumption을 기록한다.
- **검증:** default가 권한·부작용을 확대하지 않는지 검사한다.
- **실패 시:** 축소로 요구를 충족 못하면 BLOCK하고 결정 요청한다.
- **강제 계층:** Planner/Gate policy.
- **근거:** [S02][S64].
- **예시:** 승인자 미정이면 삭제 계획까지만 생성한다.
- **반례:** 모델이 적당한 승인자를 추측한다.

## GATE-13 — 경로·변경 범위 canonicalization

- **적용 조건:** 파일/URL/resource path를 검사할 때.
- **행동:** 실제 resolver로 canonical identity를 구한 뒤 allow/deny scope를 적용한다.
- **검증:** traversal, symlink, case, redirect, alternate encoding을 시험한다.
- **실패 시:** canonical scope 밖이면 BLOCK한다.
- **강제 계층:** PreToolUse + filesystem/network policy.
- **근거:** [S04][S05][S64].
- **예시:** repo root 밖 symlink를 따라가는 write를 거부한다.
- **반례:** `startswith('/repo')` 문자열 검사만 한다.

## GATE-14 — 입력 크기·자원 경계

- **적용 조건:** 압축·파일·긴 prompt·대규모 tool output.
- **행동:** bytes/items/depth/decompression/output/time limits를 정책화한다.
- **검증:** boundary·zip bomb·deep nesting·large array를 시험한다.
- **실패 시:** 한도 초과는 streaming/sampling 또는 BLOCK으로 처리한다.
- **강제 계층:** Intake/runtime/sandbox.
- **근거:** [S05][S34].
- **예시:** 최대 artifact 크기를 초과하면 chunk 처리 계획을 요구한다.
- **반례:** 파서가 메모리를 모두 쓸 때까지 읽는다.

## GATE-15 — 금지 행동을 먼저 검사

- **적용 조건:** prohibited_actions가 있을 때.
- **행동:** 허용 검사보다 먼저 명시적 금지 action/resource/pattern을 평가한다.
- **검증:** deny precedence와 우회 표현을 mutation test한다.
- **실패 시:** 금지 매치면 approval로도 자동 해제하지 않고 break-glass 정책으로만 처리한다.
- **강제 계층:** Permission/policy/hook.
- **근거:** [S03][S64].
- **예시:** prod 고객 테이블 DROP은 일반 승인으로도 불가하다.
- **반례:** allow rule이 더 먼저 매치되어 금지 동작을 허용한다.

## GATE-16 — Prompt·Skill을 하드 통제로 인정하지 않음

- **적용 조건:** 위반 시 실제 피해가 가능한 규칙.
- **행동:** Prompt는 보조 guidance로만 표시하고 enforcement_point를 별도로 요구한다.
- **검증:** hard requirement가 prompt_only에 매핑됐는지 검사한다.
- **실패 시:** hard layer가 없으면 high-risk capability를 BLOCK한다.
- **강제 계층:** Contract checker.
- **근거:** [S03][S04][S13][S64].
- **예시:** '비밀을 출력하지 마'와 별개로 secret scanner/egress policy를 둔다.
- **반례:** SKILL.md 문장 하나로 운영 삭제를 통제했다고 선언한다.

## GATE-17 — Structured output 뒤 결정적 검증

- **적용 조건:** LLM이 YAML/JSON/명령 계획을 생성할 때.
- **행동:** parse 성공 외에 schema·cross-field·reference·policy invariant를 검사한다.
- **검증:** malformed/semantically invalid/extra field를 시험한다.
- **실패 시:** 검증 실패 시 수정 루프, 반복 초과 시 FAIL한다.
- **강제 계층:** Validator + bounded revise loop.
- **근거:** [S13][S34].
- **예시:** 승인 gate id가 실제 gate catalog에 있는지 검사한다.
- **반례:** JSON 모양만 맞으면 승인한다.

## GATE-18 — 부작용 전 Hook 배치

- **적용 조건:** 도구·명령·파일 변경을 runtime에서 가로챌 수 있을 때.
- **행동:** Pre-action event에서 args·identity·policy·approval을 검사하고 실행 전에 deny한다.
- **검증:** post-only path와 direct bypass를 탐지한다.
- **실패 시:** pre-hook 미설치면 해당 high-risk path를 BLOCK한다.
- **강제 계층:** Hook/runtime adapter.
- **근거:** [S03][S04].
- **예시:** PreToolUse가 삭제 args를 검증한다.
- **반례:** PostToolUse에서 삭제 후 경고만 남긴다.

## GATE-19 — Hook 실패 의미를 명시

- **적용 조건:** Hook/remote policy handler를 배치할 때.
- **행동:** timeout/crash/malformed/exit code/transport error별 fail policy를 계약화한다.
- **검증:** 각 실패 모드를 fault injection한다.
- **실패 시:** 정책과 다른 fallback이면 Release를 막는다.
- **강제 계층:** Hook adapter + chaos test.
- **근거:** [S04][S48][S73].
- **예시:** prod write Hook timeout은 deny로 처리한다.
- **반례:** Hook이 오류나면 자동 allow되지만 문서에 기록하지 않는다.

## GATE-20 — Resource 가까운 곳에서 authorization

- **적용 조건:** DB/API/cloud/resource access.
- **행동:** 최종 시스템 IAM/RBAC/row policy에서 principal-action-resource를 검사한다.
- **검증:** tool visibility·prompt·UI 숨김을 제거해도 접근이 차단되는지 시험한다.
- **실패 시:** resource auth가 없으면 민감 capability를 BLOCK한다.
- **강제 계층:** IAM/DB/API.
- **근거:** [S20][S28][S57].
- **예시:** DB row policy가 tenant를 강제한다.
- **반례:** 애플리케이션이 WHERE tenant를 넣을 것이라 믿는다.

## GATE-21 — Sandbox로 비신뢰 실행 격리

- **적용 조건:** 코드/shell/browser/parser 실행.
- **행동:** ephemeral filesystem, network, process, secret, resource boundaries를 최소화한다.
- **검증:** escape/host socket/metadata/unsandboxed fallback을 시험한다.
- **실패 시:** profile 적용 실패 시 high-risk 실행을 막는다.
- **강제 계층:** Sandbox + OS/container policy.
- **근거:** [S05][S06][S20].
- **예시:** read-only source mount와 egress allowlist를 사용한다.
- **반례:** 컨테이너라는 이유만으로 host socket을 노출한다.

## GATE-22 — 비밀의 LLM 문맥 통과 금지

- **적용 조건:** credential이 필요한 capability.
- **행동:** secret store/env broker/out-of-band flow만 사용하고 모델에는 opaque handle·상태만 준다.
- **검증:** prompt/trace/log/tool result/artifact의 secret pattern과 실제 flow를 검사한다.
- **실패 시:** 안전한 경로가 없으면 capability를 BLOCK한다.
- **강제 계층:** Secret broker + redaction + egress.
- **근거:** [S06][S28][S30][S71].
- **예시:** OAuth는 공식 브라우저 flow로 완료하고 token은 broker에 보관한다.
- **반례:** 사용자에게 채팅에 API key를 붙여 넣게 한다.

## GATE-23 — 보호된 CI가 Release를 소유

- **적용 조건:** merge/deploy/publish.
- **행동:** required checks, trusted issuer, protected branch/environment, immutable artifact를 강제한다.
- **검증:** direct push/deploy/admin bypass/skipped job을 시험한다.
- **실패 시:** 보호 경로 밖 Release는 BLOCK한다.
- **강제 계층:** CI/environment/IAM.
- **근거:** [S43][S44][S45].
- **예시:** prod credential은 승인된 environment job만 받는다.
- **반례:** 로컬 스크립트로 동일 credential을 사용해 직접 배포한다.

## GATE-24 — 정책 엔진 decision을 실행과 결박

- **적용 조건:** 중앙 policy engine 사용.
- **행동:** decision id·policy digest·input digest를 runtime call evidence에 연결한다.
- **검증:** stale bundle·missing log·decision reuse를 시험한다.
- **실패 시:** binding 불명확하면 high-risk call을 막는다.
- **강제 계층:** Policy engine + runtime adapter.
- **근거:** [S35][S36][S37].
- **예시:** OPA decision id가 같은 tool_call_id에 기록된다.
- **반례:** 정책이 PASS했다는 로그만 있고 어떤 입력인지 모른다.

## GATE-25 — 승인을 exact payload에 결박

- **적용 조건:** 승인 필요한 행동.
- **행동:** canonical payload/action/resource/version/policy digest를 승인 요청·결정에 포함한다.
- **검증:** 한 필드씩 mutation해 기존 승인이 거부되는지 확인한다.
- **실패 시:** 불일치면 재승인 전까지 BLOCK한다.
- **강제 계층:** Approval service + pre-execution verifier.
- **근거:** [S14][S51][S52][S53].
- **예시:** 수신자 목록과 첨부 digest가 승인에 포함된다.
- **반례:** '메일 보내도 됨'을 이후 모든 메일에 사용한다.

## GATE-26 — Canonicalization을 명시

- **적용 조건:** 구조화 payload를 hash/sign할 때.
- **행동:** 검증된 canonicalization 규격과 encoding을 선택하고 duplicate/invalid numeric/unicode를 거부한다.
- **검증:** 동일 의미의 직렬화와 edge case test vector를 비교한다.
- **실패 시:** canonicalization 오류는 승인/attestation 생성 중단이다.
- **강제 계층:** Canonicalizer + signature service.
- **근거:** [S51].
- **예시:** RFC8785 JCS bytes를 SHA-256한다.
- **반례:** 언어별 기본 dict 출력 문자열을 hash한다.

## GATE-27 — 승인자 identity·권한 검증

- **적용 조건:** approval decision 수신.
- **행동:** 강한 인증 identity와 해당 action/scope의 approver role을 확인한다.
- **검증:** 위조 subject·role 변경·약한 session·cross-tenant approver를 시험한다.
- **실패 시:** 불충족 decision은 무효다.
- **강제 계층:** IdP/IAM/approval service.
- **근거:** [S14][S44].
- **예시:** data owner만 해당 dataset 삭제를 승인한다.
- **반례:** 로그인한 사용자라면 누구나 prod 배포 승인 가능하다.

## GATE-28 — 승인 scope·만료 제한

- **적용 조건:** 일회성 또는 시간 민감 승인.
- **행동:** resource/action/limits/tenant/time window를 최소화하고 expiry를 필수로 둔다.
- **검증:** 범위 확대·만료·clock skew를 시험한다.
- **실패 시:** 초과 요청은 새 승인으로 보낸다.
- **강제 계층:** Approval service + runtime.
- **근거:** [S14][S52].
- **예시:** 10분 내 특정 100건까지만 허용한다.
- **반례:** 프로젝트 전체 write를 무기한 승인한다.

## GATE-29 — 대상 변경 시 재승인

- **적용 조건:** 승인 후 실행 전 시간이 흐르거나 artifact/state가 바뀔 때.
- **행동:** payload/resource/policy/tool/phase hash를 다시 계산한다.
- **검증:** 승인 뒤 row set·금액·commit·tool version을 변경한다.
- **실패 시:** 하나라도 바뀌면 STALE 후 재승인한다.
- **강제 계층:** Pre-execution gate.
- **근거:** [S14][S21][S50].
- **예시:** ETag가 달라지면 삭제 승인 무효다.
- **반례:** 같은 자연어 목표라며 다른 대상에 사용한다.

## GATE-30 — 거부·취소를 최종 상태로 기록

- **적용 조건:** approval 거부/취소.
- **행동:** decision을 append-only로 기록하고 token 발급·pending task를 중단한다.
- **검증:** late resume·cached approve·cancel race를 시험한다.
- **실패 시:** 새 payload는 새 request id로만 재요청한다.
- **강제 계층:** Approval store + workflow.
- **근거:** [S14][S21].
- **예시:** 취소된 run의 background write가 fencing token에서 거부된다.
- **반례:** 같은 request id를 approve로 덮어쓴다.

## GATE-31 — 부분·Batch 승인을 기계 표현

- **적용 조건:** batch/부분 승인.
- **행동:** item set/root, count, total, limits를 canonical binding으로 표현한다.
- **검증:** item 추가/제거/재정렬/total mismatch를 시험한다.
- **실패 시:** 승인 집합 밖 item은 BLOCK한다.
- **강제 계층:** Approval schema + batch runner.
- **근거:** [S51][S52].
- **예시:** 승인된 100개 item digest 중 87개만 실행한다.
- **반례:** '비슷한 항목들'이라는 메모로 batch를 허용한다.

## GATE-32 — 2인 승인과 역할 분리

- **적용 조건:** critical·규제·대규모 효과.
- **행동:** distinct principal/quorum/role separation과 동일 payload binding을 요구한다.
- **검증:** 동일 계정·동일 role 불허·한 명 만료를 시험한다.
- **실패 시:** quorum 미충족은 BLOCK한다.
- **강제 계층:** Approval IAM + CI environment.
- **근거:** [S44].
- **예시:** 서비스 소유자와 데이터 소유자가 각각 승인한다.
- **반례:** 한 사용자가 두 번 클릭해 2인 승인으로 센다.

## GATE-33 — 승인 후 JIT 권한·즉시 회수

- **적용 조건:** 승인이 temporary elevation을 필요로 할 때.
- **행동:** one-shot 또는 짧은 TTL credential을 exact scope로 발급하고 finally/reconciliation 후 회수한다.
- **검증:** timeout/crash/cancel 뒤 credential 유효성을 시험한다.
- **실패 시:** 회수 실패는 incident와 추가 write BLOCK이다.
- **강제 계층:** Privilege broker + IAM.
- **근거:** [S46][S64].
- **예시:** prod deploy role을 job 동안만 발급한다.
- **반례:** 승인 후 장기 admin token을 agent memory에 저장한다.

## GATE-34 — 승인 replay·위조 방지

- **적용 조건:** approval token 소비.
- **행동:** nonce, issued/expires, signature, atomic single-use consume, revocation을 검사한다.
- **검증:** 재전송·동시 소비·서명 component 누락을 시험한다.
- **실패 시:** 중복/위조는 BLOCK하고 보안 이벤트로 기록한다.
- **강제 계층:** Approval verifier + secure store.
- **근거:** [S41][S52].
- **예시:** consumed nonce는 다시 허용되지 않는다.
- **반례:** 승인 JSON 복사본을 여러 run에서 재사용한다.

## GATE-35 — Read/write Tool 분리

- **적용 조건:** 외부 resource tool 설계.
- **행동:** read/plan과 write/execute tool·permission·approval path를 분리한다.
- **검증:** read tool로 write 가능한 hidden arg/endpoint를 시험한다.
- **실패 시:** 혼합 tool은 재설계하거나 항상 write 등급으로 취급한다.
- **강제 계층:** Tool/API design + IAM.
- **근거:** [S01][S27].
- **예시:** `preview_delete`와 `execute_delete`를 별도 tool로 둔다.
- **반례:** `mode=read|write` 하나로 권한을 공유한다.

## GATE-36 — Tool 입력·출력 schema 검증

- **적용 조건:** Tool/MCP/API 호출.
- **행동:** 입력과 가능한 경우 출력을 strict schema로 검증하고 version을 고정한다.
- **검증:** unknown field, wrong type, malformed definition/result를 시험한다.
- **실패 시:** 입력은 실행 전 차단, 출력은 downstream 전달 전 차단한다.
- **강제 계층:** Tool adapter validator.
- **근거:** [S27][S34].
- **예시:** outputSchema와 실제 result를 비교한다.
- **반례:** 모델이 이해할 수 있다는 이유로 자유형 문자열을 전달한다.

## GATE-37 — 주입 안전 Adapter

- **적용 조건:** shell/SQL/path/URL에 LLM·사용자 문자열을 넣을 때.
- **행동:** typed argument, parameter binding, identifier allowlist, URL parser를 사용한다.
- **검증:** metacharacter·comment·encoding·redirect·path traversal corpus를 시험한다.
- **실패 시:** 안전 adapter가 없으면 실행을 BLOCK한다.
- **강제 계층:** Execution code + validator.
- **근거:** [S64][S65].
- **예시:** SQL 값은 bind variable, table은 allowlist다.
- **반례:** `sh -c 'cmd '+user_input`을 사용한다.

## GATE-38 — Tool namespace·version·server identity

- **적용 조건:** 여러 server/유사 tool.
- **행동:** qualified identity와 trusted server registry를 사용한다.
- **검증:** 동명 tool, Unicode confusable, server 교체, version drift를 시험한다.
- **실패 시:** 모호성은 수정 또는 BLOCK한다.
- **강제 계층:** Tool registry + selector.
- **근거:** [S11][S27].
- **예시:** `finance.prod/refund@2`로 결박한다.
- **반례:** `refund`라는 이름만 승인한다.

## GATE-39 — Tool 필요성·선택을 별도 평가

- **적용 조건:** Agent/tool routing.
- **행동:** tool_needed/right_tool/args/authority/effect/recovery를 분리 측정한다.
- **검증:** near-miss와 no-tool case를 포함한다.
- **실패 시:** 반복 선택 오류면 설명·통합·workflow 전환을 요구한다.
- **강제 계층:** Eval harness.
- **근거:** [S11][S12].
- **예시:** 재고 조회에는 live tool, 정적 정책에는 reference를 기대한다.
- **반례:** 최종 답만 맞으면 잘못된 privileged tool 호출을 무시한다.

## GATE-40 — Timeout·rate·cost를 명시

- **적용 조건:** 원격 tool/agent/long task.
- **행동:** per-call deadline, cancellation, retry-after, total budget을 계약화한다.
- **검증:** hang/slow response/rate burst/cancel ignored를 시험한다.
- **실패 시:** 한도 도달 시 terminal reason과 partial state를 남긴다.
- **강제 계층:** Runtime + client adapter.
- **근거:** [S18][S21][S23].
- **예시:** tool timeout과 전체 run deadline을 각각 둔다.
- **반례:** 완료될 때까지 무한 대기한다.

## GATE-41 — 오류 유형을 기계 분류

- **적용 조건:** Tool/API 오류 처리.
- **행동:** retryable/non-retryable/conflict/outcome_unknown/gate_error를 stable code와 effect_state로 반환한다.
- **검증:** 동일 HTTP status의 다른 의미를 fixture로 시험한다.
- **실패 시:** 분류 불가 write 오류는 OUTCOME_UNKNOWN으로 처리한다.
- **강제 계층:** Tool adapter + workflow.
- **근거:** [S23][S50][S54].
- **예시:** 429는 retry-after, 409는 refetch/replan으로 분리한다.
- **반례:** 모든 예외를 세 번 재시도한다.

## GATE-42 — Idempotency key와 payload digest 결박

- **적용 조건:** 재시도 가능한 write.
- **행동:** stable key scope와 canonical payload digest·result ledger를 유지한다.
- **검증:** 같은 key/다른 payload, cross-tenant, retention expiry를 시험한다.
- **실패 시:** 불일치는 BLOCK하고 새 operation으로 처리한다.
- **강제 계층:** API/workflow ledger.
- **근거:** [S50][S54][S56].
- **예시:** 응답 유실 시 같은 key·같은 payload로 조회한다.
- **반례:** 매 retry마다 새 key를 생성한다.

## GATE-43 — 불명확 결과는 재대조

- **적용 조건:** request가 commit됐을 수 있는 timeout/crash.
- **행동:** OUTCOME_UNKNOWN으로 표시하고 external operation/state를 조회한다.
- **검증:** commit 후 response loss를 fault injection한다.
- **실패 시:** 새 side effect는 reconciliation 전 차단한다.
- **강제 계층:** Workflow + reconciliation.
- **근거:** [S50][S54][S56].
- **예시:** 결제 operation id로 상태를 먼저 조회한다.
- **반례:** timeout을 실패로 가정해 새 결제를 만든다.

## GATE-44 — Mock·record/replay의 계약 동등성

- **적용 조건:** live tool 평가·회귀.
- **행동:** fixture와 live schema/effect semantics를 contract test하고 write replay를 비활성화한다.
- **검증:** schema drift·nondeterminism·secret leakage를 시험한다.
- **실패 시:** 불일치 fixture는 STALE 처리한다.
- **강제 계층:** Test harness + Pact.
- **근거:** [S12][S69].
- **예시:** provider verification으로 fixture를 갱신한다.
- **반례:** 오래된 mock PASS로 production API를 승인한다.

## GATE-45 — Handoff에서 재권한검사

- **적용 조건:** agent→agent/tool handoff.
- **행동:** target, payload, original user/tenant, permission ceiling, approval binding을 다시 검사한다.
- **검증:** handoff metadata 위조와 guardrail 미적용 경로를 시험한다.
- **실패 시:** 검사 실패 시 handoff를 중단한다.
- **강제 계층:** Handoff runtime + policy.
- **근거:** [S13][S15].
- **예시:** refund agent 진입 첫 단계에서 금액·고객 권한을 확인한다.
- **반례:** 첫 agent가 검증했으므로 후속 agent는 그대로 신뢰한다.

## GATE-46 — 사용자·테넌트 identity end-to-end binding

- **적용 조건:** multi-user·multi-tenant 실행.
- **행동:** authenticated subject를 run/state/tool/query/cache/evidence에 전파하고 각 경계에서 검증한다.
- **검증:** prompt tenant spoof, thread reuse, cache cross-hit를 시험한다.
- **실패 시:** identity mismatch는 즉시 BLOCK한다.
- **강제 계층:** IAM + state + tool/RAG adapter.
- **근거:** [S27][S57][S59].
- **예시:** query filter는 session identity에서 생성된다.
- **반례:** 사용자가 말한 tenant 이름을 그대로 WHERE에 쓴다.

## GATE-47 — Agent 총예산 강제

- **적용 조건:** bounded_agent|multi_agent.
- **행동:** turn/tool/time/token/cost/parallel branch 상한을 runtime counter로 강제한다.
- **검증:** 도구 오류·handoff loop·parallel burst를 시험한다.
- **실패 시:** 상한 도달 시 checkpoint/compensate/escalate하며 PASS하지 않는다.
- **강제 계층:** Agent runtime.
- **근거:** [S01][S17][S18].
- **예시:** 총 20 calls 안에 완료하지 못하면 partial+escalate한다.
- **반례:** 각 subagent만 한도가 있고 전체 한도는 없다.

## GATE-48 — 구조화 종료 조건

- **적용 조건:** Agent/Workflow completion.
- **행동:** acceptance-linked completion/safe-stop/failure/escalation/cancel predicate를 정의한다.
- **검증:** 최종 텍스트는 있지만 pending action이 남은 경우를 시험한다.
- **실패 시:** terminal predicate 미충족이면 완료를 거부한다.
- **강제 계층:** State machine + completion gate.
- **근거:** [S21][S23][S24].
- **예시:** 모든 required output과 reconciliation이 완료돼야 terminal이다.
- **반례:** 모델이 '완료했습니다'라고 말하면 끝낸다.

## GATE-49 — Loop signature와 진행도 검사

- **적용 조건:** 동적 routing·retry·handoff.
- **행동:** state/action/args/error digest 반복과 progress 무변화를 탐지한다.
- **검증:** self-loop, two-agent cycle, same failing call을 시험한다.
- **실패 시:** 수정 retry 한도 후 중단·human escalation한다.
- **강제 계층:** Runtime monitor.
- **근거:** [S18][S24].
- **예시:** 동일 tool args가 3회 반복되면 escalation한다(횟수는 정책값).
- **반례:** turn 수가 남아 있다는 이유로 같은 행동을 계속한다.

## GATE-50 — 허용 상태 전이만 실행

- **적용 조건:** 명시적 workflow/state machine.
- **행동:** transition table과 pre/post condition을 code로 평가한다.
- **검증:** illegal jump, duplicate terminal, rollback skip를 mutation한다.
- **실패 시:** 불법 전이는 BLOCK하고 state를 보존한다.
- **강제 계층:** Workflow runtime.
- **근거:** [S22][S23][S24].
- **예시:** APPROVED 전에는 EXECUTING으로 갈 수 없다.
- **반례:** 상태 문자열을 LLM이 자유롭게 바꾼다.

## GATE-51 — Checkpoint freshness·소유자 검증

- **적용 조건:** pause/resume/time travel.
- **행동:** checkpoint digest/version/owner/tenant/policy/approval/resource version을 확인한다.
- **검증:** stale thread, cross-user, policy update, approval expiry를 시험한다.
- **실패 시:** repair/migrate/new run 전까지 resume를 막는다.
- **강제 계층:** Checkpoint loader + preflight.
- **근거:** [S21][S22][S75].
- **예시:** 새 thread로 깨끗한 상태를 시작하거나 명시적 migration한다.
- **반례:** thread_id만 같으면 무조건 이어서 실행한다.

## GATE-52 — Tool call/result transcript 불변식

- **적용 조건:** Tool-using model transcript.
- **행동:** call id·tool identity·result cardinality·ordering·pending set을 검사한다.
- **검증:** missing/duplicate/cross-thread/out-of-order result를 시험한다.
- **실패 시:** 불완전 transcript는 모델 API로 보내지 않는다.
- **강제 계층:** Transcript validator + checkpoint.
- **근거:** [S21][S75].
- **예시:** 각 tool_use 직후 대응 tool_result가 하나 존재한다.
- **반례:** 누락 result 뒤에 새 user message를 계속 쌓는다.

## GATE-53 — 병렬 입력 freeze와 deterministic merge

- **적용 조건:** 독립 branch/worker.
- **행동:** branch base digest를 고정하고 immutable output을 deterministic reducer로 병합한다.
- **검증:** shared file race, branch stale base, non-associative merge를 시험한다.
- **실패 시:** conflict는 자동 덮어쓰기 대신 replan/manual merge한다.
- **강제 계층:** Workflow orchestrator + artifact store.
- **근거:** [S24].
- **예시:** branch별 파일을 만들고 정렬된 manifest로 병합한다.
- **반례:** 여러 agent가 같은 Markdown을 동시에 append한다.

## GATE-54 — Phase boundary hash

- **적용 조건:** 설계→구현→검증→Release 인계.
- **행동:** upstream/policy/implementation/output/gate digests를 phase manifest에 고정한다.
- **검증:** 한 파일 변경 후 기존 downstream PASS가 STALE인지 검사한다.
- **실패 시:** binding 불일치면 관련 phase부터 재실행한다.
- **강제 계층:** State/CI/attestation.
- **근거:** [S01][S38][S39].
- **예시:** DESIGN digest 변경 시 구현 검사 결과가 자동 stale된다.
- **반례:** 수정시간만 보고 같은 파일이라고 판단한다.

## GATE-55 — 부분 완료를 구조화

- **적용 조건:** batch/multi-step 일부 성공.
- **행동:** completed/failed/unknown/compensated/pending을 item별로 기록한다.
- **검증:** partial batch와 mixed effect를 시험한다.
- **실패 시:** unknown이나 failed item이 있으면 전체 PASS를 금지한다.
- **강제 계층:** Workflow result schema.
- **근거:** [S23][S54].
- **예시:** 97/100 성공을 `partial`로 반환한다.
- **반례:** 성공률이 높다는 이유로 전체 완료 처리한다.

## GATE-56 — 보상 계획 선등록

- **적용 조건:** 되돌릴 수 있는 side effect chain.
- **행동:** forward action 전 compensation handler·dependency·idempotency를 등록한다.
- **검증:** forward committed 후 crash, compensation duplicate/failure를 시험한다.
- **실패 시:** 보상 불가 위험은 approval에 표시하고 failure 시 human repair한다.
- **강제 계층:** Workflow saga + ledger.
- **근거:** [S23][S55][S56].
- **예시:** 예약 생성 전에 취소 operation 정보를 ledger에 둔다.
- **반례:** 실패 후 모델이 즉석에서 롤백 방법을 생각한다.

## GATE-57 — Human escalation을 terminal 경로로 설계

- **적용 조건:** 정책 미결정·unknown outcome·반복 실패.
- **행동:** owner, 필요한 evidence, 재개 조건, timeout을 명시한다.
- **검증:** escalation 후 agent가 계속 실행하는 race를 시험한다.
- **실패 시:** run을 PAUSED/BLOCKED로 고정한다.
- **강제 계층:** Workflow + notification.
- **근거:** [S14][S21].
- **예시:** unknown 결제 상태를 운영자 queue로 넘기고 write를 멈춘다.
- **반례:** 사람에게 메시지만 보내고 agent는 계속 재시도한다.

## GATE-58 — Clean-room replay

- **적용 조건:** 상태 오염·비결정성·감사 재현.
- **행동:** 새 state와 pinned versions, mock/read-only effect로 재실행한다.
- **검증:** hidden memory/cache/previous PASS를 제거해 결과를 비교한다.
- **실패 시:** 재현 불가면 Release risk로 기록하거나 차단한다.
- **강제 계층:** Eval harness.
- **근거:** [S22][S67].
- **예시:** 새 thread와 fixture로 동일 gate path를 재현한다.
- **반례:** 기존 checkpoint를 그대로 써서 '재현'한다.

## GATE-59 — Background task lease·fencing

- **적용 조건:** 비동기/장기 task.
- **행동:** operation uniqueness, lease expiry, fencing token, cancel/replace, late result version을 강제한다.
- **검증:** 중복 worker, lease 만료 후 late write, approval expiry를 시험한다.
- **실패 시:** 오래된 worker write를 resource layer에서 거부한다.
- **강제 계층:** Task runtime + datastore.
- **근거:** [S23][S33].
- **예시:** generation 8 worker만 현재 상태를 쓸 수 있다.
- **반례:** 취소된 task가 늦게 완료돼 새 결과를 덮는다.

## GATE-60 — RAG source inventory 필수

- **적용 조건:** RAG/knowledge retrieval 선택.
- **행동:** source owner/authority/version/digest/freshness/ACL/delete channel을 등록한다.
- **검증:** metadata 없는 source·orphan index를 검사한다.
- **실패 시:** inventory 없는 corpus는 검색에서 제외한다.
- **강제 계층:** Knowledge contract + ingestion gate.
- **근거:** [S01][S57][S60].
- **예시:** 정책 문서마다 effective date와 source digest를 기록한다.
- **반례:** 벡터 DB에 들어있다는 이유만으로 신뢰한다.

## GATE-61 — Authority·freshness를 분리 판정

- **적용 조건:** 여러 버전/출처가 있을 때.
- **행동:** source authority, source freshness, index freshness를 각각 평가한다.
- **검증:** 오래된 공식 문서와 최신 비공식 문서 충돌을 시험한다.
- **실패 시:** 자동 해소 규칙이 없으면 abstain/escalate한다.
- **강제 계층:** Retrieval gate.
- **근거:** [S57][S60][S61].
- **예시:** 공식 최신 effective 정책을 우선하고 충돌을 기록한다.
- **반례:** 검색 순위가 높은 문서를 정답으로 선택한다.

## GATE-62 — ACL은 retrieval 전에 강제

- **적용 조건:** 문서/row/tenant 권한이 있는 RAG.
- **행동:** authenticated identity 기반 security trimming을 후보 생성 이전 또는 source query에서 적용한다.
- **검증:** filter omission, user-supplied tenant, cache leak를 시험한다.
- **실패 시:** 권한 증명이 없으면 retrieval을 막는다.
- **강제 계층:** Source ACL/query layer.
- **근거:** [S57][S58][S59].
- **예시:** authorized document set 안에서만 vector search한다.
- **반례:** 검색 후 LLM에게 비밀 문서를 언급하지 말라고 한다.

## GATE-63 — 삭제·정정·권한 철회 전파

- **적용 조건:** mutable corpus.
- **행동:** tombstone/watermark/SLA와 stale behavior를 정의한다.
- **검증:** 삭제 직후 query, group revoke, corrected source를 시험한다.
- **실패 시:** SLA 초과 시 affected corpus를 closed/abstain한다.
- **강제 계층:** Ingestion/index monitor.
- **근거:** [S57][S59][S60].
- **예시:** 삭제 watermark보다 오래된 index를 사용하지 않는다.
- **반례:** 주기적 재색인 예정이라는 이유로 계속 응답한다.

## GATE-64 — Chunk/index provenance metadata

- **적용 조건:** RAG index 생성.
- **행동:** source span/digest/version/ACL/parser/chunker/embedder/index metadata를 보존한다.
- **검증:** metadata stripping·wrong parent·hash mismatch를 시험한다.
- **실패 시:** high-risk corpus의 불완전 chunk는 제외한다.
- **강제 계층:** Ingestion validator.
- **근거:** [S60][S61][S63].
- **예시:** citation이 문서 버전과 정확한 section span을 가리킨다.
- **반례:** chunk text만 저장하고 원본 위치를 잃는다.

## GATE-65 — Retrieval과 generation을 별도 평가

- **적용 조건:** RAG 평가.
- **행동:** eligibility/recall/ranking과 faithfulness/citation/abstention을 분리한다.
- **검증:** 정답 생성 but wrong retrieval, good retrieval but hallucination case를 시험한다.
- **실패 시:** 어느 층 실패인지 표시하고 그 층을 수정한다.
- **강제 계층:** RAG eval harness.
- **근거:** [S61][S62][S63].
- **예시:** context precision과 citation support를 따로 측정한다.
- **반례:** 최종 문장 유사도 하나로 RAG를 승인한다.

## GATE-66 — Citation support·completeness 검증

- **적용 조건:** 출처가 필요한 출력.
- **행동:** 주장→source version/span→support relation을 검사한다.
- **검증:** 존재하지 않는 URL, 관련 없는 span, citation 누락을 시험한다.
- **실패 시:** 근거 추가·주장 축소·abstain 후 재검사한다.
- **강제 계층:** Citation checker + human/rubric.
- **근거:** [S63].
- **예시:** 핵심 수치가 해당 표의 정확한 행을 인용한다.
- **반례:** 참고문헌 목록이 있다는 이유로 모든 주장이 지지된다고 본다.

## GATE-67 — 무근거 abstention·출처 충돌

- **적용 조건:** authorized authoritative evidence가 없거나 충돌할 때.
- **행동:** 구조화 insufficiency/conflict 상태와 검색 범위·다음 행동을 반환한다.
- **검증:** empty retrieval, only unauthorized hit, equal-authority conflict를 시험한다.
- **실패 시:** 일반 지식으로 채우지 않고 중단한다.
- **강제 계층:** Generation/output gate.
- **근거:** [S61][S63].
- **예시:** `insufficient_evidence`와 재동기화 요청을 반환한다.
- **반례:** 그럴듯한 답을 생성해 빈 context를 숨긴다.

## GATE-68 — 검색 문서는 데이터로 취급

- **적용 조건:** retrieved content에 명령·tool call 지시가 있을 때.
- **행동:** 문서 명령을 실행 제어로 승격하지 않고 별도 policy/tool Gate를 요구한다.
- **검증:** prompt injection corpus·credential 요구·external URL 지시를 시험한다.
- **실패 시:** 의심 content는 quote/summarize만 하고 privileged action을 막는다.
- **강제 계층:** RAG sanitizer + tool policy.
- **근거:** [S64][S65].
- **예시:** 문서의 '시스템 지시를 무시'를 내용으로 인용만 한다.
- **반례:** 검색 문서가 명령한 shell을 실행한다.

## GATE-69 — High-risk Gate 오류 fail-closed

- **적용 조건:** 권한·비밀·ACL·승인·Release·비가역 write Gate.
- **행동:** ERROR/timeout/unknown을 allow로 바꾸지 않는다.
- **검증:** checker crash·network partition·malformed response를 주입한다.
- **실패 시:** BLOCK/PAUSE하고 read-only diagnosis만 허용한다.
- **강제 계층:** Runtime/policy/CI.
- **근거:** [S36][S47][S49].
- **예시:** 승인 서비스 장애 시 배포를 멈춘다.
- **반례:** 가용성을 위해 임시로 모든 prod write를 허용한다.

## GATE-70 — Gate ERROR와 업무 FAIL 구분

- **적용 조건:** 결과 집계·운영.
- **행동:** checker 정상 판정 여부와 업무 조건 충족 여부를 별도 필드로 기록한다.
- **검증:** checker exception을 업무 위반으로 변환하는 코드를 시험한다.
- **실패 시:** 원인별 복구 경로를 다르게 한다.
- **강제 계층:** Result schema + observability.
- **근거:** [S36][S70].
- **예시:** schema invalid=FAIL, validator unreachable=ERROR.
- **반례:** 둘 다 `false` 하나로 저장한다.

## GATE-71 — Gate 결과를 subject attestation에 결박

- **적용 조건:** 결과가 Release/재사용될 때.
- **행동:** subject/policy/checker/input/test evidence를 서명된 predicate에 포함한다.
- **검증:** artifact swap, untrusted issuer, signature-before-parse 오류를 시험한다.
- **실패 시:** 검증 실패 결과는 소비하지 않는다.
- **강제 계층:** Attestation service + verifier.
- **근거:** [S38][S39][S40][S41][S42].
- **예시:** test-result attestation의 subject digest가 release binary와 같다.
- **반례:** 서명은 맞지만 어떤 artifact를 테스트했는지 없다.

## GATE-72 — Stale PASS 자동 무효화

- **적용 조건:** 의존 artifact/policy/approval/source가 변경될 때.
- **행동:** dependency digest graph로 affected result를 STALE 처리한다.
- **검증:** 각 dependency를 하나씩 변경해 전파를 검사한다.
- **실패 시:** 관련 Gate를 재실행하기 전 Release를 막는다.
- **강제 계층:** State/CI/contract graph.
- **근거:** [S01][S38][S69].
- **예시:** policy v8 배포 시 v7 decision cache를 폐기한다.
- **반례:** 지난주 PASS 보고서를 오늘 commit에 복사한다.

## GATE-73 — Gate mutation과 ablation

- **적용 조건:** Gate 구현·규칙의 신뢰성 평가.
- **행동:** deny/TTL/digest/ACL/required field/check execution을 mutation하고 Gate 제거 ablation을 수행한다.
- **검증:** mutant kill, uncovered/survived, performance impact를 기록한다.
- **실패 시:** critical mutant 생존 시 승인하지 않는다.
- **강제 계층:** Eval/mutation harness.
- **근거:** [S01][S68].
- **예시:** approval expiry를 삭제한 mutant가 replay test에서 적발된다.
- **반례:** happy path만 테스트하고 정책이 실제 작동한다고 단정한다.

## GATE-74 — Waiver는 범위·만료·보상 통제 필수

- **적용 조건:** 일시적 예외를 허용할 때.
- **행동:** exact violation/subject/policy/scope/owner/expiry/compensating control을 기록한다.
- **검증:** 범위 확장·만료·owner 부재·중첩 waiver를 시험한다.
- **실패 시:** 조건 불충족 waiver는 무효이며 PASS로 변환하지 않는다.
- **강제 계층:** Waiver service + Release gate.
- **근거:** [S43][S44].
- **예시:** 특정 commit 한 번에만 유효한 waiver를 둔다.
- **반례:** `ignore=true`를 영구 설정한다.

## GATE-75 — Gate 관측성과 민감정보 redaction

- **적용 조건:** 분산 Gate·감사.
- **행동:** started/decision/error/stale/approval/effect/reconciliation 이벤트와 correlation을 기록하고 secret/PII를 제거한다.
- **검증:** 누락 span, forged context, PII baggage, log truncation을 시험한다.
- **실패 시:** critical evidence 누락은 Release BLOCK 또는 incident다.
- **강제 계층:** Tracing/logging/audit store.
- **근거:** [S17][S36][S70][S71].
- **예시:** tool_call_id와 policy decision id를 같은 trace에 연결한다.
- **반례:** trace header를 authorization token으로 신뢰한다.

## GATE-76 — Gate 가용성과 last-known-good 정책

- **적용 조건:** remote policy/checker 의존.
- **행동:** health, decision SLO, timeout, LKG version/TTL, rollback을 정의한다.
- **검증:** bundle activation 실패·split brain·slow decision을 시험한다.
- **실패 시:** TTL 초과 또는 high-risk는 fail-closed한다.
- **강제 계층:** Policy platform + runtime.
- **근거:** [S36][S37][S48].
- **예시:** 검증된 이전 bundle을 짧은 정책 창에서만 사용한다.
- **반례:** 정책 서버가 느리면 무기한 캐시 PASS를 사용한다.

## GATE-77 — 완료 전 외부 상태 대조

- **적용 조건:** write/deploy/send/migrate.
- **행동:** expected effect와 source-of-truth read-back/ledger를 비교한다.
- **검증:** success response but partial commit/delayed state/duplicate를 시험한다.
- **실패 시:** 불일치는 OUTCOME_UNKNOWN/PARTIAL로 남기고 완료를 차단한다.
- **강제 계층:** Reconciliation gate.
- **근거:** [S47][S50][S54].
- **예시:** 이관 row count/hash와 target 원장을 대조한다.
- **반례:** HTTP 200만 보고 데이터 이관 완료로 선언한다.

## GATE-78 — 유형별 Completion Gate

- **적용 조건:** Agent·Workflow·RAG 결과 완료.
- **행동:** Agent는 pending/trace/budget, Workflow는 state/compensation, RAG는 ACL/freshness/evidence를 각각 검사한다.
- **검증:** 각 유형의 near-miss를 교차 적용한다.
- **실패 시:** 공통 output만 맞아도 유형별 invariant가 없으면 FAIL한다.
- **강제 계층:** Completion aggregator.
- **근거:** [S21][S23][S61].
- **예시:** RAG 답은 citation이 있어도 ACL 누출이면 실패다.
- **반례:** 모든 구성에 동일한 '파일 존재' Gate만 사용한다.

## GATE-79 — 런타임 강제 불가 Capability 차단

- **적용 조건:** 필수 hard enforcement를 설치·검증할 수 없을 때.
- **행동:** 위험 기능을 blocked하고 허용 가능한 read-only/dry-run 범위를 별도 capability로 분리한다.
- **검증:** prompt-only fallback이나 unprotected direct path를 검사한다.
- **실패 시:** 고위험 기능을 생성하더라도 운영 enable을 금지한다.
- **강제 계층:** Planner/Gate status + IAM.
- **근거:** [S01][S02][S64].
- **예시:** sandbox 없는 untrusted code 실행은 설계만 산출한다.
- **반례:** '주의해서 실행' 문구를 넣고 production을 허용한다.

## GATE-80 — 계약↔구현↔테스트↔증거 양방향 추적

- **적용 조건:** Gate 구현 완료·Release.
- **행동:** gate id를 hook/policy/permission/CI/checker/test/evidence에 내장하고 역방향 inventory를 검사한다.
- **검증:** unimplemented gate와 unmodeled runtime control, orphan test/evidence를 탐지한다.
- **실패 시:** 추적이 닫히지 않으면 APPROVED_FOR_IMPLEMENTATION/RELEASE를 막는다.
- **강제 계층:** Traceability checker + CI.
- **근거:** [S01][S38][S69].
- **예시:** runtime policy 파일의 annotation이 GATE-35와 test id를 가진다.
- **반례:** YAML에는 gate가 있지만 실제 Hook은 다른 이름·조건으로 동작한다.
