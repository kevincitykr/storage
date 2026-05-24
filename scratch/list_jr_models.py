import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

api_key = "AIzaSyB-dBihJ6yrM11LzrtBYx0OTZK1-RgK340"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("--- [Checking Available Models for JR KEY] ---")
try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"Found {len(models)} models.")
        for m in models:
            print(f"- {m['name']} (Methods: {', '.join(m['supportedGenerationMethods'])})")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
