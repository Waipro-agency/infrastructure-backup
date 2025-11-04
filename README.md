# Infrastructure Backup - WAIPRO Agency

## 📋 Panoramica

Repository centralizzato per la gestione dell'infrastruttura WAIPRO Agency, inclusi backup di configurazioni, documentazione API keys, e setup per reverse proxy.

**Repository**: `Waipro-agency/infrastructure-backup`
**Server Principale**: 72.61.158.55
**Domini**: waipro.it, api.waipro.it, n8n.waipro.it

---

## 📁 Struttura Repository

```
infrastructure-backup/
├── README.md                           # Questo file
├── WAIPRO_INTEGRATION_GUIDE.md         # Guida completa integrazione
├── DEEP_AGENT_GPT_PROMPT.md            # Prompt per Deep Agent GPT
├── REVERSE_ACCESS_SETUP.md             # 🆕 Setup reverse proxy completo
├── ssh_bridge.py                       # Bridge SSH Python
│
├── api_keys/                           # Gestione API Keys
│   ├── README.md                       # Indice API keys
│   └── API_KEYS_HISTORY.md             # Storico cronologico
│
├── nginx_config/                       # 🆕 Configurazioni Nginx
│   └── waipro.it                       # Config reverse proxy
│
├── scripts/                            # 🆕 Script di deployment
│   └── deploy_reverse_proxy.sh         # Deploy automatico reverse proxy
│
├── digital-agency-swarm_config/        # Configurazioni FastAPI
│   └── digital-agency-swarm_docker-compose.yml
│
└── n8n_config/                         # Configurazioni N8N
    └── n8n_docker-compose.yml
```

---

## 🚀 Quick Start

### 1. Reverse Proxy Setup (Nuovo!)

Per configurare l'accesso reverse su waipro.it:

```bash
# Sul server remoto (72.61.158.55)
git clone https://github.com/Waipro-agency/infrastructure-backup.git
cd infrastructure-backup

# Esegui deployment automatico
sudo bash scripts/deploy_reverse_proxy.sh
```

**Documentazione completa**: [REVERSE_ACCESS_SETUP.md](./REVERSE_ACCESS_SETUP.md)

### 2. Configurazione DNS

Assicurati che i seguenti record DNS puntino a **72.61.158.55**:

| Tipo | Nome | Valore |
|------|------|--------|
| A | waipro.it | 72.61.158.55 |
| A | www.waipro.it | 72.61.158.55 |
| A | api.waipro.it | 72.61.158.55 |
| A | n8n.waipro.it | 72.61.158.55 |

### 3. Accesso ai Servizi

Dopo il deployment:

- **Main Website**: https://waipro.it
- **API Endpoint**: https://api.waipro.it
- **API Documentation**: https://api.waipro.it/docs
- **N8N Workflows**: https://n8n.waipro.it

---

## 📚 Documentazione

### Guide Principali

| Documento | Descrizione |
|-----------|-------------|
| [WAIPRO_INTEGRATION_GUIDE.md](./WAIPRO_INTEGRATION_GUIDE.md) | Guida completa integrazione Agency Swarm, Base44, N8N |
| [REVERSE_ACCESS_SETUP.md](./REVERSE_ACCESS_SETUP.md) | Setup reverse proxy con Nginx, SSL/TLS, sicurezza |
| [DEEP_AGENT_GPT_PROMPT.md](./DEEP_AGENT_GPT_PROMPT.md) | Prompt per continuazione con Deep Agent GPT |
| [api_keys/README.md](./api_keys/README.md) | Gestione centralizzata API Keys |

### Script Utili

| Script | Descrizione | Uso |
|--------|-------------|-----|
| `scripts/deploy_reverse_proxy.sh` | Deploy automatico reverse proxy | `sudo bash scripts/deploy_reverse_proxy.sh` |
| `ssh_bridge.py` | Bridge Python per comandi SSH remoti | `python ssh_bridge.py <host> <user> <pass> <cmd>` |

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

### Base44
```
URL: https://waipro.base44.app
Client: /root/digital-agency-swarm/tools/base44_integration/base44_client.py
```

### WhatsApp Business
```
Numero: +390656557060
Email: cristian.martinoli74@gmail.com
Password: Bernessere74**
```

---

## 🏗️ Architettura Infrastruttura

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet (HTTPS/SSL)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   Nginx Reverse Proxy (waipro.it)  │
        │         Port 80/443 (SSL)          │
        └────────┬──────────────┬────────────┘
                 │              │
      ┌──────────▼─────┐   ┌───▼──────────────┐
      │  FastAPI       │   │  N8N Workflows   │
      │  Port 8000     │   │  Port 5678       │
      │  (Internal)    │   │  (Internal)      │
      └────────┬───────┘   └───┬──────────────┘
               │               │
               ▼               ▼
      ┌─────────────────────────────┐
      │   Base44 + LinkedIn +       │
      │   WhatsApp Business         │
      └─────────────────────────────┘
```

---

## 🔧 Servizi Attivi

| Servizio | Porta Interna | Porta Esterna | Status |
|----------|---------------|---------------|--------|
| FastAPI Digital Agency Swarm | 8000 | 443 (api.waipro.it) | ✅ Attivo |
| N8N Automation | 5678 | 443 (n8n.waipro.it) | ✅ Attivo |
| Nginx Reverse Proxy | - | 80, 443 | ✅ Attivo |
| MCP Server | - | - | ✅ Attivo (PID 15647) |

---

## 🧪 Testing

### Test Endpoint API

```bash
# Health check
curl https://api.waipro.it/health

# API Documentation
curl -I https://api.waipro.it/docs

# Test N8N
curl -I https://n8n.waipro.it/
```

### Test SSL/TLS

```bash
# Verifica certificato
openssl s_client -connect api.waipro.it:443 -servername api.waipro.it < /dev/null

# Test con curl
curl -vI https://api.waipro.it/ 2>&1 | grep "SSL connection"
```

---

## 📊 Monitoraggio

### Logs Nginx

```bash
# Logs accesso API
tail -f /var/log/nginx/api_waipro_access.log

# Logs errori
tail -f /var/log/nginx/api_waipro_error.log

# Logs N8N
tail -f /var/log/nginx/n8n_waipro_access.log
```

### Status Servizi

```bash
# Nginx
systemctl status nginx

# Certificati SSL
certbot certificates

# Firewall
ufw status
```

---

## 🔄 Aggiornamenti

### Ultimo Aggiornamento
**Data**: 4 Novembre 2025
**Modifiche**:
- ✅ Aggiunto setup reverse proxy completo
- ✅ Configurazione Nginx per waipro.it, api.waipro.it, n8n.waipro.it
- ✅ Script di deployment automatico
- ✅ Documentazione SSL/TLS con Let's Encrypt
- ✅ Configurazione firewall e sicurezza

### Changelog
- **4 Nov 2025**: Setup reverse access, Nginx config, deployment script
- **26 Ott 2025**: Sistema di gestione API Keys centralizzato
- **18 Ott 2025**: Guida integrazione WAIPRO completa

---

## 👥 Team

- **Founder**: Cristian (Il Boss)
- **Capostruttura**: Lorenzo
- **DevOps AI**: Roy (Claudio)
- **Manager AI**: Adrian

---

## 📞 Support

Per problemi o domande:
1. Consulta la documentazione in questo repository
2. Verifica logs sui servizi
3. Contatta Lorenzo o Cristian

---

## 📜 Licenza

Proprietà privata di WAIPRO Agency. Tutti i diritti riservati.

---

**Repository**: https://github.com/Waipro-agency/infrastructure-backup
**Branch**: claude/waipro-reverse-access-011CUoVbZA7CC9eDu5Uspb7C
