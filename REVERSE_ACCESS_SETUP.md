# Reverse Access Setup - waipro.it

## 📋 Panoramica

Configurazione completa per l'accesso reverse su **waipro.it** con Nginx reverse proxy, permettendo l'accesso sicuro ai servizi interni dell'infrastruttura WAIPRO.

**Data Setup**: 4 Novembre 2025
**Versione**: 1.0
**Server**: 72.61.158.55
**Domini**: waipro.it, api.waipro.it, n8n.waipro.it

---

## 🏗️ Architettura Reverse Proxy

```
Internet
    │
    ▼
┌─────────────────────────────────────────────────┐
│         waipro.it (Nginx Reverse Proxy)         │
│              Port 80/443 (SSL)                   │
└────────────┬────────────────────┬────────────────┘
             │                    │
             │                    │
    ┌────────▼─────────┐  ┌──────▼──────────┐
    │   FastAPI Server │  │   N8N Server    │
    │   Port 8000      │  │   Port 5678     │
    │   /api/*         │  │   /n8n/*        │
    └──────────────────┘  └─────────────────┘
```

---

## 🔧 Installazione e Configurazione

### Step 1: Installare Nginx sul Server

```bash
# SSH nel server remoto
ssh root@72.61.158.55

# Aggiorna sistema e installa Nginx
apt update
apt install -y nginx certbot python3-certbot-nginx

# Verifica installazione
nginx -v
```

### Step 2: Configurazione Nginx per Reverse Proxy

Crea il file di configurazione principale:

```bash
nano /etc/nginx/sites-available/waipro.it
```

**Contenuto del file `/etc/nginx/sites-available/waipro.it`:**

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name waipro.it www.waipro.it api.waipro.it n8n.waipro.it;

    # Certbot challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# Main domain - waipro.it
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name waipro.it www.waipro.it;

    # SSL Configuration (will be added by Certbot)
    ssl_certificate /etc/letsencrypt/live/waipro.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/waipro.it/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Logs
    access_log /var/log/nginx/waipro_access.log;
    error_log /var/log/nginx/waipro_error.log;

    # Root location - Static website or redirect
    location / {
        root /var/www/waipro.it;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }
}

# API subdomain - api.waipro.it
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.waipro.it;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.waipro.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.waipro.it/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logs
    access_log /var/log/nginx/api_waipro_access.log;
    error_log /var/log/nginx/api_waipro_error.log;

    # Reverse proxy to FastAPI (Digital Agency Swarm)
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # API Documentation
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# N8N subdomain - n8n.waipro.it
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name n8n.waipro.it;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/n8n.waipro.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.waipro.it/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logs
    access_log /var/log/nginx/n8n_waipro_access.log;
    error_log /var/log/nginx/n8n_waipro_error.log;

    # Reverse proxy to N8N
    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (required for N8N)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts (N8N può richiedere tempi più lunghi)
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # Buffer settings for large webhooks
        proxy_buffering off;
        proxy_request_buffering off;
        client_max_body_size 50M;
    }
}
```

### Step 3: Attivare la Configurazione

```bash
# Crea symbolic link per abilitare il sito
ln -s /etc/nginx/sites-available/waipro.it /etc/nginx/sites-enabled/

# Testa la configurazione Nginx
nginx -t

# Se il test è OK, riavvia Nginx
systemctl restart nginx

# Verifica status
systemctl status nginx
```

### Step 4: Configurare SSL con Let's Encrypt (Certbot)

```bash
# Ottieni certificati SSL per tutti i domini
certbot --nginx -d waipro.it -d www.waipro.it

certbot --nginx -d api.waipro.it

certbot --nginx -d n8n.waipro.it

# Verifica auto-renewal
certbot renew --dry-run

# I certificati si rinnoveranno automaticamente
```

---

## 🔐 Configurazione DNS

Assicurati che i record DNS puntino al server:

| Tipo | Nome | Valore | TTL |
|------|------|--------|-----|
| A | waipro.it | 72.61.158.55 | 3600 |
| A | www.waipro.it | 72.61.158.55 | 3600 |
| A | api.waipro.it | 72.61.158.55 | 3600 |
| A | n8n.waipro.it | 72.61.158.55 | 3600 |

**Verifica DNS:**
```bash
dig waipro.it +short
dig api.waipro.it +short
dig n8n.waipro.it +short
```

---

## 🌐 Aggiornamento Configurazioni N8N e FastAPI

### Aggiornare N8N per usare il nuovo dominio

Modifica `/home/user/infrastructure-backup/n8n_config/n8n_docker-compose.yml`:

```yaml
version: '3.8'

services:
  n8n:
    image: n8n.io/n8n
    restart: always
    ports:
      - '5678:5678'
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      - N8N_HOST=n8n.waipro.it
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - N8N_BASIC_AUTH_ACTIVE=false
      - N8N_EDITOR_BASE_URL=https://n8n.waipro.it/
      - N8N_DATA_FOLDER=/home/node/.n8n
      - N8N_WEBHOOK_URL=https://n8n.waipro.it/
      - N8N_WEBHOOK_TUNNEL_URL=https://n8n.waipro.it/
      - WEBHOOK_URL=https://n8n.waipro.it/

volumes:
  n8n_data:
```

### Aggiornare FastAPI per il nuovo dominio

Modifica il file di configurazione FastAPI sul server remoto (`/root/digital-agency-swarm/config/settings.py`):

```python
# settings.py
API_BASE_URL = "https://api.waipro.it"
ALLOWED_ORIGINS = [
    "https://waipro.it",
    "https://www.waipro.it",
    "https://api.waipro.it",
    "https://n8n.waipro.it",
]
```

---

## 🧪 Testing della Configurazione

### Test 1: Verifica Accesso API

```bash
# Test endpoint API
curl -I https://api.waipro.it/

# Test documentazione API
curl -I https://api.waipro.it/docs

# Test health check
curl https://api.waipro.it/health
```

### Test 2: Verifica Accesso N8N

```bash
# Test N8N homepage
curl -I https://n8n.waipro.it/

# Apri browser e vai a:
# https://n8n.waipro.it/
```

### Test 3: Verifica Webhook N8N

```bash
# Test webhook endpoint (esempio)
curl -X POST https://n8n.waipro.it/webhook/base44-incoming \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Test 4: Verifica SSL/TLS

```bash
# Verifica certificato SSL
openssl s_client -connect api.waipro.it:443 -servername api.waipro.it < /dev/null | openssl x509 -noout -dates

# Test SSL con curl
curl -vI https://api.waipro.it/ 2>&1 | grep "SSL connection"
```

---

## 🔒 Sicurezza Aggiuntiva

### Firewall (UFW)

```bash
# Abilita firewall
ufw --force enable

# Permetti SSH
ufw allow 22/tcp

# Permetti HTTP e HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Blocca porte interne (8000, 5678) dall'esterno
# (sono accessibili solo tramite reverse proxy)
ufw deny 8000/tcp
ufw deny 5678/tcp

# Verifica regole
ufw status
```

### Rate Limiting su Nginx

Aggiungi al file `/etc/nginx/nginx.conf` nella sezione `http`:

```nginx
http {
    # ... altre configurazioni ...

    # Rate limiting zone
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=n8n_limit:10m rate=5r/s;

    # Connection limiting
    limit_conn_zone $binary_remote_addr zone=addr:10m;
}
```

Poi nei blocchi `server` aggiungi:

```nginx
location / {
    limit_req zone=api_limit burst=20 nodelay;
    limit_conn addr 10;
    # ... resto della configurazione ...
}
```

### Autenticazione Base per N8N (Opzionale)

Se vuoi proteggere N8N con autenticazione base:

```bash
# Crea file password
apt install -y apache2-utils
htpasswd -c /etc/nginx/.htpasswd waipro_admin

# Nel blocco server n8n.waipro.it aggiungi:
location / {
    auth_basic "N8N Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    # ... resto della configurazione ...
}
```

---

## 📝 Monitoraggio e Logs

### Visualizzare logs Nginx

```bash
# Logs accesso API
tail -f /var/log/nginx/api_waipro_access.log

# Logs errori API
tail -f /var/log/nginx/api_waipro_error.log

# Logs N8N
tail -f /var/log/nginx/n8n_waipro_access.log
tail -f /var/log/nginx/n8n_waipro_error.log
```

### Monitoraggio servizi

```bash
# Status Nginx
systemctl status nginx

# Status FastAPI (se usa systemd)
systemctl status digital-agency-swarm

# Status N8N
ps aux | grep n8n
```

---

## 🚀 Script di Deploy Automatico

Crea script `/root/deploy_reverse_proxy.sh`:

```bash
#!/bin/bash
# Deploy Reverse Proxy Script for waipro.it

echo "🚀 Deploying Reverse Proxy for waipro.it"

# 1. Installa Nginx e Certbot
echo "📦 Installing Nginx and Certbot..."
apt update
apt install -y nginx certbot python3-certbot-nginx

# 2. Copia configurazione Nginx
echo "📝 Copying Nginx configuration..."
curl -o /etc/nginx/sites-available/waipro.it https://raw.githubusercontent.com/Waipro-agency/infrastructure-backup/main/nginx_config/waipro.it

# 3. Attiva sito
echo "✅ Enabling site..."
ln -sf /etc/nginx/sites-available/waipro.it /etc/nginx/sites-enabled/

# 4. Testa configurazione
echo "🧪 Testing Nginx configuration..."
nginx -t

# 5. Riavvia Nginx
echo "🔄 Restarting Nginx..."
systemctl restart nginx

# 6. Configura SSL
echo "🔐 Setting up SSL certificates..."
certbot --nginx -d waipro.it -d www.waipro.it --non-interactive --agree-tos -m dev@w-adv.it
certbot --nginx -d api.waipro.it --non-interactive --agree-tos -m dev@w-adv.it
certbot --nginx -d n8n.waipro.it --non-interactive --agree-tos -m dev@w-adv.it

# 7. Configura Firewall
echo "🔒 Configuring firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 8000/tcp
ufw deny 5678/tcp

echo "✅ Reverse Proxy deployment completed!"
echo "🌐 Accessing services:"
echo "  - API: https://api.waipro.it"
echo "  - N8N: https://n8n.waipro.it"
echo "  - Main: https://waipro.it"
```

Rendi eseguibile:

```bash
chmod +x /root/deploy_reverse_proxy.sh
```

---

## ✅ Checklist di Deployment

- [ ] DNS configurato per waipro.it, api.waipro.it, n8n.waipro.it
- [ ] Nginx installato sul server 72.61.158.55
- [ ] Configurazione Nginx creata e attiva
- [ ] Certificati SSL ottenuti con Certbot
- [ ] N8N configurato con nuovo dominio https://n8n.waipro.it
- [ ] FastAPI configurato con nuovo dominio https://api.waipro.it
- [ ] Firewall configurato (porte 80, 443 aperte; 8000, 5678 bloccate dall'esterno)
- [ ] Rate limiting configurato
- [ ] Logs configurati e funzionanti
- [ ] Test end-to-end completati

---

## 📞 Troubleshooting

### Problema: 502 Bad Gateway

**Causa**: FastAPI o N8N non sono in esecuzione.

**Soluzione**:
```bash
# Verifica servizi
ps aux | grep uvicorn
ps aux | grep n8n

# Riavvia servizi se necessario
cd /root/digital-agency-swarm && uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### Problema: SSL Certificate Error

**Causa**: Certbot non ha potuto validare il dominio.

**Soluzione**:
```bash
# Verifica DNS
dig api.waipro.it +short

# Riprova Certbot manualmente
certbot --nginx -d api.waipro.it --dry-run
```

### Problema: N8N Webhooks non funzionano

**Causa**: Configurazione N8N_WEBHOOK_URL errata.

**Soluzione**:
```bash
# Aggiorna env variable N8N
export N8N_WEBHOOK_URL=https://n8n.waipro.it/

# Riavvia N8N
pkill -f n8n
nohup /usr/bin/n8n &
```

---

## 📚 Riferimenti

- [Nginx Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [N8N Reverse Proxy Setup](https://docs.n8n.io/hosting/configuration/configuration-examples/reverse-proxy/)
- [WAIPRO_INTEGRATION_GUIDE.md](./WAIPRO_INTEGRATION_GUIDE.md)

---

**Creato da**: Claude (Infrastructure Setup Agent)
**Data**: 4 Novembre 2025
**Repository**: Waipro-agency/infrastructure-backup
**Branch**: claude/waipro-reverse-access-011CUoVbZA7CC9eDu5Uspb7C
