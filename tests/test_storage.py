"""Тесты для классов хранилищ."""

import json

from src.csv_storage import CSVStorage
from src.json_storage import JSONStorage


class TestJSONStorage:
    """Тесты для класса JSONStorage."""

    def test_init_default_filename(self):
        """Тест инициализации с именем по умолчанию."""
        storage = JSONStorage()
        assert storage._filename == "data/aeroplanes_data.json"

    def test_init_custom_filename(self, temp_json_file):
        """Тест инициализации с пользовательским именем."""
        storage = JSONStorage(temp_json_file)
        assert storage._filename == temp_json_file

    def test_add_aeroplane(self, temp_json_file, sample_aeroplanes_data):
        """Тест добавления самолета."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplane(sample_aeroplanes_data[0])

        # Проверяем, что данные сохранились
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["callsign"] == "AFL101"

    def test_add_duplicate_aeroplane(self, temp_json_file, sample_aeroplanes_data):
        """Тест добавления дубликата."""
        storage = JSONStorage(temp_json_file)

        # Добавляем дважды
        storage.add_aeroplane(sample_aeroplanes_data[0])
        storage.add_aeroplane(sample_aeroplanes_data[0])

        # Проверяем, что дубликат не добавился
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1

    def test_add_aeroplanes_list(self, temp_json_file, sample_aeroplanes_data):
        """Тест добавления списка самолетов."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplanes_list(sample_aeroplanes_data)

        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 4

    def test_get_aeroplanes_all(self, temp_json_file, sample_aeroplanes_data):
        """Тест получения всех самолетов."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplanes_list(sample_aeroplanes_data)

        all_aeroplanes = storage.get_aeroplanes()
        assert len(all_aeroplanes) == 4

    def test_get_aeroplanes_with_criteria(self, temp_json_file, sample_aeroplanes_data):
        """Тест получения самолетов по критериям."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplanes_list(sample_aeroplanes_data)

        russian = storage.get_aeroplanes({"origin_country": "Russia"})
        assert len(russian) == 1
        assert russian[0]["callsign"] == "AFL101"

    def test_get_aeroplanes_by_origin_country(self, temp_json_file, sample_aeroplanes_data):
        """Тест получения самолетов по стране регистрации."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplanes_list(sample_aeroplanes_data)

        uk_aeroplanes = storage.get_aeroplanes_by_origin_country("United Kingdom")
        assert len(uk_aeroplanes) == 1
        assert uk_aeroplanes[0]["callsign"] == "BAW202"

    def test_delete_aeroplanes(self, temp_json_file, sample_aeroplanes_data):
        """Тест удаления самолетов."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplanes_list(sample_aeroplanes_data)

        deleted = storage.delete_aeroplanes({"origin_country": "Russia"})
        assert deleted == 1

        remaining = storage.get_aeroplanes()
        assert len(remaining) == 3

    def test_clear(self, temp_json_file, sample_aeroplanes_data):
        """Тест очистки хранилища."""
        storage = JSONStorage(temp_json_file)
        storage.add_aeroplanes_list(sample_aeroplanes_data)

        storage.clear()

        assert storage.get_all() == []
        assert storage.count() == 0


class TestCSVStorage:
    """Тесты для класса CSVStorage."""

    def test_init_default_filename(self):
        """Тест инициализации с именем по умолчанию."""
        storage = CSVStorage()
        assert storage._filename == "data/aeroplanes_data.csv"
