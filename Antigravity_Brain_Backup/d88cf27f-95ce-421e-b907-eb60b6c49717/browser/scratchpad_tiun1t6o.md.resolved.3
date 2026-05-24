# Domeggook Windly Button Investigation

## Goals
- [ ] Navigate to Domeggook product page
- [ ] Locate Windly collection button
- [ ] Inspect DOM structure (selectors, iframes, Shadow DOM)
- [ ] Test click reliability
- [ ] Report findings

## Progress
- [x] Navigate to Domeggook product page
- [x] Locate Windly collection button
- [x] Inspect DOM structure (selectors, iframes, Shadow DOM)
- [x] Test click reliability
- [x] Report findings

## Findings
- Two Windly buttons exist: **Overseas (해외구매대행)** at approx (961, 227) and **Domestic (국내위탁판매)** at approx (961, 429).
- They are injected at the end of the `<body>` and appear as plain `<button>` elements in simplified DOM views, likely due to Shadow DOM.
- The text labels "해외구매대행" and "국내위탁판매" are separate text nodes immediately preceding the buttons.
- The bot likely clicks the first button (Overseas) because it matches a broad selector first.
- **Solution**: Use a selector that specifically targets the button associated with "국내위탁판매".
- Recommended selector strategy: Find the text node "국내위탁판매" and click the next `button` element, or use a coordinate-based click if the position is stable (though text-based is better).
- In Playwright/Puppeteer, a selector like `//text()[contains(.,'국내위탁판매')]/following::button[1]` would be more accurate.
- Both buttons triggered a "Plan Expired" popup in this environment, but they are functionally the correct triggers.
