import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

api_key = "AIzaSyB-dBihJ6yrM11LzrtBYx0OTZK1-RgK340"
# 모델명을 gemini-1.5-flash -> gemini-flash-latest 로 변경
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": "Write a one-line lyrics about the moon."}]}]
}

print(f"--- [Direct API Diagnostic: gemini-flash-latest] ---")
try:
    response = requests.post(url, json=payload, timeout=20)
    print(f"HTTP Status: {response.status_code}")
    
    res_json = response.json()
    if response.status_code == 200:
        print("SUCCESS! This model works with your key.")
        print(f"Response: {res_json['candidates'][0]['content']['parts'][0]['text'].strip()}")
    else:
        print("FAILED! Reason:")
        print(json.dumps(res_json, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"DIAGNOSTIC ERROR: {str(e)}")
