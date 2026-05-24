import os
import subprocess

# [MELODIST SEOUL - FINAL RE-RENDER ENGINE v1.0]
# 역할: 지정된 5곡을 특정 배경과 로고, 이퀄라이저를 사용하여 렌더링합니다.

TRACKS_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\20260425 Suno_Songs_All"
OUTPUT_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\새 폴더"
LOGO_PATH = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\logo.png"
BG_IMAGE = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\INSPECT_000.png"

TARGET_TRACKS = [
    {"idx": 1, "name": "Pixelated Reverie_1.mp3", "output": "01_Pixelated_Reverie_FINAL.mp4"},
    {"idx": 2, "name": "Electric Dusk Mirror_1.mp3", "output": "02_Electric_Dusk_Mirror_FINAL.mp4"},
    {"idx": 3, "name": "Neural Net Nostalgia_1.mp3", "output": "03_Neural_Net_Nostalgia_1_FINAL.mp4"},
    {"idx": 4, "name": "City's Soft Hum_1.mp3", "output": "04_City's_Soft_Hum_1_FINAL.mp4"},
    {"idx": 5, "name": "Ephemeral Screen Glow_1.mp3", "output": "05_Ephemeral_Screen_Glow_1_FINAL.mp4"}
]

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    return float(subprocess.check_output(cmd).decode('utf-8').strip())

def render_5_tracks():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"== [START] 5곡 개별 렌더링 시작 (배경: INSPECT_000) ==")
    
    for item in TARGET_TRACKS:
        track_path = os.path.join(TRACKS_DIR, item["name"])
        output_path = os.path.join(OUTPUT_DIR, item["output"])
        
        if not os.path.exists(track_path):
            print(f"!! [SKIP] 파일 없음: {item['name']}")
            continue

        print(f"\n>> [{item['idx']}/5] {item['output']} 제작 중...")
        duration = get_duration(track_path)
        
        # FFmpeg 명령 (QSV 가속 + Equalizer)
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1', '-i', BG_IMAGE,
            '-i', LOGO_PATH,
            '-i', track_path,
            '-filter_complex', 
            '[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080[bg];' +
            '[1:v]colorkey=0xFFFFFF:0.1:0.1,scale=250:-1[logo];' +
            '[2:a]showwaves=s=400x40:mode=cline:colors=0xFFFFFF@0.6[viz];' +
            '[bg][viz]overlay=(W-w)/2:H-h-100[bg_viz];' +
            '[bg_viz][logo]overlay=W-w-50:50[outv]',
            '-map', '[outv]', '-map', '2:a',
            '-c:v', 'h264_qsv', '-global_quality', '25', '-preset', 'veryfast',
            '-t', str(duration), '-shortest', output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"   [OK] {item['output']} 완료")
        except Exception as e:
            print(f"   [FAIL] {item['output']} 오류: {e}")

if __name__ == "__main__":
    render_5_tracks()
