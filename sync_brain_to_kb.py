# -*- coding: utf-8 -*-
"""
[Antigravity Knowledge Base Sync Engine]
각 컴퓨터의 로컬 대화 기록을 감시하여 'D:\...\999. knowledge Base'로 자동 변환/백업합니다.
"""

import os
import json
import time
import re
from datetime import datetime

# ==========================================
# [경로 설정]
# ==========================================
BRAIN_DIR = os.path.expanduser(r"~\.gemini\antigravity\brain")

KB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "999. knowledge Base"))
CHECK_INTERVAL = 10  # 감시 주기 (초)

def clean_filename(text):
    """파일명으로 사용할 수 없는 특수문자 및 줄바꿈 제거"""
    # 줄바꿈을 공백으로 변환
    text = text.replace('\n', ' ').replace('\r', ' ')
    # 특수문자 제거 (알파벳, 숫자, 한글, 공백, -, _ 만 허용)
    text = re.sub(r'[^a-zA-Z0-9가-힣\s\-_]', '', text)
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text)
    return text.strip()[:30]


def process_overview_file(file_path, folder_name):
    """overview.txt 파일을 파싱하여 마크다운으로 변환 저장"""
    try:
        if not os.path.exists(file_path):
            return
            
        messages = []
        first_user_input = ""
        created_date = ""
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    msg_type = data.get("type")
                    content = data.get("content", "")
                    created_at = data.get("created_at", "")
                    
                    # 날짜 추출 (첫 번째 메시지 기준)
                    if not created_date and created_at:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        created_date = dt.strftime('%Y%m%d')
                    
                    if msg_type == "USER_INPUT":
                        # XML 태그 제거 (USER_REQUEST 등)
                        clean_content = re.sub(r'<[^>]+>', '', content).strip()
                        if clean_content:
                            messages.append(f"## 👤 USER\n\n{clean_content}\n")
                            if not first_user_input:
                                first_user_input = clean_filename(clean_content)
                                
                    elif msg_type == "PLANNER_RESPONSE" and content:
                        messages.append(f"### 🤖 Antigravity\n\n{content}\n")
                        
                except json.JSONDecodeError:
                    continue
                    
        if not messages:
            return
            
        # 파일명 조합 (날짜_대화ID_첫질문)
        date_str = created_date if created_date else datetime.now().strftime('%Y%m%d')
        short_id = folder_name[:8]
        title_str = f"_{first_user_input}" if first_user_input else ""
        
        kb_filename = f"{date_str}_{short_id}{title_str}.md"
        kb_file_path = os.path.join(KB_DIR, kb_filename)
        
        # 마크다운 내용 생성
        md_content = f"# 🧠 AI 대화 기록 (ID: {folder_name})\n"
        md_content += f"- **생성 날짜:** {date_str}\n"
        md_content += f"- **동기화 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += "---\n\n"
        md_content += "\n".join(messages)
        
        # 저장 (내용이 바뀌었을 때만 덮어쓰기)
        if os.path.exists(kb_file_path):
            with open(kb_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                if f.read() == md_content:
                    return # 변경 없음
                    
        with open(kb_file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"[SUCCESS] 동기화 완료: {kb_filename}")
        
    except Exception as e:
        print(f"[ERROR] {folder_name} 처리 중 오류 발생: {e}")

def main():
    print("============================================================")
    print("   Antigravity Knowledge Base Sync Engine v1.0 가동 중...")
    print("============================================================")
    print(f"[*] 감시 폴더: {BRAIN_DIR}")
    print(f"[*] 저장 폴더: {KB_DIR}")
    
    if not os.path.exists(BRAIN_DIR):
        print(f"[WARNING] 대화 기록 폴더({BRAIN_DIR})를 찾을 수 없습니다.")
        print("[!] 이 컴퓨터에서는 아직 AI 대화를 나눈 적이 없거나, 경로가 다를 수 있습니다.")
        # 폴더가 없으면 생성해 둡니다.
        try:
            os.makedirs(BRAIN_DIR, exist_ok=True)
            print("[*] 폴더를 생성했습니다. 대화가 시작되면 동기화가 진행됩니다.")
        except Exception as e:
            print(f"[ERROR] 폴더 생성 실패: {e}")

    if not os.path.exists(KB_DIR):
        try:
            os.makedirs(KB_DIR, exist_ok=True)
            print(f"[!] 지식 베이스 폴더({KB_DIR})를 생성했습니다.")
        except Exception as e:
            print(f"[ERROR] 저장 폴더 생성 실패: {e}")


    while True:
        try:
            if os.path.exists(BRAIN_DIR):
                for folder_name in os.listdir(BRAIN_DIR):
                    folder_path = os.path.join(BRAIN_DIR, folder_name)
                    if os.path.isdir(folder_path):
                        overview_path = os.path.join(folder_path, ".system_generated", "logs", "overview.txt")
                        if os.path.exists(overview_path):
                            process_overview_file(overview_path, folder_name)
            
        except Exception as e:
            print(f"[CRITICAL ERROR] 감시 루프 오류: {e}")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
