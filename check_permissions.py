#!/usr/bin/env python3
"""Check service account permissions and roles."""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def check_permissions():
    """Check what permissions and roles the service account has."""

    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    print("=" * 70)
    print("🔍 VERIFICA PERMESSI SERVICE ACCOUNT")
    print("=" * 70)
    print(f"Account: {creds_data['client_email']}")
    print(f"Project: {creds_data['project_id']}")
    print()

    # Check IAM policy
    try:
        print("📋 Recupero policy IAM del progetto...")
        service = build('cloudresourcemanager', 'v1', credentials=credentials)

        policy = service.projects().getIamPolicy(
            resource=creds_data['project_id'],
            body={}
        ).execute()

        # Find roles for this service account
        sa_email = creds_data['client_email']
        sa_roles = []

        for binding in policy.get('bindings', []):
            members = binding.get('members', [])
            if f'serviceAccount:{sa_email}' in members:
                sa_roles.append(binding['role'])

        if sa_roles:
            print(f"✅ Ruoli assegnati a questo service account:")
            for role in sorted(sa_roles):
                print(f"   • {role}")
        else:
            print("⚠️  Nessun ruolo trovato per questo service account")
        print()

    except HttpError as e:
        print(f"⚠️  Impossibile recuperare IAM policy: {e}")
        print()

    # Check available APIs
    print("🔧 Verifica API disponibili...")
    try:
        service = build('serviceusage', 'v1', credentials=credentials)

        request = service.services().list(
            parent=f'projects/{creds_data["project_id"]}',
            filter='state:ENABLED'
        )
        response = request.execute()

        enabled_services = response.get('services', [])
        print(f"✅ API abilitate: {len(enabled_services)}")

        # Show most important APIs
        important_apis = [
            'storage', 'compute', 'cloudresourcemanager',
            'iam', 'cloudfunctions', 'firebase', 'firestore'
        ]

        print("\n📦 API rilevanti:")
        for svc in enabled_services:
            name = svc.get('config', {}).get('name', '')
            for api in important_apis:
                if api in name.lower():
                    title = svc.get('config', {}).get('title', name)
                    print(f"   ✓ {title}")
                    break
        print()

    except HttpError as e:
        print(f"⚠️  Impossibile verificare API: {e}")
        print()

    # Summary
    print("=" * 70)
    print("✅ CONNESSIONE ATTIVA")
    print("=" * 70)
    print()
    print("Il service account è autenticato e pronto per essere utilizzato.")
    print("Puoi procedere con le operazioni sul progetto GCP.")
    print()

if __name__ == '__main__':
    check_permissions()
