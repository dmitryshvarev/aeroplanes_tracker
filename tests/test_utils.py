"""Тесты для вспомогательных функций."""

import pytest

from src.utils import (
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude_range,
    sort_aeroplanes_by_altitude,
    get_top_n_aeroplanes,
    format_aeroplanes_list,
    parse_altitude_range
)


class TestUtils:
    """Тесты для вспомогательных функций."""

    def test_filter_aeroplanes_by_country(self, sample_aeroplanes_objects):
        """Тест фильтрации по стране."""
        filtered = filter_aeroplanes_by_country(sample_aeroplanes_objects, ['Russia'])
        assert len(filtered) == 1
        assert filtered[0].origin_country == 'Russia'

        # Пустой список стран
        filtered = filter_aeroplanes_by_country(sample_aeroplanes_objects, [])
        assert len(filtered) == 4

    def test_filter_aeroplanes_by_country_multiple(self, sample_aeroplanes_objects):
        """Тест фильтрации по нескольким странам."""
        filtered = filter_aeroplanes_by_country(
            sample_aeroplanes_objects,
            ['Russia', 'Germany']
        )
        assert len(filtered) == 2

    def test_filter_aeroplanes_by_altitude_range(self, sample_aeroplanes_objects):
        """Тест фильтрации по диапазону высот."""
        filtered = filter_aeroplanes_by_altitude_range(
            sample_aeroplanes_objects,
            "9000 - 11000"
        )
        assert len(filtered) == 3  # Самолеты с высотой в диапазоне

        # Неверный формат
        filtered = filter_aeroplanes_by_altitude_range(
            sample_aeroplanes_objects,
            "invalid"
        )
        assert len(filtered) == 4

    def test_filter_aeroplanes_by_altitude_range_none(self, sample_aeroplanes_objects):
        """Тест фильтрации с None."""
        filtered = filter_aeroplanes_by_altitude_range(sample_aeroplanes_objects, None)
        assert len(filtered) == 4

    def test_sort_aeroplanes_by_altitude(self, sample_aeroplanes_objects):
        """Тест сортировки по высоте."""
        sorted_desc = sort_aeroplanes_by_altitude(sample_aeroplanes_objects, reverse=True)

        # Самый высокий должен быть первым
        assert sorted_desc[0].altitude == 11000.0
        assert sorted_desc[1].altitude == 10500.0
        assert sorted_desc[2].altitude == 9500.0

        # Самолеты без высоты в конце
        assert sorted_desc[3].altitude is None

    def test_get_top_n_aeroplanes(self, sample_aeroplanes_objects):
        """Тест получения топ N самолетов."""
        top_2 = get_top_n_aeroplanes(sample_aeroplanes_objects, 2)
        assert len(top_2) == 2

        top_10 = get_top_n_aeroplanes(sample_aeroplanes_objects, 10)
        assert len(top_10) == 4

    def test_format_aeroplanes_list_empty(self):
        """Тест форматирования пустого списка."""
        formatted = format_aeroplanes_list([])
        assert formatted == "Самолеты не найдены."

    def test_format_aeroplanes_list_non_empty(self, sample_aeroplanes_objects):
        """Тест форматирования непустого списка."""
        formatted = format_aeroplanes_list(sample_aeroplanes_objects[:2])
        assert "Найдено самолетов: 2" in formatted
        assert "AFL101" in formatted
        assert "BAW202" in formatted

    @pytest.mark.parametrize("input_str,expected", [
        ("5000 - 10000", (5000.0, 10000.0)),
        ("5000-10000", (5000.0, 10000.0)),
        ("5000,5 - 10000,5", (5000.5, 10000.5)),
        ("invalid", None),
        ("", None),
    ])
    def test_parse_altitude_range(self, input_str, expected):
        """Тест парсинга диапазона высот."""
        result = parse_altitude_range(input_str)
        assert result == expected
