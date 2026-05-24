# MCP 서버 연결을 위한 환경 구축 완료

요청하신 대로 필요한 모든 도구의 설치를 완료했습니다.

## 설치된 항목 및 경로

1. **Python 3.12**
   - 경로: `C:\Users\ksohw\AppData\Local\Programs\Python\Python312\python.exe`
2. **NotebookLM MCP Server**
   - 경로: `C:\Users\ksohw\AppData\Local\Programs\Python\Python312\Scripts\notebooklm-mcp.exe`
3. **Node.js & Npx**
   - Node 경로: `C:\Program Files\nodejs\node.exe`
   - Npx 경로: `C:\Program Files\nodejs\npx.cmd`
4. **Google Cloud CLI**
   - 설치 완료 (터미널 재시작 필요할 수 있음)

---

## 다음 단계: 인증 진행 (사용자 수동 작업 필요)

보안 및 브라우저 로그인 연동을 위해 다음 인증 단계는 사용자님께서 직접 터미널(PowerShell 등)에서 실행해 주셔야 합니다.

### 1. NotebookLM 인증
터미널을 열고 아래 명령어를 실행하여 Google 로그인을 진행해 주세요.
```powershell
& "C:\Users\ksohw\AppData\Local\Programs\Python\Python312\Scripts\notebooklm-mcp-auth.exe"
```

### 2. Google Cloud 인증 (Stitch용)
터미널을 새로 열고(PATH 갱신용) 아래 명령어를 실행하여 Google Cloud 인증을 진행해 주세요.
```powershell
gcloud auth application-default login
```
*(Stitch 사용을 위해 추가로 `gcloud config set project [프로젝트ID]` 설정이 필요할 수 있습니다.)*

## 클라이언트 설정용 JSON 예시

인증 완료 후 사용하시는 AI 클라이언트(Claude Desktop 등)의 `mcpServers` 설정에 아래와 같이 추가할 수 있습니다.

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "C:\\Users\\ksohw\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\notebooklm-mcp.exe"
    },
    "stitch": {
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": ["-y", "@_davideast/stitch-mcp", "proxy"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "YOUR_PROJECT_ID"
      }
    }
  }
}
```
