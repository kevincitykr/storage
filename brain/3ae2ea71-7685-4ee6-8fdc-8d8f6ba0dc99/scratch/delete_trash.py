import os
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

def delete_videos():
    youtube = get_authenticated_service()
    
    # 타닥타닥 모닥불 이후에 등록된 쓰레기 쇼츠들
    delete_ids = [
        "tmpBmaMQmAw", "1wI5n9KoL0Y", "8Iy_tTTwzRU", 
        "lYxO2oXbtEA", "oQKc35y19zg", "0KY04NaT1gg"
    ]
    
    for vid_id in delete_ids:
        try:
            print(f"Deleting video: {vid_id}...")
            youtube.videos().delete(id=vid_id).execute()
            print(f"  [SUCCESS] Deleted {vid_id}")
        except Exception as e:
            print(f"  [ERROR] Failed to delete {vid_id}: {e}")

if __name__ == "__main__":
    delete_videos()
