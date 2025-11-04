#!/usr/bin/env python3
"""Check and display OAuth 2.0 configuration for the project."""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def check_oauth_config():
    """Check OAuth configuration."""

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
    print("🔐 VERIFICA CONFIGURAZIONE OAUTH 2.0")
    print("=" * 80)
    print(f"Progetto: {project_id}\n")

    # Check OAuth consent screen
    print("📋 OAuth Consent Screen Configuration")
    print("-" * 80)

    # Try to get OAuth brand (consent screen)
    try:
        # List OAuth brands
        url = f'https://iap.googleapis.com/v1/projects/{project_id}/brands'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])

            if brands:
                print(f"✅ Trovati {len(brands)} OAuth consent screen(s):\n")
                for brand in brands:
                    print(f"   Brand Name: {brand.get('name')}")
                    print(f"   Support Email: {brand.get('supportEmail')}")
                    print(f"   Application Title: {brand.get('applicationTitle', 'N/A')}")
                    print()
            else:
                print("⚠️  Nessun OAuth consent screen configurato")
        else:
            print(f"⚠️  Status: {response.status_code}")
            if response.status_code == 403:
                print("   IAP API potrebbe non essere abilitata")
            else:
                print(f"   {response.text[:200]}")
    except Exception as e:
        print(f"⚠️  {e}")
    print()

    # Check for OAuth clients via OAuth2 API
    print("🔑 OAuth 2.0 Client IDs")
    print("-" * 80)

    # We need to use a different approach - check via API Console API
    try:
        # Try to list OAuth clients using the project metadata
        print("⚠️  Per visualizzare i client OAuth esistenti, accedi a:")
        print(f"   https://console.cloud.google.com/apis/credentials?project={project_id}")
        print()
        print("📌 REDIRECT URI CHE DEVE ESSERE CONFIGURATO:")
        print("   https://app.base44.com/api/apps/auth/callback")
        print()
        print("📌 POTREBBERO ESSERE NECESSARI ANCHE:")
        print("   https://nonamebar.it")
        print("   https://nonamebar.it/auth/callback")
        print("   http://localhost:3000/auth/callback (per sviluppo)")
        print()
    except Exception as e:
        print(f"⚠️  {e}")
    print()

    # Check what credentials exist
    print("🔍 Istruzioni per Risolvere l'Errore")
    print("=" * 80)
    print()
    print("Per risolvere l'errore 'redirect_uri_mismatch', segui questi passi:")
    print()
    print("1. Vai alla Google Cloud Console:")
    print(f"   https://console.cloud.google.com/apis/credentials?project={project_id}")
    print()
    print("2. Cerca 'OAuth 2.0 Client IDs' e clicca sul client esistente")
    print("   (o creane uno nuovo se non esiste)")
    print()
    print("3. Nella sezione 'Authorized redirect URIs', aggiungi:")
    print("   ✓ https://app.base44.com/api/apps/auth/callback")
    print("   ✓ https://nonamebar.it")
    print("   ✓ https://nonamebar.it/auth/callback (se necessario)")
    print()
    print("4. Clicca 'SAVE'")
    print()
    print("5. Attendi 5-10 minuti per la propagazione delle modifiche")
    print()
    print("6. Riprova l'accesso su nonamebar.it")
    print()
    print("=" * 80)
    print()

    # Try to get the project number
    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            project_number = data.get('projectNumber')
            print(f"📋 Project Number: {project_number}")
            print(f"📋 Project ID: {project_id}")
            print()
    except:
        pass

if __name__ == '__main__':
    check_oauth_config()
