"""Класс для работы с CSV-файлами как хранилищем данных."""

import csv
import os
from typing import Any, Dict, List, Optional

from src.abstract_storage import AbstractStorage
from src.exceptions import StorageError


class CSVStorage(AbstractStorage):
    """
    Класс для работы с CSV-файлами как хранилищем данных о самолетах.

    Приватные атрибуты:
        _filename: Имя CSV-файла
        _fieldnames: Заголовки колонок
    """

    __slots__ = ("_filename", "_fieldnames")

    def __init__(self, filename: str = "data/aeroplanes_data.csv") -> None:
        """
        Инициализация хранилища.

        Args:
            filename: Имя CSV-файла (по умолчанию aeroplanes_data.csv)
        """
        self._filename: str = filename
        self._fieldnames: List[str] = [
            "callsign",
            "origin_country",
            "velocity",
            "altitude",
            "latitude",
            "longitude",
            "icao24",
        ]
        self._init_file()

    def _init_file(self) -> None:
        """Инициализирует CSV-файл с заголовками, если файл не существует."""
        if not os.path.exists(self._filename):
            os.makedirs(os.path.dirname(self._filename) or ".", exist_ok=True)
            with open(self._filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self._fieldnames)
                writer.writeheader()

    def _load_data(self) -> List[Dict[str, Any]]:
        """Загружает данные из CSV-файла."""
        data = []
        try:
            with open(self._filename, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Преобразуем строки в соответствующие типы
                    converted_row = {}
                    for key, value in row:
                        if value == "" or value is None:
                            converted_row[key] = None
                        elif key in ["velocity", "altitude", "latitude", "longitude"]:
                            try:
                                converted_row[key] = float(value)
                            except ValueError:
                                converted_row[key] = None
                        else:
                            converted_row[key] = value
                    data.append(converted_row)
        except Exception as e:
            raise StorageError(f"Ошибка при загрузке данных из CSV: {e}")

        return data

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        """Сохраняет данные в CSV-файл."""
        try:
            with open(self._filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self._fieldnames)
                writer.writeheader()
                for row in data:
                    # Преобразуем None в пустые строки для CSV
                    csv_row = {k: "" if v is None else v for k, v in row.items()}
                    writer.writerow(csv_row)
        except Exception as e:
            raise StorageError(f"Ошибка при сохранении данных в CSV: {e}")

    @staticmethod
    def _is_duplicate(aeroplane: Dict[str, Any], existing_data: List[Dict[str, Any]]) -> bool:
        """Проверяет наличие дубликата."""
        for existing in existing_data:
            if existing.get("callsign") == aeroplane.get("callsign") and existing.get("icao24") == aeroplane.get(
                "icao24"
            ):
                return True
        return False

    def add_aeroplane(self, aeroplane: Dict[str, Any]) -> None:
        """Добавляет самолет в CSV-файл."""
        data = self._load_data()
        if not self._is_duplicate(aeroplane, data):
            data.append(aeroplane)
            self._save_data(data)

    def add_aeroplanes_list(self, aeroplanes_list: List[Dict[str, Any]]) -> None:
        """Добавляет список самолетов в CSV-файл."""
        data = self._load_data()
        added = False
        for aeroplane in aeroplanes_list:
            if not self._is_duplicate(aeroplane, data):
                data.append(aeroplane)
                added = True

        if added:
            self._save_data(data)

    def get_aeroplanes(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Получает самолеты по критериям из CSV-файла."""
        data = self._load_data()

        if criteria is None:
            return data

        result = []
        for aeroplane in data:
            match = True
            for key, value in criteria.items():
                if key not in aeroplane or aeroplane[key] != value:
                    match = False
                    break
            if match:
                result.append(aeroplane)

        return result

    def get_aeroplanes_by_origin_country(self, country: str) -> List[Dict[str, Any]]:
        """Получает самолеты по стране регистрации из CSV-файла."""
        data = self._load_data()
        return [a for a in data if a.get("origin_country", "").lower() == country.lower()]

    def delete_aeroplanes(self, criteria: Dict[str, Any]) -> int:
        """Удаляет самолеты по критериям из CSV-файла."""
        data = self._load_data()
        initial_count = len(data)

        data = [aeroplane for aeroplane in data if not all(aeroplane.get(k) == v for k, v in criteria.items())]

        deleted_count = initial_count - len(data)
        if deleted_count > 0:
            self._save_data(data)

        return deleted_count

    def clear(self) -> None:
        """Очищает CSV-файл."""
        self._save_data([])
