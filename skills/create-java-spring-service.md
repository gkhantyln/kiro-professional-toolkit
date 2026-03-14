# Skill: create-java-spring-service

## Açıklama
Production-grade Java Spring Boot 3 servisi oluşturur. Java 21 virtual threads, Spring Data JPA, Testcontainers stack.

## Kullanım
```
#create-java-spring-service <servis-adı> [--db postgres|mysql|h2] [--auth jwt|oauth2]
```

## Örnekler
```
#create-java-spring-service order-service --db postgres --auth jwt
#create-java-spring-service product-catalog --db postgres
```

## Oluşturulan Yapı
```
src/
├── main/
│   ├── java/com/app/<servis>/
│   │   ├── Application.java
│   │   ├── config/
│   │   │   ├── SecurityConfig.java
│   │   │   └── JpaConfig.java
│   │   ├── domain/
│   │   │   ├── Order.java          # JPA entity
│   │   │   ├── OrderItem.java
│   │   │   └── OrderStatus.java
│   │   ├── dto/
│   │   │   ├── CreateOrderRequest.java   # record
│   │   │   └── OrderResponse.java        # record
│   │   ├── repository/
│   │   │   └── OrderRepository.java
│   │   ├── service/
│   │   │   └── OrderService.java
│   │   ├── controller/
│   │   │   └── OrderController.java
│   │   └── exception/
│   │       └── GlobalExceptionHandler.java
│   └── resources/
│       ├── application.yml
│       ├── application-prod.yml
│       └── db/migration/
│           └── V1__create_orders.sql
└── test/
    └── java/com/app/<servis>/
        ├── integration/
        │   └── OrderServiceIT.java
        └── unit/
            └── OrderServiceTest.java
```

## Üretilen Kod Özellikleri

### pom.xml (Spring Boot 3.3 + Java 21)
```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.3.0</version>
</parent>

<properties>
  <java.version>21</java.version>
</properties>

<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
  </dependency>
  <dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
  </dependency>
  <dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
  </dependency>
  <!-- Test -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-testcontainers</artifactId>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

### application.yml
```yaml
spring:
  threads:
    virtual:
      enabled: true  # Java 21 virtual threads
  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/appdb}
    username: ${DB_USER:app}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      connection-timeout: 3000
  jpa:
    open-in-view: false  # N+1 önleme
    properties:
      hibernate:
        default_batch_fetch_size: 100
  flyway:
    enabled: true
    locations: classpath:db/migration

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
```

### OrderController.java
```java
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
@Validated
public class OrderController {

    private final OrderService orderService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse create(
        @Valid @RequestBody CreateOrderRequest request,
        @AuthenticationPrincipal UserDetails user
    ) {
        return OrderResponse.from(orderService.createOrder(user.getUsername(), request));
    }

    @GetMapping
    public Page<OrderSummary> list(
        @AuthenticationPrincipal UserDetails user,
        @PageableDefault(size = 20, sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable
    ) {
        return orderService.findByUser(user.getUsername(), pageable);
    }

    @GetMapping("/{id}")
    public OrderResponse get(@PathVariable UUID id, @AuthenticationPrincipal UserDetails user) {
        return OrderResponse.from(orderService.findById(id, user.getUsername()));
    }
}
```

## Özellikler
- Java 21 virtual threads (`spring.threads.virtual.enabled=true`)
- Spring Boot 3.3 + Spring Security 6
- Flyway database migrations
- Testcontainers ile integration tests
- `open-in-view: false` — N+1 önleme
- Hibernate batch fetching
- RFC 7807 ProblemDetail hata response'ları
- Actuator + Prometheus metrics
- Records ile immutable DTO'lar
