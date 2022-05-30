# Design Pattern - Proxy (프록시)

## 분류
> 구조 패턴 (Structural Pattern)

## Proxy란?
**다른 객체에 대한 접근을 제어하는 대리자 역할을 한다.**

실제 객체 대신 프록시가 앞에 서서 접근 제어, 캐싱, 지연 초기화, 로깅 등을 처리한다.

---

## 문제 상황 — 무거운 외부 API를 매번 호출

```java
@Service
public class ExchangeRateService {

    public BigDecimal getRate(String currency) {
        // 외부 환율 API 호출 — 느리고 과금됨
        return externalApiClient.fetchRate(currency);
    }
}

// 동일한 환율을 여러 번 조회해도 매번 API 호출 발생
BigDecimal rate1 = exchangeRateService.getRate("USD"); // API 호출
BigDecimal rate2 = exchangeRateService.getRate("USD"); // 또 API 호출
```

---

## 적용 예시 — 캐싱 프록시

```java
public interface ExchangeRateService {
    BigDecimal getRate(String currency);
}

// 실제 구현체
@Service("realExchangeRateService")
public class RealExchangeRateService implements ExchangeRateService {
    @Override
    public BigDecimal getRate(String currency) {
        return externalApiClient.fetchRate(currency);
    }
}

// 캐싱 프록시
@Service
@Primary
@RequiredArgsConstructor
public class CachedExchangeRateService implements ExchangeRateService {

    private final RealExchangeRateService realService;
    private final Map<String, BigDecimal> cache = new ConcurrentHashMap<>();
    private final Map<String, LocalDateTime> cacheTime = new ConcurrentHashMap<>();

    @Override
    public BigDecimal getRate(String currency) {
        LocalDateTime lastCached = cacheTime.get(currency);
        // 캐시가 있고 5분 이내라면 캐시 반환
        if (lastCached != null && lastCached.plusMinutes(5).isAfter(LocalDateTime.now())) {
            return cache.get(currency);
        }
        // 아니면 실제 API 호출 후 캐시
        BigDecimal rate = realService.getRate(currency);
        cache.put(currency, rate);
        cacheTime.put(currency, LocalDateTime.now());
        return rate;
    }
}
```

## Spring AOP 기반 프록시 (@Transactional, @Cacheable)

```java
@Service
public class ProductService {

    @Cacheable(value = "products", key = "#id")
    public Product getProduct(Long id) {
        // 최초 1회만 DB 조회, 이후는 캐시에서 반환
        return productRepository.findById(id).orElseThrow();
    }

    @Transactional
    public void updateStock(Long id, int quantity) {
        // Spring이 트랜잭션 프록시를 생성해 begin/commit/rollback 처리
        Product product = productRepository.findById(id).orElseThrow();
        product.updateStock(quantity);
    }
}
```

`@Transactional`과 `@Cacheable`은 Spring이 내부적으로 프록시 객체를 생성해서 동작한다.

---

## 핵심 정리
- 실제 객체를 감싸서 접근을 제어할 때 사용 (캐시, 인증, 로깅, 지연 로딩)
- 클라이언트는 프록시와 실제 객체를 구분하지 않고 동일한 인터페이스로 사용
- Spring의 `@Transactional`, `@Cacheable`, AOP가 모두 프록시 패턴 기반
