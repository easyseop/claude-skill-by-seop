# Planner 질문 정책

질문은 네 종류로 분류한다.

## 1. 저장소 조사로 해결

사용자에게 묻지 않는다.

예:

- 기존 Script·Tool·Skill 존재 여부
- runtime·lockfile·test runner
- 현재 Git ref와 설정 파일

## 2. 안전한 기본값

보수적으로 적용하고 plan에 기록한다.

```text
외부 write보다 read-only/dry-run
자동 실행보다 명시 실행
allow보다 deny
secret는 out-of-band
미확인 runtime enforcement는 unavailable
```

## 3. 사용자 정책 결정

결과의 architecture·권한·합격 기준을 실제로 바꾸는 경우 한 번에 묶어 질문한다.

예:

- 허용되는 외부 dependency
- 권위 지식 원천
- 결과 전달 형식
- 승인 책임자와 범위

## 4. 고위험 차단 질문

답 전에는 `BLOCKED_WAITING_USER_DECISION`이다.

예:

- 금액·삭제·발송 한도
- 운영 write 승인자
- tenant·role 정책
- retention·법적 근거
- rollback 불가능한 작업 범위

## 질문 schema

```yaml
id:
question:
why_needed:
options:
  - id:
    effect:
safe_default:
blocking:
status:
answer:
```

질문은 control mode, component set, 권한·부작용, acceptance/eval, 권위 source, 결과 형식 중 하나를 변경할 때만 허용한다.
