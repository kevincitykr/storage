import os
import json
import subprocess

# [MELODIST SEOUL - RE-RENDER TRACKS 01-05]
# 역할: 누락되거나 오류가 난 1~5번 트랙을 다시 렌더링하여 '새 폴더'에 넣습니다.

PLAN_FILE = r"d:\20260412 kevincity share\004_melodist_seoul\Suno_Factory_Customize\compilation_plan_a.json"
TARGET_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\새 폴더"
TRACKS_DIR = r"D:\20260412 kevincity share\004_melodist_seoul\20260425 Suno_Songs_All"
LOGO_PATH = r"d:\20260412 kevincity share\004_melodist_seoul\MELODIST_SEOUL_OFFICIAL_LOGO_배경투명.png"
ALBUM_DIR = r"d:\20260412 kevincity share\004_melodist_seoul\Suno_Factory_Customize\Album_A_Crystal"

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    return float(subprocess.check_output(cmd).decode('utf-8').strip())

def re_render_1_to_5():
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    tracks = plan["tracks"]
    
    # 01번부터 05번까지만 작업 (인덱스 0~4)
    for i in range(5):
        track_name = tracks[i]
        idx = i + 1
        
        base_name = track_name.replace(".mp3", "").replace(" ", "_")
        search_key = base_name.split('_')[0]
        
        # 이미지 찾기
        possible_imgs = [f for f in os.listdir(ALBUM_DIR) if search_key in f and f.endswith(".png")]
        image_path = os.path.join(ALBUM_DIR, possible_imgs[0] if possible_imgs else os.listdir(ALBUM_DIR)[0])

        # 파일명 생성 (사용자 리스트 형식 반영)
        # 03, 04, 05번은 뒤에 _1이 붙는 형식인지 확인이 필요하나, 사용자 리스트에 맞춰 생성
        clean_title = base_name.replace("_1", "").replace("_2", "")
        
        # 01, 02는 _1이 없고, 03, 04, 05는 _1이 붙는 사용자 리스트 규칙 준수
        if idx in [1, 2]:
            output_filename = f"{idx:02d}_{clean_title}_FINAL.mp4"
        else:
            output_filename = f"{idx:02d}_{clean_title}_1_FINAL.mp4"
            
        output_path = os.path.join(TARGET_DIR, output_filename)
        track_path = os.path.join(TRACKS_DIR, track_name)
        
        print(f">> [{idx}/5] 다시 렌더링 중: {output_filename}")
        
        duration = get_duration(track_path)
        
        # FFmpeg (하드웨어 가속 QSV)
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
        
        subprocess.run(cmd)
        print(f"   DONE: {output_filename}")

if __name__ == "__main__":
    re_render_1_to_5()
