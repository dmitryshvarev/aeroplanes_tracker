"""Тесты для класса AeroplanesAPI."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.aeroplanes_api import AeroplanesAPI
from src.exceptions import APIError, CountryNotFoundError


class TestAeroplanesAPI:
    """Тесты для класса AeroplanesAPI."""

    def test_init(self):
        """Тест инициализации API клиента."""
        api = AeroplanesAPI()
        assert api._nominatim_url == "https://nominatim.openstreetmap.org/search"
        assert api._opensky_url == "https://opensky-network.org/api/states/all"
        assert api._session is not None

    @patch("src.aeroplanes_api.requests.Session.get")
    def test_connect_success(self, mock_get, mock_nominatim_response):
        """Тест успешного подключения к API."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_nominatim_response
        mock_response.status_code = 200
        mock_response.headers.get.return_value = "application/json"
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        result = api._connect("https://test.com", params={"q": "test"})

        assert result == mock_nominatim_response

    @patch("src.aeroplanes_api.requests.Session.get")
    def test_connect_timeout(self, mock_get):
        """Тест таймаута при подключении."""
        mock_get.side_effect = requests.exceptions.Timeout()

        api = AeroplanesAPI()
        with pytest.raises(APIError) as exc_info:
            api._connect("https://test.com")

        assert "Превышен таймаут" in str(exc_info.value)

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_country_bounding_box_success(self, mock_connect, mock_nominatim_response):
        """Тест успешного получения bounding box страны."""
        mock_connect.return_value = mock_nominatim_response

        api = AeroplanesAPI()
        bbox = api.get_country_coordinates("Russia")

        assert bbox["south"] == 35.0
        assert bbox["north"] == 70.0
        assert bbox["west"] == -10.0
        assert bbox["east"] == 40.0

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_country_bounding_box_not_found(self, mock_connect):
        """Тест ненахождения страны."""
        mock_connect.return_value = []

        api = AeroplanesAPI()
        with pytest.raises(CountryNotFoundError):
            api.get_country_coordinates("Atlantis")

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_country_bounding_box_no_bbox(self, mock_connect):
        """Тест отсутствия bounding box в ответе."""
        mock_connect.return_value = [{"display_name": "Test"}]

        api = AeroplanesAPI()
        with pytest.raises(CountryNotFoundError):
            api.get_country_coordinates("Test")

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_aeroplanes_in_area_success(self, mock_connect, mock_opensky_response):
        """Тест успешного получения самолетов в области."""
        mock_connect.return_value = mock_opensky_response

        api = AeroplanesAPI()
        bbox = {"south": 35.0, "north": 70.0, "west": -10.0, "east": 40.0}
        aeroplanes_list = api.get_aeroplanes_in_area(bbox)

        assert len(aeroplanes_list) == 2
        assert aeroplanes_list[0]["callsign"] == "AFL101"
        assert aeroplanes_list[1]["callsign"] == "BAW202"

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_aeroplanes_in_area_empty(self, mock_connect):
        """Тест получения пустого списка самолетов."""
        mock_connect.return_value = {"states": None}

        api = AeroplanesAPI()
        bbox = {"south": 35.0, "north": 70.0, "west": -10.0, "east": 40.0}
        aeroplanes_list = api.get_aeroplanes_in_area(bbox)

        assert aeroplanes_list == []

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_aeroplanes_in_area_no_states(self, mock_connect):
        """Тест отсутствия states в ответе."""
        mock_connect.return_value = {}

        api = AeroplanesAPI()
        bbox = {"south": 35.0, "north": 70.0, "west": -10.0, "east": 40.0}
        aeroplanes_list = api.get_aeroplanes_in_area(bbox)

        assert aeroplanes_list == []

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_aeroplanes_in_area_with_null_coordinates(self, mock_connect):
        """Тест обработки null координат."""
        mock_response = {
            "states": [
                [
                    "abc123",
                    "TEST",
                    "Russia",
                    123,
                    123,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ]
            ]
        }
        mock_connect.return_value = mock_response

        api = AeroplanesAPI()
        bbox = {"south": 35.0, "north": 70.0, "west": -10.0, "east": 40.0}
        aeroplanes_list = api.get_aeroplanes_in_area(bbox)

        assert aeroplanes_list == []  # Самолет с null координатами должен быть пропущен

    @patch("src.aeroplanes_api.AeroplanesAPI._connect")
    def test_get_aeroplanes_in_area_error(self, mock_connect):
        """Тест ошибки при получении данных."""
        mock_connect.side_effect = APIError("API Error")

        api = AeroplanesAPI()
        bbox = {"south": 35.0, "north": 70.0, "west": -10.0, "east": 40.0}

        with pytest.raises(APIError):
            api.get_aeroplanes_in_area(bbox)

    @patch("src.aeroplanes_api.AeroplanesAPI.get_country_coordinates")
    @patch("src.aeroplanes_api.AeroplanesAPI.get_aeroplanes_in_area")
    def test_get_aeroplanes_by_country(self, mock_get_aeroplanes, mock_get_bbox):
        """Тест получения самолетов по стране."""
        mock_get_bbox.return_value = {"south": 35.0, "north": 70.0, "west": -10.0, "east": 40.0}
        mock_get_aeroplanes.return_value = [{"callsign": "TEST"}]

        api = AeroplanesAPI()
        result = api.get_aeroplanes_by_country("Russia")

        mock_get_bbox.assert_called_once_with("Russia")
        mock_get_aeroplanes.assert_called_once()
        assert result == [{"callsign": "TEST"}]

    @patch("src.aeroplanes_api.AeroplanesAPI.get_country_coordinates")
    def test_get_aeroplanes_by_country_not_found(self, mock_get_bbox):
        """Тест получения самолетов для несуществующей страны."""
        mock_get_bbox.side_effect = CountryNotFoundError("Страна не найдена")

        api = AeroplanesAPI()

        with pytest.raises(CountryNotFoundError):
            api.get_aeroplanes_by_country("Atlantis")
