# HW5: Работа с объектами в ORM

from pathlib import Path

from sqlalchemy import (
    ForeignKey,
    String,
    create_engine,
    func,
    or_,
    select,
    update,
)
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
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int | None] = mapped_column()
    isbn: Mapped[str | None] = mapped_column(String, unique=True)
    pages: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str | None] = mapped_column(String)
    count: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column(nullable=False, default=0)

    users: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='book', cascade='all, delete-orphan'
    )

    @property
    def is_available(self) -> bool:
        """Проверяет доступность книги.

        Returns:
            bool: True если count > 0, иначе False
        """
        return self.count > 0

    @property
    def list_users(self) -> list[str]:
        """Возвращает список пользователей книги.

        Returns:
            list[str]: Список строк вида 'id: fullname (name)'
        """
        return [
            f'{assoc.user.id}: {assoc.user.fullname} ({assoc.user.name})'
            for assoc in self.users
        ]

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
    name: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True
    )
    fullname: Mapped[str | None] = mapped_column(String(50))

    books: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    delivery_info: Mapped[list['Delivery']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    @property
    def is_books(self) -> bool:
        """Проверяет наличие книг у пользователя.

        Returns:
            bool: True если есть книги, иначе False
        """
        return len(self.books) > 0

    @property
    def list_books(self) -> list[str]:
        """Возвращает список книг пользователя.

        Returns:
            list[str]: Список строк вида 'id: title (author)'
        """
        return [
            f'{assoc.book.id}: {assoc.book.title} ({assoc.book.author})'
            for assoc in self.books
        ]

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
            f"Delivery(id={self.id}, user_id={self.user_id}, "
            f"email='{self.email}', address='{self.address}', "
            f"phone='{self.phone}')"
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
        min_len = min(len(lines1), len(lines2))
        for i in range(min_len):
            if lines1[i] != lines2[i]:
                print(f'Строка {i + 1}:')
                print(f'  Ожидается: {lines2[i]}')
                print(f'  Получено:  {lines1[i]}')
        if len(lines1) != len(lines2):
            print(
                f'Разная длина файлов: {len(lines1)} vs {len(lines2)}'
            )


def main() -> None:
    """Основная функция программы.

    Выполняет следующие действия:
    1. Создает базу данных bookstore.db
    2. Добавляет книги, пользователей, данные доставки и ассоциации
    3. Выполняет запросы
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
        {'name': 'alice', 'fullname': 'Alice Wonderland'},
        {'name': 'bob', 'fullname': 'Bob Builder'},
        {'name': 'charlie', 'fullname': 'Charlie Brown'},
        {'name': 'diana', 'fullname': 'Diana Princess'},
        {'name': 'eve', 'fullname': 'Eve Smith'},
    ]

    with Session(engine) as session:
        add_section('2.2. Добавление пользователей')
        users = [User(**data) for data in users_data]
        session.add_all(users)
        session.commit()
        print(f'Добавлено пользователей: {len(users)}')
        results.append('')
        results.append(
            '==========2.2. Добавление пользователей=========='
        )
        results.append(f'Добавлено пользователей: {len(users)}')

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

    with Session(engine) as session:
        add_section('2.3. Добавление данных доставки')
        deliveries = [Delivery(**data) for data in delivery_data]
        session.add_all(deliveries)
        session.commit()
        print(f'Добавлено данных доставки: {len(deliveries)}')
        results.append('')
        results.append(
            '==========2.3. Добавление данных доставки=========='
        )
        results.append(f'Добавлено данных доставки: {len(deliveries)}')

    association_data = [
        {'user_id': 1, 'book_id': 1},
        {'user_id': 2, 'book_id': 2},
        {'user_id': 3, 'book_id': 3},
        {'user_id': 4, 'book_id': 1},
        {'user_id': 1, 'book_id': 2},
        {'user_id': 3, 'book_id': 1},
        {'user_id': 3, 'book_id': 10},
    ]

    with Session(engine) as session:
        add_section(
            '2.4. Добавление данных ассоциации '
            'пользователя и книги'
        )
        associations = [
            UserBookAssociation(**data) for data in association_data
        ]
        session.add_all(associations)
        session.commit()
        print(f'Добавлено ассоциаций: {len(associations)}')
        results.append('')
        results.append(
            '==========2.4. Добавление данных ассоциации '
            'пользователя и книги=========='
        )
        results.append(f'Добавлено ассоциаций: {len(associations)}')

    with Session(engine) as session:
        add_section('3.1. Топ-3 самые популярные книги')
        stmt = (
            select(Book, func.count(UserBookAssociation.user_id))
            .join(UserBookAssociation)
            .group_by(Book.id)
            .order_by(func.count(UserBookAssociation.user_id).desc())
            .limit(3)
        )
        top_books = session.execute(stmt).all()
        results.append('')
        results.append(
            '==========3.1. Топ-3 самые популярные книги=========='
        )
        for book, count in top_books:
            print(f'{book} {count}')
            results.append(f'{book} {count}')

    with Session(engine) as session:
        add_section('3.2. Информация о покупках пользователей')
        users = session.query(User).all()
        results.append('')
        results.append(
            '==========3.2. Информация о покупках '
            'пользователей=========='
        )
        for user in users:
            if user.is_books:
                print()
                print(f'{user.fullname} ({user.name}):')
                print('    Купленные книги:')
                results.append('')
                results.append(f'{user.fullname} ({user.name}):')
                results.append('    Купленные книги:')
                total = 0
                for assoc in user.books:
                    book = assoc.book
                    print(
                        f'        {book.title} - {book.author} '
                        f'({book.genre}); {book.price} руб.'
                    )
                    results.append(
                        f'        {book.title} - {book.author} '
                        f'({book.genre}); {book.price} руб.'
                    )
                    total += book.price
                print(f'    Итого: {total:.2f} руб.')
                results.append(f'    Итого: {total:.2f} руб.')

    with Session(engine) as session:
        add_section(
            '3.3. Пользователи с отсутствующими данными доставки'
        )
        stmt = (
            select(User)
            .join(Delivery)
            .where(
                or_(
                    Delivery.email.is_(None),
                    Delivery.address.is_(None),
                    Delivery.phone.is_(None),
                )
            )
        )
        users = session.execute(stmt).scalars().all()
        results.append('')
        results.append(
            '==========3.3. Пользователи с отсутствующими '
            'данными доставки=========='
        )
        for user in users:
            print(user)
            results.append(str(user))

    with Session(engine) as session:
        add_section('3.4. Увеличение цены на 5%')
        stmt = select(Book)
        old_books = session.execute(stmt).scalars().all()
        old_prices = {book.id: book.price for book in old_books}

        stmt = (
            update(Book)
            .values(price=Book.price * 1.05)
            .returning(Book.id, Book.title, Book.price)
        )
        updated = session.execute(stmt).all()
        session.commit()

        results.append('')
        results.append('==========3.4. Увеличение цены на 5%==========')
        for book_id, title, new_price in updated:
            old_price = old_prices[book_id]
            diff = new_price - old_price
            print(
                f'{title}: {old_price:.2f} -> {new_price:.2f} '
                f'({diff:.2f}) руб.'
            )
            results.append(
                f'{title}: {old_price:.2f} -> {new_price:.2f} '
                f'({diff:.2f}) руб.'
            )

    with Session(engine) as session:
        add_section('3.5. Отчет по магазину')
        books = session.query(Book).order_by(Book.title).all()
        results.append('')
        results.append('==========3.5. Отчет по магазину==========')
        print()
        print('1. Книги:')
        results.append('')
        results.append('1. Книги:')
        for book in books:
            total_value = book.count * book.price
            if book.count > 0:
                print(
                    f'   - "{book.title}": {book.count} шт. x '
                    f'{book.price} руб. = {total_value:.2f} руб.'
                )
                results.append(
                    f'   - "{book.title}": {book.count} шт. x '
                    f'{book.price} руб. = {total_value:.2f} руб.'
                )
            else:
                print(
                    f'   - "{book.title}": {book.count} шт. x '
                    f'{book.price} руб. = {total_value:.2f} руб. '
                    f'(нет в наличии)'
                )
                results.append(
                    f'   - "{book.title}": {book.count} шт. x '
                    f'{book.price} руб. = {total_value:.2f} руб. '
                    f'(нет в наличии)'
                )

        print()
        print('2. Активные читатели:')
        results.append('')
        results.append('2. Активные читатели:')
        users = session.query(User).all()
        for user in users:
            if user.is_books:
                book_titles = ', '.join(
                    [assoc.book.title for assoc in user.books]
                )
                print(
                    f'   - {user.name}: {len(user.books)} '
                    f'книга(и) ({book_titles})'
                )
                results.append(
                    f'   - {user.name}: {len(user.books)} '
                    f'книга(и) ({book_titles})'
                )

        print()
        print('3. Самый популярный автор:')
        results.append('')
        results.append('3. Самый популярный автор:')
        stmt = (
            select(Book.author, func.count(UserBookAssociation.user_id))
            .join(UserBookAssociation)
            .group_by(Book.author)
            .order_by(func.count(UserBookAssociation.user_id).desc())
            .limit(1)
        )
        top_author = session.execute(stmt).first()
        if top_author:
            author, count = top_author
            print(f'   - {author} - {count} читателя')
            results.append(f'   - {author} - {count} читателя')

    with Session(engine) as session:
        add_section('3.6. Удаление пользователей без адреса')
        stmt = (
            select(User)
            .join(Delivery)
            .where(Delivery.address.is_(None))
        )
        users_to_delete = session.execute(stmt).scalars().all()

        results.append('')
        results.append(
            '==========3.6. Удаление пользователей без адреса=========='
        )
        print('Удалены пользователи: ')
        results.append('Удалены пользователи: ')
        for user in users_to_delete:
            print(f'ID: {user.id}, Name: {user.name}')
            results.append(f'ID: {user.id}, Name: {user.name}')
            session.delete(user)
        session.commit()

        print()
        print('Оставшиеся записи в таблице delivery:')
        results.append('')
        results.append('Оставшиеся записи в таблице delivery:')
        deliveries = session.query(Delivery).all()
        for delivery in deliveries:
            print(f'  {delivery}')
            results.append(f'  {delivery}')

        print()
        print('Оставшиеся записи в таблице user_book_association:')
        results.append('')
        results.append(
            'Оставшиеся записи в таблице user_book_association:'
        )
        associations = session.query(UserBookAssociation).all()
        for assoc in associations:
            print(f'  {assoc}')
            results.append(f'  {assoc}')

    with Session(engine) as session:
        add_section('3.7. Удаление книги по ISBN')
        isbn_to_delete = '978-5-17-135043-1'
        book_to_delete = (
            session.query(Book).filter(Book.isbn == isbn_to_delete).first()
        )

        results.append('')
        results.append('==========3.7. Удаление книги по ISBN==========')

        if book_to_delete:
            users_with_book = [
                assoc.user for assoc in book_to_delete.users
            ]

            print()
            print('Пользователи, у которых была эта книга:')
            results.append('')
            results.append('Пользователи, у которых была эта книга:')
            for user in users_with_book:
                print(f'  - {user.fullname} ({user.name})')
                results.append(f'  - {user.fullname} ({user.name})')

            session.delete(book_to_delete)
            session.commit()

        print()
        print('Оставшиеся записи в таблице user_book_association:')
        results.append('')
        results.append(
            'Оставшиеся записи в таблице user_book_association:'
        )
        associations = session.query(UserBookAssociation).all()
        for assoc in associations:
            user_name = assoc.user.name
            book_title = assoc.book.title
            print(
                f'  UserBookAssociation(user_id={assoc.user_id} '
                f'({user_name}), book_id={assoc.book_id} ({book_title}))'
            )
            results.append(
                f'  UserBookAssociation(user_id={assoc.user_id} '
                f'({user_name}), book_id={assoc.book_id} ({book_title}))'
            )

    save_results_to_file(results, 'hw5/my_result.txt')
    compare_results('hw5/my_result.txt', 'hw5/result.txt')


if __name__ == '__main__':
    main()
