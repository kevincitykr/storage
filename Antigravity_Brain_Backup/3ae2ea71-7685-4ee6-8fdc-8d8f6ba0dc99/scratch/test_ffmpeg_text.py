import subprocess
import os

bg_img = r"D:\20260412 kevincity share\004_melodist_seoul\Shared_Assets\Backgrounds\bright_morning_cafe_1777476318513.png"

dummy_audio = r"D:\20260412 kevincity share\004_melodist_seoul\Suno_Downloads\20260429_125141\Guam_Sun_and_Ocean_Breeze.mp3"
output_path = r"D:\20260412 kevincity share\004_melodist_seoul\Outputs_Shorts\TEST_TEXT_SHORT.mp4"

font_path = "C\\:/Windows/Fonts/malgunbd.ttf"

cmd = [
    'ffmpeg', '-y',
    '-loop', '1', '-i', bg_img,
    '-i', dummy_audio,
    '-filter_complex', 
    f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
    f"[bg]drawbox=y=200:h=200:color=black@0.6:t=fill,"
    f"drawtext=fontfile='{font_path}':text='오늘 밤, 당신의 외로움을 달래줄 멜로디':fontcolor='#FFD700':fontsize=48:x=(w-text_w)/2:y=270[v_top];"
    f"[v_top]drawbox=y=1600:h=150:color=black@0.6:t=fill,"
    f"drawtext=fontfile='{font_path}':text='풀버전은 고정댓글 확인 🎧':fontcolor='#00FFFF':fontsize=42:x=(w-text_w)/2:y=1650[v_final]",
    '-map', '[v_final]', '-map', '1:a',
    '-c:v', 'libx264', '-preset', 'veryfast', '-t', '10', '-shortest', output_path
]

print("Running test render...")
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
if result.returncode == 0:
    print(f"Success! Created {output_path}")
else:
    print("Failed!")
    print(result.stderr)
