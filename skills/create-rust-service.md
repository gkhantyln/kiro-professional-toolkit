# Skill: create-rust-service

## Açıklama
Production-grade Rust servisi oluşturur. Axum + Tokio + SQLx + Tower middleware stack kullanır.

## Kullanım
```
#create-rust-service <servis-adı> [--db postgres|sqlite] [--auth jwt|apikey]
```

## Örnekler
```
#create-rust-service user-service --db postgres --auth jwt
#create-rust-service file-processor --db sqlite
```

## Oluşturulan Yapı
```
<servis-adı>/
├── Cargo.toml
├── Cargo.lock
├── .env.example
├── Dockerfile
├── src/
│   ├── main.rs
│   ├── config.rs
│   ├── error.rs
│   ├── state.rs
│   ├── routes/
│   │   ├── mod.rs
│   │   └── health.rs
│   ├── handlers/
│   │   └── mod.rs
│   ├── models/
│   │   └── mod.rs
│   ├── db/
│   │   ├── mod.rs
│   │   └── migrations/
│   └── middleware/
│       ├── auth.rs
│       └── tracing.rs
└── tests/
    └── integration_test.rs
```

## Üretilen Kod Özellikleri

### Cargo.toml
```toml
[package]
name = "user-service"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = { version = "0.7", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
tower = { version = "0.4", features = ["full"] }
tower-http = { version = "0.5", features = ["cors", "trace", "compression-gzip"] }
sqlx = { version = "0.7", features = ["postgres", "runtime-tokio", "uuid", "chrono", "migrate"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
uuid = { version = "1", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
anyhow = "1"
thiserror = "1"
jsonwebtoken = "9"
config = "0.14"
dotenvy = "0.15"

[dev-dependencies]
axum-test = "14"
tokio-test = "0.4"
```

### main.rs
```rust
use std::net::SocketAddr;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Structured JSON logging
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::try_from_default_env()
            .unwrap_or_else(|_| "info,sqlx=warn".into()))
        .with(tracing_subscriber::fmt::layer().json())
        .init();

    let config = config::Config::from_env()?;
    let state = state::AppState::new(&config).await?;

    // Run migrations
    sqlx::migrate!("./src/db/migrations")
        .run(&state.db)
        .await?;

    let app = routes::create_router(state);
    let addr = SocketAddr::from(([0, 0, 0, 0], config.port));

    tracing::info!("Listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    Ok(())
}
```

### error.rs
```rust
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("Unauthorized")]
    Unauthorized,
    #[error("Validation error: {0}")]
    Validation(String),
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("Internal error")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".into()),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Database(e) => {
                tracing::error!("Database error: {:?}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "Database error".into())
            }
            AppError::Internal(e) => {
                tracing::error!("Internal error: {:?}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".into())
            }
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}

pub type Result<T> = std::result::Result<T, AppError>;
```

### routes/mod.rs
```rust
use axum::{Router, middleware};
use tower_http::{cors::CorsLayer, trace::TraceLayer, compression::CompressionLayer};
use crate::state::AppState;

pub fn create_router(state: AppState) -> Router {
    Router::new()
        .nest("/api/v1", api_routes())
        .route("/health", axum::routing::get(health::handler))
        .layer(TraceLayer::new_for_http())
        .layer(CompressionLayer::new())
        .layer(CorsLayer::permissive())
        .with_state(state)
}

fn api_routes() -> Router<AppState> {
    Router::new()
        .nest("/users", users::router())
        .route_layer(middleware::from_fn(crate::middleware::auth::require_auth))
}
```

## Özellikler
- Axum 0.7 + Tokio async runtime
- SQLx ile compile-time SQL doğrulama
- thiserror ile type-safe error handling
- Tower middleware: CORS, tracing, compression
- JWT authentication middleware
- Structured JSON logging (tracing)
- Docker multi-stage build
- Integration tests
- Health check endpoint
