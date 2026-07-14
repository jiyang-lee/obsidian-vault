# feature_meta_map

## 요약
- 이 문서는 `1. 역할`를 중심으로 정리된 세부 설명입니다.
- 관련 하위 링크 없이 단일 설명 또는 예시를 보존하는 문서입니다.

## 원문

## 1. 역할

```
feature_name을 보면
→ source_sensor랑 meaning을 붙여준다
```

## 2. 최소 매핑표

```PYTHON
FEATURE_META = {
    "missing_rate": {
        "source_sensor": "data_quality",
        "meaning": "window 내 결측률"
    },
    "missing_count": {
        "source_sensor": "data_quality",
        "meaning": "window 내 결측 개수"
    },
    "max_timestamp_gap_minutes": {
        "source_sensor": "data_quality",
        "meaning": "window 내 최대 시간 간격"
    },

    "p_return_gap__last_minus_first": {
        "source_sensor": "p_return_gap",
        "meaning": "window 내 return gap 변화"
    },
    "p_net_meter_flow__last_1d_std_minus_prev_6d_std": {
        "source_sensor": "p_net_meter_flow",
        "meaning": "최근 1일 유량 변동성과 이전 6일 유량 변동성 차이"
    },
    "s_hc1_supply_temperature__last_1d_mean_minus_prev_6d_mean": {
        "source_sensor": "s_hc1_supply_temperature",
        "meaning": "최근 1일 공급온도와 이전 6일 공급온도 평균 차이"
    }
}
```
