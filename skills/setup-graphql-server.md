# Skill: setup-graphql-server

## Açıklama
Production-grade GraphQL server kurar. Apollo Server 4 + Pothos schema builder + DataLoader + Prisma stack.

## Kullanım
```
#setup-graphql-server <proje-adı> [--framework express|fastify|standalone] [--db prisma|drizzle]
```

## Örnekler
```
#setup-graphql-server my-api --framework fastify --db prisma
#setup-graphql-server shop-api --framework standalone
```

## Oluşturulan Yapı
```
src/
├── schema/
│   ├── index.ts          # schema builder
│   ├── types/
│   │   ├── user.ts
│   │   ├── order.ts
│   │   └── scalars.ts    # DateTime, Money, UUID
│   ├── queries/
│   │   ├── user.ts
│   │   └── order.ts
│   ├── mutations/
│   │   ├── user.ts
│   │   └── order.ts
│   └── subscriptions/
│       └── order.ts
├── loaders/
│   ├── index.ts
│   ├── user.loader.ts
│   └── order.loader.ts
├── context.ts
├── server.ts
└── plugins/
    ├── complexity.ts
    └── persisted-queries.ts
```

## Üretilen Kod Özellikleri

### schema/index.ts — Pothos Schema Builder
```typescript
import SchemaBuilder from "@pothos/core";
import PrismaPlugin from "@pothos/plugin-prisma";
import RelayPlugin from "@pothos/plugin-relay";
import ValidationPlugin from "@pothos/plugin-validation";
import ComplexityPlugin from "@pothos/plugin-complexity";
import type { Context } from "./context";
import { db } from "./db";

export const builder = new SchemaBuilder<{
  Context: Context;
  PrismaTypes: PrismaTypes;
  Scalars: {
    DateTime: { Input: Date; Output: Date };
    UUID: { Input: string; Output: string };
  };
}>({
  plugins: [PrismaPlugin, RelayPlugin, ValidationPlugin, ComplexityPlugin],
  prisma: { client: db },
  relay: {
    clientMutationId: "optional",
    cursorType: "String",
  },
  complexity: {
    defaultComplexity: 1,
    defaultListMultiplier: 10,
    limit: { complexity: 500, depth: 7 },
  },
});
```

### loaders/user.loader.ts — DataLoader
```typescript
import DataLoader from "dataloader";
import { db } from "../db";
import type { User } from "@prisma/client";

export function createUserLoader() {
  return new DataLoader<string, User | null>(
    async (ids) => {
      const users = await db.user.findMany({
        where: { id: { in: [...ids] } },
      });
      const map = new Map(users.map(u => [u.id, u]));
      return ids.map(id => map.get(id) ?? null);
    },
    { cache: true, maxBatchSize: 100 }
  );
}
```

### context.ts
```typescript
import type { YogaInitialContext } from "graphql-yoga";
import { createUserLoader } from "./loaders/user.loader";
import { verifyToken } from "./auth";

export interface Context {
  user: { id: string; role: string } | null;
  loaders: {
    user: ReturnType<typeof createUserLoader>;
  };
}

export async function createContext(ctx: YogaInitialContext): Promise<Context> {
  const token = ctx.request.headers.get("authorization")?.split(" ")[1];
  const user = token ? await verifyToken(token) : null;

  return {
    user,
    loaders: {
      user: createUserLoader(),
    },
  };
}
```

### server.ts — GraphQL Yoga
```typescript
import { createYoga } from "graphql-yoga";
import { usePersistedOperations } from "@graphql-yoga/plugin-persisted-operations";
import { useResponseCache } from "@graphql-yoga/plugin-response-cache";
import { schema } from "./schema";
import { createContext } from "./context";

export const yoga = createYoga({
  schema,
  context: createContext,
  plugins: [
    usePersistedOperations({
      getPersistedOperation: async (hash) => persistedOps[hash] ?? null,
    }),
    useResponseCache({
      session: (ctx) => ctx.user?.id ?? null,
      ttl: 5_000,
      invalidateViaMutation: true,
    }),
  ],
  graphiql: process.env.NODE_ENV !== "production",
  maskedErrors: process.env.NODE_ENV === "production",
});
```

## Özellikler
- Pothos schema builder — code-first, type-safe
- Relay-style cursor pagination
- DataLoader ile N+1 önleme
- Persisted queries — production güvenliği
- Response cache — performans
- Depth + complexity limiting — DoS koruması
- GraphQL Yoga — framework agnostic
- Subscription desteği (WebSocket)
- Custom scalars: DateTime, UUID, Money
