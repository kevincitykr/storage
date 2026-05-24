# -*- coding: utf-8 -*-
"""
init_session.py — 개선판 (v2)

최초 1회 실행해서 구글 로그인 세션을 저장합니다.
이후 notebooklm_auto.py가 저장된 세션을 재사용합니다.
"""

import sys
import os
import asyncio

# Fix 1: 윈도우 터미널 인코딩 강제 UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from playwright.async_api import async_playwright

USER_DATA_DIR = os.path.abspath("./browser_profiles/notebooklm_profile")
CHROME_PATH   = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def init_session():
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    async with async_playwright() as p:
        print(f"[*] 실제 Chrome 실행: {CHROME_PATH}")

        # Fix 2: 자동화 감지 우회 설정
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            viewport={"width": 1280, "height": 800},
            ignore_default_args=["--enable-automation"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
            ],
        )

        page = await context.new_page()
        # Fix 2: webdriver 숨기기
        await page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        await page.goto("https://notebooklm.google.com/")

        print("\n" + "=" * 55)
        print("  [!] 수동 작업 필요")
        print("  1. 브라우저에서 구글 로그인을 완료하세요.")
        print("  2. NotebookLM 메인 화면이 뜨면 브라우저를 '직접' 닫으세요.")
        print("=" * 55 + "\n")

        # 브라우저가 닫힐 때까지 대기
        try:
            while len(context.pages) > 0:
                await asyncio.sleep(1)
        except Exception:
            pass

        print("[+] 세션 저장 완료. notebooklm_auto.py 실행 준비 됐습니다.")


if __name__ == "__main__":
    asyncio.run(init_session())
