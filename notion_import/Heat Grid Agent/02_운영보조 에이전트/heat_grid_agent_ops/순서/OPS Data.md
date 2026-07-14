# OPS Data

## 요약
- 이 문서는 `0. 구조도`를 중심으로 정리된 세부 설명입니다.
- 관련 문서: `Pasted image 20260706210749.png`

## 원문

# 0. 구조도


![](../../../image/Pasted image 20260706210749.png)


# 1. SENSOR_SUMMARIES

| 컬럼                  | 타입       | 설명                                                                         |
| ------------------- | -------- | -------------------------------------------------------------------------- |
| `sensor_summary_id` | uuid, PK | 센서 요약 ID                                                                   |
| `card_id`           | uuid, FK | 연결된 priority card                                                          |
| `window_id`         | uuid, FK | 연결된 분석 window                                                              |
| `flow_source`       | text     | 어떤 흐름의 근거인지. `shared`, `flow1_anomaly_current_best`, `flow2_m1_specialist` |
| `feature_name`      | text     | 사용된 feature 이름                                                             |
| `source_sensor`     | text     | 원천 센서 이름                                                                   |
| `meaning`           | text     | feature 의미                                                                 |
| `feature_value`     | double   | 해당 window의 feature 값                                                       |
| `direction`         | text     | 증가/감소/변동성 증가 등 해석 방향                                                       |
| `display_rank`      | int      | 카드에 보여줄 순서                                                                 |
| `summary_text`      | text     | 운영자에게 보여줄 짧은 설명                                                            |
# 2. LLM_OPS_NOTES

| 컬럼             | 타입        | 설명                |
| -------------- | --------- | ----------------- |
| `llm_note_id`  | uuid, PK  | LLM note ID       |
| `card_id`      | uuid, FK  | 연결된 priority card |
| `summary`      | text      | 한두 문장 운영 요약       |
| `action_plan`  | text      | 권장 조치             |
| `caution`      | text      | 주의사항/신뢰도/리뷰 필요 사유 |
| `prompt_input` | jsonb     | LLM에 넣은 구조화 입력    |
| `llm_output`   | jsonb     | LLM 원본 출력         |
| `created_at`   | timestamp | 생성 시각             |
