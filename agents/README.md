# 🤖 AGENTS - BAĞIMSIZ AI UZMANLARI

Bu klasörde **34 uzman AI agent'ı** bulunur. Her biri bağımsız çalışır ve özel görevleri vardır.

## 📋 AGENT LİSTESİ

### 🔍 Kod Kalitesi & İnceleme
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Code Reviewer | `code-reviewer.json` | OWASP, SOLID, performance odaklı PR review |
| Refactoring Assistant | `refactoring-assistant.json` | Code smell tespiti, safe refactoring |
| Tech Debt Analyzer | `tech-debt-analyzer.json` | Teknik borç tespiti, önceliklendirme, roadmap |
| Dependency Auditor | `dependency-auditor.json` | CVE tarama, upgrade stratejisi, lisans uyumu |

### 🧪 Test & Güvenlik
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Test Generator | `test-generator.json` | Unit, integration, E2E test üretimi |
| Security Scanner | `security-scanner.json` | OWASP Top 10, vulnerability scanning |
| Infrastructure Security | `infrastructure-security.json` | Cloud security, IAM, secrets management |
| Accessibility Auditor | `accessibility-auditor.json` | WCAG 2.1 AA/AAA, ARIA, keyboard nav |

### ⚡ Performans & Veritabanı
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Performance Analyzer | `performance-analyzer.json` | Bottleneck tespiti, Core Web Vitals |
| Database Migration Expert | `database-migration-expert.json` | Zero-downtime migrations, rollback planları |
| SQL Query Optimizer | `sql-query-optimizer.json` | Execution plan analizi, index önerileri, N+1 fix |

### 🏗️ Mimari & Tasarım
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Backend Architect | `backend-architect.json` | Microservices, CQRS, Event Sourcing, DDD |
| System Design Expert | `system-design-expert.json` | Distributed systems, CAP theorem, scalability |
| Architecture Decision Recorder | `architecture-decision-recorder.json` | ADR yazımı, design pattern seçimi |
| API Architect | `api-architect.json` | REST/GraphQL/gRPC tasarımı, OpenAPI spec |
| GraphQL Specialist | `graphql-specialist.json` | Schema tasarımı, DataLoader, federation |

### 🌐 Frontend & Mobile
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Frontend Specialist | `frontend-specialist.json` | React/Vue/Svelte, state management, perf |
| Mobile Developer | `mobile-developer.json` | React Native, Flutter, iOS, Android |
| Internationalization Expert | `internationalization-expert.json` | i18n/l10n, RTL, locale formatting |
| WebSocket & Realtime Expert | `websocket-realtime-expert.json` | WebSocket, WebRTC, SSE, pub/sub |

### ☁️ DevOps & Cloud
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| DevOps Engineer | `devops-engineer.json` | CI/CD, Docker, Kubernetes, Terraform |
| Cloud Cost Optimizer | `cloud-cost-optimizer.json` | AWS/GCP/Azure maliyet analizi, FinOps |
| Incident Responder | `incident-responder.json` | Post-mortem, RCA, runbook, SLO/SLA |
| Microservices Debugger | `microservices-debugger.json` | Distributed tracing, cascading failure analizi |
| Release Manager | `release-manager.json` | Changelog, semantic versioning, hotfix |

### 🤖 AI & Veri
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| ML Engineer | `ml-engineer.json` | MLOps, model deployment, RAG, monitoring |
| Data Engineer | `data-engineer.json` | ETL pipeline, dbt, Spark, data modeling |
| Prompt Engineer | `prompt-engineer.json` | LLM prompt optimizasyonu, RAG pipeline |

### 📚 Dokümantasyon & Onboarding
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Documentation Writer | `documentation-writer.json` | API docs, README, architecture docs |
| Code Onboarder | `code-onboarder.json` | Codebase özeti, getting started rehberi |

### 🔧 Özel Domain
| Agent | Dosya | Ne Yapar |
|-------|-------|----------|
| Blockchain Developer | `blockchain-developer.json` | Smart contract audit, gas optimizasyonu |
| CLI Tool Builder | `cli-tool-builder.json` | CLI araçları, shell scripts, TUI |
| Java Spring Expert | `java-spring-expert.json` | Spring Boot 3, Java 21, JPA optimizasyonu, Testcontainers |
| FinOps Architect | `finops-architect.json` | Maliyet-mimari dengesi, right-sizing, IaC cost analysis |

---

## 🚀 NASIL KULLANILIR?

Kiro chat'inde agent adını yazarak çağırabilirsiniz:

```
"Code Reviewer olarak bu PR'ı incele"
"SQL Query Optimizer olarak bu sorguyu optimize et"
"System Design Expert olarak URL shortener tasarla"
"Incident Responder olarak bu post-mortem'i yaz"
```

## 🎯 ÖRNEK KULLANIM SENARYOLARI

### Yeni Feature Geliştirme
```
1. Backend Architect → Mimari karar
2. API Architect → API tasarımı
3. Frontend Specialist → UI implementasyonu
4. Test Generator → Test yazımı
5. Code Reviewer → PR review
6. Security Scanner → Güvenlik kontrolü
```

### Production Incident
```
1. Microservices Debugger → Root cause bulma
2. Incident Responder → Post-mortem yazma
3. Release Manager → Hotfix yönetimi
```

### Legacy Code İyileştirme
```
1. Tech Debt Analyzer → Debt envanteri
2. Refactoring Assistant → Safe refactoring
3. Test Generator → Test coverage artırma
4. Performance Analyzer → Bottleneck giderme
```

### Yeni Geliştirici Onboarding
```
1. Code Onboarder → Codebase özeti
2. Architecture Decision Recorder → ADR'ları anlama
3. Documentation Writer → Eksik dokümantasyon
```

## 💡 İPUÇLARI

```
✅ İyi: "React TypeScript projesindeki LoginForm için Jest + RTL ile unit testler yaz"
❌ Kötü: "Test yaz"

✅ İyi: "PostgreSQL'deki users tablosunda 2 saniyelik bu sorguyu optimize et: SELECT..."
❌ Kötü: "Sorgu yavaş"

✅ İyi: "AWS ECS + RDS kullanan bu servisi Kubernetes'e migrate etmek için ADR yaz"
❌ Kötü: "Mimari karar ver"
```
