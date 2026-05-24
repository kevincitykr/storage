import os
import subprocess

FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
BG_IMG = r"C:\Users\ksohw\.gemini\antigravity\brain\bbee1948-81d6-45fa-bc2e-a2ed6291dd81\melodist_masterpiece_final_perfection_v9_1778768514551.png"
AUDIO = r"D:\Kevincity Share\004_melodist_seoul\01_RAW_AUDIO\Morning Pop\Song1_Champagne_Opening.mp3"
OUTPUT = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\ECON_BREAKING_PROTOTYPE.mp4"

# Subtitles based on the latest news (escaping colons for FFmpeg)
subtitles = [
    "2026 EMERGENCY REPORT\\: SAMSUNG ELECTRONICS STRIKE CRISIS",
    "KOSPI NEAR 8000\\: GLOBAL SMART MONEY FLOCKING TO KOREA",
    "REAL ESTATE ALERT\\: JEONSE PRICE SURGE TRIGGERING SALE PRICE HIKE",
    "100 TRILLION WON LOSS RISK? THE FATE OF SEMICONDUCTOR GIANTS"
]

# Simple drawtext filter for proof of concept
drawtext_filters = []
font_path = "C\\:/Windows/Fonts/arial.ttf"
for i, text in enumerate(subtitles):
    start = i * 15
    end = (i + 1) * 15
    f = f"drawtext=fontfile='{font_path}':text='{text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-150:enable='between(t,{start},{end})'"
    drawtext_filters.append(f)

filter_str = ",".join(drawtext_filters)

cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-i", BG_IMG,
    "-i", AUDIO,
    "-vf", filter_str,
    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "60", "-shortest", OUTPUT
]

subprocess.run(cmd, check=True)
print(f"SUCCESS: {OUTPUT} created.")
