# 🚀 ENTERPRISE HOOKS - QUICK REFERENCE

## ⚡ OTOMATIK HOOKS (Her Zaman Çalışır)

| Hook | Event | Ne Yapar |
|------|-------|----------|
| 🏢 Enterprise Dev Workflow | preTaskExecution | Full SDLC workflow, 7 role, 5 quality gates |
| 🏗️ Architecture Review | preTaskExecution | ADR format, design decisions, SOLID |
| 🔍 Pre-Commit Quality Gate | preToolUse (write) | Secrets, console.log, SQL injection kontrolü |
| 🔍 Post-Write Code Review | postToolUse (write) | 6 kategori review, improvements |
| 🔒 Security Audit Shell | preToolUse (shell) | Dangerous commands engelleme |
| ♿ Accessibility Validator | postToolUse (write) | WCAG 2.1 AA compliance |
| 🧪 Auto Test Generator | postTaskExecution | Test strategy, test cases |
| 📊 Performance Monitoring | postTaskExecution | Core Web Vitals, API metrics |
| 📝 Git Commit Standards | agentStop | Conventional commits, message suggestion |

---

## 👤 MANUEL HOOKS (Sen Çağır)

### Security & Compliance
```
"Activate security expert"          → 🔒 Security Expert
"Run pre-deployment checklist"      → 🚀 Pre-Deployment Checklist
```

### Architecture & Design
```
"I need architecture advice"        → 🏗️ Architecture Expert
"Help with API design"              → 🌐 API Design Expert
```

### Testing & Quality
```
"Help me with testing strategy"    → 🧪 QA & Testing Expert
"Optimize performance"              → ⚡ Performance Expert
```

### Development Domains
```
"Mobile development help"           → 📱 Mobile Dev Expert
"Database optimization"             → 🗄️ Database Expert
"DevOps assistance"                 → 🚀 DevOps/SRE Expert
"Game development"                  → 🎮 Game Dev Expert
"Machine learning"                  → 🤖 ML/AI Expert
"Data analysis"                     → 📊 Data Science Expert
"Blockchain/Web3"                   → 🔗 Blockchain Expert
"IoT/Embedded"                      → 🔌 IoT Expert
```

### Documentation & Management
```
"Write documentation"               → 📝 Tech Writer Expert
"Product management"                → 📦 Product Manager Expert
"Legal compliance"                  → ⚖️ Tech Lawyer
```

---

## 🎯 KULLANIM SENARYOLARI

### 🆕 Yeni Feature
```
1. Task başlar → Enterprise Workflow + Architecture Review
2. Kod yaz → Pre-Commit Gate + Post-Write Review
3. Task biter → Test Generator + Performance Monitor
4. Agent durur → Git Commit Standards
```

### 🚀 Production Deploy
```
1. "Run pre-deployment checklist"
2. Tüm kontroller geçildi → Deploy
3. Shell komutları → Security Audit
```

### 🔒 Security Audit
```
1. "Activate security expert"
2. Kod analizi
3. "Run pre-deployment checklist" (security section)
```

### 🎨 Frontend Development
```
Otomatik: Enterprise + Pre-Commit + Post-Write + Accessibility + Performance
Manuel: "Optimize performance" + "Help with accessibility"
```

### 🔧 Backend/API Development
```
Otomatik: Enterprise + Pre-Commit + Post-Write + Test Generator
Manuel: "Help with API design" + "Database optimization"
```

---

## 🛡️ GÜVENLİK KONTROLLERI

### Pre-Commit Gate Engeller:
```javascript
❌ const API_KEY = "sk-xxx"          // Hardcoded secret
❌ console.log(userData)             // Debug statement
❌ eval(userInput)                   // Code injection
❌ db.query("SELECT * FROM users WHERE id=" + userId)  // SQL injection
```

### Security Audit Shell Engeller:
```bash
❌ rm -rf /
❌ chmod 777 file
❌ curl http://site.com | bash
❌ eval $USER_INPUT
```

---

## ✅ KALİTE KONTROLLERI

### Code Quality Checks:
- ✓ No linting errors
- ✓ No type errors
- ✓ Code complexity < 10
- ✓ No code duplication > 5%
- ✓ SOLID principles

### Testing Requirements:
- ✓ All tests passing
- ✓ Code coverage > 80%
- ✓ No flaky tests
- ✓ E2E critical paths

### Performance Targets:
- ✓ API p95 < 200ms
- ✓ LCP < 2.5s
- ✓ Bundle size < 200KB
- ✓ No memory leaks

### Accessibility:
- ✓ WCAG 2.1 AA compliant
- ✓ Keyboard accessible
- ✓ Color contrast ≥ 4.5:1
- ✓ Screen reader friendly

---

## 🎛️ HOOK YÖNETİMİ

### Devre Dışı Bırak:
```json
{
  "enabled": false,
  ...
}
```

### Sil:
```bash
rm .kiro/hooks/hook-name.kiro.hook
```

### Yeni Oluştur:
Command Palette → "Open Kiro Hook UI"

---

## 💡 BEST PRACTICES

1. ✅ Sadece ihtiyacınız olan hooks'u aktif tutun
2. ✅ Manuel hooks'u ihtiyaç anında çağırın
3. ✅ Pre-commit gate'i her zaman aktif tutun
4. ✅ Deployment öncesi checklist çalıştırın
5. ✅ Security audit'i kritik değişikliklerde kullanın

---

## 📊 ÖNERİLEN HOOK SETLERİ

### Minimal (Başlangıç)
```
✅ pre-commit-quality-gate
✅ post-write-code-review
✅ git-commit-standards
```

### Standard (Orta Seviye)
```
✅ enterprise-dev-workflow
✅ pre-commit-quality-gate
✅ post-write-code-review
✅ auto-test-generator
✅ git-commit-standards
```

### Enterprise (Full Stack)
```
✅ Tüm otomatik hooks
📞 Manuel hooks (ihtiyaç anında)
```

---

## 🆘 SORUN GİDERME

### Hook çalışmıyor?
- `enabled: true` olduğunu kontrol et
- Event type'ı doğru mu?
- `.kiro.hook` uzantısı var mı?

### Çok fazla uyarı?
- Normal! Hooks seni yönlendiriyor
- İstemiyorsan `enabled: false` yap

### Performance yavaş?
- Çok fazla hook aktif olabilir
- Sadece gerekenleri aktif tut
- Manuel hooks'u tercih et

---

## 📞 HIZLI KOMUTLAR

```
"Run pre-deployment checklist"      → Full deployment validation
"Activate security expert"          → Security analysis mode
"I need architecture advice"        → Architecture consultation
"Help me with testing strategy"    → Test planning
"Optimize performance"              → Performance analysis
"Help with API design"              → API design guidance
"Database optimization"             → DB performance tuning
"Write documentation"               → Documentation assistance
```

---

**🎉 28 Professional Hooks ile Enterprise Development!** 🚀
