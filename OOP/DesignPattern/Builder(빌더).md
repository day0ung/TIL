# Design Pattern - Builder (빌더)

## 분류
> 생성 패턴 (Creational Pattern)

## Builder란?
**복잡한 객체를 단계적으로 생성할 수 있도록 하고, 동일한 생성 과정으로 다양한 결과물을 만들 수 있게 한다.**

생성자 파라미터가 많을 때 가독성과 안전성을 높이는 데 효과적이다.

---

## 문제 상황 — 파라미터가 많은 생성자

```java
// 어떤 파라미터가 뭔지 한눈에 안 보임
Order order = new Order("홍길동", "서울시 강남구", "CARD", 50000, true, false, "WELCOME10", null);

// 필드 순서 헷갈려서 버그 발생 가능
Order order2 = new Order("서울시 강남구", "홍길동", ...); // 순서 바뀜
```

---

## 적용 예시

```java
public class Order {
    private final String customerName;
    private final String address;
    private final String paymentType;
    private final int totalAmount;
    private final boolean giftWrapping;
    private final String couponCode;

    private Order(Builder builder) {
        this.customerName = builder.customerName;
        this.address = builder.address;
        this.paymentType = builder.paymentType;
        this.totalAmount = builder.totalAmount;
        this.giftWrapping = builder.giftWrapping;
        this.couponCode = builder.couponCode;
    }

    public static class Builder {
        private final String customerName; // 필수
        private final int totalAmount;     // 필수
        private String address;
        private String paymentType = "CARD"; // 기본값
        private boolean giftWrapping = false;
        private String couponCode;

        public Builder(String customerName, int totalAmount) {
            this.customerName = customerName;
            this.totalAmount = totalAmount;
        }

        public Builder address(String address) {
            this.address = address;
            return this;
        }

        public Builder paymentType(String paymentType) {
            this.paymentType = paymentType;
            return this;
        }

        public Builder giftWrapping(boolean giftWrapping) {
            this.giftWrapping = giftWrapping;
            return this;
        }

        public Builder couponCode(String couponCode) {
            this.couponCode = couponCode;
            return this;
        }

        public Order build() {
            return new Order(this);
        }
    }
}

// 사용 — 무엇을 설정하는지 명확히 보임
Order order = new Order.Builder("홍길동", 50000)
        .address("서울시 강남구")
        .paymentType("KAKAO_PAY")
        .giftWrapping(true)
        .couponCode("WELCOME10")
        .build();
```

## Lombok @Builder

```java
@Builder
@Getter
public class Order {
    private String customerName;
    private String address;
    private String paymentType;
    private int totalAmount;
    private boolean giftWrapping;
    private String couponCode;
}

// 사용
Order order = Order.builder()
        .customerName("홍길동")
        .address("서울시 강남구")
        .totalAmount(50000)
        .giftWrapping(true)
        .build();
```

---

## 핵심 정리
- 생성자 파라미터가 4개 이상이면 빌더 패턴 도입을 고려
- 필수 값과 선택 값을 명확하게 구분할 수 있음
- 실무에서는 Lombok `@Builder`로 대부분 해결
