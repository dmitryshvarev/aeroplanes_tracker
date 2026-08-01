class AeroplanesTrackerError(Exception):
    """Базовое исключение для проекта."""

    pass


class APIError(AeroplanesTrackerError):
    """Исключение при ошибках API."""

    pass


class CountryNotFoundError(APIError):
    """Исключение при ненахождении страны."""

    pass


class InvalidAeroplaneDataError(AeroplanesTrackerError):
    """Исключение при невалидных данных самолета."""

    pass


class StorageError(AeroplanesTrackerError):
    """Исключение при работе с хранилищем."""

    pass
