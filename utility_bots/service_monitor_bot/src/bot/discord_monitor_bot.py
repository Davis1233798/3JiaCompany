import discord
import asyncio
from discord.ext import commands
from ..config.settings import config
from ..repositories.service_repository import ServiceRepository
from ..services.health_checker import HealthChecker
from ..services.notification_service import NotificationService

class ServiceMonitorBot(commands.Bot):
    """
    服務監控 Discord 機器人
    遵循依賴注入和單一職責原則
    """
    def __init__(self, *args, **kwargs):
        """
        初始化機器人
        設定必要的服務和倉儲
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents, *args, **kwargs)

        # 初始化服務和倉儲
        self.service_repository = ServiceRepository()
        self.health_checker = HealthChecker(self.service_repository)
        self.notification_service = NotificationService(self)

    async def setup_hook(self):
        """
        非同步設定鉤子
        在機器人啟動時執行初始化
        """
        await self.notification_service.setup_channels()
        self.loop.create_task(self._start_monitoring())

    async def _start_monitoring(self):
        """
        啟動服務監控
        """
        await self.wait_until_ready()
        
        while not self.is_closed():
            await self.health_checker.check_all_services_health()
            
            # 發送狀態訊息
            services = self.service_repository.get_all_services()
            await self.notification_service.send_service_status_message(services)
            
            # 檢查並發送警報
            for service in services:
                if service.status != ServiceStatus.ONLINE:
                    await self.notification_service.send_alert(service)
            
            # 等待下一次檢查
            await asyncio.sleep(config.update_interval * 60)

    @commands.command(name='status')
    async def check_status(self, ctx):
        """
        手動觸發狀態檢查命令
        
        Args:
            ctx (commands.Context): 命令上下文
        """
        await ctx.send("正在檢查服務狀態...")
        await self.health_checker.check_all_services_health()
        
        services = self.service_repository.get_all_services()
        status_message = self._generate_status_message(services)
        await ctx.send(status_message)

    def _generate_status_message(self, services):
        """
        生成狀態訊息
        
        Args:
            services (List[Service]): 服務列表

        Returns:
            str: 格式化的狀態訊息
        """
        message = "🌐 服務當前狀態 🌐\n\n"
        for service in services:
            message += f"{service.name}: {service.status.value}\n"
        return message

def create_bot():
    """
    建立機器人實例
    
    Returns:
        ServiceMonitorBot: 服務監控機器人實例
    """
    bot = ServiceMonitorBot()
    return bot 