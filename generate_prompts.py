import json
import urllib.request
import os

# 설정 파일 경로
ORDER_FILE = "gemma_production_order.json"
OUTPUT_FILE = "production_output.json"
# LM Studio API 설정 (OpenAI 호환)
API_URL = "http://localhost:1234/v1/chat/completions"

def call_llm(model, prompt):
    data = {
        "model": model, # LM Studio에서는 로드된 모델을 자동으로 사용함
        "messages": [
            {"role": "system", "content": "You are a professional visual prompt engineer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(
            API_URL, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as res:
            response = json.loads(res.read().decode('utf-8'))
            return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error connecting to LM Studio: {str(e)}"

def main():
    print(f"[*] Reading production order from {ORDER_FILE}...")
    if not os.path.exists(ORDER_FILE):
        print(f"[!] Error: {ORDER_FILE} not found.")
        return

    with open(ORDER_FILE, "r", encoding="utf-8") as f:
        order = json.load(f)

    role = order.get("actor_role", "Visual Production Director")
    protocol = order.get("production_protocol", {})
    scenes = order.get("scene_storyboard", [])
    
    # 공통 스타일 가이드 추출
    style = protocol.get("step_2_visual_consistency_locking", {})
    style_desc = f"""
    Art Style: {style.get('art_style')}
    Lighting: {style.get('lighting_schema')}
    Character: {style.get('character_profile')}
    Mandatory Elements: {', '.join(style.get('mandatory_elements', []))}
    """

    results = []
    print(f"[*] Starting production with model: e2b")

    for scene in scenes:
        scene_id = scene.get("id")
        desc = scene.get("description")
        emotion = scene.get("emotion")
        
        print(f"[*] Generating prompt for Scene {scene_id} ({emotion})...")
        
        full_prompt = f"""
        Role: {role}
        Instructions: {protocol.get('step_3_prompt_generation')}
        
        Contextual Grounding: {protocol.get('step_1_contextual_grounding')}
        Visual Style Guide: {style_desc}
        
        Specific Scene to generate:
        ID: {scene_id}
        Description: {desc}
        Emotion: {emotion}
        
        Generate ONLY the prompt string starting with 'An oil painting masterpiece...'. Do not include any other text.
        """
        
        response = call_llm("gemma-4-e4b", full_prompt)
        results.append({
            "id": scene_id,
            "original_description": desc,
            "generated_prompt": response.strip()
        })

    # 결과 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Production completed! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
