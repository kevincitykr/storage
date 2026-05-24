# -*- coding: utf-8 -*-
"""
안실장_라틴음악봇.py
브라질 & 멕시코 유튜브 음악 채널 메타데이터 및 프롬프트 생성 시뮬레이터
"""
import sys
import os
import time
import io
from datetime import datetime

# 터미널 인코딩 설정
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

NOW_STR = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = os.path.abspath(f"./output/안실장_라틴음악_{NOW_STR}")

def log(msg):
    print(f"[*] {msg}", flush=True)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"\n[START] 안실장_라틴음악봇 ({NOW_STR}) 가동...", flush=True)
    time.sleep(2)
    
    print("\n[STEP 0] 브라질/멕시코 음악 트렌드 키워드 수집 중...", flush=True)
    log("Google Trends 'Music' 카테고리 분석...")
    log("브라질 인기 키워드 감지: 'Música para relaxar', 'Bossa Nova Lo-fi'")
    log("멕시코 인기 키워드 감지: 'Chill Latino', 'Reggaeton Instrumental'")
    time.sleep(3)
    
    print("\n[STEP 1] 다국어 메타데이터 (PT-BR, ES-MX) 생성 중...", flush=True)
    log("브라질(포르투갈어) 제목 생성 완료: [Bossa Lo-fi] Café da Manhã no Rio")
    log("멕시코(스페인어) 제목 생성 완료: [Chill Latino] Noche en la Ciudad de México")
    time.sleep(3)
    
    print("\n[STEP 2] 썸네일 및 쇼츠 비주얼 프롬프트 기획 중...", flush=True)
    log("브라질 타겟: 따뜻한 코파카바나 해변 일몰 화풍")
    log("멕시코 타겟: 멕시코시티의 감성적인 야경 애니메이션 화풍")
    time.sleep(3)
    
    print("\n[STEP 3] 최종 작업 지시서 저장 중...", flush=True)
    result_text = f"""
=== LATAM Expansion Work Order ({NOW_STR}) ===
1. Brazil (PT-BR)
   - Title: [Bossa Lo-fi] Café da Manhã no Rio - Música para relaxar e estudar
   - Prompt: A cozy room in Rio de Janeiro, view of Christ the Redeemer, warm sunset, lo-fi anime style.
   
2. Mexico (ES-MX)
   - Title: [Chill Latino] Noche en la Ciudad de México - Beats para concentrarse
   - Prompt: A vintage cafe in Mexico City, neon lights, rainy night, vibrant colors, detailed aesthetic.
"""
    file_path = os.path.join(OUTPUT_DIR, f"안실장_라틴음악_지시서_{NOW_STR}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result_text)
        
    log(f"작업 지시서 저장 완료: {file_path}")
    time.sleep(2)
    
    print("\n[FINISH] 라틴 음악 파이프라인 완료!", flush=True)

if __name__ == "__main__":
    main()
