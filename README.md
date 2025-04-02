在GitHub上找了一輪，滿多連線至台灣證交所要爬蟲的資料都會執行錯誤，也很懶得找原作者詢問為什麼，問了ChatGPT跟其它AI也是鬼打牆。

那我就自己叫ChatGPT寫一個吧！！！

# 設定存放 CSV 檔案的資料夾名稱
DATA_FOLDER = "TW_Stock"

下載之後會存放在一個名為TW.Stock的資料夾下。

# 讀取 CSV 檔案，確保有 "ticker" 和 "name" 欄位
stock_list = pd.read_csv("stock_list.csv", encoding="utf-8-sig")

需要一個名為stock_list.csv的檔案，裡面有所有台股的代號及名稱。(代號後面好像都要加.tw的樣子)

另外要確定這個檔案裡有ticker對應是股票代號.tw，name對應是股票名稱。

如果有這個檔案，但名稱不一樣，就叫ChatGPT幫你改一下吧。

如果沒有，就下載我的拿去用吧，這也是我用別的GitHub下載下來的。

# 設定爬取區間（過去 15 年）
period = "15y"

本程式以當天執行的日期，往前推15年，如果是要指定日期的話，請叫ChatGPT改。

# **隨機延遲 2~10 秒，避免請求過快被封鎖**
delay = random.randint(2, 10)
print(f"⏳ 休息 {delay} 秒...")
time.sleep(delay)

怕真的出什麼意外會擋，所以請ChatGPT設置一個延遲讀取，隨時2~10秒，想改的話就把2跟10改成你想要字就好。

這個就不用叫ChatGPT來了。

# 執行完整下載或更新
def main():
    mode = input("請選擇模式：完整下載 (1) / 更新 (2)：")

為了不想要每次都要跑這麼久的下載，也叫ChatGPT去比對資料，只要更新短缺的日期即可。

![image](https://github.com/user-attachments/assets/4ba67ea5-5ba8-46fb-80f2-3370e517ebe1)

在跑的畫面是這樣，我執行起來沒有問題。

有問題的話一律問ChatGPT，這是他寫給我的。
