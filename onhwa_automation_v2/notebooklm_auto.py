import os
import time
import asyncio
from playwright.async_api import async_playwright

# 설정
USER_DATA_DIR = os.path.abspath("./browser_profiles/notebooklm_profile")
OUTPUT_DIR = os.path.abspath("./output/notebooklm_images")
BASE_URL = "https://notebooklm.google.com/"
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

async def run_automation(script_path, reference_sheet_path=None):
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    async with async_playwright() as p:
        # 실제 크롬 세션 재사용
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False, # 동작 확인을 위해 보이게 실행
            viewport={'width': 1280, 'height': 800},
            ignore_default_args=["--enable-automation"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        page = await context.new_page()
        # webdriver 감지 방지
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print(f"[*] Navigating to {BASE_URL}")
        await page.goto(BASE_URL)

        # 로그인 확인 (NotebookLM 메인화면이 나올 때까지 대기)
        # 한국어/영어 버튼 모두 체크
        login_selectors = 'button:has-text("새로 만들기"), button:has-text("Create new"), button:has-text("+ 새로 만들기")'
        try:
            await page.wait_for_selector(login_selectors, timeout=15000)
            print("[+] Logged in successfully.")
        except:
            print("[!] Manual Login Required or UI is in Korean. Waiting...")
            await page.wait_for_selector(login_selectors, timeout=300000)

        # 1. 새 노트북 생성 (정밀 ARIA 레이블 및 유니코드 대응)
        print("[*] Creating new notebook...")
        try:
            # "새 노트북 생성" (\uc0c8 \ub178\ud2b8\ubd81 \uc0dd\uc131)
            await page.click('[aria-label="\uc0c8 \ub178\ud2b8\ubd81 \uc0dd\uc131"], [aria-label="Create new notebook"]', force=True, timeout=10000)
        except:
            # "새로 만들기" (\uc0c8\ub85c \ub9cc\ub4e4\uae30)
            await page.click('button:has-text("\uc0c8\ub85c \ub9cc\ub4e4\uae30"), button:has-text("Create new")', force=True)
        await page.wait_for_timeout(3000)

        # 2. 소스 추가 다이얼로그 확인 및 '컴퓨터' 선택
        print("[*] Opening 'Computer' upload dialog...")
        try:
            # '소스 추가' (\uc18c\uc2a4 \ucd94\uac00)
            await page.wait_for_selector('text=\uc18c\uc2a4 \ucd94\uac00, text=Add source', timeout=20000)
            # '컴퓨터' (\ucef4\ud4e8\ud130)
            await page.click('button:has-text("\ucef4\ud4e8\ud130"), button:has-text("Computer"), [aria-label*="Computer"]', force=True)
        except Exception as e:
            print(f"[!] Source dialog error: {e}. Trying direct file input...")

        # 3. 파일 업로드 (대본 + 스타일 가이드)
        print("[*] Uploading files...")
        try:
            files_to_upload = [script_path]
            if reference_sheet_path:
                files_to_upload.append(reference_sheet_path)
            
            await page.set_input_files('input[type="file"]', files_to_upload)
            print(f"[+] Successfully set files: {files_to_upload}")
        except Exception as e:
            print(f"[!] File setting failed: {e}")
            async with page.expect_file_chooser() as fc_info:
                # "파일" (\ud30c\uc77c)
                await page.click('button:has-text("\ud30c\uc77c"), [aria-label*="File"]', force=True)
            file_chooser = await fc_info.value
            await file_chooser.set_files(files_to_upload)

        # 4. 업로드 완료 및 분석 대기
        print("[*] Waiting for data analysis...")
        # "가이드" (\uac00\uc774\ub4dc)
        await page.wait_for_selector('button[aria-label*="\uac00\uc774\ub4dc"], button[aria-label*="Guide"]', timeout=60000)

        # 5. 노트북 가이드 -> 슬라이드 자료 생성
        print("[*] Generating Presentation slides...")
        await page.click('button[aria-label*="\uac00\uc774\ub4dc"], button[aria-label*="Guide"]', force=True)
        await page.wait_for_timeout(2000)
        
        # "슬라이드" (\uc2ac\ub77c\uc774\ub4dc)
        await page.click('button:has-text("\uc2ac\ub77c\uc774\ub4dc"), button:has-text("Presentation"), button:has-text("Slide")', force=True)
        
        # 생성 대기 (애니메이션 등 고려)
        print("[*] Waiting for slides to generate...")
        await page.wait_for_selector('.presentation-slide-container', timeout=120000) # 가상의 셀렉터

        # 4. 이미지 추출 및 다운로드
        print("[*] Extracting images...")
        slides = await page.query_selector_all('.presentation-slide-image') # 가상의 셀렉터
        
        for i, slide in enumerate(slides):
            img_url = await slide.get_attribute('src')
            if img_url:
                # 이미지 다운로드 로직 (이미지 캡처 또는 URL 다운로드)
                save_path = os.path.join(OUTPUT_DIR, f"slide_{i+1:03d}.png")
                await slide.screenshot(path=save_path)
                print(f"  [+] Saved: {save_path}")

        print("[+] Automation Completed!")
        await context.close()

if __name__ == "__main__":
    script = os.path.abspath("sample_script.txt")
    asyncio.run(run_automation(script))
