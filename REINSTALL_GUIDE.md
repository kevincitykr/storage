# 🛠️ System Rebuild Skill Guide

본 가이드는 시스템 포맷 후 **Factory Hub** 및 **AI 자동화 프로덕팅 환경**을 가장 빠르고 정확하게 복구하기 위한 매뉴얼입니다.

## 1. 💾 포맷 전 필수 백업 리스트
포맷을 시작하기 전에 아래 데이터는 반드시 별도 드라이브(D: 등)나 클라우드에 복사해 두세요.
- `d:\20260412 kevincity share\` 전체 폴더 (현재 모든 코드 및 설정 포함)
- `.env` 파일들 (API 키 등 민감 데이터)
- VS Code 설정 및 확장 프로그램 리스트 (동기화 권장)

---

## 2. 🚀 재설치 및 세팅 순서 (Recommended Order)

### [Step 1] 기본 개발 도구 설치
1.  **VS Code**: 가장 먼저 설치합니다.
2.  **Git**: [git-scm.com](https://git-scm.com/)에서 설치. 설치 시 기본 에디터를 VS Code로 설정하세요.
3.  **Node.js (LTS)**: 프로젝트 실행을 위해 필수입니다. 설치 후 터미널에서 `node -v`로 확인하세요.

### [Step 2] AI 인프라 구축 (LM Studio)
Ollama 에러를 피하기 위해 LM Studio를 가장 먼저 로컬 서버로 고정합니다.
1.  **LM Studio 설치**: [lmstudio.ai](https://lmstudio.ai/) 다운로드.
2.  **모델 다운로드**: 기존에 쓰시던 `gemma` 패밀리 또는 동급 모델 다운로드.
3.  **Local Server 설정**:
    - Port: `1234`
    - Cross-Origin Resource Sharing (CORS): `ON` (매우 중요)
    - `Start Server` 클릭하여 활성화.

### [Step 3] VS Code 확장 및 연결 (Connect AI)
1.  **Connect AI (v2.1.2) 설치**: VS Code 마켓플레이스에서 설치.
2.  **연결 설정**:
    - Provider: `OpenAI Compatible`
    - Base URL: `http://localhost:1234/v1`
    - API Key: `lm-studio` (임의값 입력)

### [Step 4] 프로젝트 복구 및 의존성 설치
1.  **프로젝트 폴더 열기**: `d:\20260412 kevincity share\000_factory_core` 등.
2.  **의존성 재설치**: 각 프로젝트 폴더 터미널에서 아래 명령 실행.
    ```powershell
    npm install
    ```
3.  **Config 확인**: `config.json` 파일의 `baseUrl`이 `http://127.0.0.1:1234/v1`인지 확인.

---

## 3. 🔍 에러 재발 방지 체크포인트
- **포트 충돌 확인**: 포맷 후 다른 프로그램이 `11434`(Ollama) 혹은 `1234`(LM Studio) 포트를 점유하지 않는지 확인하세요.
- **환경 변수 초기화**: 시스템 환경 변수에 `OLLAMA_HOST` 등이 남아있는지 확인하고 있으면 삭제하세요.
- **캐시 삭제**: 이전 설정이 꼬인다면 `%AppData%\Code\User\globalStorage` 내의 확장 프로그램 데이터를 정리하는 것이 좋습니다.

---

## 4. ✅ 정상 작동 확인 테스트
1.  LM Studio에서 서버를 켭니다.
2.  브라우저에서 `http://localhost:1234/v1/models` 접속 시 모델 리스트가 JSON으로 나오면 성공입니다.
3.  VS Code 내 `Connect AI`에서 메시지를 보내 로컬 모델이 응답하는지 최종 확인합니다.
