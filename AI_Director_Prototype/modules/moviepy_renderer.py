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

        from moviepy import TextClip
        
        clips = []
        for i, scene in enumerate(scenes):
            visual_path = scene['visual_path']
            script_text = scene.get('script', '')
            duration = 15.0 
            
            if os.path.exists(visual_path):
                clip = ImageClip(visual_path).with_duration(duration)
                try:
                    clip = zoom_in_effect(clip)
                except Exception:
                    clip = clip.resized(height=720)
            else:
                clip = ColorClip(size=(1280, 720), color=(73, 109, 137)).with_duration(duration)
            
            # 자막 추가 (간단한 오버레이)
            if script_text:
                try:
                    txt_clip = TextClip(
                        text=script_text,
                        font_size=40,
                        color='white',
                        bg_color='black',
                        size=(1100, None),
                        method='caption'
                    ).with_duration(duration).with_position(('center', 600))
                    clip = CompositeVideoClip([clip, txt_clip])
                except Exception as e:
                    print(f"TextClip Error: {str(e)}")
            
            clips.append(clip)
        
        final_clip = concatenate_videoclips(clips, method="compose")
        # 비트레이트를 8000k로 대폭 상향 (고화질 증명)
        final_clip.write_videofile(output_path, fps=24, codec="libx264", bitrate="8000k", threads=4)
        print(f"고화질 프리미엄 렌더링 완료: {output_path}")
