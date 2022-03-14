# Design Pattern - Singleton (싱글톤)

## 분류
> 생성 패턴 (Creational Pattern)

## Singleton이란?
**클래스의 인스턴스를 오직 하나만 생성하고, 어디서든 그 인스턴스에 접근할 수 있도록 한다.**

애플리케이션 전역에서 공유해야 하는 자원(설정, 커넥션 풀 등)에 주로 사용된다.

---

## 위반 예시 — 설정 클래스를 매번 new로 생성

```java
public class AppConfig {
    private String dbUrl;
    private int maxPoolSize;

    public AppConfig() {
        // 매번 파일/환경변수를 읽어서 초기화 → 비용 낭비
        this.dbUrl = System.getenv("DB_URL");
        this.maxPoolSize = Integer.parseInt(System.getenv("MAX_POOL_SIZE"));
    }
}

// 사용할 때마다 새 인스턴스 생성 → 불일치 위험
AppConfig config1 = new AppConfig();
AppConfig config2 = new AppConfig(); // config1 != config2
```

---

## 적용 예시

```java
public class AppConfig {
    private static AppConfig instance;
    private String dbUrl;
    private int maxPoolSize;

    private AppConfig() {
        this.dbUrl = System.getenv("DB_URL");
        this.maxPoolSize = Integer.parseInt(System.getenv("MAX_POOL_SIZE"));
    }

    // Thread-safe 싱글톤
    public static synchronized AppConfig getInstance() {
        if (instance == null) {
            instance = new AppConfig();
        }
        return instance;
    }

    public String getDbUrl() { return dbUrl; }
    public int getMaxPoolSize() { return maxPoolSize; }
}

// 사용
AppConfig config = AppConfig.getInstance();
```

## Spring에서의 싱글톤

Spring Bean은 기본적으로 싱글톤으로 관리된다.

```java
@Component
public class AppConfig {
    @Value("${db.url}")
    private String dbUrl;

    @Value("${db.max-pool-size}")
    private int maxPoolSize;
}

// Spring이 알아서 하나의 인스턴스만 생성하고 주입해줌
@Service
@RequiredArgsConstructor
public class UserService {
    private final AppConfig appConfig; // 항상 동일한 인스턴스
}
```

---

## 핵심 정리
- 인스턴스를 하나만 유지해야 하는 경우에 사용
- 멀티스레드 환경에서는 `synchronized` 또는 `Enum` 방식으로 안전하게 구현
- Spring 환경에서는 `@Component`, `@Service` 등 Bean으로 등록하면 자동으로 싱글톤 적용
