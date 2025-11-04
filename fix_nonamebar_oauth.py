#!/usr/bin/env python3
"""Verifica e risolve problemi OAuth per nonamebar.it"""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def check_and_fix_oauth():
    """Verifica configurazione OAuth e suggerisce fix."""

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
    print("🔍 DIAGNOSI OAUTH PER NONAMEBAR.IT")
    print("=" * 80)
    print(f"Progetto: {project_id}\n")

    # Get project number
    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}'
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            project_data = response.json()
            project_number = project_data.get('projectNumber')
            print(f"📋 Project Number: {project_number}")
            print(f"📋 Project ID: {project_id}\n")
    except Exception as e:
        print(f"⚠️  Errore recupero project info: {e}\n")

    # Check OAuth consent screen
    print("1️⃣  OAUTH CONSENT SCREEN")
    print("-" * 80)
    try:
        url = f'https://iap.googleapis.com/v1/projects/{project_id}/brands'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])

            if brands:
                for brand in brands:
                    print(f"✅ Consent Screen Configurato:")
                    print(f"   Nome: {brand.get('applicationTitle', 'N/A')}")
                    print(f"   Support Email: {brand.get('supportEmail')}")
                    print()
            else:
                print("❌ Nessun OAuth consent screen trovato")
                print("   AZIONE RICHIESTA: Crea consent screen")
        else:
            print(f"⚠️  Impossibile verificare consent screen (status: {response.status_code})")
    except Exception as e:
        print(f"⚠️  {e}")
    print()

    # Try to list OAuth clients - questo richiede IAM API
    print("2️⃣  OAUTH CLIENT IDs")
    print("-" * 80)

    # Purtroppo non possiamo listare i client OAuth tramite API senza IAM API abilitata
    # Quindi dobbiamo dare istruzioni manuali

    print("⚠️  Per verificare i client OAuth esistenti:")
    print(f"   https://console.cloud.google.com/apis/credentials?project={project_id}")
    print()
    print("🔍 CERCA UN CLIENT CON QUESTI NOMI:")
    print("   - 'nonamebar'")
    print("   - 'nonamebar.it'")
    print("   - 'Base44 - nonamebar'")
    print("   - Qualsiasi client web application")
    print()

    # Check enabled APIs
    print("3️⃣  API NECESSARIE")
    print("-" * 80)
    try:
        url = f'https://serviceusage.googleapis.com/v1/projects/{project_id}/services?filter=state:ENABLED&pageSize=200'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])
            service_names = [s.get('config', {}).get('name', '') for s in services]

            required_apis = {
                'IAM API': 'iam.googleapis.com',
                'OAuth2 API': 'oauth2.googleapis.com',
                'Cloud Identity': 'cloudidentity.googleapis.com'
            }

            for api_name, api_id in required_apis.items():
                if api_id in service_names:
                    print(f"   ✅ {api_name}: Abilitata")
                else:
                    print(f"   ❌ {api_name}: NON abilitata")
                    print(f"      Abilita: https://console.cloud.google.com/apis/library/{api_id}?project={project_id}")
        else:
            print(f"⚠️  Impossibile verificare API (status: {response.status_code})")
    except Exception as e:
        print(f"⚠️  {e}")
    print()

    # Error diagnosis
    print("=" * 80)
    print("🔴 DIAGNOSI ERRORE: redirect_uri_mismatch")
    print("=" * 80)
    print()
    print("L'errore 'redirect_uri_mismatch' significa che il redirect URI:")
    print("   https://app.base44.com/api/apps/auth/callback")
    print()
    print("NON è presente nella lista 'Authorized redirect URIs' del tuo OAuth Client.")
    print()

    # Solution
    print("=" * 80)
    print("✅ SOLUZIONE STEP-BY-STEP")
    print("=" * 80)
    print()
    print("STEP 1: Vai alle credenziali")
    print(f"   🔗 https://console.cloud.google.com/apis/credentials?project={project_id}")
    print()
    print("STEP 2: Trova il tuo OAuth 2.0 Client ID")
    print("   - Cerca nella sezione 'OAuth 2.0 Client IDs'")
    print("   - Dovrebbe essere chiamato qualcosa come 'Web client' o contenere 'nonamebar'")
    print("   - Tipo: 'Web application'")
    print()
    print("STEP 3: Clicca sul nome del client per modificarlo")
    print()
    print("STEP 4: Controlla/Modifica questi campi:")
    print()
    print("   📍 Authorized JavaScript origins:")
    print("      - https://nonamebar.it")
    print("      - https://app.base44.com (opzionale)")
    print()
    print("   📍 Authorized redirect URIs: ⚠️ CRITICO!")
    print("      - https://app.base44.com/api/apps/auth/callback")
    print()
    print("   Se manca, clicca '+ ADD URI' e incolla esattamente:")
    print("   https://app.base44.com/api/apps/auth/callback")
    print()
    print("STEP 5: Clicca 'SAVE' in fondo alla pagina")
    print()
    print("STEP 6: Attendi 5-10 minuti per la propagazione")
    print()
    print("STEP 7: Riprova il login su nonamebar.it")
    print()
    print("=" * 80)
    print()

    # Additional checks
    print("📌 VERIFICHE AGGIUNTIVE")
    print("-" * 80)
    print()
    print("✓ Verifica che in Base44 Settings → Authentication:")
    print("  - Google authentication sia abilitato")
    print("  - 'Use a custom OAuth from Google Console' sia selezionato")
    print("  - Client ID e Client Secret siano inseriti correttamente")
    print()
    print("✓ Verifica che nonamebar.it sia collegato come custom domain in Base44")
    print()
    print("✓ Verifica che ci sia una Privacy Policy pubblica (non dietro login)")
    print()
    print("=" * 80)
    print()

    # Quick links
    print("🔗 LINK UTILI")
    print("-" * 80)
    print(f"Credentials:    https://console.cloud.google.com/apis/credentials?project={project_id}")
    print(f"Consent Screen: https://console.cloud.google.com/apis/credentials/consent?project={project_id}")
    print(f"Enabled APIs:   https://console.cloud.google.com/apis/dashboard?project={project_id}")
    print()
    print("=" * 80)
    print("✅ FATTO! Segui gli step sopra per risolvere l'errore.")
    print("=" * 80)

if __name__ == '__main__':
    check_and_fix_oauth()
