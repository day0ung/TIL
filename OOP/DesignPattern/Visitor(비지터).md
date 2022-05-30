# Design Pattern - Visitor (비지터)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Visitor란?
**객체 구조를 변경하지 않고 새로운 연산을 추가할 수 있게 한다.**

데이터 구조(Element)와 그 구조를 처리하는 연산(Visitor)을 분리한다.

---

## 문제 상황 — 정산 방식이 추가될 때마다 도메인 객체를 수정해야 함

```java
public class Order {
    public double calculateSettlement(String type) {
        if (type.equals("STANDARD")) {
            return amount * 0.97; // 수수료 3%
        } else if (type.equals("PREMIUM")) {
            return amount * 0.95; // 수수료 5%
        }
        // 새 정산 방식 추가 → Order를 수정해야 함
    }
}
```

---

## 적용 예시

```java
// 비지터 인터페이스
public interface SettlementVisitor {
    double visit(Order order);
    double visit(SubscriptionOrder subscriptionOrder);
}

// 원소 인터페이스
public interface Settleable {
    double accept(SettlementVisitor visitor);
}

// 일반 주문
@Getter
@RequiredArgsConstructor
public class Order implements Settleable {
    private final Long id;
    private final double amount;

    @Override
    public double accept(SettlementVisitor visitor) {
        return visitor.visit(this);
    }
}

// 구독 주문
@Getter
@RequiredArgsConstructor
public class SubscriptionOrder implements Settleable {
    private final Long id;
    private final double monthlyFee;
    private final int months;

    @Override
    public double accept(SettlementVisitor visitor) {
        return visitor.visit(this);
    }
}

// 표준 정산 비지터
public class StandardSettlementVisitor implements SettlementVisitor {
    @Override
    public double visit(Order order) {
        return order.getAmount() * 0.97; // 수수료 3%
    }

    @Override
    public double visit(SubscriptionOrder order) {
        return order.getMonthlyFee() * order.getMonths() * 0.95;
    }
}

// 프리미엄 정산 비지터 — Order/SubscriptionOrder 수정 없이 추가
public class PremiumSettlementVisitor implements SettlementVisitor {
    @Override
    public double visit(Order order) {
        return order.getAmount() * 0.95; // 수수료 5%
    }

    @Override
    public double visit(SubscriptionOrder order) {
        return order.getMonthlyFee() * order.getMonths() * 0.90;
    }
}

// 사용
@Service
public class SettlementService {

    public double calculate(Settleable item, SettlementVisitor visitor) {
        return item.accept(visitor);
    }
}

// 클라이언트
Order order = new Order(1L, 100000);
double standard = settlementService.calculate(order, new StandardSettlementVisitor()); // 97000
double premium  = settlementService.calculate(order, new PremiumSettlementVisitor());  // 95000
```

---

## 핵심 정리
- 객체 구조는 안정적이고, 연산(기능)이 자주 추가되는 경우에 적합
- 반대로 새 타입이 자주 추가되는 경우에는 비지터가 오히려 부담 (모든 비지터에 추가해야 함)
- 정산, 세금 계산, 직렬화, AST 처리 등 여러 방식으로 처리해야 하는 요소 집합에 사용
