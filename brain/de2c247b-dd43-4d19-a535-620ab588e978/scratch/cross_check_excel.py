import pandas as pd
import sys

file_path = r'c:\공유 20260413 1342\500.윈들리\발송대기-(기본)-검색결과(2026-05-06 08;58;03).xls'

def read_with_encoding(path):
    encodings = ['cp949', 'euc-kr', 'utf-8', 'utf-16']
    for enc in encodings:
        try:
            # Try reading as HTML first with specific encoding
            dfs = pd.read_html(path, encoding=enc)
            if dfs:
                print(f"--- Successfully read as HTML with {enc} ---")
                return dfs[0]
        except Exception:
            continue
    
    try:
        # If HTML fails, try standard excel (which handles its own encoding usually)
        df = pd.read_excel(path)
        print("--- Successfully read as Excel binary ---")
        return df
    except Exception as e:
        print(f"Error reading as excel: {e}")
        return None

df = read_with_encoding(file_path)

if df is not None:
    # Rename columns if they are messy
    # Common columns in these files: 주문일시, 주문번호, 상품명, 수량, 수취인명, 판매자상품코드
    print(f"Total Rows: {len(df)}")
    
    # Try to find relevant columns even if headers are slightly different
    important_keywords = ['주문', '상품', '수량', '수취', '코드', '결제']
    found_cols = [c for c in df.columns if any(k in str(c) for k in important_keywords)]
    
    print("\n--- Order Data (Top 20 for matching) ---")
    print(df[found_cols].head(20).to_string())
else:
    print("Failed to read the file correctly.")
