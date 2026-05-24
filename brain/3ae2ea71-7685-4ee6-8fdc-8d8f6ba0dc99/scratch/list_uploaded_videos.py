import os
import json
from datetime import datetime
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

def list_uploads():
    youtube = get_authenticated_service()
    
    # Channel ID: UC_V52QvV-3O-HIjON4Ck0jA -> Uploads Playlist ID: UU_V52QvV-3O-HIjON4Ck0jA
    playlist_id = "UU_V52QvV-3O-HIjON4Ck0jA"
    
    videos = []
    next_page_token = None
    
    print("Fetching uploads...")
    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            published_at = item["snippet"]["publishedAt"]
            video_id = item["contentDetails"]["videoId"]
            
            # Parse date
            pub_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
            
            # Filter for after 2026-03-17
            if pub_date >= datetime(2026, 3, 17):
                videos.append({
                    "id": video_id,
                    "title": title,
                    "published_at": published_at
                })
            else:
                # Since playlist is sorted by date desc, we can stop when we reach older videos
                # Wait, let's make sure we don't stop prematurely if there are weird sorting cases, 
                # but usually it's safe. Just to be sure, let's check if we should continue.
                pass
                
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
            
    # Save to json
    output_path = r"C:\Users\ksohw\.gemini\antigravity\brain\3ae2ea71-7685-4ee6-8fdc-8d8f6ba0dc99\scratch\uploaded_videos.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(videos)} videos to {output_path}")


if __name__ == "__main__":
    list_uploads()
