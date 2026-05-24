# Improve Windly Domestic Sourcing Button Logic

The goal is to make the "국내위탁판매" button clicking logic extremely robust, especially since it resides within a Shadow DOM and might be injected asynchronously by the Windly extension.

## User Review Required

> [!IMPORTANT]
> The current script might fail due to invisible characters or race conditions where the button exists but isn't interactive. I will implement a "Normalization" strategy for text matching.

## Proposed Changes

### [MODIFY] [domestic_sourcing_bot.py](file:///d:/20260412%20kevincity share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/%EC%95%8C%EB%A6%AC%EC%9D%B5%EC%8A%A4%ED%94%84%EB%A0%88%EC%8A%A4%20%EC%88%98%EC%A7%91%200422/domestic_sourcing_bot.py)

Replace the existing `click_windly` function with an upgraded version based on the user's provided multi-strategy approach, but with the following improvements:
1.  **Text Normalization**: Strip all whitespace and special characters before matching "국내위탁" or "위탁판매".
2.  **Shadow DOM Recursion**: Optimize the JS recursion to handle nested shadow roots more efficiently.
3.  **Visual Interaction**: Ensure the element is scrolled into view and dispatched with a proper click event.
4.  **Wait Logic**: Better integration of waiting for the extension to load.

## Verification Plan

### Automated Tests
- I will create a standalone script `verify_windly_click.py` to test the logic against an open product page via CDP.

### Manual Verification
- Run the bot on a few Domeggook items to ensure it clicks the correct button and triggers the collection.
