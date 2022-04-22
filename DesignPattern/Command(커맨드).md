# Design Pattern - Command (커맨드)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Command란?
**요청을 객체로 캡슐화하여 요청의 실행, 취소, 재시도, 큐잉을 유연하게 처리할 수 있게 한다.**

"무엇을 해달라"는 요청 자체를 객체로 만들어서 저장하고 전달한다.

---

## 문제 상황 — 쿠폰 발급/취소 이력 관리가 어려움

```java
@Service
public class CouponService {

    public void issueCoupon(Long userId, String couponCode) {
        // 발급 처리
        couponRepository.save(new Coupon(userId, couponCode));
    }

    public void cancelCoupon(Long userId, String couponCode) {
        // 취소 처리
        couponRepository.delete(userId, couponCode);
    }
    // 발급 이력, 취소 이력, 재시도 로직을 어디에 넣어야 할지 불분명
}
```

---

## 적용 예시

```java
// 커맨드 인터페이스
public interface CouponCommand {
    void execute();
    void undo();
}

// 발급 커맨드
@RequiredArgsConstructor
public class IssueCouponCommand implements CouponCommand {
    private final CouponRepository couponRepository;
    private final Long userId;
    private final String couponCode;

    @Override
    public void execute() {
        couponRepository.save(new Coupon(userId, couponCode));
        System.out.println("쿠폰 발급: " + couponCode);
    }

    @Override
    public void undo() {
        couponRepository.delete(userId, couponCode);
        System.out.println("쿠폰 발급 취소: " + couponCode);
    }
}

// 커맨드 실행기 (Invoker) — 이력 관리 담당
@Service
public class CouponCommandInvoker {
    private final Deque<CouponCommand> history = new ArrayDeque<>();

    public void execute(CouponCommand command) {
        command.execute();
        history.push(command);
    }

    public void undoLast() {
        if (!history.isEmpty()) {
            history.pop().undo();
        }
    }
}

// 사용
@Service
@RequiredArgsConstructor
public class CouponService {

    private final CouponCommandInvoker invoker;
    private final CouponRepository couponRepository;

    public void issueCoupon(Long userId, String couponCode) {
        invoker.execute(new IssueCouponCommand(couponRepository, userId, couponCode));
    }

    public void undoLastAction() {
        invoker.undoLast(); // 마지막 작업 되돌리기
    }
}
```

---

## 핵심 정리
- 요청의 실행/취소/재시도/이력이 필요한 경우에 적합
- 실행하는 쪽(Invoker)과 실행되는 쪽(Receiver)을 분리
- 배치 작업 큐, 어드민 되돌리기 기능, 매크로 기록 등에 자주 활용
