import os
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigManager:
    """
    配置管理器
    遵循依賴反轉原則，提供靈活的配置管理
    """
    _instance = None

    def __new__(cls):
        """
        單例模式，確保全域只有一個配置實例
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """
        載入環境變數配置
        支援多環境配置
        """
        load_dotenv()
        
        # Discord 配置
        self.discord_token = os.getenv('DISCORD_TOKEN', '')
        self.monitor_channel_id = int(os.getenv('MONITOR_CHANNEL_ID', 0))
        self.alert_channel_id = int(os.getenv('ALERT_CHANNEL_ID', 0))

        # 監控配置
        self.update_interval = int(os.getenv('UPDATE_INTERVAL', 5))
        self.timeout = int(os.getenv('TIMEOUT', 5))

        # 服務配置
        self.services: Dict[str, Dict[str, Any]] = {
            'Render Service 1': {
                'url': os.getenv('SERVICE_1_URL', 'https://service1.example.com/health'),
                'type': 'render'
            },
            'Render Service 2': {
                'url': os.getenv('SERVICE_2_URL', 'https://service2.example.com/health'),
                'type': 'render'
            },
            'Vercel Service 1': {
                'url': os.getenv('VERCEL_SERVICE_1_URL', 'https://vercel-service1.example.com/health'),
                'type': 'vercel'
            }
        }

    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """
        取得特定服務配置
        
        Args:
            service_name (str): 服務名稱

        Returns:
            Dict[str, Any]: 服務配置
        """
        return self.services.get(service_name, {})

    def validate_config(self) -> bool:
        """
        驗證配置是否完整
        
        Returns:
            bool: 配置是否有效
        """
        return bool(self.discord_token and self.monitor_channel_id)

# 全域配置實例
config = ConfigManager() 