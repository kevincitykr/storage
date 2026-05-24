import os
import json
import subprocess

FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
BG_IMG = r"C:\Users\ksohw\.gemini\antigravity\brain\bbee1948-81d6-45fa-bc2e-a2ed6291dd81\melodist_masterpiece_final_perfection_v9_1778768514551.png"
AUDIO = r"D:\Kevincity Share\004_melodist_seoul\01_RAW_AUDIO\Morning Pop\Song1_Champagne_Opening.mp3"
FONT_PATH = "C\\:/Windows/Fonts/arial.ttf"
OUTPUT = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\ECON_SUMMARY_5MIN.mp4"

# Expertly curated 20 scenes based on real-time news
scripts = [
    "2026 EMERGENCY: THE KOREAN ECONOMY AT A CROSSROADS",
    "SAMSUNG ELECTRONICS STRIKE: A 100 TRILLION WON CATASTROPHE?",
    "THE HEART OF GLOBAL SEMICONDUCTORS IS ABOUT TO STOP",
    "KOSPI 8000: THE GREATEST STOCK MARKET PARADOX IN HISTORY",
    "WHY IS GLOBAL SMART MONEY FLOCKING TO THE KOREAN MARKET?",
    "REAL ESTATE ALERT: JEONSE PRICE SURGE AND THE 3-9 MONTH RULE",
    "THE LAST OPPORTUNITY FOR ASSET GROWTH IN 2026?",
    "EXPORT POWERHOUSE IN DANGER: GOVERNMENT'S EMERGENCY MEASURES",
    "NUCLEAR ENERGY EXPORT: THE NEW GROWTH ENGINE FOR KOREA",
    "INTERNATIONAL OIL PRICES AND THE INFLATION TRAP",
    "INTEREST RATES AND THE BURDEN ON THE MIDDLE CLASS",
    "THE RISE OF K-STOCKS: BEYOND THE SEMICONDUCTOR GIANTS",
    "SAMSUNG'S DECISION: RECOVERY OR FURTHER DECLINE?",
    "GLOBAL SUPPLY CHAIN RESTRUCTURING AND KOREA'S ROLE",
    "DIGITAL TRANSFORMATION: THE FUTURE OF THE KOREAN WORKFORCE",
    "RETIREMENT PLANNING IN THE AGE OF KOSPI 8000",
    "HOW TO PROTECT YOUR WEALTH IN VOLATILE TIMES",
    "THE STRATEGIC CHOICE: CASH OR EQUITY?",
    "2026 KOREA: CRISIS IS ANOTHER NAME FOR OPPORTUNITY",
    "STAY TUNED FOR THE FULL 15-MINUTE DEEP DIVE REPORT."
]

drawtext_filters = []
duration_per_scene = 15

for i, script in enumerate(scripts):
    start = i * duration_per_scene
    end = (i + 1) * duration_per_scene
    clean_script = script.replace(":", "\\:").replace("'", "").replace(",", "\\,")
    f = f"drawtext=fontfile='{FONT_PATH}':text='{clean_script}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-150:enable='between(t,{start},{end})'"
    drawtext_filters.append(f)

filter_str = ",".join(drawtext_filters)
total_duration = len(scripts) * duration_per_scene

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
