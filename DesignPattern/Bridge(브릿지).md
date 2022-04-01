# Design Pattern - Bridge (브릿지)

## 분류
> 구조 패턴 (Structural Pattern)

## Bridge란?
**구현부(Implementation)와 추상부(Abstraction)를 분리하여 각각 독립적으로 확장할 수 있게 한다.**

두 가지 축으로 변화가 생기는 경우, 상속 대신 조합으로 해결한다.

---

## 문제 상황 — 채널 × 메시지 타입 조합 폭발

```java
// 채널 2개 × 메시지 타입 3개 = 6개 클래스 필요
class KakaoOrderMessage { ... }
class KakaoPromotionMessage { ... }
class KakaoAlertMessage { ... }
class SlackOrderMessage { ... }
class SlackPromotionMessage { ... }
class SlackAlertMessage { ... }

// 새 채널(Line) 추가 → 클래스 3개 더 추가
// 새 메시지 타입(공지) 추가 → 채널 수만큼 클래스 추가
```

---

## 적용 예시

```java
// 구현부: 전송 채널
public interface MessageSender {
    void send(String recipient, String content);
}

@Component
public class KakaoSender implements MessageSender {
    @Override
    public void send(String recipient, String content) {
        kakaoClient.sendMessage(recipient, content);
    }
}

@Component
public class SlackSender implements MessageSender {
    @Override
    public void send(String recipient, String content) {
        slackClient.post(recipient, content);
    }
}

// 추상부: 메시지 타입 (구현부를 브릿지로 보유)
@RequiredArgsConstructor
public abstract class Message {
    protected final MessageSender sender;

    public abstract void send(String recipient);
}

// 주문 메시지
public class OrderMessage extends Message {
    private final Order order;

    public OrderMessage(MessageSender sender, Order order) {
        super(sender);
        this.order = order;
    }

    @Override
    public void send(String recipient) {
        String content = String.format("주문번호 %s 접수 완료. 금액: %d원", order.getId(), order.getAmount());
        sender.send(recipient, content);
    }
}

// 프로모션 메시지
public class PromotionMessage extends Message {
    private final String promoContent;

    public PromotionMessage(MessageSender sender, String promoContent) {
        super(sender);
        this.promoContent = promoContent;
    }

    @Override
    public void send(String recipient) {
        sender.send(recipient, "[이벤트] " + promoContent);
    }
}
```

```java
// 조합: 카카오로 주문 메시지 / 슬랙으로 프로모션 메시지
Message kakaoOrder = new OrderMessage(new KakaoSender(), order);
kakaoOrder.send("010-1234-5678");

Message slackPromo = new PromotionMessage(new SlackSender(), "여름 세일 30% 할인!");
slackPromo.send("#marketing");
```

새 채널(Line)을 추가해도 `MessageSender`만 구현하면 되고, 메시지 타입은 건드리지 않는다.

---

## 핵심 정리
- 두 가지 독립적인 변화 축이 있을 때 상속 대신 조합으로 해결
- 클래스 수 폭발(class explosion)을 막는 데 효과적
- 채널, 렌더러, 포맷터 등 교체 가능한 구현부가 있는 경우 적합
