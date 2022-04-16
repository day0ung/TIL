# Design Pattern - Flyweight (플라이웨이트)

## 분류
> 구조 패턴 (Structural Pattern)

## Flyweight란?
**공유를 통해 많은 수의 객체를 효율적으로 관리한다.**

객체의 내부 상태(공유 가능한 불변 데이터)를 분리해 인스턴스를 재사용함으로써 메모리를 절약한다.

---

## 문제 상황 — 대량 상품 목록에서 동일한 카테고리 정보를 객체마다 생성

```java
// 상품 10만 개에 카테고리 정보가 각각 객체로 생성됨
public class Product {
    private Long id;
    private String name;
    private Category category; // 동일한 카테고리인데 매번 new Category()
}

// 카테고리가 "전자제품"인 상품이 5만 개라면?
// → Category 객체 5만 개 = 메모리 낭비
```

---

## 적용 예시

```java
// Flyweight: 공유될 불변 객체
@Getter
@RequiredArgsConstructor
public final class Category {
    private final String code;
    private final String name;
    private final String description;
}

// Flyweight Factory: 동일한 카테고리는 재사용
public class CategoryFactory {
    private static final Map<String, Category> cache = new HashMap<>();

    public static Category get(String code) {
        return cache.computeIfAbsent(code, k -> loadFromDb(k));
    }

    private static Category loadFromDb(String code) {
        // DB에서 최초 1회만 조회
        return categoryRepository.findByCode(code);
    }
}

// 상품 객체는 카테고리 참조만 보유
@Getter
public class Product {
    private Long id;
    private String name;
    private String categoryCode; // 카테고리 객체 대신 코드만 보유

    public Category getCategory() {
        return CategoryFactory.get(this.categoryCode); // 공유 인스턴스 반환
    }
}
```

```java
// 10만 개의 상품이 있어도 카테고리 인스턴스는 실제 카테고리 수만큼만 존재
Product p1 = new Product(1L, "노트북", "ELECTRONICS");
Product p2 = new Product(2L, "스마트폰", "ELECTRONICS");

// 동일한 Category 인스턴스를 공유
p1.getCategory() == p2.getCategory(); // true
```

## Java의 Flyweight 활용 예시

```java
// String pool — 동일한 문자열 리터럴은 하나의 인스턴스를 공유
String a = "hello";
String b = "hello";
a == b; // true (같은 인스턴스)

// Integer 캐시 (-128 ~ 127)
Integer x = Integer.valueOf(100);
Integer y = Integer.valueOf(100);
x == y; // true (캐시된 인스턴스 재사용)
```

---

## 핵심 정리
- 동일하거나 유사한 객체가 대량으로 생성되어 메모리 문제가 생길 때 사용
- **내부 상태(Intrinsic)**: 공유 가능한 불변 데이터 → Flyweight에 저장
- **외부 상태(Extrinsic)**: 상황에 따라 달라지는 데이터 → 클라이언트가 전달
- Java의 `String pool`, `Integer.valueOf()` 캐시가 대표적인 Flyweight 구현
