# 🔌 MCP SERVERS - DIŞ SİSTEM ENTEGRASYONLARI

Bu klasörde MCP (Model Context Protocol) konfigürasyonu bulunur. 16 farklı dış sistem entegrasyonu sağlar.

## 📋 MCP LİSTESİ

### ✅ **AKTİF MCP'LER** (disabled: false)

#### 1. **filesystem**
**Ne yapar**: Dosya sistemi erişimi
**API Key**: Gerektirmez
**Kullanım**: Dosya okuma, yazma, listeleme
**autoApprove**: read_file, list_directory

#### 2. **memory**
**Ne yapar**: Kalıcı hafıza - konuşmalar arası bilgi saklama
**API Key**: Gerektirmez
**Kullanım**: Kullanıcı tercihleri, proje bilgileri, ilişkiler
**autoApprove**: create_entities, create_relations, add_observations

#### 3. **sequential-thinking**
**Ne yapar**: Gelişmiş problem çözme ve mantıksal düşünme
**API Key**: Gerektirmez
**Kullanım**: Karmaşık problemleri adım adım çözme
**autoApprove**: Yok (manuel onay)

### 🔒 **PASİF MCP'LER** (disabled: true) - Aktif Etmek İçin Ayar Gerekli

#### 4. **github**
**Ne yapar**: GitHub entegrasyonu
**API Key**: `GITHUB_PERSONAL_ACCESS_TOKEN`
**Kullanım**: Repository oluşturma, Issue yönetimi, PR oluşturma
**Nasıl aktif edilir**:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Token oluştur (repo, issues, pull_requests izinleri)
3. Token'ı `GITHUB_PERSONAL_ACCESS_TOKEN` alanına yapıştır
4. `"disabled": false` yap

#### 5. **postgres**
**Ne yapar**: PostgreSQL veritabanı yönetimi
**API Key**: Connection string gerekli
**Kullanım**: SQL sorguları, tablo oluşturma, veri analizi
**Nasıl aktif edilir**:
1. Connection string'i güncelle: `postgresql://user:pass@host:port/db`
2. `"disabled": false` yap

#### 6. **brave-search**
**Ne yapar**: Web araması (Brave Search API)
**API Key**: `BRAVE_API_KEY`
**Kullanım**: Güncel bilgi arama, research
**Nasıl aktif edilir**:
1. https://brave.com/search/api/ → API key al
2. Key'i `BRAVE_API_KEY` alanına yapıştır
3. `"disabled": false` yap

#### 7. **google-maps**
**Ne yapar**: Google Maps entegrasyonu
**API Key**: `GOOGLE_MAPS_API_KEY`
**Kullanım**: Geocoding, Directions, Places API
**Nasıl aktif edilir**:
1. Google Cloud Console → API key oluştur
2. Maps API'yi aktif et
3. Key'i yapıştır
4. `"disabled": false` yap

#### 8. **slack**
**Ne yapar**: Slack entegrasyonu
**API Key**: `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID`
**Kullanım**: Mesaj gönderme, Channel yönetimi
**Nasıl aktif edilir**:
1. Slack App oluştur
2. Bot token al
3. Team ID'yi bul
4. Değerleri yapıştır
5. `"disabled": false` yap

#### 9. **puppeteer**
**Ne yapar**: Browser automation, web scraping
**API Key**: Gerektirmez
**Kullanım**: Screenshot alma, PDF oluşturma, E2E testing
**Nasıl aktif edilir**: Sadece `"disabled": false` yap

#### 10. **aws-kb-retrieval**
**Ne yapar**: AWS Knowledge Base entegrasyonu
**API Key**: AWS credentials gerekli
**Kullanım**: AWS dokümantasyon arama
**Nasıl aktif edilir**:
1. AWS credentials ayarla
2. Knowledge Base ID'yi belirt
3. `"disabled": false` yap

#### 11. **sqlite**
**Ne yapar**: SQLite veritabanı yönetimi
**API Key**: Gerektirmez
**Kullanım**: Lokal database işlemleri
**Nasıl aktif edilir**:
1. Database path'ini belirt
2. `"disabled": false` yap

#### 12. **docker**
**Ne yapar**: Docker container yönetimi
**API Key**: Gerektirmez
**Kullanım**: Container başlatma/durdurma, Image yönetimi
**Nasıl aktif edilir**: Sadece `"disabled": false` yap

#### 13. **kubernetes**
**Ne yapar**: Kubernetes cluster yönetimi
**API Key**: Kubeconfig gerekli
**Kullanım**: Pod yönetimi, Deployment, Service yönetimi
**Nasıl aktif edilir**:
1. Kubeconfig'i ayarla
2. `"disabled": false` yap

#### 14. **git**
**Ne yapar**: Git operations
**API Key**: Gerektirmez
**Kullanım**: Commit, push, pull, Branch yönetimi
**Nasıl aktif edilir**: Sadece `"disabled": false` yap

#### 15. **sentry**
**Ne yapar**: Error monitoring
**API Key**: `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT`
**Kullanım**: Error tracking, Performance monitoring
**Nasıl aktif edilir**:
1. Sentry'de auth token oluştur
2. Org ve project bilgilerini al
3. Değerleri yapıştır
4. `"disabled": false` yap

#### 16. **fetch**
**Ne yapar**: Web content fetching
**API Key**: Gerektirmez
**Kullanım**: URL'den içerik çekme
**Nasıl aktif edilir**: Sadece `"disabled": false` yap

#### 17. **everart**
**Ne yapar**: AI image generation
**API Key**: `EVERART_API_KEY`
**Kullanım**: Görsel oluşturma
**Nasıl aktif edilir**:
1. EverArt'tan API key al
2. Key'i yapıştır
3. `"disabled": false` yap

## 🚀 HIZLI KURULUM REHBERİ

### 1. API Key Gerektirmeyen MCP'ler (Kolay)
```json
{
  "puppeteer": { "disabled": false },
  "docker": { "disabled": false },
  "git": { "disabled": false },
  "fetch": { "disabled": false },
  "sqlite": { "disabled": false }
}
```

### 2. GitHub MCP (Önerilen)
```json
{
  "github": {
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
    },
    "disabled": false
  }
}
```

**GitHub Token Alma**:
1. GitHub.com → Settings
2. Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Scopes: `repo`, `read:user`, `user:email`
5. Token'ı kopyala ve yapıştır

### 3. Brave Search MCP (Web Araması)
```json
{
  "brave-search": {
    "env": {
      "BRAVE_API_KEY": "your_brave_api_key"
    },
    "disabled": false
  }
}
```

**Brave API Key Alma**:
1. https://brave.com/search/api/
2. Sign up for API access
3. API key al
4. Key'i yapıştır

### 4. PostgreSQL MCP (Database)
```json
{
  "postgres": {
    "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:password@localhost:5432/mydb"],
    "disabled": false
  }
}
```

**PostgreSQL Connection String**:
- Format: `postgresql://username:password@host:port/database`
- Örnek: `postgresql://admin:secret123@localhost:5432/myapp`

## 🎯 ÖNERİLEN MCP SETUP'LARI

### Full-Stack Developer
```json
Aktif et:
✅ filesystem (zaten aktif)
✅ memory (zaten aktif)
✅ github (kod yönetimi)
✅ postgres (veritabanı)
✅ docker (containerization)
✅ puppeteer (testing)
```

### DevOps Engineer
```json
Aktif et:
✅ filesystem
✅ docker
✅ kubernetes
✅ git
✅ sentry (monitoring)
```

### Data Scientist
```json
Aktif et:
✅ filesystem
✅ memory
✅ postgres
✅ sqlite
✅ brave-search (research)
```

### Security Researcher
```json
Aktif et:
✅ filesystem
✅ puppeteer (web testing)
✅ fetch (content analysis)
✅ github (vulnerability tracking)
```

## 🔧 MCP KURULUM ADIMI ADIM

### 1. mcp.json Dosyasını Düzenle
```bash
# Dosya konumu
.kiro/settings/mcp.json
```

### 2. API Key'leri Ekle
```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "BURAYA_TOKEN_YAPISTIR"
      },
      "disabled": false
    }
  }
}
```

### 3. Kiro'yu Yeniden Başlat
- Kiro'yu kapat
- Tekrar aç
- MCP'ler otomatik bağlanır

### 4. MCP Durumunu Kontrol Et
- Command Palette → "MCP: List Servers"
- Sol panel → MCP bölümü
- Bağlantı durumunu kontrol et

## 🆘 SORUN GİDERME

### MCP Bağlanamıyor
1. **API Key Kontrol Et**
   - Key'in doğru olduğunu kontrol et
   - Expiry date'ini kontrol et
   - Permissions'ları kontrol et

2. **JSON Syntax Kontrol Et**
   - Virgül eksikliği
   - Tırnak işareti hatası
   - Bracket hatası

3. **Kiro'yu Yeniden Başlat**
   - Kiro'yu tamamen kapat
   - Tekrar aç
   - 30 saniye bekle

4. **MCP Reconnect**
   - Command Palette → "MCP: Reconnect All Servers"

### Specific MCP Sorunları

#### GitHub MCP
```
Hata: "Bad credentials"
Çözüm: Token'ın doğru olduğunu ve repo permissions'ı olduğunu kontrol et
```

#### PostgreSQL MCP
```
Hata: "Connection refused"
Çözüm: Database'in çalıştığını ve connection string'in doğru olduğunu kontrol et
```

#### Brave Search MCP
```
Hata: "Invalid API key"
Çözüm: API key'in aktif olduğunu ve quota'nın dolmadığını kontrol et
```

## 📊 MCP PERFORMANS

| MCP | Başlatma Hızı | Kullanım Kolaylığı | Fayda |
|-----|---------------|-------------------|-------|
| filesystem | Çok Hızlı | Kolay | Kritik |
| memory | Hızlı | Kolay | Yüksek |
| github | Orta | Orta | Yüksek |
| postgres | Orta | Zor | Yüksek |
| puppeteer | Yavaş | Orta | Orta |
| docker | Hızlı | Kolay | Yüksek |

## 🎉 BAŞARILAR!

MCP'ler ile Kiro'nun gücü sınırsız hale gelir!