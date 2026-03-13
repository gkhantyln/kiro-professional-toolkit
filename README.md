# 🚀 Kiro Professional Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/gkhantyln/kiro-professional-toolkit.svg)](https://github.com/gkhantyln/kiro-professional-toolkit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/gkhantyln/kiro-professional-toolkit.svg)](https://github.com/gkhantyln/kiro-professional-toolkit/network)
[![GitHub issues](https://img.shields.io/github/issues/gkhantyln/kiro-professional-toolkit.svg)](https://github.com/gkhantyln/kiro-professional-toolkit/issues)

**Complete professional development toolkit for Kiro IDE** - Transform your development workflow with 19 Expert Hooks, 8 AI Agents, 14 Skills, 10 Steering Rules & 16 MCP Integrations.

> 🎯 **Enterprise-grade development environment in one package**

## 📦 İÇERİK

### 🤖 Agents (8 Adet)
Bağımsız AI uzmanları:
- **Code Reviewer**: Kod inceleme uzmanı
- **Test Generator**: Test oluşturma uzmanı  
- **Refactoring Assistant**: Kod iyileştirme uzmanı
- **Documentation Writer**: Dokümantasyon uzmanı
- **Security Scanner**: Güvenlik tarama uzmanı
- **Performance Analyzer**: Performans analiz uzmanı
- **Database Migration Expert**: Veritabanı migration uzmanı

### 🎯 Hooks (19 Adet)
Uzmanlık modları:
- **Enterprise Dev Team**: Tam ekip yapısı
- **Security Expert**: Güvenlik uzmanı
- **Mobile Dev Expert**: Mobil geliştirme
- **DevOps/SRE Expert**: Altyapı uzmanı
- **ML/AI Expert**: Yapay zeka uzmanı
- **Database Expert**: Veritabanı uzmanı
- **API Design Expert**: API tasarım uzmanı
- **Performance Expert**: Performans uzmanı
- **Accessibility Expert**: Erişilebilirlik uzmanı
- **Architecture Expert**: Mimari uzmanı
- **Blockchain/Web3 Expert**: Blockchain uzmanı
- **Product Manager Expert**: Ürün yöneticisi
- **IoT/Embedded Expert**: IoT uzmanı
- **Technical Writer Expert**: Teknik yazar
- **QA/Testing Expert**: Test uzmanı
- **Game Dev Expert**: Oyun geliştirme
- **Data Science Expert**: Veri bilimi
- **Tech Lawyer**: Teknoloji hukuku
- **Tech Psychologist**: Geliştirici psikolojisi

### 📋 Steering (10 Adet)
Otomatik kurallar:
- **coding-standards.md**: Genel kodlama standartları
- **api-design-guidelines.md**: API tasarım kuralları
- **typescript-guidelines.md**: TypeScript kuralları
- **python-best-practices.md**: Python en iyi uygulamaları
- **go-best-practices.md**: Go en iyi uygulamaları
- **database-best-practices.md**: Veritabanı kuralları
- **frontend-standards.md**: Frontend standartları
- **security-headers.md**: Güvenlik başlıkları
- **secrets-security.md**: Secret güvenliği
- **security-checklist.md**: Güvenlik kontrol listesi

### 💪 Skills (14 Adet)
Hazır görevler:
- **create-react-component**: React component oluştur
- **create-api-endpoint**: API endpoint oluştur
- **create-fastapi-endpoint**: FastAPI endpoint oluştur
- **setup-testing**: Test altyapısı kur
- **create-docker-setup**: Docker kurulumu
- **setup-ci-cd**: CI/CD pipeline kur
- **setup-monitoring**: Monitoring kur
- **setup-secrets-management**: Secret yönetimi kur
- **security-audit**: Güvenlik denetimi
- **setup-authentication**: Kimlik doğrulama kur
- **setup-database**: Veritabanı kur
- **create-microservice**: Mikroservis oluştur
- **create-graphql-api**: GraphQL API oluştur
- **create-readme**: README oluştur

### 🔌 MCP Servers (16 Adet)
Dış sistem entegrasyonları:
- **filesystem**: Dosya sistemi erişimi ✅
- **memory**: Kalıcı hafıza ✅
- **sequential-thinking**: Gelişmiş düşünme ✅
- **github**: GitHub entegrasyonu
- **postgres**: PostgreSQL veritabanı
- **brave-search**: Web araması
- **google-maps**: Google Maps
- **slack**: Slack entegrasyonu
- **puppeteer**: Browser otomasyonu
- **aws-kb-retrieval**: AWS Knowledge Base
- **sqlite**: SQLite veritabanı
- **docker**: Docker yönetimi
- **kubernetes**: Kubernetes yönetimi
- **git**: Git işlemleri
- **sentry**: Hata izleme
- **fetch**: Web içerik çekme
- **everart**: AI görsel oluşturma

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

### Brave Search MCP
1. https://brave.com/search/api/ → API key al
2. `BRAVE_API_KEY` alanına yapıştır
3. `"disabled": false` yap

### PostgreSQL MCP
1. Connection string'i güncelle: `postgresql://user:pass@host:port/db`
2. `"disabled": false` yap

### Docker MCP (API key gerektirmez)
1. Sadece `"disabled": false` yap

### Puppeteer MCP (API key gerektirmez)
1. Sadece `"disabled": false` yap

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