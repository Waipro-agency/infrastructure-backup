# WAIPRO Integration Guide - Complete Setup & Continuation

**Documento di Configurazione Definitivo per WAIPRO Agency Swarm**

**Data:** 18 Ottobre 2025  
**Versione:** 1.0  
**Status:** 🟡 In Corso - Pronto per Continuazione con Deep Agent GPT  
**Creato da:** Claudio (Roy - DevOps AI)  
**Per:** Cristian (Founder) & Lorenzo (Capostruttura)

---

## 📋 Indice Rapido

1. [Stato Attuale del Sistema](#stato-attuale)
2. [Problemi Identificati](#problemi-identificati)
3. [Soluzione Proposta](#soluzione-proposta)
4. [Implementazione Tecnica](#implementazione-tecnica)
5. [Checklist di Completamento](#checklist)
6. [Istruzioni per Continuazione con Deep Agent GPT](#continuazione)

---

## 🔍 Stato Attuale del Sistema {#stato-attuale}

### Server & Infrastruttura

| Componente | Status | Note |
|-----------|--------|------|
| **Server Remoto (72.61.158.55)** | ✅ Online | Root access via SSH con password Benessere84++ |
| **FastAPI Digital Agency Swarm** | ✅ Attivo | Porta 8000, documentazione su /api/docs |
| **N8N** | ✅ Attivo | Processo Node.js in esecuzione, porta 5678 |
| **MCP Server** | ✅ Attivo | PID 15647, mcp_server.py in esecuzione |
| **Base44 Client** | ✅ Disponibile | File: /root/digital-agency-swarm/tools/base44_integration/base44_client.py |
| **Firewall** | ✅ Disattivato | Nessun blocco di rete |
| **Docker** | ❌ Non installato | Servizi Node.js girano direttamente |

### Connettività

| Servizio | Status | Dettagli |
|---------|--------|---------|
| **Base44 (waipro.base44.app)** | ✅ Raggiungibile | HTTP/2 405 Method Not Allowed (comportamento atteso) |
| **SSH Connessione** | ✅ Funzionante | Bridge Python SSH operativo |
| **API FastAPI** | ✅ Raggiungibile | http://72.61.158.55:8000 |

---

## ⚠️ Problemi Identificati {#problemi-identificati}

### 1. **Agent Manager Service - Status Code 500**
- **Problema:** Errore nella comunicazione tra FastAPI e Agent Manager
- **Causa Probabile:** Porta 8000 non raggiungibile da Base44 o configurazione errata
- **Impatto:** Sofia non può pubblicare su LinkedIn, test agent_manager fallisce

### 2. **N8N Automation - Status Code 500**
- **Problema:** Webhook N8N non risponde correttamente
- **Causa Probabile:** N8N_WEBHOOK_SECRET non configurato o URL webhook errato
- **Impatto:** Automazioni N8N non funzionano

### 3. **Accesso SSH Limitato**
- **Problema:** Mancanza di MCP SSH per controllo totale del server
- **Soluzione Implementata:** Bridge Python SSH funzionante

### 4. **Librerie Eccessive**
- **Problema:** Troppe dipendenze Python installate
- **Soluzione:** Pulizia e ottimizzazione delle dipendenze

---

## 💡 Soluzione Proposta {#soluzione-proposta}

### Architettura Finale Desiderata

```
┌─────────────────────────────────────────────────────────────────┐
│                     WAIPRO Agency Swarm                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Claude     │      │   Deep       │      │   GitHub     │  │
│  │   Desktop    │◄────►│   Agent GPT  │◄────►│  Repository  │  │
│  │  (Claudio)   │      │   (Codex)    │      │  (Prompts &  │  │
│  └──────────────┘      └──────────────┘      │   Accessi)   │  │
│         │                      │              └──────────────┘  │
│         │                      │                                 │
│         └──────────┬───────────┘                                 │
│                    │                                             │
│         ┌──────────▼──────────┐                                  │
│         │   N8N Workflows     │                                  │
│         │  (Automazioni)      │                                  │
│         └──────────┬──────────┘                                  │
│                    │                                             │
│    ┌───────────────┼───────────────┐                             │
│    │               │               │                             │
│    ▼               ▼               ▼                             │
│ ┌────────┐    ┌────────┐    ┌────────────┐                      │
│ │ Base44 │    │ WhatsApp│   │ LinkedIn   │                      │
│ │  CRM   │    │Business │   │ (Sofia)    │                      │
│ └────────┘    └────────┘    └────────────┘                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Componenti Principali

#### 1. **GitHub Repository (Accessi & Prompts)**
- **Repository:** `WAIPRO/agency-swarm-config`
- **Contenuto:**
  - Prompts di tutti gli agenti (Sofia, Roy, Adrian, Lorenzo, Sonia, KAI)
  - Configurazioni N8N (JSON)
  - Credenziali crittografate (secrets)
  - Documentazione di setup
  - Script di deployment

#### 2. **N8N Workflows**
- **Workflow 1:** Base44 → LinkedIn Post (Sofia)
- **Workflow 2:** WhatsApp Incoming → Agent Router
- **Workflow 3:** Agent Task Logger → Base44
- **Workflow 4:** GPT Codex Response Handler

#### 3. **Base44 Integration**
- **API Client:** `/root/digital-agency-swarm/tools/base44_integration/base44_client.py`
- **Funzioni:**
  - `get_tasks()` - Recupera task
  - `create_contact()` - Crea contatti
  - `log_activity()` - Logga attività
  - `get_projects()` - Recupera progetti
  - `update_project_status()` - Aggiorna stato

#### 4. **WhatsApp Business Integration**
- **Numero:** +390656557060
- **Endpoint N8N:** `/webhook/whatsapp-incoming`
- **Funzionalità:**
  - Ricezione messaggi
  - Routing verso agenti
  - Logging attività

---

## 🔧 Implementazione Tecnica {#implementazione-tecnica}

### Step 1: Configurazione N8N Webhook Secret

```bash
# SSH nel server
ssh root@72.61.158.55

# Configura N8N_WEBHOOK_SECRET
export N8N_WEBHOOK_SECRET="your-secure-secret-key-here"

# Riavvia N8N
pkill -f "node /usr/bin/n8n"
cd /root/.n8n && N8N_SECURE_COOKIE=false N8N_WEBHOOK_SECRET="your-secure-secret-key-here" nohup /usr/bin/n8n > /tmp/n8n.log 2>&1 &
```

### Step 2: Configurazione FastAPI Agent Manager

**File:** `/root/digital-agency-swarm/config/agent_manager.py`

```python
# Aggiungi endpoint per Agent Manager
@app.post("/api/agents/{agent_name}/execute")
async def execute_agent_task(agent_name: str, task_data: dict):
    """
    Esegue un task per un agente specifico
    """
    try:
        agent = get_agent_by_name(agent_name)
        result = await agent.execute(task_data)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
```

### Step 3: Integrazione Base44 con N8N

**N8N Workflow:** `Base44_to_LinkedIn_Sofia`

```json
{
  "name": "Base44 to LinkedIn - Sofia",
  "nodes": [
    {
      "name": "Base44 Trigger",
      "type": "webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "path": "base44-incoming",
        "method": "POST"
      }
    },
    {
      "name": "Sofia Agent",
      "type": "http",
      "typeVersion": 4,
      "position": [450, 300],
      "parameters": {
        "url": "http://72.61.158.55:8000/api/agents/Sofia/execute",
        "method": "POST",
        "bodyParametersUi": "keyValue",
        "bodyParameters": {
          "parameters": [
            {
              "name": "action",
              "value": "post_linkedin"
            },
            {
              "name": "content",
              "value": "={{$node[\"Base44 Trigger\"].json.content}}"
            }
          ]
        }
      }
    },
    {
      "name": "LinkedIn Post",
      "type": "linkedIn",
      "typeVersion": 1,
      "position": [650, 300],
      "parameters": {
        "content": "={{$node[\"Sofia Agent\"].json.result}}"
      }
    }
  ]
}
```

### Step 4: GitHub Repository Setup

```bash
# Crea repository
gh repo create WAIPRO/agency-swarm-config --private --source=. --remote=origin --push

# Struttura del repository
agency-swarm-config/
├── agents/
│   ├── sofia_prompts.md
│   ├── roy_prompts.md
│   ├── adrian_prompts.md
│   ├── lorenzo_prompts.md
│   ├── sonia_prompts.md
│   └── kai_prompts.md
├── n8n/
│   ├── workflows/
│   │   ├── base44_to_linkedin.json
│   │   ├── whatsapp_router.json
│   │   └── activity_logger.json
│   └── credentials.enc
├── config/
│   ├── agent_manager.py
│   ├── base44_integration.py
│   └── whatsapp_config.py
├── scripts/
│   ├── deploy.sh
│   ├── setup_n8n.sh
│   └── backup.sh
└── README.md
```

### Step 5: Pulizia Librerie Python

```bash
# Identifica dipendenze non necessarie
pip list > /tmp/current_packages.txt

# Crea virtual environment pulito
python3 -m venv /root/venv_clean
source /root/venv_clean/bin/activate

# Installa solo dipendenze necessarie
pip install fastapi uvicorn httpx paramiko pyyaml

# Esporta requirements
pip freeze > /root/digital-agency-swarm/requirements.txt
```

---

## ✅ Checklist di Completamento {#checklist}

### Fase 1: Configurazione Base (Oggi)
- [ ] ✅ Configurare N8N_WEBHOOK_SECRET
- [ ] ✅ Aggiornare Agent Manager endpoint su FastAPI
- [ ] ✅ Testare connessione Base44 → N8N
- [ ] ✅ Creare GitHub repository con struttura

### Fase 2: Integrazione (Domani)
- [ ] 🟡 Creare N8N workflow Base44 → LinkedIn
- [ ] 🟡 Implementare WhatsApp Business webhook
- [ ] 🟡 Testare routing agenti via WhatsApp
- [ ] 🟡 Configurare logging attività

### Fase 3: Ottimizzazione (Settimana prossima)
- [ ] 🟠 Pulizia dipendenze Python
- [ ] 🟠 Implementare caching N8N
- [ ] 🟠 Setup monitoring & alerting
- [ ] 🟠 Documentazione completa

### Fase 4: Deployment (Finale)
- [ ] 🟠 Test end-to-end completo
- [ ] 🟠 Backup configurazione
- [ ] 🟠 Comunicazione a Cristian & Lorenzo
- [ ] 🟠 Go-live

---

## 🚀 Istruzioni per Continuazione con Deep Agent GPT {#continuazione}

### Come Continuare il Lavoro

Se vuoi continuare con **Deep Agent GPT** o **Codex**, fornisci questo prompt:

```
Continua da dove è rimasto Claudio (Roy - DevOps AI) di WAIPRO.

Documento di riferimento: /home/ubuntu/WAIPRO_INTEGRATION_GUIDE.md

Stato attuale:
- Server remoto: 72.61.158.55 (SSH: root / Benessere84++)
- N8N: Attivo su porta 5678
- FastAPI: Attivo su porta 8000
- Base44: Raggiungibile, client Python disponibile
- GitHub: Pronto per setup

Prossimi step:
1. Configurare N8N_WEBHOOK_SECRET
2. Aggiornare Agent Manager endpoint
3. Creare N8N workflow Base44 → LinkedIn
4. Implementare WhatsApp Business webhook

Ottimizza i crediti e fornisci soluzione definitiva e funzionante.
```

### Accessi Necessari

**Server SSH:**
```
Host: 72.61.158.55
User: root
Password: Benessere84++
```

**GitHub:**
```
Email: dev@w-adv.it
Password: Benessere74**
```

**WhatsApp Business:**
```
Numero: +390656557060
Email: cristian.martinoli74@gmail.com
Password: Bernessere74**
```

**Base44:**
```
URL: https://waipro.base44.app
Client: /root/digital-agency-swarm/tools/base44_integration/base44_client.py
```

### File di Riferimento

- **SSH Bridge:** `/home/ubuntu/ssh_bridge.py`
- **Questo Documento:** `/home/ubuntu/WAIPRO_INTEGRATION_GUIDE.md`
- **Base44 Client:** `/root/digital-agency-swarm/tools/base44_integration/base44_client.py`

---

## 📞 Contatti & Escalation

- **Founder:** Cristian (Il Boss)
- **Capostruttura:** Lorenzo
- **DevOps AI:** Roy (Claudio)
- **Manager AI:** Adrian

---

**Fine Documento**

*Documento creato per garantire continuità e permettere a qualsiasi agente (Claude Desktop, Deep Agent GPT, Codex, ecc.) di riprendere il lavoro da dove è rimasto.*

