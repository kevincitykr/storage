import os
import json
import subprocess

# [MELODIST SEOUL - FINAL ALBUM MERGER v1.0]
# 역할: 이미 렌더링된 18개의 조각 파일들을 하나의 풀 앨범 영상으로 합칩니다.

RELEASE_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE"
FINAL_OUTPUT = os.path.join(RELEASE_DIR, "MELODIST_SEOUL_CRYSTAL_VIBE_V1_FULL_ALBUM.mp4")

def merge_album():
    PLAN_FILE = r"d:\20260412 kevincity share\004_melodist_seoul\Suno_Factory_Customize\compilation_plan_a.json"
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    tracks = plan["tracks"]
    valid_files = []
    
    print(">> [TARGET CHECK] 합칠 대상 파일을 확인 중...")
    for i, track_name in enumerate(tracks):
        idx = i + 1
        base_name = track_name.replace(".mp3", "").replace(" ", "_")
        clean_title = base_name.replace("_1", "").replace("_2", "")
        expected_name = f"{idx:02d}_{clean_title}_FINAL.mp4"
        
        full_path = os.path.join(RELEASE_DIR, expected_name)
        if os.path.exists(full_path):
            valid_files.append(full_path)
            print(f"   [{idx}/18] 확인: {expected_name}")
        else:
            print(f"   !! [MISSING] 파일을 찾을 수 없음: {expected_name}")

    if not valid_files:
        print("!! [ERROR] 합칠 수 있는 파일이 하나도 없습니다.")
        return

    list_path = os.path.join(RELEASE_DIR, "merge_list_fixed.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for path in valid_files:
            f.write(f"file '{path.replace('\\', '/')}'\n")
            
    print(f"\n>> [MERGE START] {len(valid_files)}개의 트랙 병합 시작...")
    
    # -c copy 를 사용하여 재인코딩 없이 초고속 병합
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_path,
        '-c', 'copy', FINAL_OUTPUT
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n>> [SUCCESS] 풀 앨범 영상 제작 완료!")
        print(f">> 경로: {FINAL_OUTPUT}")
    except Exception as e:
        print(f"!! [ERROR] 병합 중 오류 발생: {e}")

if __name__ == "__main__":
    merge_album()
