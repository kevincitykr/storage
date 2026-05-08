import os
import json
import random
from moviepy.editor import (
    VideoClip, AudioFileClip, ImageClip, TextClip, 
    CompositeVideoClip, ColorClip
)
from moviepy.video.fx.all import resize, crop

def create_video_v2(audio_path, image_folder, subtitle_json, output_path):
    print(f"[*] Starting Video Rendering V2...")
    
    # 1. 오디오 로드
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # 2. 이미지 시퀀스 로드
    image_files = sorted([
        os.path.join(image_folder, f) for f in os.listdir(image_folder) 
        if f.endswith(('.png', '.jpg', '.jpeg'))
    ])
    
    if not image_files:
        raise Exception("No images found in the sequence folder!")
    
    # 3. 자막 데이터 로드
    with open(subtitle_json, "r", encoding="utf-8") as f:
        subtitles = json.load(f)
        
    # 4. 이미지 배치 (이미지 개수에 맞춰 균등하게 배분하거나 자막 세그먼트에 맞춤)
    clips = []
    num_images = len(image_files)
    time_per_image = duration / num_images
    
    for i, img_path in enumerate(image_files):
        start_t = i * time_per_image
        end_t = (i + 1) * time_per_image
        if i == num_images - 1: end_t = duration
        
        img_clip = ImageClip(img_path).set_duration(end_t - start_t).set_start(start_t)
        
        # Ken Burns 효과 (서서히 줌인)
        img_clip = img_clip.resize(lambda t: 1 + 0.05 * (t / img_clip.duration))
        img_clip = img_clip.set_position(('center', 'center'))
        
        clips.append(img_clip)
        
    # 5. 자막 클립 생성 (고급 스타일)
    for seg in subtitles:
        txt = seg['text']
        start = seg['start']
        end = seg['end']
        
        # 자막 클립 (그림자, 폰트, 크기 설정)
        txt_clip = TextClip(
            txt, 
            fontsize=50, 
            color='white', 
            font='Arial-Bold', # 시스템에 설치된 폰트 사용
            stroke_color='black', 
            stroke_width=2,
            method='caption',
            size=(1080 * 0.8, None)
        ).set_start(start).set_end(end).set_position(('center', 0.8), relative=True)
        
        clips.append(txt_clip)
        
    # 6. 최종 합성 및 렌더링
    video = CompositeVideoClip(clips, size=(1080, 1920)) # 숏폼 비율
    video = video.set_audio(audio)
    
    print(f"[*] Rendering to {output_path}...")
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"[+] Rendering complete!")

if __name__ == "__main__":
    # create_video_v2("audio.mp3", "./images", "subtitles.json", "output.mp4")
    pass
