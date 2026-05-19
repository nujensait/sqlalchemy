## Оглавление

- [О проекте](#о-проекте)
- [Содержание (список уроков)](#содержание-список-уроков)
- [Команды Make](#команды-make)
- [Автор](#автор)

-------------

## О проекте

- Домашние задания по курсу ["SQLAlchemy"](https://greenatomcaselab.ispringlearn.ru/app/user-portal/learning-track/37358).

-------------

## Содержание (список уроков)

- ``27.04`` [Введение в базы данных и SQLAlchemy](hw1/README.md)
- ``30.04`` Устройство SQLAlchemy, работа с таблицами
- ``04.05`` [Запросы в SQLAlchemy](hw3/README.md)
- ``07.05`` Введение в ORM
- ``14.05`` Работа с объектами в ORM
- ``18.05`` Оптимизация запросов
- ``21.05`` Миграции, PyDantic, ИИ
- ``25.05`` Итоговое занятие

-------------

## Команды Make

Проект использует Makefile для автоматизации рутинных задач. Все команды запускаются через `make`.

**Основные команды:**

```bash
# Показать список всех доступных команд
make help

# Установить зависимости проекта
make install

# Запустить линтер ruff для проверки кода
make lint

# Автоматически исправить замечания линтера ruff
make lint-fix

# Форматировать код с помощью ruff
make format

# Проверить код (lint + format check)
make check

# Запустить тесты
make test

# Удалить временные файлы и кэш
make clean

# Запустить домашнее задание 1
make hw1

# Запустить домашнее задание 3
make hw3
```

**Примеры использования:**

```bash
# В WSL (Windows):
wsl make install
wsl make lint-fix
wsl make hw1
wsl make hw3

# В консоли Linux/MacOS: 
make install
make lint-fix
make hw1
make hw3
```

-------------

## Автор

- Mikhail Ikonnikov <mishaikon@gmail.com>

-------------
