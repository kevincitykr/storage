import os
import json
import subprocess

# [MELODIST SEOUL - INDIVIDUAL BATCH RENDERER v1.0]
# 역할: 지정된 18개 트랙을 번호 순서대로 개별 MP4 파일로 초고속 렌더링합니다.

PLAN_FILE = r"d:\20260412 kevincity share\004_melodist_seoul\Suno_Factory_Customize\compilation_plan_a.json"
OUTPUT_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE"
TRACKS_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\20260425 Suno_Songs_All"
LOGO_PATH = r"d:\20260412 kevincity share\004_melodist_seoul\MELODIST_SEOUL_OFFICIAL_LOGO_배경투명.png"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    return float(subprocess.check_output(cmd).decode('utf-8').strip())

def render_all():
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    tracks = plan["tracks"]
    total = len(tracks)
    album_dir = r"d:\20260412 kevincity share\004_melodist_seoul\Suno_Factory_Customize\Album_A_Crystal"
    
    print(f"== [BATCH RENDER START] 총 {total}곡을 순차적으로 렌더링합니다. ==")
    
    for i, track_name in enumerate(tracks):
        idx = i + 1
        # Smart Image Selection
        base_name = track_name.replace(".mp3", "").replace(" ", "_")
        search_key = base_name.split('_')[0]
        
        possible_imgs = [f for f in os.listdir(album_dir) if search_key in f and f.endswith(".png")]
        if possible_imgs:
            image_path = os.path.join(album_dir, possible_imgs[0])
        else:
            all_imgs = [f for f in os.listdir(album_dir) if f.endswith(".png")]
            image_path = os.path.join(album_dir, all_imgs[0]) if all_imgs else None

        if not image_path:
            print(f"!! [SKIP] 이미지를 찾을 수 없음: {track_name}")
            continue

        # 파일명 생성 (사용자 요청 형식: 01_Title_FINAL.mp4)
        clean_title = base_name.replace("_1", "").replace("_2", "")
        output_filename = f"{idx:02d}_{clean_title}_FINAL.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        track_path = os.path.join(TRACKS_DIR, track_name)
        
        print(f"\n>> [{idx}/{total}] 작업 중: {output_filename} (이미지: {os.path.basename(image_path)})")
        
        if not os.path.exists(track_path):
            print(f"!! [SKIP] 오디오 파일 없음: {track_path}")
            continue

        duration = get_duration(track_path)
        
        # FFmpeg 명령 (Intel QuickSync 가속 버전)
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1', '-i', image_path,
            '-i', LOGO_PATH,
            '-i', track_path,
            '-filter_complex', 
            '[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080[bg];' +
            '[1:v]colorkey=0xFFFFFF:0.1:0.1,scale=250:-1[logo];' +
            '[2:a]showwaves=s=400x40:mode=cline:colors=0xFFFFFF@0.4[viz];' +
            '[bg][viz]overlay=(W-w)/2:H-h-60[bg_viz];' +
            '[bg_viz][logo]overlay=W-w-50:50[outv]',
            '-map', '[outv]', '-map', '2:a',
            '-c:v', 'h264_qsv', '-global_quality', '25', '-preset', 'veryfast',
            '-t', str(duration), '-shortest', output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"OK: {output_filename} 완료!")
        except Exception as e:
            print(f"FAIL: {output_filename} 에러 발생 -> {e}")

if __name__ == "__main__":
    render_all()
    print("\n== [SUCCESS] 모든 곡의 개별 렌더링이 완료되었습니다! ==")
