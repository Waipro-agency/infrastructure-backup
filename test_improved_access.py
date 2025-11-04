#!/usr/bin/env python3
"""Test improved access after role cleanup."""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def test_improved_access():
    """Test if we now have better access after role cleanup."""

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
    print("🧪 TEST ACCESSO MIGLIORATO DOPO PULIZIA RUOLI")
    print("=" * 80)
    print(f"Progetto: {project_id}")
    print(f"Service Account: {creds_data['client_email']}\n")

    # Test 1: IAM Policy (prima dava 403)
    print("TEST 1: IAM Policy")
    print("-" * 80)
    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy'
        response = requests.post(url, headers=headers, json={}, timeout=30)

        if response.status_code == 200:
            print("✅ SUCCESS! Ora posso vedere IAM Policy!")
            policy = response.json()

            # Find service account roles
            sa_email = creds_data['client_email']
            print(f"\nRuoli per {sa_email}:")

            for binding in policy.get('bindings', []):
                if f'serviceAccount:{sa_email}' in binding.get('members', []):
                    role = binding.get('role')
                    print(f"   ✓ {role}")
            print()
        elif response.status_code == 403:
            print("❌ Ancora 403 - Aspetta qualche minuto per propagazione")
            print()
        else:
            print(f"⚠️  Status: {response.status_code}")
            print(f"   {response.text[:200]}\n")
    except Exception as e:
        print(f"❌ Errore: {e}\n")

    # Test 2: Project Details (prima dava 403)
    print("TEST 2: Project Details")
    print("-" * 80)
    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            print("✅ SUCCESS! Ora posso vedere Project Details!")
            data = response.json()
            print(f"   Project Name: {data.get('name')}")
            print(f"   Project Number: {data.get('projectNumber')}")
            print(f"   Project ID: {data.get('projectId')}")
            print(f"   State: {data.get('lifecycleState')}")
            print()
        elif response.status_code == 403:
            print("❌ Ancora 403 - Aspetta qualche minuto per propagazione")
            print()
        else:
            print(f"⚠️  Status: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Errore: {e}\n")

    # Test 3: List all projects (to see if we can see other projects)
    print("TEST 3: Lista Progetti (per vedere altri progetti)")
    print("-" * 80)
    try:
        url = 'https://cloudresourcemanager.googleapis.com/v1/projects'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            print("✅ SUCCESS! Posso listare i progetti!")
            data = response.json()
            projects = data.get('projects', [])

            print(f"\nTrovati {len(projects)} progetto/i:")
            for proj in projects[:10]:  # Show first 10
                print(f"   • {proj.get('name')} ({proj.get('projectId')})")

            if len(projects) > 10:
                print(f"   ... e altri {len(projects) - 10} progetti")
            print()
        elif response.status_code == 403:
            print("❌ 403 - Non posso listare progetti")
            print("   (Normale se service account è solo su waipro-agency)")
            print()
        else:
            print(f"⚠️  Status: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Errore: {e}\n")

    # Test 4: OAuth Consent Screen (dovrebbe sempre funzionare)
    print("TEST 4: OAuth Consent Screen")
    print("-" * 80)
    try:
        url = f'https://iap.googleapis.com/v1/projects/{project_id}/brands'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            print("✅ OAuth Brand accessibile")
            data = response.json()
            brands = data.get('brands', [])
            if brands:
                brand = brands[0]
                print(f"   App: {brand.get('applicationTitle')}")
                print(f"   Email: {brand.get('supportEmail')}")
            print()
        else:
            print(f"⚠️  Status: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Errore: {e}\n")

    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()
    print("✅ Se vedi 'SUCCESS' sopra: Ottimo! Ora ho più accesso")
    print("❌ Se vedi ancora 403: Aspetta 5-10 minuti e riprova questo script")
    print()
    print("⚠️  LIMITAZIONE CONFERMATA:")
    print("   Client OAuth NON sono accessibili via API")
    print("   Google blocca per sicurezza")
    print()
    print("=" * 80)
    print("🎯 PROSSIMI PASSI PER RISOLVERE OAUTH")
    print("=" * 80)
    print()
    print("Dato che OAuth clients NON sono accessibili via API,")
    print("abbiamo 2 opzioni:")
    print()
    print("OPZIONE A: TU fai screenshot")
    print("   1. Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency")
    print("   2. Screenshot del client OAuth per nonamebar")
    print("   3. Mostra sezione 'Authorized redirect URIs'")
    print("   4. Salvalo come file e caricalo su:")
    print("      - Imgur: https://imgur.com/upload")
    print("      - Google Drive: https://drive.google.com")
    print("      - Dropbox: https://www.dropbox.com/upload")
    print("   5. Mandami il link dell'immagine")
    print()
    print("OPZIONE B: TU mi scrivi la configurazione")
    print("   1. Vai a: https://console.cloud.google.com/apis/credentials?project=waipro-agency")
    print("   2. Clicca sul client OAuth per nonamebar")
    print("   3. Copia-incolla qui TUTTI gli 'Authorized redirect URIs'")
    print("   4. Io ti dico cosa modificare")
    print()
    print("OPZIONE C: COMET fa il fix")
    print("   Comet va alla console e aggiunge:")
    print("   https://app.base44.com/api/apps/auth/callback")
    print()
    print("Scegli l'opzione e procediamo!")
    print()

if __name__ == '__main__':
    test_improved_access()
