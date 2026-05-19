import os
from pathlib import Path

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    delete,
    desc,
    func,
    or_,
    select,
    update,
)

results = []


def add_section(title):
    results.append('\n' + '=' * 10 + title + '=' * 10)


def save_results_to_file(filename='my_result.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')


def compare_results(my_file='my_result.txt', expected_file='result.txt'):
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
        zip(my_lines, expected_lines, strict=True)
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

        raise AssertionError(
            f'Найдено {len(differences)} различий с эталоном'
        )
    else:
        print('✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!')
        return True


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
        Column('count', Integer, default=1),
        Column('price', Float, nullable=False, default=0),
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


def fill_tables(engine, books, users):
    add_section('2. ЗАПОЛНЕНИЕ ТАБЛИЦ ДАННЫМИ')

    books_data = [
        {
            'title': 'Война и мир',
            'author': 'Лев Толстой',
            'year': 1869,
            'isbn': '978-5-699-12345-1',
            'pages': 1225,
            'genre': 'Роман',
            'count': 5,
            'price': 1200.50,
            'available': 1,
        },
        {
            'title': 'Преступление и наказание',
            'author': 'Федор Достоевский',
            'year': 1866,
            'isbn': '978-5-699-12345-2',
            'pages': 672,
            'genre': 'Роман',
            'count': 3,
            'price': 890.00,
            'available': 1,
        },
        {
            'title': 'Мастер и Маргарита',
            'author': 'Михаил Булгаков',
            'year': 1967,
            'isbn': '978-5-699-12345-3',
            'pages': 480,
            'genre': 'Роман',
            'count': 4,
            'price': 750.50,
            'available': 1,
        },
        {
            'title': 'Евгений Онегин',
            'author': 'Александр Пушкин',
            'year': 1833,
            'isbn': '978-5-699-12345-4',
            'pages': 288,
            'genre': 'Роман в стихах',
            'count': 2,
            'price': 450.00,
            'available': 1,
        },
        {
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'year': 1949,
            'isbn': '978-5-699-12345-5',
            'pages': 320,
            'genre': 'Антиутопия',
            'count': 0,
            'price': 650.00,
            'available': 0,
        },
        {
            'title': 'Улисс',
            'author': 'Джеймс Джойс',
            'year': 1922,
            'isbn': '978-5-699-12345-6',
            'pages': 736,
            'genre': 'Модернизм',
            'count': 1,
            'price': 1500.00,
            'available': 1,
        },
        {
            'title': 'Сто лет одиночества',
            'author': 'Габриэль Гарсиа Маркес',
            'year': 1967,
            'isbn': '978-5-699-12345-7',
            'pages': 544,
            'genre': 'Магический реализм',
            'count': 2,
            'price': 850.00,
            'available': 1,
        },
        {
            'title': 'Божественная комедия',
            'author': 'Данте Алигьери',
            'year': 1320,
            'isbn': '978-5-699-12345-8',
            'pages': 960,
            'genre': 'Поэма',
            'count': 1,
            'price': 1100.00,
            'available': 1,
        },
        {
            'title': 'Илиада',
            'author': 'Гомер',
            'year': -750,
            'isbn': '978-5-699-12345-9',
            'pages': 704,
            'genre': 'Эпос',
            'count': 1,
            'price': 950.00,
            'available': 1,
        },
    ]

    users_data = [
        {'name': 'ivan', 'fullname': 'Иван Петров', 'book_id': 1},
        {'name': 'maria', 'fullname': 'Мария Иванова', 'book_id': 1},
        {'name': 'petr', 'fullname': 'Петр Сидоров', 'book_id': 2},
        {'name': 'anna', 'fullname': 'Анна Смирнова', 'book_id': 3},
        {'name': 'alex', 'fullname': 'Алексей Козлов', 'book_id': 4},
        {'name': 'elena', 'fullname': 'Елена Новикова', 'book_id': 5},
        {'name': 'dmitry', 'fullname': 'Дмитрий Морозов', 'book_id': 6},
        {'name': 'olga', 'fullname': 'Ольга Волкова', 'book_id': 7},
        {'name': 'nikolay', 'fullname': 'Николай Соколов', 'book_id': 8},
        {'name': 'tatyana', 'fullname': 'Татьяна Лебедева', 'book_id': 9},
        {'name': 'andrey', 'fullname': 'Андрей Павлов', 'book_id': 1},
        {'name': 'svetlana', 'fullname': 'Светлана Михайлова', 'book_id': 3},
    ]

    with engine.begin() as conn:
        conn.execute(books.delete())
        conn.execute(users.delete())

        result = conn.execute(books.insert().returning(books.c.id), books_data)
        book_ids = [row[0] for row in result]
        results.append(f'Добавлено книг: {len(book_ids)}')

        result = conn.execute(users.insert(), users_data)
        results.append(f'Добавлено пользователей: {result.rowcount}')


def run_queries(engine, books, users):
    with engine.begin() as conn:
        add_section('3.1 Доступные книги с ценой меньше 1000 рублей')
        result = conn.execute(
            select(books.c.title, books.c.price)
            .where((books.c.available == 1) & (books.c.price < 1000))
            .order_by(books.c.id)
        )
        for row in result:
            results.append(f'{row[0]} - {row[1]} руб.')

        add_section('3.2 Все книги авторов Достоевского ИЛИ Толстого')
        result = conn.execute(
            select(books.c.author, books.c.title).where(
                or_(
                    books.c.author == 'Федор Достоевский',
                    books.c.author == 'Лев Толстой',
                )
            )
        )
        for row in result:
            results.append(f'{row[0]}: {row[1]}')

        add_section('3.3 Доступные книги 19 века или с >1000 страниц')
        result = conn.execute(
            select(books.c.title, books.c.year, books.c.pages).where(
                (books.c.available == 1)
                & (
                    ((books.c.year >= 1800) & (books.c.year <= 1899))
                    | (books.c.pages > 1000)
                )
            )
        )
        for row in result:
            results.append(f'{row[0]} ({row[1]} год) - {row[2]} стр.')

        add_section('3.4 Пользователи с доступными книгами')
        result = conn.execute(
            select(users.c.fullname, users.c.name, books.c.title)
            .select_from(users.join(books, users.c.book_id == books.c.id))
            .where(books.c.available == 1)
            .order_by(users.c.fullname)
        )
        for row in result:
            results.append(f'{row[0]} ({row[1]}) - {row[2]}')

        add_section('3.5 Книги, которые никто не взял')
        result = conn.execute(
            select(books.c.title, books.c.author)
            .select_from(
                books.outerjoin(users, books.c.id == users.c.book_id)
            )
            .where(users.c.id.is_(None))
        )
        for row in result:
            results.append(f'{row[0]} - {row[1]}')

        add_section('3.6 Статистика по доступным книгам')
        result = conn.execute(
            select(
                func.count(books.c.id).label('total_titles'),
                func.sum(books.c.count).label('total_count'),
                func.avg(books.c.price).label('avg_price'),
                func.min(books.c.price).label('min_price'),
                func.max(books.c.price).label('max_price'),
            ).where(books.c.available == 1)
        )
        row = result.fetchone()
        results.append('Статистика по доступным книгам:')
        results.append(f'   Всего наименований: {row[0]}')
        results.append(f'   Всего экземпляров: {row[1]}')
        results.append(f'   Средняя цена: {row[2]:.2f} руб.')
        results.append(f'   Мин. цена: {row[3]} руб.')
        results.append(f'   Макс. цена: {row[4]} руб.')

        add_section('3.7 Книги по году (новые сначала) и алфавиту')
        result = conn.execute(
            select(books.c.year, books.c.title, books.c.author).order_by(
                desc(books.c.year), books.c.title
            )
        )
        for row in result:
            results.append(f'{row[0]}: {row[1]} - {row[2]}')

        add_section('3.8 Статистика по жанрам')
        result = conn.execute(
            select(
                books.c.genre,
                func.count(books.c.id).label('count'),
                func.avg(books.c.price).label('avg_price'),
            )
            .group_by(books.c.genre)
            .order_by(desc('count'))
        )
        for row in result:
            results.append(
                f'{row[0]}: {row[1]} книг, средняя цена {row[2]:.2f} руб.'
            )

    with engine.begin() as conn:
        add_section('3.9 Обновление цен (книги Толстого +10%)')
        stmt = (
            update(books)
            .where(books.c.author == 'Лев Толстой')
            .values(price=books.c.price * 1.1)
            .returning(books.c.id, books.c.title, books.c.price)
        )
        result = conn.execute(stmt)
        for row in result:
            results.append(
                f'ID {row[0]}: {row[1]} - новая цена {row[2]:.2f} руб.'
            )

    with engine.begin() as conn:
        add_section('3.10 Удаление книг с отрицательным годом')
        stmt = (
            delete(books)
            .where(books.c.year < 0)
            .returning(books.c.id, books.c.title, books.c.year)
        )
        result = conn.execute(stmt)
        for row in result:
            results.append(f'ID {row[0]}: {row[1]} ({row[2]} год)')


def main():
    db_path = Path(__file__).parent / 'bookstore.db'
    if db_path.exists():
        db_path.unlink()

    engine = create_engine(f'sqlite:///{db_path}')
    metadata = MetaData()

    books, users = create_tables(engine, metadata)

    fill_tables(engine, books, users)

    run_queries(engine, books, users)

    print(*results, sep='\n')

    save_results_to_file()

    compare_results()


if __name__ == '__main__':
    main()
