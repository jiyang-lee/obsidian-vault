# fault_group_weight

## 요약
- 이 문서는 `1. fault_group_weight의 의미?`를 중심으로 정리된 세부 설명입니다.
- 관련 하위 링크 없이 단일 설명 또는 예시를 보존하는 문서입니다.

## 원문

## 1. fault_group_weight의 의미?

고장군별로 얼마나 자주 나오고, 얼마나 모니터링 가능한 고장인가를 반영한 보정값이다.
고장군별 이벤트 수와 고장군별 고장일 가능성이 얼마나 큰지를 조합한 가중치이다.

|fault_group|rows|mean_monitoring_potential|frequency_norm|monitoring_norm|group_weight|
|---|---|---|---|---|---|
|control_controller|12|3.9167|1.0000|1.0000|1.0000|
|pump_failure|5|3.7800|0.4167|0.9651|0.6360|
|valve_actuator|5|3.2400|0.4167|0.8272|0.5809|
|pressure_regulator|4|3.1500|0.3333|0.8043|0.5217|
|leakage_water_loss|5|1.9000|0.4167|0.4851|0.4440|
|unknown_review|2|없음|0.1667|0.0000|0.1000|
- monitoring_potential: 그 고장이 센서 데이터로 관측/탐지될 가능성이 얼마나 큰지?

---

## 2. 실제 가중치

|fault_group|group_weight 근거|
|---|---|
|control_controller|1.000000|
|pump_failure|0.636043|
|valve_actuator|0.580894|
|pressure_regulator|0.521702|
|leakage_water_loss|0.444043|
|unknown_review|0.100000|
control_controller가 1.0인 이유는 M1 데이터에서 제일 자주 나오고, monitoring potential도 제일 높았기 떄문이다.

반면, leakeage_water_loss는 event 수는 5개로 pump/value와 비슷하ㅣ만, monitoring potential 평균이 1.9로 낮아서 weight가 낮아졌다.

unknown_review는 학습/자동 우선순위 판단 대상으로 보기 어렵기 때문에 0.1로 낮게 뒀다.

## 3. 결론

주 판단 신호가 아니고 0.15의 영항이다.

그러나 event수가 작기 때문에 절대적인 고장 심각도표가 아니다. 데이터가 늘어나거나 운영 기준이 생기면 다시 조정해야 한다.
