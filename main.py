import yfinance as yf
import pandas as pd
import os

# 設定存放 CSV 檔案的資料夾名稱
DATA_FOLDER = "TW_Stock"

# 確保資料夾存在，如果不存在則建立資料夾
os.makedirs(DATA_FOLDER, exist_ok=True)

# 讀取 CSV 檔案，確保 CSV 檔案中有 "ticker" 和 "name" 欄位
stock_list = pd.read_csv("stock_list.csv", encoding="utf-8-sig")

# 設定資料抓取的起始日期（從 2000 年 1 月 1 日開始）
start_date = "2000-01-01"

def download_stock_data(ticker, name):
    """ 下載指定股票的完整歷史數據並存成 CSV 文件 """
    try:
        # 利用 yfinance 抓取股票資料
        stock = yf.Ticker(ticker)
        history = stock.history(start=start_date)

        # 如果抓取到的數據為空，提示用戶檢查股票代號
        if history.empty:
            print(f"❌ {name}（{ticker}）沒有數據，請檢查代號是否正確")
            return

        # 將資料存入指定資料夾中
        filename = os.path.join(DATA_FOLDER, f"{ticker}_{name}.csv")
        history.to_csv(filename, encoding="utf-8-sig")
        print(f"✅ 已下載 {name}（{ticker}）的股價數據，存為 {filename}")

    except Exception as e:
        # 錯誤處理，如果下載過程中發生問題，顯示錯誤訊息
        print(f"❌ 下載 {name}（{ticker}）時發生錯誤：{e}")

def update_stock_data(ticker, name):
    """ 更新現有 CSV 文件的股票數據 """
    filename = os.path.join(DATA_FOLDER, f"{ticker}_{name}.csv")
    
    # 如果文件不存在，執行完整下載
    if not os.path.exists(filename):
        print(f"⚠️ {name}（{ticker}）的資料不存在，將下載完整數據")
        download_stock_data(ticker, name)
        return

    try:
        # 讀取現有的數據
        existing_data = pd.read_csv(filename, encoding="utf-8-sig", index_col=0, parse_dates=True)
        last_date = existing_data.index[-1]  # 獲取最後交易日期

        # 從最後交易日後的日期開始抓取新數據
        stock = yf.Ticker(ticker)
        new_history = stock.history(start=last_date + pd.Timedelta(days=1))  # 從最後日期的下一天開始

        # 如果無新數據，表示數據已是最新
        if new_history.empty:
            print(f"✅ {name}（{ticker}）已是最新，不需更新")
            return

        # 合併舊數據和新數據，並移除重複的日期
        updated_data = pd.concat([existing_data, new_history])
        updated_data = updated_data[~updated_data.index.duplicated(keep='last')]  # 移除重複的日期

        # 儲存更新後的數據
        updated_data.to_csv(filename, encoding="utf-8-sig")
        print(f"🔄 已更新 {name}（{ticker}）的股價數據")

    except Exception as e:
        # 錯誤處理，如果更新過程中發生問題，顯示錯誤訊息
        print(f"❌ 更新 {name}（{ticker}）時發生錯誤：{e}")

def manual_download():
    """ 手動輸入股票代號和名稱進行下載 """
    try:
        # 要求使用者輸入股票代號和名稱
        ticker = input("請輸入股票代號 (例如：2330.TW)：").strip()
        name = input("請輸入股票名稱 (例如：台積電)：").strip()
        
        # 驗證輸入是否有效
        if not ticker or not name:
            print("❌ 股票代號和名稱不得為空！")
            return

        # 執行下載
        download_stock_data(ticker, name)
    
    except Exception as e:
        # 錯誤處理，顯示手動下載過程中的錯誤訊息
        print(f"❌ 手動補充下載發生錯誤：{e}")

def main():
    """ 主程式入口，提供用戶操作選單 """
    while True:
        # 顯示操作選單
        print("\n請選擇模式：")
        print("1. 完整下載")
        print("2. 更新")
        print("3. 手動補充下載")
        print("4. 結束程式")
        mode = input("請輸入選項 (1/2/3/4)：").strip()

        if mode == "1":
            # 模式 1：完整下載所有股票數據
            print("📥 正在下載所有股票數據...")
            for index, row in stock_list.iterrows():
                download_stock_data(row["ticker"], row["name"])
            print("🎉 所有股票數據下載完成！")

        elif mode == "2":
            # 模式 2：更新所有股票數據
            print("🔄 正在更新所有股票數據...")
            for index, row in stock_list.iterrows():
                update_stock_data(row["ticker"], row["name"])
            print("✅ 所有股票數據已更新！")

        elif mode == "3":
            # 模式 3：手動補充下載特定股票
            print("➕ 手動補充下載模式啟動")
            manual_download()
            print("✅ 手動補充下載完成！")

        elif mode == "4":
            # 模式 4：結束程式
            print("👋 程式已結束，感謝使用！")
            break

        else:
            # 非法輸入提示
            print("❌ 輸入錯誤，請輸入 1、2、3 或 4！")

if __name__ == "__main__":
    main()
