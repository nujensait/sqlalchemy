# HW1: Введение в базы данных и SQLAlchemy

import sqlite3
from pathlib import Path


def print_separator(title=''):
    print('=' * 60)
    if title:
        print(f'{title:^60}')
        print('=' * 60)


def create_database():
    print_separator('ЗАДАНИЕ 1: Создание таблицы')

    db_path = Path(__file__).parent / 'library.db'
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            isbn TEXT UNIQUE,
            pages INTEGER DEFAULT 0,
            genre TEXT,
            available INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    print("✓ Таблица 'books' успешно создана")

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='books'"
    )
    if cursor.fetchone():
        print('✓ Проверка пройдена: таблица существует в базе данных')

    conn.close()
    return db_path


def fill_data(db_path):
    print()
    print_separator('ЗАДАНИЕ 2: Заполнение таблицы данными')

    books = [
        (
            'Мастер и Маргарита',
            'Михаил Булгаков',
            1967,
            '978-5-17-135043-1',
            480,
            'Роман',
            1,
        ),
        (
            'Преступление и наказание',
            'Федор Достоевский',
            1866,
            '978-5-04-116633-9',
            672,
            'Роман',
            1,
        ),
        (
            '1984',
            'Джордж Оруэлл',
            1949,
            '978-5-17-137262-4',
            320,
            'Антиутопия',
            1,
        ),
        (
            'Убить пересмешника',
            'Харпер Ли',
            1960,
            '978-5-04-116631-5',
            416,
            'Роман',
            0,
        ),
        (
            'Война и мир. Том 1',
            'Лев Толстой',
            1867,
            '978-5-17-135042-4',
            720,
            'Роман-эпопея',
            1,
        ),
        (
            'Анна Каренина',
            'Лев Толстой',
            1877,
            '978-5-04-116632-2',
            864,
            'Роман',
            0,
        ),
        (
            'Собачье сердце',
            'Михаил Булгаков',
            1925,
            '978-5-17-135044-8',
            352,
            'Повесть',
            1,
        ),
        (
            'Маленький принц',
            'Антуан де Сент-Экзюпери',
            1943,
            '978-5-04-116634-6',
            96,
            'Сказка',
            1,
        ),
        (
            'Три товарища',
            'Эрих Мария Ремарк',
            1936,
            '978-5-17-137263-1',
            384,
            'Роман',
            1,
        ),
        (
            'Портрет Дориана Грея',
            'Оскар Уайльд',
            1890,
            '978-5-04-116635-3',
            320,
            'Роман',
            0,
        ),
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO books (title, author, year, isbn, pages, genre, available)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        books,
    )

    conn.commit()
    print(f'✓ Добавлено книг: {cursor.rowcount}')

    cursor.execute('SELECT COUNT(*) FROM books')
    total = cursor.fetchone()[0]
    print(f'✓ Всего книг в таблице: {total}')

    conn.close()


def task_3_simple_selects(db_path):
    print()
    print_separator('ЗАДАНИЕ 3: Простые SELECT-запросы')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print()
    print('--- Все книги (полная информация) ---')
    cursor.execute('SELECT * FROM books')
    for row in cursor.fetchall():
        status = 'доступна' if row[7] == 1 else 'выдана'
        print(
            f'ID: {row[0]}, {row[1]}, {row[2]}, {row[3]} г., '
            f'{row[6]}, {row[4]} стр., {status}'
        )

    print()
    print('--- Названия и авторы ---')
    cursor.execute('SELECT title, author FROM books')
    for row in cursor.fetchall():
        print(f'«{row[0]}» — {row[1]}')

    print()
    print('--- Количество книг ---')
    cursor.execute('SELECT COUNT(*) FROM books')
    count = cursor.fetchone()[0]
    print(f'Всего книг в библиотеке: {count}')

    conn.close()


def task_4_where_filters(db_path):
    print()
    print_separator('ЗАДАНИЕ 4: Фильтрация с WHERE')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print()
    print('--- Книги Льва Толстого ---')
    cursor.execute(
        'SELECT title, year, pages, available FROM books '
        "WHERE author = 'Лев Толстой'"
    )
    for row in cursor.fetchall():
        status = 'доступна' if row[3] == 1 else 'выдана'
        print(f'«{row[0]}» ({row[1]}), {row[2]} стр. - {status}')

    print()
    print('--- Книги после 1900 года ---')
    cursor.execute(
        'SELECT year, title, author FROM books WHERE year > 1900 ORDER BY year'
    )
    for row in cursor.fetchall():
        print(f'{row[0]}: «{row[1]}» — {row[2]}')

    print()
    print('--- Доступные книги ---')
    cursor.execute('SELECT title, author FROM books WHERE available = 1')
    for row in cursor.fetchall():
        print(f'«{row[0]}» — {row[1]}')

    print()
    print('--- Романы с количеством страниц > 400 ---')
    cursor.execute(
        'SELECT title, author, pages FROM books '
        "WHERE genre = 'Роман' AND pages > 400"
    )
    for row in cursor.fetchall():
        print(f'«{row[0]}» — {row[1]}, {row[2]} стр.')

    print()
    print('--- Книги Булгакова или Достоевского ---')
    cursor.execute(
        'SELECT author, title, year FROM books '
        "WHERE author = 'Михаил Булгаков' "
        "OR author = 'Федор Достоевский' "
        'ORDER BY author, year'
    )
    for row in cursor.fetchall():
        print(f'{row[0]}: «{row[1]}» ({row[2]})')

    conn.close()


def task_5_sorting_limits(db_path):
    print()
    print_separator('ЗАДАНИЕ 5: Сортировка и ограничения')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print()
    print('--- Топ-3 самых толстых книг ---')
    cursor.execute(
        'SELECT title, author, pages FROM books ORDER BY pages DESC LIMIT 3'
    )
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f'{i}. «{row[0]}» — {row[1]}, {row[2]} стр.')

    print()
    print('--- Топ-3 самых старых книг ---')
    cursor.execute(
        'SELECT title, author, year FROM books ORDER BY year ASC LIMIT 3'
    )
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f'{i}. «{row[0]}» — {row[1]}, {row[2]} г.')

    print()
    print('--- Все книги (сортировка: по автору, затем по году) ---')
    cursor.execute(
        'SELECT author, year, title FROM books ORDER BY author, year'
    )

    current_author = None
    for row in cursor.fetchall():
        if row[0] != current_author:
            current_author = row[0]
            print(f'\n{current_author}:')
        print(f'  {row[1]} — «{row[2]}»')

    conn.close()


def task_6_updates(db_path):
    print()
    print_separator('ЗАДАНИЕ 6: Обновление данных')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print()
    print('--- Выдача книги по ISBN ---')
    cursor.execute(
        "UPDATE books SET available = 0 WHERE isbn = '978-5-17-135043-1'"
    )
    conn.commit()
    print(f'✓ Книга выдана. Обновлено записей: {cursor.rowcount}')

    print()
    print("--- Возврат книги 'Анна Каренина' ---")
    cursor.execute(
        "UPDATE books SET available = 1 WHERE title = 'Анна Каренина'"
    )
    conn.commit()
    print(f'✓ Книга возвращена. Обновлено записей: {cursor.rowcount}')

    print()
    print('--- Увеличение страниц у книг Льва Толстого ---')
    print('  До обновления:')
    cursor.execute(
        "SELECT title, pages FROM books WHERE author = 'Лев Толстой'"
    )
    for row in cursor.fetchall():
        print(f'    «{row[0]}»: {row[1]} стр.')

    cursor.execute(
        "UPDATE books SET pages = pages + 10 WHERE author = 'Лев Толстой'"
    )
    conn.commit()
    print(f'  ✓ Обновлено записей: {cursor.rowcount}')

    print('  После обновления:')
    cursor.execute(
        "SELECT title, pages FROM books WHERE author = 'Лев Толстой'"
    )
    for row in cursor.fetchall():
        print(f'    «{row[0]}»: {row[1]} стр.')

    print()
    print('--- Книги до 1900 года помечаются как недоступные ---')
    print('  Книги до 1900 года:')
    cursor.execute(
        'SELECT year, title, author FROM books WHERE year < 1900 ORDER BY year'
    )
    for row in cursor.fetchall():
        print(f'    {row[0]}: «{row[1]}» — {row[2]}')

    cursor.execute('UPDATE books SET available = 0 WHERE year < 1900')
    conn.commit()
    print(f'  ✓ Помечено как недоступные: {cursor.rowcount} книг')

    conn.close()


def task_7_deletes(db_path):
    print()
    print_separator('ЗАДАНИЕ 7: Удаление данных')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM books')
    total_before = cursor.fetchone()[0]
    print(f'Всего книг в библиотеке до удалений: {total_before}')

    print()
    print('--- Удаление книг, которых нет в наличии ---')
    print('  Будут удалены:')
    cursor.execute('SELECT title, author FROM books WHERE available = 0')
    for row in cursor.fetchall():
        print(f'    «{row[0]}» — {row[1]}')

    cursor.execute('DELETE FROM books WHERE available = 0')
    conn.commit()
    deleted_1 = cursor.rowcount
    print(f'  ✓ Удалено книг: {deleted_1}')

    print()
    print('--- Удаление книг с количеством страниц < 100 ---')
    cursor.execute('SELECT title, author, pages FROM books WHERE pages < 100')
    for row in cursor.fetchall():
        print(f'    «{row[0]}» — {row[1]}, {row[2]} стр.')

    cursor.execute('DELETE FROM books WHERE pages < 100')
    conn.commit()
    deleted_2 = cursor.rowcount
    print(f'  ✓ Удалено книг: {deleted_2}')

    print()
    print("--- Удаление книг жанра 'Сказка' ---")
    cursor.execute("DELETE FROM books WHERE genre = 'Сказка'")
    conn.commit()
    deleted_3 = cursor.rowcount
    print(f'  ✓ Удалено книг: {deleted_3}')

    print()
    print('--- Итог ---')
    cursor.execute('SELECT COUNT(*) FROM books')
    total_after = cursor.fetchone()[0]
    print(f'Книг осталось в библиотеке: {total_after}')
    print(f'Удалено всего: {total_before - total_after}')

    print()
    print('Оставшиеся книги:')
    cursor.execute('SELECT title, author, year, available FROM books')
    for row in cursor.fetchall():
        status = 'доступна' if row[3] == 1 else 'выдана'
        print(f'  «{row[0]}» — {row[1]} ({row[2]}) - {status}')

    conn.close()


def main():
    print_separator('ДОМАШНЕЕ ЗАДАНИЕ: БИБЛИОТЕКА')
    print()

    db_path = create_database()
    fill_data(db_path)
    task_3_simple_selects(db_path)
    task_4_where_filters(db_path)
    task_5_sorting_limits(db_path)
    task_6_updates(db_path)
    task_7_deletes(db_path)

    print()
    print_separator('ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ!')


if __name__ == '__main__':
    main()
