"""Реализация API для работы с Nominatim и OpenSky."""

import os
import time
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

from src.abstract_api_connector import AbstractAeroplanesAPI
from src.exceptions import APIError, CountryNotFoundError

load_dotenv()


class AeroplanesAPI(AbstractAeroplanesAPI):
    """
    Класс для работы с Nominatim и OpenSky API.

    Приватные атрибуты:
        _nominatim_url: Базовый URL Nominatim API
        _opensky_url: Базовый URL OpenSky API
        _session: Сессия requests для повторного использования
        _last_request_time: Время последнего запроса (для rate limiting)
        _email: Email для User-Agent
    """

    __slots__ = ("_nominatim_url", "_opensky_url", "_session", "_last_request_time", "_email")

    def __init__(self) -> None:
        """Инициализация API клиента."""
        self._nominatim_url: str = "https://nominatim.openstreetmap.org/search"
        self._opensky_url: str = "https://opensky-network.org/api/states/all"
        self._session: requests.Session = requests.Session()
        self._last_request_time: float = 0.0

        # Получаем email из .env или используем заглушку
        self._email = os.getenv("NOMINATIM_EMAIL", "student@example.com")

        self._session.headers.update({"User-Agent": f"AeroplanesTracker/1.0 ({self._email})"})

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
        try:
            # Добавляем задержку для Nominatim (требование API)
            if "nominatim" in url:
                current_time = time.time()
                time_since_last = current_time - self._last_request_time
                if time_since_last < 1.0:
                    time.sleep(1.0 - time_since_last)

                # Добавляем параметр для соблюдения политики использования
                if params is None:
                    params = {}
                params["email"] = self._email

                response = self._session.get(url, params=params, timeout=10)
                self._last_request_time = time.time()
            else:
                response = self._session.get(url, params=params, timeout=10)

            response.raise_for_status()

            # Проверяем, не вернулся ли HTML вместо JSON
            content_type = response.headers.get("Content-Type", "")
            if "application/json" not in content_type and "text/json" not in content_type:
                # Если это HTML, возможно, это страница с ошибкой
                if response.status_code == 200 and "<html" in response.text[:100].lower():
                    raise APIError("API вернул HTML страницу вместо JSON данных")

            return response.json()

        except requests.exceptions.Timeout:
            raise APIError("Превышен таймаут при подключении к API")
        except requests.exceptions.ConnectionError:
            raise APIError("Ошибка подключения к API")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise APIError(
                    f"Доступ запрещен (403). Убедитесь, что в .env файле указан корректный email. "
                    f"Текущий email: {self._email}"
                )
            elif e.response.status_code == 404:
                raise CountryNotFoundError("Страна не найдена")
            elif e.response.status_code == 429:
                raise APIError("Слишком много запросов. Попробуйте позже")
            else:
                raise APIError(f"HTTP ошибка {e.response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Ошибка при запросе: {e}")
        except ValueError as e:
            raise APIError(f"Ошибка при парсинге JSON: {e}")

    def get_country_coordinates(self, country: str) -> Dict[str, float]:
        """
        Получает координаты bounding box для страны через Nominatim API.

        Args:
            country: Название страны

        Returns:
            Словарь с координатами: south, north, west, east

        Raises:
            CountryNotFoundError: Если страна не найдена
            APIError: При ошибках API
        """
        params = {"q": country, "format": "json", "limit": 1, "addressdetails": 1, "featuretype": "country"}

        result = self._connect(self._nominatim_url, params)

        if not result or len(result) == 0:
            raise CountryNotFoundError(f"Страна '{country}' не найдена")

        country_data = result[0]

        if "boundingbox" not in country_data:
            raise CountryNotFoundError(f"Для страны '{country}' не найден bounding box")

        bbox = country_data["boundingbox"]
        return {"south": float(bbox[0]), "north": float(bbox[1]), "west": float(bbox[2]), "east": float(bbox[3])}

    def get_aeroplanes_in_area(self, bbox: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Получает информацию о самолетах в заданной области через OpenSky API.

        Args:
            bbox: Словарь с координатами области (south, north, west, east)

        Returns:
            Список словарей с данными о самолетах

        Raises:
            APIError: При ошибках API
        """
        params = {"lamin": bbox["south"], "lamax": bbox["north"], "lomin": bbox["west"], "lomax": bbox["east"]}

        try:
            result = self._connect(self._opensky_url, params)

            if "states" not in result or not result["states"]:
                return []

            aeroplanes_list = []
            for state in result["states"]:
                # Проверяем, что данные не None и корректны
                if state[5] is None or state[6] is None:  # долгота или широта отсутствуют
                    continue

                aircraft_dict = {
                    "icao24": state[0],
                    "callsign": state[1].strip() if state[1] else None,
                    "origin_country": state[2],
                    "longitude": float(state[5]) if state[5] is not None else None,
                    "latitude": float(state[6]) if state[6] is not None else None,
                    "baro_altitude": float(state[7]) if state[7] is not None else None,
                    "on_ground": state[8],
                    "velocity": float(state[9]) if state[9] is not None else None,
                    "true_track": float(state[10]) if state[10] is not None else None,
                    "vertical_rate": float(state[11]) if state[11] is not None else None,
                    "geo_altitude": float(state[13]) if state[13] is not None else None,
                }

                # Фильтруем только самолеты с минимальными данными
                if aircraft_dict["callsign"]:
                    aeroplanes_list.append(aircraft_dict)

            return aeroplanes_list

        except Exception as e:
            raise APIError(f"Ошибка при получении данных о самолетах: {e}")

    def get_aeroplanes_by_country(self, country: str) -> List[Dict[str, Any]]:
        """
        Получает информацию о самолетах в воздушном пространстве страны.

        Args:
            country: Название страны

        Returns:
            Список словарей с данными о самолетах
        """
        bbox = self.get_country_coordinates(country)
        return self.get_aeroplanes_in_area(bbox)
