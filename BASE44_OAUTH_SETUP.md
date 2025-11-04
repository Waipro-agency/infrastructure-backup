# Base44 OAuth Setup Guide - Risoluzione Errore redirect_uri_mismatch

**Progetto:** waipro-agency
**App:** nonamebar.it
**Errore:** `redirect_uri_mismatch` - https://app.base44.com/api/apps/auth/callback

---

## 🎨 IMPORTANTE: BRANDING PERSONALIZZATO

**Obiettivo:** Quando gli utenti fanno login con Google su **nonamebar.it**, devono vedere il vostro brand/dominio nel popup Google, **NON** "base44.com".

**Soluzione:** Usare **Custom Google OAuth** (non quello di default di Base44).

Con Custom Google OAuth:
- ✅ Gli utenti vedono "nonamebar.it" nel popup Google
- ✅ Branding completo con vostro logo
- ✅ Controllo totale sull'esperienza di login
- ✅ Messaggio professionale per utenti enterprise

**Requisito:** Piano Builder o superiore su Base44 + Metodo di pagamento su Google Cloud

---

## 🔴 PROBLEMA IDENTIFICATO

L'errore `redirect_uri_mismatch` si verifica perché il redirect URI di Base44 non è autorizzato nel client OAuth 2.0 di Google Cloud.

**Redirect URI richiesto da Base44:**
```
https://app.base44.com/api/apps/auth/callback
```

Questo URI **DEVE** essere aggiunto agli "Authorized redirect URIs" nel tuo OAuth 2.0 Client ID.

---

## ✅ SOLUZIONE RAPIDA (5 minuti)

### Passo 1: Accedi alle Credenziali GCP

Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency

### Passo 2: Trova il tuo OAuth 2.0 Client ID

Cerca nella sezione **"OAuth 2.0 Client IDs"** il client che stai usando per nonamebar.it

### Passo 3: Modifica il Client

1. Clicca sul nome del client
2. Scorri fino a **"Authorized redirect URIs"**
3. Clicca **"+ ADD URI"**
4. Incolla esattamente: `https://app.base44.com/api/apps/auth/callback`
5. Clicca **"SAVE"**

### Passo 4: Attendi e Testa

- Attendi **5-10 minuti** per la propagazione
- Riprova il login su nonamebar.it

---

## 📋 CONFIGURAZIONE COMPLETA SECONDO BASE44

### Requisiti Base44 per Custom Google OAuth

#### 1. **Authorized JavaScript Origins**
```
https://nonamebar.it
```

#### 2. **Authorized Redirect URIs** (CRITICO!)
```
https://app.base44.com/api/apps/auth/callback
```

#### 3. **Scopes Richiesti**
```
openid
https://www.googleapis.com/auth/userinfo.email
```

#### 4. **Authorized Domains**
```
nonamebar.it
app.base44.com
```

---

## 🛠️ SETUP COMPLETO OAUTH (Se devi crearlo da zero)

### Step 1: Crea/Modifica OAuth Client

1. Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency
2. Clicca **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Scegli **"Web application"**
4. Configura:

   **Nome:** Base44 - nonamebar.it

   **Authorized JavaScript origins:**
   - `https://nonamebar.it`

   **Authorized redirect URIs:**
   - `https://app.base44.com/api/apps/auth/callback`

5. Clicca **"CREATE"**
6. **Salva Client ID e Client Secret** (li userai in Base44)

### Step 2: Configura OAuth Consent Screen

1. Vai a: https://console.cloud.google.com/apis/credentials/consent?project=waipro-agency
2. Verifica che sia configurato:
   - **App name:** Waipro Agency (o nome app)
   - **User support email:** admin@waipro.agency
   - **Authorized domains:** nonamebar.it, app.base44.com

3. In **Scopes**, aggiungi:
   - `openid`
   - `.../auth/userinfo.email`

4. Clicca **"SAVE AND CONTINUE"**

### Step 3: Verifica Dominio (Se necessario)

1. Vai a: https://search.google.com/search-console
2. Aggiungi e verifica **nonamebar.it**
3. Torna a Google Cloud e aggiungi come "Authorized Domain"

### Step 4: Configura in Base44

1. Vai su **Base44 Dashboard** → **Settings** → **Authentication**
2. Abilita **Google authentication toggle**
3. Seleziona **"Use a custom OAuth from Google Console"**
4. Inserisci:
   - **Client ID:** (dal passo 1)
   - **Client Secret:** (dal passo 1)
5. Clicca **"Update"**

---

## 🔍 CHECKLIST CONFIGURAZIONE

### In Google Cloud Console:

- [ ] OAuth Client ID creato
- [ ] Authorized JavaScript origins: `https://nonamebar.it`
- [ ] **Authorized redirect URIs: `https://app.base44.com/api/apps/auth/callback`** ⚠️ CRITICO
- [ ] OAuth Consent Screen configurato
- [ ] Scopes aggiunti: `openid` e `userinfo.email`
- [ ] Authorized domains: `nonamebar.it`, `app.base44.com`
- [ ] Dominio verificato in Search Console (se richiesto)

### In Base44:

- [ ] Custom domain connesso (nonamebar.it)
- [ ] Google authentication abilitato
- [ ] Custom OAuth configurato con Client ID e Secret
- [ ] Landing page pubblica con Privacy Policy
- [ ] Support page disponibile

---

## 🚨 ERRORI COMUNI E SOLUZIONI

### Errore: `redirect_uri_mismatch`
**Causa:** Redirect URI non autorizzato
**Soluzione:** Aggiungi `https://app.base44.com/api/apps/auth/callback` agli Authorized redirect URIs

### Errore: `invalid_client`
**Causa:** Client ID o Secret errati
**Soluzione:** Verifica di aver copiato correttamente le credenziali in Base44

### Errore: `access_denied`
**Causa:** Scopes non autorizzati
**Soluzione:** Verifica che `openid` e `userinfo.email` siano configurati

### Errore: `unauthorized_domain`
**Causa:** Dominio non autorizzato
**Soluzione:** Aggiungi nonamebar.it come Authorized Domain

---

## 📞 LINK UTILI

- **GCP Credentials:** https://console.cloud.google.com/apis/credentials?project=waipro-agency
- **OAuth Consent Screen:** https://console.cloud.google.com/apis/credentials/consent?project=waipro-agency
- **Search Console (Verifica Dominio):** https://search.google.com/search-console
- **Base44 Documentation:** https://docs.base44.com/Guides/Managing-login-and-registration

---

## 🎯 AZIONE IMMEDIATA PER RISOLVERE L'ERRORE

**Per risolvere l'errore su nonamebar.it SUBITO:**

1. Vai qui: https://console.cloud.google.com/apis/credentials?project=waipro-agency
2. Clicca sul tuo OAuth 2.0 Client ID
3. In "Authorized redirect URIs", aggiungi: `https://app.base44.com/api/apps/auth/callback`
4. Clicca "SAVE"
5. Aspetta 5-10 minuti
6. Riprova il login su nonamebar.it

**Fatto!** L'errore dovrebbe scomparire.

---

**Status Corrente:**
- ✅ OAuth Consent Screen: Configurato (Waipro Agency)
- ❌ Redirect URI: Mancante (da aggiungere)
- ⚠️  Client ID: Da verificare/configurare in Base44

**Prossimi Passi:**
1. Aggiungi redirect URI in GCP
2. Verifica Client ID e Secret in Base44
3. Testa il login
