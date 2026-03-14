---
inclusion: fileMatch
fileMatchPattern: "**/*.rs"
---

# Rust Best Practices

## Ownership & Borrowing

### Ownership rules
```rust
// ✅ Move semantics — transfer ownership
let s1 = String::from("hello");
let s2 = s1;  // s1 moved, no longer valid
// println!("{}", s1);  // ❌ compile error

// ✅ Clone when you need a copy
let s2 = s1.clone();

// ✅ References for borrowing
fn print_len(s: &str) {  // borrow, not own
    println!("{}", s.len());
}
```

### Lifetime annotations
```rust
// ✅ Explicit lifetimes when needed
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// ✅ Struct with references
struct Parser<'a> {
    input: &'a str,
    pos: usize,
}
```

## Error Handling

### Use Result and ? operator
```rust
use std::io;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("Not found: {id}")]
    NotFound { id: String },
    #[error("Validation failed: {field} — {message}")]
    Validation { field: String, message: String },
    #[error(transparent)]
    Io(#[from] io::Error),
}

pub type Result<T> = std::result::Result<T, AppError>;

// ✅ Propagate with ?
async fn get_user(id: &str) -> Result<User> {
    let user = db.find_user(id).await?;  // auto-converts error
    user.ok_or(AppError::NotFound { id: id.to_string() })
}
```

### Never use unwrap() in production
```rust
// ❌ Bad — panics in production
let value = map.get("key").unwrap();

// ✅ Good — handle the None case
let value = map.get("key").ok_or(AppError::NotFound { id: "key".into() })?;

// ✅ Or provide a default
let value = map.get("key").unwrap_or(&default_value);

// ✅ expect() only in tests or truly impossible cases
let config = Config::load().expect("Config must be valid at startup");
```

## Async Rust (Tokio)

### Async patterns
```rust
use tokio::sync::{RwLock, Semaphore};
use std::sync::Arc;

// ✅ Shared state with Arc<RwLock<T>>
#[derive(Clone)]
pub struct AppState {
    pub db: Arc<sqlx::PgPool>,
    pub cache: Arc<RwLock<HashMap<String, String>>>,
    pub semaphore: Arc<Semaphore>,
}

// ✅ Concurrent tasks with join!
async fn fetch_all(ids: Vec<String>) -> Result<Vec<User>> {
    let futures: Vec<_> = ids.iter().map(|id| get_user(id)).collect();
    let results = futures::future::join_all(futures).await;
    results.into_iter().collect()
}

// ✅ Bounded concurrency with Semaphore
async fn process_batch(items: Vec<Item>) -> Result<()> {
    let sem = Arc::new(Semaphore::new(10));  // max 10 concurrent
    let mut handles = vec![];
    for item in items {
        let permit = sem.clone().acquire_owned().await?;
        handles.push(tokio::spawn(async move {
            let _permit = permit;  // released on drop
            process_item(item).await
        }));
    }
    for h in handles { h.await??; }
    Ok(())
}
```

## Type System

### Newtype pattern for type safety
```rust
// ✅ Prevent mixing up IDs
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct UserId(uuid::Uuid);

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct OrderId(uuid::Uuid);

// Now you can't accidentally pass OrderId where UserId is expected
fn get_user(id: UserId) -> Result<User> { ... }
```

### Builder pattern
```rust
#[derive(Default)]
pub struct RequestBuilder {
    url: Option<String>,
    timeout: Duration,
    headers: HashMap<String, String>,
}

impl RequestBuilder {
    pub fn url(mut self, url: impl Into<String>) -> Self {
        self.url = Some(url.into()); self
    }
    pub fn timeout(mut self, t: Duration) -> Self {
        self.timeout = t; self
    }
    pub fn header(mut self, k: impl Into<String>, v: impl Into<String>) -> Self {
        self.headers.insert(k.into(), v.into()); self
    }
    pub fn build(self) -> Result<Request> {
        Ok(Request {
            url: self.url.ok_or(AppError::Validation {
                field: "url".into(), message: "required".into()
            })?,
            timeout: self.timeout,
            headers: self.headers,
        })
    }
}
```

## Performance

### Avoid unnecessary allocations
```rust
// ❌ Bad — allocates String
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// ✅ Good — use Cow for conditional allocation
use std::borrow::Cow;
fn normalize(s: &str) -> Cow<str> {
    if s.chars().all(|c| c.is_lowercase()) {
        Cow::Borrowed(s)  // no allocation
    } else {
        Cow::Owned(s.to_lowercase())  // allocates only when needed
    }
}

// ✅ Use iterators — lazy, zero-cost abstractions
let sum: i64 = data.iter()
    .filter(|&&x| x > 0)
    .map(|&x| x as i64)
    .sum();
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tokio::test;

    #[test]
    async fn test_get_user_returns_user_when_exists() {
        let db = setup_test_db().await;
        let user = create_test_user(&db).await;
        let result = get_user(&user.id.to_string()).await;
        assert!(result.is_ok());
        assert_eq!(result.unwrap().email, user.email);
    }

    #[test]
    async fn test_get_user_returns_not_found_for_unknown_id() {
        let result = get_user("nonexistent").await;
        assert!(matches!(result, Err(AppError::NotFound { .. })));
    }
}
```

## Clippy Rules (must-have)
```toml
# .clippy.toml or Cargo.toml
[lints.clippy]
all = "warn"
pedantic = "warn"
nursery = "warn"
unwrap_used = "deny"
expect_used = "warn"
panic = "warn"
```
