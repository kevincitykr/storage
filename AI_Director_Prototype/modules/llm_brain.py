import requests
import json
from config import OLLAMA_MODEL, OLLAMA_BASE_URL

class LLMBrain:
    @staticmethod
    def generate_plan(topic):
        """주제에 따른 영상 제작 계획 생성"""
        prompt = f"""
        You are a 20-year Veteran Economic Journalist running the 'LogEconomy(@LogEconomy_KR)' YouTube channel. 
        Topic: {topic}
        
        [STORYTELLING RULES]
        1. INVESTIGATIVE TONE: Start with a hard-hitting question about common people's financial struggle.
        2. STRUCTURAL ANALYSIS: Explain 'Streamflation' and how platforms (Kakao, Coupang, Baemin) are locking users in to raise prices.
        3. LONG-FORM: Generate 40 detailed scenes (10-15s each) to fill a 10-minute professional documentary.
        4. DATA-DRIVEN: Use specific percentages and industry terminology (Lock-in effect, ARPU, Churn rate).

        [OUTPUT REQUIREMENT]
        Output ONLY the JSON structure.
        
        Provide the result in JSON format:
        {{
            "title": "Platform_Subscription_Trap_LogEconomy",
            "scenes": [ ... ]
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
