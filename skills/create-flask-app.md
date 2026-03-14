---
name: create-flask-app
description: Production Flask 3 application with application factory, Blueprints, SQLAlchemy 2, Flask-JWT-Extended, Marshmallow, Celery, and async views
---

# Create Flask App

Production-ready Flask 3 uygulaması oluşturur:
- Application factory pattern
- Blueprint mimarisi
- SQLAlchemy 2 (async + sync)
- Flask-JWT-Extended (access + refresh)
- Marshmallow schema validation
- Flask-Limiter (rate limiting)
- Celery + Redis
- Flask-Migrate (Alembic)

## Usage
```
#create-flask-app <project-name>
```

## app/__init__.py (Application Factory)
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from celery import Celery
import structlog

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["1000/hour"])
celery_app = Celery()

def create_app(config_name: str = "production") -> Flask:
    app = Flask(__name__)

    # Config
    from app.config import config_map
    app.config.from_object(config_map[config_name])

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["ALLOWED_ORIGINS"]}})

    # Celery
    celery_app.config_from_object(app.config, namespace="CELERY")
    celery_app.conf.update(app.config)

    # Blueprints
    from app.api.v1.auth import auth_bp
    from app.api.v1.users import users_bp
    from app.api.v1.health import health_bp

    app.register_blueprint(auth_bp,   url_prefix="/api/v1/auth")
    app.register_blueprint(users_bp,  url_prefix="/api/v1/users")
    app.register_blueprint(health_bp, url_prefix="/health")

    # Error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
    )

    return app
```

## app/config.py
```python
import os
from datetime import timedelta

class BaseConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "max_overflow": 20,
    }
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = "HS256"
    CELERY_BROKER_URL    = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://localhost/myapp_dev")
    SQLALCHEMY_ECHO = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
```

## app/models/user.py
```python
import uuid
from datetime import datetime, timezone
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email      = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    _password  = db.Column("password_hash", db.String(255), nullable=False)
    role       = db.Column(db.Enum("user", "admin", "moderator", name="user_role"), default="user")
    is_active  = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.Index("ix_users_email_active", "email", "is_active"),
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, value: str):
        self._password = generate_password_hash(value, method="pbkdf2:sha256:600000")

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self._password, password)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }
```

## app/api/v1/auth.py
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt,
)
from marshmallow import Schema, fields, validate, ValidationError
from app import db, limiter
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

class RegisterSchema(Schema):
    email    = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=8), load_only=True)

class LoginSchema(Schema):
    email    = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

@auth_bp.post("/register")
@limiter.limit("10/hour")
def register():
    try:
        data = RegisterSchema().load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 422

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(email=data["email"], username=data["username"])
    user.password = data["password"]
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user": user.to_dict(),
        "tokens": {
            "access":  create_access_token(identity=str(user.id)),
            "refresh": create_refresh_token(identity=str(user.id)),
        },
    }), 201

@auth_bp.post("/login")
@limiter.limit("20/hour")
def login():
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 422

    user = User.query.filter_by(email=data["email"], is_active=True).first()
    if not user or not user.verify_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "access":  create_access_token(identity=str(user.id)),
        "refresh": create_refresh_token(identity=str(user.id)),
    })

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify({"access": create_access_token(identity=identity)})

@auth_bp.delete("/logout")
@jwt_required()
def logout():
    # Add JTI to blocklist (implement with Redis)
    from app.services.token_blocklist import add_to_blocklist
    jti = get_jwt()["jti"]
    add_to_blocklist(jti)
    return jsonify({"message": "Logged out"}), 200
```

## app/errors.py
```python
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import structlog

logger = structlog.get_logger()

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": "Validation failed", "details": e.messages}), 422

    @app.errorhandler(IntegrityError)
    def handle_integrity(e):
        return jsonify({"error": "Database constraint violation"}), 409

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(429)
    def handle_429(e):
        return jsonify({"error": "Too many requests", "retry_after": e.retry_after}), 429

    @app.errorhandler(500)
    def handle_500(e):
        logger.exception("Unhandled error", exc_info=e)
        return jsonify({"error": "Internal server error"}), 500
```

## wsgi.py
```python
from app import create_app
app = create_app("production")

if __name__ == "__main__":
    app.run()
```

## Dockerfile
```dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

FROM base AS builder
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM base AS production
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
EXPOSE 8000
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "gevent", "--worker-connections", "1000", "--timeout", "30"]
```
