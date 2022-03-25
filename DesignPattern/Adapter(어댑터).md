# Design Pattern - Adapter (어댑터)

## 분류
> 구조 패턴 (Structural Pattern)

## Adapter란?
**호환되지 않는 인터페이스를 가진 클래스들이 함께 동작할 수 있도록 중간에서 변환해주는 패턴.**

기존 코드를 수정하지 않고 새로운 인터페이스와 연결할 때 사용한다.

---

## 문제 상황 — 외부 결제 라이브러리 교체

기존에 `KakaoPayClient`를 직접 사용하다가 PG사가 토스로 바뀐 상황.
`TossPayClient`는 메서드명과 파라미터 구조가 다르다.

```java
// 기존 카카오페이 클라이언트
public class KakaoPayClient {
    public String requestPayment(String orderId, int amount) {
        return "kakao_" + orderId;
    }
}

// 새로 도입된 토스페이 클라이언트 (외부 라이브러리 — 수정 불가)
public class TossPayClient {
    public TossPayResponse pay(TossPayRequest request) {
        return new TossPayResponse("toss_" + request.getOrderId(), "SUCCESS");
    }
}

// 기존 서비스 코드에서 TossPayClient를 직접 쓰려면 전체 수정 필요
@Service
public class PaymentService {
    private final KakaoPayClient kakaoPayClient; // 여기를 바꾸면 연쇄 수정 발생
}
```

---

## 적용 예시

```java
// 공통 인터페이스 (Target)
public interface PaymentClient {
    String pay(String orderId, int amount);
}

// 기존 카카오 → 어댑터로 래핑
public class KakaoPayAdapter implements PaymentClient {
    private final KakaoPayClient kakaoPayClient;

    public KakaoPayAdapter(KakaoPayClient kakaoPayClient) {
        this.kakaoPayClient = kakaoPayClient;
    }

    @Override
    public String pay(String orderId, int amount) {
        return kakaoPayClient.requestPayment(orderId, amount);
    }
}

// 토스 → 어댑터로 래핑 (파라미터 변환 처리)
public class TossPayAdapter implements PaymentClient {
    private final TossPayClient tossPayClient;

    public TossPayAdapter(TossPayClient tossPayClient) {
        this.tossPayClient = tossPayClient;
    }

    @Override
    public String pay(String orderId, int amount) {
        TossPayRequest request = new TossPayRequest(orderId, amount);
        TossPayResponse response = tossPayClient.pay(request);
        return response.getTransactionId();
    }
}

// PaymentService는 수정 없이 인터페이스만 사용
@Service
@RequiredArgsConstructor
public class PaymentService {
    private final PaymentClient paymentClient; // 어댑터가 주입됨

    public String processPayment(String orderId, int amount) {
        return paymentClient.pay(orderId, amount);
    }
}
```

```java
// Spring 설정으로 어댑터 교체
@Configuration
public class PaymentConfig {
    @Bean
    public PaymentClient paymentClient() {
        return new TossPayAdapter(new TossPayClient()); // 토스로 교체
    }
}
```

---

## 핵심 정리
- 외부 라이브러리나 레거시 코드를 수정하지 않고 기존 시스템에 통합할 때 사용
- 인터페이스가 맞지 않는 두 클래스 사이에 어댑터를 끼워 호환성 확보
- Spring에서 외부 SDK를 `@Bean`으로 감싸는 패턴이 어댑터의 일종
