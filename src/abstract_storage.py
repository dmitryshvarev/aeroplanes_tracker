"""Абстрактный класс для работы с хранилищем данных."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AbstractStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем данных о самолетах.

    Определяет интерфейс для добавления, получения и удаления
    информации о самолетах из файлового хранилища.
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: Dict[str, Any]) -> None:
        """
        Добавляет информацию о самолете в хранилище.

        Args:
            aeroplane: Словарь с данными о самолете

        Raises:
            StorageError: При ошибках записи в хранилище
        """
        pass

    @abstractmethod
    def add_aeroplanes_list(self, aeroplanes_list: List[Dict[str, Any]]) -> None:
        """
        Добавляет список самолетов в хранилище.

        Args:
            aeroplanes_list: Список словарей с данными о самолетах

        Raises:
            StorageError: При ошибках записи в хранилище
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получает информацию о самолетах из хранилища по критериям.

        Args:
            criteria: Словарь с критериями фильтрации (ключ-значение)
                     Если None, возвращает все самолеты

        Returns:
            Список словарей с данными о самолетах
        """
        pass

    @abstractmethod
    def get_aeroplanes_by_origin_country(self, country: str) -> List[Dict[str, Any]]:
        """
        Получает самолеты по стране регистрации.

        Args:
            country: Страна регистрации

        Returns:
            Список словарей с данными о самолетах
        """
        pass

    @abstractmethod
    def delete_aircraft(self, criteria: Dict[str, Any]) -> int:
        """
        Удаляет информацию о самолетах из хранилища по критериям.

        Args:
            criteria: Словарь с критериями для удаления

        Returns:
            Количество удаленных записей
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очищает хранилище."""
        pass
