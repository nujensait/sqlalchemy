# HW4: Введение в ORM

import os

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

results = []


class ResultHandler:
    """Класс для обработки и сохранения результатов запросов."""

    @staticmethod
    def add_section(title: str) -> None:
        """Добавляет заголовок раздела в результаты.

        Args:
            title (str): Название раздела
        """
        results.append('\n' + '=' * 10 + title + '=' * 10)

    @staticmethod
    def save_results_to_file(filename: str = 'hw4/my_result.txt') -> None:
        """Сохраняет результаты в файл.

        Args:
            filename (str): Имя файла для сохранения
        """
        with open(filename, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')

    @staticmethod
    def compare_results(
        my_file: str = 'hw4/my_result.txt',
        expected_file: str = 'hw4/result.txt',
    ) -> bool:
        """Сравнивает результаты с эталоном.

        Args:
            my_file (str): Файл с моими результатами
            expected_file (str): Эталонный файл

        Returns:
            bool: True если результаты совпадают, False иначе
        """
        print('\n' + '=' * 60)
        print('🔍 СРАВНЕНИЕ РЕЗУЛЬТАТОВ С ЭТАЛОНОМ')
        print('=' * 60)

        if not os.path.exists(expected_file):
            print(f'⚠️  Эталонный файл {expected_file} не найден.')
            print('   Создайте его вручную.')
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
            zip(my_lines, expected_lines)  # noqa: B905
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

            assert False, f'Найдено {len(differences)} различий с эталоном'  # noqa: B011, PT015
        else:
            print('✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!')
            return True


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
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
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
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None] = mapped_column(String(50))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))

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


class LibraryORM:
    """Класс для работы с библиотекой через ORM."""

    def __init__(
        self, db_url: str = 'sqlite:///bookstore.db', echo: bool = True
    ) -> None:
        """Инициализация библиотеки.

        Args:
            db_url (str): URL базы данных
            echo (bool): Выводить ли SQL-запросы в консоль
        """
        self.engine = create_engine(db_url, echo=echo)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        """Создает таблицы в базе данных."""
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def insert_books(self) -> None:
        """Добавляет книги в базу данных."""
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

        with self.Session() as session:
            books = [Book(**data) for data in books_data]
            session.add_all(books)
            session.flush()
            book_ids = [book.id for book in books]
            session.commit()

            ResultHandler.add_section('2.1. Добавление книг')
            results.append(f'Добавлено книг: {len(book_ids)}')

    def insert_users(self) -> None:
        """Добавляет пользователей в базу данных."""
        users_data = [
            {'name': 'alice', 'fullname': 'Alice Wonderland', 'book_id': 1},
            {'name': 'bob', 'fullname': 'Bob Builder', 'book_id': 3},
            {'name': 'charlie', 'fullname': 'Charlie Brown', 'book_id': 2},
            {'name': 'diana', 'fullname': 'Diana Princess', 'book_id': 7},
            {'name': 'eve', 'fullname': 'Eve Smith', 'book_id': 5},
        ]

        with self.Session() as session:
            users = [User(**data) for data in users_data]
            session.add_all(users)
            session.commit()

            ResultHandler.add_section('2.2. Добавление пользователей')
            results.append(f'Добавлено пользователей: {len(users)}')

    def execute_queries(self) -> None:
        """Выполняет SELECT-запросы."""
        with self.Session() as session:
            ResultHandler.add_section('3.1. Все книги (все поля)')
            books = session.query(Book).all()
            for book in books:
                results.append(str(book))

            ResultHandler.add_section('3.2. Все пользователи (все поля)')
            users = session.query(User).all()
            for user in users:
                results.append(str(user))

            ResultHandler.add_section('3.3. Доступные книги (available = 1)')
            books = session.query(Book).where(Book.available == 1).all()
            for book in books:
                results.append(str(book))

            ResultHandler.add_section(
                "3.4. Книги, авторы которых имеют букву 'э'"
            )
            books = session.query(Book).where(Book.author.contains('э')).all()
            for book in books:
                results.append(str(book))

            ResultHandler.add_section(
                '3.5. Доступные книги, год которых меньше 1900'
            )
            books = (
                session
                .query(Book)
                .where(Book.available == 1, Book.year < 1900)
                .all()
            )
            for book in books:
                results.append(str(book))

            ResultHandler.add_section('3.6. Ник и ФИО пользователей')
            users = session.query(User.name, User.fullname).all()
            for name, fullname in users:
                results.append(f'{name}: {fullname}')

            ResultHandler.add_section('3.7. Пользователи и их книги')
            users = session.query(User).all()
            for user in users:
                results.append(
                    f'{user.name} ({user.fullname}): {user.book.title}'
                )

    def run_all(self) -> None:
        """Запускает все операции."""
        self.create_tables()

        self.insert_books()
        self.insert_users()

        self.execute_queries()

        print(*results, sep='\n')

        ResultHandler.save_results_to_file()

        ResultHandler.compare_results()


def main() -> None:
    """Основная функция программы."""
    library = LibraryORM()
    library.run_all()


if __name__ == '__main__':
    main()
