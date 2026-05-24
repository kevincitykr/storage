import os
import whisper
import json

def generate_synced_subtitles(audio_path, output_json_path):
    print(f"[*] Loading Whisper model for forced alignment...")
    # 'base' 모델을 사용하여 속도와 정확도의 균형을 맞춤 (한국어는 'base'나 'small' 권장)
    model = whisper.load_model("base")
    
    print(f"[*] Transcribing audio: {audio_path}")
    # word_timestamps=True 옵션을 사용하여 단어 단위 타이밍 추출
    result = model.transcribe(audio_path, verbose=False, word_timestamps=True)
    
    # 렌더러가 사용하기 쉬운 구조로 변환
    segments = []
    for segment in result['segments']:
        segments.append({
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text'].strip(),
            "words": [
                {"word": w['word'], "start": w['start'], "end": w['end']} 
                for w in segment.get('words', [])
            ]
        })
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    
    print(f"[+] Synced subtitles saved to {output_json_path}")
    return segments

if __name__ == "__main__":
    # generate_synced_subtitles("audio.mp3", "subtitles.json")
    pass
