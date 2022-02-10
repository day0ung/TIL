# OOP - SOLID : ISP (인터페이스 분리 원칙)

## ISP란?
> Interface Segregation Principle

**클라이언트는 자신이 사용하지 않는 메서드에 의존하도록 강요받으면 안 된다.**

하나의 비대한 인터페이스보다 **역할별로 나눈 작은 인터페이스** 여러 개가 낫다.

---

## 위반 예시 — 알림 서비스

```java
// 모든 알림 방식을 하나의 인터페이스에 때려넣음
public interface NotificationService {
    void sendEmail(String to, String subject, String body);
    void sendSMS(String phoneNumber, String message);
    void sendSlack(String channel, String message);
    void sendPushNotification(String deviceToken, String message);
}

// SMS 발송 전용 구현체인데 나머지를 억지로 구현해야 함
public class SMSNotificationService implements NotificationService {
    @Override
    public void sendSMS(String phoneNumber, String message) {
        System.out.println("SMS 발송: " + phoneNumber);
    }

    @Override
    public void sendEmail(String to, String subject, String body) {
        throw new UnsupportedOperationException("SMS 서비스는 이메일 미지원");
    }

    @Override
    public void sendSlack(String channel, String message) {
        throw new UnsupportedOperationException("SMS 서비스는 Slack 미지원");
    }

    @Override
    public void sendPushNotification(String deviceToken, String message) {
        throw new UnsupportedOperationException("SMS 서비스는 푸시 미지원");
    }
}
```

새 알림 수단이 추가될 때마다 모든 구현체를 수정해야 한다.

---

## 개선 예시 (ISP 적용)

```java
// 역할별로 인터페이스 분리
public interface EmailSender {
    void sendEmail(String to, String subject, String body);
}

public interface SMSSender {
    void sendSMS(String phoneNumber, String message);
}

public interface SlackSender {
    void sendSlack(String channel, String message);
}

public interface PushSender {
    void sendPushNotification(String deviceToken, String message);
}

// 이메일 전용 구현체
@Service
public class EmailNotificationService implements EmailSender {
    @Override
    public void sendEmail(String to, String subject, String body) {
        mailSender.send(to, subject, body);
    }
}

// SMS 전용 구현체
@Service
public class SMSNotificationService implements SMSSender {
    @Override
    public void sendSMS(String phoneNumber, String message) {
        smsClient.send(phoneNumber, message);
    }
}

// 주문 완료 알림: 이메일 + SMS만 필요
@Service
@RequiredArgsConstructor
public class OrderNotificationFacade {

    private final EmailSender emailSender;
    private final SMSSender smsSender;

    public void notifyOrderComplete(Order order) {
        emailSender.sendEmail(order.getEmail(), "주문 완료", buildBody(order));
        smsSender.sendSMS(order.getPhone(), "주문이 접수되었습니다.");
    }
}

// 장애 알림: Slack만 필요
@Service
@RequiredArgsConstructor
public class AlertService {

    private final SlackSender slackSender;

    public void alertIncident(String message) {
        slackSender.sendSlack("#incident", message);
    }
}
```

각 서비스는 자기가 필요한 인터페이스에만 의존한다.
새 알림 채널이 추가되어도 기존 구현체는 건드리지 않는다.

---

## 핵심 정리
- 구현 클래스에서 `throw new UnsupportedOperationException()`이 보이면 ISP 위반 신호
- 인터페이스를 **역할(행위) 단위**로 쪼개면 변경 영향 범위가 좁아짐
- Spring에서 필요한 인터페이스만 `@Autowired`로 주입받는 구조가 ISP를 자연스럽게 따름
