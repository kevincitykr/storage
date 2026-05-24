import os
from moviepy.editor import AudioFileClip
import json

tracks_dir = r"D:\20260412 kevincity share\004_melodist_seoul\20260425 Suno_Songs_All"
plan_path = r"D:\20260412 kevincity share\004_melodist_seoul\FINAL_RELEASE\plan_b.json"

with open(plan_path, "r", encoding="utf-8") as f:
    plan = json.load(f)

current_time = 0
print("TRACKLIST:")
for track_name in plan["tracks"]:
    track_path = os.path.join(tracks_dir, track_name)
    if os.path.exists(track_path):
        duration = AudioFileClip(track_path).duration
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        title = track_name.replace("_2.mp3", "").replace("_", " ")
        print(f"{minutes:02d}:{seconds:02d} - {title}")
        current_time += duration
    else:
        print(f"MISSING: {track_name}")
