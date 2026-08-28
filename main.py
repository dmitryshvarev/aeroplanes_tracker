#!/usr/bin/env python3
"""
Главный модуль программы для отслеживания самолетов.

Точка входа в приложение. Содержит функцию взаимодействия с пользователем
и объединяет все компоненты системы.
"""

import logging
import os

from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.exceptions import AeroplanesTrackerError, APIError, CountryNotFoundError
from src.json_storage import JSONStorage
from src.utils import (
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude_range,
    format_aeroplanes_list,
    get_top_n_aeroplanes,
    sort_aeroplanes_by_altitude,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("aeroplanes_tracker.log", encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def print_header(text: str) -> None:
    """Выводит заголовок с оформлением."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_success(text: str) -> None:
    """Выводит сообщение об успехе."""
    print(f"✅ {text}")


def print_error(text: str) -> None:
    """Выводит сообщение об ошибке."""
    print(f"❌ {text}")


def print_info(text: str) -> None:
    """Выводит информационное сообщение."""
    print(f"ℹ️ {text}")


def get_user_input(prompt: str, required: bool = False, default: str = "") -> str:
    """
    Получает ввод от пользователя с возможностью пропуска.

    Args:
        prompt: Приглашение для ввода
        required: Обязателен ли ввод
        default: Значение по умолчанию

    Returns:
        Введенная строка или значение по умолчанию
    """
    while True:
        value = input(prompt).strip()

        if not value and not required:
            return default
        elif not value and required:
            print_error("Это поле обязательно для заполнения")
            continue

        return value


def get_int_input(prompt: str, min_val: int = 1, default: int = 10) -> int:
    """
    Получает целочисленный ввод от пользователя.

    Args:
        prompt: Приглашение для ввода
        min_val: Минимальное допустимое значение
        default: Значение по умолчанию

    Returns:
        Введенное число
    """
    while True:
        value = input(prompt).strip()

        if not value:
            return default

        try:
            num = int(value)
            if num < min_val:
                print_error(f"Число должно быть не меньше {min_val}")
                continue
            return num
        except ValueError:
            print_error("Пожалуйста, введите целое число")


def main() -> None:
    """
    Основная функция взаимодействия с пользователем.

    Запрашивает у пользователя параметры, получает данные о самолетах,
    фильтрует, сортирует и сохраняет их.
    """
    print_header("ПРОГРАММА ОТСЛЕЖИВАНИЯ САМОЛЕТОВ")
    print_info("Данная программа позволяет получить информацию о самолетах")
    print_info("в воздушном пространстве выбранной страны через OpenSky Network API")

    # Создаем экземпляры классов
    api = AeroplanesAPI()
    storage = JSONStorage("data/aeroplanes_data.json")

    # Создаем директорию для данных, если её нет
    os.makedirs("data", exist_ok=True)

    while True:
        try:
            print_header("ГЛАВНОЕ МЕНЮ")
            print("1. Получить информацию о самолетах по стране")
            print("2. Показать сохраненные самолеты")
            print("3. Очистить сохраненные данные")
            print("4. Выход")

            choice = get_user_input("Выберите действие (1-4): ", required=True)

            if choice == "1":
                # Получение данных о самолетах
                country = get_user_input(
                    "\nВведите название страны (например, Russia, Spain, France): ", required=True
                )

                print_info(f"Запрашиваю информацию о самолетах в {country}...")

                try:
                    # Получаем данные через API
                    aeroplanes_data = api.get_aeroplanes_by_country(country)

                    if not aeroplanes_data:
                        print_info(f"В воздушном пространстве {country} самолеты не обнаружены")
                        continue

                    print_success(f"Получено {len(aeroplanes_data)} самолетов")

                    # Преобразуем в объекты Aeroplanes
                    aeroplanes_objects = Aeroplane.cast_to_object_list(aeroplanes_data)

                    # Сохраняем в JSON
                    storage.add_aeroplanes_list(aeroplanes_data)
                    print_success(f"Данные сохранены в файл {str(storage)}")

                    # Запрашиваем параметры для фильтрации
                    print_header("ФИЛЬТРАЦИЯ И СОРТИРОВКА")

                    top_n = get_int_input(
                        "Введите количество самолетов для вывода в топ N (по высоте) [10]: ", default=10
                    )

                    filter_countries_input = get_user_input(
                        "Введите названия стран регистрации для фильтрации (через пробел, Enter чтобы пропустить): "
                    )

                    filter_countries = filter_countries_input.split() if filter_countries_input else []

                    altitude_range_str = get_user_input(
                        "Введите диапазон высот (например, 5000 - 10000, Enter чтобы пропустить): "
                    )

                    # Применяем фильтры
                    filtered = aeroplanes_objects

                    if filter_countries:
                        filtered = filter_aeroplanes_by_country(filtered, filter_countries)
                        print_info(f"После фильтрации по странам: {len(filtered)} самолетов")

                    if altitude_range_str:
                        filtered = filter_aeroplanes_by_altitude_range(filtered, altitude_range_str)
                        print_info(f"После фильтрации по высоте: {len(filtered)} самолетов")

                    # Сортируем и берем топ
                    sorted_aeroplanes = sort_aeroplanes_by_altitude(filtered, reverse=True)
                    top_aeroplanes = get_top_n_aeroplanes(sorted_aeroplanes, top_n)

                    # Выводим результат
                    print_header(f"ТОП-{top_n} САМОЛЕТОВ ПО ВЫСОТЕ")
                    print(format_aeroplanes_list(top_aeroplanes))

                except CountryNotFoundError as e:
                    print_error(f"Страна не найдена: {e}")
                except APIError as e:
                    print_error(f"Ошибка API: {e}")

            elif choice == "2":
                # Показать сохраненные самолеты
                all_aeroplanes = storage.get_all()

                if not all_aeroplanes:
                    print_info("В хранилище нет данных")
                    continue

                print_header(f"СОХРАНЕННЫЕ ДАННЫЕ ({len(all_aeroplanes)} самолетов)")

                # Преобразуем в объекты для удобного вывода
                aeroplanes_objects = Aeroplane.cast_to_object_list(all_aeroplanes)

                # Запрашиваем фильтр по стране
                country_filter = get_user_input("Введите страну для фильтрации (Enter чтобы показать все): ")

                if country_filter:
                    aeroplanes_objects = filter_aeroplanes_by_country(aeroplanes_objects, [country_filter])

                # Выводим
                for i, aeroplane in enumerate(aeroplanes_objects, 1):
                    print(f"\n{i}. {aeroplane}")

            elif choice == "3":
                # Очистить данные
                confirm = get_user_input(
                    "Вы уверены, что хотите очистить все сохраненные данные? (да/нет): ", required=True
                ).lower()

                if confirm in ["да", "yes", "y"]:
                    storage.clear()
                    print_success("Данные удалены")
                else:
                    print_info("Операция отменена")

            elif choice == "4":
                print_info("Программа завершена")
                break
            else:
                print_error("Неверный выбор. Пожалуйста, выберите 1-4")

        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print_info("Программа прервана пользователем")
            break
        except AeroplanesTrackerError as e:
            print_error(f"Ошибка программы: {e}")
            logger.error(f"Ошибка программы: {e}", exc_info=True)
        except Exception as e:
            print_error(f"Неожиданная ошибка: {e}")
            logger.error(f"Неожиданная ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    main()
