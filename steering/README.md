# 📋 STEERING - OTOMATIK KURALLAR

Bu klasörde 10 farklı steering dosyası bulunur. Her biri benim davranışımı otomatik olarak yönlendirir.

## 📋 STEERING LİSTESİ

### 🔄 **AUTO (Her Zaman Aktif)**

#### 1. **coding-standards.md**
**Ne yapar**: Genel kodlama standartları
**Aktif olma**: Her zaman
**İçerik**:
- SOLID principles
- Clean code rules
- Error handling patterns
- Git commit standards
- Code review checklist

#### 2. **secrets-security.md**
**Ne yapar**: Secret güvenliği kuralları
**Aktif olma**: Her zaman
**İçerik**:
- ❌ NEVER commit secrets
- ✅ Environment variables kullan
- Secret validation rules
- Logging redaction
- Emergency procedures

### 📁 **FILE MATCH (Belirli Dosyalarda Aktif)**

#### 3. **api-design-guidelines.md**
**Pattern**: `**/*.{api,route,controller,endpoint}.*`
**Ne yapar**: API tasarım kuralları
**Aktif olma**: API dosyalarını açtığında
**İçerik**:
- RESTful API standards
- Status codes
- Pagination strategies
- Authentication patterns
- Rate limiting

#### 4. **typescript-guidelines.md**
**Pattern**: `**/*.{ts,tsx}`
**Ne yapar**: TypeScript kuralları
**Aktif olma**: TS/TSX dosyalarını açtığında
**İçerik**:
- Type safety rules
- Generics usage
- Utility types
- Error handling

#### 5. **python-best-practices.md**
**Pattern**: `**/*.py`
**Ne yapar**: Python en iyi uygulamaları
**Aktif olma**: Python dosyalarını açtığında
**İçerik**:
- PEP 8 standards
- Type hints
- Async/await patterns
- Testing with pytest

#### 6. **go-best-practices.md**
**Pattern**: `**/*.go`
**Ne yapar**: Go en iyi uygulamaları
**Aktif olma**: Go dosyalarını açtığında
**İçerik**:
- Go idioms
- Error handling
- Concurrency patterns
- Testing

#### 7. **database-best-practices.md**
**Pattern**: `**/*.{sql,prisma,migration,model,entity,repository}.*`
**Ne yapar**: Veritabanı kuralları
**Aktif olma**: DB dosyalarını açtığında
**İçerik**:
- Schema design
- Indexing strategies
- Query optimization
- Migrations

#### 8. **frontend-standards.md**
**Pattern**: `**/*.{tsx,jsx,vue,svelte}`
**Ne yapar**: Frontend standartları
**Aktif olma**: Frontend dosyalarını açtığında
**İçerik**:
- Component structure
- State management
- Performance optimization
- Accessibility

#### 9. **security-headers.md**
**Pattern**: `**/*.{server,app,middleware,config}.*`
**Ne yapar**: Güvenlik başlıkları
**Aktif olma**: Server dosyalarını açtığında
**İçerik**:
- CSP (Content Security Policy)
- HSTS, CORS configuration
- Rate limiting setup
- Node.js, Python, Go örnekleri

### 📞 **MANUAL (Sen Çağırınca Aktif)**

#### 10. **security-checklist.md**
**Çağırma**: `#security-checklist`
**Ne yapar**: Güvenlik kontrol listesi
**Aktif olma**: Sen çağırdığında
**İçerik**:
- Pre-deployment security audit
- OWASP Top 10 checklist
- Authentication & Authorization checks
- Compliance verification

## 🚀 NASIL ÇALIŞIR?

### AUTO Steering
```
Her zaman aktif → Sürekli uyarır ve yönlendirir
Örnek: Secret yazmaya çalışırsan hemen uyarır
```

### FILE MATCH Steering
```
Belirli dosya açılınca → O dosya tipine özel kurallar aktif
Örnek: user.api.ts açarsan → API design guidelines aktif
```

### MANUAL Steering
```
Sen çağırınca → Chat'te #steering-name yazarsın
Örnek: #security-checklist → Güvenlik kontrol listesi gelir
```

## 🎯 KULLANIM ÖRNEKLERİ

### React Component Yazarken
```
1. LoginForm.tsx dosyasını aç
2. typescript-guidelines.md otomatik aktif
3. frontend-standards.md otomatik aktif
4. coding-standards.md zaten aktif
→ TypeScript + React + genel kurallar uygulanır
```

### API Endpoint Yazarken
```
1. users.api.ts dosyasını aç
2. api-design-guidelines.md otomatik aktif
3. typescript-guidelines.md otomatik aktif
4. coding-standards.md zaten aktif
→ API + TypeScript + genel kurallar uygulanır
```

### Python FastAPI Yazarken
```
1. main.py dosyasını aç
2. python-best-practices.md otomatik aktif
3. coding-standards.md zaten aktif
→ Python + genel kurallar uygulanır
```

### Database Migration Yazarken
```
1. 001_add_users.sql dosyasını aç
2. database-best-practices.md otomatik aktif
3. coding-standards.md zaten aktif
→ Database + genel kurallar uygulanır
```

### Deployment Öncesi Kontrol
```
1. Chat'te #security-checklist yaz
2. security-checklist.md aktif olur
3. Tüm güvenlik kontrolleri listelenir
→ Manuel güvenlik audit
```

## 💡 İPUÇLARI

### Steering Kombinasyonları
```
✅ Otomatik kombinasyonlar:
- coding-standards (AUTO) + typescript-guidelines (FILE MATCH)
- coding-standards (AUTO) + api-design-guidelines (FILE MATCH)
- secrets-security (AUTO) + security-headers (FILE MATCH)

📞 Manuel ekleme:
- Yukarıdakiler + #security-checklist (MANUAL)
```

### Dosya İsimlendirme
```
✅ İyi dosya isimleri (steering tetikler):
- users.api.ts → API guidelines aktif
- auth.middleware.ts → Security headers aktif
- user.model.ts → Database best practices aktif
- LoginForm.tsx → Frontend standards aktif

❌ Kötü dosya isimleri (steering tetiklenmez):
- utils.ts → Sadece TypeScript guidelines
- index.js → Sadece coding standards
```

## 🔧 SORUN GİDERME

### Steering Aktif Değil
- Dosya pattern'ini kontrol et
- `.kiro/steering/` klasöründe olduğunu kontrol et
- Dosya uzantısının `.md` olduğunu kontrol et

### Çok Fazla Uyarı Geliyor
- Normal! Steering'ler seni yönlendirmek için var
- Kuralları öğrendikçe uyarılar azalır
- İstemiyorsan dosyayı silebilirsin

### Manuel Steering Çalışmıyor
- `#steering-name` formatını kontrol et
- Dosya adının doğru olduğunu kontrol et
- `inclusion: manual` olduğunu kontrol et

## 📊 STEERING ETKİ ALANLARI

| Steering | Etki Alanı | Uyarı Sıklığı | Fayda |
|----------|-------------|---------------|-------|
| coding-standards | Tüm kodlar | Yüksek | Çok Yüksek |
| secrets-security | Tüm kodlar | Orta | Kritik |
| typescript-guidelines | TS dosyaları | Yüksek | Yüksek |
| api-design-guidelines | API dosyaları | Orta | Yüksek |
| python-best-practices | Python dosyaları | Yüksek | Yüksek |
| database-best-practices | DB dosyaları | Orta | Yüksek |
| security-checklist | Manuel | Düşük | Kritik |

## 🎉 BAŞARILAR!

Bu steering dosyaları ile kod kalitesi ve güvenliğiniz otomatik olarak üst seviyede olacak!