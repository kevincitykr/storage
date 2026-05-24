@echo off
title 🚀 ANTIGRAVITY MASTER PC SETUP ENGINE
color 0b
echo ============================================================
echo   ANTIGRAVITY MASTER PC AUTO-SETUP v1.0
echo   [Target: High-Spec Master Workstation]
echo ============================================================
echo.

:: 1. 파이썬 확인
echo [*] Step 1: Checking Python Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python is not installed or not in PATH.
    echo [!] Please install Python 3.10+ and check 'Add Python to PATH'.
    pause
    exit
)
echo [OK] Python is ready.

:: 2. 필수 라이브러리 설치
echo.
echo [*] Step 2: Installing Essential Libraries...
python -m pip install --upgrade pip
pip install streamlit pandas requests selenium webdriver-manager tqdm colorama
echo [OK] Libraries installed successfully.

:: 3. Ollama (AI 추론 엔진) 확인
echo.
echo [*] Step 3: Checking AI Inference Engine (Ollama)...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] WARNING: Ollama is not found. 
    echo [!] This is a MASTER PC. High-speed AI inference is recommended.
    echo [!] Downloading Ollama is highly suggested: https://ollama.com/
) else (
    echo [OK] Ollama is already installed.
)

:: 4. 바로가기 생성 (PowerShell 활용)
echo.
echo [*] Step 4: Creating Dashboard Shortcut on Desktop...
set SCRIPT_PATH=%~dp0..\0001 Dashboard\통합대시보드_실행하기.bat
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Master_Dashboard.lnk
powershell -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%SHORTCUT_PATH%');$s.TargetPath='%SCRIPT_PATH%';$s.Save()"
echo [OK] Shortcut created on Desktop.

:: 5. 동기화 엔진 가동 준비
echo.
echo [*] Step 5: Initializing Knowledge Base Sync...
start python "%~dp0sync_brain_to_kb.py"
echo [OK] Sync Engine started in background.

echo.
echo ============================================================
echo   SETUP COMPLETE! Welcome to your new Master PC, Boss.
echo   Now you can start the Master Dashboard from Desktop.
echo ============================================================
echo.
pause
