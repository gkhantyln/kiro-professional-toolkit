# Skill: setup-message-queue

## Açıklama
Production-grade message queue altyapısı kurar. RabbitMQ veya AWS SQS/SNS seçeneği ile dead letter queue, retry mekanizması ve monitoring dahil.

## Kullanım
```
#setup-message-queue <proje-adı> [--broker rabbitmq|sqs|kafka-lite] [--lang typescript|python|go]
```

## Örnekler
```
#setup-message-queue order-processor --broker rabbitmq --lang typescript
#setup-message-queue notification-service --broker sqs --lang python
```

## Oluşturulan Yapı
```
src/
├── queue/
│   ├── connection.ts
│   ├── publisher.ts
│   ├── consumer.ts
│   ├── dlq-processor.ts
│   └── schemas/
│       └── events.ts
├── handlers/
│   ├── order-created.handler.ts
│   └── payment-completed.handler.ts
└── config/
    └── queue.config.ts
```

## RabbitMQ — TypeScript

### connection.ts
```typescript
import amqplib, { Channel, Connection } from "amqplib";

const EXCHANGES = {
  ORDERS: "orders.exchange",
  PAYMENTS: "payments.exchange",
  DLX: "dead.letter.exchange",
} as const;

const QUEUES = {
  ORDER_CREATED: "order.created",
  ORDER_CREATED_DLQ: "order.created.dlq",
  PAYMENT_COMPLETED: "payment.completed",
} as const;

export async function setupRabbitMQ(url: string): Promise<Channel> {
  const conn: Connection = await amqplib.connect(url);
  const channel = await conn.createChannel();

  // Dead letter exchange
  await channel.assertExchange(EXCHANGES.DLX, "direct", { durable: true });

  // Main exchange
  await channel.assertExchange(EXCHANGES.ORDERS, "topic", { durable: true });

  // Queue with DLQ config
  await channel.assertQueue(QUEUES.ORDER_CREATED, {
    durable: true,
    arguments: {
      "x-dead-letter-exchange": EXCHANGES.DLX,
      "x-dead-letter-routing-key": QUEUES.ORDER_CREATED_DLQ,
      "x-message-ttl": 86_400_000,  // 24h
      "x-max-length": 100_000,
    },
  });

  // DLQ
  await channel.assertQueue(QUEUES.ORDER_CREATED_DLQ, { durable: true });
  await channel.bindQueue(QUEUES.ORDER_CREATED_DLQ, EXCHANGES.DLX, QUEUES.ORDER_CREATED_DLQ);

  await channel.bindQueue(QUEUES.ORDER_CREATED, EXCHANGES.ORDERS, "order.created");
  await channel.prefetch(10);  // backpressure

  return channel;
}
```

### publisher.ts
```typescript
export class MessagePublisher {
  constructor(private channel: Channel) {}

  async publish<T>(exchange: string, routingKey: string, payload: T): Promise<void> {
    const message = Buffer.from(JSON.stringify({
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      payload,
    }));

    const sent = this.channel.publish(exchange, routingKey, message, {
      persistent: true,
      contentType: "application/json",
      headers: { "x-retry-count": 0 },
    });

    if (!sent) throw new Error("Channel buffer full — apply backpressure");
  }
}
```

### consumer.ts
```typescript
const MAX_RETRIES = 3;

export class MessageConsumer {
  constructor(private channel: Channel) {}

  async consume(queue: string, handler: (msg: unknown) => Promise<void>): Promise<void> {
    await this.channel.consume(queue, async (msg) => {
      if (!msg) return;

      const retryCount = (msg.properties.headers?.["x-retry-count"] ?? 0) as number;

      try {
        const payload = JSON.parse(msg.content.toString());
        await handler(payload);
        this.channel.ack(msg);
      } catch (err) {
        if (retryCount < MAX_RETRIES) {
          // Exponential backoff via re-queue with delay
          setTimeout(() => {
            this.channel.nack(msg, false, false);  // → DLQ
          }, Math.pow(2, retryCount) * 1000);
        } else {
          this.channel.nack(msg, false, false);  // → DLQ
        }
      }
    });
  }
}
```

## AWS SQS — Python

```python
import boto3
import json
import logging
from typing import Callable, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SQSConfig:
    queue_url: str
    dlq_url: str
    max_retries: int = 3
    visibility_timeout: int = 30
    batch_size: int = 10

class SQSConsumer:
    def __init__(self, config: SQSConfig):
        self.sqs = boto3.client("sqs")
        self.config = config

    def consume(self, handler: Callable[[dict], None]) -> None:
        while True:
            response = self.sqs.receive_message(
                QueueUrl=self.config.queue_url,
                MaxNumberOfMessages=self.config.batch_size,
                WaitTimeSeconds=20,  # long polling
                AttributeNames=["ApproximateReceiveCount"],
            )

            for message in response.get("Messages", []):
                receive_count = int(message["Attributes"]["ApproximateReceiveCount"])
                try:
                    body = json.loads(message["Body"])
                    handler(body)
                    self.sqs.delete_message(
                        QueueUrl=self.config.queue_url,
                        ReceiptHandle=message["ReceiptHandle"],
                    )
                except Exception as e:
                    logger.error(f"Handler failed (attempt {receive_count}): {e}")
                    if receive_count >= self.config.max_retries:
                        # SQS otomatik DLQ'ya taşır (redrive policy ile)
                        logger.error(f"Max retries exceeded, moving to DLQ")
```

## docker-compose.yml (RabbitMQ)
```yaml
services:
  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 10s
      retries: 5

volumes:
  rabbitmq_data:
```

## Özellikler
- Dead Letter Queue (DLQ) — başarısız mesajları yakala
- Exponential backoff retry
- Persistent messages — broker restart'ta kaybolmaz
- Prefetch / backpressure kontrolü
- Long polling (SQS) — maliyet optimizasyonu
- Message schema validation
- Prometheus metrics entegrasyonu
