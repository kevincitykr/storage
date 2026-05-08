import requests
import json
import sys

# 인코딩 강제 설정
sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:2027/generate"
payload = {
    "concept": "Spring Rain",
    "track_count": 1
}

print("--- [Server Final Check] ---")
try:
    response = requests.post(url, json=payload, timeout=70)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("SUCCESS: Engine is working!")
        track = data['tracks'][0]
        print(f"Title: {track['title']}")
        print(f"Lyrics Preview: {track['lyrics_ko'][:50]}...")
    elif response.status_code == 401:
        print("ERROR 401: API Key is invalid or expired (Unauthorized)")
        print(f"Server Message: {response.text}")
    else:
        print(f"ERROR {response.status_code}: Something went wrong.")
        print(f"Server Message: {response.text}")
except Exception as e:
    print(f"CONNECTION ERROR: {str(e)}")
