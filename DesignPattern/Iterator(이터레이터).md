# Design Pattern - Iterator (이터레이터)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Iterator란?
**컬렉션의 내부 구조를 노출하지 않고 순차적으로 요소에 접근하는 방법을 제공한다.**

컬렉션의 종류가 바뀌어도 순회 코드를 바꾸지 않아도 된다.

---

## 문제 상황 — 데이터 소스가 바뀌면 순회 코드도 바뀜

```java
// DB 페이징으로 조회할 때
List<Order> orders = orderRepository.findAll(pageRequest);
for (int i = 0; i < orders.size(); i++) {
    process(orders.get(i));
}

// Redis에서 조회로 바뀌면 → 순회 코드도 바꿔야 함
Set<Order> redisOrders = redisTemplate.opsForSet().members("orders");
Iterator<Order> it = redisOrders.iterator();
while (it.hasNext()) {
    process(it.next());
}
```

---

## 적용 예시 — 대용량 주문 배치 처리

```java
// 이터레이터 인터페이스
public interface OrderIterator {
    boolean hasNext();
    Order next();
}

// DB 페이징 이터레이터 (대용량 처리 시 전체를 메모리에 올리지 않음)
public class DbOrderIterator implements OrderIterator {
    private final OrderRepository repository;
    private int page = 0;
    private final int pageSize = 1000;
    private Queue<Order> buffer = new LinkedList<>();

    public DbOrderIterator(OrderRepository repository) {
        this.repository = repository;
        loadNextPage();
    }

    @Override
    public boolean hasNext() {
        if (buffer.isEmpty()) loadNextPage();
        return !buffer.isEmpty();
    }

    @Override
    public Order next() {
        return buffer.poll();
    }

    private void loadNextPage() {
        List<Order> orders = repository.findAll(PageRequest.of(page++, pageSize)).getContent();
        buffer.addAll(orders);
    }
}

// 배치 처리 서비스 — 이터레이터에만 의존
@Service
@RequiredArgsConstructor
public class OrderBatchService {

    private final OrderRepository orderRepository;

    public void processAllOrders() {
        OrderIterator iterator = new DbOrderIterator(orderRepository);

        while (iterator.hasNext()) {
            Order order = iterator.next();
            processOrder(order);
        }
    }
}
```

## Java의 이터레이터 패턴

```java
// Java Iterable/Iterator가 이미 이터레이터 패턴
List<Order> orders = orderRepository.findAll();
for (Order order : orders) {  // 내부적으로 Iterator 사용
    process(order);
}

// Stream도 이터레이터 패턴 기반
orders.stream()
      .filter(o -> o.getStatus().equals("PENDING"))
      .forEach(this::process);
```

---

## 핵심 정리
- 컬렉션 종류(List, Set, Queue, DB 페이징)에 관계없이 동일한 순회 인터페이스 제공
- 대용량 데이터 배치 처리 시 페이징 이터레이터로 OOM 방지 가능
- Java의 `for-each`, `Stream`, `Cursor` 모두 이터레이터 패턴의 구현
