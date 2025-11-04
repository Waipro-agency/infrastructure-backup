#!/bin/bash
# Deploy Reverse Proxy Script for waipro.it
# Version: 1.0
# Date: 2025-11-04
# Server: 72.61.158.55

set -e

echo "🚀 Deploying Reverse Proxy for waipro.it"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root"
    exit 1
fi

# Variables
ADMIN_EMAIL="dev@w-adv.it"
SERVER_IP="72.61.158.55"

# 1. Update system and install required packages
echo ""
echo "📦 Step 1/7: Installing Nginx and Certbot..."
apt update -qq
apt install -y nginx certbot python3-certbot-nginx ufw

# 2. Copy Nginx configuration
echo ""
echo "📝 Step 2/7: Configuring Nginx..."
if [ -f "/etc/nginx/sites-available/waipro.it" ]; then
    echo "⚠️  Backing up existing configuration..."
    mv /etc/nginx/sites-available/waipro.it /etc/nginx/sites-available/waipro.it.backup.$(date +%Y%m%d_%H%M%S)
fi

# Download or copy configuration
if [ -f "../nginx_config/waipro.it" ]; then
    cp ../nginx_config/waipro.it /etc/nginx/sites-available/waipro.it
else
    echo "❌ Nginx configuration file not found!"
    exit 1
fi

# 3. Create web root directory
echo ""
echo "📁 Step 3/7: Creating web root directory..."
mkdir -p /var/www/waipro.it
cat > /var/www/waipro.it/index.html << 'EOF'
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAIPRO Agency</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        h1 { margin: 0 0 20px 0; font-size: 3em; }
        p { font-size: 1.2em; }
        .links { margin-top: 30px; }
        .links a {
            display: inline-block;
            margin: 10px;
            padding: 15px 30px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            transition: transform 0.3s;
        }
        .links a:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 WAIPRO Agency</h1>
        <p>Infrastructure & AI Services</p>
        <div class="links">
            <a href="https://api.waipro.it/docs" target="_blank">API Docs</a>
            <a href="https://n8n.waipro.it" target="_blank">N8N Workflows</a>
        </div>
    </div>
</body>
</html>
EOF

# 4. Enable site
echo ""
echo "✅ Step 4/7: Enabling site..."
ln -sf /etc/nginx/sites-available/waipro.it /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 5. Test Nginx configuration
echo ""
echo "🧪 Step 5/7: Testing Nginx configuration..."
nginx -t

# 6. Restart Nginx
echo ""
echo "🔄 Step 6/7: Restarting Nginx..."
systemctl restart nginx
systemctl enable nginx

# 7. Configure SSL (only if domains are pointing to this server)
echo ""
echo "🔐 Step 7/7: Setting up SSL certificates..."
echo "⚠️  Make sure DNS records are pointing to $SERVER_IP before proceeding!"
read -p "Press Enter to continue with SSL setup or Ctrl+C to cancel..."

# Setup SSL for main domain
certbot --nginx -d waipro.it -d www.waipro.it \
    --non-interactive --agree-tos --email "$ADMIN_EMAIL" || {
    echo "⚠️  SSL setup for waipro.it failed. You may need to configure DNS first."
}

# Setup SSL for API subdomain
certbot --nginx -d api.waipro.it \
    --non-interactive --agree-tos --email "$ADMIN_EMAIL" || {
    echo "⚠️  SSL setup for api.waipro.it failed. You may need to configure DNS first."
}

# Setup SSL for N8N subdomain
certbot --nginx -d n8n.waipro.it \
    --non-interactive --agree-tos --email "$ADMIN_EMAIL" || {
    echo "⚠️  SSL setup for n8n.waipro.it failed. You may need to configure DNS first."
}

# 8. Configure Firewall
echo ""
echo "🔒 Step 8/7: Configuring firewall..."
ufw --force enable
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw deny 8000/tcp comment 'Block direct FastAPI access'
ufw deny 5678/tcp comment 'Block direct N8N access'

echo ""
echo "=========================================="
echo "✅ Reverse Proxy deployment completed!"
echo "=========================================="
echo ""
echo "🌐 Your services are now accessible at:"
echo "   - Main Site: https://waipro.it"
echo "   - API:       https://api.waipro.it"
echo "   - API Docs:  https://api.waipro.it/docs"
echo "   - N8N:       https://n8n.waipro.it"
echo ""
echo "📝 Next steps:"
echo "   1. Verify DNS records point to $SERVER_IP"
echo "   2. Test all endpoints"
echo "   3. Update N8N environment variables to use new domain"
echo "   4. Update FastAPI CORS settings for new domains"
echo ""
echo "📊 Check status:"
echo "   systemctl status nginx"
echo "   certbot certificates"
echo "   ufw status"
echo ""
