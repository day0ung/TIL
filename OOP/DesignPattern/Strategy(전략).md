# Design Pattern - Strategy (전략)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Strategy란?
**알고리즘을 캡슐화하고 교체 가능하게 만든다. 런타임에 알고리즘을 선택할 수 있다.**

조건 분기로 처리하던 알고리즘 선택 로직을 전략 객체로 분리한다.

---

## 문제 상황 — 배송비 계산 방식이 조건에 따라 다름

```java
@Service
public class DeliveryService {

    public int calculateFee(String memberGrade, int orderAmount) {
        if (memberGrade.equals("VIP")) {
            return 0; // VIP는 무료
        } else if (memberGrade.equals("GOLD")) {
            return orderAmount >= 30000 ? 0 : 1500; // 3만원 이상 무료
        } else {
            return orderAmount >= 50000 ? 0 : 3000; // 5만원 이상 무료
        }
        // 새 등급 추가 → 이 코드 수정 필요
    }
}
```

---

## 적용 예시

```java
// 전략 인터페이스
public interface DeliveryFeeStrategy {
    int calculate(int orderAmount);
}

// VIP 전략
@Component("vipDeliveryFeeStrategy")
public class VipDeliveryFeeStrategy implements DeliveryFeeStrategy {
    @Override
    public int calculate(int orderAmount) {
        return 0; // 항상 무료
    }
}

// 골드 전략
@Component("goldDeliveryFeeStrategy")
public class GoldDeliveryFeeStrategy implements DeliveryFeeStrategy {
    @Override
    public int calculate(int orderAmount) {
        return orderAmount >= 30000 ? 0 : 1500;
    }
}

// 일반 전략
@Component("basicDeliveryFeeStrategy")
public class BasicDeliveryFeeStrategy implements DeliveryFeeStrategy {
    @Override
    public int calculate(int orderAmount) {
        return orderAmount >= 50000 ? 0 : 3000;
    }
}

// 전략 선택기
@Component
@RequiredArgsConstructor
public class DeliveryFeeStrategySelector {

    private final Map<String, DeliveryFeeStrategy> strategyMap;

    public DeliveryFeeStrategy select(String memberGrade) {
        String beanName = memberGrade.toLowerCase() + "DeliveryFeeStrategy";
        DeliveryFeeStrategy strategy = strategyMap.get(beanName);
        if (strategy == null) throw new IllegalArgumentException("알 수 없는 등급: " + memberGrade);
        return strategy;
    }
}

// 서비스
@Service
@RequiredArgsConstructor
public class DeliveryService {

    private final DeliveryFeeStrategySelector selector;

    public int calculateFee(String memberGrade, int orderAmount) {
        return selector.select(memberGrade).calculate(orderAmount);
    }
}
```

새 등급이 생기면 `DeliveryFeeStrategy` 구현체만 추가하면 된다.

---

## 핵심 정리
- `if/else`나 `switch`로 알고리즘을 분기하는 코드가 늘어나면 전략 패턴 적용을 고려
- 런타임에 알고리즘을 교체해야 하는 경우에 적합
- Spring에서 `Map<String, Interface>` 주입으로 전략을 깔끔하게 관리할 수 있음
