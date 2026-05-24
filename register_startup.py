# -*- coding: utf-8 -*-
import os
import winshell
from win32com.client import Dispatch

def create_startup_shortcut():
    # 1. 대상 파일 (START_SYNC_KB.bat)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, "START_SYNC_KB.bat")
    
    if not os.path.exists(target_file):
        print(f"[ERROR] 대상을 찾을 수 없습니다: {target_file}")
        return

    # 2. 시작프로그램 폴더 경로
    startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_path, "ANTIGRAVITY_SYNC.lnk")

    # 3. 바로가기 생성
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_file
        shortcut.WorkingDirectory = current_dir
        shortcut.IconLocation = target_file
        shortcut.Description = "Antigravity Knowledge Base Sync Engine"
        shortcut.Save()
        print(f"[SUCCESS] 시작프로그램에 등록되었습니다: {shortcut_path}")
    except Exception as e:
        print(f"[ERROR] 등록 실패: {e}")

if __name__ == "__main__":
    # 필요한 라이브러리 설치 시도
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("[*] 필수 라이브러리(pywin32, winshell) 설치 중...")
        os.system("pip install pywin32 winshell")
        import winshell
        from win32com.client import Dispatch

    create_startup_shortcut()
