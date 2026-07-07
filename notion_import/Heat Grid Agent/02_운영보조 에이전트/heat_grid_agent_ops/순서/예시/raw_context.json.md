# raw_context.json

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
      },
      {
        "feature_name": "p_return_gap__last_minus_first",
        "source_sensor": "p_return_gap",
        "meaning": "window 내 return gap 변화",
        "feature_value": 4.2
      }
    ]
  }
}
