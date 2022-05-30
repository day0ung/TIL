# Design Pattern - State (스테이트)

## 분류
> 행동 패턴 (Behavioral Pattern)

## State란?
**객체의 내부 상태가 바뀔 때 행동도 함께 바뀌게 한다. 마치 클래스가 바뀐 것처럼 보이게 한다.**

상태에 따른 분기 로직을 상태 객체로 분리한다.

---

## 문제 상황 — 주문 상태별 처리 로직이 복잡한 if/else로 뭉쳐있음

```java
@Service
public class OrderService {

    public void cancel(Order order) {
        if (order.getStatus().equals("PENDING")) {
            order.setStatus("CANCELLED");
        } else if (order.getStatus().equals("PAID")) {
            refundService.refund(order);
            order.setStatus("CANCELLED");
        } else if (order.getStatus().equals("SHIPPED")) {
            throw new IllegalStateException("배송 중에는 취소 불가");
        } else if (order.getStatus().equals("DELIVERED")) {
            throw new IllegalStateException("배송 완료 후 취소 불가");
        }
    }

    public void ship(Order order) {
        if (order.getStatus().equals("PAID")) {
            order.setStatus("SHIPPED");
        } else {
            throw new IllegalStateException("결제 완료 상태에서만 배송 가능");
        }
    }
    // 상태가 늘어날수록 if/else 복잡도 폭발
}
```

---

## 적용 예시

```java
// 상태 인터페이스
public interface OrderState {
    void cancel(Order order);
    void ship(Order order);
    void deliver(Order order);
}

// 결제 대기 상태
public class PendingState implements OrderState {
    @Override
    public void cancel(Order order) {
        order.setState(new CancelledState());
    }

    @Override
    public void ship(Order order) {
        throw new IllegalStateException("결제 전에는 배송 불가");
    }

    @Override
    public void deliver(Order order) {
        throw new IllegalStateException("결제 전에는 배달 불가");
    }
}

// 결제 완료 상태
public class PaidState implements OrderState {
    @Override
    public void cancel(Order order) {
        refundService.refund(order);
        order.setState(new CancelledState());
    }

    @Override
    public void ship(Order order) {
        order.setState(new ShippedState());
    }

    @Override
    public void deliver(Order order) {
        throw new IllegalStateException("배송 출발 후 배달 처리 가능");
    }
}

// 배송 중 상태
public class ShippedState implements OrderState {
    @Override
    public void cancel(Order order) {
        throw new IllegalStateException("배송 중에는 취소 불가");
    }

    @Override
    public void ship(Order order) {
        throw new IllegalStateException("이미 배송 중");
    }

    @Override
    public void deliver(Order order) {
        order.setState(new DeliveredState());
    }
}

// Order 객체는 현재 상태에게 위임
@Entity
public class Order {
    @Transient
    private OrderState state = new PendingState();

    public void cancel() { state.cancel(this); }
    public void ship()   { state.ship(this); }
    public void deliver(){ state.deliver(this); }

    void setState(OrderState state) { this.state = state; }
}
```

---

## 핵심 정리
- 상태에 따라 다르게 동작하는 로직이 많고 상태가 자주 추가될 때 적합
- 조건 분기 대신 **상태 객체가 직접 처리**하므로 각 상태의 책임이 명확해짐
- 주문, 결제, 배송, 회원 등 상태 머신이 필요한 도메인에 잘 맞음
