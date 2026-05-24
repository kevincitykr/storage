# Implementation Plan - Fix Economy Factory Hub Execution

The user is experiencing issues running the automation system via the batch file and the Economy Factory Hub dashboard. Based on investigation, there are several technical hurdles:
1. **Missing Import**: `안실장_경제자동봇.py` is missing `import json`, which causes it to fail during the visual prompt generation step.
2. **CORS Policy**: The dashboard is opened as a local file (`file://`), which modern browsers block from making requests to a local server (`http://127.0.0.1:5000`) unless CORS is explicitly enabled on the server.
3. **Dashboard Mismatch**: The server script defaults to a dashboard in another directory (`003_onhwa_mindnote`), whereas the user is using `Economy_Factory_Hub_20260419.html` in the current directory.

## Proposed Changes

### [Component] Automation Scripts

#### [MODIFY] [안실장_경제자동봇.py](file:///D:/20260412%20kevincity%20share/000_factory_core/%EC%95%88%EC%8B%A4%EC%9E%A5_%EA%B2%BD%EC%A0%9C%EC%9E%90%EB%8F%99%EB%B4%87.py)
- Add `import json` at the top.
- Ensure all subprocess calls use the correct python executable.

### [Component] Server

#### [MODIFY] [안실장_서버.py](file:///D:/20260412%20kevincity share/000_factory_core/%EC%95%88%EC%8B%A4%EC%9E%A5_%EC%84%9C%EB%B2%84.py)
- Add `from flask_cors import CORS` and initialize it (`CORS(app)`).
- Update `DASHBOARD_PATH` to prioritize `Economy_Factory_Hub_20260419.html` if it exists in the current directory.
- Improve error handling for missing files.

### [Component] Startup Script

#### [MODIFY] [0_서버_및_대시보드_통합실행.bat](file:///D:/20260412%20kevincity%20share/000_factory_core/0_%EC%84%9C%EB%B2%84_%EB%B0%8F_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C_%ED%86%B5%ED%95%A9%EC%8B%A4%ED%96%89.bat)
- Add a check for Python availability.
- Launch the dashboard via `http://127.0.0.1:5000` instead of the local file path to avoid CORS issues and ensure consistency.

## Verification Plan

### Automated Tests
- Run `python 안실장_서버.py` and check if it starts without errors.
- Run `python -c "import json; import flask_cors"` to verify dependencies.

### Manual Verification
- Execute the batch file and confirm the browser opens the dashboard at `http://127.0.0.1:5000`.
- Click "GENERATE SCRIPT" and monitor the console in the dashboard to ensure it communicates with the server.
