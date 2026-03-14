---
name: setup-redis-cache
description: Setup Redis caching layer with connection pooling, cache-aside pattern, invalidation strategies, and rate limiting
---

# Setup Redis Cache

Creates a production-ready Redis caching layer with:
- Connection pooling with ioredis
- Cache-aside pattern with TTL management
- Tag-based cache invalidation
- Rate limiting middleware
- Session storage
- Pub/Sub for real-time events
- Distributed locks

## Usage
```
#setup-redis-cache <framework>
```

## lib/redis.ts
```typescript
import Redis, { type RedisOptions } from 'ioredis';
import { logger } from './logger';

const options: RedisOptions = {
  host: process.env.REDIS_HOST ?? 'localhost',
  port: Number(process.env.REDIS_PORT ?? 6379),
  password: process.env.REDIS_PASSWORD,
  db: Number(process.env.REDIS_DB ?? 0),
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: true,
  retryStrategy: (times) => Math.min(times * 50, 2000),
};

export const redis = new Redis(options);
export const redisSubscriber = new Redis(options);

redis.on('error', (err) => logger.error({ err }, 'Redis error'));
redis.on('connect', () => logger.info('Redis connected'));
```

## lib/cache.ts
```typescript
import { redis } from './redis';

type CacheOptions = {
  ttl?: number;        // seconds, default 300
  tags?: string[];     // for tag-based invalidation
};

export class Cache {
  private prefix: string;

  constructor(prefix = 'cache') {
    this.prefix = prefix;
  }

  private key(k: string) {
    return `${this.prefix}:${k}`;
  }

  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(this.key(key));
    return data ? JSON.parse(data) : null;
  }

  async set<T>(key: string, value: T, options: CacheOptions = {}): Promise<void> {
    const { ttl = 300, tags = [] } = options;
    const serialized = JSON.stringify(value);
    const pipeline = redis.pipeline();

    pipeline.setex(this.key(key), ttl, serialized);

    // Register key under each tag for bulk invalidation
    for (const tag of tags) {
      pipeline.sadd(`tag:${tag}`, this.key(key));
      pipeline.expire(`tag:${tag}`, ttl + 60);
    }

    await pipeline.exec();
  }

  async invalidate(key: string): Promise<void> {
    await redis.del(this.key(key));
  }

  async invalidateByTag(tag: string): Promise<void> {
    const keys = await redis.smembers(`tag:${tag}`);
    if (keys.length > 0) {
      await redis.del(...keys, `tag:${tag}`);
    }
  }

  // Cache-aside helper
  async remember<T>(
    key: string,
    fetcher: () => Promise<T>,
    options: CacheOptions = {},
  ): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached !== null) return cached;

    const value = await fetcher();
    await this.set(key, value, options);
    return value;
  }
}

export const cache = new Cache();
```

## middleware/rate-limit.ts
```typescript
import { redis } from '@/lib/redis';
import { NextRequest, NextResponse } from 'next/server';

type RateLimitOptions = {
  limit: number;
  window: number; // seconds
  identifier?: (req: NextRequest) => string;
};

export function rateLimit(options: RateLimitOptions) {
  const { limit, window, identifier } = options;

  return async (req: NextRequest) => {
    const id = identifier
      ? identifier(req)
      : req.headers.get('x-forwarded-for') ?? req.ip ?? 'anonymous';

    const key = `rl:${req.nextUrl.pathname}:${id}`;
    const now = Date.now();
    const windowStart = now - window * 1000;

    const pipeline = redis.pipeline();
    pipeline.zremrangebyscore(key, 0, windowStart);
    pipeline.zadd(key, now, `${now}`);
    pipeline.zcard(key);
    pipeline.expire(key, window);

    const results = await pipeline.exec();
    const count = results?.[2]?.[1] as number;

    const remaining = Math.max(0, limit - count);
    const reset = Math.ceil((now + window * 1000) / 1000);

    if (count > limit) {
      return NextResponse.json(
        { error: 'Too Many Requests' },
        {
          status: 429,
          headers: {
            'X-RateLimit-Limit': String(limit),
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Reset': String(reset),
            'Retry-After': String(window),
          },
        },
      );
    }

    return null; // continue
  };
}
```

## lib/lock.ts (Distributed Lock)
```typescript
import { redis } from './redis';
import { randomUUID } from 'crypto';

export class DistributedLock {
  async acquire(resource: string, ttl = 30): Promise<string | null> {
    const token = randomUUID();
    const key = `lock:${resource}`;
    const result = await redis.set(key, token, 'EX', ttl, 'NX');
    return result === 'OK' ? token : null;
  }

  async release(resource: string, token: string): Promise<boolean> {
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    const result = await redis.eval(script, 1, `lock:${resource}`, token);
    return result === 1;
  }

  async withLock<T>(resource: string, fn: () => Promise<T>, ttl = 30): Promise<T> {
    const token = await this.acquire(resource, ttl);
    if (!token) throw new Error(`Could not acquire lock for ${resource}`);
    try {
      return await fn();
    } finally {
      await this.release(resource, token);
    }
  }
}

export const lock = new DistributedLock();
```
