import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 우리가 믿었던 jr 골든 키
api_key = "AIzaSyB-dBihJ6yrM11LzrtBYx0OTZK1-RgK340"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": "Write a short poem about rain."}]}]
}

print(f"--- [Direct API Diagnostic: JR KEY] ---")
try:
    response = requests.post(url, json=payload, timeout=20)
    print(f"HTTP Status: {response.status_code}")
    
    res_json = response.json()
    if response.status_code == 200:
        print("SUCCESS! API is working fine.")
        print(f"Response: {res_json['candidates'][0]['content']['parts'][0]['text'][:100]}...")
    else:
        print("FAILED! Google says:")
        print(json.dumps(res_json, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"DIAGNOSTIC ERROR: {str(e)}")
