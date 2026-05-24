# Walkthrough - Fix Duplicate Sourcing Issue

I have fixed the issue where the bot was collecting two of each product.

## Changes Made

### 1. Fix Redundant Click Trigger
In `final_sourcing_bot.py`, the `click_windly` function was previously sending both a standard `.click()` and a manual `dispatchEvent`. This caused the Windly extension to trigger twice for a single product. I have removed the redundant dispatch event.

### 2. URL Normalization
Enhanced the URL parsing logic to ensure consistency. It now:
- Removes query parameters.
- Removes `.html` suffixes.
- Ensures a trailing slash.
This prevents minor URL variations from being treated as unique products.

### 3. Improved Logging & Forbidden Keywords
- Added logging to clarify when items are skipped due to forbidden keywords or because they have already been checked.
- **New Forbidden Keywords**: Added "퀸메이드" and "반디" to `forbidden_master_list.json` as requested.

## Verification Results

The code logic has been updated to:
- Trigger only one click per product.
- Use a stricter URL matching pattern in the persistent `collected_master.json`.

Please run the bot and confirm if the duplicates are resolved.
