from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AbstractAeroplanesAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов авиаданных,
    определяет интерфейс для получения информации о самолетах
    и географических данных стран.
    """

    @abstractmethod
    def _connect(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Приватный метод для подключения к API и отправки запроса.

        Args:
            url: URL для запроса
            params: Параметры запроса

        Returns:
            Ответ API в виде словаря

        Raises:
            APIError: При ошибках подключения или неверном статус-коде
        """
        pass

    @abstractmethod
    def get_country_coordinates(self, country: str) -> Dict[str, float]:
        """
        Получает координаты страны по ее названию.

        Args:
            country: Название страны

        Returns:
            Словарь с координатами: south, north, west, east

        Raises:
            CountryNotFoundError: Если страна не найдена
            APIError: При ошибках API
        """
        pass

    @abstractmethod
    def get_aeroplanes_in_area(self, bbox: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Получает информацию о самолетах в заданной географической области.

        Args:
            bbox: Словарь с координатами области (south, north, west, east)

        Returns:
            Список словарей с данными о самолетах

        Raises:
            APIError: При ошибках API
        """
        pass

    @abstractmethod
    def get_aeroplanes_by_country(self, country: str) -> List[Dict[str, Any]]:
        """
        Получает информацию о самолетах в воздушном пространстве страны.

        Объединяет вызовы get_country_coordinates и get_aeroplanes_in_area.

        Args:
            country: Название страны

        Returns:
            Список словарей с данными о самолетах
        """
        pass
