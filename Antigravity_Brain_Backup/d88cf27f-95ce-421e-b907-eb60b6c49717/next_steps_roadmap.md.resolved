# 🗺️ Roadmap: Expanding to Domemae & OwnerClan

Following the success of the AliExpress K-Venue bot, we will now apply the same **CDP-based automation** to other wholesale platforms.

## 🎯 Target Platforms

1.  **OwnerClan (오너클랜)**
2.  **Domemae (도매매)**
3.  **Domeggook (도매꾹)**

## 🛠 Strategic Approach

The "Winner's Strategy" from the Ali project will be directly ported:

1.  **Browser Context**: Continue using `start_chrome.bat` with the `C:\ChromeDebugProfile`. This ensures the Windly extension is already loaded and logged in for all sites.
2.  **Universal Clicker**: We will verify the CSS selector for the Windly button on these new sites. Usually, it's the same `button.sesame-floating-action-legacy`.
3.  **Site-Specific Scrapers**:
    *   Create listing page scrapers for each site to extract product IDs/URLs.
    *   Maintain the same `click_windly` logic for the detailed pages.

## 📋 Action Plan

- [ ] **Step 1: URL Research**: Identify the main "K-Venue equivalent" or "Recommended Products" listing pages for each site.
- [ ] **Step 2: Selector Verification**: Manually check if the Windly button selector changes on these platforms.
- [ ] **Step 3: Bot Modularization**: Update `final_sourcing_bot.py` to support multiple site profiles.

---
**Next session priority**: Implementation of the **OwnerClan** listing scraper.
