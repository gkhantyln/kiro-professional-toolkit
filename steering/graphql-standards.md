---
inclusion: fileMatch
fileMatchPattern: "**/*.{graphql,gql}"
---

# GraphQL Standards — İleri Seviye

## Schema Tasarımı

```graphql
# ✅ Relay-style pagination — cursor-based
type Query {
  orders(
    first: Int
    after: String
    last: Int
    before: String
    filter: OrderFilter
    orderBy: OrderOrderBy
  ): OrderConnection!

  order(id: ID!): Order
  me: User
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# ✅ Input types — mutation için ayrı type
type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
  cancelOrder(input: CancelOrderInput!): CancelOrderPayload!
}

input CreateOrderInput {
  clientMutationId: String  # idempotency
  items: [OrderItemInput!]!
}

type CreateOrderPayload {
  clientMutationId: String
  order: Order
  errors: [UserError!]!
}

# ✅ UserError — field-level hata
type UserError {
  field: [String!]
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  NOT_FOUND
  VALIDATION_ERROR
  INSUFFICIENT_STOCK
  UNAUTHORIZED
}

# ✅ Union — polymorphic response
union SearchResult = Order | Product | User

type Query {
  search(query: String!): [SearchResult!]!
}

# ✅ Interface — ortak alanlar
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Order implements Node & Timestamped {
  id: ID!
  status: OrderStatus!
  items: [OrderItem!]!
  total: Money!
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

## DataLoader — N+1 Çözümü

```typescript
// dataloader/user.loader.ts
import DataLoader from "dataloader";

export function createUserLoader(db: Database) {
  return new DataLoader<string, User>(
    async (userIds) => {
      const users = await db.user.findMany({
        where: { id: { in: [...userIds] } },
      });
      const userMap = new Map(users.map(u => [u.id, u]));
      // Sırayı koru — DataLoader zorunluluğu
      return userIds.map(id => userMap.get(id) ?? new Error(`User ${id} not found`));
    },
    { cache: true, maxBatchSize: 100 }
  );
}

// resolver/order.resolver.ts
const resolvers = {
  Order: {
    user: (order: Order, _: unknown, ctx: Context) =>
      ctx.loaders.user.load(order.userId),

    items: (order: Order, _: unknown, ctx: Context) =>
      ctx.loaders.orderItems.loadMany(order.itemIds),
  },
};
```

## Resolver Yapısı

```typescript
// ✅ Resolver — ince tut, iş mantığını service'e taşı
const resolvers = {
  Query: {
    orders: async (_: unknown, args: OrdersArgs, ctx: Context) => {
      ctx.auth.requireAuthenticated();
      return ctx.services.order.findByUser(ctx.user.id, args);
    },

    order: async (_: unknown, { id }: { id: string }, ctx: Context) => {
      const order = await ctx.services.order.findById(id);
      ctx.auth.requireOwnership(order.userId);
      return order;
    },
  },

  Mutation: {
    createOrder: async (_: unknown, { input }: CreateOrderArgs, ctx: Context) => {
      ctx.auth.requireAuthenticated();
      try {
        const order = await ctx.services.order.create(ctx.user.id, input);
        return { order, errors: [] };
      } catch (err) {
        if (err instanceof ValidationError) {
          return { order: null, errors: err.toUserErrors() };
        }
        throw err;
      }
    },
  },

  // ✅ Subscription
  Subscription: {
    orderUpdated: {
      subscribe: (_: unknown, { orderId }: { orderId: string }, ctx: Context) => {
        ctx.auth.requireAuthenticated();
        return ctx.pubsub.asyncIterator(`ORDER_UPDATED:${orderId}`);
      },
    },
  },
};
```

## Persisted Queries + Güvenlik

```typescript
// ✅ Depth limiting — DoS önleme
import depthLimit from "graphql-depth-limit";
import { createComplexityLimitRule } from "graphql-validation-complexity";

const server = new ApolloServer({
  schema,
  validationRules: [
    depthLimit(7),
    createComplexityLimitRule(1000, {
      onCost: (cost) => console.log("Query cost:", cost),
    }),
  ],
  // ✅ Persisted queries — production'da arbitrary query engelle
  persistedQueries: {
    cache: new InMemoryLRUCache({ maxSize: 30_000_000 }),
  },
});

// ✅ Field-level authorization
const resolvers = {
  User: {
    email: (user: User, _: unknown, ctx: Context) => {
      if (ctx.user?.id !== user.id && !ctx.user?.isAdmin) {
        return null; // mask sensitive field
      }
      return user.email;
    },
  },
};
```

## Kurallar

- Cursor-based pagination kullan — offset pagination büyük veri setlerinde yavaş
- Her mutation için `errors: [UserError!]!` döndür — exception fırlatma
- DataLoader ile N+1 sorununu çöz — her resolver'da DB çağrısı yapma
- `clientMutationId` ile idempotency sağla
- Depth limit + complexity limit ekle — DoS koruması
- Production'da persisted queries kullan
- `Node` interface'i ile global object identification
- Subscription'larda auth kontrolü yap
