#!/usr/bin/env python3
"""Enable required APIs and attempt to fix OAuth configuration remotely."""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests
import time

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def enable_api(project_id, api_name, headers):
    """Enable a specific API."""
    url = f'https://serviceusage.googleapis.com/v1/projects/{project_id}/services/{api_name}:enable'
    response = requests.post(url, headers=headers, timeout=30)
    return response

def main():
    """Main function to enable APIs and configure OAuth."""

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
    print("🚀 TENTATIVO DI FIX AUTOMATICO OAUTH PER NONAMEBAR.IT")
    print("=" * 80)
    print(f"Progetto: {project_id}\n")

    # Step 1: Enable required APIs
    print("STEP 1: Abilitazione API necessarie...")
    print("-" * 80)

    apis_to_enable = {
        'IAM API': 'iam.googleapis.com',
        'Cloud Identity': 'cloudidentity.googleapis.com',
    }

    for api_name, api_id in apis_to_enable.items():
        print(f"Abilitazione {api_name}...", end=" ")
        try:
            response = enable_api(project_id, api_id, headers)
            if response.status_code in [200, 201, 409]:
                print("✅")
            else:
                print(f"⚠️  (status: {response.status_code})")
                print(f"   {response.text[:200]}")
        except Exception as e:
            print(f"❌ {e}")

    print()
    print("⏳ Attendo 10 secondi per propagazione API...")
    time.sleep(10)
    print()

    # Step 2: Try to list OAuth clients
    print("STEP 2: Ricerca client OAuth esistenti...")
    print("-" * 80)

    # Unfortunately, Google doesn't provide a direct API to list OAuth clients
    # We need to use the IAM service account credentials API

    print("⚠️  LIMITAZIONE API GOOGLE:")
    print("Google non fornisce un'API pubblica per modificare client OAuth 2.0")
    print("via codice per motivi di sicurezza.")
    print()
    print("I client OAuth possono essere modificati solo tramite:")
    print("  1. Google Cloud Console (interfaccia web)")
    print("  2. gcloud CLI (richiede autenticazione utente interattiva)")
    print()

    # Step 3: Verify project access
    print("STEP 3: Verifica accesso al progetto...")
    print("-" * 80)

    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Progetto: {data.get('name')}")
            print(f"   Project Number: {data.get('projectNumber')}")
            print(f"   State: {data.get('lifecycleState')}")
        else:
            print(f"⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"❌ {e}")

    print()

    # Step 4: Check if we have Owner/Editor role
    print("STEP 4: Verifica permessi service account...")
    print("-" * 80)

    try:
        # Try to get IAM policy
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy'
        response = requests.post(url, headers=headers, json={}, timeout=30)

        if response.status_code == 200:
            policy = response.json()
            sa_email = creds_data['client_email']

            roles = []
            for binding in policy.get('bindings', []):
                if f'serviceAccount:{sa_email}' in binding.get('members', []):
                    roles.append(binding.get('role'))

            if roles:
                print(f"✅ Service account ha questi ruoli:")
                for role in roles:
                    print(f"   • {role}")

                # Check if we have enough permissions
                has_owner = any('roles/owner' in r for r in roles)
                has_editor = any('roles/editor' in r for r in roles)

                if has_owner or has_editor:
                    print()
                    print("✅ Permessi sufficienti per modifiche progetto")
                else:
                    print()
                    print("⚠️  Potrebbe servire ruolo Owner o Editor")
            else:
                print("⚠️  Nessun ruolo trovato per questo service account")
        else:
            print(f"⚠️  Impossibile verificare IAM policy (status: {response.status_code})")
            if response.status_code == 403:
                print("   Il service account potrebbe non avere permessi IAM")
    except Exception as e:
        print(f"⚠️  {e}")

    print()

    # Conclusion
    print("=" * 80)
    print("📋 CONCLUSIONE")
    print("=" * 80)
    print()
    print("❌ NON POSSO modificare direttamente il client OAuth via API")
    print("   (limitazione di sicurezza di Google)")
    print()
    print("✅ POSSO fornirti le istruzioni esatte o accedere alla console")
    print()
    print("OPZIONI:")
    print()
    print("1️⃣  MANUALE (5 minuti):")
    print("   Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency")
    print("   Modifica il client OAuth")
    print("   Aggiungi redirect URI: https://app.base44.com/api/apps/auth/callback")
    print()
    print("2️⃣  SCREEN SHARING:")
    print("   Posso guidarti passo-passo in tempo reale")
    print()
    print("3️⃣  CREO UN NUOVO CLIENT OAuth:")
    print("   Posso creare un NUOVO client OAuth con configurazione corretta")
    print("   (richiede poi di aggiornare Client ID/Secret in Base44)")
    print()
    print("Cosa preferisci?")
    print()

if __name__ == '__main__':
    main()
