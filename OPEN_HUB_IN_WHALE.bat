@echo off
set "WHALE_PATH=C:\Program Files\Naver\Naver Whale\Application\whale.exe"
if exist "%WHALE_PATH%" (
    start "" "%WHALE_PATH%" "%~dp0YouTube_Factory_Hub_20260429_0020.html"
) else (
    echo [ERROR] Naver Whale not found at the expected path.
    pause
)
exit
