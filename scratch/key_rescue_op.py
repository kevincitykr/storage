import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

test_keys = [
    {"name": "0127 (kevincity0127)", "key": "AIzaSyAo3cbJdaFi_upe5NmD09HM2RNPGakIVwQ"},
    {"name": "0116 (kkseob)", "key": "AIzaSyBvDNNFJqWJxs2ktJzQ_GsVKU_rm0DNe3k"},
    {"name": "116 (gsgim)", "key": "AIzaSyBo_mSzeOg_bHoY8eGziO6SaaEXObhPZwU"},
    {"name": "005 (kevincitykr005)", "key": "AIzaSyAj-kjDlGzWieJ4Cn3jm-xAYqf-OTd3Xqs"}
]

print("--- [Multi-Key Rescue Operation] ---")

for item in test_keys:
    name = item['name']
    key = item['key']
    print(f"\nTesting {name}...")
    
    # 모델명은 가장 표준적인 flash-latest 사용
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ SUCCESS! Key {name} is ALIVE and has QUOTA.")
        else:
            print(f"❌ FAILED ({response.status_code}): {response.text[:100]}")
    except Exception as e:
        print(f"⚠️ ERROR: {str(e)}")

print("\n--- [Rescue Operation Finished] ---")
