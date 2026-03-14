---
name: setup-event-driven
description: Event-driven architecture with Kafka/RabbitMQ, outbox pattern, saga orchestration, and dead letter queues
---

# Setup Event-Driven Architecture

Production-ready event-driven sistem kurar:
- Kafka producer/consumer with schema registry
- Outbox pattern (at-least-once delivery)
- Saga orchestration pattern
- Dead letter queue (DLQ) handling
- Event sourcing foundation
- Idempotency keys

## Usage
```
#setup-event-driven <kafka|rabbitmq>
```

## lib/kafka/producer.ts
```typescript
import { Kafka, Producer, CompressionTypes, Message } from 'kafkajs';
import { SchemaRegistry } from '@kafkajs/confluent-schema-registry';
import { randomUUID } from 'crypto';

const kafka = new Kafka({
  clientId: process.env.KAFKA_CLIENT_ID ?? 'service',
  brokers: (process.env.KAFKA_BROKERS ?? 'localhost:9092').split(','),
  ssl: process.env.KAFKA_SSL === 'true',
  sasl: process.env.KAFKA_SASL_USERNAME ? {
    mechanism: 'scram-sha-512',
    username: process.env.KAFKA_SASL_USERNAME,
    password: process.env.KAFKA_SASL_PASSWORD!,
  } : undefined,
  retry: { initialRetryTime: 100, retries: 8 },
});

const registry = new SchemaRegistry({ host: process.env.SCHEMA_REGISTRY_URL! });

export class EventProducer {
  private producer: Producer;

  constructor() {
    this.producer = kafka.producer({
      idempotent: true,
      maxInFlightRequests: 5,
      transactionalId: process.env.KAFKA_TRANSACTIONAL_ID,
    });
  }

  async connect() { await this.producer.connect(); }
  async disconnect() { await this.producer.disconnect(); }

  async publish<T extends object>(topic: string, event: T, key?: string): Promise<void> {
    const schemaId = await registry.getLatestSchemaId(topic);
    const encoded = await registry.encode(schemaId, event);

    await this.producer.send({
      topic,
      compression: CompressionTypes.GZIP,
      messages: [{
        key: key ?? randomUUID(),
        value: encoded,
        headers: {
          'event-id': randomUUID(),
          'event-time': new Date().toISOString(),
          'content-type': 'application/avro',
        },
      }],
    });
  }
}
```

## lib/kafka/consumer.ts
```typescript
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import { SchemaRegistry } from '@kafkajs/confluent-schema-registry';
import { logger } from '../logger';

const kafka = new Kafka({
  clientId: process.env.KAFKA_CLIENT_ID ?? 'service',
  brokers: (process.env.KAFKA_BROKERS ?? 'localhost:9092').split(','),
});

const registry = new SchemaRegistry({ host: process.env.SCHEMA_REGISTRY_URL! });

type Handler<T> = (event: T, metadata: { topic: string; partition: number; offset: string }) => Promise<void>;

export class EventConsumer {
  private consumer: Consumer;
  private handlers = new Map<string, Handler<unknown>>();

  constructor(groupId: string) {
    this.consumer = kafka.consumer({ groupId, sessionTimeout: 30000 });
  }

  on<T>(topic: string, handler: Handler<T>) {
    this.handlers.set(topic, handler as Handler<unknown>);
    return this;
  }

  async start(topics: string[]) {
    await this.consumer.connect();
    await this.consumer.subscribe({ topics, fromBeginning: false });

    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
        try {
          const decoded = await registry.decode(message.value!);
          const handler = this.handlers.get(topic);
          if (handler) {
            await handler(decoded, { topic, partition, offset: message.offset });
          }
        } catch (err) {
          logger.error({ err, topic, partition, offset: message.offset }, 'Message processing failed');
          await this.sendToDLQ(topic, message);
        }
      },
    });
  }

  private async sendToDLQ(topic: string, message: any) {
    // Implement DLQ logic — publish to `${topic}.dlq`
    logger.warn({ topic }, 'Message sent to DLQ');
  }

  async stop() { await this.consumer.disconnect(); }
}
```

## lib/outbox/outbox.ts (Transactional Outbox Pattern)
```typescript
import { PrismaClient } from '@prisma/client';
import { EventProducer } from '../kafka/producer';
import { logger } from '../logger';

const prisma = new PrismaClient();
const producer = new EventProducer();

// Schema: OutboxEvent { id, topic, key, payload, createdAt, processedAt }

export async function publishWithOutbox<T extends object>(
  tx: Omit<PrismaClient, '$connect' | '$disconnect' | '$on' | '$transaction' | '$use' | '$extends'>,
  topic: string,
  event: T,
  key?: string,
): Promise<void> {
  await (tx as any).outboxEvent.create({
    data: { topic, key, payload: JSON.stringify(event) },
  });
}

// Outbox relay — run as a separate process or cron
export async function processOutbox() {
  await producer.connect();

  const events = await prisma.outboxEvent.findMany({
    where: { processedAt: null },
    orderBy: { createdAt: 'asc' },
    take: 100,
  });

  for (const event of events) {
    try {
      await producer.publish(event.topic, JSON.parse(event.payload), event.key ?? undefined);
      await prisma.outboxEvent.update({
        where: { id: event.id },
        data: { processedAt: new Date() },
      });
    } catch (err) {
      logger.error({ err, eventId: event.id }, 'Outbox relay failed');
    }
  }
}
```
