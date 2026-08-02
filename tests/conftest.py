"""Фикстуры для тестирования."""

import json
import tempfile
from typing import Any, Dict, List

import pytest

from src.aeroplane import Aeroplane


@pytest.fixture
def sample_aeroplanes_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными самолетов."""
    return [
        {
            "callsign": "AFL101",
            "origin_country": "Russia",
            "velocity": 250.5,
            "altitude": 10500.0,
            "latitude": 55.5,
            "longitude": 37.5,
            "icao24": "abc123",
        },
        {
            "callsign": "BAW202",
            "origin_country": "United Kingdom",
            "velocity": 240.0,
            "altitude": 9500.0,
            "latitude": 51.5,
            "longitude": -0.1,
            "icao24": "def456",
        },
        {
            "callsign": "UAL303",
            "origin_country": "United States",
            "velocity": 260.0,
            "altitude": 11000.0,
            "latitude": 40.7,
            "longitude": -74.0,
            "icao24": "ghi789",
        },
        {
            "callsign": None,
            "origin_country": "Germany",
            "velocity": None,
            "altitude": None,
            "latitude": 52.5,
            "longitude": 13.4,
            "icao24": "jkl012",
        },
    ]


@pytest.fixture
def sample_aeroplanes_objects(sample_aeroplanes_data) -> List[Aeroplane]:
    """Фикстура с тестовыми объектами Aeroplane."""
    return [Aeroplane.from_dict(data) for data in sample_aeroplanes_data]


@pytest.fixture
def temp_json_file():
    """Фикстура для временного JSON файла."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([], f)
        temp_file = f.name

    yield temp_file

    import os

    os.unlink(temp_file)


@pytest.fixture
def mock_nominatim_response():
    """Фикстура с мок-ответом от Nominatim API."""
    return [{"place_id": 123, "boundingbox": ["35.0", "70.0", "-10.0", "40.0"], "display_name": "Russia"}]


@pytest.fixture
def mock_opensky_response():
    """Фикстура с мок-ответом от OpenSky API."""
    return {
        "time": 1234567890,
        "states": [
            [
                "abc123",
                "AFL101  ",
                "Russia",
                1234567890,
                1234567890,
                37.5,
                55.5,
                10500.0,
                False,
                250.5,
                120.0,
                0.0,
                None,
                11000.0,
                None,
                False,
                0,
            ],
            [
                "def456",
                "BAW202",
                "United Kingdom",
                1234567890,
                1234567890,
                -0.1,
                51.5,
                9500.0,
                False,
                240.0,
                110.0,
                0.0,
                None,
                10000.0,
                None,
                False,
                0,
            ],
        ],
    }
