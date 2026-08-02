# Проект "aeroplanes_tracker"

## Описание:

Проект "aeroplanes_tracker" собирает данные о самолетах в воздушных пространствах тех стран, которые выберет пользователь.
Чтобы получить географические координаты стран, в проекте использовалось API [nominatim.openstreetmap.org](https://nominatim.openstreetmap.org/ui/search.html),
а чтобы получить информацию о самолетах — API [opensky-network.org](https://opensky-network.org/).

## Установка:

1. Клонируйте репозиторий:
```
https://github.com/dmitryshvarev/aeroplanes_tracker.git
```

2. Установите зависимости:
```
pip install poetry
```
## Тестирование:

- с помощью библиотеки pytest в проекте протестированы все классы,
  тесты выполнены успешно
- сгенерирован отчет index.html о покрытии кода тестированием
