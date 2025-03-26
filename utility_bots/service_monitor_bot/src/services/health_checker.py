import asyncio
import aiohttp
from typing import Optional
from ..models.service import ServiceStatus
from ..repositories.service_repository import ServiceRepository
from ..config.settings import config

class HealthChecker:
    """
    健康檢查服務
    遵循單一職責原則，專注於服務健康檢查
    """
    def __init__(self, service_repository: ServiceRepository):
        """
        初始化健康檢查服務
        
        Args:
            service_repository (ServiceRepository): 服務倉儲
        """
        self._service_repository = service_repository

    async def check_service_health(self, service_name: str) -> Optional[ServiceStatus]:
        """
        非同步檢查單一服務健康狀態
        
        Args:
            service_name (str): 服務名稱

        Returns:
            Optional[ServiceStatus]: 服務狀態
        """
        service = self._service_repository.get_service(service_name)
        if not service:
            return None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(service.url, timeout=config.timeout) as response:
                    if response.status == 200:
                        return ServiceStatus.ONLINE
                    return ServiceStatus.DEGRADED
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            return ServiceStatus.OFFLINE

    async def check_all_services_health(self):
        """
        非同步檢查所有服務健康狀態
        使用協程並行檢查
        """
        services = self._service_repository.get_all_services()
        tasks = [self.check_service_health(service.name) for service in services]
        
        results = await asyncio.gather(*tasks)
        
        for service, status in zip(services, results):
            if status is not None:
                self._service_repository.update_service_status(
                    service.name, 
                    status, 
                    error_message=f"Health check {'passed' if status == ServiceStatus.ONLINE else 'failed'}"
                )

    async def start_periodic_health_check(self):
        """
        啟動定期健康檢查
        """
        while True:
            await self.check_all_services_health()
            await asyncio.sleep(config.update_interval * 60)  # 轉換為秒 