# Temu Sourcing Bot Research

## Task Checklist
- [x] Analyze product detail link selector on category page (`https://www.temu.com/k-tools-industrial-o3-1420.html`)
- [x] Analyze product title selector on detail page
- [x] Check for Windly button and identify its selector
- [x] Record 2-3 additional category URLs

## Findings
- **Product Link Selector (Category Page):** `a._1ak1dai3` (Consistent across items)
- **Product Title Selector (Detail Page):** `h1` (Usually an `h1` or a `div` with a specific class like `._2v9L_Yp6`. In the current view, it was element index 118, which is a span containing the full product description.)
- **Windly Button Selector:** `button.sesame-floating-action-legacy` (This is the "Sesame" floating action button used by the Windly extension).
- **Additional Categories:**
  - Home & Kitchen: `https://www.temu.com/kr/home-kitchen-o3-36.html`
  - Women's Clothing: `https://www.temu.com/kr/womens-clothing-o3-28.html`
  - Sports & Outdoors: `https://www.temu.com/kr/sports-outdoors-o3-178.html`
  - Beauty & Health: `https://www.temu.com/kr/beauty-health-o3-25.html`
