import requests
import base64
import os

url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
save_path = r'D:\Kevincity Share\700 Connect AI\AI_Director_Prototype'

prompts = [
    'Cinematic close up of Samsung electronics building with red protest signs, dramatic lighting, 8k',
    'Digital stock market board showing KOSPI index reaching 8000, glowing numbers, high tech atmosphere',
    'Modern luxury apartments in Seoul at sunset, real estate concept, photorealistic, 8k'
]

for i, p in enumerate(prompts):
    payload = {
        'prompt': f"{p}, masterpiece, professional documentary style",
        'steps': 20,
        'width': 1024,
        'height': 576
    }
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        with open(os.path.join(save_path, f"scene_asset_{i+1}.png"), 'wb') as f:
            f.write(base64.b64decode(r.json()['images'][0]))
        print(f"Saved scene_asset_{i+1}.png")
    except Exception as e:
        print(f"Failed to generate asset {i+1}: {e}")
