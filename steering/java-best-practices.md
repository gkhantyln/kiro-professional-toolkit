---
inclusion: fileMatch
fileMatchPattern: "**/*.java"
---

# Java Best Practices — İleri Seviye (Spring Boot 3 / Java 21)

## Virtual Threads (Java 21)

```java
// ✅ Virtual thread executor — yüksek concurrency, düşük bellek
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Result>> futures = tasks.stream()
        .map(task -> executor.submit(() -> process(task)))
        .toList();
    return futures.stream().map(Future::get).toList();
}

// Spring Boot 3.2+ — virtual threads aktif et
// application.properties
// spring.threads.virtual.enabled=true
```

## Records + Sealed Classes

```java
// ✅ Record — immutable DTO
public record CreateOrderRequest(
    @NotBlank String userId,
    @NotEmpty List<@Valid OrderItem> items
) {}

public record OrderItem(
    @NotBlank String productId,
    @Positive int quantity
) {}

// ✅ Sealed class — exhaustive pattern matching
public sealed interface OrderResult
    permits OrderResult.Success, OrderResult.Failure {}

public record Success(Order order) implements OrderResult {}
public record Failure(String reason, ErrorCode code) implements OrderResult {}

// Pattern matching switch (Java 21)
String message = switch (result) {
    case Success(var order) -> "Order created: " + order.id();
    case Failure(var reason, var code) -> "Failed [%s]: %s".formatted(code, reason);
};
```

## Spring Boot 3 — Service Katmanı

```java
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        // Validate stock
        var products = productRepository.findAllById(
            request.items().stream().map(OrderItem::productId).toList()
        );

        if (products.size() != request.items().size()) {
            throw new ProductNotFoundException("One or more products not found");
        }

        var order = Order.create(request.userId(), request.items());
        var saved = orderRepository.save(order);

        // Domain event
        eventPublisher.publishEvent(new OrderCreatedEvent(saved.getId(), saved.getUserId()));
        return saved;
    }

    public Page<Order> findByUser(String userId, Pageable pageable) {
        return orderRepository.findByUserIdOrderByCreatedAtDesc(userId, pageable);
    }
}
```

## Spring Data JPA — Optimizasyon

```java
@Repository
public interface OrderRepository extends JpaRepository<Order, UUID> {

    // ✅ Projection — sadece gerekli alanlar
    @Query("SELECT new com.app.dto.OrderSummary(o.id, o.status, o.totalAmount, o.createdAt) " +
           "FROM Order o WHERE o.userId = :userId")
    Page<OrderSummary> findSummariesByUserId(@Param("userId") String userId, Pageable pageable);

    // ✅ EntityGraph — N+1 önleme
    @EntityGraph(attributePaths = {"items", "items.product"})
    Optional<Order> findWithItemsById(UUID id);

    // ✅ Bulk update — dirty checking bypass
    @Modifying
    @Query("UPDATE Order o SET o.status = :status WHERE o.id IN :ids")
    int bulkUpdateStatus(@Param("ids") List<UUID> ids, @Param("status") OrderStatus status);

    // ✅ Exists check
    boolean existsByUserIdAndStatus(String userId, OrderStatus status);
}
```

## Exception Handling

```java
// ✅ Global exception handler
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ProblemDetail handleValidation(ConstraintViolationException ex) {
        var detail = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "Validation failed");
        detail.setProperty("violations", ex.getConstraintViolations().stream()
            .map(v -> Map.of("field", v.getPropertyPath().toString(), "message", v.getMessage()))
            .toList());
        return detail;
    }

    @ExceptionHandler(ProductNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ProblemDetail handleNotFound(ProductNotFoundException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ProblemDetail handleGeneral(Exception ex) {
        log.error("Unhandled exception", ex);
        return ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected error occurred"
        );
    }
}
```

## Configuration Properties

```java
// ✅ Type-safe config
@ConfigurationProperties(prefix = "app.order")
@Validated
public record OrderProperties(
    @Positive int maxItemsPerOrder,
    @NotNull Duration processingTimeout,
    @NotBlank String defaultCurrency
) {}

// application.yml
// app:
//   order:
//     max-items-per-order: 50
//     processing-timeout: 30s
//     default-currency: USD
```

## Testing

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class OrderServiceIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired OrderService orderService;

    @Test
    void shouldCreateOrderSuccessfully() {
        var request = new CreateOrderRequest("user-1", List.of(new OrderItem("p-1", 2)));
        var order = orderService.createOrder(request);

        assertThat(order.getId()).isNotNull();
        assertThat(order.getStatus()).isEqualTo(OrderStatus.PENDING);
        assertThat(order.getItems()).hasSize(1);
    }
}
```

## Kurallar

- Java 21 features kullan: records, sealed classes, pattern matching, virtual threads
- `@Transactional(readOnly = true)` — read-only metodlarda performans kazanımı
- Projection kullan — entity yerine DTO döndür (N+1 + over-fetching önle)
- `@EntityGraph` ile lazy loading sorunlarını çöz
- `ProblemDetail` (RFC 7807) ile standart hata response'ları
- `@ConfigurationProperties` ile type-safe konfigürasyon
- Testcontainers ile gerçek DB'de integration test
- `var` keyword'ünü okunabilirliği artırdığında kullan
