@echo off
title [안실장 통합 컨트롤러] 서버 가동 및 대시보드 실행
cd /d "%~dp0"

echo.
echo ==================================================
echo    안실장 자동화 시스템 가동을 시작합니다.
echo ==================================================
echo.

:: 1. 파이썬 설치 확인
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] 오류: 파이썬(Python)이 설치되어 있지 않거나 PATH에 없습니다.
    pause
    exit /b
)

:: 2. 기존 서버 종료 (포트 5000 사용 중인 프로세스 종료)
echo [*] 기존 서버 정리 중...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    if not "%%a"=="" (
        taskkill /F /PID %%a >nul 2>&1
        echo [✓] 기존 프로세스(PID: %%a) 종료 완료.
    )
)

:: 3. 서버 및 대시보드 실행
echo [*] 통합 서버 가동 (http://127.0.0.1:5000)
echo [*] 대시보드 브라우저 실행 중...

:: 서버 실행 전 약간의 지연 후 브라우저 열기
:: /economy 경로를 명시적으로 호출하여 캐시 문제를 방지합니다.
start http://127.0.0.1:5000/economy

echo [!] 이 창을 닫으면 서버가 종료됩니다.
echo.
python "안실장_서버.py"

pause
