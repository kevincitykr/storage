# 유튜브 자동화 프로젝트 히스토리

## 프로젝트 개요
- **목적**: AI 도구(NotebookLM, Gemini 등)를 활용한 유튜브 영상 제작 자동화 및 수익화 전략 실행.
- **벤치마킹 타겟**: 심리학 니치 (Psych2Go 채널)
- **주요 도구**: NotebookLM, Gemini, Vrew, Pollinations AI

## 작업 로그 (2026-04-13)
1. **벤치마킹 채널 선정 및 URL 추출**: Psych2Go 채널에서 최근/인기 영상 12개의 URL 추출 완료.
2. **NotebookLM 설정**: `YouTube Psychology Automation Project` 노트북 생성 및 12개 URL 소스로 추가.
3. **인증 처리**: NotebookLM MCP 인증 에러 해결을 위해 `nlm login --force` 실행 및 성공.
4. **인덱싱 대기 및 결과 분석**: 텍스트 소스를 활용하여 채널명 5개, 영상 아이디어 20개, 상세 대본 개요 생성 완료.
5. **자동화 툴 설계 (New)**: 
    - 파이썬 기반 `content_factory.py` 프로토타입 개발.
    - 6단계 공정의 상세 규격을 담은 `workflow_config.json` 설계 완료.
    - 각 단계별 AI 프롬프트 및 파일 저장 시스템 규격화.
6. **컨텐츠 품질 고도화 (QA)**: 
    - 기존 요약형 대본의 한계를 인지하고, 5분 분량(약 3,000자 수준)의 심층 다큐멘터리 대본으로 전면 재작성.
    - NotebookLM을 통해 DMN 메커니즘, 4F 반응 조절 등 전문적 근거 보강.
    - 5분 롱폼 오디오 생성 작업 재착수.
