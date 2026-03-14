# 📋 STEERING - OTOMATIK KURALLAR

Bu klasörde **22 farklı steering dosyası** bulunur. Her biri Kiro'nun davranışını otomatik olarak yönlendirir.

## 📋 STEERING LİSTESİ

### 🔄 **AUTO (Her Zaman Aktif)**

#### 1. **coding-standards.md**
**Ne yapar**: Genel kodlama standartları
**İçerik**: SOLID principles, Clean code, Error handling, Git commit standards, Code review checklist

#### 2. **secrets-security.md**
**Ne yapar**: Secret güvenliği kuralları
**İçerik**: ❌ NEVER commit secrets, ✅ Environment variables, Secret validation, Logging redaction

### 📁 **FILE MATCH (Belirli Dosyalarda Aktif)**

#### 3. **api-design-guidelines.md**
**Pattern**: `**/*.{api,route,controller,endpoint}.*`
**İçerik**: RESTful standards, Status codes, Pagination, Authentication, Rate limiting

#### 4. **typescript-guidelines.md**
**Pattern**: `**/*.{ts,tsx}`
**İçerik**: Type safety, Generics, Utility types, Error handling, Strict mode

#### 5. **python-best-practices.md**
**Pattern**: `**/*.py`
**İçerik**: PEP 8, Type hints, Async/await, pytest, dataclasses, pydantic

#### 6. **go-best-practices.md**
**Pattern**: `**/*.go`
**İçerik**: Go idioms, Error handling, Concurrency, Testing, interfaces

#### 7. **database-best-practices.md**
**Pattern**: `**/*.{sql,prisma,migration,model,entity,repository}.*`
**İçerik**: Schema design, Indexing, Query optimization, Migrations

#### 8. **frontend-standards.md**
**Pattern**: `**/*.{tsx,jsx,vue,svelte}`
**İçerik**: Component structure, State management, Performance, Accessibility

#### 9. **security-headers.md**
**Pattern**: `**/*.{server,app,middleware,config}.*`
**İçerik**: CSP, HSTS, CORS, Rate limiting, Node.js/Python/Go örnekleri

#### 10. **cpp-best-practices.md**
**Pattern**: `**/*.{cpp,cxx,cc,hpp,hxx,h}`
**İçerik**: C++23, RAII, std::expected, coroutines, SIMD, sanitizers, CMake

#### 11. **rust-best-practices.md**
**Pattern**: `**/*.rs`
**İçerik**: Ownership, Result/?, async Tokio, newtype pattern, Clippy, unsafe kuralları

#### 12. **django-best-practices.md**
**Pattern**: `**/*.{py,django}`
**İçerik**: ORM optimizasyonu, N+1 önleme, Signals, Celery, Settings yapısı

#### 13. **react-best-practices.md**
**Pattern**: `**/*.{tsx,jsx}`
**İçerik**: Hooks kuralları, useMemo/useCallback, RSC, Zustand, React Hook Form + Zod

#### 14. **docker-kubernetes.md**
**Pattern**: `**/{Dockerfile,docker-compose*,*.yaml,*.yml,*.k8s.*}`
**İçerik**: Multi-stage build, Non-root user, K8s manifests, HPA, PDB, NetworkPolicy

#### 15. **performance-optimization.md**
**Pattern**: `**/*.{ts,tsx,js,jsx,py,go}`
**İçerik**: Core Web Vitals, Virtual list, Redis cache, DB index, Profiling

#### 16. **testing-standards.md**
**Pattern**: `**/*.{test,spec}.{ts,tsx,js,jsx,py,go}`
**İçerik**: Test piramidi, AAA pattern, pytest fixtures, Table-driven tests, Coverage hedefleri

### 📞 **MANUAL (Sen Çağırınca Aktif)**

#### 17. **security-checklist.md**
**Çağırma**: `#security-checklist`
**İçerik**: Pre-deployment audit, OWASP Top 10, Auth checks, Compliance

#### 18. **microservices-patterns.md**
**Çağırma**: `#microservices-patterns`
**İçerik**: Circuit breaker, Saga, Outbox, CQRS, API Gateway, Health checks

#### 19. **java-best-practices.md**
**Pattern**: `**/*.java`
**İçerik**: Spring Boot 3, Java 21 virtual threads, records, JPA optimizasyonu, Testcontainers

#### 20. **kotlin-best-practices.md**
**Pattern**: `**/*.kt`
**İçerik**: Coroutines, Flow, sealed classes, value classes, KMP, Spring Boot + Kotlin

#### 21. **graphql-standards.md**
**Pattern**: `**/*.{graphql,gql}`
**İçerik**: Schema tasarımı, DataLoader, Relay pagination, persisted queries, depth limiting

#### 22. **infrastructure-as-code.md**
**Pattern**: `**/*.{tf,tfvars,hcl,pulumi,cdk}`
**İçerik**: Terraform modules, remote state, Pulumi TypeScript, AWS CDK, secret management

## 🚀 NASIL ÇALIŞIR?

### AUTO Steering
```
Her zaman aktif → Sürekli yönlendirir
Örnek: Secret yazmaya çalışırsan hemen uyarır
```

### FILE MATCH Steering
```
Belirli dosya açılınca → O dosya tipine özel kurallar aktif
Örnek: LoginForm.tsx açarsan → react-best-practices + typescript-guidelines aktif
```

### MANUAL Steering
```
Chat'te #steering-name yazarsın
Örnek: #microservices-patterns → Microservices pattern rehberi gelir
```

## 🎯 KULLANIM ÖRNEKLERİ

### React Component Yazarken
```
LoginForm.tsx aç →
  typescript-guidelines (FILE MATCH)
  frontend-standards (FILE MATCH)
  react-best-practices (FILE MATCH)
  coding-standards (AUTO)
→ 4 steering birden aktif
```

### Django API Yazarken
```
views.py aç →
  python-best-practices (FILE MATCH)
  django-best-practices (FILE MATCH)
  coding-standards (AUTO)
→ Django ORM + Python kuralları aktif
```

### C++ Servis Yazarken
```
service.cpp aç →
  cpp-best-practices (FILE MATCH)
  coding-standards (AUTO)
→ C++23 + RAII + sanitizer kuralları aktif
```

### Kubernetes Manifest Yazarken
```
deployment.yaml aç →
  docker-kubernetes (FILE MATCH)
  coding-standards (AUTO)
→ K8s best practices aktif
```

### Microservices Tasarımı
```
Chat'te #microservices-patterns yaz →
  Circuit breaker, Saga, Outbox, CQRS rehberi gelir
```

## 📊 STEERING ETKİ ALANLARI

| Steering | Tip | Etki Alanı | Fayda |
|----------|-----|------------|-------|
| coding-standards | AUTO | Tüm kodlar | Çok Yüksek |
| secrets-security | AUTO | Tüm kodlar | Kritik |
| typescript-guidelines | FILE | TS dosyaları | Yüksek |
| python-best-practices | FILE | Python dosyaları | Yüksek |
| cpp-best-practices | FILE | C++ dosyaları | Yüksek |
| rust-best-practices | FILE | Rust dosyaları | Yüksek |
| django-best-practices | FILE | Python/Django | Yüksek |
| react-best-practices | FILE | TSX/JSX | Yüksek |
| docker-kubernetes | FILE | Docker/K8s | Yüksek |
| performance-optimization | FILE | TS/JS/Py/Go | Yüksek |
| testing-standards | FILE | Test dosyaları | Yüksek |
| api-design-guidelines | FILE | API dosyaları | Yüksek |
| database-best-practices | FILE | DB dosyaları | Yüksek |
| frontend-standards | FILE | Frontend | Yüksek |
| security-headers | FILE | Server dosyaları | Kritik |
| go-best-practices | FILE | Go dosyaları | Yüksek |
| java-best-practices | FILE | Java dosyaları | Yüksek |
| kotlin-best-practices | FILE | Kotlin dosyaları | Yüksek |
| graphql-standards | FILE | GraphQL dosyaları | Yüksek |
| infrastructure-as-code | FILE | Terraform/CDK | Yüksek |
| security-checklist | MANUAL | Manuel | Kritik |
| microservices-patterns | MANUAL | Manuel | Yüksek |
