import os
from moviepy import ImageClip, AudioFileClip, ColorClip, CompositeVideoClip, concatenate_videoclips

class MoviepyRenderer:
    @staticmethod
    def render(scenes, output_path):
        """씬 리스트를 받아서 줌 효과와 고화질이 포함된 MP4 영상으로 렌더링"""
        from moviepy import ColorClip, ImageClip, concatenate_videoclips
        import numpy as np

        def zoom_in_effect(clip, zoom_ratio=0.04):
            """이미지에 부드러운 줌인 효과 추가"""
            def effect(get_frame, t):
                img = get_frame(t)
                h, w = img.shape[:2]
                new_w = int(w * (1 + zoom_ratio * (t / clip.duration)))
                new_h = int(h * (1 + zoom_ratio * (t / clip.duration)))
                
                # Resize and crop to center
                import cv2
                resized = cv2.resize(img, (new_w, new_h))
                start_x = (new_w - w) // 2
                start_y = (new_h - h) // 2
                return resized[start_y:start_y+h, start_x:start_x+w]
            
            return clip.transform(effect)

        clips = []
        for i, scene in enumerate(scenes):
            visual_path = scene['visual_path']
            duration = 15.0 
            
            if os.path.exists(visual_path):
                # 줌인 효과 적용
                clip = ImageClip(visual_path).with_duration(duration)
                try:
                    clip = zoom_in_effect(clip)
                except Exception:
                    clip = clip.resized(height=720) # OpenCV 실패 시 기본 리사이즈
            else:
                clip = ColorClip(size=(1280, 720), color=(73, 109, 137)).with_duration(duration)
            
            clips.append(clip)
        
        final_clip = concatenate_videoclips(clips, method="compose")
        # 비트레이트를 8000k로 대폭 상향 (고화질 증명)
        final_clip.write_videofile(output_path, fps=24, codec="libx264", bitrate="8000k", threads=4)
        print(f"고화질 프리미엄 렌더링 완료: {output_path}")
