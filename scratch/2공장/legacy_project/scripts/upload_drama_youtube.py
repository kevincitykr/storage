
"""
황혼의 라이브 드라마 전용 YouTube 업로드 스크립트
drama_script.json의 메타데이터를 사용하여 output_drama_video.mp4를 업로드합니다.
"""

import json
import sys
import os
from pathlib import Path
import random
import time
import http.client
import httplib2

# 프로젝트 루트 설정
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "execution"))

from _utils import load_json, log, TMP_DIR, save_json

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError as e:
    log(f"필수 라이브러리가 설치되지 않았습니다: {e}", "ERROR")
    sys.exit(1)


# YouTube API 설정
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.upload'
]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = PROJECT_ROOT / 'client_secrets.json'
TOKEN_FILE = PROJECT_ROOT / 'token.json'

# 재시도 설정
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def get_authenticated_service():
    """YouTube API 인증 서비스 생성"""
    log("YouTube API 인증 중...")
    
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            log("토큰 갱신 중...")
            creds.refresh(Request())
        else:
            if not CLIENT_SECRETS_FILE.exists():
                log(f"client_secrets.json 파일이 없습니다: {CLIENT_SECRETS_FILE}", "ERROR")
                sys.exit(1)
            
            log("새 인증 필요 - 브라우저가 열립니다...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        log("인증 토큰 저장 완료")
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def upload_video(youtube, video_path: Path, title: str, description: str, 
                 tags: list, category_id: str = "24") -> str: # 24: Entertainment
    """YouTube에 영상 업로드"""
    log(f"업로드 시작: {title}")
    
    body = {
        'snippet': {
            'title': title[:100],
            'description': description[:5000],
            'tags': tags[:500] if tags else [],
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
            'shorts_enabled': False # 드라마는 롱폼이므로 False 권장
        }
    }
    
    media = MediaFileUpload(
        str(video_path),
        mimetype='video/mp4',
        resumable=True,
        chunksize=1024 * 1024
    )
    
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = None
    error = None
    retry = 0
    
    while response is None:
        try:
            log("업로드 진행 중...")
            status, response = insert_request.next_chunk()
            if status:
                log(f"업로드 진행률: {int(status.progress() * 100)}%")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"재시도 가능한 HTTP 오류: {e.resp.status}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"재시도 가능한 오류: {e}"
        
        if error:
            log(error, "WARNING")
            retry += 1
            if retry > MAX_RETRIES:
                log("최대 재시도 횟수 초과", "ERROR")
                raise Exception("업로드 실패")
            sleep_seconds = random.random() * (2 ** retry)
            time.sleep(sleep_seconds)
            error = None
    
    video_id = response.get('id')
    log(f"업로드 완료! Video ID: {video_id}")
    return video_id


def main():
    log("=== 황혼의 라이브 유튜브 업로드 ===")
    
    # 1. 메타데이터 로드
    try:
        data = load_json('drama_script.json')
    except:
        data = {}
    
    # 메타데이터 강제 보정 (JSON에 타이틀이 없는 경우 대비)
    if not data.get('title'):
        data['title'] = '엄마의 낡은 레시피 노트 (여성 성우 Ver.)'
        data['description'] = '치매 초기 진단을 받은 엄마가 딸을 위해 남기는 요리 비법과 사랑 이야기.\n#드라마 #라디오 #감동 #엄마 #요리'
        data['hashtags'] = ['드라마', '감동', '라디오', '오디오북', '엄마', '요리']

    # 2. 영상 파일 확인
    video_path = TMP_DIR / "output_drama_video_female.mp4"
    if not video_path.exists():
        log(f"영상 파일이 없습니다: {video_path}", "ERROR")
        return

    # 3. 인증 및 업로드
    youtube = get_authenticated_service()
    
    video_id = upload_video(
        youtube,
        video_path,
        data.get('title'),
        data.get('description'),
        data.get('hashtags')
    )
    
    # 4. 결과 저장
    result = {
        'video_id': video_id,
        'url': f'https://youtu.be/{video_id}',
        'uploaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    save_json(result, 'upload_result.json')
    log(f"최종 완료: https://youtu.be/{video_id}")

if __name__ == "__main__":
    main()
