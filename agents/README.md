# 🤖 AGENTS - BAĞIMSIZ AI UZMANLARI

Bu klasörde 8 farklı uzman AI agent'ı bulunur. Her biri bağımsız çalışır ve özel görevleri vardır.

## 📋 AGENT LİSTESİ

### 1. **code-reviewer.json**
**Ne yapar**: Kod inceleme uzmanı
**Kullanım**: `invokeSubAgent("Code Reviewer", "Bu PR'ı incele")`
**Özellikler**:
- Security vulnerability kontrolü
- Performance analizi
- Best practices incelemesi
- SOLID principles kontrolü
- Detaylı feedback

### 2. **test-generator.json**
**Ne yapar**: Test oluşturma uzmanı
**Kullanım**: `invokeSubAgent("Test Generator", "UserService için test yaz")`
**Özellikler**:
- Unit test oluşturma
- Integration test yazma
- Edge case'leri kapsama
- Mock setup
- Test coverage analizi

### 3. **refactoring-assistant.json**
**Ne yapar**: Kod iyileştirme uzmanı
**Kullanım**: `invokeSubAgent("Refactoring Assistant", "Bu legacy kodu refactor et")`
**Özellikler**:
- Code smell tespiti
- Refactoring önerileri
- SOLID principles uygulama
- Before/after örnekleri
- Impact assessment

### 4. **documentation-writer.json**
**Ne yapar**: Dokümantasyon uzmanı
**Kullanım**: `invokeSubAgent("Documentation Writer", "Bu API'yi dokümante et")`
**Özellikler**:
- API dokümantasyonu
- README dosyaları
- Architecture docs
- User guide'lar
- Code comments

### 5. **security-scanner.json**
**Ne yapar**: Güvenlik tarama uzmanı
**Kullanım**: `invokeSubAgent("Security Scanner", "Bu codebase'i tara")`
**Özellikler**:
- OWASP Top 10 kontrolü
- Vulnerability scanning
- Hardcoded secret tespiti
- Authentication/Authorization analizi
- Detaylı güvenlik raporu

### 6. **performance-analyzer.json**
**Ne yapar**: Performans analiz uzmanı
**Kullanım**: `invokeSubAgent("Performance Analyzer", "Bu API'nin performansını analiz et")`
**Özellikler**:
- Bottleneck tespiti
- Memory leak analizi
- Database query optimizasyonu
- Frontend performance (Core Web Vitals)
- Optimization önerileri

### 7. **database-migration-expert.json**
**Ne yapar**: Veritabanı migration uzmanı
**Kullanım**: `invokeSubAgent("Database Migration Expert", "User tablosuna status kolonu ekle")`
**Özellikler**:
- Safe migration oluşturma
- Zero-downtime strategies
- Rollback planları
- Data transformation
- Risk assessment

## 🚀 NASIL KULLANILIR?

### 1. Agent Çağırma
```typescript
// Kiro chat'inde
invokeSubAgent("Agent Adı", "Görev açıklaması")
```

### 2. Örnek Kullanımlar
```typescript
// Code review
invokeSubAgent("Code Reviewer", "Bu authentication modülünü incele")

// Test yazma
invokeSubAgent("Test Generator", "PaymentService sınıfı için comprehensive testler yaz")

// Refactoring
invokeSubAgent("Refactoring Assistant", "Bu 500 satırlık fonksiyonu refactor et")

// Dokümantasyon
invokeSubAgent("Documentation Writer", "REST API endpoints için OpenAPI spec oluştur")

// Güvenlik tarama
invokeSubAgent("Security Scanner", "Tüm authentication flow'unu güvenlik açısından incele")

// Performance analizi
invokeSubAgent("Performance Analyzer", "Bu e-commerce sitesinin yavaşlık nedenlerini bul")

// Database migration
invokeSubAgent("Database Migration Expert", "Users tablosunu normalize et")
```

## 🎯 KULLANIM İPUÇLARI

### En İyi Uygulamalar
1. **Spesifik ol**: "Kodu incele" yerine "Authentication modülündeki security vulnerabilities'i incele"
2. **Context ver**: Hangi teknoloji stack'i kullandığını belirt
3. **Beklentini belirt**: Ne tür output istediğini açıkla

### Örnek İyi Promptlar
```
✅ İyi: "React TypeScript projesindeki LoginForm component'i için unit testler yaz. Jest ve React Testing Library kullan."

❌ Kötü: "Test yaz"

✅ İyi: "Node.js Express API'sindeki user authentication endpoint'lerini OWASP Top 10'a göre incele"

❌ Kötü: "Güvenlik kontrol et"
```

## 🔧 SORUN GİDERME

### Agent Çalışmıyor
- Agent dosyasının `.kiro/agents/` klasöründe olduğunu kontrol edin
- JSON syntax'ının doğru olduğunu kontrol edin
- Kiro'yu yeniden başlatın

### Agent Yavaş Çalışıyor
- Çok büyük dosyalar için agent'ları kullanmayın
- Spesifik görevler verin, genel görevler yerine

### Agent Hatalı Sonuç Veriyor
- Daha spesifik prompt yazın
- Context bilgisi ekleyin
- Teknoloji stack'ini belirtin

## 📊 AGENT KARŞILAŞTIRMA

| Agent | Hız | Detay | Kullanım Alanı |
|-------|-----|-------|----------------|
| Code Reviewer | Orta | Yüksek | PR review, code quality |
| Test Generator | Hızlı | Orta | Test yazma, coverage |
| Refactoring Assistant | Yavaş | Yüksek | Legacy code, cleanup |
| Documentation Writer | Hızlı | Orta | Docs, README |
| Security Scanner | Orta | Yüksek | Security audit |
| Performance Analyzer | Yavaş | Yüksek | Performance tuning |
| Database Migration Expert | Orta | Yüksek | DB schema changes |

## 🎉 BAŞARILAR!

Bu agent'lar ile kod kalitesi, güvenlik ve performansınızı üst seviyeye çıkarabilirsiniz!