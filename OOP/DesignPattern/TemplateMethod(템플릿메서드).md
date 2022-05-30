# Design Pattern - Template Method (템플릿 메서드)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Template Method란?
**알고리즘의 골격(순서)을 상위 클래스에서 정의하고, 세부 구현은 하위 클래스에서 오버라이드한다.**

공통 흐름은 부모가 제어하고, 달라지는 부분만 자식이 구현한다.

---

## 문제 상황 — 파일 형식별 보고서 생성 로직이 중복

```java
public class ExcelReportGenerator {
    public void generate(String reportId) {
        // 1. 데이터 조회 (동일)
        List<Data> data = reportRepository.findByReportId(reportId);
        // 2. 데이터 검증 (동일)
        validate(data);
        // 3. 엑셀 변환 (다름)
        byte[] excel = convertToExcel(data);
        // 4. 파일 저장 (동일)
        fileStorage.save(reportId + ".xlsx", excel);
    }
}

public class PdfReportGenerator {
    public void generate(String reportId) {
        // 1~2 동일한 코드 중복
        List<Data> data = reportRepository.findByReportId(reportId);
        validate(data);
        // 3. PDF 변환 (다름)
        byte[] pdf = convertToPdf(data);
        // 4 동일한 코드 중복
        fileStorage.save(reportId + ".pdf", pdf);
    }
}
```

---

## 적용 예시

```java
// 템플릿 메서드 정의 (추상 클래스)
public abstract class ReportGenerator {

    // 템플릿 메서드: 알고리즘의 골격 (final로 오버라이드 방지)
    public final void generate(String reportId) {
        List<Data> data = fetchData(reportId);  // 공통
        validate(data);                          // 공통
        byte[] file = convert(data);             // 각자 구현
        String filename = reportId + "." + getExtension(); // 각자 구현
        fileStorage.save(filename, file);        // 공통
    }

    // 공통 로직
    private List<Data> fetchData(String reportId) {
        return reportRepository.findByReportId(reportId);
    }

    private void validate(List<Data> data) {
        if (data.isEmpty()) throw new IllegalStateException("데이터 없음");
    }

    // 하위 클래스가 구현할 부분
    protected abstract byte[] convert(List<Data> data);
    protected abstract String getExtension();
}

// 엑셀 구현체
@Component
public class ExcelReportGenerator extends ReportGenerator {
    @Override
    protected byte[] convert(List<Data> data) {
        return excelConverter.convert(data);
    }

    @Override
    protected String getExtension() { return "xlsx"; }
}

// PDF 구현체
@Component
public class PdfReportGenerator extends ReportGenerator {
    @Override
    protected byte[] convert(List<Data> data) {
        return pdfConverter.convert(data);
    }

    @Override
    protected String getExtension() { return "pdf"; }
}

// CSV 추가 → generate() 로직 재사용, convert()만 구현
@Component
public class CsvReportGenerator extends ReportGenerator {
    @Override
    protected byte[] convert(List<Data> data) {
        return csvConverter.convert(data);
    }

    @Override
    protected String getExtension() { return "csv"; }
}
```

---

## 핵심 정리
- 여러 클래스에서 순서는 같고 일부 단계만 다를 때 적합
- 공통 흐름을 부모가 제어하므로 중복 제거와 일관성 유지에 효과적
- 전략 패턴과 비교: 템플릿 메서드는 **상속**으로, 전략 패턴은 **조합**으로 변화를 처리
