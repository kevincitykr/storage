import requests
import base64
import os
import json
import subprocess

# Paths
FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FORGE_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"
SCRIPT_PATH = r"C:\Users\ksohw\.gemini\antigravity\brain\bbee1948-81d6-45fa-bc2e-a2ed6291dd81\full_economic_documentary_script.md"
OUTPUT_DIR = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\production"
if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

def generate_scene_image(scene_num, visual_prompt):
    payload = {
        "prompt": f"Korean economic documentary style, {visual_prompt}, cinematic lighting, photorealistic, 8k",
        "steps": 20, "width": 1024, "height": 576, "sampler_name": "Euler a"
    }
    r = requests.post(FORGE_URL, json=payload)
    img_path = os.path.join(OUTPUT_DIR, f"scene_{scene_num:03d}.png")
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(r.json()['images'][0]))
    return img_path

# Dummy script parsing for first 10 scenes to start fast
scenes = [
    {"num": 1, "text": "2026 EMERGENCY REPORT: THE KOREAN ECONOMY AT A CROSSROADS", "prompt": "Samsung headquarters in Seoul with dramatic red sunset"},
    {"num": 2, "text": "SAMSUNG STRIKE: 100 TRILLION WON AT RISK", "prompt": "Samsung semiconductor factory with warning signs"},
    {"num": 3, "text": "GLOBAL SUPPLY CHAIN COLLAPSE WARNING", "prompt": "Digital world map with red supply chain lines"},
    {"num": 4, "text": "KOSPI 8000: THE GREATEST PARADOX", "prompt": "Glowing KOSPI 8000 numbers over Yeouido buildings"},
    {"num": 5, "text": "US SMART MONEY FLOCKING TO KOREA", "prompt": "Golden money flowing into Korea map"},
    {"num": 6, "text": "REAL ESTATE: THE 3-9 MONTH RULE", "prompt": "Luxury apartments along Han river at sunset"},
    {"num": 7, "text": "JEONSE PRICE SURGE TRIGGERING SALE PRICE HIKE", "prompt": "Rising real estate price chart overlay"},
    {"num": 8, "text": "THE LAST OPPORTUNITY FOR ASSET GROWTH", "prompt": "Dignified Korean senior man looking at data"},
    {"num": 9, "text": "SAMSUNG'S RECOVERY OR DECLINE?", "prompt": "Samsung logo and stock chart trending down then up"},
    {"num": 10, "text": "STAY TUNED FOR THE FULL REPORT", "prompt": "Cinematic newsroom background"}
]

print("Starting production of first 10 scenes...")
for scene in scenes:
    img = generate_scene_image(scene['num'], scene['prompt'])
    print(f"Generated {img}")

print("Production phase 1 complete. Ready for FFmpeg assembly.")
