@echo off
title ANTIGRAVITY_KB_SYNC_ENGINE
color 0a
echo ============================================================
echo   ANTIGRAVITY KNOWLEDGE BASE SYNC ENGINE - BOOTING...
echo ============================================================
echo.
python "%~dp0sync_brain_to_kb.py"
pause
