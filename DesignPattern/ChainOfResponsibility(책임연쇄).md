# Design Pattern - Chain of Responsibility (책임 연쇄)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Chain of Responsibility란?
**요청을 처리할 수 있는 핸들러를 체인으로 연결하고, 요청이 처리될 때까지 다음 핸들러로 전달한다.**

요청의 발신자와 수신자를 분리하고, 처리 순서를 유연하게 조합할 수 있다.

---

## 문제 상황 — API 요청 검증 로직이 뒤섞임

```java
@PostMapping("/orders")
public ResponseEntity<?> createOrder(@RequestBody OrderRequest request) {
    // 인증 체크
    if (!tokenValidator.isValid(request.getToken())) {
        return ResponseEntity.status(401).build();
    }
    // 요청 데이터 검증
    if (request.getAmount() <= 0) {
        return ResponseEntity.badRequest().body("금액 오류");
    }
    // 권한 체크
    if (!authorizationChecker.hasPermission(request.getUserId(), "ORDER")) {
        return ResponseEntity.status(403).build();
    }
    // 실제 로직
    orderService.create(request);
    return ResponseEntity.ok().build();
}
```

---

## 적용 예시

```java
// 핸들러 인터페이스
public abstract class OrderRequestHandler {
    protected OrderRequestHandler next;

    public OrderRequestHandler setNext(OrderRequestHandler next) {
        this.next = next;
        return next;
    }

    public abstract void handle(OrderRequest request);

    protected void passToNext(OrderRequest request) {
        if (next != null) next.handle(request);
    }
}

// 인증 핸들러
@Component
public class AuthenticationHandler extends OrderRequestHandler {
    @Override
    public void handle(OrderRequest request) {
        if (!tokenValidator.isValid(request.getToken())) {
            throw new UnauthorizedException("인증 실패");
        }
        System.out.println("인증 통과");
        passToNext(request);
    }
}

// 데이터 검증 핸들러
@Component
public class ValidationHandler extends OrderRequestHandler {
    @Override
    public void handle(OrderRequest request) {
        if (request.getAmount() <= 0) {
            throw new IllegalArgumentException("금액 오류");
        }
        System.out.println("검증 통과");
        passToNext(request);
    }
}

// 권한 핸들러
@Component
public class AuthorizationHandler extends OrderRequestHandler {
    @Override
    public void handle(OrderRequest request) {
        if (!authorizationChecker.hasPermission(request.getUserId(), "ORDER")) {
            throw new ForbiddenException("권한 없음");
        }
        System.out.println("권한 통과");
        passToNext(request);
    }
}

// 체인 조립 및 사용
@Configuration
public class HandlerChainConfig {
    @Bean
    public OrderRequestHandler orderHandlerChain(
            AuthenticationHandler auth,
            ValidationHandler validation,
            AuthorizationHandler authorization) {

        auth.setNext(validation).setNext(authorization);
        return auth; // 체인의 시작
    }
}

@RestController
@RequiredArgsConstructor
public class OrderController {
    private final OrderRequestHandler orderHandlerChain;
    private final OrderService orderService;

    @PostMapping("/orders")
    public ResponseEntity<?> createOrder(@RequestBody OrderRequest request) {
        orderHandlerChain.handle(request); // 체인 실행
        orderService.create(request);
        return ResponseEntity.ok().build();
    }
}
```

---

## 핵심 정리
- Spring Security의 필터 체인이 책임 연쇄 패턴의 대표적인 구현
- 핸들러 추가/제거/순서 변경이 체인 조립만으로 가능
- 검증, 인증, 로깅 등 순차적으로 처리해야 하는 미들웨어 구성에 적합
