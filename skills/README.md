# 💪 SKILLS - HAZIR GÖREVLER

Bu klasörde 14 farklı skill bulunur. Her biri sık kullanılan karmaşık görevler için hazır şablonlardır.

## 📋 SKILL LİSTESİ

### 🎨 **Frontend Skills**

#### 1. **create-react-component.md**
**Kullanım**: `#create-react-component Button`
**Ne yapar**: Tam React component paketi oluşturur
**Oluşturur**:
- Component.tsx (TypeScript)
- Component.module.css (Styles)
- Component.test.tsx (Tests)
- Component.stories.tsx (Storybook)
- index.ts (Export)

#### 2. **setup-testing.md**
**Kullanım**: `#setup-testing react`
**Ne yapar**: Test altyapısı kurar
**Oluşturur**:
- Jest configuration
- React Testing Library setup
- Mock server (MSW)
- Coverage configuration
- Test utilities

### 🔗 **Backend Skills**

#### 3. **create-api-endpoint.md**
**Kullanım**: `#create-api-endpoint users POST`
**Ne yapar**: REST API endpoint oluşturur
**Oluşturur**:
- Route handler
- Controller
- Service layer
- Validation schema (Zod)
- Unit tests

#### 4. **create-fastapi-endpoint.md**
**Kullanım**: `#create-fastapi-endpoint users POST`
**Ne yapar**: FastAPI endpoint oluşturur
**Oluşturur**:
- Router (FastAPI)
- Pydantic schemas
- Service layer
- SQLAlchemy model
- Pytest tests

#### 5. **create-graphql-api.md**
**Kullanım**: `#create-graphql-api users`
**Ne yapar**: GraphQL API oluşturur
**Oluşturur**:
- Apollo Server setup
- Schema definition
- Resolvers
- DataLoader (N+1 prevention)
- Subscriptions

#### 6. **setup-authentication.md**
**Kullanım**: `#setup-authentication jwt-oauth`
**Ne yapar**: Kimlik doğrulama sistemi kurar
**Oluşturur**:
- JWT access/refresh tokens
- OAuth 2.0 (Google, GitHub)
- Multi-factor authentication
- Password reset flow
- Email verification

### 🗄️ **Database Skills**

#### 7. **setup-database.md**
**Kullanım**: `#setup-database prisma postgresql`
**Ne yapar**: Veritabanı altyapısı kurar
**Oluşturur**:
- ORM configuration (Prisma/TypeORM)
- Connection pooling
- Migrations
- Seeders
- Backup strategy

### 🏗️ **Architecture Skills**

#### 8. **create-microservice.md**
**Kullanım**: `#create-microservice user-service rest`
**Ne yapar**: Mikroservis oluşturur
**Oluşturur**:
- REST/gRPC API
- Database integration
- Message queue (RabbitMQ/Kafka)
- Docker containerization
- Health checks

### 🐳 **DevOps Skills**

#### 9. **create-docker-setup.md**
**Kullanım**: `#create-docker-setup node-api`
**Ne yapar**: Docker konfigürasyonu oluşturur
**Oluşturur**:
- Multi-stage Dockerfile
- docker-compose.yml
- .dockerignore
- Health checks
- Security best practices

#### 10. **setup-ci-cd.md**
**Kullanım**: `#setup-ci-cd github-actions`
**Ne yapar**: CI/CD pipeline kurar
**Oluşturur**:
- GitHub Actions workflows
- Test pipeline
- Security scanning
- Deployment pipeline
- Environment management

#### 11. **setup-monitoring.md**
**Kullanım**: `#setup-monitoring node`
**Ne yapar**: Monitoring altyapısı kurar
**Oluşturur**:
- Winston logger
- Prometheus metrics
- Sentry error tracking
- Health check endpoint
- Performance monitoring

### 🔒 **Security Skills**

#### 12. **security-audit.md**
**Kullanım**: `#security-audit full`
**Ne yapar**: Kapsamlı güvenlik denetimi yapar
**Çalıştırır**:
- Dependency scanning (npm audit, Snyk)
- Secret detection (GitLeaks, TruffleHog)
- Static code analysis (SonarQube, Semgrep)
- Container security (Trivy, Docker Scout)
- API security testing (OWASP ZAP)

#### 13. **setup-secrets-management.md**
**Kullanım**: `#setup-secrets-management aws`
**Ne yapar**: Secret yönetimi kurar
**Oluşturur**:
- .env setup with validation
- AWS Secrets Manager integration
- HashiCorp Vault integration
- Secret rotation setup
- Encryption helpers

### 📝 **Documentation Skills**

#### 14. **create-readme.md**
**Kullanım**: `#create-readme my-awesome-project`
**Ne yapar**: Kapsamlı README oluşturur
**Oluşturur**:
- Project description
- Installation guide
- Usage examples
- API documentation
- Contributing guidelines

## 🚀 NASIL KULLANILIR?

### 1. Skill Çağırma
```
Chat'te: #skill-name parametreler
```

### 2. Örnek Kullanımlar
```bash
# React component oluştur
#create-react-component LoginForm

# API endpoint oluştur
#create-api-endpoint users POST

# Test altyapısı kur
#setup-testing react

# Docker setup
#create-docker-setup node-api

# CI/CD pipeline
#setup-ci-cd github-actions

# Güvenlik audit
#security-audit full

# README oluştur
#create-readme my-project
```

## 🎯 KULLANIM SENARYOLARI

### Yeni React Projesi
```bash
1. #setup-testing react
2. #create-react-component App
3. #create-react-component LoginForm
4. #create-docker-setup react-app
5. #setup-ci-cd github-actions
6. #create-readme my-react-app
```

### Backend API Projesi
```bash
1. #setup-database prisma postgresql
2. #create-api-endpoint users POST
3. #create-api-endpoint auth POST
4. #setup-authentication jwt-oauth
5. #setup-monitoring node
6. #security-audit full
7. #create-docker-setup node-api
```

### Mikroservis Projesi
```bash
1. #create-microservice user-service rest
2. #create-microservice order-service rest
3. #setup-monitoring node
4. #create-docker-setup microservice
5. #setup-ci-cd github-actions
```

### Python FastAPI Projesi
```bash
1. #setup-database prisma postgresql
2. #create-fastapi-endpoint users POST
3. #setup-authentication jwt-oauth
4. #security-audit full
5. #create-docker-setup python-api
```

## 💡 İPUÇLARI

### Skill Kombinasyonları
```
✅ İyi kombinasyonlar:
- setup-testing → create-react-component
- setup-database → create-api-endpoint
- create-docker-setup → setup-ci-cd
- setup-authentication → security-audit

❌ Gereksiz kombinasyonlar:
- Aynı skill'i tekrar çağırmak
- Çelişen teknolojiler (React + Vue)
```

### Parametre Kullanımı
```
✅ İyi parametreler:
#create-react-component LoginForm
#setup-database prisma postgresql
#create-api-endpoint users POST

❌ Kötü parametreler:
#create-react-component (parametre eksik)
#setup-database (teknoloji belirtilmemiş)
```

## 🔧 SORUN GİDERME

### Skill Çalışmıyor
- `#skill-name` formatını kontrol et
- Skill dosyasının `.kiro/skills/` klasöründe olduğunu kontrol et
- Parametrelerin doğru olduğunu kontrol et

### Skill Yavaş Çalışıyor
- Normal! Skill'ler çok dosya oluşturur
- Büyük projeler için daha uzun sürer
- Sabırlı ol, kaliteli kod üretiyor

### Skill Hatalı Dosya Oluşturuyor
- Parametreleri kontrol et
- Teknoloji stack'ini doğru belirt
- Skill'i tekrar çağır

## 📊 SKILL KARŞILAŞTIRMA

| Skill | Hız | Karmaşıklık | Dosya Sayısı | Fayda |
|-------|-----|-------------|--------------|-------|
| create-react-component | Hızlı | Düşük | 5 | Yüksek |
| create-api-endpoint | Orta | Orta | 4 | Yüksek |
| setup-testing | Orta | Orta | 3 | Yüksek |
| create-microservice | Yavaş | Yüksek | 10+ | Çok Yüksek |
| setup-ci-cd | Orta | Yüksek | 3 | Yüksek |
| security-audit | Hızlı | Düşük | 1 | Kritik |
| setup-database | Orta | Orta | 4 | Yüksek |

## 🎉 BAŞARILAR!

Bu skill'ler ile geliştirme hızınız 10x artacak!