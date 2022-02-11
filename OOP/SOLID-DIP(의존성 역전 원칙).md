# OOP - SOLID : DIP (의존성 역전 원칙)

## DIP란?
> Dependency Inversion Principle

**고수준 모듈은 저수준 모듈에 의존해서는 안 된다. 둘 다 추상화에 의존해야 한다.**

비즈니스 로직(고수준)이 DB, 외부 API 등 세부 구현(저수준)에 직접 의존하면
구현이 바뀔 때마다 비즈니스 로직을 수정해야 한다.

---

## 위반 예시 — 회원 조회 서비스

```java
// 저수준: JPA 레포지토리 구현체
public class UserJpaRepository {
    @PersistenceContext
    private EntityManager em;

    public User findById(Long id) {
        return em.find(User.class, id);
    }
}

// 고수준: 비즈니스 로직이 JPA 구현체에 직접 의존
@Service
public class UserService {

    private final UserJpaRepository userJpaRepository; // 구체 클래스에 직접 의존 → DIP 위반

    public UserService() {
        this.userJpaRepository = new UserJpaRepository(); // 강결합
    }

    public UserDto getUser(Long id) {
        User user = userJpaRepository.findById(id);
        return new UserDto(user);
    }
}
```

나중에 MyBatis나 QueryDSL로 바꾸거나 캐시 레이어를 끼우려면 `UserService` 자체를 수정해야 한다.
테스트 시 실제 DB 없이는 `UserService` 단독 테스트가 불가능하다.

---

## 개선 예시 (DIP 적용)

```java
// 추상화: 레포지토리 인터페이스 (고수준이 의존하는 대상)
public interface UserRepository {
    User findById(Long id);
    void save(User user);
}

// 저수준 구현체 1: JPA
@Repository
public class UserJpaRepository implements UserRepository {
    private final JpaUserRepository jpa; // Spring Data JPA

    @Override
    public User findById(Long id) {
        return jpa.findById(id).orElseThrow(() -> new EntityNotFoundException("유저 없음"));
    }

    @Override
    public void save(User user) {
        jpa.save(user);
    }
}

// 저수준 구현체 2: Redis 캐시 (나중에 추가해도 UserService 수정 불필요)
@Repository
@Primary
public class CachedUserRepository implements UserRepository {
    private final UserJpaRepository jpaRepository;
    private final RedisTemplate<String, User> redisTemplate;

    @Override
    public User findById(Long id) {
        String key = "user:" + id;
        User cached = redisTemplate.opsForValue().get(key);
        if (cached != null) return cached;

        User user = jpaRepository.findById(id);
        redisTemplate.opsForValue().set(key, user, Duration.ofMinutes(10));
        return user;
    }

    @Override
    public void save(User user) {
        jpaRepository.save(user);
        redisTemplate.delete("user:" + user.getId()); // 캐시 무효화
    }
}

// 고수준: 인터페이스에만 의존 → 구현체가 바뀌어도 UserService는 수정 불필요
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository; // 인터페이스에 의존

    public UserDto getUser(Long id) {
        User user = userRepository.findById(id);
        return new UserDto(user);
    }
}
```

```java
// 테스트 시 Mock으로 대체 가능
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository; // 인터페이스이므로 Mock 가능

    @InjectMocks
    private UserService userService;

    @Test
    void 유저_조회_성공() {
        given(userRepository.findById(1L)).willReturn(new User(1L, "홍길동"));
        UserDto dto = userService.getUser(1L);
        assertThat(dto.getName()).isEqualTo("홍길동");
    }
}
```

DB 없이도 `UserService` 단독 테스트가 가능해진다.

---

## 핵심 정리
- **고수준**: 비즈니스 로직 (Service, UseCase)
- **저수준**: 세부 구현 (Repository, 외부 API 클라이언트, 메시지 큐 등)
- Spring의 `@Autowired`가 DIP를 기반으로 동작하는 이유가 바로 이것
- DIP를 지키면 **테스트 용이성**과 **교체 가능성**이 동시에 올라감
