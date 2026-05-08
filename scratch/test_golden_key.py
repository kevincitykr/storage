import requests
import json

key = "AIzaSyA1gYeI9RjWPQaOtC539cgvUdm_OSB00us"
models = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-pro"]
versions = ["v1beta", "v1"]

results = []

for version in versions:
    for model in models:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": "hi"}]}]}
        try:
            response = requests.post(url, json=payload, timeout=10)
            status = "OK" if response.status_code == 200 else f"FAILED ({response.status_code})"
            error_msg = response.text if response.status_code != 200 else "SUCCESS"
            results.append({
                "version": version,
                "model": model,
                "status": status,
                "response_preview": error_msg[:100]
            })
        except Exception as e:
            results.append({
                "version": version,
                "model": model,
                "status": "ERROR",
                "error": str(e)
            })

print(json.dumps(results, indent=2, ensure_ascii=False))
