# 🚀 Setup MCP per Claude Desktop - WAIPRO Agency

## 📋 Cosa fa questo MCP?

Questo MCP (Model Context Protocol) server permette a **Claude Desktop** di:

✅ **Caricare file** (JSON, configurazioni, credenziali)
✅ **Accedere al server VPS** WAIPRO (72.61.158.55)
✅ **Configurare Google Cloud** automaticamente
✅ **Gestire credenziali** in modo sicuro
✅ **Integrare Opus 4** con il sistema WAIPRO

---

## 🔧 Installazione su Claude Desktop

### Step 1: Trova il file di configurazione Claude Desktop

**Su macOS:**
```bash
~/.config/claude/claude_desktop_config.json
```

**Su Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Su Linux:**
```bash
~/.config/claude/claude_desktop_config.json
```

---

### Step 2: Aggiungi la configurazione MCP

Apri `claude_desktop_config.json` e aggiungi:

```json
{
  "mcpServers": {
    "waipro-integration": {
      "command": "python3",
      "args": [
        "/home/user/infrastructure-backup/google_cloud_integration/mcp_server_waipro.py"
      ],
      "env": {
        "WAIPRO_WORKSPACE": "/home/user/infrastructure-backup",
        "WAIPRO_VPS": "72.61.158.55"
      },
      "disabled": false
    }
  }
}
```

**NOTA:** Se hai già altri MCP server, aggiungi solo la sezione `"waipro-integration": {...}` dentro `"mcpServers"`.

---

### Step 3: Riavvia Claude Desktop

1. Chiudi completamente Claude Desktop
2. Riapri Claude Desktop
3. Dovresti vedere un'icona MCP nella barra in basso

---

## 📤 Come Caricare il File JSON Google Cloud

Una volta configurato l'MCP, puoi caricare il file JSON in **2 modi**:

### Metodo 1: Copia/Incolla (Più semplice)

1. Apri il file `waipro-agency-be11621d4340.json`
2. Copia tutto il contenuto
3. In Claude Desktop, scrivi:

```
Carica questo JSON di Google Cloud:

{
  "type": "service_account",
  "project_id": "waipro-agency",
  ...
}
```

L'MCP salverà automaticamente il file!

---

### Metodo 2: Riferimento Diretto

Se il file è già sul tuo computer, scrivi:

```
Leggi il file Google Cloud da: /path/to/waipro-agency-be11621d4340.json
```

---

## 🎯 Comandi Disponibili nell'MCP

Una volta attivo, puoi usare questi comandi in Claude Desktop:

### 📤 Upload File
```
Carica il file credentials.json con questo contenuto: {...}
```

### 📋 Lista File Caricati
```
Mostrami i file caricati nell'MCP WAIPRO
```

### 📖 Leggi File
```
Leggi il file waipro-agency-be11621d4340.json
```

### ⚙️ Configura Google Cloud
```
Configura Google Cloud usando il file waipro-agency-be11621d4340.json
```

---

## 🧪 Test dell'MCP

Per verificare che funzioni, apri Claude Desktop e scrivi:

```
Test MCP WAIPRO: mostrami lo status
```

Dovresti vedere:
- ✅ MCP attivo
- 📁 Workspace directory
- 📤 Upload directory pronta

---

## 🔒 Sicurezza

L'MCP salva i file in:
```
/home/user/infrastructure-backup/uploads/
```

**Importante:**
- I file JSON con credenziali sono salvati localmente
- Non vengono condivisi pubblicamente
- Sono accessibili solo dall'MCP server

---

## 🆘 Troubleshooting

### Problema: MCP non si attiva

**Soluzione:**
1. Verifica che Python 3 sia installato: `python3 --version`
2. Controlla i permessi del file: `chmod +x mcp_server_waipro.py`
3. Guarda i log di Claude Desktop

### Problema: File non trovato

**Soluzione:**
1. Verifica il percorso assoluto nel config
2. Assicurati che il file `mcp_server_waipro.py` esista
3. Usa percorsi assoluti, non relativi

### Problema: Python module non trovato

**Soluzione:**
```bash
pip3 install --user json pathlib
```

---

## 📚 Prossimi Passi

Una volta configurato l'MCP:

1. ✅ Carica il file JSON Google Cloud
2. ✅ Configura OAuth 2.0 per login/registrazione
3. ✅ Attiva Claude Opus 4 con i 250€ bonus
4. ✅ Integra con Base44 CRM
5. ✅ Testa il sistema completo

---

## 🔗 Link Utili

- **Claude Desktop:** https://claude.ai/download
- **MCP Documentation:** https://docs.anthropic.com/mcp
- **WAIPRO Integration Guide:** ../WAIPRO_INTEGRATION_GUIDE.md

---

**Creato per:** WAIPRO Agency
**Data:** 4 Novembre 2025
**Versione:** 1.0

🎉 Ora puoi caricare il JSON direttamente da Claude Desktop!
