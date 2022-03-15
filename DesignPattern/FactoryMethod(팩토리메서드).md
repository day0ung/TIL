# Design Pattern - Factory Method (팩토리 메서드)

## 분류
> 생성 패턴 (Creational Pattern)

## Factory Method란?
**객체 생성을 서브클래스에 위임하여, 어떤 클래스의 인스턴스를 만들지를 서브클래스가 결정하게 한다.**

객체 생성 로직을 클라이언트 코드에서 분리해 결합도를 낮춘다.

---

## 문제 상황 — 알림 유형별로 분기 처리

```java
@Service
public class NotificationService {

    public void send(String type, String message) {
        if (type.equals("EMAIL")) {
            EmailNotification noti = new EmailNotification();
            noti.send(message);
        } else if (type.equals("SMS")) {
            SmsNotification noti = new SmsNotification();
            noti.send(message);
        } else if (type.equals("SLACK")) {
            SlackNotification noti = new SlackNotification();
            noti.send(message);
        }
        // 새 알림 타입 추가 → 이 코드를 직접 수정해야 함
    }
}
```

---

## 적용 예시

```java
// 제품 인터페이스
public interface Notification {
    void send(String message);
}

// 구체 제품
public class EmailNotification implements Notification {
    @Override
    public void send(String message) {
        System.out.println("이메일 발송: " + message);
    }
}

public class SmsNotification implements Notification {
    @Override
    public void send(String message) {
        System.out.println("SMS 발송: " + message);
    }
}

public class SlackNotification implements Notification {
    @Override
    public void send(String message) {
        System.out.println("Slack 발송: " + message);
    }
}

// 팩토리 메서드
public class NotificationFactory {
    public static Notification create(String type) {
        return switch (type) {
            case "EMAIL" -> new EmailNotification();
            case "SMS"   -> new SmsNotification();
            case "SLACK" -> new SlackNotification();
            default -> throw new IllegalArgumentException("지원하지 않는 알림 타입: " + type);
        };
    }
}

// 클라이언트
@Service
public class NotificationService {

    public void send(String type, String message) {
        Notification notification = NotificationFactory.create(type);
        notification.send(message);
    }
}
```

---

## 핵심 정리
- 객체 생성 로직이 여러 곳에 중복될 때 팩토리로 일원화
- 새 타입 추가 시 팩토리만 수정하면 됨 (OCP와 함께 사용)
- Spring에서는 `@Bean` 메서드가 팩토리 메서드 역할을 함
