from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class ServiceType(Enum):
    """
    服務類型枚舉
    遵循開放-封閉原則，易於擴展
    """
    RENDER = auto()
    VERCEL = auto()
    CUSTOM = auto()

class ServiceStatus(Enum):
    """
    服務狀態枚舉
    提供清晰的狀態表示
    """
    ONLINE = '✅'
    OFFLINE = '❌'
    DEGRADED = '⚠️'

@dataclass
class Service:
    """
    服務實體類
    遵循單一職責原則，僅負責儲存服務相關資訊
    """
    name: str
    url: str
    service_type: ServiceType
    status: ServiceStatus = ServiceStatus.OFFLINE
    last_checked: Optional[str] = None
    error_message: Optional[str] = None

    def update_status(self, new_status: ServiceStatus, error_message: Optional[str] = None):
        """
        更新服務狀態
        
        Args:
            new_status (ServiceStatus): 新的服務狀態
            error_message (Optional[str], optional): 錯誤訊息. Defaults to None.
        """
        self.status = new_status
        self.error_message = error_message 