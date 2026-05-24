import requests
import base64
import os

url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
save_path = r'D:\Kevincity Share\700 Connect AI\AI_Director_Prototype'

payload = {
    'prompt': "Cinematic documentary style, a dignified Korean senior man in his late 60s, gray hair, wearing a premium navy suit, looking at a glowing tablet with KOSPI stock charts, luxurious library background, masterpiece, 8k, photorealistic",
    'steps': 30,
    'width': 1024,
    'height': 576,
    'cfg_scale': 7,
    'sampler_name': 'Euler a'
}

try:
    r = requests.post(url, json=payload)
    r.raise_for_status()
    with open(os.path.join(save_path, "master_visual_korean_senior.png"), 'wb') as f:
        f.write(base64.b64decode(r.json()['images'][0]))
    print("Saved master_visual_korean_senior.png")
except Exception as e:
    print(f"Failed to generate local image: {e}")
