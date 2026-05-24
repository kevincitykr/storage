import os
from modules.llm_brain import LLMBrain
from modules.media_service import MediaService
from modules.moviepy_renderer import MoviepyRenderer
from config import OUTPUT_DIR

def run_orchestrator(topic):
    print(f"--- '{topic}' 주제로 자동화 프로세스 시작 ---")
    
    # 1. 계획 수립 (Gemma)
    plan = LLMBrain.generate_plan(topic)
    print(f"계획 수립 완료: {plan['title']}")
    
    # 2. 씬 데이터 수집 (최소 40개 씬 강제 확보)
    rendered_scenes = []
    base_scenes = plan.get('scenes', [])
    
    # 씬이 부족하면 40개가 될 때까지 반복해서 채움
    total_needed = 40
    for i in range(total_needed):
        scene = base_scenes[i % len(base_scenes)] if base_scenes else {"script": "Analysis continues...", "visual_prompt": "Economy background"}
        
        # 오디오 에셋 (여기서는 시뮬레이션)
        audio_path = os.path.join(OUTPUT_DIR, f"audio_{i}.mp3")
        
        # 비주얼 에셋 (생성한 2개 이미지를 번갈아 사용)
        asset_name = "platform_trap.png" if i % 2 == 0 else "inflation_chart.png"
        visual_path = os.path.join(r"c:\Users\admin\Documents\Sync\Kevincity Share\700 Connect AI\AI_Director_Prototype\opal_assets", asset_name)
        
        rendered_scenes.append({
            "visual_path": visual_path,
            "audio_path": audio_path
        })
    
    # 3. 직접 렌더링 시작 (고정 파일명)
    output_filename = "logeconomy_premium_10min.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    MoviepyRenderer.render(rendered_scenes, output_path)
    
    print(f"\n--- 모든 공정 완료! 영상 파일 확인: {output_path} ---")

if __name__ == "__main__":
    target_topic = "플랫폼 구독료 인상의 실체와 자본주의 함정"
    run_orchestrator(target_topic)
