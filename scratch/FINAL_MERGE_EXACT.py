import os
import subprocess

# [MELODIST SEOUL - EXACT 18 TRACK MERGER]
# 역할: 사용자님이 지정한 정확한 18개 파일명을 순서대로 합칩니다.

RELEASE_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE"
FINAL_OUTPUT = os.path.join(RELEASE_DIR, "MELODIST_SEOUL_CRYSTAL_VIBE_V1_FULL_ALBUM.mp4")

TARGET_FILES = [
    "01_Pixelated_Reverie_FINAL.mp4",
    "02_Electric_Dusk_Mirror_FINAL.mp4",
    "03_Neural_Net_Nostalgia_1_FINAL.mp4",
    "04_City's_Soft_Hum_1_FINAL.mp4",
    "05_Ephemeral_Screen_Glow_1_FINAL.mp4",
    "06_Circuit_Bloom_1_FINAL.mp4",
    "07_Midnight_Glow_Algorithm_1_A_FINAL.mp4",
    "08_Invisible_Network_Heart_1_A_FINAL.mp4",
    "09_Flicker_&_Fade_1_A_FINAL.mp4",
    "10_Broken_Signal_Lullaby_1_A_FINAL.mp4",
    "11_Static_Heartbeat_1_A_FINAL.mp4",
    "12_Whispers_of_the_Wired_World_1_A_FINAL.mp4",
    "13_Dream_Loop_Protocol_1_A_FINAL.mp4",
    "14_Circuit_Board_Blues_1_A_FINAL.mp4",
    "15_Ghost_in_the_Machine_1_A_FINAL.mp4",
    "16_Neon_Rain_Echoes_1_A_FINAL.mp4",
    "17_Dreaming_in_Data_1_A_FINAL.mp4",
    "18_Holographic_Echo_1_A_FINAL.mp4"
]

def merge_exact_18():
    list_path = os.path.join(RELEASE_DIR, "merge_list_exact.txt")
    valid_count = 0
    
    with open(list_path, "w", encoding="utf-8") as f:
        for filename in TARGET_FILES:
            full_path = os.path.join(RELEASE_DIR, filename)
            if os.path.exists(full_path):
                f.write(f"file '{full_path.replace('\\', '/')}'\n")
                print(f"   [OK] {filename}")
                valid_count += 1
            else:
                print(f"   [!!] MISSING: {filename}")
                
    if valid_count == 0:
        print("!! [ERROR] 합칠 수 있는 파일이 없습니다.")
        return

    print(f"\n>> [MERGE START] {valid_count}개의 파일을 합치는 중...")
    
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_path,
        '-c', 'copy', FINAL_OUTPUT
    ]
    
    subprocess.run(cmd)
    print(f"\n>> [SUCCESS] 앨범 병합 완료: {FINAL_OUTPUT}")

if __name__ == "__main__":
    merge_exact_18()
