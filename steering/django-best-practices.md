---
inclusion: fileMatch
fileMatchPattern: "**/*.{py,django}"
---

# Django Best Practices — İleri Seviye

## ORM Optimizasyonu

```python
# ❌ N+1 sorunu
for order in Order.objects.all():
    print(order.user.email)  # Her iterasyonda yeni sorgu

# ✅ select_related (ForeignKey/OneToOne)
orders = Order.objects.select_related("user", "user__profile").all()

# ✅ prefetch_related (ManyToMany/reverse FK)
orders = Order.objects.prefetch_related(
    Prefetch("items", queryset=OrderItem.objects.select_related("product"))
).all()

# ✅ only() / defer() — sadece gerekli alanlar
users = User.objects.only("id", "email", "created_at")

# ✅ values() / values_list() — dict/tuple döner, model instance yok
emails = User.objects.filter(is_active=True).values_list("email", flat=True)

# ✅ annotate + aggregate
from django.db.models import Count, Avg, Sum, F, Q
stats = Order.objects.annotate(
    item_count=Count("items"),
    total=Sum(F("items__price") * F("items__quantity"))
).filter(total__gt=100)

# ✅ bulk_create / bulk_update
Product.objects.bulk_create([
    Product(name=name, price=price) for name, price in products
], batch_size=500)

Product.objects.bulk_update(products_to_update, ["price", "stock"], batch_size=500)

# ✅ update() — SQL UPDATE, signal tetiklemez
Order.objects.filter(status="pending", created_at__lt=cutoff).update(status="expired")

# ✅ exists() — count() yerine
if Order.objects.filter(user=user, status="active").exists():
    ...
```

## Model Tasarımı

```python
from django.db import models
from django.utils import timezone
import uuid

class TimestampedModel(models.Model):
    """Abstract base — tüm modellerde kullan"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeleteModel(TimestampedModel):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    class Meta:
        abstract = True

class Order(SoftDeleteModel):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,  # CASCADE yerine PROTECT — veri kaybını önle
        related_name="orders",
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
        db_index=True,
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]
        ordering = ["-created_at"]
```

## Signals — Dikkatli Kullan

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        # transaction.on_commit — DB commit sonrası çalış
        transaction.on_commit(lambda: send_order_confirmation.delay(instance.id))
```

## Custom Manager & QuerySet

```python
class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=["pending", "processing"])

    def for_user(self, user):
        return self.filter(user=user)

    def with_totals(self):
        return self.annotate(
            item_count=Count("items"),
            calculated_total=Sum(F("items__price") * F("items__quantity"))
        )

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
```

## Middleware

```python
# middleware.py
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        if hasattr(request, "_start_time"):
            duration = time.monotonic() - request._start_time
            response["X-Request-Duration"] = f"{duration:.3f}s"
            if duration > 1.0:
                logger.warning(
                    "Slow request",
                    extra={"path": request.path, "duration": duration, "method": request.method}
                )
        return response
```

## Celery ile Async Tasks

```python
# tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def send_order_confirmation(self, order_id: str) -> dict:
    try:
        order = Order.objects.select_related("user").get(id=order_id)
        # email gönder...
        return {"status": "sent", "order_id": order_id}
    except Order.DoesNotExist:
        logger.error(f"Order not found: {order_id}")
        raise
```

## Settings Yapısı

```python
# settings/base.py — ortak ayarlar
# settings/development.py — DEBUG=True, local DB
# settings/production.py — güvenli ayarlar

# production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": "require"},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "TIMEOUT": 300,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
```

## Kurallar

- `select_related` / `prefetch_related` — N+1 sorgularını önle
- `transaction.atomic()` — birden fazla DB işlemini wrap et
- `transaction.on_commit()` — side effect'leri commit sonrasına bırak
- Model'de `__str__` ve `Meta.verbose_name` tanımla
- Migration'ları küçük tut, geri alınabilir yap
- `settings/` klasörünü ortama göre böl (base/dev/prod)
- Celery task'larında `bind=True` + retry mekanizması kullan
- Signal'lerde ağır iş yapma, Celery'e devret
