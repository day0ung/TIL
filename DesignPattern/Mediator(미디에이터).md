# Design Pattern - Mediator (미디에이터)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Mediator란?
**여러 객체 간의 직접 통신 대신, 중재자를 통해 통신하게 하여 객체 간 결합도를 낮춘다.**

모든 통신을 중재자가 제어하므로 각 객체는 서로를 알 필요가 없다.

---

## 문제 상황 — 마이크로서비스 간 직접 호출로 강결합 발생

```java
@Service
public class OrderService {

    private final PaymentService paymentService;   // 직접 의존
    private final InventoryService inventoryService; // 직접 의존
    private final NotificationService notificationService; // 직접 의존

    public void placeOrder(OrderRequest request) {
        Order order = create(request);
        paymentService.pay(order);           // 직접 호출
        inventoryService.decrease(order);    // 직접 호출
        notificationService.notify(order);   // 직접 호출
    }
}
// OrderService가 모든 서비스를 알고 있음 → 서비스 추가마다 OrderService 수정
```

---

## 적용 예시 — 이벤트 버스를 미디에이터로

```java
// 미디에이터 역할: 이벤트 버스
@Component
@RequiredArgsConstructor
public class OrderEventMediator {

    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    public void onOrderPlaced(Order order) {
        paymentService.pay(order);
        inventoryService.decrease(order);
        notificationService.notify(order);
    }
}

// OrderService는 미디에이터만 호출
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final OrderEventMediator mediator;

    public void placeOrder(OrderRequest request) {
        Order order = orderRepository.save(new Order(request));
        mediator.onOrderPlaced(order); // 이후 처리는 미디에이터에 위임
    }
}
```

## 실무에서는 메시지 브로커가 미디에이터 역할

```java
// Kafka를 미디에이터로 사용
@Service
@RequiredArgsConstructor
public class OrderService {

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public void placeOrder(OrderRequest request) {
        Order order = save(request);
        // 각 서비스에 직접 호출하지 않고 토픽에 발행
        kafkaTemplate.send("order.placed", new OrderEvent(order));
    }
}

// 각 서비스는 독립적으로 구독
@KafkaListener(topics = "order.placed")
public void onOrderPlaced(OrderEvent event) {
    paymentService.pay(event.getOrder());
}
```

---

## 핵심 정리
- N:N 관계의 객체 통신을 1:N(미디에이터:나머지) 구조로 단순화
- Spring의 `ApplicationEventPublisher`, Kafka, RabbitMQ 등이 미디에이터 역할
- 마이크로서비스에서 서비스 간 직접 호출 대신 메시지 브로커를 통한 통신이 미디에이터 패턴의 적용
