---
name: create-python-async-worker
description: Production async task worker with Celery, asyncio, Redis/RabbitMQ broker, priority queues, rate limiting, circuit breaker, and distributed tracing
---

# Create Python Async Worker

İleri seviye async task worker sistemi kurar:
- Celery + asyncio entegrasyonu
- Priority queue yönetimi
- Circuit breaker pattern
- Exponential backoff + dead letter queue
- OpenTelemetry distributed tracing
- Prometheus metrics
- Task result caching

## Usage
```
#create-python-async-worker <service-name>
```

## worker/celery_app.py
```python
from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure
from kombu import Queue, Exchange
import structlog
from opentelemetry import trace

logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)

def create_celery_app() -> Celery:
    app = Celery("worker")
    app.config_from_object("worker.config")

    # Priority queues
    app.conf.task_queues = (
        Queue("critical", Exchange("critical"), routing_key="critical",
              queue_arguments={"x-max-priority": 10}),
        Queue("high",     Exchange("high"),     routing_key="high",
              queue_arguments={"x-max-priority": 7}),
        Queue("default",  Exchange("default"),  routing_key="default",
              queue_arguments={"x-max-priority": 5}),
        Queue("low",      Exchange("low"),      routing_key="low",
              queue_arguments={"x-max-priority": 2}),
    )
    app.conf.task_default_queue = "default"
    app.conf.task_default_exchange = "default"
    app.conf.task_default_routing_key = "default"

    # Dead letter queue
    app.conf.task_queues += (
        Queue("dlq", Exchange("dlq"), routing_key="dlq"),
    )

    return app

celery_app = create_celery_app()
```

## worker/config.py
```python
import os

# Broker & Backend
broker_url = os.environ["CELERY_BROKER_URL"]          # redis:// or amqp://
result_backend = os.environ["CELERY_RESULT_BACKEND"]  # redis://

# Serialization
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# Reliability
task_acks_late = True                    # Ack after completion, not receipt
task_reject_on_worker_lost = True        # Re-queue on worker crash
task_track_started = True
result_expires = 3600                    # 1 hour TTL

# Concurrency
worker_prefetch_multiplier = 1           # Fair dispatch for long tasks
worker_max_tasks_per_child = 1000        # Prevent memory leaks
worker_max_memory_per_child = 512_000   # 512MB limit (KB)

# Rate limiting (global)
task_annotations = {
    "*": {"rate_limit": "1000/m"},
}

# Retry policy defaults
task_soft_time_limit = 300   # 5 min soft limit → SoftTimeLimitExceeded
task_time_limit = 360        # 6 min hard limit → SIGKILL
```

## worker/tasks/base.py
```python
from celery import Task
from celery.exceptions import MaxRetriesExceededError
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import structlog
import time
from worker.celery_app import celery_app
from worker.circuit_breaker import CircuitBreaker

logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)
propagator = TraceContextTextMapPropagator()

class BaseTask(Task):
    """Base task with tracing, structured logging, and circuit breaker."""
    abstract = True
    _circuit_breakers: dict[str, CircuitBreaker] = {}

    def get_circuit_breaker(self, name: str) -> CircuitBreaker:
        if name not in self._circuit_breakers:
            self._circuit_breakers[name] = CircuitBreaker(
                failure_threshold=5,
                recovery_timeout=60,
                expected_exception=Exception,
            )
        return self._circuit_breakers[name]

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(
            "task_failed",
            task_id=task_id,
            task_name=self.name,
            exc_type=type(exc).__name__,
            exc_message=str(exc),
        )
        # Send to DLQ after max retries
        if isinstance(exc, MaxRetriesExceededError):
            self.send_to_dlq(task_id, args, kwargs, exc)

    def send_to_dlq(self, task_id, args, kwargs, exc):
        from worker.tasks.dlq import dead_letter_handler
        dead_letter_handler.apply_async(
            args=[self.name, task_id, args, kwargs, str(exc)],
            queue="dlq",
        )

    def apply_async(self, args=None, kwargs=None, **options):
        # Inject trace context into task headers
        carrier: dict = {}
        propagator.inject(carrier)
        headers = options.pop("headers", {}) or {}
        headers.update(carrier)
        return super().apply_async(args=args, kwargs=kwargs, headers=headers, **options)
```

## worker/tasks/email.py
```python
from celery import shared_task
from celery.utils.log import get_task_logger
from worker.tasks.base import BaseTask
from worker.celery_app import celery_app
import httpx

logger = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    base=BaseTask,
    name="worker.tasks.email.send_email",
    queue="high",
    max_retries=5,
    default_retry_delay=60,
    autoretry_for=(httpx.HTTPError, ConnectionError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_email(self, *, to: str, subject: str, body: str, template_id: str | None = None):
    """Send transactional email with retry and circuit breaker."""
    cb = self.get_circuit_breaker("email_provider")

    with cb:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={"Authorization": f"Bearer {os.environ['SENDGRID_API_KEY']}"},
                json={
                    "to": [{"email": to}],
                    "subject": subject,
                    "content": [{"type": "text/html", "value": body}],
                },
            )
            response.raise_for_status()

    logger.info("Email sent", to=to, subject=subject)
    return {"status": "sent", "to": to}
```

## worker/circuit_breaker.py
```python
import time
import threading
from enum import Enum
from typing import Type

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._state = State.CLOSED
        self._lock = threading.Lock()

    @property
    def state(self) -> State:
        with self._lock:
            if self._state == State.OPEN:
                if time.monotonic() - self._last_failure_time > self.recovery_timeout:
                    self._state = State.HALF_OPEN
            return self._state

    def __enter__(self):
        if self.state == State.OPEN:
            raise RuntimeError(f"Circuit breaker is OPEN")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self._lock:
            if exc_type and issubclass(exc_type, self.expected_exception):
                self._failure_count += 1
                self._last_failure_time = time.monotonic()
                if self._failure_count >= self.failure_threshold:
                    self._state = State.OPEN
                return False
            # Success
            self._failure_count = 0
            self._state = State.CLOSED
            return False
```

## worker/metrics.py
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from celery.signals import task_prerun, task_postrun, task_failure, task_retry
import time

TASK_DURATION = Histogram(
    "celery_task_duration_seconds",
    "Task execution duration",
    ["task_name", "queue"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5, 10, 30, 60, 300],
)
TASK_TOTAL = Counter("celery_tasks_total", "Total tasks", ["task_name", "status"])
TASK_RETRIES = Counter("celery_task_retries_total", "Task retries", ["task_name"])
ACTIVE_TASKS = Gauge("celery_active_tasks", "Currently running tasks", ["task_name"])

_task_start_times: dict[str, float] = {}

@task_prerun.connect
def on_task_prerun(task_id, task, **kwargs):
    _task_start_times[task_id] = time.monotonic()
    ACTIVE_TASKS.labels(task_name=task.name).inc()

@task_postrun.connect
def on_task_postrun(task_id, task, state, **kwargs):
    duration = time.monotonic() - _task_start_times.pop(task_id, time.monotonic())
    TASK_DURATION.labels(task_name=task.name, queue=task.queue or "default").observe(duration)
    TASK_TOTAL.labels(task_name=task.name, status=state).inc()
    ACTIVE_TASKS.labels(task_name=task.name).dec()

@task_failure.connect
def on_task_failure(task_id, exception, task, **kwargs):
    TASK_TOTAL.labels(task_name=task.name, status="FAILURE").inc()

@task_retry.connect
def on_task_retry(request, reason, **kwargs):
    TASK_RETRIES.labels(task_name=request.task).inc()

def start_metrics_server(port: int = 9090):
    start_http_server(port)
```
