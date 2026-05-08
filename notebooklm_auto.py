# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import io

# ── Fix 1: 터미널 인코딩 ──────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── 설정 ───────────────────────────────────────────────────────────────────
USER_DATA_DIR = os.path.abspath("./browser_profiles/notebooklm_profile")
OUTPUT_DIR    = os.path.abspath("./output")
BASE_URL      = "https://notebooklm.google.com/"
CHROME_PATH   = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def safe_click(page, selectors, label="", timeout=15000):
    for sel in selectors:
        try:
            print(f"    [*] 시도 중: {sel}", flush=True)
            await page.wait_for_selector(sel, timeout=timeout, state="visible")
            await page.click(sel, force=True)
            print(f"    [✓] 클릭 성공: {label or sel}", flush=True)
            return True
        except: continue
    return False

async def safe_wait(page, selectors, label="", timeout=20000):
    for sel in selectors:
        try:
            await page.wait_for_selector(sel, timeout=timeout, state="visible")
            print(f"    [✓] 요소 발견: {label or sel}", flush=True)
            return True
        except: continue
    return False

# ── 메인 봇 로직 ──────────────────────────────────────────────────────────
async def run_automation(script_path):
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        print("\n[START] NotebookLM 자동화 봇 가동...", flush=True)
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            viewport={"width": 1280, "height": 800},
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        page = await context.new_page()

        print("[*] NotebookLM 접속 및 로그인 확인...", flush=True)
        await page.goto(BASE_URL, wait_until="load")
        
        # 메인 화면 진입 확인
        is_main = await safe_wait(page, ['button:has-text("새")', 'button:has-text("Create")', '[aria-label*="Create"]'], label="메인 대시보드")
        if not is_main:
            print("[!] 로그인이 필요합니다. 브라우저에서 로그인 후 다시 실행해주세요.", flush=True)
            await context.close()
            return

        # 1. 새 노트북 생성
        print("\n[STEP 1] 새 노트북 생성...", flush=True)
        await safe_click(page, ['[aria-label*="Create new notebook"]', 'button:has-text("새 노트북")', 'button:has-text("Create")'], label="새 노트북 버튼")
        await page.wait_for_timeout(3000)

        # 2. 대본 주입 (복사된 텍스트 방식 - 가장 안정적)
        print("\n[STEP 2] 대본 내용 주입...", flush=True)
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        await safe_click(page, ['button:has-text("복사된 텍스트")', 'button:has-text("Copied text")', '[aria-label*="text"]'], label="텍스트 입력 버튼")
        await page.wait_for_timeout(2000)
        
        # 텍스트 박스에 붙여넣기
        await page.fill('textarea', content)
        await safe_click(page, ['button:has-text("추가")', 'button:has-text("Insert")', 'button:has-text("Add")'], label="추가 버튼")
        print(f"    [✓] 대본 주입 완료 ({len(content)}자)", flush=True)
        
        # 3. 비주얼 스토리보드 생성 (채팅창 활용)
        print("\n[STEP 3] 비주얼 스토리보드 생성 요청 (채팅)...", flush=True)
        # 가이드 버튼 클릭하여 채팅창 열기
        await safe_click(page, ['button[aria-label*="Guide"]', 'button[aria-label*="가이드"]', '.notebook-guide-button'], label="가이드 버튼")
        await page.wait_for_timeout(3000)

        # 채팅 입력창 찾기 및 입력
        # 텍스트 영역을 찾기 위해 더 넓은 범위의 셀렉터 사용
        chat_selectors = [
            'textarea[placeholder*="질문"]', 
            'textarea[placeholder*="Ask"]', 
            '[role="textbox"]',
            'div[contenteditable="true"]'
        ]
        
        visual_prompt = (
            "이 대본을 바탕으로 유튜브 영상 제작을 위한 '장면별 시각적 묘사'를 작성해줘. "
            "슬라이드에 글자를 쓰지 말고, 오직 영상의 화면에 보일 이미지의 구체적인 화풍과 묘사만 작성해줘. "
            "일관된 캐릭터와 배경 톤을 유지해야 해."
        )

        found_chat = False
        for sel in chat_selectors:
            try:
                await page.wait_for_selector(sel, timeout=5000)
                await page.fill(sel, visual_prompt)
                await page.keyboard.press("Enter")
                found_chat = True
                print(f"    [✓] 프롬프트 전송 성공 (셀렉터: {sel})", flush=True)
                break
            except: continue
        
        if not found_chat:
            print("    [!] 채팅창을 찾을 수 없어 직접 입력을 시도합니다...", flush=True)
            await page.keyboard.press("Tab") # 탭으로 포커스 이동 시도
            await page.keyboard.type(visual_prompt)
            await page.keyboard.press("Enter")

        # 4. 결과 추출 및 저장
        print("\n[STEP 4] 결과 추출 중...", flush=True)
        await page.wait_for_timeout(15000) # AI 답변 대기
        
        responses = await page.query_selector_all('.response-content, [data-testid="bot-message"], .chat-message')
        if responses:
            result_text = await responses[-1].inner_text()
            file_path = os.path.join(OUTPUT_DIR, "bot_result.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result_text)
            print(f"\n[+] 자동화 완료! 결과 파일: {file_path}", flush=True)
            print("-" * 50)
            print(result_text[:300] + "...")
            print("-" * 50)
        else:
            print("[!] 답변 추출 실패. 스크린샷 확인 필요.", flush=True)
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "error_debug.png"))

        await context.close()

if __name__ == "__main__":
    # 사용자가 원하는 주제의 대본 경로
    target_script = os.path.abspath("smart_people_script.txt")
    asyncio.run(run_automation(target_script))
