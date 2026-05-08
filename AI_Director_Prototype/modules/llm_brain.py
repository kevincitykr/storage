import requests
import json
from config import OLLAMA_MODEL, OLLAMA_BASE_URL

class LLMBrain:
    @staticmethod
    def generate_plan(topic):
        """주제에 따른 영상 제작 계획 생성"""
        prompt = f"""
        You are an AI YouTube Director. Create a production plan for the following topic:
        Topic: {topic}
        
        Provide the result in JSON format:
        {{
            "title": "video title",
            "scenes": [
                {{"script": "voiceover text", "visual_prompt": "image generation prompt"}},
                ...
            ]
        }}
        """
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            response = requests.post(OLLAMA_BASE_URL, json=payload)
            result = response.json()
            return json.loads(result['response'])
        except Exception as e:
            print(f"Ollama 연동 에러: {e}")
            # 폴백용 샘플 데이터
            return {
                "title": f"Sample: {topic}",
                "scenes": [
                    {"script": "안녕하세요. 오늘은 AI 자동화에 대해 알아봅니다.", "visual_prompt": "Futuristic AI city"}
                ]
            }
