# CAPABILITY_PLAN schema 가이드

이 구현은 외부 YAML 의존성을 피하기 위해 `.yaml` 파일에 canonical JSON을 기록할 수 있다. JSON은 YAML 1.2의 유효한 부분집합이다.

## 필수 top-level

```text
schema_version
plan_id
status
snapshot
request
repository_facts
atomic_capabilities
architecture
workflow
permissions_and_effects
state
knowledge_plan
questions
checks_and_evals
handoff_contracts
open_risks
assumptions
change_history
```

## Atomic Capability

```yaml
id:
name:
purpose:
inputs: []
outputs: []
acceptance_criteria: []
decision_axes: []
knowledge: {}
placement:
  primary_owner: llm|code|knowledge|tool|agent|human
dependencies: []
failure_modes: []
recovery: []
```

`primary_owner`는 정확히 하나다.

## Selected component

```yaml
type:
capability_ids: []
evidence:
owner:
necessity_test:
  planned_hypothesis:
  baseline_result:
  post_build_ablation_result:
```

## Rejected component

```yaml
type:
reason:
reconsider_when:
```

## Agent termination

`bounded_agent`와 `multi_agent`는 다음을 요구한다.

```yaml
workflow:
  termination:
    max_turns:
    max_tool_calls:
    max_time_seconds:
    completion_condition:
    error_stop_condition:
    human_handoff_condition:
```

## RAG

RAG가 선택되면 다음이 모두 필요하다.

```yaml
knowledge_plan:
  mode: rag
  corpus: []
  freshness: {}
  acl: {}
  citation: {}
  retrieval_eval: {}
```

## Persistent state

```yaml
state:
  persistent: true
  scope:
  owner:
  ttl:
  deletion:
  identity_binding:
  migration:
```

## Approval status

실제 독립 실행 identity가 없는 procedural audit는 `PASS_LOCAL_PROCEDURE`까지만 허용한다. `APPROVED_FOR_DESIGN`은 current machine check와 실제 독립 read-only audit를 모두 요구한다.
