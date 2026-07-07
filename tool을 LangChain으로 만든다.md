# 1. Tool

>내가 만든 Python 함수를 LLM이 호출할 수 있는 기능으로 등록한다.

##### LangChain Tool:
```
from langchain.tools import tool

@tool
def get_sensor_data(card_id: str) -> str:
    """card_id에 해당하는 지역난방 센서 데이터를 조회한다."""
    return "공급온도 85도, 환수온도 55도"
```

이 툴을 사용하면 LLM은 이런 식으로 판단할 수 있다.
```
사용자: card_001 상태 알려줘

LLM 생각:
아, 센서 데이터가 필요하네.
get_sensor_data tool을 card_id="card_001"로 호출해야겠다.
```

=> LLM이 직접 DB를 뒤지는 게 아니라, Tool로 등록된 함수를 호출해서 데ㅇ터를 가져오는 것이다.

##### 프로젝트에서,
```
사용자: 이 card_id 상태 분석해줘
→ LLM
→ "센서 데이터 필요함"
→ get_sensor_data Tool 호출
→ DB/예제 데이터 조회
→ 결과를 LLM에게 다시 전달
→ LLM이 summary/action_plan/caution 생성
```

---

# 2. v1에서의 Tool

|Tool 이름 예시|하는 일|
|---|---|
|`get_card_data`|선택한 `card_id`의 카드 정보 조회|
|`get_sensor_values`|현재 센서값 조회|
|`get_model_signals`|모델이 감지한 이상 신호 조회|
|`save_ops_note`|LLM 운영 메모를 DB에 저장|
|`search_past_cases`|과거 유사 사례 검색|

>DB 조회 함수, 저장 함수, 검색 함수 같은 기능을 LangChain Tool 형태로 감싸서 LLM이 사용할 수 있게 만든다.

