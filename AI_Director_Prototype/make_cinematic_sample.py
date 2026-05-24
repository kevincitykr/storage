import requests
import base64
import os
import subprocess

# Paths
FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FORGE_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"
SAMPLE_DIR = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\cinematic_sample"
if not os.path.exists(SAMPLE_DIR): os.makedirs(SAMPLE_DIR)
FONT_PATH = "C\\:/Windows/Fonts/batang.ttc" # Use a more classic serif font for economy

def gen_img(num, prompt):
    payload = {
        "prompt": f"Korean economic documentary cinematic style, {prompt}, masterpiece, 8k, photorealistic, dramatic lighting",
        "steps": 30, "width": 1280, "height": 720, "sampler_name": "Euler a"
    }
    r = requests.post(FORGE_URL, json=payload)
    path = os.path.join(SAMPLE_DIR, f"s{num}.png")
    with open(path, 'wb') as f:
        f.write(base64.b64decode(r.json()['images'][0]))
    return path

# 1. Generate 5 unique cinematic images
print("Generating 5 unique cinematic images...")
gen_img(1, "close up of a cracked semiconductor wafer with Samsung logo, red emergency lighting")
gen_img(2, "empty dark high-tech factory floor, single red warning light, misty atmosphere")
gen_img(3, "global map hologram with breaking red supply chain lines, glitch effect")
gen_img(4, "Yeouido skyline at night with a giant golden holographic '8000' rising above clouds")
gen_img(5, "Close up of a wise Korean senior in suit, holding a glowing tablet with rising charts")

# 2. Assemble with Ken Burns effect (Zoom) and better text
print("Assembling with cinematic motion...")
cmd = [FFMPEG, "-y"]
for i in range(1, 6):
    cmd.extend(["-loop", "1", "-t", "5", "-i", os.path.join(SAMPLE_DIR, f"s{i}.png")])

texts = [
    "2026: THE FALL OF SAMSUNG'S EMPIRE?",
    "A SILENT CRISIS IN THE SEMICONDUCTOR HEART",
    "GLOBAL SUPPLY CHAINS ARE BREAKING APART",
    "THE KOSPI 8000 PARADOX: WEALTH REBORN",
    "THE LAST SURVIVAL STRATEGY FOR SENIORS"
]

filter_parts = []
for i in range(5):
    # Zoom in effect + Drawtext with a background box for premium feel
    txt = texts[i].replace(":", "\\:").replace("'", "")
    filter_parts.append(f"[{i}:v]scale=2560:-1,zoompan=z='min(zoom+0.001,1.1)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720,drawtext=fontfile='{FONT_PATH}':text='{txt}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=h-120:box=1:boxcolor=black@0.5:boxborderw=10[v{i}]")

concat = "".join([f"[v{i}]" for i in range(5)]) + "concat=n=5:v=1:a=0[outv]"
cmd.extend(["-filter_complex", ";".join(filter_parts) + ";" + concat, "-map", "[outv]", "-c:v", "libx264", "-pix_fmt", "yuv420p", os.path.join(SAMPLE_DIR, "CINEMATIC_REBORN.mp4")])

subprocess.run(cmd, check=True)
print("CINEMATIC SAMPLE COMPLETE.")
