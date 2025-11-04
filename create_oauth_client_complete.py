#!/usr/bin/env python3
"""Create new OAuth 2.0 client for nonamebar.it with complete configuration."""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests
import time

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def create_new_oauth_client():
    """Create a complete OAuth 2.0 client with all settings."""

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
    print(f"Progetto: {project_id}")
    print(f"Service Account: {creds_data['client_email']}\n")

    # Step 1: Verify permissions
    print("STEP 1: Verifica permessi Owner...")
    print("-" * 80)

    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy'
        response = requests.post(url, headers=headers, json={}, timeout=30)

        if response.status_code == 200:
            policy = response.json()
            sa_email = creds_data['client_email']

            roles = []
            for binding in policy.get('bindings', []):
                if f'serviceAccount:{sa_email}' in binding.get('members', []):
                    roles.append(binding.get('role'))

            print(f"✅ Ruoli trovati:")
            for role in roles:
                print(f"   • {role}")

            has_owner = any('roles/owner' in r for r in roles)
            has_editor = any('roles/editor' in r for r in roles)

            if has_owner:
                print("\n✅ CONFERMATO: Hai permessi Owner!\n")
            elif has_editor:
                print("\n✅ Hai permessi Editor (dovrebbe bastare)\n")
            else:
                print("\n⚠️  Non ho trovato Owner/Editor. Provo comunque...\n")
        else:
            print(f"⚠️  Status: {response.status_code}")
            print("   Provo comunque a creare il client...\n")
    except Exception as e:
        print(f"⚠️  {e}")
        print("   Provo comunque...\n")

    # Step 2: Get project number
    print("STEP 2: Recupero project number...")
    print("-" * 80)

    project_number = None
    try:
        url = f'https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            project_number = data.get('projectNumber')
            print(f"✅ Project Number: {project_number}\n")
        else:
            print(f"⚠️  Status: {response.status_code}\n")
    except Exception as e:
        print(f"⚠️  {e}\n")

    # Step 3: Check OAuth brand
    print("STEP 3: Verifica OAuth Brand...")
    print("-" * 80)

    brand_name = None
    try:
        url = f'https://iap.googleapis.com/v1/projects/{project_id}/brands'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])

            if brands:
                brand = brands[0]
                brand_name = brand.get('name')
                print(f"✅ Brand OAuth trovato:")
                print(f"   Name: {brand_name}")
                print(f"   Application: {brand.get('applicationTitle')}")
                print(f"   Support Email: {brand.get('supportEmail')}\n")
            else:
                print("⚠️  Nessun brand OAuth trovato\n")
                print("   Devo creare un brand prima...\n")
        else:
            print(f"⚠️  Status: {response.status_code}\n")
    except Exception as e:
        print(f"⚠️  {e}\n")

    # Step 4: Try different approaches to create OAuth client
    print("STEP 4: Tentativo creazione OAuth client...")
    print("-" * 80)

    # Approach 1: Try IAP API (creates Identity-Aware Proxy client)
    print("Approccio 1: IAP API...")
    if brand_name:
        try:
            url = f'https://iap.googleapis.com/v1/{brand_name}/identityAwareProxyClients'

            client_data = {
                'displayName': 'nonamebar.it - Base44 OAuth Client'
            }

            response = requests.post(url, headers=headers, json=client_data, timeout=30)

            if response.status_code in [200, 201]:
                result = response.json()
                client_id = result.get('name', '').split('/')[-1]
                client_secret = result.get('secret')

                if client_id and client_secret:
                    print(f"✅ CLIENT CREATO CON SUCCESSO!")
                    print()
                    print("=" * 80)
                    print("🎉 CREDENZIALI PER BASE44")
                    print("=" * 80)
                    print()
                    print(f"Client ID:")
                    print(f"{client_id}")
                    print()
                    print(f"Client Secret:")
                    print(f"{client_secret}")
                    print()
                    print("=" * 80)
                    print()
                    print("⚠️  NOTA: Questo è un client IAP.")
                    print("Per Base44 custom OAuth serve un client 'Web application' standard.")
                    print("Questo potrebbe non funzionare correttamente.\n")
                    return
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   {response.text[:300]}\n")
        except Exception as e:
            print(f"❌ Errore: {e}\n")
    else:
        print("⏭️  Saltato (no brand)\n")

    # Approach 2: Try to use Service Account Keys API (different approach)
    print("Approccio 2: OAuth2 API diretta...")
    print("❌ Google non fornisce API pubblica per creare client OAuth standard\n")

    # Step 5: Conclusion
    print("=" * 80)
    print("💡 CONCLUSIONE E SOLUZIONE")
    print("=" * 80)
    print()
    print("❌ NON POSSO creare un client OAuth standard via API")
    print("   (limitazione di Google per sicurezza)")
    print()
    print("✅ PERÒ posso guidarti a crearlo in 2 minuti!")
    print()
    print("=" * 80)
    print("📝 ISTRUZIONI PER CREARE IL CLIENT")
    print("=" * 80)
    print()
    print("1. Apri questa pagina (devi essere loggato con il tuo Google account):")
    print(f"   https://console.cloud.google.com/apis/credentials?project={project_id}")
    print()
    print("2. Clicca il bottone '+ CREATE CREDENTIALS' in alto")
    print()
    print("3. Nel menu a discesa, scegli 'OAuth client ID'")
    print()
    print("4. Application type: Seleziona 'Web application'")
    print()
    print("5. Name: Scrivi 'nonamebar.it - Base44'")
    print()
    print("6. Authorized JavaScript origins:")
    print("   Clicca '+ ADD URI' e aggiungi:")
    print("   • https://nonamebar.it")
    print("   • https://app.base44.com")
    print()
    print("7. Authorized redirect URIs:")
    print("   Clicca '+ ADD URI' e aggiungi:")
    print("   • https://app.base44.com/api/apps/auth/callback")
    print()
    print("8. Clicca il bottone blu 'CREATE'")
    print()
    print("9. Apparirà un popup con Client ID e Client Secret")
    print("   COPIALO SUBITO! (puoi anche scaricarlo come JSON)")
    print()
    print("10. Vai su Base44:")
    print("    Settings → Authentication → Google")
    print("    • Toggle ON 'Use a custom OAuth from Google Console'")
    print("    • Incolla Client ID")
    print("    • Incolla Client Secret")
    print("    • Clicca 'Update'")
    print()
    print("11. Testa il login su nonamebar.it")
    print()
    print("=" * 80)
    print()
    print("💡 VUOI UN'ALTERNATIVA?")
    print()
    print("Posso creare un prompt dettagliato per comet.ai che fa questo")
    print("automaticamente se comet ha accesso alla tua console Google.")
    print()
    print("Oppure possiamo fare screen sharing e lo faccio insieme a te")
    print("in 30 secondi mentre guardi.")
    print()
    print("Cosa preferisci?")
    print()

if __name__ == '__main__':
    create_new_oauth_client()
