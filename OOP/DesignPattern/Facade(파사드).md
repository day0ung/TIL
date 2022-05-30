# Design Pattern - Facade (파사드)

## 분류
> 구조 패턴 (Structural Pattern)

## Facade란?
**복잡한 서브시스템에 단순한 인터페이스를 제공한다.**

클라이언트가 내부의 복잡한 구조를 알 필요 없이 파사드 하나만 호출하면 된다.

---

## 문제 상황 — 회원가입 시 여러 서비스를 직접 조합

```java
@RestController
public class UserController {

    @PostMapping("/join")
    public void join(@RequestBody JoinRequest request) {
        // 컨트롤러가 너무 많은 것을 알고 있음
        userValidator.validate(request);
        User user = userRepository.save(new User(request));
        emailService.sendWelcome(user.getEmail());
        couponService.issueWelcomeCoupon(user.getId());
        slackService.notify("#new-user", user.getName() + " 가입");
        analyticsService.track("USER_JOIN", user.getId());
    }
}
```

서비스가 하나 추가될 때마다 컨트롤러를 수정해야 하고, 순서 제어도 어렵다.

---

## 적용 예시

```java
// 파사드: 복잡한 가입 흐름을 하나로 캡슐화
@Service
@RequiredArgsConstructor
public class UserJoinFacade {

    private final UserValidator userValidator;
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final CouponService couponService;
    private final SlackService slackService;
    private final AnalyticsService analyticsService;

    public void join(JoinRequest request) {
        userValidator.validate(request);
        User user = userRepository.save(new User(request));
        emailService.sendWelcome(user.getEmail());
        couponService.issueWelcomeCoupon(user.getId());
        slackService.notify("#new-user", user.getName() + " 가입");
        analyticsService.track("USER_JOIN", user.getId());
    }
}

// 컨트롤러는 파사드만 호출
@RestController
@RequiredArgsConstructor
public class UserController {

    private final UserJoinFacade userJoinFacade;

    @PostMapping("/join")
    public void join(@RequestBody JoinRequest request) {
        userJoinFacade.join(request);
    }
}
```

가입 흐름이 바뀌어도 `UserJoinFacade`만 수정하면 된다.
컨트롤러는 변경이 필요없다.

---

## 핵심 정리
- 여러 서비스를 조합하는 복잡한 흐름을 하나의 클래스로 묶을 때 사용
- 컨트롤러가 비즈니스 로직을 직접 알고 있다면 파사드 도입을 고려
- 실무에서는 `XxxFacade`, `XxxProcessor`, `XxxManager` 네이밍으로 자주 등장
