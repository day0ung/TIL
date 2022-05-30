# OOP

객체지향 프로그래밍(Object-Oriented Programming)의 핵심 원칙과 설계 패턴을 정리한 내용이다.

---

## SOLID 원칙

객체지향 설계의 5가지 기본 원칙으로, 유지보수하기 좋고 확장 가능한 소프트웨어를 만들기 위한 가이드라인이다.

| 원칙 | 이름 | 핵심 |
|------|------|------|
| [SRP](./SOLID-SRP(단일%20책임%20원칙).md) | Single Responsibility Principle | 하나의 클래스는 하나의 책임만 가진다 |
| [OCP](./SOLID-OCP(개방-폐쇄%20원칙).md) | Open/Closed Principle | 확장에는 열려 있고, 수정에는 닫혀 있어야 한다 |
| [LSP](./SOLID-LSP(리스코프%20치환%20원칙).md) | Liskov Substitution Principle | 자식 클래스는 부모 클래스를 완전히 대체할 수 있어야 한다 |
| [ISP](./SOLID-ISP(인터페이스%20분리%20원칙).md) | Interface Segregation Principle | 사용하지 않는 메서드에 의존하도록 강요받으면 안 된다 |
| [DIP](./SOLID-DIP(의존성%20역전%20원칙).md) | Dependency Inversion Principle | 고수준 모듈은 저수준 모듈에 의존해서는 안 된다 |

---

## Design Pattern

GoF(Gang of Four)의 23가지 디자인 패턴. 반복적으로 발생하는 설계 문제를 해결하기 위한 검증된 솔루션으로, 생성/구조/행동 3가지로 분류된다.

### 생성 패턴 (Creational Pattern)
> 객체 생성 방식을 다루는 패턴. 객체를 어떻게, 누가 만들지를 캡슐화한다.

| 패턴 | 설명 |
|------|------|
| [Singleton (싱글톤)](./DesignPattern/Singleton(싱글톤).md) | 클래스의 인스턴스를 오직 하나만 생성하고 전역에서 접근 |
| [Factory Method (팩토리 메서드)](./DesignPattern/FactoryMethod(팩토리메서드).md) | 객체 생성을 서브클래스에 위임 |
| [Abstract Factory (추상 팩토리)](./DesignPattern/AbstractFactory(추상팩토리).md) | 관련 객체 군을 생성하는 인터페이스 제공 |
| [Builder (빌더)](./DesignPattern/Builder(빌더).md) | 복잡한 객체를 단계적으로 생성 |
| [Prototype (프로토타입)](./DesignPattern/Prototype(프로토타입).md) | 기존 객체를 복사해서 새 객체를 생성 |

### 구조 패턴 (Structural Pattern)
> 클래스나 객체를 조합해 더 큰 구조를 만드는 패턴.

| 패턴 | 설명 |
|------|------|
| [Adapter (어댑터)](./DesignPattern/Adapter(어댑터).md) | 호환되지 않는 인터페이스를 연결 |
| [Bridge (브릿지)](./DesignPattern/Bridge(브릿지).md) | 구현부와 추상부를 분리해 독립적으로 확장 |
| [Composite (컴포지트)](./DesignPattern/Composite(컴포지트).md) | 객체를 트리 구조로 구성해 단일/복합 객체를 동일하게 처리 |
| [Decorator (데코레이터)](./DesignPattern/Decorator(데코레이터).md) | 객체에 동적으로 기능을 추가 |
| [Facade (파사드)](./DesignPattern/Facade(파사드).md) | 복잡한 서브시스템에 단순한 인터페이스를 제공 |
| [Flyweight (플라이웨이트)](./DesignPattern/Flyweight(플라이웨이트).md) | 공유를 통해 많은 수의 객체를 효율적으로 관리 |
| [Proxy (프록시)](./DesignPattern/Proxy(프록시).md) | 다른 객체에 대한 접근을 제어하는 대리자 |

### 행동 패턴 (Behavioral Pattern)
> 객체 간의 상호작용과 책임 분배를 다루는 패턴.

| 패턴 | 설명 |
|------|------|
| [Chain of Responsibility (책임 연쇄)](./DesignPattern/ChainOfResponsibility(책임연쇄).md) | 요청을 처리할 수 있는 객체를 체인으로 연결 |
| [Command (커맨드)](./DesignPattern/Command(커맨드).md) | 요청을 객체로 캡슐화해 실행/취소 처리 |
| [Iterator (이터레이터)](./DesignPattern/Iterator(이터레이터).md) | 컬렉션 내부 구조를 노출하지 않고 순회 |
| [Mediator (미디에이터)](./DesignPattern/Mediator(미디에이터).md) | 객체 간 통신을 중재자를 통해 처리 |
| [Memento (메멘토)](./DesignPattern/Memento(메멘토).md) | 객체의 상태를 저장하고 복원 |
| [Observer (옵저버)](./DesignPattern/Observer(옵저버).md) | 상태 변화를 구독자에게 자동으로 전달 |
| [State (스테이트)](./DesignPattern/State(스테이트).md) | 상태에 따라 객체의 행동을 변경 |
| [Strategy (전략)](./DesignPattern/Strategy(전략).md) | 알고리즘을 캡슐화하고 교체 가능하게 구성 |
| [Template Method (템플릿 메서드)](./DesignPattern/TemplateMethod(템플릿메서드).md) | 알고리즘 골격을 정의하고 세부 단계를 서브클래스에 위임 |
| [Visitor (비지터)](./DesignPattern/Visitor(비지터).md) | 객체 구조를 변경하지 않고 새로운 연산을 추가 |
