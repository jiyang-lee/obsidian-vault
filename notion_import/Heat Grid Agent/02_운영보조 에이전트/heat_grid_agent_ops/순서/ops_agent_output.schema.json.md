# ops_agent_output.schema.json

## 요약
- 이 문서는 `예시 json: [[ops_agent_output.json]]`를 중심으로 정리된 세부 설명입니다.
- 관련 문서: `ops_agent_output.json`

## 원문

## 예시 json: [ops_agent_output.json](예시/ops_agent_output.json.md)


### 역할
|필드|역할|
|---|---|
|`summary`|이 카드가 무슨 상황인지 한눈에 설명|
|`action_plan`|운영자가 다음에 뭘 확인/조치해야 하는지|
|`caution`|오탐, 데이터 품질, 모델 신뢰도 같은 주의사항|

### DB 저장한다면, LLM_OPS_NOTES 랑 바로 연결

```
LLM_OPS_NOTES
- summary
- action_plan
- caution
- prompt_input
- llm_output
- created_at
```

### 흐름

```
ops_agent_input.json
→ LLM
→ summary / action_plan / caution
→ LLM_OPS_NOTES 저장
```
