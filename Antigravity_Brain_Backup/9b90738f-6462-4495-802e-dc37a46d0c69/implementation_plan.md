# 영구 기피단어(Forbidden Keywords) 관리 시스템 계획

매번 이메일을 분석하는 번거로움 없이, 한 번 추출된 위험 단어들을 '마스터 기피단어 리스트'로 관리하여 모든 수집 도구에서 공유합니다.

## User Review Required

> [!IMPORTANT]
> **리스트 관리**: 이메일에서 자동으로 추출된 단어 외에도, 사용자가 직접 수동으로 기피단어를 추가/삭제할 수 있도록 `forbidden_master_list.json` 형식을 단순하게 유지합니다.

## Proposed Changes

### [Component] Master Keyword Manager

#### [NEW] [forbidden_master_list.json](file:///d:/20260412%20kevincity%20share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/forbidden_master_list.json)
- 브랜드명, 금지 문구 등을 통합 관리하는 JSON DB.
- 형식: `{"브랜드/키워드": "추출 사유(이메일/수동)"}`

#### [MODIFY] [legal_issue_extractor.py](file:///D:/Goodtobehere%EA%B3%B5%EC%9C%A0%ED%8F%B4%EB%8D%94/%EC%9D%B4%EB%A9%94%EC%9D%BC%EA%B4%80%EB%A6%AC%EC%8B%9C%EC%8A%A4%ED%85%9C/legal_issue_extractor.py)
- 추출 결과를 기존 리스트와 **병합(Merge)**하여 누적 저장하도록 수정.

### [Component] Integrated Scrapers

#### [MODIFY] [deep_filter_scraper.py](file:///d:/20260412%20kevincity%20share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/deep_filter_scraper.py)
- `forbidden_master_list.json`을 읽어 모든 스캔 과정에 반영.

#### [MODIFY] [deep_scraper_v2.js](file:///d:/20260412%20kevincity%20share/500.%EC%9C%88%EB%93%A4%EB%A6%AC/deep_scraper_v2.js)
- 북마클릿 코드 내부에 최신 기피단어 리스트를 포함시키거나, 로컬 파일에서 읽어올 수 있도록 구조 개선.

## Verification Plan

1. **병합 테스트**: 새 메일 수집 후 `extractor` 실행 시 기존 리스트가 보존되고 새 단어만 추가되는지 확인.
2. **필터링 테스트**: 수집기가 마스터 리스트의 단어를 기반으로 상품을 정확히 차단하는지 확인.
