#!/usr/bin/env python3
"""Inspect detailed OAuth configuration to find what's wrong."""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def inspect_oauth():
    """Detailed inspection of OAuth configuration."""

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
    print("🔍 ISPEZIONE DETTAGLIATA CONFIGURAZIONE OAUTH")
    print("=" * 80)
    print(f"Progetto: {project_id}\n")

    # Get OAuth brand details
    print("1️⃣  OAUTH CONSENT SCREEN / BRAND")
    print("-" * 80)
    try:
        url = f'https://iap.googleapis.com/v1/projects/{project_id}/brands'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])

            if brands:
                brand = brands[0]
                print(f"✅ Brand configurato:")
                print(f"   Name: {brand.get('name')}")
                print(f"   Application Title: {brand.get('applicationTitle')}")
                print(f"   Support Email: {brand.get('supportEmail')}")
                print(f"   Org Internal Only: {brand.get('orgInternalOnly', False)}")
                print()
            else:
                print("❌ Nessun brand trovato - DEVI crearlo!\n")
        else:
            print(f"⚠️  Status: {response.status_code}\n")
    except Exception as e:
        print(f"❌ {e}\n")

    # Try to list IAP clients
    print("2️⃣  TENTATIVO DI LISTARE CLIENT OAUTH")
    print("-" * 80)

    # Try multiple endpoints
    endpoints_to_try = [
        ('IAP Clients', f'https://iap.googleapis.com/v1/projects/{project_id}/brands/-/identityAwareProxyClients'),
        ('Service Accounts', f'https://iam.googleapis.com/v1/projects/{project_id}/serviceAccounts'),
    ]

    for endpoint_name, url in endpoints_to_try:
        print(f"Tentativo {endpoint_name}...")
        try:
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Risposta ricevuta:")
                print(json.dumps(data, indent=2)[:1000])
                print()
            elif response.status_code == 403:
                print(f"❌ 403 Forbidden - Permessi insufficienti")
                print()
            elif response.status_code == 404:
                print(f"⚠️  404 Not Found - Nessun client trovato o endpoint non valido")
                print()
            else:
                print(f"⚠️  Status: {response.status_code}")
                print(f"   {response.text[:300]}")
                print()
        except Exception as e:
            print(f"❌ {e}\n")

    # Check what APIs are enabled
    print("3️⃣  API ABILITATE RILEVANTI")
    print("-" * 80)
    try:
        url = f'https://serviceusage.googleapis.com/v1/projects/{project_id}/services?filter=state:ENABLED&pageSize=200'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])
            service_names = [s.get('config', {}).get('name', '') for s in services]

            relevant = {
                'IAM': 'iam.googleapis.com',
                'IAP': 'iap.googleapis.com',
                'Cloud Identity': 'cloudidentity.googleapis.com',
                'OAuth2': 'oauth2.googleapis.com',
                'Service Management': 'servicemanagement.googleapis.com'
            }

            for name, api_id in relevant.items():
                status = "✅" if api_id in service_names else "❌"
                print(f"   {status} {name}")
            print()
    except Exception as e:
        print(f"❌ {e}\n")

    # Print what we know about the error
    print("=" * 80)
    print("🔴 ANALISI ERRORE: redirect_uri_mismatch")
    print("=" * 80)
    print()
    print("L'errore dice:")
    print('  "redirect_uri=https://app.base44.com/api/apps/auth/callback"')
    print()
    print("Questo significa che quando Google OAuth prova a reindirizzare l'utente")
    print("a questo URL, NON lo trova nella lista degli Authorized redirect URIs")
    print("del tuo OAuth Client.")
    print()
    print("=" * 80)
    print("✅ COSA DEVI VERIFICARE MANUALMENTE")
    print("=" * 80)
    print()
    print("Dato che non posso vedere i tuoi client OAuth via API,")
    print("DEVI controllare manualmente:")
    print()
    print("1. Vai a:")
    print(f"   https://console.cloud.google.com/apis/credentials?project={project_id}")
    print()
    print("2. Guarda la sezione 'OAuth 2.0 Client IDs'")
    print()
    print("3. Per ogni client di tipo 'Web application', controlla:")
    print()
    print("   ✓ C'è un client chiamato 'nonamebar' o simile?")
    print("   ✓ Clicca sul nome per aprirlo")
    print()
    print("4. Nella pagina del client, verifica:")
    print()
    print("   📍 Authorized JavaScript origins:")
    print("      DEVE contenere:")
    print("      • https://nonamebar.it")
    print("      • https://app.base44.com (opzionale)")
    print()
    print("   📍 Authorized redirect URIs: ⚠️⚠️⚠️ CRITICO!")
    print("      DEVE contenere ESATTAMENTE:")
    print("      • https://app.base44.com/api/apps/auth/callback")
    print()
    print("      ❌ NON:")
    print("      • https://nonamebar.it/callback")
    print("      • https://nonamebar.it/auth/callback")
    print("      • https://app.base44.com/callback")
    print("      • Qualsiasi altro URI")
    print()
    print("      ✅ SOLO:")
    print("      • https://app.base44.com/api/apps/auth/callback")
    print()
    print("5. Se NON c'è questo URI, clicca '+ ADD URI' e aggiungilo")
    print()
    print("6. Clicca SAVE")
    print()
    print("7. Aspetta 5-10 minuti")
    print()
    print("8. Riprova il login")
    print()
    print("=" * 80)
    print("📸 MANDAMI UNO SCREENSHOT")
    print("=" * 80)
    print()
    print("Se vuoi che verifichi cosa c'è di sbagliato, mandami:")
    print()
    print("1. Screenshot della pagina OAuth 2.0 Client IDs")
    print("   (mostrando tutti i client)")
    print()
    print("2. Screenshot della pagina di dettaglio del client OAuth")
    print("   (mostrando gli Authorized redirect URIs configurati)")
    print()
    print("3. Screenshot di Base44 Settings → Authentication")
    print("   (mostrando la configurazione Google OAuth)")
    print()
    print("Così vedo ESATTAMENTE cosa è configurato e cosa manca!")
    print()
    print("=" * 80)
    print()

if __name__ == '__main__':
    inspect_oauth()
