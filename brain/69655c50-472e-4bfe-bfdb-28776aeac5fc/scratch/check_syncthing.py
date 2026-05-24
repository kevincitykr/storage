import requests
import json

API_KEY = "w3ErEbSuoqNd9DtiifDzszosg6Rxp7My"
BASE_URL = "http://127.0.0.1:8384"
HEADERS = {"X-API-Key": API_KEY}

try:
    response = requests.get(f"{BASE_URL}/rest/system/config", headers=HEADERS)
    if response.status_code == 200:
        config = response.json()
        print("=== Devices ===")
        for device in config.get('devices', []):
            print(f"Name: {device.get('name')}, ID: {device.get('deviceID')}")
        
        print("\n=== Folders ===")
        for folder in config.get('folders', []):
            print(f"Label: {folder.get('label')}, ID: {folder.get('id')}")
            print("Shared with:")
            for dev in folder.get('devices', []):
                print(f"  - {dev.get('deviceID')}")
    else:
        print(f"Failed to fetch config. Status: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
