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
if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
FONT_PATH = "C\\:/Windows/Fonts/arial.ttf"

# Full 100-scene script skeleton (abbreviated for the orchestrator to run)
# In a real scenario, this would be read from the full_economic_documentary_script.md
def get_full_scenes():
    # Simplified scene list for the orchestrator to process 100 items
    base_scenes = [
        "2026 EMERGENCY REPORT: THE KOREAN ECONOMY AT A CROSSROADS",
        "SAMSUNG STRIKE: 100 TRILLION WON AT RISK",
        "GLOBAL SUPPLY CHAIN COLLAPSE WARNING",
        "KOSPI 8000: THE GREATEST PARADOX",
        "US SMART MONEY FLOCKING TO KOREA",
        "REAL ESTATE: THE 3-9 MONTH RULE",
        "JEONSE PRICE SURGE AND SALE PRICE HIKE",
        "ASSET PROTECTION STRATEGY FOR SENIORS",
        "THE FUTURE OF KOREAN SEMICONDUCTORS",
        "INVESTMENT INSIGHTS FOR 2026"
    ]
    # Repeat and vary for 100 scenes
    full_list = []
    for i in range(100):
        topic = base_scenes[i % 10]
        full_list.append({
            "num": i + 1,
            "text": f"SCENE {i+1}: {topic} - DEEP ANALYSIS PHASE {i//10 + 1}",
            "prompt": f"Korean economic documentary, {topic}, cinematic 8k, photorealistic"
        })
    return full_list

def generate_image(scene):
    payload = {
        "prompt": f"{scene['prompt']}, masterpiece, professional documentary style",
        "steps": 20, "width": 1024, "height": 576, "sampler_name": "Euler a"
    }
    try:
        r = requests.post(FORGE_URL, json=payload, timeout=120)
        img_path = os.path.join(OUTPUT_DIR, f"scene_{scene['num']:03d}.png")
        with open(img_path, 'wb') as f:
            f.write(base64.b64decode(r.json()['images'][0]))
        return img_path
    except:
        return None

def assemble_video(scene_count):
    # Assemble whatever is ready
    cmd = [FFMPEG, "-y"]
    filter_complex = []
    for i in range(scene_count):
        img_path = os.path.join(OUTPUT_DIR, f"scene_{i+1:03d}.png")
        if os.path.exists(img_path):
            cmd.extend(["-loop", "1", "-t", "9", "-i", img_path])
            text = f"ANALYSIS SCENE {i+1}".replace(":", "\\:")
            filter_complex.append(f"[{i}:v]drawtext=fontfile='{FONT_PATH}':text='{text}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-100:enable='between(t,0,9)'[v{i}]")
    
    concat_str = "".join([f"[v{i}]" for i in range(scene_count)]) + f"concat=n={scene_count}:v=1:a=0[outv]"
    cmd.extend(["-filter_complex", ";".join(filter_complex) + ";" + concat_str, "-map", "[outv]", "-c:v", "libx264", "-preset", "ultrafast", os.path.join(OUTPUT_DIR, "FINAL_MASTERPIECE_DRAFT.mp4")])
    subprocess.run(cmd)

if __name__ == "__main__":
    all_scenes = get_full_scenes()
    for i in range(0, 100, 10): # Process in batches of 10
        print(f"Processing Batch {i//10 + 1}/10...")
        for j in range(i, i+10):
            generate_image(all_scenes[j])
        print(f"Batch {i//10 + 1} complete. Current progress: {i+10}%")
        # Optional: Intermediate assembly
        assemble_video(i+10)
