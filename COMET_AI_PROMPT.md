# 🤖 Prompt per Comet.AI - Configurazione OAuth nonamebar.it

## COPIA E INCOLLA QUESTO PROMPT A COMET.AI:

```
Ciao Comet! Devi configurare Google OAuth per la mia app nonamebar.it su Base44.

TASK: Crea un nuovo OAuth 2.0 Client ID nella Google Cloud Console per il progetto waipro-agency.

STEP-BY-STEP:

1. Vai a questa URL:
   https://console.cloud.google.com/apis/credentials?project=waipro-agency

2. Assicurati che il progetto selezionato sia "waipro-agency" (vedi in alto)

3. Clicca il bottone "+ CREATE CREDENTIALS" nella barra in alto

4. Dal menu a discesa, seleziona "OAuth client ID"

5. Se ti chiede di configurare l'OAuth consent screen prima:
   - Clicca "CONFIGURE CONSENT SCREEN"
   - Scegli "External" user type
   - Clicca "CREATE"
   - Inserisci:
     * App name: "nonamebar.it"
     * User support email: admin@waipro.agency
     * Authorized domains: nonamebar.it, app.base44.com
     * Developer contact: admin@waipro.agency
   - Clicca "SAVE AND CONTINUE"
   - Negli scopes, aggiungi:
     * openid
     * .../auth/userinfo.email
   - Clicca "SAVE AND CONTINUE" fino alla fine
   - Torna alla pagina Credentials

6. Ora crea il client OAuth:
   - Clicca "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Application type: Seleziona "Web application"
   - Name: "nonamebar.it - Base44"

7. In "Authorized JavaScript origins":
   - Clicca "+ ADD URI"
   - Aggiungi: https://nonamebar.it
   - Clicca "+ ADD URI" di nuovo
   - Aggiungi: https://app.base44.com

8. In "Authorized redirect URIs":
   - Clicca "+ ADD URI"
   - Aggiungi ESATTAMENTE questo URI:
     https://app.base44.com/api/apps/auth/callback

9. Clicca il bottone blu "CREATE" in basso

10. Apparirà un popup con "OAuth client created"
    - Copia il "Client ID" (stringa lunga tipo: 123456789-abc.apps.googleusercontent.com)
    - Copia il "Client secret" (stringa tipo: GOCSPX-abc123xyz)
    - Puoi anche cliccare "DOWNLOAD JSON" per salvare

11. IMPORTANTE: Dammi questi valori:
    Client ID: [incolla qui]
    Client Secret: [incolla qui]

VERIFICA FINALE:
- Il Client ID deve finire con ".apps.googleusercontent.com"
- Il Client Secret deve iniziare con "GOCSPX-"
- Il redirect URI deve essere ESATTAMENTE: https://app.base44.com/api/apps/auth/callback

Se riscontri errori, copiami l'errore esatto e risolviamo insieme.

Grazie!
```

---

## 📋 DOPO CHE COMET TI DÀ LE CREDENZIALI:

1. Vai su Base44: https://app.base44.com
2. Apri la tua app nonamebar.it
3. Vai a: Settings → Authentication
4. Trova la sezione "Google"
5. Toggle ON "Use a custom OAuth from Google Console"
6. Incolla:
   - **Client ID** (che ti ha dato Comet)
   - **Client Secret** (che ti ha dato Comet)
7. Clicca "Update"
8. Testa il login su nonamebar.it

---

## 🎯 ALTERNATIVA SE COMET NON HA ACCESSO:

Fai tu manualmente seguendo le istruzioni sopra. Sono letteralmente 10 click. Ti mando anche uno screenshot guide se vuoi.

O possiamo fare un veloce screen share di 2 minuti e lo faccio insieme a te mentre guardi.

---

## ✅ RISULTATO FINALE:

Una volta configurato, quando un utente clicca "Sign in with Google" su nonamebar.it, vedrà:

```
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

NON vedrà più "base44.com" ma "nonamebar.it" - professionale e brandizzato!

---

**Fatto! Hai il prompt per Comet.AI pronto! 🚀**

Vuoi che ti crei anche uno screenshot guide visuale o va bene così?
