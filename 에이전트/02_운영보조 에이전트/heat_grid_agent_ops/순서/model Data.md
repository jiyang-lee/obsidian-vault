# 0. 구조도

![[Pasted image 20260706202154.png]]
# 1. MODEL_RUNS
|컬럼|의미|
|---|---|
|`model_run_id`|모델 실행 ID|
|`model_family`|모델 계열. 예: `anomaly`, `risk`, `leadtime`, `m1_specialist`, `priority`|
|`model_name`|실제 모델/정책 이름|
|`model_version`|모델 버전|
|`run_type`|실행 방식. 예: `batch`, `replay`, `imported_score`, `policy`|

# 2. MODEL_OUTPUTS
|컬럼|의미|
|---|---|
|`model_output_id`|모델 산출물 ID|
|`window_id`|어떤 window의 결과인지|
|`model_run_id`|어떤 모델 실행에서 나온 결과인지|
|`model_family`|모델 계열|
|`score_name`|점수 이름|
|`score_value`|점수 값|
|`label_name`|라벨 이름|
|`label_value`|라벨 값|
# 3. PRIORITY_DECISIONS
|컬럼|의미|
|---|---|
|`priority_decision_id`|우선순위 판단 ID|
|`window_id`|어떤 window에 대한 판단인지|
|`current_best_priority_score`|기존 Current-Best priority 점수|
|`current_best_priority_level`|기존 Current-Best priority level|
|`m1_specialist_priority_score`|M1 specialist priority 점수|
|`m1_specialist_priority_level`|M1 specialist priority level|
|`priority_score`|최종 hybrid priority 점수|
|`priority_level`|최종 level|
|`priority_source`|어떤 공식/정책으로 계산했는지|
|`m1_priority_agreement`|Current-Best와 M1이 같은 방향인지|