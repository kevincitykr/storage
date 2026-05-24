# 🖥️ 새 PC 환경 구축 마스터 가이드 (New PC Setup Master Guide)

이 가이드는 최상의 개발 및 AI 업무 환경을 신속하게 구축하기 위한 표준 절차를 담고 있습니다. 새로운 워크스테이션을 세팅할 때 이 순서대로 진행하십시오.

---

## 1. 🚀 시스템 최적화 및 정리 (System Cleanup)

새 PC에 포함된 불필요한 번들 소프트웨어(Bloatware)를 정리하여 시스템 성능을 확보합니다.

- [x] **보안 프로그램 제거**: Norton 360 등 성능을 저하시키는 기본 백신 제거 (Windows Defender 권장)
- [x] **MSI Center 팝업 비활성화**: 
    - `DCv2.exe` 프로세스 종료
    - 불필요한 시작 프로그램 및 서비스 비활성화
- [x] **커스텀 테마 적용**: 프리미엄 미니멀리즘 배경화면 설정 (Navy/Gold Gradient)

---

## 2. 🛠️ 핵심 개발 환경 구축 (Development Environment)

모든 설치는 관리자 권한으로 진행하는 것을 권장합니다.

### 🔹 언어 및 런타임
- **Python 3.12.x**: 설치 시 `Add Python to PATH` 반드시 체크
- **Node.js (LTS)**: 최신 안정화 버전 설치
- **Git**: [Git for Windows](https://git-scm.com/) 설치 및 기본 설정
    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

### 🔹 IDE 및 확장 도구
- **VS Code**: 설치 후 필수 Extension 설치
    - `Python`, `Pylance`, `Jupyter`, `Prettier`, `GitLens`

---

## 3. 🤖 AI 및 미디어 도구 (AI & Media)

로컬 AI 환경 및 미디어 처리 엔진을 설정합니다.

- **Ollama**: 로컬 LLM 서버 실행용 (`gemma2`, `llama3` 등 모델 다운로드)
- **LM Studio**: GUI 기반 로컬 모델 테스트 도구
- **FFmpeg**: 영상/오디오 처리용 엔진 (환경 변수 `PATH` 등록 필수)

---

## 5. 🛠️ MCP (Model Context Protocol) 및 AI 도구 고도화

AI 에이전트의 능력을 확장하기 위한 설정입니다.

### 🧩 MCP 서버 설정 (`mcp_config.json`)
- **FileSystem**: 로컬 파일 시스템 제어 (`d:\Kevincity Share`)
- **Brave Search**: 실시간 웹 검색 기반 데이터 수집
- **GitHub**: 코드 및 지식 저장소 자동 관리
- **Stitch (Google)**: 디자인-투-코드 자동화 엔동

### 📓 NotebookLM (구글 지식 분석)
- **용도**: 복잡한 지식 베이스(`knowledge Base`) 심층 분석 및 인사이트 도출
- **방법**: `knowledge Base` 내의 .md 파일들을 NotebookLM 소스로 업로드하여 활용

### 🎨 Google Stitch (스티치)
- **용도**: AI 네이티브 UI 디자인 및 프런트엔드 코드 생성
- **작동**: `stitch-mcp`를 통해 생성된 디자인을 VS Code로 즉시 가져오기

---

## 6. 📂 파일 동기화 및 협업 (Sync & Productivity)

- **SyncTrayzor (Syncthing)**: `000_factory_core` 등 핵심 프로젝트 폴더 동기화
- **카카오톡**: PC 버전 설치
- **네이버 MYBOX**: 클라우드 백업 설정
- **Microsoft Office 2021 / 한컴오피스 2022**: 문서 작업 환경 구축

---

## 5. 🏗️ 프로젝트 프로젝트 초기화 (Project Init)

동기화 완료 후 프로젝트 폴더(`000_factory_core`)에서 다음 명령을 실행합니다.

```bash
# 1. 가상환경 생성 (권장)
python -m venv venv
.\venv\Scripts\activate

# 2. 필수 라이브러리 설치
pip install -r requirements.txt

# 3. 브라우저 자동화 설정
playwright install
```

---

## 💡 유용한 팁 (Tips)

> [!TIP]
> **터미널 커스터마이징**: PowerShell에서 `Oh My Posh`를 적용하면 더욱 쾌적한 터미널 환경을 사용할 수 있습니다.

> [!IMPORTANT]
> **환경 변수 확인**: 새로운 도구 설치 후 `echo $env:Path`를 통해 경로가 올바르게 등록되었는지 확인하십시오.

---
*마지막 업데이트: 2026-05-08 by Antigravity*
