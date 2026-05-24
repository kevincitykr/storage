import os
import json
from pathlib import Path
from datetime import datetime

# 상수 정의
# 이 파일은 execution 폴더에 있으므로, parent는 legacy_project
PROJECT_ROOT = Path(__file__).parent.parent
TMP_DIR = PROJECT_ROOT / ".tmp"

def ensure_tmp_dir():
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    return TMP_DIR

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def load_json(filename):
    # 1. 현재 작업 디렉토리에서 찾기
    path = Path.cwd() / filename
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    # 2. scripts 폴더에서 찾기
    path = PROJECT_ROOT / "scripts" / filename
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    raise FileNotFoundError(f"Could not find json file: {filename}")

def generate_image(prompt, output_path):
    """
    이미지 생성 함수.
    실제 생성 API가 없으므로 False를 반환하여
    호출하는 쪽(create_drama_video.py)에서 기본 이미지(Dummy)를 생성하도록 유도함.
    """
    log(f"[Mock] 이미지 생성 요청: {prompt[:30]}...", "DEBUG")
    # False를 반환하면 메인 스크립트가 Pillow로 더미 이미지를 생성함
    return False
