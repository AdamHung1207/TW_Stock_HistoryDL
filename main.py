import yfinance as yf
import pandas as pd
import time
import random
import os

# 設定存放 CSV 檔案的資料夾名稱
DATA_FOLDER = "TW_Stock"

# 確保資料夾存在
os.makedirs(DATA_FOLDER, exist_ok=True)

# 讀取 CSV 檔案，確保有 "ticker" 和 "name" 欄位
stock_list = pd.read_csv("stock_list.csv", encoding="utf-8-sig")

# 設定爬取區間（過去 15 年）
period = "15y"

def download_stock_data(ticker, name):
    """ 下載指定股票的完整歷史數據並存成 CSV """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        if history.empty:
            print(f"❌ {name}（{ticker}）沒有數據，請檢查代號是否正確")
            return

        filename = os.path.join(DATA_FOLDER, f"{ticker}_{name}.csv")
        history.to_csv(filename, encoding="utf-8-sig")
        print(f"✅ 已下載 {name}（{ticker}）的股價數據，存為 {filename}")

        # **隨機延遲 2~10 秒，避免請求過快被封鎖**
        delay = random.randint(2, 10)
        print(f"⏳ 休息 {delay} 秒...")
        time.sleep(delay)

    except Exception as e:
        print(f"❌ 下載 {name}（{ticker}）時發生錯誤：{e}")

def update_stock_data(ticker, name):
    """ 更新現有 CSV 檔案的股價數據 """
    filename = os.path.join(DATA_FOLDER, f"{ticker}_{name}.csv")
    
    if not os.path.exists(filename):
        print(f"⚠️ {name}（{ticker}）的資料不存在，將下載完整數據")
        download_stock_data(ticker, name)
        return

    try:
        existing_data = pd.read_csv(filename, encoding="utf-8-sig", index_col=0, parse_dates=True)
        last_date = existing_data.index[-1]  # 取得最後交易日期

        # 下載從最後交易日之後的新數據
        stock = yf.Ticker(ticker)
        new_history = stock.history(start=last_date)

        if new_history.empty:
            print(f"✅ {name}（{ticker}）已是最新，不需更新")
            return

        # 合併舊數據和新數據
        updated_data = pd.concat([existing_data, new_history])
        updated_data = updated_data[~updated_data.index.duplicated(keep='last')]  # 移除重複的日期

        # 儲存更新後的數據
        updated_data.to_csv(filename, encoding="utf-8-sig")
        print(f"🔄 已更新 {name}（{ticker}）的股價數據")

        # **隨機延遲 2~10 秒，避免請求過快被封鎖**
        delay = random.randint(2, 10)
        print(f"⏳ 休息 {delay} 秒...")
        time.sleep(delay)

    except Exception as e:
        print(f"❌ 更新 {name}（{ticker}）時發生錯誤：{e}")

# 執行完整下載或更新
def main():
    mode = input("請選擇模式：完整下載 (1) / 更新 (2)：")
    
    if mode == "1":
        print("📥 正在下載所有股票數據...")
        for index, row in stock_list.iterrows():
            download_stock_data(row["ticker"], row["name"])
        print("🎉 所有股票數據下載完成！")

    elif mode == "2":
        print("🔄 正在更新所有股票數據...")
        for index, row in stock_list.iterrows():
            update_stock_data(row["ticker"], row["name"])
        print("✅ 所有股票數據已更新！")

    else:
        print("❌ 輸入錯誤，請輸入 1 或 2！")

if __name__ == "__main__":
    main()
