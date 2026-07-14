# Gate

## 요약
- 이 문서는 `1. Front Gate Threshold: 0.5`를 중심으로 정리된 세부 설명입니다.
- 관련 하위 링크 없이 단일 설명 또는 예시를 보존하는 문서입니다.

## 원문

# 1. Front Gate Threshold: 0.5

| 모델              | 타입                   | 질문                  |
| --------------- | -------------------- | ------------------- |
| `fault_gate`    | RandomForest depth=3 | 이 패턴이 fault 쪽인가?    |
| `task_gate`     | RandomForest depth=3 | 정비 task 쪽인가?        |
| `activity_gate` | RandomForest depth=3 | 일반 운영 activity 쪽인가? |
RF gate 출력은 해당 class일 확률처럼 쓰인다.
그래서 0.5는 그 class일 가능성이 아닐 가능성보다 크면 통과라는 기준이다.

fault_probability >= 0.5 → fault일 가능성이 normal보다 크다고 판단

**왜 0.5를 썼냐?** fault/task/activity gate는 먼저 상태를 나누는 front gate라서이다.

너무 보수적으로 잡으면 초기에 세 라벨 후보를 놓칠 수 있고,
너무 낮게 잡으면 normal이 너무 많이 들어와서 첫 runtime에는 분류기의 기본 기준으로 검증

|gate|threshold 0.5 결과|
|---|---|
|fault_gate|balanced accuracy 0.8455, recall 0.8909, normal FPR 0.2000|
|task_gate|balanced accuracy 1.0000, normal FPR 0.0000|
|activity_gate|balanced accuracy 1.0000, normal FPR 0.0000|

특히 fault gate는 0.45, 0.5, 0.55, 0.6 중에서 비교됐고, 0.5가 balanced accuracy 기준으로 가장 좋았다.

(balanced accuray = (normal을 맞춘 비율 + fault를 맞춘 비율) / 2, 고장도 잘 잡고 정상도 잘 거르는지”를 반반으로 보는 점수)

|fault_gate threshold|balanced accuracy|
|---|---|
|0.45|0.8351|
|0.50|0.8455|
|0.55|0.7909|
|0.60|0.7649|

---

# 2. Pre-event Gate Threshold: 0.6

> 일반 fault gate보다 더 보수적인 기준을 적용
> 이미 fault gate 안에서 이게 진짜 고자 전조 위험인가?를 다시 보는 단계라서 오탐을 줄이는 쪽으로 목표를 세움

|기준|값|
|---|---|
|평가 row|49개|
|normal|35개|
|positive|14개|
|threshold|0.6|
|balanced accuracy|0.8500|
|recall|0.7857|
|normal FPR|0.0857|
|FP / FN|3 / 3|
0.6 기준에서 고장 전조 14개 중 11개 탐지, 정상 35개 중 3개만 오탐이라는 결과다.

**0.5랑 비교하면 왜 0.6이냐?**

|threshold|balanced accuracy|recall|FP|
|---|---|---|---|
|0.4|0.6000|0.5714|13|
|0.5|0.6286|0.5714|11|
|0.6|0.6500|0.5000|7|
|0.7|0.6286|0.4286|6|

0.6 은 0.5보다 recall은 조금 낮지만, FP가 11에서 7로 줄고, BA가 가장 높다.
0.7 로 올리면 FP는 조금 더 줄지만 recall이 더 떨어진다.

따라서 0.6은 오탐을 줄이면서 전조 탐지 성능을 유지하는 기준이다.

**한계** : 현장 출동 비용까지 반영한 최종 운영 최적값은 아니다. 운영 비용/SLA가 생기면 다시 조정.
