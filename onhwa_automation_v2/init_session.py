import asyncio
import os
from playwright.async_api import async_playwright

USER_DATA_DIR = os.path.abspath("./browser_profiles/notebooklm_profile")
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

async def init_session():
    async with async_playwright() as p:
        print(f"[*] Launching REAL Chrome for login: {CHROME_PATH}")
        
        # 실제 크롬을 사용하고 자동화 플래그를 숨김
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            viewport={'width': 1280, 'height': 800},
            # 구글 보안 차단 방지를 위한 핵심 설정
            ignore_default_args=["--enable-automation"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        page = await context.new_page()
        # webdriver 감지 방지 스크립트 삽입
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        await page.goto("https://notebooklm.google.com/")
        
        print("\n" + "="*50)
        print(" [!] MANUAL ACTION REQUIRED")
        print(" 1. 구글 로그인을 완료하세요.")
        print(" 2. 보안 경고가 뜨지 않는지 확인하세요.")
        print(" 3. NotebookLM 메인 화면이 나오면 브라우저를 '직접 닫으세요'.")
        print("="*50 + "\n")
        
        try:
            while len(context.pages) > 0:
                await asyncio.sleep(1)
        except:
            pass
        
        print("[+] Session saved. Automation will use this session.")

if __name__ == "__main__":
    asyncio.run(init_session())
