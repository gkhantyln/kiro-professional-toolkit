# Skill: setup-cdn-edge

## Açıklama
Cloudflare Workers / Edge Functions altyapısı kurar. CDN cache stratejisi, edge middleware, A/B testing ve geo-routing dahil.

## Kullanım
```
#setup-cdn-edge <proje-adı> [--platform cloudflare|vercel-edge|deno-deploy] [--features cache,ab-test,geo]
```

## Örnekler
```
#setup-cdn-edge my-app --platform cloudflare --features cache,ab-test,geo
#setup-cdn-edge api-gateway --platform vercel-edge --features cache
```

## Oluşturulan Yapı
```
workers/
├── wrangler.toml
├── src/
│   ├── index.ts          # main worker
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── rate-limit.ts
│   │   └── geo-block.ts
│   ├── handlers/
│   │   ├── cache.ts
│   │   ├── ab-test.ts
│   │   └── static.ts
│   └── utils/
│       └── cache-key.ts
└── test/
    └── worker.test.ts
```

## Cloudflare Worker — Ana Worker

### src/index.ts
```typescript
import { Hono } from "hono";
import { cache } from "hono/cache";
import { cors } from "hono/cors";
import { secureHeaders } from "hono/secure-headers";
import { rateLimiter } from "./middleware/rate-limit";
import { geoBlock } from "./middleware/geo-block";
import { abTest } from "./handlers/ab-test";

export interface Env {
  CACHE: KVNamespace;
  AB_CONFIG: KVNamespace;
  RATE_LIMIT: DurableObjectNamespace;
  ORIGIN_URL: string;
}

const app = new Hono<{ Bindings: Env }>();

// Global middleware
app.use("*", secureHeaders());
app.use("*", cors({ origin: ["https://myapp.com"] }));
app.use("*", geoBlock(["RU", "CN", "KP"]));  // geo-based blocking
app.use("/api/*", rateLimiter({ limit: 100, window: 60 }));

// Cache static assets
app.use("/static/*", cache({
  cacheName: "static-assets",
  cacheControl: "public, max-age=31536000, immutable",
}));

// A/B test routing
app.get("/", abTest);

// API proxy with cache
app.all("/api/*", async (c) => {
  const cacheKey = new Request(c.req.url, c.req.raw);
  const cached = await caches.default.match(cacheKey);
  if (cached) return cached;

  const response = await fetch(`${c.env.ORIGIN_URL}${c.req.path}`, c.req.raw);

  if (response.ok && c.req.method === "GET") {
    const toCache = new Response(response.body, response);
    toCache.headers.set("Cache-Control", "public, s-maxage=60");
    c.executionCtx.waitUntil(caches.default.put(cacheKey, toCache.clone()));
    return toCache;
  }

  return response;
});

export default app;
```

### middleware/rate-limit.ts — Durable Objects
```typescript
export class RateLimiter implements DurableObject {
  private requests: number[] = [];

  async fetch(request: Request): Promise<Response> {
    const { limit, window } = await request.json<{ limit: number; window: number }>();
    const now = Date.now();

    // Sliding window
    this.requests = this.requests.filter(t => now - t < window * 1000);

    if (this.requests.length >= limit) {
      return new Response("Rate limit exceeded", {
        status: 429,
        headers: {
          "Retry-After": String(window),
          "X-RateLimit-Limit": String(limit),
          "X-RateLimit-Remaining": "0",
        },
      });
    }

    this.requests.push(now);
    return new Response("OK", {
      headers: {
        "X-RateLimit-Limit": String(limit),
        "X-RateLimit-Remaining": String(limit - this.requests.length),
      },
    });
  }
}
```

### handlers/ab-test.ts
```typescript
export async function abTest(c: Context<{ Bindings: Env }>): Promise<Response> {
  // Sticky session — aynı kullanıcı hep aynı variant
  const userId = getCookie(c, "user_id") ?? crypto.randomUUID();
  const variant = parseInt(userId.slice(-1), 16) < 8 ? "control" : "treatment";

  const config = await c.env.AB_CONFIG.get(variant, "json") as { origin: string };
  const response = await fetch(config.origin, c.req.raw);

  const newResponse = new Response(response.body, response);
  newResponse.headers.set("X-AB-Variant", variant);
  setCookie(c, "user_id", userId, { maxAge: 86400 * 30, httpOnly: true });

  return newResponse;
}
```

### wrangler.toml
```toml
name = "my-app-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"
compatibility_flags = ["nodejs_compat"]

[[kv_namespaces]]
binding = "CACHE"
id = "YOUR_KV_ID"

[[kv_namespaces]]
binding = "AB_CONFIG"
id = "YOUR_AB_KV_ID"

[[durable_objects.bindings]]
name = "RATE_LIMIT"
class_name = "RateLimiter"

[vars]
ORIGIN_URL = "https://api.myapp.com"

[env.production]
routes = [{ pattern = "myapp.com/*", zone_name = "myapp.com" }]
```

## Vercel Edge Middleware

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const country = request.geo?.country ?? "US";
  const response = NextResponse.next();

  // Geo-based content
  response.headers.set("X-User-Country", country);

  // A/B test cookie
  if (!request.cookies.has("ab-variant")) {
    const variant = Math.random() < 0.5 ? "a" : "b";
    response.cookies.set("ab-variant", variant, { maxAge: 86400 * 30 });
  }

  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

## Özellikler
- Cloudflare Workers + Hono framework
- Durable Objects ile distributed rate limiting
- KV Store ile edge caching
- A/B testing — sticky sessions
- Geo-based routing ve blocking
- Cache-Control stratejisi (immutable static, s-maxage API)
- Vercel Edge Middleware alternatifi
- `wrangler` ile local dev + deploy
