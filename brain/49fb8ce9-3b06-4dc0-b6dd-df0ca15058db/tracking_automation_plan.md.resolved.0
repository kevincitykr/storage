# Implementation Plan: AliExpress Order Tracking Automation Line

## 1. Goal
Build a fully automated pipeline that:
1. Monitors Shopmine's exported "Pending Shipment" (발송대기) Excel files.
2. Logins into multiple AliExpress accounts (via saved browser sessions).
3. Matches Shopmine orders with AliExpress orders using intelligent matching (Name masking, address normalization).
4. Retrieves tracking numbers and courier information.
5. Generates a Shopmine-compatible Excel file for bulk tracking number upload.

## 2. Components
### A. Master Controller (`tracking_sync_master.py`)
- Monitors a designated network drive (e.g., `N:\...`) for new Excel files.
- Orchestrates the scraping and matching process.
- Handles the final Excel generation.

### B. AliExpress Scraper Module (`ali_order_scraper.py`)
- Uses Playwright/Selenium to connect to existing browser profiles (Chrome, Whale, Edge).
- Navigates to "My Orders" (주문 목록).
- Scrapes order details: Order ID, Product Name, Tracking Number, Courier, Recipient, Address.

### C. Matching Engine (`order_matcher.py`)
- Logic to match "Hong*Gildong" (Shopmine) with "Hong Gildong" (AliExpress).
- Logic to handle virtual phone numbers and address variants.

### D. Shopmine Integration Module (`shopmine_excel_util.py`)
- Reads Shopmine export format.
- Writes Shopmine import format (Bulk Tracking Upload).

## 3. Implementation Steps

### Phase 1: Foundation (Current)
- [ ] Create directory structure in `000_factory_core/tracking_automation`.
- [ ] Implement `shopmine_excel_util.py` to parse '발송대기' and '통합주문' files.
- [ ] Create `config.json` to store browser profile paths and AliExpress account nicknames.

### Phase 2: Scraper Development
- [ ] Implement `ali_order_scraper.py` with multi-browser support.
- [ ] Add logic to handle "View Details" page if tracking info is not visible on the list page.

### Phase 3: Matching & Output
- [ ] Implement `order_matcher.py` with fuzzy matching for names and addresses.
- [ ] Generate the final Excel file.

### Phase 4: Full Automation
- [ ] Integrate into the `안실장_서버.py` dashboard for one-click execution.
- [ ] Add background monitoring capability.

## 4. Next Action
1. Create the `tracking_automation` folder in the workspace.
2. Initialize `config.json` with the user's browser profile locations.
3. Start implementing the `shopmine_excel_util.py`.
