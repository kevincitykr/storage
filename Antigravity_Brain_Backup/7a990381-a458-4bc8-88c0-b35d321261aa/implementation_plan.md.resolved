# Bypass AliExpress Anti-Bot Detection

The current scraper is being detected by AliExpress as a bot "from the start". This is likely due to standard Playwright automation markers and clean browser sessions which lack user history/cookies.

## Proposed Changes

### [Component] Automation Script

#### [MODIFY] [kvenue_auto.py](file:///d:/20260412%20kevincity share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/kvenue_auto.py)
- **Implement Persistent Context**: Instead of a fresh browser every time, use `launch_persistent_context` with a dedicated directory (e.g., `user_data`). This maintains login sessions and looks like a real user.
- **Add Stealth Arguments**: 
    - `--disable-blink-features=AutomationControlled`
    - Custom User-Agent.
- **Hide `navigator.webdriver`**: Inject a script at start to set `Object.defineProperty(navigator, 'webdriver', {get: () => undefined})`.

### [Component] Scraper Logic

#### [MODIFY] [deep_scraper_v2.js](file:///d:/20260412%20kevincity share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/deep_scraper_v2.js)
- **Lower Concurrency**: Reduce default concurrency from 5 to 2.
- **Randomized Delays**: Introduce random wait times (e.g., 2-5 seconds) between `fetch` calls.
- **Initial Wait**: Add a 5-10 second wait before starting the deep scan to simulate a user looking at the page.

## Verification Plan

### Automated Tests
- Run `kvenue_auto.py` manually to verify the browser opens without immediate "Robot detected" messages.
- Test `deep_scraper_v2.js` in the console to ensure it processes items without triggering blocks.

### Manual Verification
- Verify that the browser persists login if the user logs into AliExpress manually once.
- Check if the "Windly Master v5.1" overlay functions correctly with the new delays.
