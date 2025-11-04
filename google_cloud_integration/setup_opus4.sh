#!/bin/bash

###############################################################################
# SETUP CLAUDE OPUS 4 - WAIPRO AGENCY
# Script di configurazione automatica
###############################################################################

echo "🚀 WAIPRO Agency - Setup Claude Opus 4"
echo "=========================================="
echo ""

# Colori
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funzione per installare dipendenze
install_dependencies() {
    echo -e "${BLUE}📦 Installazione dipendenze Python...${NC}"

    # Controlla se pip è installato
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}❌ pip3 non trovato! Installalo prima.${NC}"
        exit 1
    fi

    # Installa anthropic SDK
    echo "Installazione anthropic SDK..."
    pip3 install anthropic requests httpx

    echo -e "${GREEN}✅ Dipendenze installate!${NC}"
    echo ""
}

# Funzione per configurare API Key
configure_api_key() {
    echo -e "${BLUE}🔑 Configurazione API Key${NC}"
    echo ""
    echo "Hai il bonus su:"
    echo "  1) Anthropic Console (console.anthropic.com)"
    echo "  2) OpenRouter (openrouter.ai)"
    echo ""
    read -p "Scegli opzione (1 o 2): " choice

    case $choice in
        1)
            echo ""
            echo "🔸 Vai su: https://console.anthropic.com/settings/keys"
            echo "🔸 Copia la tua API Key (inizia con sk-ant-...)"
            echo ""
            read -p "Incolla la tua Anthropic API Key: " api_key

            # Salva nel .bashrc per persistenza
            echo "export ANTHROPIC_API_KEY='$api_key'" >> ~/.bashrc
            export ANTHROPIC_API_KEY="$api_key"

            echo -e "${GREEN}✅ API Key Anthropic configurata!${NC}"
            PROVIDER="anthropic"
            ;;
        2)
            echo ""
            echo "🔸 Vai su: https://openrouter.ai/keys"
            echo "🔸 Usa una delle chiavi esistenti o creane una nuova"
            echo ""
            echo "Chiavi WAIPRO esistenti:"
            echo "  - Ward: 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"
            echo ""
            read -p "Usa 'Ward' o incolla una nuova chiave: " api_key

            if [ "$api_key" == "Ward" ]; then
                api_key="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"
            fi

            echo "export OPENROUTER_API_KEY='$api_key'" >> ~/.bashrc
            export OPENROUTER_API_KEY="$api_key"

            echo -e "${GREEN}✅ API Key OpenRouter configurata!${NC}"
            PROVIDER="openrouter"
            ;;
        *)
            echo -e "${RED}❌ Scelta non valida${NC}"
            exit 1
            ;;
    esac

    echo ""
}

# Funzione per testare Opus 4
test_opus4() {
    echo -e "${BLUE}🧪 Test Claude Opus 4...${NC}"
    echo ""

    if [ "$PROVIDER" == "anthropic" ]; then
        # Test con Anthropic diretta
        python3 << 'EOF'
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=200,
        messages=[
            {"role": "user", "content": "Ciao! Presentati brevemente come Claude Opus 4 e dimmi che sei pronto per WAIPRO Agency!"}
        ]
    )

    print("✅ TEST RIUSCITO!")
    print("\n📝 Risposta Opus 4:")
    print("-" * 60)
    print(message.content[0].text)
    print("-" * 60)

except Exception as e:
    print(f"❌ ERRORE: {e}")
    exit(1)
EOF

    else
        # Test con OpenRouter
        python3 << 'EOF'
import requests
import os

api_key = os.getenv("OPENROUTER_API_KEY")

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "anthropic/claude-opus-4-20250514",
        "messages": [
            {"role": "user", "content": "Ciao! Presentati brevemente come Claude Opus 4 e dimmi che sei pronto per WAIPRO Agency!"}
        ],
        "max_tokens": 200
    }
)

if response.status_code == 200:
    result = response.json()
    print("✅ TEST RIUSCITO!")
    print("\n📝 Risposta Opus 4:")
    print("-" * 60)
    print(result["choices"][0]["message"]["content"])
    print("-" * 60)
else:
    print(f"❌ ERRORE {response.status_code}: {response.text}")
    exit(1)
EOF
    fi

    echo ""
    echo -e "${GREEN}🎉 Claude Opus 4 è ATTIVO e funzionante!${NC}"
}

# Funzione per creare file di configurazione
create_config_file() {
    echo -e "${BLUE}📄 Creazione file di configurazione...${NC}"

    cat > ~/waipro_opus4_config.json << EOF
{
    "provider": "$PROVIDER",
    "model": "claude-opus-4-20250514",
    "bonus_credits": "250 EUR",
    "api_key_location": "~/.bashrc (variabile d'ambiente)",
    "setup_date": "$(date +%Y-%m-%d)",
    "status": "✅ ATTIVO",
    "usage_notes": "Usa opus4_config.py o anthropic_direct_config.py per interagire con il modello"
}
EOF

    echo -e "${GREEN}✅ Config salvata in: ~/waipro_opus4_config.json${NC}"
    echo ""
}

# Funzione per mostrare riepilogo
show_summary() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ SETUP COMPLETATO CON SUCCESSO!${NC}"
    echo "=========================================="
    echo ""
    echo "📋 Riepilogo:"
    echo "  • Provider: $PROVIDER"
    echo "  • Modello: Claude Opus 4"
    echo "  • Bonus: 250 EUR"
    echo "  • Status: ✅ ATTIVO"
    echo ""
    echo "🚀 Prossimi passi:"
    echo "  1. Usa opus4_config.py per OpenRouter"
    echo "  2. Usa anthropic_direct_config.py per Anthropic"
    echo "  3. Integra con gli agenti WAIPRO (Sofia, Roy, etc.)"
    echo ""
    echo "📚 Esempi:"
    if [ "$PROVIDER" == "anthropic" ]; then
        echo "  python3 google_cloud_integration/anthropic_direct_config.py"
    else
        echo "  python3 google_cloud_integration/opus4_config.py"
    fi
    echo ""
    echo "💰 Monitora l'utilizzo:"
    if [ "$PROVIDER" == "anthropic" ]; then
        echo "  https://console.anthropic.com/settings/usage"
    else
        echo "  https://openrouter.ai/activity"
    fi
    echo ""
    echo "🎉 Claude Opus 4 è pronto per WAIPRO Agency!"
    echo ""
}

# ===== ESECUZIONE PRINCIPALE =====

main() {
    install_dependencies
    configure_api_key
    test_opus4
    create_config_file
    show_summary
}

# Avvia lo script
main
