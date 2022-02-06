# OOP - SOLID : LSP (리스코프 치환 원칙)

## LSP란?
> Liskov Substitution Principle

**자식 클래스는 부모 클래스를 완전히 대체할 수 있어야 한다.**

부모 타입을 사용하는 코드에서 자식 타입으로 바꿔도 동작이 달라지거나 예외가 발생하면 안 된다.
"IS-A" 관계가 현실에서 맞더라도 코드에서는 LSP를 깰 수 있다.

---

## 위반 예시 — 파일 저장소

```java
public class FileStorage {
    public void upload(String filename, byte[] data) {
        // 로컬 파일 시스템에 저장
        Files.write(Paths.get(filename), data);
    }

    public byte[] download(String filename) {
        return Files.readAllBytes(Paths.get(filename));
    }

    public void delete(String filename) {
        Files.delete(Paths.get(filename));
    }
}

// S3는 파일 저장소의 일종? → 맞지만 delete가 문제
public class S3Storage extends FileStorage {
    @Override
    public void upload(String filename, byte[] data) {
        s3Client.putObject(bucket, filename, data);
    }

    @Override
    public byte[] download(String filename) {
        return s3Client.getObject(bucket, filename);
    }

    @Override
    public void delete(String filename) {
        // S3 버킷 정책상 삭제 불가 → LSP 위반
        throw new UnsupportedOperationException("S3에서는 삭제가 허용되지 않습니다.");
    }
}
```

```java
// 사용하는 쪽
FileStorage storage = new S3Storage();
storage.delete("old-file.jpg"); // RuntimeException 발생 → 예상치 못한 장애
```

`FileStorage` 자리에 `S3Storage`를 넣었더니 런타임 예외가 터진다.

---

## 개선 예시 (LSP 적용)

```java
// 공통 능력만 추상화
public interface ReadableStorage {
    byte[] download(String filename);
}

public interface WritableStorage extends ReadableStorage {
    void upload(String filename, byte[] data);
}

public interface DeletableStorage extends WritableStorage {
    void delete(String filename);
}

// 로컬: 삭제 가능
public class LocalStorage implements DeletableStorage {
    @Override
    public void upload(String filename, byte[] data) { /* 로컬 저장 */ }

    @Override
    public byte[] download(String filename) { /* 로컬 읽기 */ return new byte[0]; }

    @Override
    public void delete(String filename) { /* 로컬 삭제 */ }
}

// S3: 삭제 불가하므로 DeletableStorage 구현하지 않음
public class S3Storage implements WritableStorage {
    @Override
    public void upload(String filename, byte[] data) { /* S3 업로드 */ }

    @Override
    public byte[] download(String filename) { /* S3 다운로드 */ return new byte[0]; }
}
```

이제 `S3Storage`를 사용하는 곳에서는 `delete()`를 호출할 수 없어 컴파일 단계에서 막힌다.

---

## 핵심 정리
- 자식 클래스에서 부모 메서드를 `throw new UnsupportedOperationException()`으로 막는다면 LSP 위반
- 상속 전에 "행동이 진짜 호환되는가"를 먼저 따져봐야 함
- 기능 범위에 따라 **인터페이스를 세분화**하면 LSP를 지키기 쉬워짐
