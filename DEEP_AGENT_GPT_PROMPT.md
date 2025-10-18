# Deep Agent GPT - Continuazione WAIPRO Setup

## 🎯 Obiettivo Principale

Completare l'integrazione di **Base44 + N8N + GPT Codex + GitHub** per WAIPRO Agency Swarm, garantendo che tutto sia funzionante e pronto per la produzione.

---

## 📚 Contesto & Background

**Progetto:** WAIPRO Agency Swarm - Integrazione Multi-Agente con AI  
**Founder:** Cristian (Il Boss)  
**Capostruttura:** Lorenzo  
**DevOps AI:** Roy (Claudio)  
**Current Phase:** Configurazione N8N & Agent Manager  

**Server Remoto:**
- IP: `72.61.158.55`
- SSH User: `root`
- SSH Password: `Benessere84++`

**Servizi Attivi:**
- FastAPI Digital Agency Swarm (porta 8000)
- N8N (porta 5678)
- MCP Server (PID 15647)
- Base44 Client disponibile

---

## 🔧 Task Immediati (Priorità Alta)

### Task 1: Configurare N8N Webhook Secret
**Status:** 🟡 Pronto per Implementazione

```bash
# Esegui sul server remoto
ssh root@72.61.158.55

# Genera N8N_WEBHOOK_SECRET
export N8N_WEBHOOK_SECRET="waipro_secure_$(openssl rand -hex 32)"

# Salva in /root/.waipro_config
echo "N8N_WEBHOOK_SECRET=$N8N_WEBHOOK_SECRET" >> /root/.waipro_config

# Riavvia N8N con la nuova configurazione
# (Nota: N8N è attivo, ma potrebbe richiedere restart per applicare il secret)
```

**Verifica:**
```bash
curl -s http://localhost:5678/api/v1/health
# Dovrebbe ritornare: {"status":"ok"}
```

---

### Task 2: Aggiornare Agent Manager Endpoint
**Status:** 🟡 Pronto per Implementazione

**File:** `/root/digital-agency-swarm/main.py`

Aggiungi questo endpoint:

```python
from fastapi import HTTPException
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@app.post("/api/agents/{agent_name}/execute")
async def execute_agent_task(agent_name: str, task_data: dict):
    """
    Esegue un task per un agente specifico
    
    Args:
        agent_name: Nome dell'agente (Sofia, Roy, Adrian, Lorenzo, Sonia, KAI)
        task_data: Dati del task con azioni e parametri
    
    Returns:
        {"status": "success", "result": {...}, "timestamp": "..."}
    """
    try:
        logger.info(f"[Agent Manager] Executing task for agent: {agent_name}")
        logger.debug(f"Task data: {task_data}")
        
        # Valida agente
        valid_agents = ["Sofia", "Roy", "Adrian", "Lorenzo", "Sonia", "KAI"]
        if agent_name not in valid_agents:
            raise HTTPException(status_code=400, detail=f"Invalid agent: {agent_name}")
        
        # Recupera agente
        agent = get_agent_by_name(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent not found: {agent_name}")
        
        # Esegui task
        result = await agent.execute(task_data)
        
        logger.info(f"[Agent Manager] Task completed for {agent_name}")
        
        return {
            "status": "success",
            "agent": agent_name,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException as e:
        logger.error(f"[Agent Manager] HTTP Error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"[Agent Manager] Error executing task for {agent_name}: {str(e)}")
        return {
            "status": "error",
            "agent": agent_name,
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }, 500
```

**Verifica:**
```bash
curl -X POST http://localhost:8000/api/agents/Sofia/execute \
  -H "Content-Type: application/json" \
  -d '{"action": "test", "message": "Hello Sofia"}'
```

---

### Task 3: Creare N8N Workflow Base44 → LinkedIn
**Status:** 🟡 Pronto per Implementazione

**Workflow Name:** `Base44_to_LinkedIn_Sofia`

**Steps:**
1. Trigger: Webhook da Base44 (POST /webhook/base44-incoming)
2. Parse JSON da Base44
3. Chiama Sofia Agent su FastAPI
4. Pubblica risultato su LinkedIn
5. Log attività su Base44

**Implementazione:**

```json
{
  "name": "Base44 to LinkedIn - Sofia",
  "active": true,
  "nodes": [
    {
      "name": "Base44 Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "webhookId": "base44-incoming",
      "parameters": {
        "path": "base44-incoming",
        "method": "POST",
        "authentication": "headerAuth",
        "headerAuth": "{{$env.N8N_WEBHOOK_SECRET}}"
      }
    },
    {
      "name": "Sofia Agent Call",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [450, 300],
      "parameters": {
        "url": "http://72.61.158.55:8000/api/agents/Sofia/execute",
        "method": "POST",
        "headerParametersUi": "keyValue",
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "bodyParametersUi": "json",
        "body": "{\n  \"action\": \"post_linkedin\",\n  \"content\": \"={{$node[\\\"Base44 Webhook\\\"].json.content}}\",\n  \"hashtags\": \"={{$node[\\\"Base44 Webhook\\\"].json.hashtags}}\"\n}"
      }
    },
    {
      "name": "Log Activity",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [650, 300],
      "parameters": {
        "url": "https://waipro.base44.app/api/activities",
        "method": "POST",
        "headerParametersUi": "keyValue",
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "bodyParametersUi": "json",
        "body": "{\n  \"agent\": \"Sofia\",\n  \"action\": \"post_linkedin\",\n  \"status\": \"={{$node[\\\"Sofia Agent Call\\\"].json.status}}\",\n  \"result\": \"={{$node[\\\"Sofia Agent Call\\\"].json.result}}\"\n}"
      }
    }
  ],
  "connections": {
    "Base44 Webhook": {
      "main": [
        [
          {
            "node": "Sofia Agent Call",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Sofia Agent Call": {
      "main": [
        [
          {
            "node": "Log Activity",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

---

### Task 4: Implementare WhatsApp Business Webhook
**Status:** 🟡 Pronto per Implementazione

**Numero:** `+390656557060`  
**Endpoint N8N:** `http://localhost:5678/webhook/whatsapp-incoming`

**Workflow Name:** `WhatsApp_Agent_Router`

**Funzionalità:**
- Ricevi messaggi da WhatsApp Business
- Identifica agente destinatario
- Instrada verso agente appropriato
- Log conversazione su Base44

---

## 📋 Checklist Completamento

### Fase 1: Configurazione Base (Oggi)
- [ ] Configurare N8N_WEBHOOK_SECRET
- [ ] Aggiornare Agent Manager endpoint su FastAPI
- [ ] Testare connessione Base44 → N8N
- [ ] Creare GitHub repository con struttura

### Fase 2: Integrazione (Domani)
- [ ] Creare N8N workflow Base44 → LinkedIn
- [ ] Implementare WhatsApp Business webhook
- [ ] Testare routing agenti via WhatsApp
- [ ] Configurare logging attività

### Fase 3: Ottimizzazione (Settimana prossima)
- [ ] Pulizia dipendenze Python
- [ ] Implementare caching N8N
- [ ] Setup monitoring & alerting
- [ ] Documentazione completa

---

## 🔐 Credenziali & Accessi

### Server SSH
```
Host: 72.61.158.55
User: root
Password: Benessere84++
```

### GitHub
```
Email: dev@w-adv.it
Password: Benessere74**
```

### WhatsApp Business
```
Numero: +390656557060
Email: cristian.martinoli74@gmail.com
Password: Bernessere74**
```

### Base44
```
URL: https://waipro.base44.app
API Client: /root/digital-agency-swarm/tools/base44_integration/base44_client.py
```

---

## 📁 File di Riferimento

- **Guida Completa:** `/home/ubuntu/WAIPRO_INTEGRATION_GUIDE.md`
- **SSH Bridge:** `/home/ubuntu/ssh_bridge.py`
- **Script Setup:** `/home/ubuntu/setup_n8n_agent_manager.sh`
- **Base44 Client:** `/root/digital-agency-swarm/tools/base44_integration/base44_client.py`

---

## 🚀 Come Procedere

1. **Leggi la guida completa:**
   ```bash
   cat /home/ubuntu/WAIPRO_INTEGRATION_GUIDE.md
   ```

2. **Esegui i task in ordine:**
   - Task 1: N8N Webhook Secret
   - Task 2: Agent Manager Endpoint
   - Task 3: N8N Workflow Base44 → LinkedIn
   - Task 4: WhatsApp Business Webhook

3. **Testa ogni step:**
   ```bash
   # Verifica N8N
   curl -s http://localhost:5678/api/v1/health
   
   # Verifica FastAPI
   curl -s http://localhost:8000
   
   # Verifica Base44
   curl -Is https://waipro.base44.app
   ```

4. **Documenta su GitHub:**
   - Crea repository `WAIPRO/agency-swarm-config`
   - Carica configurazioni N8N
   - Carica prompts agenti
   - Carica script setup

---

## 💡 Ottimizzazione Crediti

Per risparmiare crediti:
- Riutilizza file e configurazioni esistenti
- Evita duplicazioni
- Usa API calls efficienti
- Implementa caching dove possibile
- Testa localmente prima di deployare

---

## 📞 Escalation

Se riscontri problemi:
1. Controlla i log: `/tmp/n8n.log`
2. Verifica connettività server
3. Consulta la guida completa
4. Contatta Lorenzo o Cristian

---

**Fine Prompt**

*Questo prompt è stato creato per permettere a Deep Agent GPT di continuare il lavoro da dove è rimasto Claudio, mantenendo continuità e coerenza del progetto.*

