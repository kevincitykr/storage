"""
시니어 휴먼 드라마 전자동 영상 합성 모듈
100장의 이미지 생성 및 5개 챕터 오디오 합성하여 최종 MP4 생성
"""

import json
import sys
import os
import time
import asyncio
from pathlib import Path

# 프로젝트 루트 설정
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "execution"))

from _utils import ensure_tmp_dir, load_json, log, TMP_DIR, generate_image

# 라이브러리 로드
try:
    from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
except ImportError:
    try:
        from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
    except ImportError:
        log("moviepy 설치가 필요합니다.", "ERROR")
        sys.exit(1)

def generate_tts_sync(text: str, output_path: Path):
    """Edge-TTS를 사용하여 동기 방식으로 TTS 생성"""
    try:
        import edge_tts
        # 목소리 변경: ko-KR-InJoonNeural (남성 톤)
        communicate = edge_tts.Communicate(text, "ko-KR-InJoonNeural")
        asyncio.run(communicate.save(str(output_path)))
        return True
    except Exception as e:
        log(f"TTS 생성 실패: {e}", "ERROR")
        return False

def main(test_mode: bool = False):
    log("=== 시니어 휴먼 드라마 전자동 합성 시작 ===")
    
    try:
        drama_data = load_json('drama_script.json')
    except:
        log("drama_script.json 파일을 찾을 수 없습니다.", "ERROR")
        return False

    # 이미지 저장 폴더 생성
    image_dir = TMP_DIR / "drama_images"
    image_dir.mkdir(exist_ok=True)
    
    chapter_clips = []
    
    total_chapters = drama_data.get('total_chapters', 0)
    log(f"총 {total_chapters}개 챕터 처리 시작 (챕터당 1장 이미지 생성)")

    for ch_idx, chapter in enumerate(drama_data.get('chapters', [])):
        ch_num = chapter.get('chapter_number')
        log(f"\n[챕터 {ch_num}/5] 합성 중: {chapter.get('title')}")
        
        # 1. 오디오 생성
        audio_path = TMP_DIR / f"ch_{ch_num}_audio.mp3"
        if not generate_tts_sync(chapter.get('narration', ""), audio_path):
            continue
            
        audioclip = AudioFileClip(str(audio_path))
        duration = audioclip.duration
        
        # 2. 이미지 생성 및 클립 구성 (사용자 요청: 5장 이내, 고품질, 특정 장면)
        # 챕터별 프롬프트 리스트 로드
        prompts = chapter.get('image_prompts', [])
        if not prompts:
             # 하위 호환성: image_prompt가 단일 문자열인 경우
             single_prompt = chapter.get('image_prompt', "A cinematic drama scene.")
             prompts = [single_prompt]

        # 이미지당 지속 시간 계산
        num_images = len(prompts)
        if num_images == 0:
            log("이미지 프롬프트가 없습니다. 스킵합니다.", "WARNING")
            continue
            
        img_duration = duration / num_images
        
        img_clips = []
        for img_idx, prompt in enumerate(prompts):
            img_filename = f"ch_{ch_num}_img_{img_idx}.jpg"
            img_path = image_dir / img_filename
            
            # 이미지 생성 시도 (이미 존재하면 스킵)
            success = False
            if not img_path.exists():
                for attempt in range(2): # 2번 시도
                    log(f"  - 이미지 {img_idx+1}/{num_images} 생성 중... (시도 {attempt+1})", "INFO")
                    # 프롬프트 강화
                    full_prompt = f"{prompt}, cinematic lighting, high resolution, 4k, photorealistic, korean drama style"
                    if generate_image(full_prompt, img_path):
                        success = True
                        break
                    
                    # Rate Limit 방지를 위한 대기
                    log(f"  - 대기 중...", "INFO")
                    time.sleep(5)
                
                if not success:
                    log(f"  - 이미지 생성 실패, 기본 배경 생성", "WARNING")
                    # 기본 배경 생성 (Pillow)
                    try:
                        from PIL import Image
                        color = (50, 50, 70) # RGB tuple
                        dummy_img = Image.new('RGB', (1080, 1920), color=color)
                        dummy_img.save(img_path)
                    except Exception as e:
                        log(f"  - 기본 이미지 생성 실패: {e}", "ERROR")
            
            if img_path.exists():
                try:
                    # MoviePy 버전 호환성 처리
                    try:
                        img_clip = ImageClip(str(img_path)).with_duration(img_duration)
                    except AttributeError:
                        img_clip = ImageClip(str(img_path)).set_duration(img_duration)
                    img_clips.append(img_clip)
                except Exception as e:
                    log(f"이미지 클립 생성 실패: {e}", "ERROR")

            # 테스트 모드 시 챕터당 이미지는 1장만 처리하고 넘어갈 수도 있으나,
            # 멀티 이미지 테스트를 위해 다 하거나 제한을 둠
            if test_mode and img_idx >= 1:
                break
        
        if img_clips:
            # 이미지 클립들을 하나로 합치고 오디오 입히기
            try:
                chapter_video_visual = concatenate_videoclips(img_clips, method="compose")
                try:
                    chapter_video = chapter_video_visual.with_audio(audioclip)
                except AttributeError:
                    chapter_video = chapter_video_visual.set_audio(audioclip)
                
                chapter_clips.append(chapter_video)
                log(f"  [성공] 챕터 {ch_num} 클립 생성 완료 (이미지 {len(img_clips)}장)")
            except Exception as e:
                log(f"  [실패] 챕터 {ch_num} 영상 합성 중 에러: {e}", "ERROR")
        
        # 테스트 모드 시 첫 챕터만 처리
        if test_mode:
            log("테스트 모드: 첫 챕터 처리 후 중단")
            break

    # 3. 최종 영상 병합
    if chapter_clips:
        log("\n=== 최종 영상 병합 중... ===")
        final_video = concatenate_videoclips(chapter_clips, method="compose")
        # 출력 파일명 변경: output_drama_video.mp4
        output_path = TMP_DIR / "output_drama_video.mp4"
        final_video.write_videofile(str(output_path), fps=24, preset='ultrafast', threads=4, logger=None)
        
        log(f"\n✨ 전자동 합성 완료!")
        log(f"🎬 최종 영상: {output_path}")
        log(f"🖼️ 생성된 이미지들: {image_dir}")
        return True
    else:
        log("영상 클립이 생성되지 않았습니다.", "ERROR")
        return False

if __name__ == "__main__":
    # 직접 실행 시 테스트 모드 옵션 지원
    test = "--test" in sys.argv
    main(test_mode=test)
