import os
import json
import subprocess
from datetime import datetime

def search_trending_topics(query="심리학", max_results=20):
    print(f"[*] Searching for trending topics: {query}")
    
    # yt-dlp를 사용하여 최근 한 달간 조회수가 높은 영상 검색
    # --get-filename 대신 --print를 사용하여 필요한 정보만 추출
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:https://www.youtube.com/results?search_query={query}&sp=CAMSAhAB", # sp=CAMSAhAB is "This month" + "View count"
        "--print", "%(title)s|%(view_count)s|%(uploader)s|%(channel_url)s|%(webpage_url)s",
        "--quiet", "--no-warnings"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        lines = result.stdout.strip().split('\n')
        
        candidates = []
        for line in lines:
            if not line: continue
            parts = line.split('|')
            if len(parts) < 5: continue
            
            title, views, uploader, ch_url, url = parts
            views = int(views) if views.isdigit() else 0
            
            candidates.append({
                "title": title,
                "views": views,
                "uploader": uploader,
                "channel_url": ch_url,
                "url": url
            })
            
        return candidates
    except Exception as e:
        print(f"[!] Error during search: {e}")
        return []

def filter_small_giants(candidates):
    print("[*] Filtering for Small Giants...")
    small_giants = []
    
    for c in candidates:
        # 각 채널의 구독자 수를 확인 (yt-dlp로 추가 호출)
        cmd = ["yt-dlp", "--print", "%(channel_follower_count)s", "--quiet", c['channel_url']]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            subs = res.stdout.strip()
            # 구독자 수가 '1.5k', '100k' 등 문자열로 올 수 있음
            # 간단한 변환 로직 (필요 시 정교화)
            sub_count = parse_subs(subs)
            
            c['subscribers'] = sub_count
            c['ratio'] = c['views'] / sub_count if sub_count > 0 else 0
            
            # 조회수가 구독자 수보다 5배 이상 높으면 '작은 거인'으로 간주
            if sub_count < 100000 and c['ratio'] > 5:
                print(f"  [+] Found Small Giant: {c['uploader']} ({subs} subs, {c['views']} views)")
                small_giants.append(c)
        except:
            continue
            
    return sorted(small_giants, key=lambda x: x['ratio'], reverse=True)

def parse_subs(subs_str):
    try:
        subs_str = subs_str.lower().replace(' ', '').replace('구독자', '').replace('명', '')
        if 'k' in subs_str:
            return float(subs_str.replace('k', '')) * 1000
        if 'm' in subs_str:
            return float(subs_str.replace('m', '')) * 1000000
        if '만' in subs_str:
            return float(subs_str.replace('만', '')) * 10000
        return float(subs_str) if subs_str.isdigit() else 0
    except:
        return 0

def main():
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "심리학"
    max_results = 30
    
    topics = search_trending_topics(query, max_results)
    results = filter_small_giants(topics)
    
    output_filename = f"trending_topics_{query}.json"
    output_path = os.path.join(os.path.dirname(__file__), output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 레거시 호환성을 위해 기본 파일로도 저장
    with open("trending_topics.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n[+] Analysis complete. Saved {len(results)} topics to {output_path}")

if __name__ == "__main__":
    main()
