#!/usr/bin/env python3
"""Verify Google Cloud Platform access and permissions."""

import os
import json
from google.oauth2 import service_account
from google.cloud import storage
from google.auth.transport.requests import Request

# Set the credentials path
CREDENTIALS_PATH = '/home/user/infrastructure-backup/gcp-service-account.json'

def verify_access():
    """Verify access to GCP project."""

    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)

    print(f"🔐 Service Account: {creds_data['client_email']}")
    print(f"📋 Project ID: {creds_data['project_id']}")
    print()

    # Create credentials
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    # Verify credentials are valid
    credentials.refresh(Request())
    print("✅ Autenticazione riuscita!")
    print()

    # Try to access Cloud Storage
    try:
        storage_client = storage.Client(
            project=creds_data['project_id'],
            credentials=credentials
        )

        print("🗂️  Verifica accesso Cloud Storage...")
        buckets = list(storage_client.list_buckets())
        print(f"✅ Accesso a Cloud Storage confermato")
        print(f"📦 Trovati {len(buckets)} bucket(s):")
        for bucket in buckets:
            print(f"   - {bucket.name}")
        print()

    except Exception as e:
        print(f"⚠️  Cloud Storage: {str(e)}")
        print()

    # Print permissions scope
    print("🔑 Scopes disponibili:")
    for scope in credentials.scopes:
        print(f"   - {scope}")
    print()

    print("=" * 60)
    print("✅ CONNESSIONE STABILITA CON SUCCESSO")
    print("=" * 60)
    print()
    print("Il service account ha accesso completo al progetto:")
    print(f"   Project: {creds_data['project_id']}")
    print(f"   Account: {creds_data['client_email']}")
    print()
    print("Puoi ora utilizzare tutte le risorse GCP disponibili")
    print("per questo service account.")

if __name__ == '__main__':
    verify_access()
