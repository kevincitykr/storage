import pandas as pd
import sys

files = {
    "통합": r"N:\개인\20260413\덩치와쪼꼬미\##일기장\통합주문관리-(기본)-검색결과(2026-05-05 06;50;28).xlsx",
    "신규": r"N:\개인\20260413\덩치와쪼꼬미\##일기장\신규주문-(기본)-검색결과(2026-05-05 06;51;46).xlsx",
    "발송": r"N:\개인\20260413\덩치와쪼꼬미\##일기장\발송대기-(기본)-검색결과(2026-05-05 06;51;11).xlsx",
}

try:
    # 샵마인 엑셀은 가끔 상단에 타이틀이 있을 수 있으므로 첫 줄이 진짜 헤더인지 확인을 위해 
    # 기본 읽기를 해보고, 문제가 있다면 보완
    df_tong = pd.read_excel(files["통합"])
    df_new = pd.read_excel(files["신규"])
    df_ship = pd.read_excel(files["발송"])
    
    print("--- 1. 데이터 행/열 수 ---")
    print(f"통합주문관리: {df_tong.shape[0]}행, {df_tong.shape[1]}열")
    print(f"신규주문    : {df_new.shape[0]}행, {df_new.shape[1]}열")
    print(f"발송대기    : {df_ship.shape[0]}행, {df_ship.shape[1]}열")
    
    print(f"\n--- 2. 컬럼 목록 확인 (일부) ---")
    cols = list(df_tong.columns)
    print(cols[:20])
    
    # '주문번호' 컬럼명 찾기
    order_col = [c for c in cols if '주문번호' in str(c) or '주문번호(마켓)' in str(c) or '수집주문번호' in str(c)]
    
    if order_col:
        # 첫 번째로 매칭되는 주문번호 컬럼 사용
        col = order_col[0]
        print(f"\n--- 3. 기준 컬럼: '{col}' ---")
        
        tong_orders = set(df_tong[col].dropna().astype(str))
        
        if col in df_new.columns:
            new_orders = set(df_new[col].dropna().astype(str))
            missing_in_tong = new_orders - tong_orders
            print(f"통합에 신규주문건({len(new_orders)}개)이 모두 포함되어 있는가? {'예' if new_orders.issubset(tong_orders) else '아니오'}")
            if missing_in_tong:
                print(f"  -> 누락된 신규주문 번호 (최대 5개): {list(missing_in_tong)[:5]}")
        else:
            print(f"신규주문 파일에 '{col}' 컬럼이 없습니다.")
            
        if col in df_ship.columns:
            ship_orders = set(df_ship[col].dropna().astype(str))
            missing_in_tong2 = ship_orders - tong_orders
            print(f"통합에 발송대기건({len(ship_orders)}개)이 모두 포함되어 있는가? {'예' if ship_orders.issubset(tong_orders) else '아니오'}")
            if missing_in_tong2:
                print(f"  -> 누락된 발송대기 번호 (최대 5개): {list(missing_in_tong2)[:5]}")
        else:
            print(f"발송대기 파일에 '{col}' 컬럼이 없습니다.")
            
        # 통합 파일 내의 상태 컬럼 확인
        print(f"\n--- 4. 통합 파일의 '상태' 종류 ---")
        status_cols = [c for c in cols if '상태' in str(c) or '단계' in str(c)]
        for sc in status_cols:
            unique_status = df_tong[sc].dropna().unique()
            print(f"[{sc}] 종류: {list(unique_status)}")
            
    else:
        print("\n'주문번호' 관련 컬럼을 찾지 못했습니다. 컬럼명을 직접 확인해야 합니다.")
        
except Exception as e:
    import traceback
    print(f"에러 발생:\n{traceback.format_exc()}")
