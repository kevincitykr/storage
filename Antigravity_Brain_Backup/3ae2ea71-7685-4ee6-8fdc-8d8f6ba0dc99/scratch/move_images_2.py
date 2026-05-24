import shutil
import os

src_dir = r"C:\Users\ksohw\.gemini\antigravity\brain\3ae2ea71-7685-4ee6-8fdc-8d8f6ba0dc99"
dst_dir = r"D:\20260412 kevincity share\004_melodist_seoul\Shared_Assets\Backgrounds"

files = [
    "sunny_reading_nook_1777502149240.png",
    "pink_cherry_blossoms_1777502163179.png",
    "ocean_view_balcony_1777502178628.png",
    "cute_lofi_bedroom_1777502196059.png",
    "green_forest_path_1777502212469.png"
]

for f in files:
    src = os.path.join(src_dir, f)
    dst = os.path.join(dst_dir, f)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {f} to {dst_dir}")
    else:
        print(f"File not found: {src}")
