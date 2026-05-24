import pandas as pd
import sys

file_path = r'c:\공유 20260413 1342\500.윈들리\발송대기-(기본)-검색결과(2026-05-06 08;58;03).xls'

try:
    # Try reading as HTML first (common for exported files)
    try:
        df = pd.read_html(file_path)[0]
        print("--- File read as HTML table ---")
    except:
        # Try reading as standard excel
        df = pd.read_excel(file_path)
        print("--- File read as Excel binary ---")
    
    print(f"Total Rows: {len(df)}")
    print("\n--- Column Names ---")
    print(df.columns.tolist())
    
    print("\n--- First 5 Rows (Selected Columns) ---")
    # Show some interesting columns if they exist
    cols_to_show = [c for c in df.columns if any(k in c for k in ['주문', '상품', '수량', '판매', '수취'])]
    if not cols_to_show:
        cols_to_show = df.columns[:5]
    
    print(df[cols_to_show].head(5))

except Exception as e:
    print(f"Error reading file: {e}")
    # Try reading as plain text just in case it's CSV/TSV
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            print("\n--- First 500 characters of raw content ---")
            print(f.read(500))
    except:
        pass
