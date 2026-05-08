import os
from modules.llm_brain import LLMBrain
from modules.media_service import MediaService
from modules.capcut_engine import CapCutEngine
from config import OUTPUT_DIR, CAPCUT_DRAFTS_DIR

def run_orchestrator(topic):
    print(f"--- '{topic}' 주제로 자동화 프로세스 시작 ---")
    
    # 1. 계획 수립 (Gemma)
    plan = LLMBrain.generate_plan(topic)
    print(f"계획 수립 완료: {plan['title']}")
    
    # 2. 프로젝트 폴더 설정
    project_path = os.path.join(CAPCUT_DRAFTS_DIR, plan['title'].replace(" ", "_"))
    engine = CapCutEngine(project_path)
    engine.create_empty_draft(plan['title'])
    
    # 3. 각 씬별 제작 및 배치
    for i, scene in enumerate(plan['scenes']):
        print(f"\n[Scene {i+1}] 제작 중...")
        
        # 음성 생성
        audio_path = MediaService.generate_tts(scene['script'], f"audio_{i}.mp3")
        
        # 이미지 생성
        image_path = MediaService.generate_image(scene['visual_prompt'], f"image_{i}.png")
        
        # 캡컷 엔진으로 배치
        engine.add_media_to_track(audio_path, "audio")
        engine.add_media_to_track(image_path, "video")
    
    print("\n--- 모든 공정 완료! 캡컷에서 프로젝트를 확인하세요. ---")

if __name__ == "__main__":
    target_topic = "AI가 바꾸는 미래의 일자리"
    run_orchestrator(target_topic)
