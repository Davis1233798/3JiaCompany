from typing import Dict, List
from ..models.service import Service, ServiceType, ServiceStatus
from ..config.settings import config

class ServiceRepository:
    """
    服務倉儲
    遵循依賴倒轉原則和單一職責原則
    負責管理和提供服務實例
    """
    def __init__(self):
        """
        初始化服務倉儲
        從配置中載入服務
        """
        self._services: Dict[str, Service] = {}
        self._load_services()

    def _load_services(self):
        """
        從配置載入服務
        支援動態服務配置
        """
        for name, service_config in config.services.items():
            service_type = self._map_service_type(service_config.get('type', 'custom'))
            self._services[name] = Service(
                name=name,
                url=service_config['url'],
                service_type=service_type
            )

    def _map_service_type(self, type_str: str) -> ServiceType:
        """
        將字串映射到 ServiceType
        
        Args:
            type_str (str): 服務類型字串

        Returns:
            ServiceType: 對應的服務類型
        """
        type_mapping = {
            'render': ServiceType.RENDER,
            'vercel': ServiceType.VERCEL
        }
        return type_mapping.get(type_str.lower(), ServiceType.CUSTOM)

    def get_service(self, name: str) -> Service:
        """
        取得特定服務
        
        Args:
            name (str): 服務名稱

        Returns:
            Service: 服務實例
        """
        return self._services.get(name)

    def get_all_services(self) -> List[Service]:
        """
        取得所有服務
        
        Returns:
            List[Service]: 所有服務列表
        """
        return list(self._services.values())

    def update_service_status(self, name: str, status: ServiceStatus, error_message: str = None):
        """
        更新服務狀態
        
        Args:
            name (str): 服務名稱
            status (ServiceStatus): 新的服務狀態
            error_message (str, optional): 錯誤訊息. Defaults to None.
        """
        service = self._services.get(name)
        if service:
            service.update_status(status, error_message)

    def add_service(self, service: Service):
        """
        新增服務
        
        Args:
            service (Service): 要新增的服務
        """
        self._services[service.name] = service 