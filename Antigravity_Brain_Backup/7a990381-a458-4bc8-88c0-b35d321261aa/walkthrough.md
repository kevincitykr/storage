# Anti-Bot Bypass Implementation Walkthrough

We have implemented several layers of protection to bypass AliExpress's bot detection.

## Changes Made

### 1. [kvenue_auto.py](file:///d:/20260412%20kevincity share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/kvenue_auto.py)
- **Persistent Context**: Now uses `browser_user_data` folder to store cookies and session data. This makes the browser look like a returning user rather than a suspicious new bot.
- **Stealth Arguments**: Added `--disable-blink-features=AutomationControlled` to hide Playwright's presence.
- **Webdriver Hiding**: Injected an initial script to set `navigator.webdriver` to `undefined`.
- **Custom User-Agent**: Set a standard Windows Chrome User-Agent.

### 2. [deep_scraper_v2.js](file:///d:/20260412%20kevincity share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/deep_scraper_v2.js)
- **Reduced Concurrency**: Changed from 5 to 2 to reduce the request rate.
- **Random Delays**: Added a 2-5 second random wait between batches of requests.
- **Initial Scan Delay**: Added a 5-second initial wait to simulate a user "reading" the page before starting the scan.

## How to Verify

1. **Run the Dashboard**: Start the `안실장_서버.py` and navigate to the Windly Hub.
2. **Launch K-Venue**: Click "1. K-Venue 호출".
3. **Manual Action**: **(중요)** 브라우저가 열리면 알리익스프레스 로그인을 한 번 수동으로 진행해 주세요. 이 세션이 `browser_user_data`에 저장되어 다음부터는 훨씬 안전하게 동작합니다.
4. **Trigger Scrape**: Proceed with the collection as usual.
