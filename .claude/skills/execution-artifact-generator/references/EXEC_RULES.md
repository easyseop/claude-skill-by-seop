# Execution 공통 규칙

봉인된 Execution 조사 catalog에서 생성된다.

## EXEC-01

- **조건·행동:** Planner component/control mode를 그대로 copy한다.
- **검증·실패·강제:** mismatch → `PLANNER_REENTRY_REQUIRED`; compiler/checker.
- **예시·반례:** `tool`을 몰래 `workflow`로 추가 / Gate에서 architecture 재설계
- **근거:** [R01][R02]

## EXEC-02

- **조건·행동:** `execution_required`를 code 필요성 전에 판정한다.
- **검증·실패·강제:** Prompt/Skill-only인데 executable 생성 → BLOCK; trace checker.
- **예시·반례:** ADR Skill / 불필요한 Python service
- **근거:** [R01][S02]

## EXEC-03

- **조건·행동:** 기존 Script/CLI/SDK/Tool/MCP/stdlib를 먼저 inventory한다.
- **검증·실패·강제:** candidate/evidence 부재 → new-code justification 불가.
- **예시·반례:** existing `validate.py` reuse / 같은 API용 MCP 재생성
- **근거:** [R01][S01]

## EXEC-04

- **조건·행동:** 새 artifact는 deterministic/repeated/objective/adapter/recovery need가 있을 때만 만든다.
- **검증·실패·강제:** necessity test와 baseline required.
- **예시·반례:** CSV validator / 단발성 메일 문장 수정
- **근거:** [R01][S02]

## EXEC-05

- **조건·행동:** artifact마다 한 primary responsibility를 둔다.
- **검증·실패·강제:** multi-purpose hidden write or undefined effect → BLOCK.
- **예시·반례:** `preview_delete` vs `execute_delete` / read flag로 write 겸용
- **근거:** [S03][S04]

## EXEC-06

- **조건·행동:** runtime/language는 repo/build/deploy fact로 고른다.
- **검증·실패·강제:** no fact → `BLOCKED_PENDING_REPO_FACTS`.
- **예시·반례:** Java service adapter / 취향으로 Python sidecar
- **근거:** [R01][S07][S09]

## EXEC-07

- **조건·행동:** deterministic contract를 implementation보다 먼저 확정한다.
- **검증·실패·강제:** I/O/effect/error/Gate/eval 누락 → no code.
- **예시·반례:** schema-first CLI / tests 뒤늦게 맞추기
- **근거:** [R01][S05]

## EXEC-08

- **조건·행동:** input is closed, versioned, bounded, and canonicalized where hashed.
- **검증·실패·강제:** unknown/duplicate/malformed input → exit 2/BLOCK.
- **예시·반례:** JSON Schema / free-form dict passthrough
- **근거:** [S05]

## EXEC-09

- **조건·행동:** stdout has one structured result; diagnostics go elsewhere.
- **검증·실패·강제:** extra/malformed stdout → ERROR/BLOCK.
- **예시·반례:** one JSON result / logs mixed with JSON
- **근거:** [S07][S09]

## EXEC-10

- **조건·행동:** exit 0 means result emitted, not PASS.
- **검증·실패·강제:** output status/Gate result must be separately verified.
- **예시·반례:** dry-run exit 0 / `0=production success`
- **근거:** [R02]

## EXEC-11

- **조건·행동:** LLM only proposes semantic candidates; code verifies objective facts.
- **검증·실패·강제:** LLM self-approval/final hash → BLOCK.
- **예시·반례:** LLM maps field / validator validates date
- **근거:** [R01][S02]

## EXEC-12

- **조건·행동:** shell calls use explicit argv, fixed executable, cwd/env allowlist.
- **검증·실패·강제:** `sh -c` + untrusted string → BLOCK.
- **예시·반례:** `subprocess.run([...], shell=False)` / concatenated command
- **근거:** [S07][S10]

## EXEC-13

- **조건·행동:** SQL values bind, identifiers allowlist, DB boundary explicit.
- **검증·실패·강제:** raw identifiers/implicit autocommit effect → BLOCK.
- **예시·반례:** transaction batch / SQL string concat
- **근거:** [S11]

## EXEC-14

- **조건·행동:** external write needs typed effect class and pre-effect Gate result.
- **검증·실패·강제:** missing pre-effect evidence → BLOCK.
- **예시·반례:** write adapter / PostToolUse-only defense
- **근거:** [R02]

## EXEC-15

- **조건·행동:** dry-run exercises same checks, never writer.
- **검증·실패·강제:** dry-run has side effect or lacks target fingerprint → FAIL.
- **예시·반례:** plan + fingerprint / “likely no change” text
- **근거:** [S13]

## EXEC-16

- **조건·행동:** apply rechecks plan/Gate/target state.
- **검증·실패·강제:** any dependency changed → STALE.
- **예시·반례:** new ETag requires replan / reuse old dry run
- **근거:** [R02][S13]

## EXEC-17

- **조건·행동:** write idempotency key binds exact semantic payload.
- **검증·실패·강제:** same key/different digest or cross-tenant reuse → BLOCK.
- **예시·반례:** stable operation key / timestamp key each retry
- **근거:** [S12][S14]

## EXEC-18

- **조건·행동:** retry classification is bounded and policy-owned.
- **검증·실패·강제:** retry auth/schema/Gate errors → BLOCK.
- **예시·반례:** Retry-After read / retry denial forever
- **근거:** [S12][S14]

## EXEC-19

- **조건·행동:** uncertain effect is `OUTCOME_UNKNOWN`.
- **검증·실패·강제:** blind retry/new key/PASS conversion → BLOCK.
- **예시·반례:** timeout after dispatch / treating timeout as failed
- **근거:** [S12][S14]

## EXEC-20

- **조건·행동:** reconciliation reads source of truth and emits its own result.
- **검증·실패·강제:** no readback means unknown persists.
- **예시·반례:** operation lookup / tool success text only
- **근거:** [R02][S11]

## EXEC-21

- **조건·행동:** compensation is registered before reversible multi-step effect.
- **검증·실패·강제:** no handler/manual repair path → high-risk BLOCK.
- **예시·반례:** reservation cancel / invent rollback after crash
- **근거:** [S14]

## EXEC-22

- **조건·행동:** Gate binding includes Plan/Gate/checker/source/lock/input/runtime digests.
- **검증·실패·강제:** absent or mismatch → STALE.
- **예시·반례:** contract digest / filename-only binding
- **근거:** [R02]

## EXEC-23

- **조건·행동:** every entrypoint has forward and reverse trace.
- **검증·실패·강제:** orphan CLI/CI/MCP task → BLOCK.
- **예시·반례:** Docker entrypoint in inventory / hidden shell task
- **근거:** [R02]

## EXEC-24

- **조건·행동:** runtime high-risk controls must be actually verified.
- **검증·실패·강제:** profile/config only → `HARD_ENFORCEMENT_UNAVAILABLE`.
- **예시·반례:** verified sandbox / declaring YAML sufficient
- **근거:** [R02][S16][S17]

## EXEC-25

- **조건·행동:** deny-first least privilege separates read/write/reconcile/release.
- **검증·실패·강제:** wildcard/broad credential → BLOCK.
- **예시·반례:** scoped role / Tool listing equals permission
- **근거:** [S04][S25]

## EXEC-26

- **조건·행동:** secrets are references only and never LLM context/log/build args.
- **검증·실패·강제:** canary/value leakage → BLOCK and rotate.
- **예시·반례:** `secret_ref` / token in CLI argument
- **근거:** [S18][S25]

## EXEC-27

- **조건·행동:** dependencies/toolchain/image are immutable and auditable.
- **검증·실패·강제:** floating tag/no lock/digest → STALE/BLOCK.
- **예시·반례:** lock + OCI digest / `latest`
- **근거:** [S15][S19][S21]

## EXEC-28

- **조건·행동:** test evidence binds tested artifact, command, runner/env, result and self-digest.
- **검증·실패·강제:** historical `/tmp` evidence or unbound result → no PASS.
- **예시·반례:** in-toto-like test record / screenshot claim
- **근거:** [S20]

## EXEC-29

- **조건·행동:** critical negative mutation and independent audit are required.
- **검증·실패·강제:** critical mutant survives/disagreement → BLOCK.
- **예시·반례:** remove Gate ID caught / generator grades itself
- **근거:** [S22][S24]

## EXEC-30

- **조건·행동:** unimplemented runtime/write/deploy/state/RAG is named unavailable.
- **검증·실패·강제:** representation as implemented/PASS → BLOCK.
- **예시·반례:** local-only contract / “sandboxed” without inventory
- **근거:** [R02]
