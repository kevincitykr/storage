# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import io
from datetime import datetime

# ── 터미널 인코딩 ──────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── 설정 ───────────────────────────────────────────────────────────────────
NOW_STR = datetime.now().strftime("%Y%m%d_%H%M%S")
USER_DATA_DIR = os.path.abspath("./browser_profiles/notebooklm_profile")
OUTPUT_DIR    = os.path.abspath(f"./output/안실장_{NOW_STR}")
BASE_URL      = "https://notebooklm.google.com/"
CHROME_PATH   = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def safe_click(page, selectors, label="", timeout=15000):
    for sel in selectors:
        try:
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

async def run_automation(dummy_path=None):
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        print(f"\n[START] 안실장_심리자동봇 ({NOW_STR}) 완전 자율 모드 가동...", flush=True)
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            viewport={"width": 1280, "height": 800},
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        page = await context.new_page()

        print("[*] NotebookLM 접속...", flush=True)
        await page.goto(BASE_URL, wait_until="load")
        
        # ── STEP 0: 새 노트북 생성 ───────────────────────────────────────
        print("\n[STEP 0] 새 노트북 생성 중...", flush=True)
        await safe_click(page, ['mat-card.create-new-action-button', '[aria-label*="Create new notebook"]', 'button:has-text("새")'], label="새 노트북 버튼")
        await page.wait_for_timeout(5000)

        # ── STEP 1: 마중물 소스 추가 (채팅 활성화를 위해 필수) ──────────────
        print("\n[STEP 1] 채팅 활성화를 위한 마중물 소스 주입...", flush=True)
        # 소스 추가 모달이 자동으로 안 열릴 경우를 대비해 '소스 추가' 버튼 클릭 시도
        await safe_click(page, ['button:has-text("소스 추가")', 'button:has-text("Add source")'], label="소스 추가 버튼")
        
        await safe_click(page, ['button:has-text("복사된 텍스트")', 'button:has-text("Copied text")'], label="텍스트 입력 버튼")
        await page.wait_for_timeout(2000)
        
        source_text_area = 'textarea.copied-text-input-textarea, textarea[placeholder*="입력"], textarea'
        await page.wait_for_selector(source_text_area, timeout=10000)
        await page.fill(source_text_area, "심리학 트렌드 분석을 시작합니다. 최신 유튜브 인기 주제를 선정해주세요.")
        await page.wait_for_timeout(1000)
        
        await safe_click(page, ['button:has-text("삽입")', 'button:has-text("추가")', 'button:has-text("Insert")'], label="삽입 버튼")
        print("    [*] 소스 삽입 완료. UI 업데이트 대기...", flush=True)
        await page.wait_for_timeout(8000) # 소스 분석 및 채팅창 생성 대기

        # ── STEP 2: 주제 자동 선정 ───────────────────────────────────────
        print("\n[STEP 2] 최신 트렌드 주제 분석 중...", flush=True)
        
        # 채팅창이 div에서 textarea.query-box-input으로 교체될 때까지 대기
        print("    [*] 소스 분석 및 채팅창 활성화 대기 중 (최대 40초)...", flush=True)
        chat_sel = "textarea.query-box-input"
        
        try:
            # textarea가 나타나고 활성화될 때까지 대기 (분석 완료 신호)
            await page.wait_for_selector(chat_sel, timeout=45000, state="visible")
            # 활성화(enabled) 상태까지 대기
            await page.wait_for_function(f"document.querySelector('{chat_sel}') && !document.querySelector('{chat_sel}').disabled", timeout=20000)
            print("    [✓] 채팅창 활성화 확인! (분석 완료)", flush=True)
        except:
            print("    [!] 자동 감지 타임아웃 또는 비활성 상태. 강제 대기 후 일반 셀렉터로 시도합니다.", flush=True)
            await page.wait_for_timeout(15000)
            chat_sel = "textarea[aria-label='쿼리 상자'], [role='textbox'], textarea"

        topic_prompt = "지금 유튜브에서 조회수가 가장 잘 나올만한 참신한 심리학 주제 하나만 추천해줘. 주제 제목만 한 줄로 딱 말해줘."
        
        # 입력 시도
        try:
            await page.click(chat_sel)
            await page.fill(chat_sel, topic_prompt)
            await page.keyboard.press("Enter")
        except:
            # 최후의 수단: Tab 키로 포커스 이동 후 타이핑
            await page.keyboard.press("Tab")
            await page.keyboard.type(topic_prompt)
            await page.keyboard.press("Enter")
        await page.wait_for_timeout(10000)
        
        responses = await page.query_selector_all('.response-content, [data-testid="bot-message"]')
        selected_topic = "추천된 심리학 주제"
        if responses:
            selected_topic = (await responses[-1].inner_text()).strip().split('\n')[0]
            print(f"    [★] 선정된 주제: {selected_topic}", flush=True)

        # ── STEP 3: 대본 및 비주얼 추출 ──────────────────────────────────
        print(f"\n[STEP 3] '{selected_topic}' 대본 및 비주얼 기획안 생성...", flush=True)
        final_prompt = (
            f"선정된 '{selected_topic}' 주제로 유튜브 대본을 쓰고, "
            "추가로 각 장면별 '시각적 묘사(Visual Description)'를 작성해줘. "
            "이미지만으로도 메시지가 전달되도록 글자 없는 고퀄리티 화풍으로 묘사해줘."
        )
        await page.fill(chat_sel, final_prompt)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(20000) # 답변 대기

        # 결과 저장
        responses = await page.query_selector_all('.response-content, [data-testid="bot-message"]')
        if responses:
            result_text = await responses[-1].inner_text()
            file_path = os.path.join(OUTPUT_DIR, f"안실장_결과_{NOW_STR}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result_text)
            print(f"\n[✓] 모든 과정 완료! 파일명: 안실장_결과_{NOW_STR}.txt", flush=True)
            print("-" * 50)
            print(result_text[:200] + "...")
            print("-" * 50)
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
