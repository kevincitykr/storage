# 알리익스프레스 한국 발송 상품 수집 최적화 계획

K-Venue(한국 발송) 상품 수집의 한계를 극복하기 위해 세부 카테고리 순환 및 일반 카테고리 필터링 기능을 추가하고, 모든 작업의 기준이 될 **작업 표준(Work Standard)**을 수립합니다.

## User Review Required

> [!IMPORTANT]
> **K-Venue 탭 ID 순환 방식:** 현재 조사된 바로는 `tabId=1001`부터 순차적으로 카테고리가 구성되어 있습니다. 이를 자동으로 순환하며 수집할지, 혹은 사용자가 수집할 탭 범위를 지정할지 결정이 필요합니다. (기본값은 자동 순환으로 설정 예정)

> [!NOTE]
> **일반 카테고리 필터:** K-Venue 외의 일반 카테고리(예: 공구, 신발 등)에서도 한국 배송 상품만 골라내는 필터(`shpf_co=KR`)를 적용합니다. 이 경우 K-Venue 전용 상품이 아닌 일반 셀러의 한국 배송 상품도 포함될 수 있습니다.

## Proposed Changes

### [Component] Sourcing Bot Logic (final_sourcing_bot.py)

#### [MODIFY] [final_sourcing_bot.py](file:///e:/desktop_kevincity/500.%EC%9C%88%EB%93%A4%EB%A6%AC/%EC%95%8C%EB%A6%AC%EC%9D%B5%EC%8A%A4%ED%94%84%EB%A0%88%EC%8A%A4%20%EC%88%98%EC%A7%91%200422/final_sourcing_bot.py)

1.  **K-Venue 세부 메뉴 확장:**
    *   기존 K-Venue 메인 URL 외에 `tabId`를 포함한 세부 카테고리 리스트를 프리셋에 추가합니다.
    *   (1001: 추천, 1002: 가전, 1003: 식품, 1004: 생활용품 등)
2.  **자동 카테고리 순환(Auto-Rotation) 기능:**
    *   특정 URL에서 '새 상품 없음'이 연속 10회 발생할 경우, 다음 `tabId`로 자동 이동하거나 다음 프리셋 카테고리로 전환하는 로직을 구현합니다.
3.  **일반 카테고리 한국 필터 강제 적용:**
    *   사용자가 일반 카테고리(11~23번) 선택 시, URL 끝에 `&shpf_co=KR`을 강제로 붙여 중국 배송 상품을 원천 차단합니다.
4.  **로그 출력 강화:**
    *   현재 어떤 카테고리/URL을 분석 중인지, 왜 다음으로 넘어가는지 터미널에 명확히 기록합니다.

### [NEW] [work_standard.md](file:///C:/Users/ksohw/.gemini/antigravity/brain/8aa3805a-f510-4a08-9221-224396d5c433/work_standard.md)
*   향후 모든 컴퓨터에서 작업할 때 기준이 될 "수집 작업 표준 가이드"를 작성합니다.

---

## Verification Plan

### Automated Tests
1.  **URL 생성 검증:** 봇 실행 시 선택한 카테고리에 맞게 `shpf_co=KR` 또는 `tabId`가 포함된 URL이 정상 생성되는지 확인.
2.  **순환 로직 테스트:** 인위적으로 수집된 상품만 있는 페이지를 로드하여, 10회 실패 후 다음 카테고리로 정상 전환되는지 확인.

### Manual Verification
1.  **브라우저 직접 확인:** 봇이 접속한 URL을 브라우저에서 열어 실제로 "한국 발송" 상품들만 노출되는지 최종 확인.
