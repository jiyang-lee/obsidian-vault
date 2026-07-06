
![[Pasted image 20260706215700.png]]


# 1. raw_context

![[Pasted image 20260706215725.png]]


### 예시 json: [[raw_context.json]]

- 매핑표는 만들어줘야 한다: [[feature_meta_map]]

---

## 2. priority_context

![[Pasted image 20260706215805.png]]

### 예시 json: [[priority_context.json]]

---

## 3. 최종 예시 json: [[ops_agent_input.json]]

#### 호출 단위: 

```
card_id 1개 = ops_agent_input.json 1개 = LLM 호출 1번
```

#### 흐름:

```
card_id 선택
→ DB에서 raw_context 조립
→ DB에서 priority_context 조립
→ 둘을 합쳐 ops_agent_input.json 생성
→ LLM 호출
→ 결과를 LLM_OPS_NOTES에 저장
```
