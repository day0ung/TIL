# Design Pattern - Composite (컴포지트)

## 분류
> 구조 패턴 (Structural Pattern)

## Composite란?
**객체들을 트리 구조로 구성하여 단일 객체와 복합 객체를 동일하게 다룰 수 있게 한다.**

개별 객체와 그 객체들의 그룹을 같은 인터페이스로 처리할 수 있다.

---

## 문제 상황 — 카테고리 트리에서 전체 가격 합산

```java
// 단건 상품과 상품 묶음을 다르게 처리해야 함
public int calculateTotal(Object item) {
    if (item instanceof Product) {
        return ((Product) item).getPrice();
    } else if (item instanceof ProductBundle) {
        int total = 0;
        for (Object child : ((ProductBundle) item).getItems()) {
            total += calculateTotal(child); // 재귀 처리 직접 구현
        }
        return total;
    }
    throw new IllegalArgumentException("알 수 없는 타입");
}
```

---

## 적용 예시

```java
// 공통 컴포넌트 인터페이스
public interface PriceComponent {
    int getPrice();
    String getName();
}

// 단말 노드: 개별 상품
@Getter
@RequiredArgsConstructor
public class Product implements PriceComponent {
    private final String name;
    private final int price;
}

// 복합 노드: 상품 묶음 (자식을 가질 수 있음)
@Getter
public class ProductBundle implements PriceComponent {
    private final String name;
    private final List<PriceComponent> children = new ArrayList<>();

    public void add(PriceComponent component) {
        children.add(component);
    }

    @Override
    public int getPrice() {
        return children.stream()
                       .mapToInt(PriceComponent::getPrice)
                       .sum();
    }
}
```

```java
// 사용
Product keyboard = new Product("키보드", 80000);
Product mouse = new Product("마우스", 50000);
Product monitor = new Product("모니터", 300000);

ProductBundle peripherals = new ProductBundle("주변기기 세트");
peripherals.add(keyboard);
peripherals.add(mouse);

ProductBundle workstation = new ProductBundle("워크스테이션 풀세트");
workstation.add(peripherals);
workstation.add(monitor);

// 단일 객체든 복합 객체든 동일하게 getPrice() 호출
System.out.println(keyboard.getPrice());      // 80000
System.out.println(peripherals.getPrice());   // 130000
System.out.println(workstation.getPrice());   // 430000
```

---

## 핵심 정리
- 계층 구조(카테고리, 메뉴, 조직도, 파일 시스템)를 표현할 때 적합
- 클라이언트가 단일/복합 객체를 구분 없이 동일하게 다룰 수 있음
- 트리 순회 로직을 클라이언트가 아닌 복합 객체 내부에 캡슐화
