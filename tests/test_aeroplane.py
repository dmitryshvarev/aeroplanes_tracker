"""Тесты для класса Aeroplane."""

import pytest

from src.aeroplane import Aeroplane
from src.exceptions import InvalidAeroplaneDataError


class TestAeroplane:
    """Тесты для класса Aeroplane."""

    def test_aeroplane_creation_valid(self, sample_aeroplanes_data):
        """Тест создания самолета с валидными данными."""
        data = sample_aeroplanes_data[0]
        aeroplane = Aeroplane(
            callsign=data["callsign"],
            origin_country=data["origin_country"],
            velocity=data["velocity"],
            altitude=data["altitude"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            icao24=data["icao24"],
        )

        assert aeroplane.callsign == "AFL101"
        assert aeroplane.origin_country == "Russia"
        assert aeroplane.velocity == 250.5
        assert aeroplane.altitude == 10500.0
        assert aeroplane.latitude == 55.5
        assert aeroplane.longitude == 37.5
        assert aeroplane.icao24 == "abc123"

    def test_aeroplane_creation_with_none_values(self):
        """Тест создания самолета с None значениями."""
        aeroplane = Aeroplane(callsign=None, origin_country="Russia", velocity=None, altitude=None)

        assert aeroplane.callsign is None
        assert aeroplane.origin_country == "Russia"
        assert aeroplane.velocity is None
        assert aeroplane.altitude is None

    def test_aeroplane_creation_invalid_callsign(self):
        """Тест создания с невалидным позывным."""
        with pytest.raises(InvalidAeroplaneDataError):
            Aeroplane(callsign=123, origin_country="Russia", velocity=100.0, altitude=10000.0)  # Должна быть строка

    def test_aeroplane_creation_invalid_country(self):
        """Тест создания с невалидной страной."""
        with pytest.raises(InvalidAeroplaneDataError):
            Aeroplane(callsign="TEST", origin_country="", velocity=100.0, altitude=10000.0)  # Пустая строка

    def test_aeroplane_creation_invalid_velocity(self):
        """Тест создания с невалидной скоростью."""
        with pytest.raises(InvalidAeroplaneDataError):
            Aeroplane(callsign="TEST", origin_country="Russia", velocity="not a number", altitude=10000.0)

    def test_aeroplane_creation_negative_velocity(self):
        """Тест создания с отрицательной скоростью."""
        with pytest.raises(InvalidAeroplaneDataError):
            Aeroplane(callsign="TEST", origin_country="Russia", velocity=-100.0, altitude=10000.0)

    def test_aeroplanes_comparison_lt(self, sample_aeroplanes_objects):
        """Тест сравнения 'меньше' по высоте."""
        a1, a2, a3 = sample_aeroplanes_objects[:3]

        # a2 (9500) < a1 (10500)
        assert a2 < a1
        assert not (a1 < a2)

        # Сравнение с самолетом без высоты
        a4 = sample_aeroplanes_objects[3]  # altitude = None
        assert not (a1 < a4)
        assert not (a4 < a1)

    def test_aeroplanes_comparison_gt(self, sample_aeroplanes_objects):
        """Тест сравнения 'больше' по высоте."""
        a1, a2, a3 = sample_aeroplanes_objects[:3]

        # a1 (10500) > a2 (9500)
        assert a1 > a2
        assert not (a2 > a1)

    def test_aeroplanes_comparison_eq(self, sample_aeroplanes_objects):
        """Тест сравнения на равенство."""
        a1, a2 = sample_aeroplanes_objects[:2]
        a1_copy = Aeroplane.from_dict(
            {
                "callsign": "AFL101",
                "origin_country": "Russia",
                "velocity": 250.5,
                "altitude": 10500.0,
                "latitude": 55.5,
                "longitude": 37.5,
                "icao24": "abc123",
            }
        )

        assert a1 == a1_copy
        assert a1 != a2
        assert a1 != "not an aeroplane"

    def test_to_dict(self, sample_aeroplanes_objects):
        """Тест преобразования в словарь."""
        aeroplane = sample_aeroplanes_objects[0]
        data = aeroplane.to_dict()

        assert data["callsign"] == "AFL101"
        assert data["origin_country"] == "Russia"
        assert data["velocity"] == 250.5
        assert data["altitude"] == 10500.0
        assert data["latitude"] == 55.5
        assert data["longitude"] == 37.5
        assert data["icao24"] == "abc123"

    def test_from_dict(self, sample_aeroplanes_data):
        """Тест создания из словаря."""
        data = sample_aeroplanes_data[0]
        aeroplane = Aeroplane.from_dict(data)

        assert aeroplane.callsign == "AFL101"
        assert aeroplane.origin_country == "Russia"

    def test_cast_to_object_list(self, sample_aeroplanes_data):
        """Тест преобразования списка словарей в список объектов."""
        aeroplanes_list = Aeroplane.cast_to_object_list(sample_aeroplanes_data)

        assert len(aeroplanes_list) == 4
        assert all(isinstance(a, Aeroplane) for a in aeroplanes_list)

    def test_str_representation(self, sample_aeroplanes_objects):
        """Тест строкового представления."""
        aeroplane = sample_aeroplanes_objects[0]
        str_repr = str(aeroplane)

        assert "AFL101" in str_repr
        assert "Russia" in str_repr
        assert "10500.0" in str_repr
