# Implementation Plan - Fix Duplicate Sourcing Issue

The user reports that the bot is collecting two of each product. This is likely caused by redundant click events in the `click_windly` function, which triggers both a native `.click()` and a manual `dispatchEvent('click')`.

## User Review Required

> [!IMPORTANT]
> I will be removing one of the two click triggers in the JavaScript code. If the Windly button is a highly non-standard custom element that requires both to function, please let me know. However, standard automation practices suggest that one should suffice.

## Proposed Changes

### Sourcing Bot Logic

#### [MODIFY] [final_sourcing_bot.py](file:///d:/20260412%20kevincity%20share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/%EC%95%8C%EB%A6%AC%EC%9D%B5%EC%8A%A4%ED%94%84%EB%A0%88%EC%8A%A4%20%EC%88%98%EC%A7%91%200422/final_sourcing_bot.py)

- **Fix Double Click**: Remove `btn.dispatchEvent(...)` in the `evaluate` block of `click_windly`. Native `btn.click()` is usually sufficient.
- **URL Normalization**: Improve URL parsing to handle variations (e.g. ensuring absolute paths and removing tracking parameters consistently).
- **Log skip events**: Add clearer logging for when an item is skipped due to duplication.

## Verification Plan

### Manual Verification
- Run the bot and observe the Windly dashboard to see if products are still being collected in pairs.
- Verify that `collected_master.json` is correctly populating and preventing repeat collection of the same items.
