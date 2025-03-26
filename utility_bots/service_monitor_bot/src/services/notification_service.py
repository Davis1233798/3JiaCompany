import discord
from typing import List, Optional
from ..models.service import Service, ServiceStatus
from ..config.settings import config

class NotificationService:
    """
    通知服務
    遵循單一職責原則，專注於服務狀態通知
    """
    def __init__(self, client: discord.Client):
        """
        初始化通知服務
        
        Args:
            client (discord.Client): Discord 客戶端
        """
        self._client = client
        self._monitor_channel: Optional[discord.TextChannel] = None
        self._alert_channel: Optional[discord.TextChannel] = None

    async def setup_channels(self):
        """
        設定監控和警報頻道
        """
        self._monitor_channel = await self._client.fetch_channel(config.monitor_channel_id)
        self._alert_channel = await self._client.fetch_channel(config.alert_channel_id) if config.alert_channel_id else None

    async def send_service_status_message(self, services: List[Service]):
        """
        發送服務狀態訊息
        
        Args:
            services (List[Service]): 服務列表
        """
        if not self._monitor_channel:
            return

        status_message = self._generate_status_message(services)
        try:
            await self._monitor_channel.send(status_message)
        except discord.HTTPException as e:
            print(f"發送訊息失敗: {e}")

    def _generate_status_message(self, services: List[Service]) -> str:
        """
        生成服務狀態訊息
        
        Args:
            services (List[Service]): 服務列表

        Returns:
            str: 格式化的狀態訊息
        """
        message = "🌐 服務監控狀態 🌐\n\n"
        message += "```\n服務名稱\t\t狀態\t\t詳細資訊\n"
        message += "-" * 50 + "\n"

        for service in services:
            status_emoji = service.status.value
            error_info = service.error_message or "無錯誤"
            message += f"{service.name}\t\t{status_emoji}\t\t{error_info}\n"

        message += "```"
        return message

    async def send_alert(self, service: Service):
        """
        發送服務警報
        
        Args:
            service (Service): 服務實例
        """
        if not self._alert_channel or service.status == ServiceStatus.ONLINE:
            return

        alert_message = self._generate_alert_message(service)
        try:
            await self._alert_channel.send(alert_message)
        except discord.HTTPException as e:
            print(f"發送警報失敗: {e}")

    def _generate_alert_message(self, service: Service) -> str:
        """
        生成警報訊息
        
        Args:
            service (Service): 服務實例

        Returns:
            str: 警報訊息
        """
        return (
            f"🚨 服務異常警報 🚨\n"
            f"服務名稱: {service.name}\n"
            f"當前狀態: {service.status.value}\n"
            f"錯誤詳情: {service.error_message or '未知錯誤'}\n"
            f"檢查 URL: {service.url}"
        ) 