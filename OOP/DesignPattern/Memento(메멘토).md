# Design Pattern - Memento (메멘토)

## 분류
> 행동 패턴 (Behavioral Pattern)

## Memento란?
**객체의 내부 상태를 저장했다가 나중에 그 상태로 되돌릴 수 있게 한다.**

캡슐화를 깨뜨리지 않으면서 객체의 스냅샷을 찍어 복원할 수 있다.

---

## 문제 상황 — 어드민에서 설정 변경 후 되돌리기 기능이 없음

```java
@Service
public class SiteConfigService {

    public void updateConfig(SiteConfig newConfig) {
        // 변경 전 상태를 저장하는 로직이 없음
        configRepository.save(newConfig);
        // 잘못 변경했을 때 되돌릴 방법이 없음
    }
}
```

---

## 적용 예시

```java
// 메멘토: 저장할 상태 스냅샷
@Getter
@RequiredArgsConstructor
public class SiteConfigMemento {
    private final String maintenanceMessage;
    private final boolean isMaintenanceMode;
    private final int maxConcurrentUsers;
    private final LocalDateTime savedAt;
}

// 원본 객체: 메멘토 생성/복원
@Entity
@Getter
public class SiteConfig {
    private String maintenanceMessage;
    private boolean isMaintenanceMode;
    private int maxConcurrentUsers;

    // 현재 상태 저장
    public SiteConfigMemento save() {
        return new SiteConfigMemento(
            maintenanceMessage,
            isMaintenanceMode,
            maxConcurrentUsers,
            LocalDateTime.now()
        );
    }

    // 이전 상태로 복원
    public void restore(SiteConfigMemento memento) {
        this.maintenanceMessage = memento.getMaintenanceMessage();
        this.isMaintenanceMode = memento.isMaintenanceMode();
        this.maxConcurrentUsers = memento.getMaxConcurrentUsers();
    }
}

// 관리자(Caretaker): 메멘토를 보관
@Service
@RequiredArgsConstructor
public class SiteConfigService {

    private final SiteConfigRepository configRepository;
    private final Deque<SiteConfigMemento> history = new ArrayDeque<>();

    public void updateConfig(SiteConfig newConfig) {
        SiteConfig current = configRepository.findCurrent();
        history.push(current.save()); // 변경 전 상태 저장
        configRepository.save(newConfig);
    }

    public void rollback() {
        if (history.isEmpty()) throw new IllegalStateException("되돌릴 이력 없음");
        SiteConfig current = configRepository.findCurrent();
        current.restore(history.pop()); // 이전 상태로 복원
        configRepository.save(current);
    }
}
```

```java
// 사용
siteConfigService.updateConfig(newConfig);  // 변경
siteConfigService.rollback();               // 되돌리기
```

---

## 핵심 정리
- Undo/Redo, 되돌리기, 임시저장 기능이 필요할 때 적합
- 원본 객체의 캡슐화를 유지하면서 상태를 외부에 저장
- 어드민 설정, 문서 편집기, 게임 세이브 포인트 등에서 활용
