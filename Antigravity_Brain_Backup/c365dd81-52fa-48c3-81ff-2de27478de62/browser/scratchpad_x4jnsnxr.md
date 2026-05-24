# Task Plan: Suno Factory Dashboard Verification

- [x] Open the dashboard: `file:///D:/...` (Workaround: Use Windows path `D:\...`)
- [x] Click 'REFRESH' in the TREND_INJECTION_PULSE section.
- [x] Wait for trends to load. (Succeeded)
- [x] Click on one of the loaded trend tags. (Succeeded)
- [ ] Click the 'INITIALIZE 12-TRACK SCHEMA' button. (FAILED: Server returns 500 Error)
- [ ] Observe if the track grid fills with data. (Did not fill)
- [ ] Report the result.

## Findings:
- `open_browser_url` blocks `file:///`, but Windows-style paths like `D:\...` work.
- The dashboard is reachable but reports `ENGINE_OFFLINE` due to CORS errors when fetching from a `file://` origin.
- Manual verification via Swagger UI (`/docs`) reveals that the `/generate` endpoint returns a **500 Internal Server Error**.
- Analyzing the server code reveals a potential **ZeroDivisionError** in the `generate_pro_masterpiece_tracks` function if `GEMINI_API_KEYS` is not set (due to `key_idx % len(API_KEYS)` where `len(API_KEYS)` is 0).
- This prevents even the MOCK data from being returned.
