---
inclusion: fileMatch
fileMatchPattern: "**/*.{ts,tsx,js,jsx,py,go}"
---

# Performance Optimization — İleri Seviye

## Core Web Vitals Hedefleri

| Metrik | İyi | İyileştirme Gerekli | Kötü |
|--------|-----|---------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

## Frontend Optimizasyonları

```tsx
// ✅ Image optimizasyonu (Next.js)
import Image from "next/image";
<Image src="/hero.webp" width={1200} height={600} priority alt="Hero" />

// ✅ Dynamic import — code splitting
const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton />,
  ssr: false,
});

// ✅ Virtual list — büyük listeler için
import { useVirtualizer } from "@tanstack/react-virtual";
function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 60,
    overscan: 5,
  });
  return (
    <div ref={parentRef} style={{ height: "600px", overflow: "auto" }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map(vItem => (
          <div key={vItem.key} style={{ transform: `translateY(${vItem.start}px)` }}>
            <ItemRow item={items[vItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}

// ✅ Web Worker — ağır hesaplama
const worker = new Worker(new URL("./heavy-calc.worker.ts", import.meta.url));
worker.postMessage({ data: largeDataset });
worker.onmessage = (e) => setResult(e.data);
```

## Backend — Python Optimizasyonları

```python
# ✅ asyncio + httpx — concurrent requests
import asyncio
import httpx

async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return [r.json() for r in responses if not isinstance(r, Exception)]

# ✅ Redis caching decorator
import functools
import json
import hashlib
from redis.asyncio import Redis

def cache(ttl: int = 300, key_prefix: str = ""):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            redis: Redis = kwargs.get("redis") or args[0].redis
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

# ✅ Generator — büyük veri setleri
def process_large_file(filepath: str):
    with open(filepath) as f:
        for line in f:  # Tüm dosyayı belleğe yükleme
            yield process_line(line.strip())

# ✅ __slots__ — bellek optimizasyonu
class Point:
    __slots__ = ("x", "y", "z")
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z
```

## Database Sorgu Optimizasyonu

```sql
-- ✅ EXPLAIN ANALYZE ile sorgu planı
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT u.id, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id, u.email;

-- ✅ Partial index — koşullu sorgular için
CREATE INDEX CONCURRENTLY idx_orders_pending
ON orders (created_at, user_id)
WHERE status = 'pending';

-- ✅ Covering index — index-only scan
CREATE INDEX CONCURRENTLY idx_users_email_active
ON users (email) INCLUDE (id, name)
WHERE is_active = true;

-- ✅ Materialized view — pahalı aggregation
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT
  DATE_TRUNC('day', created_at) AS day,
  SUM(total_amount) AS revenue,
  COUNT(*) AS order_count
FROM orders
WHERE status = 'completed'
GROUP BY 1;

CREATE UNIQUE INDEX ON daily_revenue (day);

-- Refresh (cron ile)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;
```

## Go Optimizasyonları

```go
// ✅ sync.Pool — GC baskısını azalt
var bufPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
}

func processRequest(data []byte) string {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()
    buf.Write(data)
    return buf.String()
}

// ✅ Goroutine pool — sınırsız goroutine açma
func workerPool(jobs <-chan Job, results chan<- Result, workers int) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}
```

## Profiling

```bash
# Node.js
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Python
python -m cProfile -o output.prof app.py
python -m pstats output.prof

# Go
go tool pprof http://localhost:6060/debug/pprof/heap
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

## Kurallar

- Önce ölç, sonra optimize et — premature optimization yapma
- N+1 sorgu problemi için ORM'de `select_related`/`include` kullan
- Redis cache TTL'ini iş mantığına göre ayarla
- Büyük listeler için virtual scrolling kullan
- Image'ları WebP/AVIF formatında sun, `loading="lazy"` ekle
- Bundle analyzer ile gereksiz dependency'leri tespit et
- DB index'lerini `CONCURRENTLY` ile ekle — lock almaz
- CPU-bound işleri Worker Thread/Process Pool'a taşı
