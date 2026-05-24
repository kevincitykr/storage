"""
공통 유틸리티 함수 모듈
모든 execution 스크립트에서 사용할 수 있는 헬퍼 함수들
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
TMP_DIR = PROJECT_ROOT / ".tmp"


def ensure_tmp_dir():
    """임시 디렉토리가 존재하는지 확인하고 없으면 생성"""
    TMP_DIR.mkdir(exist_ok=True)
    return TMP_DIR


def get_env(key: str, default: str = None) -> str:
    """환경 변수 가져오기"""
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"환경 변수 '{key}'가 설정되지 않았습니다.")
    return value


def save_json(data: dict, filename: str, to_tmp: bool = True) -> Path:
    """JSON 파일로 저장"""
    if to_tmp:
        ensure_tmp_dir()
        filepath = TMP_DIR / filename
    else:
        filepath = PROJECT_ROOT / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filepath


def load_json(filename: str, from_tmp: bool = True) -> dict:
    """JSON 파일 로드"""
    if from_tmp:
        filepath = TMP_DIR / filename
    else:
        filepath = PROJECT_ROOT / filename
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def log(message: str, level: str = "INFO"):
    """간단한 로깅 함수"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


# 히스토리 파일 경로
HISTORY_FILE = PROJECT_ROOT / ".history.json"


def load_history() -> list:
    """사용된 주제 히스토리 로드"""
    if not HISTORY_FILE.exists():
        return []
    try:
        return load_json(".history.json", from_tmp=False)
    except Exception:
        return []


def save_to_history(topic: str):
    """주제를 히스토리에 추가"""
    history = load_history()
    if topic not in history:
        history.append(topic)
        # 최근 100개만 유지
        if len(history) > 100:
            history = history[-100:]
        
        save_json(history, ".history.json", to_tmp=False)
        log(f"히스토리 추가됨: {topic}")


def generate_image(prompt: str, output_path: Path, model: str = "flux") -> bool:
    """고품질 AI 이미지 생성 (Pollinations.ai / Stable Diffusion)"""
    import requests
    import urllib.parse
    import time
    
    # 캐싱 로직 제거: 항상 새로 생성
    # if output_path.exists() and output_path.stat().st_size > 0:
    #     return True
        
    log(f"AI 이미지 생성 중 ({model}): {prompt[:50]}...")
    
    try:
        # Prompt 최적화
        # 품질 보정 및 부작용(기구한 손, 텍스트) 방지를 위한 키워드 추가
        quality_boost = ", high quality, photorealistic, 8k, highly detailed, anatomically correct, perfect hands, five fingers, no text, no letters, no watermark, no distorted faces, cinematic lighting, distinct Korean face, East Asian features"
        full_prompt = prompt + quality_boost
        encoded_prompt = urllib.parse.quote(full_prompt)
        
        # 1080x1920 세로 비율
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&seed={int(time.time())}&model={model}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            # 파일 유효성 검사
            if os.path.getsize(output_path) > 1024: # 1KB 이상
                log(f"이미지 생성 성공: {output_path}")
                return True
        
        log(f"이미지 생성 응답 오류: {response.status_code}", "WARNING")
        return False
        
    except Exception as e:
        log(f"이미지 생성 실패: {e}", "ERROR")
        return False


if __name__ == "__main__":
    # 모듈 테스트
    log("유틸리티 모듈이 정상적으로 로드되었습니다.")
    print(f"프로젝트 루트: {PROJECT_ROOT}")
    print(f"임시 디렉토리: {ensure_tmp_dir()}")
