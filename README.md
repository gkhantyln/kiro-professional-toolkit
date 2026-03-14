# 🚀 Kiro Professional Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/gkhantyln/kiro-professional-toolkit.svg)](https://github.com/gkhantyln/kiro-professional-toolkit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/gkhantyln/kiro-professional-toolkit.svg)](https://github.com/gkhantyln/kiro-professional-toolkit/network)
[![GitHub issues](https://img.shields.io/github/issues/gkhantyln/kiro-professional-toolkit.svg)](https://github.com/gkhantyln/kiro-professional-toolkit/issues)

**Complete professional development toolkit for Kiro IDE** - Transform your development workflow with 32 Expert Hooks, 34 AI Agents, 50 Skills, 22 Steering Rules & 44 MCP Integrations.

> 🎯 **Enterprise-grade development environment in one package**

## 📦 İÇERİK

### 🤖 Agents (34 Adet)
Bağımsız AI uzmanları:

**Kod Kalitesi & İnceleme**
- **Code Reviewer**: PR review, SOLID, security, performance
- **Refactoring Assistant**: Code smell tespiti, safe refactoring
- **Tech Debt Analyzer**: Teknik borç envanteri ve roadmap
- **Dependency Auditor**: CVE tarama, upgrade stratejisi, lisans uyumu

**Test & Güvenlik**
- **Test Generator**: Unit, integration, E2E test üretimi
- **Security Scanner**: OWASP Top 10, vulnerability scanning
- **Infrastructure Security**: Cloud security, IAM, secrets management
- **Accessibility Auditor**: WCAG 2.1 AA/AAA, ARIA, keyboard nav

**Performans & Veritabanı**
- **Performance Analyzer**: Bottleneck tespiti, Core Web Vitals
- **Database Migration Expert**: Zero-downtime migrations, rollback
- **SQL Query Optimizer**: Execution plan, index önerileri, N+1 fix

**Mimari & Tasarım**
- **Backend Architect**: Microservices, CQRS, Event Sourcing, DDD
- **System Design Expert**: Distributed systems, CAP theorem, scalability
- **Architecture Decision Recorder**: ADR yazımı, design pattern seçimi
- **API Architect**: REST/GraphQL/gRPC tasarımı, OpenAPI spec
- **GraphQL Specialist**: Schema tasarımı, DataLoader, federation

**Frontend & Mobile**
- **Frontend Specialist**: React/Vue/Svelte, state management, perf
- **Mobile Developer**: React Native, Flutter, iOS, Android
- **Internationalization Expert**: i18n/l10n, RTL, locale formatting
- **WebSocket & Realtime Expert**: WebSocket, WebRTC, SSE, pub/sub

**DevOps & Cloud**
- **DevOps Engineer**: CI/CD, Docker, Kubernetes, Terraform
- **Cloud Cost Optimizer**: AWS/GCP/Azure maliyet analizi, FinOps
- **Incident Responder**: Post-mortem, RCA, runbook, SLO/SLA
- **Microservices Debugger**: Distributed tracing, cascading failure
- **Release Manager**: Changelog, semantic versioning, hotfix

**AI & Veri**
- **ML Engineer**: MLOps, model deployment, RAG pipeline
- **Data Engineer**: ETL pipeline, dbt, Spark, data modeling
- **Prompt Engineer**: LLM prompt optimizasyonu, RAG tasarımı

**Dokümantasyon & Onboarding**
- **Documentation Writer**: API docs, README, architecture docs
- **Code Onboarder**: Codebase özeti, getting started rehberi

**Özel Domain**
- **Blockchain Developer**: Smart contract audit, gas optimizasyonu
- **CLI Tool Builder**: CLI araçları, shell scripts, TUI
- **Java Spring Expert**: Spring Boot 3, Java 21 virtual threads, JPA optimizasyonu, Testcontainers
- **FinOps Architect**: Maliyet-mimari dengesi, right-sizing, IaC cost analysis

### 🎯 Hooks (32 Adet)
Uzmanlık modları:
- **Enterprise Dev Workflow**: Tam SDLC workflow, 7 rol, 5 quality gate
- **Enterprise Dev Team**: 5 rol ekip yapısı (Owner, Frontend, Backend, UI/UX, QA)
- **Enterprise Dev Team V2**: Enterprise Dev Team'in geliştirilmiş versiyonu
- **Architecture Review**: ADR formatı, SOLID, design decisions
- **Pre-Commit Quality Gate**: Secrets, console.log, SQL injection kontrolü
- **Post-Write Code Review**: 6 kategori otomatik review
- **Security Audit Shell**: Tehlikeli shell komutlarını engeller
- **Pre-Deployment Checklist**: 10 kategori deployment validasyonu
- **Accessibility Validator**: WCAG 2.1 AA compliance kontrolü
- **Auto Test Generator**: Test stratejisi ve test case önerileri
- **Performance Monitoring**: Core Web Vitals, API metrics analizi
- **Git Commit Standards**: Conventional commits formatı
- **Security Expert**: Güvenlik uzmanı
- **Architecture Expert**: Mimari uzmanı
- **QA/Testing Expert**: Test uzmanı
- **Accessibility Expert**: Erişilebilirlik uzmanı
- **Mobile Dev Expert**: Mobil geliştirme
- **Database Expert**: Veritabanı uzmanı
- **DevOps/SRE Expert**: Altyapı uzmanı
- **Game Dev Expert**: Oyun geliştirme
- **ML/AI Expert**: Yapay zeka uzmanı
- **Data Science Expert**: Veri bilimi
- **Blockchain/Web3 Expert**: Blockchain uzmanı
- **API Design Expert**: API tasarım uzmanı
- **Performance Expert**: Performans uzmanı
- **Tech Writer Expert**: Teknik yazar
- **Product Manager Expert**: Ürün yöneticisi
- **IoT/Embedded Expert**: IoT uzmanı
- **Tech Lawyer**: Teknoloji hukuku
- **Tech Psychologist**: Geliştirici psikolojisi
- **Dependency Update Checker**: Güvenlik açıkları, outdated paketler, upgrade yolu
- **License Compliance**: GPL/AGPL riski, lisans uyumluluğu kontrolü

### 📋 Steering (22 Adet)
Otomatik kurallar — dosya tipine göre tetiklenir:

**AUTO (Her Zaman Aktif)**
- **coding-standards.md**: SOLID, clean code, git commit standartları
- **secrets-security.md**: Secret güvenliği, env var kuralları

**FILE MATCH (Dosya Tipine Göre)**
- **typescript-guidelines.md**: Type safety, generics, strict mode
- **python-best-practices.md**: PEP 8, type hints, async/await, pytest
- **go-best-practices.md**: Go idioms, error handling, concurrency
- **cpp-best-practices.md**: C++23, RAII, std::expected, coroutines, SIMD
- **rust-best-practices.md**: Ownership, Result/?, async Tokio, Clippy
- **java-best-practices.md**: Spring Boot 3, Java 21 virtual threads, JPA, Testcontainers
- **kotlin-best-practices.md**: Coroutines, Flow, sealed classes, KMP
- **django-best-practices.md**: ORM optimizasyonu, N+1 önleme, Celery
- **react-best-practices.md**: Hooks, useMemo/useCallback, RSC, Zustand
- **graphql-standards.md**: Schema tasarımı, DataLoader, Relay pagination, depth limiting
- **api-design-guidelines.md**: RESTful standards, pagination, rate limiting
- **database-best-practices.md**: Schema design, indexing, query optimization
- **frontend-standards.md**: Component structure, state management, a11y
- **security-headers.md**: CSP, HSTS, CORS, rate limiting
- **docker-kubernetes.md**: Multi-stage build, K8s manifests, HPA, PDB
- **infrastructure-as-code.md**: Terraform modules, remote state, Pulumi, CDK
- **performance-optimization.md**: Core Web Vitals, caching, profiling
- **testing-standards.md**: Test piramidi, AAA pattern, coverage hedefleri

**MANUAL (Chat'te #isim ile çağır)**
- **security-checklist.md**: OWASP Top 10, pre-deployment audit
- **microservices-patterns.md**: Circuit breaker, Saga, Outbox, CQRS

### 💪 Skills (50 Adet)
Hazır görevler:

**Frontend**
- **create-react-component**: React component oluştur (TSX + Test + Storybook)
- **create-nextjs-app**: Next.js 15 App Router projesi kur
- **create-design-system**: Token tabanlı design system oluştur
- **setup-testing**: Test altyapısı kur (Vitest + RTL + Playwright)

**Backend**
- **create-api-endpoint**: REST API endpoint oluştur
- **create-fastapi-endpoint**: FastAPI endpoint oluştur
- **create-graphql-api**: GraphQL API oluştur
- **create-go-service**: Production Go servisi oluştur
- **create-python-service**: Production Python servisi oluştur
- **setup-authentication**: JWT + OAuth2 + MFA kur
- **create-openapi-spec**: OpenAPI 3.1 spec oluştur

**Database**
- **setup-database**: ORM + pooling + migrations kur

**Architecture**
- **create-microservice**: Mikroservis oluştur
- **setup-event-driven**: Kafka + Outbox + Saga kur

**Mobile**
- **create-mobile-app**: React Native + Expo uygulaması oluştur
- **create-chrome-extension**: Chrome Extension MV3 oluştur

**DevOps**
- **create-docker-setup**: Multi-stage Docker konfigürasyonu
- **setup-ci-cd**: GitHub Actions CI/CD pipeline
- **setup-kubernetes**: K8s manifests + HPA + RBAC
- **setup-terraform**: IaC modules + remote state

**Observability**
- **setup-monitoring**: Winston + Prometheus + Sentry
- **setup-observability**: OpenTelemetry + Jaeger + Grafana

**Caching & Messaging**
- **setup-redis-cache**: Redis + cache-aside + distributed lock
- **setup-websocket-server**: Socket.io + Redis adapter + presence

**Payments**
- **setup-stripe-payments**: Subscriptions + webhooks + portal

**AI/ML**
- **setup-ml-pipeline**: MLflow + Optuna + FastAPI serving
- **setup-data-pipeline**: Airflow + dbt + Great Expectations

**Feature Management**
- **setup-feature-flags**: OpenFeature + LaunchDarkly + A/B testing

**Security**
- **security-audit**: OWASP + Snyk + Semgrep + Trivy
- **setup-secrets-management**: AWS Secrets Manager + Vault

**Documentation**
- **create-readme**: Kapsamlı README oluştur

**Django & Flask**
- **create-django-app**: Django 5 + Custom User + DRF + SimpleJWT + Celery + cachalot
- **create-django-rest-api**: ViewSet + cursor pagination + drf-spectacular + query optimization
- **create-flask-app**: Flask 3 factory + Blueprint + SQLAlchemy 2 + JWT + Marshmallow + Celery
- **create-flask-rest-api**: Flask-Smorest + OpenAPI 3.1 + MethodView + service layer + ETag

**Python Advanced**
- **create-python-async-worker**: Celery + asyncio + circuit breaker + DLQ + Prometheus
- **create-python-grpc-service**: gRPC + protobuf + async interceptors + reflection
- **setup-python-testing-advanced**: Hypothesis + mutmut + Pact + pytest-benchmark
- **create-python-cli-tool**: Typer + Rich TUI + async + plugin architecture + hatch
- **setup-python-package**: hatch + src layout + py.typed + OIDC PyPI publish

**C++ Advanced**
- **create-cpp-modern-service**: C++23 + Boost.Asio + coroutines + spdlog + vcpkg
- **setup-cpp-build-system**: CMake presets + Conan 2 + sanitizers + clang-tidy + fuzzing
- **create-cpp-high-performance-lib**: Lock-free SPSC + SIMD AVX2 + memory pool + SoA
- **create-cpp-embedded-firmware**: FreeRTOS + HAL abstraction + HSM + watchdog + OTA
- **create-cpp-game-engine-component**: Archetype ECS + job system + SIMD math + work-stealing

**Rust & Java**
- **create-rust-service**: Axum + Tokio + SQLx + Tower middleware + OpenTelemetry
- **create-java-spring-service**: Spring Boot 3.3 + Java 21 virtual threads + Testcontainers + GraalVM

**GraphQL & Messaging**
- **setup-graphql-server**: Apollo/Yoga + Pothos schema builder + DataLoader + persisted queries
- **setup-message-queue**: RabbitMQ + AWS SQS + DLQ + retry/backoff + Outbox pattern

**Edge & CDN**
- **setup-cdn-edge**: Cloudflare Workers + Hono + Durable Objects + KV + R2

### 🔌 MCP Servers (44 Adet)
Dış sistem entegrasyonları:

**Temel (Varsayılan Aktif)**
- **filesystem**: Dosya sistemi erişimi ✅
- **memory**: Kalıcı hafıza ✅
- **sequential-thinking**: Gelişmiş düşünme ✅

**Geliştirme & Versiyon Kontrol**
- **github**: GitHub repo, issue, PR yönetimi
- **gitlab**: GitLab repo, MR, CI/CD pipeline
- **git**: Yerel Git işlemleri

**Veritabanı**
- **postgres**: PostgreSQL veritabanı
- **sqlite**: SQLite veritabanı
- **mongodb**: MongoDB NoSQL (Official)
- **redis**: Redis cache ve pub/sub
- **supabase**: Supabase (Postgres + Auth + Storage)
- **neon**: Neon serverless Postgres

**Proje Yönetimi**
- **notion**: Notion workspace (Official)
- **linear**: Linear issue tracker (Official)
- **jira**: Jira issue ve sprint yönetimi
- **confluence**: Atlassian Confluence dokümantasyon
- **airtable**: Airtable veritabanı ve tablolar

**İletişim**
- **slack**: Slack mesajlaşma
- **discord**: Discord bot entegrasyonu
- **twilio**: SMS ve WhatsApp bildirimleri

**Cloud & Altyapı**
- **docker**: Docker container yönetimi
- **kubernetes**: Kubernetes cluster yönetimi
- **vercel**: Vercel deployment yönetimi
- **cloudflare**: Cloudflare Workers, KV, R2, DNS (Official)
- **aws-kb-retrieval**: AWS Knowledge Base
- **aws-docs**: AWS resmi dokümantasyon arama

**Monitoring & Observability**
- **sentry**: Hata izleme (Official)
- **datadog**: Metrics, log ve trace izleme (Official)
- **grafana**: Dashboard ve alerting (Official)
- **pagerduty**: Incident yönetimi

**Arama & Web**
- **brave-search**: Brave Search API
- **tavily**: AI-optimized web arama (LLM için üstün)
- **exa**: Semantic web arama
- **fetch**: Web içerik çekme
- **playwright**: Browser otomasyonu (Official, accessibility tree)
- **puppeteer**: Browser otomasyonu ve scraping

**Tasarım & Medya**
- **figma**: Figma Dev Mode — design specs ve component çıkarma
- **everart**: AI görsel oluşturma

**AI & Dokümantasyon**
- **huggingface**: HuggingFace model hub ve inference
- **context7**: Güncel kütüphane dokümantasyonu
- **markitdown**: PDF/Word/Excel/PPT → Markdown dönüştürme

**Ödeme & Diğer**
- **stripe**: Stripe ödeme sistemi (Official)
- **google-maps**: Google Maps ve geocoding
- **google-workspace**: Gmail, Drive, Docs, Sheets, Calendar (12 servis)

## 🚀 KURULUM

### Otomatik Kurulum (Önerilen)
```bash
# Windows
install.bat

# veya Python ile
python install.py
```

### Manuel Kurulum
1. `.kiro` klasörünü workspace'inizde oluşturun
2. Dosyaları ilgili klasörlere kopyalayın:
   - `agents/` → `.kiro/agents/`
   - `steering/` → `.kiro/steering/`
   - `skills/` → `.kiro/skills/`
   - `hooks/` → `.kiro/hooks/`
   - `mcp/mcp.json` → `.kiro/settings/mcp.json`

## 📖 KULLANIM REHBERİ

### Hooks Nasıl Kullanılır?
1. Sol panel → "Agent Hooks"
2. İstediğin hook'u bul
3. ▶️ Play butonuna tıkla
4. Hook aktif olur

### Skills Nasıl Kullanılır?
Chat'te `#skill-name` yazarak:
```
#create-react-component Button
#setup-testing react
#security-audit full
```

### Steering Nasıl Çalışır?
- **AUTO**: Her zaman aktif
- **FILE MATCH**: Belirli dosyalarda aktif
- **MANUAL**: `#steering-name` ile çağır

### MCP Nasıl Aktif Edilir?
1. `mcp.json` dosyasında `"disabled": false` yap
2. Gerekli API key'leri ekle
3. Kiro'yu yeniden başlat

## ⚙️ MCP KURULUM REHBERİ

### GitHub MCP
1. GitHub → Settings → Developer settings → Personal access tokens
2. Token oluştur (repo, issues, pull_requests izinleri)
3. `mcp.json`'da `GITHUB_PERSONAL_ACCESS_TOKEN` alanına yapıştır
4. `"disabled": false` yap

### GitLab MCP
1. GitLab → User Settings → Access Tokens
2. Token oluştur (api, read_repository izinleri)
3. `GITLAB_PERSONAL_ACCESS_TOKEN` alanına yapıştır
4. `"disabled": false` yap

### Brave Search MCP
1. https://brave.com/search/api/ → API key al
2. `BRAVE_API_KEY` alanına yapıştır
3. `"disabled": false` yap

### Tavily MCP (Önerilen Arama)
1. https://tavily.com → API key al (ücretsiz tier mevcut)
2. `TAVILY_API_KEY` alanına yapıştır
3. `"disabled": false` yap

### PostgreSQL MCP
1. Connection string'i güncelle: `postgresql://user:pass@host:port/db`
2. `"disabled": false` yap

### MongoDB MCP
1. `MDB_MCP_CONNECTION_STRING` alanına connection string yapıştır
2. `"disabled": false` yap

### Redis MCP
1. `REDIS_URL` alanını güncelle: `redis://localhost:6379`
2. `"disabled": false` yap

### Supabase MCP
1. Supabase Dashboard → Account → Access Tokens
2. `SUPABASE_ACCESS_TOKEN` alanına yapıştır
3. `"disabled": false` yap

### Neon MCP
1. https://neon.tech → API Keys → New API Key
2. `NEON_API_KEY` alanına yapıştır
3. `"disabled": false` yap

### Notion MCP (Official)
1. https://www.notion.so/my-integrations → New Integration
2. Token'ı `OPENAPI_MCP_HEADERS` içindeki `Bearer YOUR_NOTION_TOKEN` kısmına yapıştır
3. `"disabled": false` yap

### Linear MCP
1. Linear → Settings → API → Personal API Keys
2. `LINEAR_API_KEY` alanına yapıştır
3. `"disabled": false` yap

### Jira MCP
1. https://id.atlassian.com/manage-profile/security/api-tokens → Token oluştur
2. `JIRA_HOST`, `JIRA_EMAIL`, `JIRA_API_TOKEN` alanlarını doldur
3. `"disabled": false` yap

### Confluence MCP
1. Jira ile aynı API token kullanılabilir
2. `CONFLUENCE_HOST`, `CONFLUENCE_EMAIL`, `CONFLUENCE_API_TOKEN` alanlarını doldur
3. `"disabled": false` yap

### Stripe MCP (Official)
1. Stripe Dashboard → Developers → API Keys → Secret key
2. `STRIPE_SECRET_KEY` alanına yapıştır
3. `"disabled": false` yap

### Figma MCP
1. Figma → Account Settings → Personal Access Tokens
2. `FIGMA_API_KEY` alanına yapıştır ve args içindeki `""` kısmını da doldur
3. `"disabled": false` yap

### Vercel MCP
1. Vercel Dashboard → Settings → Tokens → Create Token
2. `VERCEL_TOKEN` alanına yapıştır
3. `"disabled": false` yap

### Cloudflare MCP (Official)
1. Cloudflare Dashboard → My Profile → API Tokens → Create Token
2. `CLOUDFLARE_API_TOKEN` ve `CLOUDFLARE_ACCOUNT_ID` alanlarını doldur
3. `"disabled": false` yap

### Datadog MCP (Official)
1. Datadog → Organization Settings → API Keys + Application Keys
2. `DD_API_KEY` ve `DD_APP_KEY` alanlarını doldur
3. `"disabled": false` yap

### Grafana MCP (Official)
1. Grafana → Administration → Service Accounts → Add token
2. `GRAFANA_URL` ve `GRAFANA_API_KEY` alanlarını doldur
3. `"disabled": false` yap

### Sentry MCP (Official)
1. Sentry → Settings → Auth Tokens → Create New Token
2. `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT` alanlarını doldur
3. `"disabled": false` yap

### Google Workspace MCP (12 Servis)
1. Google Cloud Console → OAuth 2.0 credentials oluştur
2. `GOOGLE_CLIENT_ID` ve `GOOGLE_CLIENT_SECRET` alanlarını doldur
3. `uvx` kurulu olmalı: `pip install uv`
4. `"disabled": false` yap

### AWS Documentation MCP
1. API key gerektirmez
2. `uvx` kurulu olmalı: `pip install uv`
3. `"disabled": false` yap

### Playwright MCP (Official)
1. API key gerektirmez
2. `"disabled": false` yap

### Docker MCP (API key gerektirmez)
1. Sadece `"disabled": false` yap

### Puppeteer MCP (API key gerektirmez)
1. Sadece `"disabled": false` yap

### Context7 MCP (API key gerektirmez)
1. Sadece `"disabled": false` yap

### MarkItDown MCP (API key gerektirmez)
1. `uvx` kurulu olmalı: `pip install uv`
2. `"disabled": false` yap

### Exa MCP
1. https://exa.ai → Dashboard → API Keys
2. `EXA_API_KEY` alanına yapıştır
3. `"disabled": false` yap

### HuggingFace MCP
1. https://huggingface.co/settings/tokens → New Token
2. `HF_TOKEN` alanına yapıştır
3. `"disabled": false` yap

### Discord MCP
1. Discord Developer Portal → New Application → Bot → Token
2. `DISCORD_TOKEN` ve `DISCORD_GUILD_ID` alanlarını doldur
3. `"disabled": false` yap

### Twilio MCP
1. Twilio Console → Account SID ve Auth Token
2. `TWILIO_ACCOUNT_SID` ve `TWILIO_AUTH_TOKEN` alanlarını doldur
3. `"disabled": false` yap

### Airtable MCP
1. https://airtable.com/create/tokens → Personal Access Token
2. `AIRTABLE_API_KEY` ve `AIRTABLE_BASE_ID` alanlarını doldur
3. `"disabled": false` yap

### PagerDuty MCP
1. PagerDuty → My Profile → User Settings → API Access Key
2. `PAGERDUTY_API_KEY` alanına yapıştır
3. `"disabled": false` yap

## 🎯 KULLANIM ÖRNEKLERİ

### Yeni React Projesi
```
1. #create-react-component LoginForm
2. Hook: Frontend Developer moduna geç
3. Steering: typescript-guidelines otomatik aktif
4. Agent: Code Reviewer ile review
```

### API Geliştirme
```
1. #create-api-endpoint users POST
2. Hook: API Design Expert + Security Expert
3. Steering: api-design-guidelines aktif
4. #security-audit full
```

### Güvenlik Denetimi
```
1. #security-checklist
2. Agent: Security Scanner
3. Hook: Security Expert modu
4. #security-audit full
```

## 🆘 SORUN GİDERME

### Hook Çalışmıyor
- Kiro'yu yeniden başlat
- Hook dosyasının `.kiro/hooks/` klasöründe olduğunu kontrol et

### Skill Çalışmıyor
- `#skill-name` formatını kontrol et
- Skill dosyasının `.kiro/skills/` klasöründe olduğunu kontrol et

### MCP Bağlanamıyor
- API key'lerin doğru olduğunu kontrol et
- Command Palette → "MCP: Reconnect All Servers"
- Kiro'yu yeniden başlat

### Steering Aktif Değil
- Dosya pattern'ini kontrol et
- `.kiro/steering/` klasöründe olduğunu kontrol et

## 📞 DESTEK

Bu paket ile ilgili sorunlar için:
1. README dosyalarını kontrol edin
2. Kurulum adımlarını tekrar gözden geçirin
3. Kiro'yu yeniden başlatmayı deneyin

## 🎉 BAŞARILAR!

Artık tam profesyonel bir Kiro geliştirme ortamına sahipsiniz!

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=gkhantyln/kiro-professional-toolkit&type=Date)](https://star-history.com/#gkhantyln/kiro-professional-toolkit&Date)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Contributors

Thanks to all contributors who have helped make this toolkit better!

<!-- Add contributor images here -->

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact & Support

### 👨‍💻 Maintainer
**Gökhan Taylan**
- 📧 Email: [tylngkhn@gmail.com](mailto:tylngkhn@gmail.com)
- 🐙 GitHub: [@gkhantyln](https://github.com/gkhantyln)
- 🔗 Repository: [kiro-professional-toolkit](https://github.com/gkhantyln/kiro-professional-toolkit)

### 💬 Get Help
- 🐛 **Bug Reports**: [Create an Issue](https://github.com/gkhantyln/kiro-professional-toolkit/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Request Feature](https://github.com/gkhantyln/kiro-professional-toolkit/issues/new?template=feature_request.md)
- ❓ **Questions**: [Start Discussion](https://github.com/gkhantyln/kiro-professional-toolkit/discussions)
- 📧 **Direct Contact**: [tylngkhn@gmail.com](mailto:tylngkhn@gmail.com)

### 🤝 Community
- ⭐ **Star this repo** if you find it useful
- 🍴 **Fork** to contribute your improvements
- 📢 **Share** with your developer friends
- 💝 **Sponsor** the project development

## 🙏 Acknowledgments

- [Kiro IDE](https://kiro.ai) team for creating an amazing development environment
- All contributors who have helped improve this toolkit
- The open-source community for inspiration and feedback

## 📊 Repository Stats

![GitHub repo size](https://img.shields.io/github/repo-size/gkhantyln/kiro-professional-toolkit)
![GitHub language count](https://img.shields.io/github/languages/count/gkhantyln/kiro-professional-toolkit)
![GitHub top language](https://img.shields.io/github/languages/top/gkhantyln/kiro-professional-toolkit)
![GitHub last commit](https://img.shields.io/github/last-commit/gkhantyln/kiro-professional-toolkit)

---

<div align="center">

**Made with ❤️ for the Kiro community**

[⭐ Star this repo](https://github.com/gkhantyln/kiro-professional-toolkit) • [🐛 Report Bug](https://github.com/gkhantyln/kiro-professional-toolkit/issues) • [💡 Request Feature](https://github.com/gkhantyln/kiro-professional-toolkit/issues) • [📧 Contact](mailto:tylngkhn@gmail.com)

</div>