import requests
import json

keys = [
    "AIzaSyDOZHgTiy1ZxJLCE9yu9WXWE2U8eH4kxSw"  # 신규 발급 (Kevin-2026-04-30)
]

results = []

for i, key in enumerate(keys):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    try:
        response = requests.post(url, json=payload, timeout=10)
        status = "OK" if response.status_code == 200 else f"FAILED ({response.status_code})"
        error_msg = response.text if response.status_code != 200 else ""
        results.append({
            "index": i,
            "key_prefix": key[:10],
            "status": status,
            "error": error_msg[:100]
        })
    except Exception as e:
        results.append({
            "index": i,
            "key_prefix": key[:10],
            "status": "ERROR",
            "error": str(e)
        })

print(json.dumps(results, indent=2, ensure_ascii=False))
