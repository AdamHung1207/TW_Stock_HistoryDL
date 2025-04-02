import yfinance as yf
import pandas as pd
import time
import random

# 讀取 CSV 檔案，確保有 "ticker" 和 "name" 欄位
stock_list = pd.read_csv("stock_list.csv", encoding="utf-8-sig")

# 設定爬取區間（過去 15 年）
period = "15y"

def download_stock_data(ticker, name):
    """ 下載指定股票的歷史數據並存成 CSV """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        if history.empty:
            print(f"❌ {name}（{ticker}）沒有數據，請檢查代號是否正確")
            return

        filename = f"{ticker}_{name}.csv"  # 檔名包含股票名稱
        history.to_csv(filename, encoding="utf-8-sig")
        print(f"✅ 已下載 {name}（{ticker}）的股價數據，存為 {filename}")

        # **隨機延遲 2~10 秒，避免請求過快被封鎖**
        delay = random.randint(2, 5)
        print(f"⏳ 休息 {delay} 秒...")
        time.sleep(delay)

    except Exception as e:
        print(f"❌ 下載 {name}（{ticker}）時發生錯誤：{e}")

# 逐一下載所有股票數據
for index, row in stock_list.iterrows():
    download_stock_data(row["ticker"], row["name"])

print("🎉 所有股票數據下載完成！")
