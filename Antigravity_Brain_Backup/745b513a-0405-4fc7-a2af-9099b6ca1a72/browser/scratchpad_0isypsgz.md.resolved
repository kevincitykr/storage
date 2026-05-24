# Task Checklist
- [x] Open OwnerClan product search page.
- [x] Check if products are visible (Login required for full list).
- [ ] Look for the "Windly" collection button.
- [ ] Analyze the button's selector/XPath.
- [ ] Analyze the collection modal and "Start Collection" button.
- [ ] Check pagination area.
- [ ] Identify failure points in the user's script.

# Notes
- Opened `https://www.ownerclan.com/V2/product/search.php?categoryCode=50000006`.
- Page shows 0 products. Login is definitely required to see the item list and the Windly button.
- Attempted to search for "마스크" but it didn't solve the 0 product issue in the specific category.
- Observed 401 errors in console, confirming unauthorized access to product data.
- Analyzed the user's script:
    - It uses very rigid XPaths for the Windly button (`/html/body/div[18]/...`).
    - It uses `.page_inbox` for pagination, which I need to verify on a page with actual content.
    - It searches for "수집 시작" and "실패한 수집 재시도" buttons by text.
