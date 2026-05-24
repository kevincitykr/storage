import requests
import json

url = "http://localhost:2027/generate"
payload = {
    "concept": "Spring Rain (Spring in Seoul)",
    "track_count": 1
}

print("--- [서버 최종 검증 시작] ---")
print(f"서버 주소: {url}")
print("요청 중... (최대 60초 소요될 수 있습니다)")

try:
    response = requests.post(url, json=payload, timeout=70)
    if response.status_code == 200:
        data = response.json()
        print("\n✅ [검증 성공!] 서버가 정상적으로 응답했습니다.")
        track = data['tracks'][0]
        print(f"곡 제목: {track['title']}")
        print(f"가사 (한글) 일부: {track['lyrics_ko'][:100]}...")
    else:
        print(f"\n❌ [검증 실패] 서버 에러 발생: {response.status_code}")
        print(f"상세 내용: {response.text}")
except Exception as e:
    print(f"\n❌ [연결 실패] 서버가 응답하지 않습니다: {str(e)}")
