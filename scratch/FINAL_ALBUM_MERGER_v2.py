import os
import subprocess

# [MELODIST SEOUL - ULTIMATE ALBUM MERGER v2.0]
# 역할: '새 폴더'에 준비된 18개의 조각을 하나의 풀 앨범으로 합칩니다.

TARGET_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\새 폴더"
OUTPUT_PATH = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\MELODIST_SEOUL_CRYSTAL_VIBE_V1_FULL_ALBUM_FINAL.mp4"

def merge_final_album():
    # 파일 목록 가져오기 및 번호순 정렬
    files = [f for f in os.listdir(TARGET_DIR) if f.endswith(".mp4")]
    files.sort() # 01, 02... 18 순서대로 정렬됨
    
    if len(files) != 18:
        print(f"!! [주의] 파일 개수가 18개가 아닙니다. (현재 {len(files)}개 발견)")
    
    list_path = os.path.join(TARGET_DIR, "merge_list.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for filename in files:
            # FFmpeg concat 파일에서 따옴표(')는 '\'' 로 이스케이프 해야 합니다.
            escaped_name = filename.replace("'", "'\\''")
            f.write(f"file '{escaped_name}'\n")
            
    print(f">> [MERGE START] 18개의 조각을 하나로 합치는 중...")
    
    # -c copy 를 사용하여 초고속 병합
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'merge_list.txt',
        '-c', 'copy', OUTPUT_PATH
    ]
    
    try:
        # TARGET_DIR 에서 실행하여 상대 경로 참조
        subprocess.run(cmd, check=True, cwd=TARGET_DIR)
        print(f"\n>> [SUCCESS] 최종 합본 제작 완료!")
        print(f">> 경로: {OUTPUT_PATH}")
    except Exception as e:
        print(f"!! [ERROR] 병합 중 오류 발생: {e}")

if __name__ == "__main__":
    merge_final_album()
