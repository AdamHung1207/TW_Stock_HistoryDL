import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import yaml
import re

def fetch_stock_list(mode, label, suffix):
    url = f"https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'big5'
    except Exception as e:
        print(f"❌ 錯誤：無法連線 {label}，原因：{e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all('tr')[1:]
    data = []

    print(f"📥 開始抓取 {label}，共 {len(rows)} 筆原始資料")
    for row in tqdm(rows, desc=label, ncols=80):
        cols = row.find_all('td')
        if len(cols) >= 1:
            text = cols[0].text.strip()
            if text and text[0].isdigit():
                parts = text.split('　')
                if len(parts) >= 2:
                    stock_id = parts[0].strip()
                    name = '　'.join(parts[1:]).strip()

                    # ✅ 強化版：過濾條件 ➜ 開頭為 4~5 位數字 + 可選英文字母
                    if re.match(r'^\d{4,5}[A-Z]*$', stock_id):
                        yahoo_code = f"{stock_id}.{suffix}"
                        data.append({
                            'stock_id': stock_id,
                            'name': name,
                            'market': label,
                            'yahoo_code': yahoo_code
                        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    sources = [
        (2, "TWSE", "TW"),       # 上市股票
        (4, "OTC", "TWO"),       # 上櫃股票
        (5, "ETF_TW", "TW"),     # 上市 ETF
        (6, "ETF_OTC", "TWO")    # 上櫃 ETF
    ]

    all_dfs = []
    for mode, label, suffix in sources:
        df = fetch_stock_list(mode, label, suffix)
        all_dfs.append(df)

    df_all = pd.concat(all_dfs, ignore_index=True)
    df_all = df_all.sort_values(by='stock_id').reset_index(drop=True)

    # 輸出 CSV
    df_all.to_csv("stock_list.csv", index=False, encoding="utf-8-sig")
    print(f"📄 已儲存 stock_list.csv（共 {len(df_all)} 檔）")

    # 輸出 YAML
    stock_list = df_all.to_dict(orient="records")
    with open("stock_list.yaml", "w", encoding="utf-8") as f:
        yaml.dump(stock_list, f, allow_unicode=True)
    print(f"📄 已儲存 stock_list.yaml（共 {len(stock_list)} 檔）")

    print("\n✅ 全部完成！股票 + ETF 已整理完畢（含強化過濾條件）")
