.PHONY: help lint lint-fix format check test clean install hw1 hw2 hw3

help:
	@echo "Доступные команды:"
	@echo "  make help       - показать список команд"
	@echo "  make install    - установить зависимости проекта"
	@echo "  make lint       - запустить линтер ruff"
	@echo "  make lint-fix   - исправить замечания линтера ruff"
	@echo "  make format     - форматировать код с помощью ruff"
	@echo "  make check      - проверить код (lint + format check)"
	@echo "  make test       - запустить тесты"
	@echo "  make clean      - удалить временные файлы и кэш"
	@echo "  make hw1        - запустить домашнее задание 1"
	@echo "  make hw2        - запустить домашнее задание 2"
	@echo "  make hw3        - запустить домашнее задание 3"

install:
	@echo "Установка зависимостей..."
	uv sync

lint:
	@echo "Запуск линтера ruff..."
	uv run ruff check .

lint-fix:
	@echo "Исправление замечаний линтера ruff..."
	uv run ruff check --fix .

format:
	@echo "Форматирование кода..."
	uv run ruff format .

check: lint
	@echo "Проверка форматирования..."
	uv run ruff format --check .

test:
	@echo "Запуск тестов..."
	@echo "Тесты пока не настроены"

clean:
	@echo "Очистка временных файлов..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.db" -delete 2>/dev/null || true
	@echo "Очистка завершена"

hw1:
	@echo "Запуск домашнего задания 1..."
	uv run python hw1/hw1.py

hw2:
	@echo "Запуск домашнего задания 2..."
	cd hw2 && uv run python hw2.py

hw3:
	@echo "Запуск домашнего задания 3..."
	cd hw3 && uv run python hw3.py
