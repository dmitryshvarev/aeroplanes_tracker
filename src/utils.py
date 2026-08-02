"""Вспомогательные функции для проекта."""

from typing import List, Optional, Tuple

from src.aeroplane import Aeroplane


def filter_aeroplanes_by_country(aeroplanes_list: List[Aeroplane], countries: List[str]) -> List[Aeroplane]:
    """
    Фильтрует самолеты по стране регистрации.

    Args:
        aeroplanes_list: Список объектов Aeroplane
        countries: Список стран для фильтрации

    Returns:
        Отфильтрованный список самолетов
    """
    if not countries:
        return aeroplanes_list

    countries_lower = [c.lower() for c in countries]
    return [a for a in aeroplanes_list if a.origin_country.lower() in countries_lower]


def filter_aeroplanes_by_altitude_range(
    aeroplanes_list: List[Aeroplane], altitude_range: Optional[str]
) -> List[Aeroplane]:
    """
    Фильтрует самолеты по диапазону высот.

    Args:
        aeroplanes_list: Список объектов Aeroplane
        altitude_range: Строка вида "min - max"

    Returns:
        Отфильтрованный список самолетов
    """
    if not altitude_range:
        return aeroplanes_list

    try:
        parts = altitude_range.replace(",", ".").split("-")
        if len(parts) != 2:
            return aeroplanes_list

        min_alt = float(parts[0].strip())
        max_alt = float(parts[1].strip())

        return [a for a in aeroplanes_list if a.altitude is not None and min_alt <= a.altitude <= max_alt]
    except (ValueError, TypeError):
        # Если не удалось распарсить, возвращаем исходный список
        return aeroplanes_list


def sort_aeroplanes_by_altitude(aeroplanes_list: List[Aeroplane], reverse: bool = True) -> List[Aeroplane]:
    """
    Сортирует самолеты по высоте.

    Args:
        aeroplanes_list: Список объектов Aeroplane
        reverse: По убыванию (True) или возрастанию (False)

    Returns:
        Отсортированный список
    """
    # Отделяем самолеты с известной высотой
    with_altitude = [a for a in aeroplanes_list if a.altitude is not None]
    without_altitude = [a for a in aeroplanes_list if a.altitude is None]

    # Сортируем с известной высотой
    sorted_with = sorted(with_altitude, reverse=reverse)

    # Добавляем самолеты без высоты в конец
    return sorted_with + without_altitude


def get_top_n_aeroplanes(aeroplanes_list: List[Aeroplane], n: int) -> List[Aeroplane]:
    """
    Возвращает топ N самолетов (по высоте).

    Args:
        aeroplanes_list: Список объектов Aeroplane
        n: Количество самолетов

    Returns:
        Первые N самолетов из списка
    """
    return aeroplanes_list[:n] if n < len(aeroplanes_list) else aeroplanes_list


def format_aeroplanes_list(aeroplanes_list: List[Aeroplane]) -> str:
    """
    Форматирует список самолетов для вывода пользователю.

    Args:
        aeroplanes_list: Список объектов Aeroplane

    Returns:
        Отформатированная строка
    """
    if not aeroplanes_list:
        return "Самолеты не найдены."

    lines = [f"Найдено самолетов: {len(aeroplanes_list)}"]
    for i, aeroplane in enumerate(aeroplanes_list, 1):
        lines.append(f"\n{i}. {aeroplane}")

    return "\n".join(lines)


def parse_altitude_range(altitude_str: str) -> Optional[Tuple[float, float]]:
    """
    Парсит строку с диапазоном высот.

    Args:
        altitude_str: Строка вида "min - max"

    Returns:
        Кортеж (min, max) или None если формат неверный
    """
    try:
        parts = altitude_str.replace(",", ".").split("-")
        if len(parts) != 2:
            return None

        min_alt = float(parts[0].strip())
        max_alt = float(parts[1].strip())

        return min_alt, max_alt
    except (ValueError, TypeError):
        return None
