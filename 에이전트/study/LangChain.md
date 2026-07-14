
# 1. LangChain이 뭐냐?

>프롬프트 만들기 -> 모델 호출하기 -> 결과 정리하기를 하나의 흐름으로 묶어주는 도구

#### 그냥 LLM을 쓴다면?

```
"이 상황 요약해줘"
→ LLM
→ 긴 문장 답변
```

#### 근데 LangChain을 쓴다면?

```
PromptTemplate
→ LLM
→ OutputParser
→ 정리된 결과
```

- 구조화가 가능하다.
- 공식 문서에서, PromptTemplate는 사용자의 입력 변수를 받아 LLM에 넣을 프롬프트를 만드는 역할
- ChatPromptTemplate는 채팅 모델용으로 system/human 메시지를 구성할 때 쓰는 방식
---
# 2. 제일 기본 구조

#### LangChain의 기본 모양

```
입력값
→ Prompt
→ LLM
→ Parser
→ 출력값
```

##### 지역난방 프로젝트에 대입한다면?

```
센서 데이터
→ 운영 판단 프롬프트
→ LLM
→ JSON Parser
→ summary / action_plan / caution
```

##### 프로젝트에서 LangChain 부분

```
ops_agent_input
→ PromptTemplate
→ LLM
→ OutputParser
→ ops_agent_output
```

---
# 3. PromptTemplate이란?

> 프롬프트를 매번 손으로 쓰는 게 아닌, 빈칸을 만들어두고 데이터를 끼워넣음

##### 예를 들어서,

```
너는 지역난방 운영 보조 AI야.
현재 센서값은 {sensor_values}야.
이 상황을 요약하고, 운영자가 확인할 행동을 알려줘.
```

여기서 {sensor_values} 가 빈칸이고,
실제 실행할 때 이 안에 센서 데이터가 들어간다.

```
sensor_values = "공급온도 85도, 환수온도 55도, 유량 감소"
```

##### 최종 프롬프트:

```
너는 지역난방 운영 보조 AI야.
현재 센서값은 공급온도 85도, 환수온도 55도, 유량 감소야.
이 상황을 요약하고, 운영자가 확인할 행동을 알려줘.
```

---
# 4. Chain이란?

>Chain은 여러 단계를 |로 연결한 것이다.

```PYTHON
chain = prompt | llm | parser
```

말로 풀면:

```
prompt로 질문 형태를 만들고
→ llm에게 보내고
→ parser로 결과를 정리한다
```

---
# 5. 프로젝트에 연결하면?

v1에서 LangChain의 역할

```
ops_agent_input 생성 완료
→ LangChain chain 실행
→ LLM이 운영 메모 생성
→ JSON 형태로 파싱
→ ops_agent_output 생성
```

**LLM에게 일을 시키는 한 묶음**이 LangChain

---
# 6. [[tool을 LangChain으로 만든다]]
