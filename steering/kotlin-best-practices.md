---
inclusion: fileMatch
fileMatchPattern: "**/*.kt"
---

# Kotlin Best Practices — İleri Seviye (Kotlin 2.0 / KMP)

## Coroutines — Structured Concurrency

```kotlin
// ✅ SupervisorScope — bir child fail olunca diğerleri etkilenmesin
suspend fun fetchDashboard(userId: String): Dashboard = supervisorScope {
    val orders = async { orderService.getOrders(userId) }
    val profile = async { userService.getProfile(userId) }
    val notifications = async {
        try { notificationService.getUnread(userId) }
        catch (e: Exception) { emptyList() }  // graceful degradation
    }
    Dashboard(
        orders = orders.await(),
        profile = profile.await(),
        notifications = notifications.await()
    )
}

// ✅ Flow — reactive stream
fun orderUpdates(userId: String): Flow<Order> = flow {
    while (currentCoroutineContext().isActive) {
        val orders = orderRepo.getRecentOrders(userId)
        orders.forEach { emit(it) }
        delay(5_000)
    }
}.flowOn(Dispatchers.IO)
 .catch { e -> log.error("Flow error", e) }
 .retryWhen { cause, attempt -> attempt < 3 && cause is IOException }
```

## Sealed Classes + Result

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable, val message: String) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}

// Extension functions
inline fun <T, R> Result<T>.map(transform: (T) -> R): Result<R> = when (this) {
    is Result.Success -> Result.Success(transform(data))
    is Result.Error -> this
    is Result.Loading -> this
}

suspend fun createOrder(request: CreateOrderRequest): Result<Order> = runCatching {
    orderRepo.save(Order.from(request))
}.fold(
    onSuccess = { Result.Success(it) },
    onFailure = { Result.Error(it, it.message ?: "Unknown error") }
)
```

## Data Classes + Value Classes

```kotlin
// ✅ Value class — zero-cost wrapper, type safety
@JvmInline
value class UserId(val value: String) {
    init { require(value.isNotBlank()) { "UserId cannot be blank" } }
}

@JvmInline
value class Money(val cents: Long) {
    operator fun plus(other: Money) = Money(cents + other.cents)
    fun toDecimal() = cents.toBigDecimal().movePointLeft(2)
}

// ✅ Data class — copy, equals, hashCode otomatik
data class Order(
    val id: UUID = UUID.randomUUID(),
    val userId: UserId,
    val items: List<OrderItem>,
    val status: OrderStatus = OrderStatus.PENDING,
    val createdAt: Instant = Instant.now()
) {
    val total: Money get() = items.fold(Money(0)) { acc, item -> acc + item.subtotal }
}
```

## Extension Functions

```kotlin
// ✅ Extension — mevcut sınıfları genişlet
fun String.toSlug(): String = lowercase()
    .replace(Regex("[^a-z0-9\\s-]"), "")
    .replace(Regex("\\s+"), "-")
    .trim('-')

fun <T> List<T>.chunkedParallel(size: Int, block: suspend (List<T>) -> Unit) = runBlocking {
    chunked(size).map { chunk ->
        async(Dispatchers.IO) { block(chunk) }
    }.awaitAll()
}

// ✅ Scope functions
val order = orderRepo.findById(id)
    ?.also { log.info("Found order: ${it.id}") }
    ?.takeIf { it.status == OrderStatus.PENDING }
    ?: throw OrderNotFoundException(id)
```

## Kotlin Multiplatform (KMP)

```kotlin
// commonMain — shared logic
expect class PlatformStorage {
    fun save(key: String, value: String)
    fun load(key: String): String?
}

// androidMain
actual class PlatformStorage {
    actual fun save(key: String, value: String) {
        sharedPrefs.edit().putString(key, value).apply()
    }
    actual fun load(key: String): String? = sharedPrefs.getString(key, null)
}

// iosMain
actual class PlatformStorage {
    actual fun save(key: String, value: String) {
        NSUserDefaults.standardUserDefaults.setObject(value, key)
    }
    actual fun load(key: String): String? =
        NSUserDefaults.standardUserDefaults.stringForKey(key)
}
```

## Spring Boot + Kotlin

```kotlin
@RestController
@RequestMapping("/api/v1/orders")
class OrderController(private val orderService: OrderService) {

    @PostMapping
    suspend fun create(
        @Valid @RequestBody request: CreateOrderRequest,
        @AuthenticationPrincipal user: UserPrincipal
    ): ResponseEntity<OrderResponse> {
        val order = orderService.createOrder(user.id, request)
        return ResponseEntity.created(URI("/api/v1/orders/${order.id}"))
            .body(OrderResponse.from(order))
    }

    @GetMapping
    suspend fun list(
        @AuthenticationPrincipal user: UserPrincipal,
        pageable: Pageable
    ): Page<OrderSummary> = orderService.findByUser(user.id, pageable)
}
```

## Kurallar

- `suspend fun` — blocking IO'yu coroutine'e taşı
- `Flow` — reactive stream için, `Channel` — hot stream için
- `value class` — primitive wrapper'lar için (type safety + zero overhead)
- `sealed class/interface` — exhaustive when expression için
- `data class` — DTO ve value object için
- `?.let`, `?.also`, `?.takeIf` — null-safe chaining
- `runCatching` — exception'ı Result'a dönüştür
- KMP'de `expect/actual` ile platform-specific implementasyon
