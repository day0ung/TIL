# Design Pattern - Observer (옵저버)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Observer란?
**한 객체의 상태가 변하면 그 객체에 의존하는 다른 객체들이 자동으로 알림을 받고 갱신된다.**

발행(Publisher)과 구독(Subscriber)을 분리하여 느슨한 결합을 만든다.

---

## 문제 상황 — 주문 완료 후 처리를 OrderService가 직접 다 함

```java
@Service
public class OrderService {

    public void completeOrder(Order order) {
        order.complete();
        orderRepository.save(order);

        // 이하 모든 후처리를 OrderService가 직접 알고 있음
        emailService.sendOrderComplete(order);
        smsService.sendOrderComplete(order);
        inventoryService.decreaseStock(order);
        pointService.accumulatePoint(order);
        // 새 요구사항: 쿠폰 발급 추가 → OrderService 또 수정
    }
}
```

---

## 적용 예시 — Spring ApplicationEvent 활용

```java
// 이벤트 객체
public class OrderCompletedEvent {
    private final Order order;

    public OrderCompletedEvent(Order order) {
        this.order = order;
    }

    public Order getOrder() { return order; }
}

// 발행자: OrderService는 이벤트만 발행
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final ApplicationEventPublisher eventPublisher;

    public void completeOrder(Order order) {
        order.complete();
        orderRepository.save(order);
        eventPublisher.publishEvent(new OrderCompletedEvent(order)); // 이벤트 발행
    }
}

// 구독자 1: 이메일
@Component
public class EmailEventListener {
    @EventListener
    public void onOrderCompleted(OrderCompletedEvent event) {
        emailService.sendOrderComplete(event.getOrder());
    }
}

// 구독자 2: 재고
@Component
public class InventoryEventListener {
    @EventListener
    public void onOrderCompleted(OrderCompletedEvent event) {
        inventoryService.decreaseStock(event.getOrder());
    }
}

// 구독자 3: 포인트 (나중에 추가 — OrderService 수정 없음)
@Component
public class PointEventListener {
    @EventListener
    @Async // 비동기 처리
    public void onOrderCompleted(OrderCompletedEvent event) {
        pointService.accumulatePoint(event.getOrder());
    }
}
```

새 처리가 필요할 때 리스너 클래스만 추가하면 되고, `OrderService`는 수정하지 않는다.

---

## 핵심 정리
- 한 이벤트에 여러 후처리가 필요할 때 발행-구독으로 분리
- `OrderService`의 책임이 "주문 완료"로 한정되어 SRP도 함께 지켜짐
- Spring `ApplicationEventPublisher` + `@EventListener`가 옵저버 패턴의 실무 구현
- 비동기 처리가 필요하면 `@Async`와 함께 사용
