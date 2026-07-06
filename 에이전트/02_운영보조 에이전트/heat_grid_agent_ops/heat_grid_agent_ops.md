
# 1. DB 구조

![[Pasted image 20260706203027.png]]

![[Pasted image 20260706210520.png]]


```
SENSOR_READINGS
= raw 센서값

WINDOWS
= 분석 단위

WINDOW_FEATURES
= 모델에 들어간 feature들
  compact13도 여기에 저장

MODEL_OUTPUTS
= anomaly, risk, leadtime, M1 gate 같은 모델 결과

PRIORITY_DECISIONS
= Current-Best + M1 + hybrid priority 점수 계산 결과

PRIORITY_CARDS
= 운영자가 볼 카드

SENSOR_SUMMARIES
= 카드에 보여줄 Top 3 센서 요약

LLM_OPS_NOTES
= LLM이 만든 운영 요약/액션/주의사항
```

## 1. [[Raw Data]] 구조
## 2. [[model Data]]  구조
## 3. [[Priority Data]] 구조
## 4. [[OPS Data]] 구조

---

# 2. JSON 설계

![[Pasted image 20260706211839.png]]


## 1. [[ops_agent_input.schema.json]]
## 2. [[ops_agent_output.schema.json]]

