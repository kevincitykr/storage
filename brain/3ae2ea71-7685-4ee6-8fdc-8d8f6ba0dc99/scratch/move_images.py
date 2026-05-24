import shutil
import os

src_dir = r"C:\Users\ksohw\.gemini\antigravity\brain\3ae2ea71-7685-4ee6-8fdc-8d8f6ba0dc99"
dst_dir = r"D:\20260412 kevincity share\004_melodist_seoul\Shared_Assets\Backgrounds"

files = [
    "bright_morning_cafe_1777476318513.png",
    "pastel_dreamscape_1777476333797.png",
    "fresh_spring_meadow_1777476350444.png"
]

for f in files:
    src = os.path.join(src_dir, f)
    dst = os.path.join(dst_dir, f)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {f} to {dst_dir}")
    else:
        print(f"File not found: {src}")
