# 0. 구조도

![[Pasted image 20260706202602.png|388]]
# 1.PRIORITY_CARDS
|컬럼|의미|
|---|---|
|`card_id`|priority card ID|
|`priority_decision_id`|어떤 priority decision에서 나온 카드인지|
|`operational_label`|운영 해석 라벨. 예: `predictive_fault_risk`|
|`primary_state`|최종 운영 상태. 예: `normal`, `fault`, `predictive_fault_risk`|
|`review_required`|운영자 검토 필요 여부|
|`trust_level`|신뢰도/주의 수준|
|`first_crossing_time`|기준을 처음 넘은 시점|
|`stable_crossing_time`|안정적으로 기준을 넘은 시점|
|`stable_crossing_lead_hours`|안정 crossing 기준 lead time|
|`why_reason`|왜 이런 판단이 나왔는지|
|`recommended_action`|권장 운영 액션|
|`raw_card`|원본 priority card 전체 JSON|
|`created_at`|생성 시각|
# 2. PRIORITY_CARD_REVIEW_REASONS
| 컬럼                 | 의미                   |
| ------------------ | -------------------- |
| `review_reason_id` | review reason row ID |
| `card_id`          | 어떤 card의 reason인지    |
| `reason_code`      | review 사유 코드         |
# 3. 저장 구조

window 관련 값      → windows
모델 신호 값        → model_outputs
우선순위 계산 값    → priority_decisions
운영 설명/액션 값   → priority_cards
review 사유         → priority_card_review_reasons
원본 전체 55개      → priority_cards.raw_card JSONB