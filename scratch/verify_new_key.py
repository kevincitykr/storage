import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 오늘 새로 뽑은 키
api_key = "AIzaSyC8gBs_g8vNYNWC8EgAoms5S1Gnh6e9snA"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": "Write a short one-line song title about victory."}]}]
}

print(f"--- [Brand New Key Verification] ---")
try:
    response = requests.post(url, json=payload, timeout=20)
    print(f"HTTP Status: {response.status_code}")
    
    res_json = response.json()
    if response.status_code == 200:
        print("SUCCESS! This key is PERFECT.")
        print(f"Response: {res_json['candidates'][0]['content']['parts'][0]['text'].strip()}")
    else:
        print("FAILED! Reason:")
        print(json.dumps(res_json, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"DIAGNOSTIC ERROR: {str(e)}")
