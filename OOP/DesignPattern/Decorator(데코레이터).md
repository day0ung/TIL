# Design Pattern - Decorator (데코레이터)

## 분류
> 구조 패턴 (Structural Pattern)

## Decorator란?
**객체에 동적으로 새로운 기능을 추가한다. 서브클래싱 없이 기능을 유연하게 확장할 수 있다.**

기존 객체를 감싸서(Wrapping) 추가 동작을 끼워넣는 방식으로 동작한다.

---

## 문제 상황 — 로깅/인증을 서비스마다 중복 코드로 처리

```java
@Service
public class OrderService {
    public Order getOrder(Long id) {
        // 인증 체크
        if (!SecurityContext.isAuthenticated()) throw new UnauthorizedException();
        // 로깅
        log.info("getOrder 호출: id={}", id);

        return orderRepository.findById(id);
    }
}

@Service
public class UserService {
    public User getUser(Long id) {
        // 똑같은 인증 체크 반복
        if (!SecurityContext.isAuthenticated()) throw new UnauthorizedException();
        // 똑같은 로깅 반복
        log.info("getUser 호출: id={}", id);

        return userRepository.findById(id);
    }
}
```

---

## 적용 예시

```java
// 기본 인터페이스
public interface DataService {
    String getData(String key);
}

// 기본 구현체
public class BasicDataService implements DataService {
    @Override
    public String getData(String key) {
        return "data:" + key;
    }
}

// 로깅 데코레이터
public class LoggingDataService implements DataService {
    private final DataService delegate;

    public LoggingDataService(DataService delegate) {
        this.delegate = delegate;
    }

    @Override
    public String getData(String key) {
        log.info("getData 호출: key={}", key);
        String result = delegate.getData(key);
        log.info("getData 결과: {}", result);
        return result;
    }
}

// 캐시 데코레이터
public class CachingDataService implements DataService {
    private final DataService delegate;
    private final Map<String, String> cache = new HashMap<>();

    public CachingDataService(DataService delegate) {
        this.delegate = delegate;
    }

    @Override
    public String getData(String key) {
        return cache.computeIfAbsent(key, delegate::getData);
    }
}
```

```java
// 데코레이터 조합: 캐시 → 로깅 → 기본
DataService service = new LoggingDataService(
                        new CachingDataService(
                          new BasicDataService()));

service.getData("user-1");
```

## Spring AOP가 데코레이터 패턴의 대표 구현

```java
// Spring AOP로 로깅/인증을 횡단 관심사로 분리
@Aspect
@Component
public class LoggingAspect {
    @Around("@annotation(Loggable)")
    public Object log(ProceedingJoinPoint pjp) throws Throwable {
        log.info("메서드 시작: {}", pjp.getSignature().getName());
        Object result = pjp.proceed();
        log.info("메서드 종료");
        return result;
    }
}
```

---

## 핵심 정리
- 상속 없이 기능을 동적으로 추가할 때 사용
- 여러 데코레이터를 조합해 기능을 레이어별로 쌓을 수 있음
- Spring AOP(`@Around`, `@Before`)가 데코레이터 패턴을 프레임워크 수준에서 구현한 것
