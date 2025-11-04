#!/usr/bin/env python3
"""List all enabled APIs in the GCP project."""

import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def list_apis():
    """List all enabled APIs."""

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
    print("🔧 LISTA COMPLETA API ABILITATE")
    print("=" * 80)
    print(f"Progetto: {project_id}\n")

    try:
        url = f'https://serviceusage.googleapis.com/v1/projects/{project_id}/services?filter=state:ENABLED&pageSize=200'
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])

            print(f"✅ Trovate {len(services)} API abilitate:\n")

            # Group by category
            categories = {}
            for service in services:
                name = service.get('config', {}).get('name', '')
                title = service.get('config', {}).get('title', name)

                # Categorize
                if 'firebase' in name.lower() or 'firestore' in name.lower():
                    category = '🔥 Firebase'
                elif 'storage' in name.lower():
                    category = '📦 Storage'
                elif 'compute' in name.lower():
                    category = '💻 Compute'
                elif 'function' in name.lower():
                    category = '⚡ Functions'
                elif 'bigquery' in name.lower():
                    category = '📊 BigQuery'
                elif 'iam' in name.lower() or 'auth' in name.lower():
                    category = '🔐 Security'
                elif 'api' in name.lower() or 'cloud' in name.lower():
                    category = '☁️ Core Services'
                else:
                    category = '📋 Other'

                if category not in categories:
                    categories[category] = []
                categories[category].append({'name': name, 'title': title})

            # Print by category
            for category in sorted(categories.keys()):
                print(f"\n{category}")
                print("-" * 80)
                for svc in sorted(categories[category], key=lambda x: x['title']):
                    print(f"   ✓ {svc['title']}")
                    print(f"     {svc['name']}")

            print("\n" + "=" * 80)
            print("✅ LISTA COMPLETA")
            print("=" * 80)

            # Check specific services
            print("\n📌 SERVIZI CHIAVE:")
            key_services = {
                'Firebase': 'firebase.googleapis.com',
                'Firestore': 'firestore.googleapis.com',
                'Cloud Functions': 'cloudfunctions.googleapis.com',
                'Cloud Storage': 'storage-component.googleapis.com',
                'IAM': 'iam.googleapis.com',
                'Service Usage': 'serviceusage.googleapis.com'
            }

            for service_name, service_id in key_services.items():
                enabled = any(s.get('config', {}).get('name') == service_id for s in services)
                status = "✅ ABILITATA" if enabled else "❌ NON ABILITATA"
                print(f"   {service_name}: {status}")

        else:
            print(f"❌ Errore: {response.status_code}")
            print(response.text[:500])

    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == '__main__':
    list_apis()
