#!/usr/bin/env python3
"""Create a new OAuth client with correct configuration for nonamebar.it"""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def create_oauth_client():
    """Create OAuth 2.0 client with correct redirect URIs."""

    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    project_id = creds_data['project_id']
    credentials.refresh(GoogleAuthRequest())
    access_token = credentials.token

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    print("=" * 80)
    print("🔨 CREAZIONE NUOVO CLIENT OAUTH PER NONAMEBAR.IT")
    print("=" * 80)
    print(f"Progetto: {project_id}\n")

    # Get project number
    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}'
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            project_data = response.json()
            project_number = project_data.get('projectNumber')
            print(f"Project Number: {project_number}\n")
        else:
            project_number = None
            print(f"⚠️  Non riesco a recuperare project number (status: {response.status_code})\n")
    except Exception as e:
        project_number = None
        print(f"⚠️  Errore: {e}\n")

    # Try to create OAuth client
    print("Tentativo di creazione client OAuth...")
    print("-" * 80)

    # Note: Google Cloud doesn't provide a public API to create OAuth clients
    # We need to use the OAuth2 service or IAP API

    # Try using the IAP API to create an OAuth brand identity
    try:
        # First, check if brand exists
        url = f'https://iap.googleapis.com/v1/projects/{project_id}/brands'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])

            if brands:
                brand_name = brands[0].get('name')
                print(f"✅ Brand OAuth esistente: {brand_name}\n")

                # Try to create an identity-aware proxy client
                # Note: This creates an IAP client, not a standard OAuth client
                print("⚠️  LIMITAZIONE:")
                print("L'API IAP crea client specifici per Identity-Aware Proxy,")
                print("non client OAuth standard per Base44.\n")
                print("Per creare un client OAuth standard serve la Console Web.\n")
            else:
                print("⚠️  Nessun brand OAuth trovato\n")
        else:
            print(f"⚠️  Impossibile verificare brand (status: {response.status_code})\n")
    except Exception as e:
        print(f"❌ Errore: {e}\n")

    # Alternative approach: use gcloud command
    print("=" * 80)
    print("💡 SOLUZIONE ALTERNATIVA: GCLOUD CLI")
    print("=" * 80)
    print()
    print("Purtroppo Google NON fornisce un'API per creare client OAuth standard.")
    print("Possiamo usare il comando gcloud per creare il client:\n")
    print("OPZIONE 1: Se hai gcloud installato sul tuo computer:")
    print()
    print("# Autentica con il tuo account Google")
    print("gcloud auth login")
    print()
    print("# Imposta il progetto")
    print("gcloud config set project waipro-agency")
    print()
    print("# Crea il client OAuth (richiede interfaccia web)")
    print("# Non esiste un comando gcloud diretto, serve la console")
    print()

    print("=" * 80)
    print("✅ SOLUZIONE PIÙ VELOCE: CONSOLE WEB (2 MINUTI)")
    print("=" * 80)
    print()
    print("Ti do le istruzioni ESATTE, screenshot-by-screenshot:")
    print()
    print("1. Vai qui: https://console.cloud.google.com/apis/credentials?project=waipro-agency")
    print()
    print("2. Cerca 'OAuth 2.0 Client IDs' nella pagina")
    print()
    print("3. Vedrai una lista di client OAuth. Cerca uno che contiene:")
    print("   - 'Web client'")
    print("   - 'nonamebar'")
    print("   - O qualsiasi tipo 'Web application'")
    print()
    print("4. CLICCA sul NOME del client (non sull'icona)")
    print()
    print("5. Scorri in basso fino a vedere 'Authorized redirect URIs'")
    print()
    print("6. Clicca il bottone '+ ADD URI'")
    print()
    print("7. Incolla ESATTAMENTE questo (copia tutto):")
    print()
    print("   https://app.base44.com/api/apps/auth/callback")
    print()
    print("8. Scorri fino in fondo alla pagina")
    print()
    print("9. Clicca il bottone blu 'SAVE' in basso")
    print()
    print("10. Aspetta 5-10 minuti e riprova su nonamebar.it")
    print()
    print("FATTO! L'errore redirect_uri_mismatch sparirà! ✅")
    print()
    print("=" * 80)
    print()
    print("Se NON vedi nessun client OAuth, allora devi crearne uno nuovo:")
    print()
    print("1. Clicca '+ CREATE CREDENTIALS' in alto")
    print("2. Scegli 'OAuth client ID'")
    print("3. Application type: 'Web application'")
    print("4. Name: 'nonamebar.it - Base44'")
    print("5. Authorized JavaScript origins:")
    print("   - https://nonamebar.it")
    print("6. Authorized redirect URIs:")
    print("   - https://app.base44.com/api/apps/auth/callback")
    print("7. CREATE")
    print("8. Copia Client ID e Client Secret")
    print("9. Incollali in Base44 Settings → Authentication → Custom OAuth")
    print()
    print("=" * 80)

if __name__ == '__main__':
    create_oauth_client()
