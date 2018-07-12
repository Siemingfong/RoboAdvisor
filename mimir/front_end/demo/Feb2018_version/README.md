### 說明

- 由於「價格、新聞爬蟲自動化」尚未串接，以下兩個檔案做為測試用途。
    - `price_data_sender.py`
        1. 以coindesk網站下載之ohlc-data csv檔案作為bitcoin價格資料。
        2. 清洗該資料。
        3. 存入mongodb。
    - `news_data_sender_technews.ipynb`
        1. 爬下technews btc新聞資料。
        2. 清洗該資料。
        3. 存入mongodb。
- `indicators.ipynb`是價格技術分析使用，未來可規劃至analysis部分。
