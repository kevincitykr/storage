# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import io
import json
from datetime import datetime

# ── 터미널 인코딩 ──────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── 설정 ───────────────────────────────────────────────────────────────────
NOW_STR = datetime.now().strftime("%Y%m%d_%H%M%S")
USER_DATA_DIR = os.path.abspath("./browser_profiles/notebooklm_profile")
OUTPUT_DIR    = os.path.abspath(f"./output/안실장_경제_{NOW_STR}")
BASE_URL      = "https://notebooklm.google.com/"
CHROME_PATH   = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def smart_click(page, text_list, label=""):
    """글자 기반으로 가장 확실하게 버튼을 찾아 클릭함"""
    print(f"    [*] '{label}' 탐색 중...", flush=True)
    for text in text_list:
        try:
            # 1. 텍스트로 찾기
            btn = page.get_by_text(text, exact=False).first
            if await btn.is_visible():
                await btn.click(force=True)
                print(f"    [✓] {label} 클릭 성공 (Text: {text})", flush=True)
                return True
            # 2. Role로 찾기
            btn = page.get_by_role("button", name=text).first
            if await btn.is_visible():
                await btn.click(force=True)
                print(f"    [✓] {label} 클릭 성공 (Role: {text})", flush=True)
                return True
        except: continue
    
    # 3. 최후의 수단: 화면에 보이는 모든 버튼 텍스트 출력 (디버깅용)
    print(f"    [!] {label} 찾기 실패. 현재 화면의 버튼들:", flush=True)
    try:
        buttons = await page.query_selector_all('button, [role="button"]')
        for b in buttons[:10]:
            t = await b.inner_text()
            if t.strip(): print(f"      - 발견된 버튼: {t.strip()[:20]}", flush=True)
    except: pass
    return False

async def run_automation():
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        print(f"\n[START] 안실장_경제자동봇 V2.4 (지능형 탐색) 시작 ({NOW_STR})", flush=True)
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                executable_path=CHROME_PATH,
                headless=False,
                viewport={"width": 1280, "height": 800},
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            page = await context.new_page()

            print("[*] NotebookLM 접속 중...", flush=True)
            await page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
            
            # ── STEP 0: 새 노트북 생성 ───────────────────────────────────────
            print("\n[STEP 0] 새 노트북 생성", flush=True)
            if not await smart_click(page, ["새 노트북", "New notebook", "Create"], label="새 노트북"):
                # 수동 셀렉터 시도
                await page.click('mat-card.create-new-action-button', force=True)
            
            await page.wait_for_timeout(7000)

            # ── STEP 1: 마중물 소스 주입 ───────────────────────────────────
            print("\n[STEP 1] 마중물 소스 주입 (최대 난관)", flush=True)
            
            # 소스 추가 버튼
            await smart_click(page, ["소스 추가", "Add source"], label="소스 추가")
            await page.wait_for_timeout(3000)

            # 복사된 텍스트 (텍스트 매칭 강화)
            if not await smart_click(page, ["복사된 텍스트", "Copied text", "텍스트", "content_paste"], label="텍스트 입력 메뉴"):
                print("[ERROR] 텍스트 입력 메뉴를 열지 못했습니다.", flush=True)
                return

            await page.wait_for_timeout(3000)
            
            # 텍스트 입력창
            source_text_area = 'textarea.copied-text-input-textarea, textarea[placeholder*="입력"], textarea'
            print("    [*] 마중물 내용 작성 중...", flush=True)
            try:
                await page.wait_for_selector(source_text_area, timeout=10000)
                await page.fill(source_text_area, "경제 트렌드 분석을 시작합니다. 최신 재테크 정보를 바탕으로 유익한 주제를 선정해 주세요.")
                await page.wait_for_timeout(1000)
                await page.keyboard.press("Control+Enter") # 삽입 시도
                print("    [✓] 텍스트 입력 및 삽입 시도 완료", flush=True)
            except:
                print("[ERROR] 텍스트 입력창을 찾지 못했습니다.", flush=True)
                return

            # 삽입 버튼 최종 클릭
            await smart_click(page, ["삽입", "Insert", "추가"], label="삽입 확정")
            print("    [*] 소스 분석 대기 (20초)...", flush=True)
            await page.wait_for_timeout(20000)

            # ── STEP 2: 주제 자동 선정 ───────────────────────────────────────
            print("\n[STEP 2] 주제 자동 분석 단계", flush=True)
            chat_sel = "textarea.query-box-input, [role='textbox'], textarea"
            
            try:
                await page.wait_for_selector(chat_sel, timeout=30000)
                await page.click(chat_sel)
                await page.keyboard.type("지금 당장 만들어야 할 경제 주제 하나만 제목으로 추천해줘.", delay=30)
                await page.keyboard.press("Enter")
                print("    [✓] 주제 요청 완료", flush=True)
            except:
                print("[ERROR] 채팅창을 찾지 못했습니다.", flush=True)
                return

            await page.wait_for_timeout(20000)
            
            responses = await page.query_selector_all('.response-content, [data-testid="bot-message"]')
            selected_topic = "선정된 경제 주제"
            if responses:
                selected_topic = (await responses[-1].inner_text()).strip().split('\n')[0]
                print(f"    [★] 최종 선정: {selected_topic}", flush=True)

            # ── STEP 3: 대본 생성 ─────────────────────────────────────────
            print(f"\n[STEP 3] '{selected_topic}' 대본 생성 중...", flush=True)
            await page.fill(chat_sel, f"'{selected_topic}' 주제로 유튜브 대본과 시각 묘사안을 만들어줘.")
            await page.keyboard.press("Enter")
            print("    [*] 최종 결과 도출 중 (약 50초)...", flush=True)
            await page.wait_for_timeout(50000)

            # 결과 저장
            responses = await page.query_selector_all('.response-content, [data-testid="bot-message"]')
            if responses:
                result_text = await responses[-1].inner_text()
                file_path = os.path.join(OUTPUT_DIR, f"안실장_경제결과_{NOW_STR}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(result_text)
                print(f"\n[FINISH] 성공! 파일명: {os.path.basename(file_path)}", flush=True)

        except Exception as e:
            print(f"\n[ERROR] 시스템 예외: {str(e)}", flush=True)

if __name__ == "__main__":
    asyncio.run(run_automation())
