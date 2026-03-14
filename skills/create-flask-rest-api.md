---
name: create-flask-rest-api
description: Production Flask REST API with Flask-Smorest, OpenAPI 3, MethodView, SQLAlchemy 2 async, caching, and service layer pattern
---

# Create Flask REST API

Production-ready Flask REST API oluşturur:
- Flask-Smorest (OpenAPI 3.1 otomatik)
- MethodView + Blueprint mimarisi
- SQLAlchemy 2 async session
- Service layer pattern
- Flask-Caching (Redis)
- ETag + conditional GET
- Bulk endpoints
- API key + JWT dual auth

## Usage
```
#create-flask-rest-api <resource-name>
```

## app/api/v1/resources/products.py
```python
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, EXCLUDE
from app import db, cache
from app.models.product import Product
from app.services.product_service import ProductService
from app.api.decorators import require_role, etag_cached

blp = Blueprint("products", __name__, url_prefix="/api/v1/products", description="Product operations")

class ProductQuerySchema(Schema):
    class Meta: unknown = EXCLUDE
    page      = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page  = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))
    search    = fields.Str(load_default=None)
    category  = fields.Str(load_default=None)
    min_price = fields.Float(load_default=None)
    max_price = fields.Float(load_default=None)
    sort_by   = fields.Str(load_default="created_at", validate=validate.OneOf(["price", "created_at", "name"]))
    order     = fields.Str(load_default="desc", validate=validate.OneOf(["asc", "desc"]))

class ProductSchema(Schema):
    id          = fields.UUID(dump_only=True)
    name        = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(load_default="")
    price       = fields.Float(required=True, validate=validate.Range(min=0))
    stock       = fields.Int(load_default=0)
    category_id = fields.UUID(required=True)
    is_active   = fields.Bool(dump_only=True)
    created_at  = fields.DateTime(dump_only=True)

class ProductListSchema(Schema):
    items      = fields.List(fields.Nested(ProductSchema))
    total      = fields.Int()
    page       = fields.Int()
    per_page   = fields.Int()
    pages      = fields.Int()

@blp.route("/")
class ProductList(MethodView):
    @blp.arguments(ProductQuerySchema, location="query")
    @blp.response(200, ProductListSchema)
    @cache.cached(timeout=60, query_string=True)
    def get(self, args):
        """List products with filtering and pagination."""
        return ProductService.list_products(**args)

    @jwt_required()
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        """Create a new product."""
        user_id = get_jwt_identity()
        return ProductService.create_product(product_data, owner_id=user_id)

@blp.route("/<uuid:product_id>")
class ProductDetail(MethodView):
    @blp.response(200, ProductSchema)
    @etag_cached(timeout=300)
    def get(self, product_id):
        """Get product by ID."""
        product = Product.query.get_or_404(product_id)
        return product

    @jwt_required()
    @blp.arguments(ProductSchema(partial=True))
    @blp.response(200, ProductSchema)
    def patch(self, product_data, product_id):
        """Partially update a product."""
        return ProductService.update_product(product_id, product_data, get_jwt_identity())

    @jwt_required()
    @blp.response(204)
    def delete(self, product_id):
        """Delete a product."""
        ProductService.delete_product(product_id, get_jwt_identity())

@blp.route("/bulk")
class ProductBulk(MethodView):
    class BulkCreateSchema(Schema):
        items = fields.List(fields.Nested(ProductSchema), required=True, validate=validate.Length(min=1, max=100))

    class BulkResponseSchema(Schema):
        created = fields.List(fields.Nested(ProductSchema))
        errors  = fields.List(fields.Dict())

    @jwt_required()
    @require_role("admin")
    @blp.arguments(BulkCreateSchema)
    @blp.response(207, BulkResponseSchema)
    def post(self, data):
        """Bulk create products (admin only)."""
        return ProductService.bulk_create(data["items"], get_jwt_identity())
```

## app/services/product_service.py
```python
from uuid import UUID
from flask import abort
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from app import db
from app.models.product import Product

class ProductService:
    @staticmethod
    def list_products(
        page: int = 1,
        per_page: int = 20,
        search: str | None = None,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> dict:
        query = (
            Product.query
            .options(selectinload(Product.category), selectinload(Product.tags))
            .filter(Product.is_active == True)
        )

        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )
        if category:
            query = query.join(Product.category).filter_by(slug=category)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        sort_col = getattr(Product, sort_by)
        query = query.order_by(sort_col.desc() if order == "desc" else sort_col.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def create_product(data: dict, owner_id: str) -> Product:
        product = Product(**data, owner_id=owner_id)
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)
        return product

    @staticmethod
    def update_product(product_id: UUID, data: dict, user_id: str) -> Product:
        product = Product.query.get_or_404(product_id)
        if str(product.owner_id) != user_id:
            abort(403, message="Not authorized")
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id: UUID, user_id: str):
        product = Product.query.get_or_404(product_id)
        if str(product.owner_id) != user_id:
            abort(403, message="Not authorized")
        product.is_active = False  # soft delete
        db.session.commit()

    @staticmethod
    def bulk_create(items: list[dict], owner_id: str) -> dict:
        created, errors = [], []
        for i, item in enumerate(items):
            try:
                product = Product(**item, owner_id=owner_id)
                db.session.add(product)
                db.session.flush()
                created.append(product)
            except Exception as e:
                errors.append({"index": i, "error": str(e)})
                db.session.rollback()
        db.session.commit()
        return {"created": created, "errors": errors}
```

## app/api/decorators.py
```python
import hashlib
import json
from functools import wraps
from flask import request, make_response, current_app
from flask_jwt_extended import get_jwt

def require_role(*roles: str):
    """Decorator to restrict endpoint to specific JWT roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role", "user")
            if user_role not in roles:
                from flask_smorest import abort
                abort(403, message=f"Role '{user_role}' not authorized. Required: {roles}")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def etag_cached(timeout: int = 300):
    """ETag-based conditional GET caching."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            # Generate ETag from response content
            content = json.dumps(result, default=str, sort_keys=True)
            etag = hashlib.md5(content.encode()).hexdigest()

            if request.headers.get("If-None-Match") == etag:
                return make_response("", 304)

            response = make_response(result)
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = f"private, max-age={timeout}"
            return response
        return wrapper
    return decorator
```

## app/api/v1/__init__.py
```python
from flask_smorest import Api

def register_api(app):
    api = Api(app)
    from app.api.v1.resources.products import blp as products_blp
    from app.api.v1.resources.users import blp as users_blp
    from app.api.v1.resources.auth import blp as auth_blp
    api.register_blueprint(products_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(auth_blp)
    return api
```

## config additions for Flask-Smorest
```python
# Add to BaseConfig:
API_TITLE = "My API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.1.0"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/docs"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
OPENAPI_REDOC_PATH = "/redoc"
OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"
```
