# 🏗️ WAIPRO Infrastructure Backup & Configuration

Backup completo e documentazione dell'infrastruttura WAIPRO Agency su Google Cloud Platform.

## 📋 Indice

- [Panoramica](#panoramica)
- [Social Login e Autenticazione](#social-login-e-autenticazione)
- [Struttura del Progetto](#struttura-del-progetto)
- [Guide e Documentazione](#guide-e-documentazione)
- [Utility Scripts](#utility-scripts)
- [Quick Start](#quick-start)

---

## 🎯 Panoramica

**Progetto Google Cloud:** `waipro-agency`
**Service Account:** `claudio-admin-waipro@waipro-agency.iam.gserviceaccount.com`
**Progetti Attivi:** nonamebar.it, e altri

Questo repository contiene:
- ✅ Configurazione Google Cloud Platform
- ✅ Setup OAuth 2.0 per Base44 apps
- ✅ Documentazione social login (Google, Microsoft, Facebook)
- ✅ Script di verifica e monitoring
- ✅ Guide setup e troubleshooting

---

## 🔐 Social Login e Autenticazione

### Cos'è il Social Login?

Il **Social Login** permette agli utenti di accedere alle tue app Base44 usando account social esistenti (Google, Facebook, Microsoft) invece di creare nuove password.

**Vantaggi:**
- ⚡ Login in 1 click
- 🔒 Sicurezza gestita da provider affidabili
- 📈 Più conversioni (+77% preferenza utenti)
- ✅ Email già verificate
- 🎨 Branding personalizzato (con Custom OAuth)

### Provider Supportati

| Provider | Ideale Per | Utenti |
|----------|-----------|--------|
| 🔵 **Google** | B2B e B2C | 2+ miliardi |
| 🔷 **Microsoft** | Business/Enterprise | Office 365 |
| 🔵 **Facebook** | Social apps | 2.9+ miliardi |
| 📧 **Email/Password** | Fallback | Tutti |
| 🏢 **SSO** (Elite) | Enterprise | Okta, Auth0 |

### 🎨 Branding: Default vs Custom

#### Default Base44 OAuth (Veloce - 2 min)
```
Popup Google mostra: "base44.com richiede accesso..."
```
✅ Veloce da configurare
❌ Brand Base44, non il tuo

#### Custom OAuth (Professionale - 60 min)
```
Popup Google mostra: "nonamebar.it richiede accesso..."
```
✅ **IL TUO brand nel popup Google**
✅ Logo personalizzato
✅ Professionale per clienti
⚠️ Richiede setup GCP e approvazione (1-5 giorni)

**👉 Per progetti professionali, usa sempre Custom OAuth!**

### 📚 Guide Disponibili

- **[SOCIAL_LOGIN_GUIDE.md](SOCIAL_LOGIN_GUIDE.md)** - Guida completa al social login
  - Come funziona OAuth 2.0
  - Vantaggi e best practices
  - Configurazione provider
  - Sicurezza e privacy

- **[BASE44_OAUTH_SETUP.md](BASE44_OAUTH_SETUP.md)** - Setup tecnico OAuth
  - Fix errore `redirect_uri_mismatch`
  - Configurazione Google Cloud
  - Setup Base44 custom OAuth
  - Checklist completa

---

## 📁 Struttura del Progetto

```
infrastructure-backup/
│
├── README.md                      # Questo file
├── .gitignore                     # Esclude credenziali sensibili
│
├── 📚 DOCUMENTAZIONE
│   ├── SOCIAL_LOGIN_GUIDE.md     # Guida completa social login
│   ├── BASE44_OAUTH_SETUP.md     # Setup OAuth tecnico
│   ├── CONNECTION_STATUS.md       # Status connessione GCP
│   └── docs/
│       └── api_keys/
│           ├── README.md          # Gestione API keys
│           └── API_KEYS_HISTORY.md
│
├── 🔧 UTILITY SCRIPTS
│   ├── verify_gcp_access.py      # Verifica connessione GCP
│   ├── check_oauth_config.py     # Verifica OAuth setup
│   ├── full_gcp_scan.py          # Scan completo progetto
│   ├── list_all_apis.py          # Lista API abilitate
│   ├── test_api_key.py           # Test API keys
│   └── check_permissions.py      # Verifica permessi
│
└── 🔒 CREDENZIALI (non in git)
    └── gcp-service-account.json  # Service account GCP
```

---

## 📖 Guide e Documentazione

### 🔐 Autenticazione e Login

1. **[SOCIAL_LOGIN_GUIDE.md](SOCIAL_LOGIN_GUIDE.md)**
   - Cos'è il social login e come funziona
   - Vantaggi per utenti e business
   - Provider disponibili (Google, Microsoft, Facebook)
   - Default vs Custom OAuth
   - Best practices e sicurezza

2. **[BASE44_OAUTH_SETUP.md](BASE44_OAUTH_SETUP.md)**
   - Risoluzione errore `redirect_uri_mismatch`
   - Setup Google Cloud OAuth Client
   - Configurazione Base44 custom OAuth
   - Checklist configurazione completa
   - Troubleshooting errori comuni

### ☁️ Google Cloud Platform

3. **[CONNECTION_STATUS.md](CONNECTION_STATUS.md)**
   - Status connessione GCP
   - Service account details
   - Servizi accessibili
   - Esempi di utilizzo

### 🔑 API Keys

4. **[docs/api_keys/README.md](docs/api_keys/README.md)**
   - Gestione API keys del progetto
   - Best practices sicurezza
   - Rotazione chiavi

---

## 🛠️ Utility Scripts

Tutti gli script usano il service account in `gcp-service-account.json` (escluso da git).

### Verifica Connessione

```bash
# Verifica autenticazione GCP
python3 verify_gcp_access.py

# Output:
# ✅ Autenticazione riuscita!
# ✅ Accesso a Cloud Storage confermato
```

### Check OAuth Configuration

```bash
# Verifica setup OAuth per Base44
python3 check_oauth_config.py

# Output:
# ✅ OAuth Consent Screen: Configurato
# 📌 Redirect URI necessario: https://app.base44.com/api/apps/auth/callback
```

### Scan Progetto Completo

```bash
# Scansiona tutte le risorse GCP
python3 full_gcp_scan.py

# Output:
# 📦 Cloud Storage: 0 buckets
# 🔧 API Abilitate: 50
# ⚡ Cloud Functions: 0
```

### Lista API Abilitate

```bash
# Lista tutte le API abilitate per categoria
python3 list_all_apis.py

# Output:
# ✅ 50 API abilitate
# 📦 Storage: Cloud Storage ✓
# 🔐 Security: ...
```

### Test API Keys

```bash
# Testa una API key Google
python3 test_api_key.py YOUR_API_KEY

# O usa variabile ambiente
export GCP_API_KEY='your-key'
python3 test_api_key.py
```

---

## 🚀 Quick Start

### 1. Setup Iniziale

```bash
# Clone repository
git clone <repo-url>
cd infrastructure-backup

# Verifica Python
python3 --version  # 3.8+

# Installa dipendenze
pip3 install google-cloud-storage google-auth google-api-python-client requests
```

### 2. Configura Credenziali

Richiedi il file `gcp-service-account.json` all'admin e salvalo nella root del progetto:

```bash
# Il file viene automaticamente ignorato da git (.gitignore)
ls gcp-service-account.json  # Deve esistere
```

### 3. Verifica Connessione

```bash
python3 verify_gcp_access.py
# Dovresti vedere: ✅ CONNESSIONE STABILITA CON SUCCESSO
```

### 4. Setup Social Login per una App

**Se hai l'errore `redirect_uri_mismatch` su una app Base44:**

1. Leggi: [BASE44_OAUTH_SETUP.md](BASE44_OAUTH_SETUP.md)
2. Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency
3. Aggiungi redirect URI: `https://app.base44.com/api/apps/auth/callback`
4. Salva e attendi 5-10 minuti
5. Riprova il login

**Per setup completo custom OAuth (branding personalizzato):**

1. Leggi: [SOCIAL_LOGIN_GUIDE.md](SOCIAL_LOGIN_GUIDE.md)
2. Segui: [BASE44_OAUTH_SETUP.md](BASE44_OAUTH_SETUP.md) sezione "Setup Completo"
3. Configura OAuth Client in GCP
4. Configura Base44 Settings → Authentication
5. Testa!

---

## 🔧 Progetti Configurati

### nonamebar.it

**Status:** 🟡 In configurazione
**Errore Corrente:** `redirect_uri_mismatch`
**Provider:** Google (Custom OAuth)
**Action Required:** Aggiungi redirect URI in GCP

**Fix:**
1. Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency
2. Clicca sul OAuth Client ID per nonamebar
3. Aggiungi: `https://app.base44.com/api/apps/auth/callback`
4. Salva

**Documentazione:** Vedi [BASE44_OAUTH_SETUP.md](BASE44_OAUTH_SETUP.md)

---

## 📊 Risorse GCP Attive

**Progetto:** waipro-agency
**Project Number:** 573103282033

### API Abilitate (50)

- ✅ Cloud Storage
- ✅ BigQuery (6 API)
- ✅ Google Maps (15+ API)
- ✅ Gemini AI & Generative Language
- ✅ Cloud Run, Pub/Sub, Monitoring

### Servizi Non Abilitati

- ❌ Firebase
- ❌ Firestore
- ❌ Cloud Functions
- ❌ IAM API

*(Possono essere abilitati on-demand)*

---

## 🔒 Sicurezza

### File Esclusi da Git (.gitignore)

```
*.json                    # Credenziali service account
gcp-service-account.json  # Specifico
*.key, *.pem              # Chiavi private
.env                      # Environment variables
```

### Best Practices

- ✅ Non committare mai credenziali
- ✅ Usa variabili ambiente per API keys
- ✅ Rota service account keys periodicamente
- ✅ Principio least-privilege per permessi
- ✅ Monitora accessi sospetti

---

## ⚠️ Troubleshooting

### Errore: `redirect_uri_mismatch`

**Causa:** Redirect URI di Base44 non autorizzato
**Fix:** Vedi [BASE44_OAUTH_SETUP.md](BASE44_OAUTH_SETUP.md) → Soluzione Rapida

### Errore: `invalid_grant: account not found`

**Causa:** Service account non valido o disabilitato
**Fix:** Verifica service account in GCP Console

### Errore: `403 Forbidden` su API

**Causa:** API non abilitata o permessi insufficienti
**Fix:**
1. Abilita API in GCP Console
2. Verifica ruoli service account

### Script non trova credenziali

**Causa:** File `gcp-service-account.json` mancante
**Fix:**
```bash
# Richiedi file all'admin e posizionalo nella root
ls gcp-service-account.json
```

---

## 📞 Link Utili

- **Google Cloud Console:** https://console.cloud.google.com/
- **GCP Credentials:** https://console.cloud.google.com/apis/credentials?project=waipro-agency
- **OAuth Consent Screen:** https://console.cloud.google.com/apis/credentials/consent?project=waipro-agency
- **Base44 Documentation:** https://docs.base44.com/
- **Base44 Auth Guide:** https://docs.base44.com/Guides/Managing-login-and-registration

---

## 👥 Contatti

**Progetto:** WAIPRO Agency
**Support Email:** admin@waipro.agency
**GCP Project:** waipro-agency

---

## 📝 Note

- Questo repository è privato - contiene configurazioni sensibili
- Credenziali service account NON sono committate (escluse da git)
- Documentazione aggiornata al: 2025-11-04
- Per modifiche a OAuth setup, consultare sempre le guide

---

## 🎯 Prossimi Passi

### Per Nuovi Progetti Base44:

1. ✅ Crea app in Base44
2. ✅ Connetti custom domain
3. ✅ Configura OAuth Client in GCP
4. ✅ Aggiungi redirect URI Base44
5. ✅ Configura branding (logo, privacy policy)
6. ✅ Testa login flow
7. ✅ Submit per Google review (se custom OAuth)
8. ✅ Lancia in produzione

### Per Progetti Esistenti:

1. ✅ Risolvi errori OAuth (vedi guide)
2. ✅ Migra da default a custom OAuth (per branding)
3. ✅ Aggiungi provider alternativi (Microsoft, Facebook)
4. ✅ Configura data collection at signup
5. ✅ Implementa landing page con privacy policy

---

**Happy coding! 🚀**

Per domande o supporto, consulta le guide in questo repository o contatta admin@waipro.agency.
