---
name: create-django-rest-api
description: Production Django REST API with ViewSets, custom permissions, cursor pagination, OpenAPI schema, query optimization, and API versioning
---

# Create Django REST API

Production-ready Django REST API oluşturur:
- ViewSet + Router mimarisi
- Custom permission classes
- Cursor-based pagination
- drf-spectacular (OpenAPI 3.1)
- select_related / prefetch_related optimizasyonu
- API versioning (namespace)
- Bulk operations
- ETag + conditional requests

## Usage
```
#create-django-rest-api <resource-name>
```

## apps/api/v1/views/products.py
```python
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, Count, Avg
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.products.models import Product, Category, Review
from apps.api.v1.serializers.products import (
    ProductListSerializer, ProductDetailSerializer,
    ProductCreateSerializer, ReviewSerializer,
)
from apps.api.v1.filters import ProductFilter
from apps.api.v1.permissions import IsOwnerOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["price", "created_at", "rating"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category", "owner")
            .prefetch_related(
                Prefetch("reviews", queryset=Review.objects.select_related("user").order_by("-created_at")[:5]),
                "tags",
            )
            .annotate(
                review_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
            )
            .filter(is_active=True)
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action in ("create", "update", "partial_update"):
            return ProductCreateSerializer
        return ProductDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        parameters=[OpenApiParameter("ids", str, description="Comma-separated product IDs")],
        responses={200: ProductListSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def bulk_fetch(self, request):
        ids = request.query_params.get("ids", "").split(",")
        qs = self.get_queryset().filter(id__in=ids)
        serializer = ProductListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def review(self, request, pk=None):
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={"request": request, "product": product})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60 * 5))
    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        qs = self.get_queryset().filter(is_featured=True)[:10]
        return Response(ProductListSerializer(qs, many=True).data)
```

## apps/api/v1/permissions.py
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level: only owner can write."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user

class HasAPIKey(permissions.BasePermission):
    """Service-to-service API key auth."""
    def has_permission(self, request, view):
        from apps.core.models import APIKey
        key = request.META.get("HTTP_X_API_KEY")
        if not key:
            return False
        return APIKey.objects.filter(key=key, is_active=True).exists()
```

## apps/api/v1/pagination.py
```python
from rest_framework.pagination import CursorPagination as BaseCursorPagination
from rest_framework.response import Response

class CursorPagination(BaseCursorPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created_at"

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count if hasattr(self.page, "paginator") else None,
            "results": data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "next": {"type": "string", "nullable": True},
                "previous": {"type": "string", "nullable": True},
                "results": schema,
            },
        }
```

## apps/api/v1/filters.py
```python
import django_filters
from apps.products.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category__slug")
    in_stock = django_filters.BooleanFilter(field_name="stock", lookup_expr="gt", label="In stock")
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr="date__gte")

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "category", "in_stock", "created_after"]
```

## config/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.api.v1.views.products import ProductViewSet
from apps.api.v1.views.users import UserViewSet

router_v1 = DefaultRouter()
router_v1.register("products", ProductViewSet, basename="product")
router_v1.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include((router_v1.urls, "v1"))),
    path("api/v1/auth/", include("rest_framework_simplejwt.urls")),
    # OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("health/", include("health_check.urls")),
]
```

## apps/products/managers.py
```python
from django.db import models
from django.db.models import Count, Avg, Q

class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(is_featured=True, is_active=True)

    def with_stats(self):
        return self.annotate(
            review_count=Count("reviews"),
            avg_rating=Avg("reviews__rating"),
        )

    def in_stock(self):
        return self.filter(stock__gt=0)

    def search(self, query: str):
        return self.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()
```
