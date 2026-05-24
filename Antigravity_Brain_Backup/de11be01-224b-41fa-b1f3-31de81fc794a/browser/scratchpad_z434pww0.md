# Windly Excel Bulk Upload Conversion Task

## Plan
1. [x] Navigate to Windly guide and understand Excel bulk upload instructions.
2. [x] Identify required templates or formatting rules for Google Spreadsheets.
3. [x] Extract information about mandatory columns and data formats.
4. [x] Summarize findings for the next steps.

## Findings
- Windly supports only Excel (.xlsx) files; Hancom Cell (.cell) is not supported.
- If using Hansell, save as .xlsx or import to Google Sheets first.
- Mandatory field: "수집할 상품 URL" (Product URL to collect).
- Optional fields: "쿠팡 카테고리(선택)", "네이버 카테고리(선택)", "메모(선택)".
- Google Sheets Import: File -> Import -> Upload -> Browse.
- Max 300 products per upload.
- Sheet names should be "엑셀 수집 양식", "쿠팡 전체 카테고리", "네이버 전체 카테고리".
- Sheet protection: Some cells are protected to prevent formatting errors. Use cell copying instead of row/column copying.
