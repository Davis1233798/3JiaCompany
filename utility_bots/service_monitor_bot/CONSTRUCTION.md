# 服務監控 Discord 機器人 - 開發文件

## 架構設計原則

本專案遵循 SOLID 設計原則：

1. 單一職責原則 (SRP)
   - 每個類別和模組都有明確且單一的職責
   - 例如：`HealthChecker` 僅負責服務健康檢查
   - `NotificationService` 僅負責發送通知

2. 開放-封閉原則 (OCP)
   - 使用枚舉和抽象類別，便於擴展
   - `ServiceType` 和 `ServiceStatus` 可輕鬆新增新的類型
   - 服務檢查和通知邏輯可以輕鬆擴展

3. 依賴反轉原則 (DIP)
   - 高層模組不依賴低層模組，兩者都依賴抽象
   - 使用依賴注入，解耦合各個元件
   - 例如：`HealthChecker` 依賴 `ServiceRepository` 的抽象介面

## 模組設計

### `models/service.py`
- 定義服務實體模型
- 使用 `dataclass` 簡化資料類別
- 提供狀態更新方法

### `config/settings.py`
- 集中管理配置
- 支援環境變數配置
- 單例模式確保全域配置一致性

### `repositories/service_repository.py`
- 管理服務實例的倉儲
- 提供服務的增刪改查
- 支援動態服務配置

### `services/health_checker.py`
- 非同步檢查服務健康狀態
- 支援並行檢查多個服務
- 使用協程提高效能

### `services/notification_service.py`
- 管理 Discord 通知邏輯
- 支援狀態訊息和警報訊息
- 靈活的通知頻道設定

### `bot/discord_monitor_bot.py`
- 整合所有服務的主機器人類別
- 提供服務監控的核心邏輯
- 支援手動狀態檢查命令

## 非同步設計

- 使用 `asyncio` 實現非阻塞的服務檢查
- 並行檢查多個服務，提高效能
- 定期執行健康檢查和通知

## 錯誤處理

- 優雅地處理服務檢查的異常
- 提供詳細的錯誤訊息
- 支援服務狀態的動態變更

## 未來擴展方向

1. 支援更多服務類型
2. 增加更複雜的健康檢查邏輯
3. 提供更多監控指令
4. 支援更客製化的通知設定 