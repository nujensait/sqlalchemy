# HW2: Устройство SQLAlchemy, работа с таблицами

import os
from pathlib import Path

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
)

results = []


def save_results_to_file(filename: str = 'my_result.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')


def compare_results(
    my_file: str = 'my_result.txt', expected_file: str = 'result.txt'
):
    print('\n' + '=' * 60)
    print('🔍 СРАВНЕНИЕ РЕЗУЛЬТАТОВ С ЭТАЛОНОМ')
    print('=' * 60)

    if not os.path.exists(expected_file):
        print(f'⚠️  Эталонный файл {expected_file} не найден.')
        print('   Создайте его вручную или скопируйте от преподавателя.')
        print('   Пропускаю сравнение...')
        return False

    if not os.path.exists(my_file):
        print(f'❌ Файл с моими результатами {my_file} не найден!')
        return False

    with open(my_file, 'r', encoding='utf-8') as f:
        my_lines = [line.rstrip() for line in f.readlines()]

    with open(expected_file, 'r', encoding='utf-8') as f:
        expected_lines = [line.rstrip() for line in f.readlines()]

    assert len(my_lines) == len(expected_lines), (
        f'Разное количество строк: моих {len(my_lines)}, эталон '
        f'{len(expected_lines)}'
    )

    differences = []
    for i, (my_line, expected_line) in enumerate(
        zip(my_lines, expected_lines)
    ):
        if my_line != expected_line:
            differences.append(
                f'Строка {i + 1}:\n  '
                f'Моя:     {my_line}\n  Эталон:  {expected_line}'
            )

    if differences:
        print('❌ НАЙДЕНЫ РАЗЛИЧИЯ:')
        for diff in differences:
            print(diff)

        assert False, f'Найдено {len(differences)} различий с эталоном'
    else:
        print('✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!')
        return True


def add_section(title: str):
    results.append('\n' + '=' * 10 + title + '=' * 10)


def create_tables(engine, metadata):
    books = Table(
        'books',
        metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('title', String, nullable=False),
        Column('author', String, nullable=False),
        Column('year', Integer),
        Column('isbn', String, unique=True),
        Column('pages', Integer, default=0),
        Column('genre', String),
        Column('available', Integer, default=1),
    )

    users = Table(
        'users',
        metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(30), nullable=False, unique=True),
        Column('fullname', String(50)),
        Column('book_id', Integer, ForeignKey('books.id'), nullable=False),
    )

    metadata.create_all(engine)

    return books, users


def insert_books(engine, books):
    books_data = [
        {
            'title': 'Мастер и Маргарита',
            'author': 'Михаил Булгаков',
            'year': 1967,
            'isbn': '978-5-17-135043-1',
            'pages': 480,
            'genre': 'Роман',
            'available': 1,
        },
        {
            'title': 'Преступление и наказание',
            'author': 'Федор Достоевский',
            'year': 1866,
            'isbn': '978-5-04-116633-9',
            'pages': 672,
            'genre': 'Роман',
            'available': 1,
        },
        {
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'year': 1949,
            'isbn': '978-5-17-137262-4',
            'pages': 320,
            'genre': 'Антиутопия',
            'available': 1,
        },
        {
            'title': 'Убить пересмешника',
            'author': 'Харпер Ли',
            'year': 1960,
            'isbn': '978-5-04-116631-5',
            'pages': 416,
            'genre': 'Роман',
            'available': 0,
        },
        {
            'title': 'Война и мир. Том 1',
            'author': 'Лев Толстой',
            'year': 1867,
            'isbn': '978-5-17-135042-4',
            'pages': 720,
            'genre': 'Роман-эпопея',
            'available': 1,
        },
        {
            'title': 'Анна Каренина',
            'author': 'Лев Толстой',
            'year': 1877,
            'isbn': '978-5-04-116632-2',
            'pages': 864,
            'genre': 'Роман',
            'available': 0,
        },
        {
            'title': 'Собачье сердце',
            'author': 'Михаил Булгаков',
            'year': 1925,
            'isbn': '978-5-17-135044-8',
            'pages': 352,
            'genre': 'Повесть',
            'available': 1,
        },
        {
            'title': 'Маленький принц',
            'author': 'Антуан де Сент-Экзюпери',
            'year': 1943,
            'isbn': '978-5-04-116634-6',
            'pages': 96,
            'genre': 'Сказка',
            'available': 1,
        },
        {
            'title': 'Три товарища',
            'author': 'Эрих Мария Ремарк',
            'year': 1936,
            'isbn': '978-5-17-137263-1',
            'pages': 384,
            'genre': 'Роман',
            'available': 1,
        },
        {
            'title': 'Портрет Дориана Грея',
            'author': 'Оскар Уайльд',
            'year': 1890,
            'isbn': '978-5-04-116635-3',
            'pages': 320,
            'genre': 'Роман',
            'available': 0,
        },
    ]

    with engine.connect() as conn:
        conn.execute(books.delete())
        conn.commit()

        result = conn.execute(books.insert().returning(books.c.id), books_data)
        book_ids = [row[0] for row in result]
        conn.commit()

        add_section('2.1. Добавление книг')
        results.append(f'Добавлено книг: {len(book_ids)}')


def insert_users(engine, users):
    users_data = [
        {'name': 'alice', 'fullname': 'Alice Wonderland', 'book_id': 1},
        {'name': 'bob', 'fullname': 'Bob Builder', 'book_id': 3},
        {'name': 'charlie', 'fullname': 'Charlie Brown', 'book_id': 2},
        {'name': 'diana', 'fullname': 'Diana Princess', 'book_id': 7},
        {'name': 'eve', 'fullname': 'Eve Smith', 'book_id': 5},
    ]

    with engine.connect() as conn:
        conn.execute(users.delete())
        conn.commit()

        result = conn.execute(users.insert(), users_data)
        conn.commit()

        add_section('2.2. Добавление пользователей')
        results.append(f'Добавлено пользователей: {result.rowcount}')


def execute_queries(engine, books, users):
    with engine.connect() as conn:
        add_section('3.1. Все книги (все поля)')
        result = conn.execute(select(books))
        for row in result:
            results.append(str(tuple(row)))

        add_section('3.2. Все пользователи (все поля)')
        result = conn.execute(select(users))
        for row in result:
            results.append(str(tuple(row)))

        add_section('3.3. Доступные книги (available = 1)')
        result = conn.execute(
            select(books).where(books.c.available == 1)
        )
        for row in result:
            results.append(str(tuple(row)))

        add_section("3.4. Авторы с буквой 'э'")
        result = conn.execute(
            select(books).where(books.c.author.like('%э%'))
        )
        for row in result:
            results.append(str(tuple(row)))

        add_section('3.5. Доступные книги, год которых меньше 1900')
        result = conn.execute(
            select(books).where(
                (books.c.available == 1) & (books.c.year < 1900)
            )
        )
        for row in result:
            results.append(str(tuple(row)))

        add_section('3.6. Ник и ФИО пользователей')
        result = conn.execute(select(users.c.name, users.c.fullname))
        for row in result:
            results.append(f'{row[0]}: {row[1]}')

        add_section('3.7. * Пользователи и их книги (с JOIN)')
        result = conn.execute(
            select(
                users.c.name,
                users.c.fullname,
                books.c.title,
                books.c.author,
            ).select_from(users.join(books, users.c.book_id == books.c.id))
        )
        for row in result:
            results.append(
                f"{row[0]}: ({row[1]}) -> '{row[2]}' - {row[3]}"
            )


def main():
    db_path = Path(__file__).parent / 'bookstore.db'
    if db_path.exists():
        db_path.unlink()

    engine = create_engine(f'sqlite:///{db_path}')
    metadata = MetaData()

    books, users = create_tables(engine, metadata)

    insert_books(engine, books)

    insert_users(engine, users)

    execute_queries(engine, books, users)

    print(*results, sep='\n')

    save_results_to_file()

    compare_results()


if __name__ == '__main__':
    main()
