import os
from moviepy.editor import AudioFileClip

tracks_dir = r"D:\20260412 kevincity share\004_melodist_seoul\20260425 Suno_Songs_All"
plan_path = r"D:\20260412 kevincity share\004_melodist_seoul\Suno_Factory_Customize\compilation_plan_a.json"

import json
with open(plan_path, "r", encoding="utf-8") as f:
    plan = json.load(f)

total_duration = 0
for track_name in plan["tracks"]:
    track_path = os.path.join(tracks_dir, track_name)
    if os.path.exists(track_path):
        duration = AudioFileClip(track_path).duration
        print(f"{track_name}: {duration}s")
        total_duration += duration
    else:
        print(f"MISSING: {track_name}")

print(f"\nTOTAL DURATION: {total_duration}s ({total_duration/60:.2f} minutes)")
