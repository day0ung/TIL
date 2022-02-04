# OOP - SOLID : SRP (단일 책임 원칙)

## SRP란?
> Single Responsibility Principle

**하나의 클래스는 하나의 책임만 가져야 한다.**

클래스를 변경하는 이유는 오직 하나뿐이어야 한다.
책임이 많아질수록 하나를 수정할 때 다른 기능까지 영향을 줄 가능성이 높아진다.

---

## 위반 예시 — 주문 처리 서비스

실무에서 흔히 보이는 패턴: 하나의 Service 클래스가 너무 많은 일을 한다.

```java
@Service
public class OrderService {

    public void placeOrder(Order order) {
        // 1. 재고 확인
        if (order.getQuantity() > getStock(order.getProductId())) {
            throw new IllegalStateException("재고 부족");
        }

        // 2. DB 저장
        orderRepository.save(order);

        // 3. 결제 처리
        String paymentResult = callPaymentGateway(order.getAmount());
        if (!paymentResult.equals("SUCCESS")) {
            throw new RuntimeException("결제 실패");
        }

        // 4. 알림 이메일 발송
        String body = "주문번호 " + order.getId() + " 접수되었습니다.";
        emailClient.send(order.getUserEmail(), "주문 완료", body);

        // 5. Slack 알림
        slackClient.post("#orders", "새 주문: " + order.getId());
    }
}
```

`OrderService`를 수정해야 하는 이유가 너무 많다.
- 결제사 변경 → 수정
- 이메일 템플릿 변경 → 수정
- Slack 채널 변경 → 수정
- 재고 정책 변경 → 수정

---

## 개선 예시 (SRP 적용)

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final StockValidator stockValidator;
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final NotificationService notificationService;

    public void placeOrder(Order order) {
        stockValidator.validate(order);
        orderRepository.save(order);
        paymentService.pay(order);
        notificationService.notifyOrderPlaced(order);
    }
}

// 재고 검증 책임
@Component
public class StockValidator {
    public void validate(Order order) {
        if (order.getQuantity() > getStock(order.getProductId())) {
            throw new IllegalStateException("재고 부족");
        }
    }
}

// 결제 책임
@Service
public class PaymentService {
    public void pay(Order order) {
        String result = callPaymentGateway(order.getAmount());
        if (!result.equals("SUCCESS")) {
            throw new RuntimeException("결제 실패");
        }
    }
}

// 알림 책임
@Service
public class NotificationService {
    public void notifyOrderPlaced(Order order) {
        emailClient.send(order.getUserEmail(), "주문 완료", buildEmailBody(order));
        slackClient.post("#orders", "새 주문: " + order.getId());
    }
}
```

이제 결제사가 바뀌면 `PaymentService`만, 알림 방식이 바뀌면 `NotificationService`만 수정하면 된다.

---

## 핵심 정리
- 클래스를 수정해야 하는 이유가 **두 가지 이상**이라면 SRP 위반 신호
- 메서드가 너무 많거나 파일이 너무 길어졌다면 책임 분리를 고려
- Spring 환경에서는 Service → 여러 Component/Service로 역할을 나누는 방식으로 적용
