# OOP

객체지향 프로그래밍(Object-Oriented Programming)의 핵심 원칙과 설계 패턴을 정리한 내용이다.

---

## SOLID 원칙

객체지향 설계의 5가지 기본 원칙으로, 유지보수하기 좋고 확장 가능한 소프트웨어를 만들기 위한 가이드라인이다.

| 원칙 | 이름 | 핵심 |
|------|------|------|
| [S](./SOLID-SRP(단일%20책임%20원칙).md) | Single Responsibility Principle | 하나의 클래스는 하나의 책임만 가진다 |
| [O](./SOLID-OCP(개방-폐쇄%20원칙).md) | Open/Closed Principle | 확장에는 열려 있고, 수정에는 닫혀 있어야 한다 |
| [L](./SOLID-LSP(리스코프%20치환%20원칙).md) | Liskov Substitution Principle | 자식 클래스는 부모 클래스를 완전히 대체할 수 있어야 한다 |
| [I](./SOLID-ISP(인터페이스%20분리%20원칙).md) | Interface Segregation Principle | 사용하지 않는 메서드에 의존하도록 강요받으면 안 된다 |
| [D](./SOLID-DIP(의존성%20역전%20원칙).md) | Dependency Inversion Principle | 고수준 모듈은 저수준 모듈에 의존해서는 안 된다 |

---

## Design Pattern

GoF(Gang of Four)의 23가지 디자인 패턴. 반복적으로 발생하는 설계 문제를 해결하기 위한 검증된 솔루션이다.

→ [Design Pattern 목차 보기](./DesignPattern/README.md)
