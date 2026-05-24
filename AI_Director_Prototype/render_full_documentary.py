import os
import json
import subprocess

FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
BG_IMG = r"C:\Users\ksohw\.gemini\antigravity\brain\bbee1948-81d6-45fa-bc2e-a2ed6291dd81\melodist_masterpiece_final_perfection_v9_1778768514551.png"
AUDIO = r"D:\Kevincity Share\004_melodist_seoul\01_RAW_AUDIO\Morning Pop\Song1_Champagne_Opening.mp3"
FONT_PATH = "C\\:/Windows/Fonts/arial.ttf"
OUTPUT = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\FULL_1M_DOCUMENTARY.mp4"

def render_documentary(script_json_path):
    with open(script_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    scenes = data.get('scenes', [])[:50] # Limit for speed in prototype, will use full later
    
    drawtext_filters = []
    duration_per_scene = 15 # 15 seconds per scene
    
    for i, scene in enumerate(scenes):
        script = scene.get('script', '')
        start = i * duration_per_scene
        end = (i + 1) * duration_per_scene
        # Basic escaping for FFmpeg
        clean_script = script.replace(":", "\\:").replace("'", "").replace(",", "\\,")
        f = f"drawtext=fontfile='{FONT_PATH}':text='{clean_script}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h-150:enable='between(t,{start},{end})'"
        drawtext_filters.append(f)

    filter_str = ",".join(drawtext_filters)
    total_duration = len(scenes) * duration_per_scene

    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", BG_IMG,
        "-i", AUDIO,
        "-vf", filter_str,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_duration), "-shortest", OUTPUT
    ]

    subprocess.run(cmd, check=True)
    print(f"SUCCESS: {OUTPUT} created.")

if __name__ == "__main__":
    # This will be called once gemma_script.json is ready
    if os.path.exists("gemma_script.json"):
        render_documentary("gemma_script.json")
