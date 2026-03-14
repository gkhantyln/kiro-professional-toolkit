# 🔌 MCP SERVERS - DIŞ SİSTEM ENTEGRASYONLARI

Bu klasörde MCP (Model Context Protocol) konfigürasyonu bulunur. **44 farklı** dış sistem entegrasyonu sağlar.

## 📋 MCP LİSTESİ

### ✅ AKTİF (disabled: false)

| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 1 | **filesystem** | Dosya sistemi okuma/yazma | Gerektirmez |
| 2 | **memory** | Konuşmalar arası kalıcı hafıza | Gerektirmez |
| 3 | **sequential-thinking** | Gelişmiş adım adım problem çözme | Gerektirmez |

---

### 🔒 PASİF (disabled: true) — Kategoriye Göre

#### 🛠️ Geliştirme & Versiyon Kontrol
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 4 | **github** | Repo, issue, PR, workflow yönetimi | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| 5 | **gitlab** | Repo, MR, CI/CD pipeline yönetimi | `GITLAB_PERSONAL_ACCESS_TOKEN` |
| 6 | **git** | Yerel Git işlemleri | Gerektirmez |
| 7 | **playwright** | Browser otomasyonu (accessibility tree) | Gerektirmez |
| 8 | **puppeteer** | Browser otomasyonu ve scraping | Gerektirmez |
| 9 | **context7** | Güncel kütüphane dokümantasyonu | Gerektirmez |
| 10 | **markitdown** | PDF/Word/Excel/PPT → Markdown | Gerektirmez |

#### 🗄️ Veritabanı
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 11 | **postgres** | PostgreSQL sorgu ve yönetim | Connection string |
| 12 | **sqlite** | SQLite lokal veritabanı | Gerektirmez |
| 13 | **mongodb** | MongoDB NoSQL (Official) | Connection string |
| 14 | **redis** | Redis cache, pub/sub, streams | `REDIS_URL` |
| 15 | **supabase** | Postgres + Auth + Storage + Edge | `SUPABASE_ACCESS_TOKEN` |
| 16 | **neon** | Neon serverless Postgres | `NEON_API_KEY` |

#### 📋 Proje Yönetimi
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 17 | **notion** | Notion workspace (Official) | `NOTION_TOKEN` |
| 18 | **linear** | Linear issue tracker (Official) | `LINEAR_API_KEY` |
| 19 | **jira** | Jira issue ve sprint yönetimi | `JIRA_API_TOKEN` |
| 20 | **confluence** | Atlassian Confluence dokümantasyon | `CONFLUENCE_API_TOKEN` |
| 21 | **airtable** | Airtable veritabanı ve tablolar | `AIRTABLE_API_KEY` |

#### 💬 İletişim
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 22 | **slack** | Slack mesajlaşma ve kanal yönetimi | `SLACK_BOT_TOKEN` |
| 23 | **discord** | Discord bot entegrasyonu | `DISCORD_TOKEN` |
| 24 | **twilio** | SMS ve WhatsApp bildirimleri | `TWILIO_ACCOUNT_SID` |

#### ☁️ Cloud & Altyapı
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 25 | **docker** | Container ve image yönetimi | Gerektirmez |
| 26 | **kubernetes** | Kubernetes cluster yönetimi | Kubeconfig |
| 27 | **vercel** | Deployment, domain, env yönetimi | `VERCEL_TOKEN` |
| 28 | **cloudflare** | Workers, KV, R2, DNS (Official) | `CLOUDFLARE_API_TOKEN` |
| 29 | **aws-kb-retrieval** | AWS Knowledge Base erişimi | AWS credentials |
| 30 | **aws-docs** | AWS resmi dokümantasyon arama | Gerektirmez |

#### 📊 Monitoring & Observability
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 31 | **sentry** | Hata izleme ve debug (Official) | `SENTRY_AUTH_TOKEN` |
| 32 | **datadog** | Metrics, log, trace izleme (Official) | `DD_API_KEY` |
| 33 | **grafana** | Dashboard ve alerting (Official) | `GRAFANA_API_KEY` |
| 34 | **pagerduty** | Incident yönetimi ve on-call | `PAGERDUTY_API_KEY` |

#### 🔍 Arama & Web
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 35 | **brave-search** | Brave Search API | `BRAVE_API_KEY` |
| 36 | **tavily** | AI-optimized web arama (LLM için üstün) | `TAVILY_API_KEY` |
| 37 | **exa** | Semantic web arama | `EXA_API_KEY` |
| 38 | **fetch** | Web içerik çekme | Gerektirmez |

#### 🎨 Tasarım & Medya
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 39 | **figma** | Design specs, component çıkarma | `FIGMA_API_KEY` |
| 40 | **everart** | AI görsel oluşturma | `EVERART_API_KEY` |

#### 🤖 AI & Veri
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 41 | **huggingface** | Model hub, inference, dataset | `HF_TOKEN` |

#### 💳 Ödeme & Workspace
| # | MCP | Ne Yapar | API Key |
|---|-----|----------|---------|
| 42 | **stripe** | Ödeme, müşteri, abonelik (Official) | `STRIPE_SECRET_KEY` |
| 43 | **google-maps** | Geocoding, Directions, Places | `GOOGLE_MAPS_API_KEY` |
| 44 | **google-workspace** | Gmail, Drive, Docs, Sheets, Calendar (12 servis) | OAuth 2.0 |

---

## 🚀 ÖNERİLEN SETUP'LAR

### Full-Stack Developer
```
✅ filesystem + memory + sequential-thinking (aktif)
+ github, postgres, docker, playwright, context7
```

### DevOps / SRE
```
✅ filesystem + memory
+ github, docker, kubernetes, sentry, datadog, grafana, pagerduty
```

### Frontend Developer
```
✅ filesystem + memory
+ github, figma, playwright, context7, vercel
```

### Data / AI Engineer
```
✅ filesystem + memory
+ postgres, mongodb, redis, supabase, huggingface, tavily
```

### Product Manager
```
✅ filesystem + memory
+ notion, linear, jira, confluence, airtable, slack
```

---

## ⚙️ KURULUM

### API Key Gerektirmeyen MCP'ler (Hemen Aktif Et)
```json
"git": { "disabled": false },
"docker": { "disabled": false },
"puppeteer": { "disabled": false },
"playwright": { "disabled": false },
"fetch": { "disabled": false },
"sqlite": { "disabled": false },
"context7": { "disabled": false },
"aws-docs": { "disabled": false },
"markitdown": { "disabled": false }
```

> `uvx` gerektiren MCP'ler için: `pip install uv`

### API Key Gerektiren MCP'ler
İlgili servisin dashboard'undan token alıp `mcp.json`'daki `env` alanına yapıştır, ardından `"disabled": false` yap.

---

## 🆘 SORUN GİDERME

**MCP bağlanamıyor?**
1. API key'in doğru ve aktif olduğunu kontrol et
2. JSON syntax hatası olmadığını kontrol et
3. Command Palette → "MCP: Reconnect All Servers"
4. Kiro'yu yeniden başlat

**uvx komutu bulunamıyor?**
```bash
pip install uv
```

**npx komutu bulunamıyor?**
```bash
# Node.js kur: https://nodejs.org
node --version  # v18+ olmalı
```
