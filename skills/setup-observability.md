---
name: setup-observability
description: Setup full observability stack with OpenTelemetry, Prometheus, Grafana, and structured logging
---

# Setup Observability

Creates a complete observability stack with:
- OpenTelemetry SDK instrumentation (traces, metrics, logs)
- Prometheus metrics with custom dashboards
- Grafana dashboards as code
- Structured JSON logging with correlation IDs
- Alerting rules for SLOs
- Health check endpoints

## Usage
```
#setup-observability <framework>
```

## Node.js / TypeScript

### instrumentation.ts (load before app)
```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { Resource } from '@opentelemetry/resources';
import { SEMRESATTRS_SERVICE_NAME, SEMRESATTRS_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SEMRESATTRS_SERVICE_NAME]: process.env.SERVICE_NAME ?? 'unknown',
    [SEMRESATTRS_SERVICE_VERSION]: process.env.SERVICE_VERSION ?? '0.0.0',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318/v1/traces',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter(),
    exportIntervalMillis: 10_000,
  }),
  instrumentations: [getNodeAutoInstrumentations({
    '@opentelemetry/instrumentation-fs': { enabled: false },
  })],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());
```

### lib/logger.ts
```typescript
import pino from 'pino';
import { context, trace } from '@opentelemetry/api';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  formatters: {
    level: (label) => ({ level: label }),
    log: (obj) => {
      const span = trace.getActiveSpan();
      if (span) {
        const ctx = span.spanContext();
        return { ...obj, traceId: ctx.traceId, spanId: ctx.spanId };
      }
      return obj;
    },
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: ['password', 'token', 'authorization', '*.password', '*.token'],
});
```

### lib/metrics.ts
```typescript
import { metrics } from '@opentelemetry/api';

const meter = metrics.getMeter('app');

export const httpRequestDuration = meter.createHistogram('http_request_duration_ms', {
  description: 'HTTP request duration in milliseconds',
  unit: 'ms',
  boundaries: [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000],
});

export const httpRequestTotal = meter.createCounter('http_requests_total', {
  description: 'Total number of HTTP requests',
});

export const activeConnections = meter.createUpDownCounter('active_connections', {
  description: 'Number of active connections',
});

export const dbQueryDuration = meter.createHistogram('db_query_duration_ms', {
  description: 'Database query duration in milliseconds',
  unit: 'ms',
});
```

### health/route.ts
```typescript
import { db } from '@/lib/db';
import { redis } from '@/lib/redis';

export async function GET() {
  const checks = await Promise.allSettled([
    db.$queryRaw`SELECT 1`,
    redis.ping(),
  ]);

  const [dbCheck, redisCheck] = checks;
  const healthy = checks.every(c => c.status === 'fulfilled');

  return Response.json({
    status: healthy ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    checks: {
      database: dbCheck.status === 'fulfilled' ? 'ok' : 'error',
      redis: redisCheck.status === 'fulfilled' ? 'ok' : 'error',
    },
  }, { status: healthy ? 200 : 503 });
}
```

## Grafana Dashboard (JSON)
```json
{
  "title": "Service Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "rate(http_requests_total[5m])",
        "legendFormat": "{{method}} {{route}}"
      }]
    },
    {
      "title": "P95 Latency",
      "type": "timeseries",
      "targets": [{
        "expr": "histogram_quantile(0.95, rate(http_request_duration_ms_bucket[5m]))",
        "legendFormat": "p95"
      }]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [{
        "expr": "rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m])"
      }]
    }
  ]
}
```

## Prometheus Alert Rules
```yaml
groups:
  - name: slo
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 1% SLO"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_ms_bucket[5m])) > 500
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency above 500ms"
```
