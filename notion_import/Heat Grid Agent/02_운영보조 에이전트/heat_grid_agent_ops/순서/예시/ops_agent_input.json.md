# ops_agent_input.json

## 요약
- 이 문서는 `{`를 중심으로 정리된 세부 설명입니다.
- 관련 하위 링크 없이 단일 설명 또는 예시를 보존하는 문서입니다.

## 원문

{
  "raw_context": {
    "window": {
      "window_id": "uuid",
      "manufacturer_id": "manufacturer 1",
      "substation_id": 31,
      "configuration_type": "SH + DHW",
      "window_start": "2020-01-11T00:00:00",
      "window_end": "2020-01-11T06:00:00"
    },
    "features": [
      {
        "feature_name": "missing_rate",
        "source_sensor": "data_quality",
        "meaning": "window 내 결측률",
        "feature_value": 0.02
      }
    ]
  },
  "priority_context": {
    "card": {
      "card_id": "uuid",
      "operational_label": "urgent",
      "primary_state": "pre_fault",
      "review_required": true,
      "trust_level": "medium"
    },
    "priority": {
      "priority_decision_id": "uuid",
      "priority_score": 87.4,
      "priority_level": "urgent",
      "priority_source": "hybrid",
      "m1_priority_agreement": "agree"
    },
    "model_signals": {
      "current_best_priority_score": 82.1,
      "current_best_priority_level": "high",
      "m1_specialist_priority_score": 91.8,
      "m1_specialist_priority_level": "urgent"
    },
    "explanation": {
      "why_reason": "M1 specialist and current-best both indicate elevated priority.",
      "recommended_action": "Review the substation operation and inspect return temperature behavior."
    }
  }
}
