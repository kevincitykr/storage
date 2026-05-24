# Suno Factory Pro API v4.0 구현 계획

## 1. 개요
현재의 `suno_factory_server_v35.py`를 고도화하여, Melodist Seoul 브랜드의 핵심 엔진 역할을 수행할 수 있는 전문적인 API 서버를 구축합니다.

## 2. 주요 기능
### 2.1. 고도화된 가사 생성 (Gemini Pro Integrated)
- `gemini_pro` 패키지의 `GeminiClient`를 사용하여 다중 API 키 관리.
- `gemini-1.5-flash` 등 최신 모델 우선 사용 및 자동 폴백.

### 2.2. 데이터 영구 저장 (Archive System)
- 생성된 모든 가사와 트랙 정보를 `tracks_archive.json`에 저장.
- 최근 생성된 곡뿐만 아니라 과거 이력 조회 가능.

### 2.3. 시스템 제어 API
- `/trends`: 실시간 유튜브 트렌드 데이터 제공.
- `/generate`: 병렬 고속 가사 생성.
- `/archive`: 저장된 트랙 리스트 조회.
- `/system/status`: 서버 부하 및 API 키 상태 모니터링.

## 3. 기술 스택
- **Framework**: FastAPI (Asynchronous Support)
- **Engine**: Gemini 1.5 Flash
- **Logic**: Python 3.10+
- **Security**: CORS Middleware & Environment Variables

## 4. 단계별 실행 계획
1. **환경 설정**: `gemini_pro` 패키지 연동 확인.
2. **서버 개발**: `suno_api_v4.py` 신규 작성.
3. **데이터 로직**: JSON 기반의 아카이브 시스템 구축.
4. **테스트**: Swagger UI를 통한 엔드포인트 검증.
