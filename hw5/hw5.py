# HW5: Работа с объектами в ORM

import os

from sqlalchemy import (
    ForeignKey,
    String,
    create_engine,
    distinct,
    func,
    or_,
    update,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

AVAILABLE = 1
NOT_AVAILABLE = 0

results = []


class ResultHandler:
    """Класс для работы с результатами запросов."""

    @staticmethod
    def add_section(title: str) -> None:
        """Добавляет заголовок раздела в результаты.

        Args:
            title (str): Название раздела
        """
        results.append('\n' + '=' * 10 + title + '=' * 10)

    @staticmethod
    def save_results_to_file(filename: str = 'my_result.txt') -> None:
        """Сохраняет результаты в файл.

        Args:
            filename (str): Имя файла для сохранения
        """
        with open(filename, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')

    @staticmethod
    def compare_results(
        my_file: str = 'my_result.txt', expected_file: str = 'result.txt'
    ) -> bool:
        """Сравнивает результаты с эталоном.

        Args:
            my_file (str): Файл с результатами
            expected_file (str): Эталонный файл

        Returns:
            bool: True если результаты совпадают, False иначе
        """
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
            zip(my_lines, expected_lines, strict=False)
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


class Base(DeclarativeBase):
    """Базовый класс для всех моделей ORM."""

    pass


class Book(Base):
    """Модель книги в магазине.

    Attributes:
        id (int): Уникальный идентификатор книги
        title (str): Название книги
        author (str): Автор книги
        year (int | None): Год издания
        isbn (str | None): ISBN книги (уникальный)
        pages (int): Количество страниц (по умолчанию 0)
        genre (str | None): Жанр книги
        count (int): Количество экземпляров (по умолчанию 1)
        price (float): Цена книги (по умолчанию 0)
        users (list[UserBookAssociation]): Список пользователей книги
    """

    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    year: Mapped[int | None] = mapped_column()
    isbn: Mapped[str | None] = mapped_column(String, unique=True)
    pages: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str | None] = mapped_column(String)
    count: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column(default=0)

    users: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='book', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта книги.

        Returns:
            str: Строка с полной информацией о книге
        """
        return (
            f"Book(id={self.id}, title='{self.title}', "
            f"author='{self.author}', year='{self.year}', "
            f"isbn='{self.isbn}', pages='{self.pages}', "
            f"genre='{self.genre}', count='{self.count}', "
            f"price='{self.price}')"
        )


class User(Base):
    """Модель пользователя магазина.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        name (str): Ник пользователя (уникальный, до 30 символов)
        fullname (str | None): Полное имя (до 50 символов)
        books (list[UserBookAssociation]): Список книг пользователя
        delivery_info (list[Delivery]): Список данных доставки
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None] = mapped_column(String(50))

    books: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    delivery_info: Mapped[list['Delivery']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта пользователя.

        Returns:
            str: Строка с полной информацией о пользователе
        """
        return (
            f"User(id={self.id}, name='{self.name}', "
            f"fullname='{self.fullname}')"
        )


class UserBookAssociation(Base):
    """Ассоциативная таблица для связи пользователей и книг.

    Attributes:
        user_id (int): ID пользователя (внешний ключ на users.id)
        book_id (int): ID книги (внешний ключ на books.id)
        user (User): Объект пользователя
        book (Book): Объект книги
    """

    __tablename__ = 'user_book_association'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id'), primary_key=True
    )

    user: Mapped['User'] = relationship(back_populates='books')
    book: Mapped['Book'] = relationship(back_populates='users')

    def __repr__(self) -> str:
        """Возвращает строковое представление ассоциации.

        Returns:
            str: Строка с информацией об ассоциации
        """
        return (
            f'UserBookAssociation(user_id={self.user_id}, '
            f'book_id={self.book_id})'
        )


class Delivery(Base):
    """Модель данных доставки.

    Attributes:
        id (int): Уникальный идентификатор
        user_id (int): ID пользователя (внешний ключ на users.id)
        email (str | None): Почта (уникальная, до 50 символов)
        address (str | None): Адрес пользователя
        phone (str | None): Телефон (уникальный, до 15 символов)
        user (User): Объект пользователя
    """

    __tablename__ = 'delivery'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    email: Mapped[str | None] = mapped_column(String(50), unique=True)
    address: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String(15), unique=True)

    user: Mapped['User'] = relationship(back_populates='delivery_info')

    def __repr__(self) -> str:
        """Возвращает строковое представление данных доставки.

        Returns:
            str: Строка с информацией о доставке
        """
        return (
            f'Delivery(id={self.id}, user_id={self.user_id}, '
            f"email='{self.email}', address='{self.address}', "
            f"phone='{self.phone}')"
        )


class BookStore:
    """Класс для управления книжным магазином."""

    def __init__(
        self, db_url: str = 'sqlite:///bookstore.db', echo: bool = True
    ) -> None:
        """Инициализирует подключение к БД.

        Args:
            db_url (str): URL базы данных
            echo (bool): Включить логирование SQL запросов
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
                'count': 5,
                'price': 890.0,
            },
            {
                'title': 'Преступление и наказание',
                'author': 'Федор Достоевский',
                'year': 1866,
                'isbn': '978-5-04-116633-9',
                'pages': 672,
                'genre': 'Роман',
                'count': 3,
                'price': 750.0,
            },
            {
                'title': '1984',
                'author': 'Джордж Оруэлл',
                'year': 1949,
                'isbn': '978-5-17-137262-4',
                'pages': 320,
                'genre': 'Антиутопия',
                'count': 2,
                'price': 650.0,
            },
            {
                'title': 'Убить пересмешника',
                'author': 'Харпер Ли',
                'year': 1960,
                'isbn': '978-5-04-116631-5',
                'pages': 416,
                'genre': 'Роман',
                'count': 0,
                'price': 550.0,
            },
            {
                'title': 'Война и мир. Том 1',
                'author': 'Лев Толстой',
                'year': 1867,
                'isbn': '978-5-17-135042-4',
                'pages': 720,
                'genre': 'Роман-эпопея',
                'count': 1,
                'price': 1200.0,
            },
            {
                'title': 'Анна Каренина',
                'author': 'Лев Толстой',
                'year': 1877,
                'isbn': '978-5-04-116632-2',
                'pages': 864,
                'genre': 'Роман',
                'count': 0,
                'price': 950.0,
            },
            {
                'title': 'Собачье сердце',
                'author': 'Михаил Булгаков',
                'year': 1925,
                'isbn': '978-5-17-135044-8',
                'pages': 352,
                'genre': 'Повесть',
                'count': 4,
                'price': 590.0,
            },
            {
                'title': 'Маленький принц',
                'author': 'Антуан де Сент-Экзюпери',
                'year': 1943,
                'isbn': '978-5-04-116634-6',
                'pages': 96,
                'genre': 'Сказка',
                'count': 7,
                'price': 450.0,
            },
            {
                'title': 'Три товарища',
                'author': 'Эрих Мария Ремарк',
                'year': 1936,
                'isbn': '978-5-17-137263-1',
                'pages': 384,
                'genre': 'Роман',
                'count': 2,
                'price': 690.0,
            },
            {
                'title': 'Портрет Дориана Грея',
                'author': 'Оскар Уайльд',
                'year': 1890,
                'isbn': '978-5-04-116635-3',
                'pages': 320,
                'genre': 'Роман',
                'count': 0,
                'price': 520.0,
            },
        ]

        with self.Session() as session:
            books = [Book(**data) for data in books_data]
            session.add_all(books)
            session.commit()

            ResultHandler.add_section('2.1. Добавление книг')
            results.append(f'Добавлено книг: {len(books_data)}')

    def insert_users(self) -> None:
        """Добавляет пользователей в базу данных."""
        users_data = [
            {'name': 'alice', 'fullname': 'Alice Wonderland'},
            {'name': 'bob', 'fullname': 'Bob Builder'},
            {'name': 'charlie', 'fullname': 'Charlie Brown'},
            {'name': 'diana', 'fullname': 'Diana Princess'},
            {'name': 'eve', 'fullname': 'Eve Smith'},
        ]

        with self.Session() as session:
            users = [User(**data) for data in users_data]
            session.add_all(users)
            session.commit()

            ResultHandler.add_section('2.2. Добавление пользователей')
            results.append(f'Добавлено пользователей: {len(users_data)}')

    def insert_delivery(self) -> None:
        """Добавляет данные доставки в базу данных."""
        delivery_data = [
            {
                'user_id': 1,
                'email': 'alice@example.com',
                'address': 'Wonderland 1, London',
                'phone': '+79997776655',
            },
            {
                'user_id': 2,
                'email': 'bob@example.com',
                'address': 'Builder St 123, London',
                'phone': '+44-20-7946-0002',
            },
            {'user_id': 3, 'email': None, 'address': None, 'phone': None},
            {
                'user_id': 4,
                'email': 'diana@example.com',
                'address': 'Princess Palace, London',
                'phone': None,
            },
            {
                'user_id': 5,
                'email': None,
                'address': 'Smith Lane 78, Dublin',
                'phone': '+353-1-234-5678',
            },
        ]

        with self.Session() as session:
            deliveries = [Delivery(**data) for data in delivery_data]
            session.add_all(deliveries)
            session.commit()

            ResultHandler.add_section('2.3. Добавление данных доставки')
            results.append(f'Добавлено данных доставки: {len(delivery_data)}')

    def insert_user_book_association(self) -> None:
        """Добавляет ассоциации пользователей и книг."""
        association_data = [
            {'user_id': 1, 'book_id': 1},
            {'user_id': 2, 'book_id': 2},
            {'user_id': 3, 'book_id': 3},
            {'user_id': 4, 'book_id': 1},
            {'user_id': 1, 'book_id': 2},
            {'user_id': 3, 'book_id': 1},
            {'user_id': 3, 'book_id': 10},
        ]

        with self.Session() as session:
            associations = [
                UserBookAssociation(**data) for data in association_data
            ]
            session.add_all(associations)
            session.commit()

            ResultHandler.add_section(
                '2.4. Добавление данных ассоциации пользователя и книги'
            )
            results.append(f'Добавлено ассоциаций: {len(association_data)}')

    def get_top_books(self) -> None:
        """Получает топ-3 самые популярные книги."""
        with self.Session() as session:
            ResultHandler.add_section('3.1. Топ-3 самые популярные книги')
            stmt = (
                session
                .query(Book, func.count(UserBookAssociation.user_id))
                .join(UserBookAssociation)
                .group_by(Book.id)
                .order_by(func.count(UserBookAssociation.user_id).desc())
                .limit(3)
            )
            top_books = stmt.all()
            for book, count in top_books:
                results.append(f'{book} {count}')

    def get_user_purchases_report(self) -> None:
        """Выводит отчет о покупках пользователей."""
        with self.Session() as session:
            ResultHandler.add_section(
                '3.2. Информация о покупках пользователей'
            )
            users = session.query(User).all()
            for user in users:
                if len(user.books) > 0:
                    results.append('')
                    results.append(f'{user.fullname} ({user.name}):')
                    results.append('    Купленные книги:')
                    total = 0
                    for assoc in user.books:
                        book = assoc.book
                        results.append(
                            f'        {book.title} - {book.author} '
                            f'({book.genre}); {book.price} руб.'
                        )
                        total += book.price
                    results.append(f'    Итого: {total:.2f} руб.')

    def get_users_with_missing_delivery_data(self) -> None:
        """Получает пользователей с отсутствующими данными доставки."""
        with self.Session() as session:
            ResultHandler.add_section(
                '3.3. Пользователи с отсутствующими данными доставки'
            )
            stmt = (
                session
                .query(User)
                .join(Delivery)
                .where(
                    or_(
                        Delivery.email.is_(None),
                        Delivery.address.is_(None),
                        Delivery.phone.is_(None),
                    )
                )
            )
            users = stmt.all()
            for user in users:
                results.append(str(user))

    def increase_prices_by_percent(self) -> None:
        """Увеличивает цены на 5%."""
        with self.Session() as session:
            ResultHandler.add_section('3.4. Увеличение цены на 5%')
            old_books = session.query(Book).all()
            old_prices = {book.id: book.price for book in old_books}

            stmt = (
                update(Book)
                .values(price=Book.price * 1.05)
                .returning(Book.id, Book.title, Book.price)
            )
            updated = session.execute(stmt).all()
            session.commit()

            for book_id, title, new_price in updated:
                old_price = old_prices[book_id]
                diff = new_price - old_price
                results.append(
                    f'{title}: {old_price:.2f} -> {new_price:.2f} '
                    f'({diff:.2f}) руб.'
                )

    def generate_store_report(self) -> None:
        """Генерирует отчет по магазину."""
        with self.Session() as session:
            ResultHandler.add_section('3.5. Отчет по магазину')

            results.append('')
            results.append('1. Книги:')
            books = session.query(Book).order_by(Book.title).all()
            for book in books:
                total_value = book.count * book.price
                if book.count > 0:
                    results.append(
                        f'   - "{book.title}": {book.count} шт. x '
                        f'{book.price} руб. = {total_value:.2f} руб.'
                    )
                else:
                    results.append(
                        f'   - "{book.title}": {book.count} шт. x '
                        f'{book.price} руб. = {total_value:.2f} руб. '
                        f'(нет в наличии)'
                    )

            results.append('')
            results.append('2. Активные читатели:')
            users = session.query(User).all()
            for user in users:
                if len(user.books) > 0:
                    book_titles = ', '.join([
                        assoc.book.title for assoc in user.books
                    ])
                    results.append(
                        f'   - {user.name}: {len(user.books)} '
                        f'книга(и) ({book_titles})'
                    )

            results.append('')
            results.append('3. Самый популярный автор:')
            stmt = (
                session
                .query(
                    Book.author,
                    func.count(distinct(UserBookAssociation.user_id)),
                )
                .join(UserBookAssociation)
                .group_by(Book.author)
                .order_by(
                    func.count(distinct(UserBookAssociation.user_id)).desc()
                )
                .limit(1)
            )
            top_author = stmt.first()
            if top_author:
                author, count = top_author
                results.append(f'   - {author} - {count} читателя')

    def delete_users_without_address(self) -> None:
        """Удаляет пользователей без адреса."""
        with self.Session() as session:
            ResultHandler.add_section('3.6. Удаление пользователей без адреса')
            stmt = (
                session
                .query(User)
                .join(Delivery)
                .where(Delivery.address.is_(None))
            )
            users_to_delete = stmt.all()

            results.append('Удалены пользователи: ')
            for user in users_to_delete:
                results.append(f'ID: {user.id}, Name: {user.name}')
                session.delete(user)
            session.commit()

            results.append('')
            results.append('Оставшиеся записи в таблице delivery:')
            deliveries = session.query(Delivery).all()
            for delivery in deliveries:
                results.append(f'  {delivery}')

            results.append('')
            results.append(
                'Оставшиеся записи в таблице user_book_association:'
            )
            associations = session.query(UserBookAssociation).all()
            for assoc in associations:
                results.append(f'  {assoc}')

    def delete_book_by_isbn(self, isbn: str = '978-5-17-135043-1') -> None:
        """Удаляет книгу по ISBN.

        Args:
            isbn (str): ISBN книги для удаления
        """
        with self.Session() as session:
            ResultHandler.add_section('3.7. Удаление книги по ISBN')
            book_to_delete = (
                session.query(Book).filter(Book.isbn == isbn).first()
            )

            if book_to_delete:
                users_with_book = [
                    assoc.user for assoc in book_to_delete.users
                ]

                results.append('')
                results.append('Пользователи, у которых была эта книга:')
                for user in users_with_book:
                    results.append(f'  - {user.fullname} ({user.name})')

                session.delete(book_to_delete)
                session.commit()

            results.append('')
            results.append(
                'Оставшиеся записи в таблице user_book_association:'
            )
            associations = session.query(UserBookAssociation).all()
            for assoc in associations:
                user_name = assoc.user.name
                book_title = assoc.book.title
                results.append(
                    f'  UserBookAssociation(user_id={assoc.user_id} '
                    f'({user_name}), book_id={assoc.book_id} ({book_title}))'
                )

    def run_all(self) -> None:
        """Запускает все операции."""
        self.create_tables()

        self.insert_books()
        self.insert_users()
        self.insert_delivery()
        self.insert_user_book_association()

        self.get_top_books()
        self.get_user_purchases_report()
        self.get_users_with_missing_delivery_data()
        self.increase_prices_by_percent()
        self.generate_store_report()
        self.delete_users_without_address()
        self.delete_book_by_isbn()

        print(*results, sep='\n')

        ResultHandler.save_results_to_file('hw5/my_result.txt')

        ResultHandler.compare_results('hw5/my_result.txt', 'hw5/result.txt')


def main() -> None:
    """Основная функция программы."""
    bookstore = BookStore()
    bookstore.run_all()


if __name__ == '__main__':
    main()
