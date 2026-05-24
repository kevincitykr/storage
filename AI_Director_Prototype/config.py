import os

# API Keys (사용자가 직접 채워넣어야 함)
ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# 로컬 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CAPCUT_DRAFTS_DIR = os.path.join(os.environ.get('LOCALAPPDATA', ''), "CapCut", "User Data", "Projects", "com.lveditor.draft")

# 디렉토리 생성
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Ollama 설정
OLLAMA_MODEL = "gemma:7b" # 또는 사용 중인 모델명
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
