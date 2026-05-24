# Windly Sourcing Button Automation Plan

Finalize the "Windly Clicker" system to automatically navigate AliExpress product detail pages, filter forbidden brands, and click the Windly extension's sourcing button.

## User Review Required

> [!IMPORTANT]
> The automation requires Chrome to be closed before launching the "Debug Chrome" mode to allow access to the user's profile.
> Please ensure you have the Windly extension installed in your default Chrome profile.

## Proposed Changes

### [500.윈들리]

#### [MODIFY] [Windly_Factory_Hub.html](file:///d:/20260412%20kevincity%20share/500.윈들리/Windly_Factory_Hub.html)
- Add a new section for **"Windly Direct Sourcing (Extension)"**.
- Add buttons to:
  1. **Launch Debug Chrome**: Opens Chrome with `--remote-debugging-port=9222` and your real profile.
  2. **Start Windly Clicker**: Runs the script that visits pages and clicks the Windly button.

#### [MODIFY] [windly_clicker.py](file:///d:/20260412%20kevincity%20share/500.윈들리/windly_clicker.py)
- Ensure the selectors for the Windly button (`.windly-collect-btn`) and the confirmation button in the popup are accurate.
- Improve logging to show real-time progress in the dashboard.

### [000_factory_core]

#### [MODIFY] [안실장_서버.py](file:///d:/20260412%20kevincity%20share/000_factory_core/안실장_서버.py)
- Add API endpoints:
  - `/api/launch_debug_chrome`: Kills existing Chrome and launches it in debug mode.
  - `/api/run_windly_clicker`: Executes `windly_clicker.py` in the background.

## Verification Plan

### Automated Tests
- Run `launch_debug_chrome` and verify Chrome opens.
- Manually navigate to a product page and check if the Windly button appears.
- Run `run_windly_clicker` and watch the terminal/dashboard logs for "SUCCESS" messages.

### Manual Verification
- Check the Windly dashboard (extension or web) to see if the 5 items are successfully collected.
