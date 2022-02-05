# OOP - SOLID : OCP (개방-폐쇄 원칙)

## OCP란?
> Open/Closed Principle

**소프트웨어는 확장에는 열려 있고, 수정에는 닫혀 있어야 한다.**

새로운 기능이 추가될 때 기존 코드를 건드리지 않고 새 코드를 추가하는 것만으로 해결해야 한다.
인터페이스와 다형성을 활용하는 것이 핵심이다.

---

## 위반 예시 — 결제 방식 처리

```java
@Service
public class PaymentService {

    public void pay(String paymentType, int amount) {
        if (paymentType.equals("CARD")) {
            System.out.println("카드 결제: " + amount + "원");
            // 카드사 API 호출 로직...
        } else if (paymentType.equals("KAKAO_PAY")) {
            System.out.println("카카오페이 결제: " + amount + "원");
            // 카카오페이 API 호출 로직...
        } else if (paymentType.equals("NAVER_PAY")) {  // 신규 결제수단 추가 시 기존 코드 수정
            System.out.println("네이버페이 결제: " + amount + "원");
        }
        // 토스페이 추가? → 또 여기를 수정해야 함
    }
}
```

결제 수단이 추가될 때마다 `PaymentService`의 핵심 로직을 수정해야 한다.
수정 과정에서 기존에 잘 동작하던 카드/카카오페이 로직에 실수가 생길 수 있다.

---

## 개선 예시 (OCP 적용)

```java
// 추상화
public interface PaymentGateway {
    void pay(int amount);
    String getType();
}

// 카드 결제
@Component
public class CardPayment implements PaymentGateway {
    @Override
    public void pay(int amount) {
        System.out.println("카드 결제 API 호출: " + amount + "원");
    }

    @Override
    public String getType() { return "CARD"; }
}

// 카카오페이
@Component
public class KakaoPayment implements PaymentGateway {
    @Override
    public void pay(int amount) {
        System.out.println("카카오페이 API 호출: " + amount + "원");
    }

    @Override
    public String getType() { return "KAKAO_PAY"; }
}

// 토스페이 추가 → 기존 코드 수정 없이 클래스만 추가
@Component
public class TossPayment implements PaymentGateway {
    @Override
    public void pay(int amount) {
        System.out.println("토스페이 API 호출: " + amount + "원");
    }

    @Override
    public String getType() { return "TOSS"; }
}

// PaymentService는 수정하지 않아도 됨
@Service
@RequiredArgsConstructor
public class PaymentService {

    private final List<PaymentGateway> gateways;

    public void pay(String paymentType, int amount) {
        gateways.stream()
                .filter(g -> g.getType().equals(paymentType))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("지원하지 않는 결제 수단"))
                .pay(amount);
    }
}
```

새로운 결제 수단이 생겨도 `PaymentGateway` 구현체만 추가하면 된다.
`PaymentService`는 손대지 않는다.

---

## 핵심 정리
- `if/else`, `switch`로 타입을 분기하는 코드가 늘어난다면 OCP 위반 신호
- **인터페이스 + 다형성**으로 분기를 제거하는 것이 목표
- Spring에서는 `List<Interface>` 주입으로 OCP를 자연스럽게 구현할 수 있음
