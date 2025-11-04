#!/usr/bin/env python3
"""Test API key access to Google Cloud services."""

import requests
import json
import os
import sys

# Get API key from environment variable or command line argument
API_KEY = os.environ.get('GCP_API_KEY') or (sys.argv[1] if len(sys.argv) > 1 else None)
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'waipro-agency')

def test_api_key():
    """Test the API key with various Google Cloud endpoints."""

    if not API_KEY:
        print("❌ Error: No API key provided")
        print()
        print("Usage:")
        print("  export GCP_API_KEY='your-api-key'")
        print("  python3 test_api_key.py")
        print()
        print("Or:")
        print("  python3 test_api_key.py your-api-key")
        return

    print("=" * 60)
    print("🔑 Testing API Key")
    print("=" * 60)
    print(f"Key: {API_KEY[:10]}...{API_KEY[-10:] if len(API_KEY) > 20 else ''}")
    print(f"Project: {PROJECT_ID}")
    print()

    # Test 1: Cloud Storage API
    print("1️⃣  Testing Cloud Storage API...")
    try:
        url = f"https://storage.googleapis.com/storage/v1/b?project={PROJECT_ID}&key={API_KEY}"
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Found {len(data.get('items', []))} buckets")
            for item in data.get('items', [])[:5]:
                print(f"      - {item.get('name')}")
        else:
            print(f"   ❌ Error: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    print()

    # Test 2: Cloud Resource Manager API
    print("2️⃣  Testing Cloud Resource Manager API...")
    try:
        url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT_ID}?key={API_KEY}"
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success!")
            print(f"      Project: {data.get('name')}")
            print(f"      State: {data.get('lifecycleState')}")
        else:
            print(f"   ❌ Error: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    print()

    # Test 3: Try as Firebase/Base44 key
    print("3️⃣  Testing as potential Base44/Firebase key...")
    try:
        # Try Firebase Database
        url = f"https://{PROJECT_ID}.firebaseio.com/.json?auth={API_KEY}"
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Firebase/Database access successful!")
        else:
            print(f"   ❌ Error: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    print()

    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print()
    print("Se la chiave ha funzionato, vedresti messaggi ✅ sopra.")
    print("Altrimenti, potrebbero servire credenziali diverse.")
    print()

if __name__ == '__main__':
    test_api_key()
