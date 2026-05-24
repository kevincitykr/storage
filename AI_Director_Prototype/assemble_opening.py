import os
import subprocess

FFMPEG = r"C:\Users\ksohw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
INPUT_DIR = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\production"
OUTPUT = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\ECON_FULL_OP_PREVIEW.mp4"
FONT_PATH = "C\\:/Windows/Fonts/arial.ttf"

scenes = [
    "2026 EMERGENCY REPORT: THE KOREAN ECONOMY AT A CROSSROADS",
    "SAMSUNG STRIKE: 100 TRILLION WON AT RISK",
    "GLOBAL SUPPLY CHAIN COLLAPSE WARNING",
    "KOSPI 8000: THE GREATEST PARADOX",
    "US SMART MONEY FLOCKING TO KOREA",
    "REAL ESTATE: THE 3-9 MONTH RULE",
    "JEONSE PRICE SURGE TRIGGERING SALE PRICE HIKE",
    "THE LAST OPPORTUNITY FOR ASSET GROWTH",
    "SAMSUNG'S RECOVERY OR DECLINE?",
    "STAY TUNED FOR THE FULL REPORT"
]

# Build filter complex for sequence of images with subtitles
filter_complex = []
for i in range(10):
    start = i * 5
    end = (i + 1) * 5
    text = scenes[i].replace(":", "\\:").replace("'", "").replace(",", "\\,")
    # Drawtext on each input
    filter_complex.append(f"[{i}:v]drawtext=fontfile='{FONT_PATH}':text='{text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-150:enable='between(t,0,5)'[v{i}]")

# Concatenate videos
concat_str = "".join([f"[v{i}]" for i in range(10)]) + f"concat=n=10:v=1:a=0[outv]"

cmd = [FFMPEG, "-y"]
for i in range(10):
    cmd.extend(["-loop", "1", "-t", "5", "-i", os.path.join(INPUT_DIR, f"scene_{i+1:03d}.png")])

cmd.extend(["-filter_complex", ";".join(filter_complex) + ";" + concat_str, "-map", "[outv]", "-c:v", "libx264", "-preset", "ultrafast", OUTPUT])

subprocess.run(cmd, check=True)
print(f"SUCCESS: {OUTPUT} created.")
