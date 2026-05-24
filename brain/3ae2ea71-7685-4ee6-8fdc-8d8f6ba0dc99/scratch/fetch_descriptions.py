import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

client_secrets_path = r"D:\20260412 kevincity share\004_melodist_seoul\client_secret.json"
token_dir = r"D:\20260412 kevincity share\004_melodist_seoul\tokens"
token_path = os.path.join(token_dir, "token_melodist_final.json")

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return build("youtube", "v3", credentials=creds)
    else:
        raise FileNotFoundError("Token file missing.")

def fetch_descriptions():
    youtube = get_authenticated_service()
    
    video_ids = [
        "5JdMVM0vnxQ", "ajWXcsZqDmU", "7PeRfu5dgSo", "IaZNquj5qY0", "ClkEklMsn8Y",
        "QPbQepJt4_8", "k02lYBygnw0", "utCvxYSHSF0", "E5J7ucz0RHs", "wDcIiPbavHs"
    ]
    
    results = {}
    
    request = youtube.videos().list(
        part="snippet",
        id=",".join(video_ids)
    )
    response = request.execute()
    
    for item in response.get("items", []):
        video_id = item["id"]
        title = item["snippet"]["title"]
        desc = item["snippet"]["description"]
        results[video_id] = {
            "title": title,
            "description": desc
        }
        
    output_path = r"C:\Users\ksohw\.gemini\antigravity\brain\3ae2ea71-7685-4ee6-8fdc-8d8f6ba0dc99\scratch\video_descriptions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} descriptions to {output_path}")

if __name__ == "__main__":
    fetch_descriptions()
