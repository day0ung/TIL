# Design Pattern - Prototype (프로토타입)

## 분류
> 생성 패턴 (Creational Pattern)

## Prototype이란?
**기존 객체를 복사(clone)해서 새 객체를 생성한다.**

객체 생성 비용이 클 때, 또는 동일한 설정의 객체를 여러 개 만들어야 할 때 유용하다.

---

## 문제 상황 — 복잡한 초기화가 필요한 객체를 반복 생성

```java
// DB 조회 + 외부 API 호출로 초기화되는 객체
public class ReportTemplate {
    private List<String> columns;
    private Map<String, String> styles;
    private ChartConfig chartConfig;

    public ReportTemplate() {
        // DB에서 기본 컬럼 조회
        this.columns = reportColumnRepository.findDefaults();
        // 외부 스타일 서버에서 불러오기
        this.styles = styleApiClient.fetchDefaultStyles();
        // 차트 기본 설정 로딩
        this.chartConfig = ChartConfig.loadDefault();
    }
}

// 보고서마다 매번 이 과정을 반복 → 느리고 비쌈
ReportTemplate t1 = new ReportTemplate();
ReportTemplate t2 = new ReportTemplate();
```

---

## 적용 예시

```java
@Getter
public class ReportTemplate implements Cloneable {
    private List<String> columns;
    private Map<String, String> styles;
    private String title;

    // 최초 1회만 무거운 초기화
    public ReportTemplate() {
        this.columns = reportColumnRepository.findDefaults();
        this.styles = styleApiClient.fetchDefaultStyles();
        this.title = "기본 보고서";
    }

    // clone으로 복사본 생성 (얕은 복사)
    @Override
    public ReportTemplate clone() {
        try {
            ReportTemplate copy = (ReportTemplate) super.clone();
            copy.columns = new ArrayList<>(this.columns); // 깊은 복사
            copy.styles = new HashMap<>(this.styles);
            return copy;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}

// 사용
ReportTemplate base = new ReportTemplate(); // 최초 1회 초기화

// 이후에는 clone으로 빠르게 복사
ReportTemplate salesReport = base.clone();
salesReport.setTitle("매출 보고서");

ReportTemplate inventoryReport = base.clone();
inventoryReport.setTitle("재고 보고서");
```

## Spring에서의 Prototype Scope

```java
// Spring Bean의 prototype scope도 같은 개념
@Component
@Scope("prototype") // 요청마다 새 인스턴스 생성
public class ReportGenerator {
    // ...
}
```

---

## 핵심 정리
- 객체 초기화 비용이 높고, 동일한 구조의 객체가 여러 개 필요할 때 사용
- 얕은 복사(shallow copy)와 깊은 복사(deep copy)를 구분해서 구현해야 함
- 컬렉션 필드는 반드시 새 컬렉션으로 복사하지 않으면 공유 상태 버그가 발생
