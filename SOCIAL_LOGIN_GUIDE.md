# 🔐 Guida al Social Login per Base44

## Cos'è il Social Login?

Il **Social Login** (o "Sign in with Google/Facebook/Microsoft") permette agli utenti di accedere alla tua app usando le credenziali dei loro account social esistenti, invece di creare nuove username e password.

### 🎯 Vantaggi del Social Login

**Per gli Utenti:**
- ✅ **Accesso istantaneo** - Niente password da ricordare
- ✅ **Sicurezza** - Credenziali gestite da provider affidabili (Google, Microsoft, Facebook)
- ✅ **Velocità** - Login in 1 click
- ✅ **Convenienza** - Un solo account per multiple app

**Per i Proprietari delle App:**
- ✅ **Più conversioni** - Il 77% degli utenti preferisce social login
- ✅ **Meno abbandoni** - Registrazioni più veloci = più utenti completano signup
- ✅ **Dati verificati** - Email già verificate dai provider
- ✅ **Meno supporto** - Meno problemi con password dimenticate
- ✅ **Sicurezza** - OAuth 2.0 è uno standard sicuro e testato

---

## 🏗️ Come Funziona il Social Login

```
1. Utente clicca "Sign in with Google" su nonamebar.it
      ↓
2. Viene reindirizzato alla pagina di login Google
      ↓
3. Utente inserisce credenziali Google (o è già loggato)
      ↓
4. Google chiede permesso di condividere dati (email, nome)
      ↓
5. Utente approva
      ↓
6. Google reindirizza a: app.base44.com/api/apps/auth/callback
      ↓
7. Base44 crea/autentica l'utente nella tua app
      ↓
8. Utente è loggato su nonamebar.it ✅
```

---

## 🎨 Branding: Default vs Custom OAuth

### Opzione 1: Default Base44 OAuth (Veloce)
**Setup:** 2 minuti
**Branding:** Gli utenti vedono "base44.com" nel popup Google

```
Popup Google mostra:
┌─────────────────────────────────┐
│ Sign in with Google             │
│                                 │
│ base44.com wants to access:    │
│ • Your email address            │
│ • Your basic profile info       │
│                                 │
│ [Continue] [Cancel]             │
└─────────────────────────────────┘
```

**Ideale per:**
- Test e sviluppo
- Progetti personali
- App interne

### Opzione 2: Custom Google OAuth (Brandizzato) ⭐ CONSIGLIATO
**Setup:** 30-60 minuti + 1-5 giorni approvazione Google
**Branding:** Gli utenti vedono **il TUO dominio** (es: nonamebar.it)

```
Popup Google mostra:
┌─────────────────────────────────┐
│ Sign in with Google             │
│                                 │
│ nonamebar.it wants to access:  │  ← IL TUO BRAND!
│ • Your email address            │
│ • Your basic profile info       │
│                                 │
│ [Continue] [Cancel]             │
└─────────────────────────────────┘
```

**Ideale per:**
- ✅ App professionali/aziendali
- ✅ Clienti esterni
- ✅ Branding importante
- ✅ Requisiti enterprise

---

## 📋 Provider di Social Login Supportati da Base44

### 1. **Google** ⭐ PIÙ POPOLARE
- 2+ miliardi di utenti
- Ottimo per B2B e B2C
- Setup relativamente semplice

### 2. **Microsoft**
- Ideale per ambiente aziendale
- Integrazione con Office 365
- Perfetto per B2B

### 3. **Facebook**
- Ottimo per app social
- 2.9+ miliardi di utenti
- Popolare per B2C

### 4. **Email & Password**
- Sempre disponibile come fallback
- Utenti che non usano social
- Controllo completo

### 5. **SSO (Single Sign-On)**
- Solo per piani Elite
- Provider come Okta, Auth0
- Enterprise-grade

---

## 🔧 Setup per nonamebar.it (Progetto waipro-agency)

### Configurazione Attuale

**Progetto Google Cloud:** waipro-agency
**OAuth Consent Screen:** ✅ Configurato
- Nome: Waipro Agency
- Email: admin@waipro.agency

**App Base44:** nonamebar.it
**Provider Attivi:** Google (Custom OAuth)

### Obiettivo
Quando un utente fa login su **nonamebar.it**, deve vedere:
```
"nonamebar.it richiede accesso al tuo account Google"
```
NON "base44.com richiede accesso..."

---

## 🚀 Quick Start per Altri Progetti

### Per aggiungere Google Login a una nuova app:

1. **In Base44:**
   - Dashboard → Settings → Authentication
   - Abilita "Google"
   - Scegli "Default Base44 OAuth" (veloce) o "Custom OAuth" (brandizzato)

2. **Se Custom OAuth:**
   - Crea OAuth Client in Google Cloud
   - Aggiungi redirect URI: `https://app.base44.com/api/apps/auth/callback`
   - Copia Client ID e Secret in Base44

3. **Testa:**
   - Prova il login sulla tua app
   - Verifica che funzioni correttamente

---

## 🔒 Sicurezza e Privacy

### Dati Raccolti
Con Google OAuth, Base44 riceve solo:
- Email address (verificata)
- Nome completo
- Foto profilo (opzionale)

**NON riceve:**
- Password Google
- Contatti
- Email o altri dati privati

### Scopes Utilizzati
```
openid                                      - Identità utente
https://www.googleapis.com/auth/userinfo.email  - Email
```

### Dove vengono Salvati i Dati
- **Base44 Dataset "Users"** - Gestito automaticamente
- Dati sicuri, accessibili solo agli admin dell'app
- Conformità GDPR

---

## 📊 Best Practices

### 1. Offrire Multiple Opzioni
```
✅ Google
✅ Email/Password
✅ Microsoft (se B2B)
```
Non tutti usano Google - offri alternative!

### 2. Comunicazione Chiara
Spiega agli utenti:
- Perché chiedi il social login
- Quali dati raccoglierai
- Come li userai

### 3. Fallback
Mantieni sempre Email/Password come opzione, per utenti che:
- Non hanno account social
- Non vogliono connettere account social
- Hanno problemi tecnici

### 4. Privacy Policy
**OBBLIGATORIO per Custom OAuth:**
- Pagina pubblica (non dietro login)
- Collegata dalla homepage
- Conforme a GDPR

### 5. Testing
Testa il flusso completo:
- Registrazione nuovo utente
- Login utente esistente
- Logout
- Password reset (se email/password abilitato)

---

## ⚠️ Errori Comuni

### `redirect_uri_mismatch`
**Causa:** Redirect URI non configurato
**Fix:** Aggiungi `https://app.base44.com/api/apps/auth/callback` in GCP

### `invalid_client`
**Causa:** Client ID/Secret errati
**Fix:** Verifica credenziali in Base44 Settings

### `access_denied`
**Causa:** Utente ha rifiutato permessi
**Fix:** Normale - l'utente può riprovare

### Popup si chiude subito
**Causa:** Popup blocker del browser
**Fix:** Chiedi all'utente di abilitare popup per tuo dominio

---

## 📚 Risorse

- **Base44 Documentation:** https://docs.base44.com/Guides/Managing-login-and-registration
- **Google OAuth Setup:** Vedi `BASE44_OAUTH_SETUP.md` in questo repo
- **Google Cloud Console:** https://console.cloud.google.com/apis/credentials?project=waipro-agency

---

## 🎓 Terminologia

**OAuth 2.0** - Standard di autenticazione sicuro usato dai provider

**Client ID** - Identificatore pubblico della tua app

**Client Secret** - Password segreta (mai condividere!)

**Redirect URI** - Dove Google rimanda l'utente dopo login

**Scopes** - Permessi/dati che la tua app richiede

**Consent Screen** - Popup che chiede permesso all'utente

**Authorized Domain** - Domini verificati/autorizzati per OAuth

---

## 💡 Suggerimenti Finali

1. **Inizia con Default OAuth** per testare velocemente
2. **Passa a Custom OAuth** quando sei pronto per produzione
3. **Testa sempre** prima di lanciare
4. **Monitora** i tassi di conversione (social vs email/password)
5. **Chiedi feedback** agli utenti sul processo di login

---

**Domande?** Consulta `BASE44_OAUTH_SETUP.md` per la configurazione tecnica completa.

**Problemi?** Controlla la sezione "Errori Comuni" sopra.

**Ready to launch?** Segui la checklist in `BASE44_OAUTH_SETUP.md`!
