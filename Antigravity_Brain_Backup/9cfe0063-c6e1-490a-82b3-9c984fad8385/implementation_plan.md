# MCP 서버 연결 계획 (NotebookLM & Stitch)

사용자님의 요청에 따라 **NotebookLM**과 **Stitch** 두 가지 MCP(Model Context Protocol) 서버를 연결하기 위한 계획입니다.

## 사용자 확인 필요 사항 (User Review Required)

현재 환경 분석 결과, MCP 서버 실행에 필요한 일부 도구가 설치되어 있지 않거나 환경 변수에 등록되어 있지 않습니다. 진행을 위해 다음 사항을 확인해 주세요.

> [!IMPORTANT]
> 1. **사용하실 AI 클라이언트:** 어떤 프로그램(예: Claude Desktop, Cursor, Windsurf, Cline 등)에 MCP를 연결하실지 알려주세요.
> 2. **Prerequisites 설치:**
>    - **NotebookLM MCP:** Python은 설치되어 있으나 `uv`가 없습니다. `pip`를 통해 설치할 수 있습니다.
>    - **Stitch MCP:** `Node.js` 및 `Google Cloud CLI (gcloud)`가 설치되어 있지 않습니다. Stitch 사용을 위해 설치가 필요합니다.

## 오픈 질문 (Open Questions)

> [!NOTE]
> - Stitch MCP를 사용하려면 **Google Cloud Project ID**가 필요하며, `gcloud auth application-default login`을 통한 인증이 필요합니다. 준비된 프로젝트가 있으신가요?

## 제안하는 변경 사항 (Proposed Changes)

### 1. NotebookLM MCP 서버 설정

`wonseokjung/notebooklm-mcp` 기반의 서버를 설정합니다.

#### 설치 및 인증
```bash
# Python 패키지 설치
pip install notebooklm-mcp-server

# 인증 실행 (Google 로그인)
notebooklm-mcp-auth
```

#### 클라이언트 설정 (JSON 예시)
```json
"notebooklm": {
  "command": "python",
  "args": ["-m", "notebooklm_mcp_server"]
}
```

---

### 2. Stitch MCP 서버 설정

Google의 Stitch API를 연동합니다.

#### 필수 도구 설치
- [Node.js](https://nodejs.org/) 설치 필요
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) 설치 필요

#### 인증 및 설정
```bash
# Google Cloud 인증
gcloud auth application-default login
gcloud config set project [YOUR_PROJECT_ID]
```

#### 클라이언트 설정 (JSON 예시)
```json
"stitch": {
  "command": "npx",
  "args": ["-y", "@_davideast/stitch-mcp", "proxy"],
  "env": {
    "GOOGLE_CLOUD_PROJECT": "[YOUR_PROJECT_ID]"
  }
}
```

## 검증 계획 (Verification Plan)

### 수동 검증
1. 클라이언트 재시작 후 MCP 서버 연결 상태 확인.
2. NotebookLM 도구 호출 테스트 (예: "내 노트북 목록 보여줘").
3. Stitch 도구 호출 테스트.
