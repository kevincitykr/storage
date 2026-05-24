import requests
import base64
import os
import json
import subprocess
import time

# Paths
FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FORGE_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"
OUTPUT_DIR = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\final_production"
FONT_PATH = "C\\:/Windows/Fonts/arial.ttf"

def assemble_video_fixed():
    # Find all existing images
    images = sorted([f for f in os.listdir(OUTPUT_DIR) if f.startswith("scene_") and f.endswith(".png")])
    if not images: return
    
    count = len(images)
    print(f"Assembling {count} scenes...")
    
    cmd = [FFMPEG, "-y"]
    for img in images:
        cmd.extend(["-loop", "1", "-t", "9", "-i", os.path.join(OUTPUT_DIR, img)])
    
    filter_complex = []
    for i in range(count):
        text = f"CHAPTER ANALYSIS SCENE {i+1}".replace(":", "\\:")
        filter_complex.append(f"[{i}:v]drawtext=fontfile='{FONT_PATH}':text='{text}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-100:enable='between(t,0,9)'[v{i}]")
    
    concat_str = "".join([f"[v{i}]" for i in range(count)]) + f"concat=n={count}:v=1:a=0[outv]"
    cmd.extend(["-filter_complex", ";".join(filter_complex) + ";" + concat_str, "-map", "[outv]", "-c:v", "libx264", "-preset", "ultrafast", os.path.join(OUTPUT_DIR, "FINAL_MASTERPIECE_DRAFT.mp4")])
    
    subprocess.run(cmd)

if __name__ == "__main__":
    assemble_video_fixed()
    print("RESUME SUCCESS: MASTERPIECE DRAFT UPDATED.")
