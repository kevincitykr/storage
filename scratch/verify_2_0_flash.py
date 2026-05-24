import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

api_key = "AIzaSyC8gBs_g8vNYNWC8EgAoms5S1Gnh6e9snA"
# 마지막 희망: 모델명을 gemini-2.0-flash 로 시도
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": "Say hello."}]}]
}

print(f"--- [Last Hope: Gemini 2.0 Flash Check] ---")
try:
    response = requests.post(url, json=payload, timeout=20)
    print(f"HTTP Status: {response.status_code}")
    
    res_json = response.json()
    if response.status_code == 200:
        print("OMG! It works with 2.0 Flash!")
        print(f"Response: {res_json['candidates'][0]['content']['parts'][0]['text'].strip()}")
    else:
        print(f"FAILED: {res_json.get('error', {}).get('message', 'Unknown Error')}")
except Exception as e:
    print(f"DIAGNOSTIC ERROR: {str(e)}")
