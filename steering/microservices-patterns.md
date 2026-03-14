---
inclusion: manual
---

# Microservices Patterns — İleri Seviye

## Circuit Breaker

```typescript
// circuit-breaker.ts
enum State { CLOSED, OPEN, HALF_OPEN }

class CircuitBreaker {
  private state = State.CLOSED;
  private failureCount = 0;
  private lastFailureTime?: number;

  constructor(
    private readonly threshold = 5,
    private readonly timeout = 60_000,
    private readonly halfOpenRequests = 1,
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === State.OPEN) {
      if (Date.now() - this.lastFailureTime! > this.timeout) {
        this.state = State.HALF_OPEN;
      } else {
        throw new Error("Circuit breaker is OPEN");
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      this.onFailure();
      throw err;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = State.CLOSED;
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.threshold) {
      this.state = State.OPEN;
    }
  }
}
```

## Saga Pattern — Choreography

```typescript
// Distributed transaction — event-driven
// Her servis kendi event'ini yayar, diğerleri dinler

// order-service: OrderCreated yayar
await eventBus.publish("OrderCreated", {
  orderId, userId, items, total,
  correlationId: uuid(),
});

// payment-service: OrderCreated dinler
eventBus.subscribe("OrderCreated", async (event) => {
  try {
    await paymentService.charge(event.userId, event.total);
    await eventBus.publish("PaymentCompleted", { orderId: event.orderId });
  } catch {
    await eventBus.publish("PaymentFailed", { orderId: event.orderId });
  }
});

// order-service: PaymentFailed dinler → compensate
eventBus.subscribe("PaymentFailed", async (event) => {
  await orderRepo.updateStatus(event.orderId, "cancelled");
  await eventBus.publish("OrderCancelled", { orderId: event.orderId });
});
```

## Outbox Pattern — At-Least-Once Delivery

```typescript
// Aynı transaction içinde hem DB'ye yaz hem outbox'a ekle
async function createOrder(data: CreateOrderDto): Promise<Order> {
  return await db.transaction(async (tx) => {
    const order = await tx.order.create({ data });

    // Outbox — event kaybolmaz
    await tx.outboxEvent.create({
      data: {
        aggregateId: order.id,
        eventType: "OrderCreated",
        payload: JSON.stringify(order),
        status: "pending",
      },
    });

    return order;
  });
}

// Outbox processor (ayrı worker)
async function processOutbox() {
  const events = await db.outboxEvent.findMany({
    where: { status: "pending" },
    take: 100,
    orderBy: { createdAt: "asc" },
  });

  for (const event of events) {
    try {
      await eventBus.publish(event.eventType, JSON.parse(event.payload));
      await db.outboxEvent.update({
        where: { id: event.id },
        data: { status: "processed", processedAt: new Date() },
      });
    } catch {
      await db.outboxEvent.update({
        where: { id: event.id },
        data: { retryCount: { increment: 1 } },
      });
    }
  }
}
```

## CQRS — Command Query Responsibility Segregation

```typescript
// Command side — write model
class CreateOrderCommand {
  constructor(
    public readonly userId: string,
    public readonly items: OrderItem[],
  ) {}
}

class CreateOrderHandler {
  async handle(cmd: CreateOrderCommand): Promise<string> {
    const order = Order.create(cmd.userId, cmd.items); // domain model
    await this.writeRepo.save(order);
    await this.eventBus.publishAll(order.domainEvents);
    return order.id;
  }
}

// Query side — read model (denormalized, optimized for reads)
class GetOrderSummaryQuery {
  constructor(public readonly userId: string) {}
}

class GetOrderSummaryHandler {
  async handle(query: GetOrderSummaryQuery): Promise<OrderSummaryDto[]> {
    // Read model — ayrı tablo, join yok, hızlı
    return this.readDb.query(
      `SELECT * FROM order_summaries WHERE user_id = $1 ORDER BY created_at DESC`,
      [query.userId]
    );
  }
}
```

## API Gateway Pattern

```typescript
// Rate limiting + auth + routing
import Fastify from "fastify";
import { createProxyMiddleware } from "http-proxy-middleware";

const gateway = Fastify();

// Auth middleware
gateway.addHook("preHandler", async (req, reply) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return reply.code(401).send({ error: "Unauthorized" });
  req.user = await verifyJWT(token);
});

// Rate limiting
gateway.register(import("@fastify/rate-limit"), {
  max: 100,
  timeWindow: "1 minute",
  keyGenerator: (req) => req.user?.id ?? req.ip,
});

// Service routing
const routes = {
  "/api/orders": "http://order-service:3001",
  "/api/payments": "http://payment-service:3002",
  "/api/users": "http://user-service:3003",
};
```

## Health Check Standardı

```typescript
// Her servis bu endpoint'i expose etmeli
app.get("/health/live", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

app.get("/health/ready", async (req, res) => {
  const checks = await Promise.allSettled([
    db.query("SELECT 1"),
    redis.ping(),
  ]);

  const results = {
    database: checks[0].status === "fulfilled" ? "ok" : "error",
    redis: checks[1].status === "fulfilled" ? "ok" : "error",
  };

  const isReady = Object.values(results).every(v => v === "ok");
  res.status(isReady ? 200 : 503).json({ status: isReady ? "ready" : "not ready", checks: results });
});
```

## Kurallar

- Her servis kendi DB'sine sahip olmalı — shared DB yasak
- Servisler arası iletişim: sync için gRPC, async için event bus
- Outbox pattern ile event kaybını önle
- Circuit breaker ile cascade failure'ı engelle
- Idempotency key ile duplicate işlemleri önle
- Distributed tracing için her request'e `correlationId` ekle
- Health check: `/health/live` (liveness) + `/health/ready` (readiness)
- CQRS'de write ve read modellerini ayrı tut
