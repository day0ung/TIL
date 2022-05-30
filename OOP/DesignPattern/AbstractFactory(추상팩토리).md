# Design Pattern - Abstract Factory (추상 팩토리)

## 분류
> 생성 패턴 (Creational Pattern)

## Abstract Factory란?
**관련 있는 객체들의 집합을 생성하는 인터페이스를 제공하고, 구체적인 클래스를 지정하지 않는다.**

팩토리 메서드가 하나의 객체를 만든다면, 추상 팩토리는 연관된 객체 군(family)을 함께 생성한다.

---

## 문제 상황 — 환경별로 다른 인프라 객체를 사용해야 할 때

로컬 개발 환경에서는 인메모리 DB와 콘솔 메일을 쓰고,
운영 환경에서는 MySQL과 실제 SMTP 서버를 써야 한다.

```java
// 환경마다 직접 분기 → 코드 전체에 퍼짐
if (profile.equals("local")) {
    db = new H2Database();
    mailer = new FakeMailer();
} else {
    db = new MySQLDatabase();
    mailer = new SmtpMailer();
}
```

---

## 적용 예시

```java
// 추상 팩토리
public interface InfraFactory {
    Database createDatabase();
    Mailer createMailer();
}

// 로컬용 팩토리
public class LocalInfraFactory implements InfraFactory {
    @Override
    public Database createDatabase() { return new H2Database(); }

    @Override
    public Mailer createMailer() { return new FakeMailer(); }
}

// 운영용 팩토리
public class ProdInfraFactory implements InfraFactory {
    @Override
    public Database createDatabase() { return new MySQLDatabase(); }

    @Override
    public Mailer createMailer() { return new SmtpMailer(); }
}

// 클라이언트는 팩토리에만 의존
@Service
@RequiredArgsConstructor
public class AppInitializer {
    private final InfraFactory infraFactory;

    public void init() {
        Database db = infraFactory.createDatabase();
        Mailer mailer = infraFactory.createMailer();
        db.connect();
        mailer.ready();
    }
}
```

```java
// Spring에서 프로파일로 팩토리 주입
@Configuration
@Profile("local")
public class LocalConfig {
    @Bean
    public InfraFactory infraFactory() { return new LocalInfraFactory(); }
}

@Configuration
@Profile("prod")
public class ProdConfig {
    @Bean
    public InfraFactory infraFactory() { return new ProdInfraFactory(); }
}
```

---

## 핵심 정리
- 함께 사용해야 하는 객체들의 조합이 환경/플랫폼마다 달라질 때 적합
- 팩토리 메서드: 하나의 객체 생성 / 추상 팩토리: 연관된 객체 군 생성
- Spring `@Profile` + `@Configuration` 조합이 추상 팩토리와 동일한 역할
