![[Pasted image 20260706162013.png]]

# 1. 모델이 4개인 이유?

하나의 고장이다/아니다 모델로 끝내기에는 운영 상태 라벨들이 섞여 있기 떄문이다.
고장 전조를 보면서도, 그 신호가 실제 fault인지, task인지, 일반 activity 인지 구분하려 한다.

```
1. 고장/정비/운영활동을 먼저 분리하고
2. 고장 쪽에서는 다시 pre-event 전조 가능성을 따로 본다
```

왜 이렇게 복잡한 구성이냐?
```
이게 진짜 점검 우선순위를 올릴 만한 고장 전조인가?
아니면 정비/운영활동 때문에 생긴 변화인가?
```
를 단계별로 확인하고 싶었기 때문이다.

# 2. Front [[Gate]] 3개

| 모델              | 타입                   | 질문                  |
| --------------- | -------------------- | ------------------- |
| `fault_gate`    | RandomForest depth=3 | 이 패턴이 fault 쪽인가?    |
| `task_gate`     | RandomForest depth=3 | 정비 task 쪽인가?        |
| `activity_gate` | RandomForest depth=3 | 일반 운영 activity 쪽인가? |

왜 나누냐? 센서 패턴이 튀는 이유가 꼭 고장만은 아니기 때문이다.

온도/유량 패턴 변화가 있어도 원인은 여러 가지일 수 있다.
진짜 고장 전조 / 정비 작업 이후 변화 / 운영 모드 변경 / 일반 활동/제어 변화 등의 원인이 존재하고, 이를 하나의 모델로 이상=고장 이라고 하면 오탐이 많아진다.

그래서 먼저 fault/task/activity 세 gate로 맥락을 분리한다.

# 3. Fault 내부 pre-event gate 1개

fault gate가 고장 쪽 신호가 있어 보인다를 본다면, pre event gate는 더 좁게 본다.

```
이게 실제 fault report 전에 나타나는 전조 패턴인가?
```

이 모델은 [[LogisticRegression_balanced]]이고, threshold가 0.6이다.

