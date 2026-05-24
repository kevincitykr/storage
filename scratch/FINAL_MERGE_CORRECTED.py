import os
import subprocess

# [MELODIST SEOUL - USER-SPECIFIED 18 TRACK MERGER]
# 역할: 사용자님이 주신 정확한 파일명 18개를 번호 순으로 합칩니다.

RELEASE_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE"
FINAL_OUTPUT = os.path.join(RELEASE_DIR, "MELODIST_SEOUL_CRYSTAL_VIBE_V1_FULL_ALBUM.mp4")

# 사용자님이 주신 리스트 (순서 정렬용)
RAW_LIST = [
    "17_Dreaming_in_Data_1_A_FINAL.mp4",
    "02_Electric_Dusk_Mirror_FINAL.mp4",
    "01_Pixelated_Reverie_FINAL.mp4",
    "05_Ephemeral_Screen_Glow_1_FINAL.mp4",
    "04_City's_Soft_Hum_1_FINAL.mp4",
    "12_Whispers_of_the_Wired_World_1_A_FINAL.mp4",
    "16_Neon_Rain_Echoes_1_A_FINAL.mp4",
    "15_Ghost_in_the_Machine_1_A_FINAL.mp4",
    "13_Dream_Loop_Protocol_1_A_FINAL.mp4",
    "08_Invisible_Network_Heart_1_A_FINAL.mp4",
    "10_Broken_Signal_Lullaby_1_A_FINAL.mp4",
    "09_Flicker_&_Fade_1_A_FINAL.mp4",
    "11_Static_Heartbeat_1_A_FINAL.mp4",
    "03_Neural_Net_Nostalgia_1_FINAL.mp4",
    "18_Holographic_Echo_1_A_FINAL.mp4",
    "07_Midnight_Glow_Algorithm_1_A_FINAL.mp4",
    "06_Circuit_Bloom_1_FINAL.mp4",
    "14_Circuit_Board_Blues_1_A_FINAL.mp4"
]

def merge_user_list():
    # 번호 순서(01, 02, ...)대로 정렬
    sorted_list = sorted(RAW_LIST)
    
    list_path = os.path.join(RELEASE_DIR, "final_merge_list.txt")
    print(">> [CHECK] 대상 파일 존재 여부 확인 중...")
    
    with open(list_path, "w", encoding="utf-8") as f:
        for filename in sorted_list:
            full_path = os.path.join(RELEASE_DIR, filename)
            if os.path.exists(full_path):
                # FFmpeg concat용 특수 이스케이프 처리
                f.write(f"file '{filename}'\n") 
                print(f"   [OK] {filename}")
            else:
                print(f"   [!!] MISSING: {filename}")
                
    print(f"\n>> [MERGE START] {len(sorted_list)}개 파일을 합치는 중...")
    
    # 작업 디렉토리를 RELEASE_DIR로 설정하여 파일명만 참조하도록 함
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'final_merge_list.txt',
        '-c', 'copy', FINAL_OUTPUT
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=RELEASE_DIR)
        print(f"\n>> [SUCCESS] 풀 앨범 완성: {FINAL_OUTPUT}")
    except Exception as e:
        print(f"!! [ERROR] 병합 실패: {e}")

if __name__ == "__main__":
    merge_user_list()
