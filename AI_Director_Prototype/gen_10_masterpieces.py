import os
import shutil
import requests
import base64

# 1. Clean up "trash"
path = r"D:\Kevincity Share\700 Connect AI\AI_Director_Prototype\final_production"
if os.path.exists(path):
    shutil.rmtree(path)
os.makedirs(path)
print("Cleaned up previous trash images.")

# 2. Gemma's Deep Analysis Prompts (10 Unique Masterpieces)
# These are rewritten to be highly specific and cinematic
master_prompts = [
    "Ultra-high resolution, cinematic close-up of a shattered semiconductor wafer on a cold laboratory floor, red emergency lights reflecting on the metallic surface, Samsung logo visible on a fragment, high contrast, dramatic lighting",
    "Atmospheric wide shot of an empty, dark high-tech automated factory at night, one tiny red warning light blinking in the distance, fog swirling around robot arms, futuristic documentary style",
    "3D holographic visualization of a global supply chain map, red broken lines glitching and sparking, floating in a dark high-tech command center, intricate details, cyber-tech aesthetic",
    "Yeouido financial district at night, a giant glowing golden numbers '8000' emerging through thick dark clouds, epic scale, lens flare, professional architectural photography",
    "Close up of a smart, elderly Korean investor with gray hair, looking at a wall of glowing stock charts reflecting on his glasses, wise expression, dramatic chiaroscuro lighting",
    "Cinematic aerial view of luxury apartments along the Han River at sunset, glowing golden lines tracing the building outlines like a circuit board, symbol of high-end real estate",
    "Close up of a house key being handed over between a senior and a young person, the key is made of glowing gold, symbolic of asset transfer, blurred high-end apartment background",
    "Dramatic shot of a countdown timer showing '3:00' (3 months) glowing in red, superimposed over a busy real estate agency office at night, symbolic of the Jeonse-Sale gap rule",
    "A chessboard where the King piece (Samsung logo) is being surrounded by black knights (TSMC/Intel logos), dramatic lighting, metaphorical battle of semiconductor giants",
    "End scene: A beautiful sunrise over Namsan Tower, gold light flooding the city, symbol of economic hope and new opportunity for seniors, 8k resolution, cinematic masterpiece"
]

# 3. Generate 10 Masterpieces using local Forge
FORGE_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

def gen_masterpiece(i, prompt):
    payload = {
        "prompt": prompt,
        "steps": 35, # Increased steps for higher quality
        "width": 1024,
        "height": 576,
        "cfg_scale": 8,
        "sampler_name": "Euler a"
    }
    r = requests.post(FORGE_URL, json=payload)
    img_path = os.path.join(path, f"MASTERPIECE_{i+1:03d}.png")
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(r.json()['images'][0]))
    print(f"Generated Masterpiece {i+1}")

print("Gemma is now directing the local engine to create 10 masterpieces...")
for i, p in enumerate(master_prompts):
    gen_masterpiece(i, p)

print("ALL 10 MASTERPIECES GENERATED.")
