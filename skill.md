# 🖥️ 워크스테이션 관리 센터 (Workstation Management)

이 폴더는 시스템의 핵심 설정과 프로젝트 가이드를 포함하고 있습니다. 

> [!IMPORTANT]
> **[새 PC 세팅 마스터 가이드](file:///d:/Kevincity%20Share/000_factory_core/pc_setup_guide.md)**: 새로운 환경을 구축할 때는 이 파일을 최우선으로 참조하십시오.

---

## 1. 실시간 세팅 상태 (Current Status)

## 1. 필수 소프트웨어 설치 리스트

### 🔹 개발 환경 (가장 먼저 설치)
- [x] **Python 3.12.10**: [공식 다운로드](https://www.python.org/downloads/)
  - **주의**: 설치 시 `Add Python to PATH` 옵션 반드시 체크
- [x] **Git**: [다운로드](https://git-scm.com/)
- [x] **Node.js (LTS)**: [다운로드](https://nodejs.org/)
- [x] **VS Code**: [다운로드](https://code.visualstudio.com/)
  - 추천 확장도구: Python, Pylance, Jupyter

### 🔹 AI 및 라이브러리
- [ ] **LM Studio**: 로컬 대규모 언어 모델 실행용 (설치 확인 필요)
- [x] **Ollama**: 로컬 AI 서버 실행용
- [x] **FFmpeg**: 영상/오디오 처리 필수 도구 (환경 변수 등록 필요)

### 🔹 동기화 및 협업
- [x] **SyncTrayzor (Syncthing)**: 파일 동기화 필수
- [x] **카카오톡**: PC 버전 설치
- [ ] **네이버 MYBOX**: 클라우드 백업용
- [ ] **Chrome Remote Desktop**: 원격 제어용

### 🔹 업무 및 문서
- [ ] **Microsoft Office 2019**
- [ ] **한컴오피스 2022**
- [x] **브라우저**: Chrome, Whale 설치

### 🔹 깃허브(GitHub) 연결 설정
- [ ] **Git 최초 설정**:
    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```
- [ ] **인증**: 첫 `git push` 시 나타나는 브라우저 로그인 팝업으로 인증 완료.
- [ ] **토큰(PAT)**: 필요한 경우 GitHub Settings에서 발급 후 안전한 곳에 저장.

---

## 2. 프로젝트 환경 복구 (Sync 이후)

동기화가 완료되어 프로젝트 폴더(`000_factory_core`)가 생성되면, 해당 폴더에서 다음 과정을 진행하세요.

1.  **터미널(CMD/PowerShell) 열기**
2.  **필수 패키지 설치**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Playwright 설정** (자동화 스크립트 사용 시):
    ```bash
    playwright install
    ```

---

## 3. Syncthing 연결 방법
1.  새 PC에서 SyncTrayzor 실행
2.  `동작` -> `ID 보기`에서 기기 ID 복사
3.  기존 PC(현재 PC)의 Syncthing 관리 페이지에서 `원격 기기 추가` -> ID 입력
4.  공유할 폴더(`000_factory_core`) 설정에서 새 기기 체크

---

## 4. 인공지능(Antigravity)을 위한 이전 세션 문맥 (Context)
> [!NOTE]
> 새 컴퓨터에서 작업을 시작할 때, Antigravity에게 아래 내용을 읽으라고 하세요.

**세션 요약 (2026-05-08):**
1.  **목적**: 이전 PC의 환경을 완벽하게 새 PC로 이관하는 작업 진행 중.
2.  **동기화**: `000_factory_core` 폴더가 Syncthing을 통해 동기화됨.
3.  **프로그램**: Python 3.12.10, Node.js, VS Code, LM Studio, Ollama, FFmpeg 등이 핵심 환경임.
4.  **연결 정보**: GitHub은 HTTPS/GCM 방식을 사용하며, 새 컴퓨터에서 첫 시도 시 브라우저 로그인이 필요함.
5.  **현재 상태**: Syncthing ID를 교환하여 두 기기를 연결할 준비가 완료됨.

---

## 5. Syncthing 기기 정보 (Device IDs)
> [!IMPORTANT]
> **HQ (현재 컴퓨터/본체)**의 ID입니다. 다른 컴퓨터(킹덤, 새 PC 등)에서 연결할 때 사용하세요.
> 
> **HQ Device ID:** `UW5V5CO-T4XDF3O-Y522MUS-FR46E2D-GRFH5KT-FIYWM5S-NWDBKOQ-3A7ZYAL`

---
*최종 업데이트: 2026-05-08*
