# level

## 요약
- 이 문서는 `레벨의 기준?`를 중심으로 정리된 세부 설명입니다.
- 관련 하위 링크 없이 단일 설명 또는 예시를 보존하는 문서입니다.

## 원문

# 레벨의 기준?

>**validation 데이터에서 오탐을 제한하면서 recall을 최대화하도록 고른 threshold**

검증 데이터 기반 threshold calibration 
= 오탐을 20% 이하로 제한하면서 실제 위험 후보를 최대한 잡는 등급 기준이다.

# 1.로직

```
1. validation split만 본다.
2. threshold 후보를 20 ~ 95 사이에서 훑는다.
3. 각 threshold에서 high/urgent 판정을 만든다.
4. false positive rate <= 0.20 조건을 만족하는 후보 중
5. recall이 가장 높은 threshold를 고른다.
6. recall이 같으면 precision이 높은 쪽을 고른다.
```

- 기준 철학: 정상 설비를 너무 많이 high/urgent로 올리지 않으면서, 진짜 pre_fault는 최대한 많이 잡자.

#### 1. high threshold

```
if FPR <= 0.20:
    candidate = (recall, precision, threshold)
    가장 좋은 candidate 선택
```

high threshold = 67.5 는 validation split에서 이 조건을 만족하는 threshold 중 선택된 값

#### 2. urgent threshold

```
urgent_threshold
= max(high_threshold + 15, validation score의 90% 분위값)
단, 최대 95
```

urgent는 high 기준보다 충분히 더 높거나, validation 상위 10% 에 해당하는 점수

#### 3. medium threshold

```
medium_threshold = max(20, high_threshold * 0.60)
```

medium threshold는 운영용 보조 등급이다.

---

# 2. level threshold의 한계

왜 FPR 허용치를 0.20으로 잡았는지 근거가 없다.

0.20은 모델이 정한 값이 아니라 사람이 정한 허용 오탐률이다.
근데 왜 그 허용치가 맞는지 운영/실험 근거가 부족하다.

#### 1. 해결 방안
FPR cap = 0.05 / 0.10 / 0.15 / 0.20 각각에서 high threshold를 다시 잡고 holdout precision, recall, FPR, top-K를 비교

#### 2. 결정 이유
우리는 넓게 잡는 데모 목적이니까 0.20, 운영 신뢰도를 우선하니까 0.10, 아주 보수적으로 가니까 0.05
