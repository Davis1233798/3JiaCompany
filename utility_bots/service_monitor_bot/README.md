# Discord 服務監控機器人

這是一個用於監控多個服務健康狀態的 Discord 機器人，特別支援 Render 和 Vercel 服務。

## 功能特點

- 監控多個服務的健康狀態
- 自動定期更新狀態訊息
- 支援 Render 和 Vercel 服務
- 錯誤通知功能
- 可自定義監控間隔
- 狀態變化通知

## 安裝步驟

1. 克隆此專案
2. 安裝依賴套件：
   ```bash
   pip install -r requirements.txt
   ```
3. 複製 `.env.example` 到 `.env` 並設置必要的環境變數：
   ```
   DISCORD_TOKEN=你的Discord機器人Token
   MONITOR_CHANNEL_ID=監控頻道ID
   ALERT_CHANNEL_ID=通知頻道ID
   UPDATE_INTERVAL=5
   TIMEOUT=5
   SERVICE_1_URL=https://service1.example.com/health
   SERVICE_2_URL=https://service2.example.com/health
   VERCEL_SERVICE_1_URL=https://vercel-service1.example.com/health
   VERCEL_SERVICE_2_URL=https://vercel-service2.example.com/health
   ```

## 使用方法

1. 設置環境變數
2. 運行機器人：
   ```bash
   python main.py
   ```

## 配置說明

- `config.py`: 包含所有配置設定
- `main.py`: 主程式
- `utils.py`: 工具函數
- `.env`: 環境變數設定

## 注意事項

- 請確保所有服務的健康檢查端點都正確設置
- 建議定期備份設定檔
- 監控頻道需要機器人的讀寫權限 