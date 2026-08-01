"""Класс для работы с JSON-файлами как хранилищем данных."""

import json
import os
from typing import Any, Dict, List, Optional

from src.abstract_storage import AbstractStorage
from src.exceptions import StorageError


class JSONStorage(AbstractStorage):
    """
    Класс для работы с JSON-файлами как хранилищем данных о самолетах.

    Приватные атрибуты:
        _filename: Имя JSON-файла
        _data: Кэш данных из файла
    """

    __slots__ = ("_filename", "_data")

    def __init__(self, filename: str = "../data/aeroplanes_data.json") -> None:
        """
        Инициализация хранилища.

        Args:
            filename: Имя JSON-файла (по умолчанию aeroplanes_data.json)
        """
        self._filename: str = filename
        self._data: List[Dict[str, Any]] = []
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из JSON-файла в кэш."""
        if not os.path.exists(self._filename):
            self._data = []
            return

        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except json.JSONDecodeError:
            # Если файл пустой или поврежден, начинаем с пустого списка
            self._data = []
        except Exception as e:
            raise StorageError(f"Ошибка при загрузке данных из файла: {e}")

    def _save_data(self) -> None:
        """Сохраняет данные из кэша в JSON-файл."""
        try:
            # Создаем директорию, если нужно
            os.makedirs(os.path.dirname(self._filename) or ".", exist_ok=True)

            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise StorageError(f"Ошибка при сохранении данных в файл: {e}")

    def _is_duplicate(self, aeroplane: Dict[str, Any]) -> bool:
        """
        Проверяет, есть ли уже такой самолет в хранилище.

        Args:
            aeroplane: Словарь с данными о самолете

        Returns:
            True если самолет уже существует, иначе False
        """
        for existing in self._data:
            # Считаем дубликатом по сочетанию callsign и icao24
            if existing.get("callsign") == aeroplane.get("callsign") and existing.get("icao24") == aeroplane.get(
                "icao24"
            ):
                return True
        return False

    def add_aeroplane(self, aeroplane: Dict[str, Any]) -> None:
        """
        Добавляет информацию о самолете в хранилище.

        Args:
            aeroplane: Словарь с данными о самолете

        Raises:
            StorageError: При ошибках записи в хранилище
        """
        if not self._is_duplicate(aeroplane):
            self._data.append(aeroplane)
            self._save_data()

    def add_aeroplanes_list(self, aeroplanes_list: List[Dict[str, Any]]) -> None:
        """
        Добавляет список самолетов в хранилище.

        Args:
            aeroplanes_list: Список словарей с данными о самолетах

        Raises:
            StorageError: При ошибках записи в хранилище
        """
        added = False
        for aeroplane in aeroplanes_list:
            if not self._is_duplicate(aeroplane):
                self._data.append(aeroplane)
                added = True

        if added:
            self._save_data()

    def get_aeroplanes(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получает информацию о самолетах из хранилища по критериям.

        Args:
            criteria: Словарь с критериями фильтрации (ключ-значение)
                     Если None, возвращает все самолеты

        Returns:
            Список словарей с данными о самолетах
        """
        if criteria is None:
            return self._data.copy()

        result = []
        for aeroplane in self._data:
            match = True
            for key, value in criteria.items():
                if key not in aeroplane or aeroplane[key] != value:
                    match = False
                    break
            if match:
                result.append(aeroplane)

        return result

    def get_aeroplanes_by_origin_country(self, country: str) -> List[Dict[str, Any]]:
        """
        Получает самолеты по стране регистрации.

        Args:
            country: Страна регистрации

        Returns:
            Список словарей с данными о самолетах
        """
        return [a for a in self._data if a.get("origin_country", "").lower() == country.lower()]

    def delete_aeroplanes(self, criteria: Dict[str, Any]) -> int:
        """
        Удаляет информацию о самолетах из хранилища по критериям.

        Args:
            criteria: Словарь с критериями для удаления

        Returns:
            Количество удаленных записей
        """
        initial_count = len(self._data)
        self._data = [
            aeroplane for aeroplane in self._data if not all(aeroplane.get(k) == v for k, v in criteria.items())
        ]
        deleted_count = initial_count - len(self._data)

        if deleted_count > 0:
            self._save_data()

        return deleted_count

    def clear(self) -> None:
        """Очищает хранилище."""
        self._data = []
        self._save_data()

    def get_all(self) -> List[Dict[str, Any]]:
        """Возвращает все данные из хранилища."""
        return self._data.copy()

    def count(self) -> int:
        """Возвращает количество записей в хранилище."""
        return len(self._data)
