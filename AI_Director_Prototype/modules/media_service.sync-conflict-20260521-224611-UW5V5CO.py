import requests
import os
from config import ELEVENLABS_API_KEY, OPENAI_API_KEY, OUTPUT_DIR

class MediaService:
    @staticmethod
    def get_asset(scene, i):
        """Opal Agent 에셋이 있으면 사용하고, 없으면 생성"""
        opal_dir = os.path.join(os.path.dirname(OUTPUT_DIR), "opal_assets")
        asset_name = scene.get('asset_name', f"scene_{i}.png")
        opal_path = os.path.join(opal_dir, asset_name)
        
        if os.path.exists(opal_path):
            print(f"[Opal Agent] 에셋 발견: {asset_name}")
            return opal_path
        
        # 에셋이 없으면 기존 생성 로직 호출
        if ".mp3" in asset_name:
            return MediaService.generate_tts(scene['script'], asset_name)
        else:
            return MediaService.generate_image(scene['visual_prompt'], asset_name)

    @staticmethod
    def generate_tts(text, filename="voice.mp3"):
        """ElevenLabs를 통한 TTS 생성 (더미 구현 포함)"""
        if ELEVENLABS_API_KEY == "YOUR_ELEVENLABS_API_KEY":
            print(f"[MOCK] TTS 생성 시뮬레이션: {text[:30]}...")
            return os.path.join(OUTPUT_DIR, filename)
        
        # 실제 API 호출 로직 (예시)
        # url = "https://api.elevenlabs.io/v1/text-to-speech/voice_id"
        # headers = {"xi-api-key": ELEVENLABS_API_KEY}
        # ... 
        pass

    @staticmethod
    def generate_image(prompt, filename="image.png"):
        """Pillow를 사용하여 텍스트가 포함된 플레이스홀더 이미지 생성"""
        from PIL import Image, ImageDraw, ImageFont
        
        path = os.path.join(OUTPUT_DIR, filename)
        img = Image.new('RGB', (1280, 720), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # 텍스트 삽입 (한글 폰트가 없을 경우를 대비해 기본 폰트 사용)
        text = f"Scene Prompt: {prompt[:50]}..."
        d.text((100, 300), text, fill=(255, 255, 0))
        
        img.save(path)
        print(f"[SYSTEM] 플레이스홀더 이미지 생성됨: {filename}")
        return path
