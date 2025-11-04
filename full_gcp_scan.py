#!/usr/bin/env python3
"""Complete scan of Google Cloud Project resources."""

import json
from google.oauth2 import service_account
from google.cloud import storage
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def full_scan():
    """Scan all accessible resources in the GCP project."""

    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    project_id = creds_data['project_id']

    print("=" * 80)
    print("🔍 SCANSIONE COMPLETA PROGETTO GOOGLE CLOUD")
    print("=" * 80)
    print(f"Progetto: {project_id}")
    print(f"Service Account: {creds_data['client_email']}")
    print()

    # Get access token for API calls
    credentials.refresh(GoogleAuthRequest())
    access_token = credentials.token

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # 1. Cloud Storage
    print("📦 CLOUD STORAGE")
    print("-" * 80)
    try:
        storage_client = storage.Client(project=project_id, credentials=credentials)
        buckets = list(storage_client.list_buckets())

        if buckets:
            print(f"✅ Trovati {len(buckets)} bucket(s):")
            for bucket in buckets:
                print(f"\n   Bucket: {bucket.name}")
                print(f"   Location: {bucket.location}")
                print(f"   Storage Class: {bucket.storage_class}")
                print(f"   Created: {bucket.time_created}")

                # List some files
                blobs = list(bucket.list_blobs(max_results=5))
                if blobs:
                    print(f"   Files (first 5):")
                    for blob in blobs:
                        print(f"      - {blob.name} ({blob.size} bytes)")
                else:
                    print(f"   Files: (vuoto)")
        else:
            print("ℹ️  Nessun bucket trovato")
    except Exception as e:
        print(f"❌ Errore: {e}")
    print()

    # 2. Enabled APIs
    print("🔧 API ABILITATE")
    print("-" * 80)
    try:
        url = f'https://serviceusage.googleapis.com/v1/projects/{project_id}/services?filter=state:ENABLED'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])
            print(f"✅ {len(services)} API abilitate:")

            for service in services[:20]:  # Show first 20
                name = service.get('config', {}).get('name', '')
                title = service.get('config', {}).get('title', name)
                print(f"   • {title}")

            if len(services) > 20:
                print(f"   ... e altre {len(services) - 20} API")
        else:
            print(f"⚠️  Status: {response.status_code}")
            print(f"   {response.text[:200]}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    print()

    # 3. Firebase/Firestore
    print("🔥 FIREBASE / FIRESTORE")
    print("-" * 80)
    try:
        # Check if Firebase is enabled
        firebase_url = f'https://firebase.googleapis.com/v1beta1/projects/{project_id}'
        response = requests.get(firebase_url, headers=headers, timeout=30)

        if response.status_code == 200:
            firebase_data = response.json()
            print(f"✅ Firebase abilitato:")
            print(f"   Project Number: {firebase_data.get('projectNumber')}")
            print(f"   Display Name: {firebase_data.get('displayName')}")

            resources = firebase_data.get('resources', {})
            if 'realtimeDatabaseInstance' in resources:
                print(f"   Realtime Database: {resources['realtimeDatabaseInstance']}")
            if 'storageBucket' in resources:
                print(f"   Storage Bucket: {resources['storageBucket']}")
        else:
            print(f"ℹ️  Firebase non configurato o non accessibile")
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  {e}")
    print()

    # 4. Cloud Functions
    print("⚡ CLOUD FUNCTIONS")
    print("-" * 80)
    try:
        functions_url = f'https://cloudfunctions.googleapis.com/v1/projects/{project_id}/locations/-/functions'
        response = requests.get(functions_url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            functions = data.get('functions', [])

            if functions:
                print(f"✅ Trovate {len(functions)} function(s):")
                for func in functions:
                    print(f"\n   Function: {func.get('name')}")
                    print(f"   Runtime: {func.get('runtime')}")
                    print(f"   Status: {func.get('status')}")
                    print(f"   Trigger: {func.get('httpsTrigger', {}).get('url', 'N/A')}")
            else:
                print("ℹ️  Nessuna Cloud Function trovata")
        else:
            print(f"⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    print()

    # 5. Compute Engine
    print("💻 COMPUTE ENGINE")
    print("-" * 80)
    try:
        compute_url = f'https://compute.googleapis.com/compute/v1/projects/{project_id}/aggregated/instances'
        response = requests.get(compute_url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get('items', {})

            vm_count = 0
            for zone, zone_data in items.items():
                instances = zone_data.get('instances', [])
                vm_count += len(instances)

                for instance in instances:
                    print(f"\n   VM: {instance.get('name')}")
                    print(f"   Zone: {zone}")
                    print(f"   Status: {instance.get('status')}")
                    print(f"   Machine Type: {instance.get('machineType', '').split('/')[-1]}")

            if vm_count == 0:
                print("ℹ️  Nessuna VM trovata")
            else:
                print(f"\n✅ Totale VMs: {vm_count}")
        else:
            print(f"⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    print()

    # 6. IAM Service Accounts
    print("👤 SERVICE ACCOUNTS")
    print("-" * 80)
    try:
        iam_url = f'https://iam.googleapis.com/v1/projects/{project_id}/serviceAccounts'
        response = requests.get(iam_url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            accounts = data.get('accounts', [])

            print(f"✅ Trovati {len(accounts)} service account(s):")
            for acc in accounts:
                email = acc.get('email')
                current = " (QUESTO)" if email == creds_data['client_email'] else ""
                print(f"   • {email}{current}")
        else:
            print(f"⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    print()

    # Summary
    print("=" * 80)
    print("✅ SCANSIONE COMPLETATA")
    print("=" * 80)
    print()
    print("Il progetto è stato scansionato completamente.")
    print("Tutti i servizi accessibili sono stati elencati sopra.")
    print()

if __name__ == '__main__':
    full_scan()
