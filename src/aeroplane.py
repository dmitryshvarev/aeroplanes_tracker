"""Класс для работы с информацией о самолетах."""

from typing import Any, Dict, Optional

from src.exceptions import InvalidAeroplaneDataError


class Aeroplane:
    """
    Класс, представляющий самолет.

    Атрибуты:
        callsign: Позывной самолета
        origin_country: Страна регистрации
        velocity: Скорость в м/с
        altitude: Высота в метрах (барометрическая)
        latitude: Широта
        longitude: Долгота
        icao24: ICAO24 код

    Поддерживает сравнение по скорости и высоте через магические методы.
    """

    __slots__ = ("_callsign", "_origin_country", "_velocity", "_altitude", "_latitude", "_longitude", "_icao24")

    def __init__(
        self,
        callsign: Optional[str],
        origin_country: str,
        velocity: Optional[float],
        altitude: Optional[float],
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        icao24: Optional[str] = None,
    ) -> None:
        """
        Инициализация самолета с валидацией данных.

        Args:
            callsign: Позывной самолета
            origin_country: Страна регистрации
            velocity: Скорость в м/с
            altitude: Высота в метрах
            latitude: Широта
            longitude: Долгота
            icao24: ICAO24 код

        Raises:
            InvalidAeroplaneDataError: При невалидных данных
        """
        self._callsign = self._validate_callsign(callsign)
        self._origin_country = self._validate_origin_country(origin_country)
        self._velocity = self._validate_velocity(velocity)
        self._altitude = self._validate_altitude(altitude)
        self._latitude = self._validate_latitude(latitude)
        self._longitude = self._validate_longitude(longitude)
        self._icao24 = self._validate_icao24(icao24)

    @staticmethod
    def _validate_callsign(callsign: Optional[str]) -> Optional[str]:
        """Валидация позывного."""
        if callsign is None:
            return None
        if not isinstance(callsign, str):
            raise InvalidAeroplaneDataError(f"Позывной должен быть строкой, получен {type(callsign)}")
        if len(callsign.strip()) == 0:
            return None
        return callsign.strip()

    @staticmethod
    def _validate_origin_country(origin_country: str) -> str:
        """Валидация страны регистрации."""
        if not isinstance(origin_country, str):
            raise InvalidAeroplaneDataError(f"Страна регистрации должна быть строкой, получен {type(origin_country)}")
        if len(origin_country.strip()) == 0:
            raise InvalidAeroplaneDataError("Страна регистрации не может быть пустой")
        return origin_country.strip()

    @staticmethod
    def _validate_velocity(velocity: Optional[float]) -> Optional[float]:
        """Валидация скорости."""
        if velocity is None:
            return None
        try:
            vel = float(velocity)
            if vel < 0:
                raise InvalidAeroplaneDataError(f"Скорость не может быть отрицательной: {vel}")
            return vel
        except (TypeError, ValueError):
            raise InvalidAeroplaneDataError(f"Некорректное значение скорости: {velocity}")

    @staticmethod
    def _validate_altitude(altitude: Optional[float]) -> Optional[float]:
        """Валидация высоты."""
        if altitude is None:
            return None
        try:
            alt = float(altitude)
            # Высота может быть отрицательной (ниже уровня моря)
            return alt
        except (TypeError, ValueError):
            raise InvalidAeroplaneDataError(f"Некорректное значение высоты: {altitude}")

    @staticmethod
    def _validate_latitude(latitude: Optional[float]) -> Optional[float]:
        """Валидация широты."""
        if latitude is None:
            return None
        try:
            lat = float(latitude)
            if lat < -90 or lat > 90:
                raise InvalidAeroplaneDataError(f"Широта должна быть в диапазоне [-90, 90], получена {lat}")
            return lat
        except (TypeError, ValueError):
            raise InvalidAeroplaneDataError(f"Некорректное значение широты: {latitude}")

    @staticmethod
    def _validate_longitude(longitude: Optional[float]) -> Optional[float]:
        """Валидация долготы."""
        if longitude is None:
            return None
        try:
            lon = float(longitude)
            if lon < -180 or lon > 180:
                raise InvalidAeroplaneDataError(f"Долгота должна быть в диапазоне [-180, 180], получена {lon}")
            return lon
        except (TypeError, ValueError):
            raise InvalidAeroplaneDataError(f"Некорректное значение долготы: {longitude}")

    @staticmethod
    def _validate_icao24(icao24: Optional[str]) -> Optional[str]:
        """Валидация ICAO24 кода."""
        if icao24 is None:
            return None
        if not isinstance(icao24, str):
            raise InvalidAeroplaneDataError(f"ICAO24 должен быть строкой, получен {type(icao24)}")
        if len(icao24.strip()) == 0:
            return None
        return icao24.strip().lower()

    # Свойства для доступа к приватным атрибутам
    @property
    def callsign(self) -> Optional[str]:
        """Позывной самолета."""
        return self._callsign

    @property
    def origin_country(self) -> str:
        """Страна регистрации."""
        return self._origin_country

    @property
    def velocity(self) -> Optional[float]:
        """Скорость в м/с."""
        return self._velocity

    @property
    def altitude(self) -> Optional[float]:
        """Высота в метрах."""
        return self._altitude

    @property
    def latitude(self) -> Optional[float]:
        """Широта."""
        return self._latitude

    @property
    def longitude(self) -> Optional[float]:
        """Долгота."""
        return self._longitude

    @property
    def icao24(self) -> Optional[str]:
        """ICAO24 код."""
        return self._icao24

    # Магические методы для сравнения по высоте
    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение 'меньше' по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.altitude is None or other.altitude is None:
            return False
        return self.altitude < other.altitude

    def __le__(self, other: "Aeroplane") -> bool:
        """Сравнение 'меньше или равно' по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.altitude is None or other.altitude is None:
            return self.altitude == other.altitude
        return self.altitude <= other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение 'больше' по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.altitude is None or other.altitude is None:
            return False
        return self.altitude > other.altitude

    def __ge__(self, other: "Aeroplane") -> bool:
        """Сравнение 'больше или равно' по высоте."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.altitude is None or other.altitude is None:
            return self.altitude == other.altitude
        return self.altitude >= other.altitude

    def __eq__(self, other: object) -> bool:
        """Сравнение на равенство."""
        if not isinstance(other, Aeroplane):
            return False
        return (
            self.callsign == other.callsign
            and self.origin_country == other.origin_country
            and self.velocity == other.velocity
            and self.altitude == other.altitude
        )

    def __repr__(self) -> str:
        """Строковое представление для отладки."""
        return (
            f"Aircraft(callsign={self.callsign}, "
            f"origin={self.origin_country}, "
            f"altitude={self.altitude}, "
            f"velocity={self.velocity})"
        )

    def __str__(self) -> str:
        """Пользовательское строковое представление."""

        parts = [f"Самолет {self.callsign}", f"Страна регистрации: {self.origin_country}"]
        if self.altitude is not None:
            parts.append(f"Высота: {self.altitude:.1f} м")
        if self.velocity is not None:
            # Переводим м/с в км/ч для лучшего восприятия
            kmh = self.velocity * 3.6
            parts.append(f"Скорость: {kmh:.1f} км/ч")
        if self.latitude is not None and self.longitude is not None:
            parts.append(f"Координаты: {self.latitude:.4f}, {self.longitude:.4f}")

        return " | ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект в словарь для сохранения в JSON.

        Returns:
            Словарь с данными самолета
        """
        return {
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "icao24": self.icao24,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Aeroplane":
        """
        Создает объект Aeroplane из словаря.

        Args:
            data: Словарь с данными самолета

        Returns:
            Объект Aeroplane
        """
        return cls(
            callsign=data.get("callsign"),
            origin_country=data.get("origin_country", "Unknown"),
            velocity=data.get("velocity"),
            altitude=data.get("altitude"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            icao24=data.get("icao24"),
        )

    @classmethod
    def cast_to_object_list(cls, aeroplane_list: list[Dict[str, Any]]) -> list["Aeroplane"]:
        """
        Преобразует список словарей в список объектов Aeroplane.

        Args:
            aeroplane_list: Список словарей с данными самолетов

        Returns:
            Список объектов Aeroplane
        """
        result = []
        for item in aeroplane_list:
            try:
                aeroplane = cls.from_dict(item)
                result.append(aeroplane)
            except InvalidAeroplaneDataError:
                # Пропускаем некорректные записи
                continue
        return result
