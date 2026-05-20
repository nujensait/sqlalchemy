# HW4: Введение в ORM

from pathlib import Path

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей ORM."""

    pass


class Book(Base):
    """Модель книги в библиотеке.

    Attributes:
        id (int): Уникальный идентификатор книги
        title (str): Название книги
        author (str): Автор книги
        year (int | None): Год издания
        isbn (str | None): ISBN книги (уникальный)
        pages (int): Количество страниц (по умолчанию 0)
        genre (str | None): Жанр книги
        available (int): Доступность книги (1 - доступна, 0 - выдана)
        users (list[User]): Список пользователей, взявших эту книгу
    """

    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int | None] = mapped_column()
    isbn: Mapped[str | None] = mapped_column(String, unique=True)
    pages: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str | None] = mapped_column(String)
    available: Mapped[int] = mapped_column(default=1)

    users: Mapped[list['User']] = relationship(back_populates='book')

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта книги.

        Returns:
            str: Строка с полной информацией о книге
        """
        return (
            f"Book(id={self.id}, title='{self.title}', "
            f"author='{self.author}', year={self.year}, "
            f"isbn='{self.isbn}', pages={self.pages}, "
            f"genre='{self.genre}', available={self.available})"
        )


class User(Base):
    """Модель пользователя библиотеки.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        name (str): Ник пользователя (уникальный, до 30 символов)
        fullname (str | None): Полное имя пользователя (до 50 символов)
        book_id (int): ID взятой книги (внешний ключ на books.id)
        book (Book): Объект книги, взятой пользователем
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    fullname: Mapped[str | None] = mapped_column(String(50))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)

    book: Mapped['Book'] = relationship(back_populates='users')

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта пользователя.

        Returns:
            str: Строка с полной информацией о пользователе
        """
        return (
            f"User(id={self.id}, name='{self.name}', "
            f"fullname='{self.fullname}', book_id={self.book_id})"
        )


def add_section(title: str) -> None:
    """Выводит заголовок раздела с разделителем.

    Args:
        title (str): Название раздела

    Returns:
        None
    """
    print()
    print(f'={title:=<50}')


def save_results_to_file(results: list[str], filename: str) -> None:
    """Сохраняет результаты запросов в файл.

    Args:
        results (list[str]): Список строк с результатами
        filename (str): Путь к файлу для сохранения

    Returns:
        None
    """
    with Path(filename).open('w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')


def compare_results(file1: str, file2: str) -> None:
    """Сравнивает содержимое двух файлов и выводит различия.

    Args:
        file1 (str): Путь к первому файлу (полученные результаты)
        file2 (str): Путь к второму файлу (эталонные результаты)

    Returns:
        None
    """
    with (
        Path(file1).open('r', encoding='utf-8') as f1,
        Path(file2).open('r', encoding='utf-8') as f2,
    ):
        content1 = f1.read()
        content2 = f2.read()

    if content1 == content2:
        print('\n✓ Результаты совпадают с эталоном!')
    else:
        print('\n✗ Результаты НЕ совпадают с эталоном!')
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        for i, (line1, line2) in enumerate(zip(lines1, lines2, strict=True), 1):
            if line1 != line2:
                print(f'Строка {i}:')
                print(f'  Ожидается: {line2}')
                print(f'  Получено:  {line1}')


def main() -> None:
    """Основная функция программы.

    Выполняет следующие действия:
    1. Создает базу данных bookstore.db
    2. Добавляет книги и пользователей
    3. Выполняет SELECT-запросы
    4. Сохраняет результаты в файл
    5. Сравнивает с эталонным файлом

    Returns:
        None
    """
    db_path = Path(__file__).parent / 'bookstore.db'
    if db_path.exists():
        db_path.unlink()

    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)

    results: list[str] = []

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

    with Session(engine) as session:
        add_section('2.1. Добавление книг')
        books = [Book(**data) for data in books_data]
        session.add_all(books)
        session.flush()
        book_ids = [book.id for book in books]
        session.commit()
        print(f'Добавлено книг: {len(book_ids)}')
        results.append('')
        results.append('==========2.1. Добавление книг==========')
        results.append(f'Добавлено книг: {len(book_ids)}')

    users_data = [
        {'name': 'alice', 'fullname': 'Alice Wonderland', 'book_id': 1},
        {'name': 'bob', 'fullname': 'Bob Builder', 'book_id': 3},
        {'name': 'charlie', 'fullname': 'Charlie Brown', 'book_id': 2},
        {'name': 'diana', 'fullname': 'Diana Princess', 'book_id': 7},
        {'name': 'eve', 'fullname': 'Eve Smith', 'book_id': 5},
    ]

    with Session(engine) as session:
        add_section('2.2. Добавление пользователей')
        users = [User(**data) for data in users_data]
        session.add_all(users)
        session.commit()
        print(f'Добавлено пользователей: {len(users)}')
        results.append('')
        results.append('==========2.2. Добавление пользователей==========')
        results.append(f'Добавлено пользователей: {len(users)}')

    with Session(engine) as session:
        add_section('3.1. Все книги (все поля)')
        books = session.query(Book).all()
        results.append('')
        results.append('==========3.1. Все книги (все поля)==========')
        for book in books:
            print(book)
            results.append(str(book))

    with Session(engine) as session:
        add_section('3.2. Все пользователи (все поля)')
        users = session.query(User).all()
        results.append('')
        results.append('==========3.2. Все пользователи (все поля)==========')
        for user in users:
            print(user)
            results.append(str(user))

    with Session(engine) as session:
        add_section('3.3. Доступные книги (available = 1)')
        books = session.query(Book).filter(Book.available == 1).all()
        results.append('')
        results.append('==========3.3. Доступные книги (available = 1)==========')
        for book in books:
            print(book)
            results.append(str(book))

    with Session(engine) as session:
        add_section("3.4. Книги, авторы которых имеют букву 'э'")
        books = session.query(Book).filter(Book.author.contains('э')).all()
        results.append('')
        results.append("==========3.4. Книги, авторы которых имеют букву 'э'==========")
        for book in books:
            print(book)
            results.append(str(book))

    with Session(engine) as session:
        add_section('3.5. Доступные книги, год которых меньше 1900')
        books = (
            session.query(Book)
            .filter(Book.available == 1, Book.year < 1900)
            .all()
        )
        results.append('')
        results.append(
            '==========3.5. Доступные книги, год которых меньше 1900=========='
        )
        for book in books:
            print(book)
            results.append(str(book))

    with Session(engine) as session:
        add_section('3.6. Ник и ФИО пользователей')
        users = session.query(User.name, User.fullname).all()
        results.append('')
        results.append('==========3.6. Ник и ФИО пользователей==========')
        for name, fullname in users:
            print(f'{name}: {fullname}')
            results.append(f'{name}: {fullname}')

    with Session(engine) as session:
        add_section('3.7. Пользователи и их книги')
        users = session.query(User).all()
        results.append('')
        results.append('==========3.7. Пользователи и их книги==========')
        for user in users:
            print(f'{user.name} ({user.fullname}): {user.book.title}')
            results.append(f'{user.name} ({user.fullname}): {user.book.title}')

    save_results_to_file(results, 'hw4/my_result.txt')
    compare_results('hw4/my_result.txt', 'hw4/result.txt')


if __name__ == '__main__':
    main()
