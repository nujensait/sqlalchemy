import asyncio
from typing import List

from sqlalchemy import ForeignKey, String, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)

# Конфигурация
DATABASE_URL = (
    'postgresql+asyncpg://superuser:superpassword@localhost:5432/postgres'
)

# Асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# Модели
class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    bio: Mapped[str | None] = mapped_column(String(500))

    books: Mapped[list['Book']] = relationship(back_populates='author')


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    author: Mapped['Author'] = relationship(back_populates='books')


class AsyncBookStore:
    """Асинхронный менеджер книжного магазина"""

    async def init_db(self):
        """Инициализация базы данных"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        print('✅ База данных инициализирована')

    async def add_author(self, name: str, bio: str = None) -> Author:
        """Добавление автора"""
        async with AsyncSessionLocal() as session:
            author = Author(name=name, bio=bio)
            session.add(author)
            await session.commit()
            await session.refresh(author)
            print(f'✅ Добавлен автор: {author.name} (ID: {author.id})')
            return author

    async def add_book(
        self, title: str, price: float, author_id: int, stock: int = 0
    ) -> Book:
        """Добавление книги"""
        async with AsyncSessionLocal() as session:
            # Проверяем существование автора
            author = await session.get(Author, author_id)
            if not author:
                raise ValueError(f'Автор с ID {author_id} не найден')

            book = Book(
                title=title, price=price, author_id=author_id, stock=stock
            )
            session.add(book)
            await session.commit()
            await session.refresh(book)
            print(f'✅ Добавлена книга: {book.title} (ID: {book.id})')
            return book

    async def get_books_by_author(self, author_name: str) -> List[Book]:
        """Получение книг автора с оптимизированной загрузкой"""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(Book)
                .join(Author)
                .where(Author.name == author_name)
                .options(selectinload(Book.author))
                .order_by(Book.price.desc())
            )

            result = await session.execute(stmt)
            books = result.scalars().all()
            return books

    async def get_author_stats(self) -> List[tuple]:
        """Статистика по авторам"""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(
                    Author.name,
                    func.count(Book.id).label('book_count'),
                    func.avg(Book.price).label('avg_price'),
                    func.sum(Book.stock).label('total_stock'),
                )
                .outerjoin(Book)
                .group_by(Author.id, Author.name)
                .order_by(func.count(Book.id).desc())
            )

            result = await session.execute(stmt)
            return result.all()

    async def search_books(self, query: str, limit: int = 10) -> List[Book]:
        """Поиск книг по названию или автору"""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(Book)
                .join(Author)
                .where(
                    (Book.title.ilike(f'%{query}%'))
                    | (Author.name.ilike(f'%{query}%'))
                )
                .limit(limit)
                .options(selectinload(Book.author))
            )

            result = await session.execute(stmt)
            return result.scalars().all()

    async def update_stock(self, book_id: int, new_stock: int) -> bool:
        """Обновление количества книг"""
        async with AsyncSessionLocal() as session:
            book = await session.get(Book, book_id)
            if not book:
                return False

            old_stock = book.stock
            book.stock = new_stock
            await session.commit()
            print(f"\n📚 '{book.title}': {old_stock} → {new_stock} шт.")
            return True

    async def delete_book(self, book_id: int) -> bool:
        """Удаление книги"""
        async with AsyncSessionLocal() as session:
            book = await session.get(Book, book_id)
            if not book:
                return False

            await session.delete(book)
            await session.commit()
            print(f'🗑️ Удалена книга: {book.title}')
            return True


async def main():
    """Главная функция"""
    store = AsyncBookStore()

    # 1. Инициализация
    await store.init_db()

    # 2. Добавление авторов
    authors = [
        ('Михаил Булгаков', 'Русский писатель, драматург'),
        ('Лев Толстой', 'Великий русский писатель'),
        ('Джордж Оруэлл', 'Британский писатель'),
    ]

    for name, bio in authors:
        await store.add_author(name, bio)

    # 3. Добавление книг
    books_data = [
        ('Мастер и Маргарита', 890.0, 1, 5),
        ('Собачье сердце', 590.0, 1, 3),
        ('Война и мир', 1200.0, 2, 2),
        ('Анна Каренина', 950.0, 2, 0),
        ('1984', 650.0, 3, 4),
    ]

    for title, price, author_id, stock in books_data:
        await store.add_book(title, price, author_id, stock)

    # 4. Поиск книг
    print("\n🔍 Поиск по запросу 'мир':")
    books = await store.search_books('мир')
    for book in books:
        print(f'  - {book.title} ({book.author.name}) - {book.price} руб.')

    # 5. Статистика по авторам
    print('\n📊 Статистика по авторам:')
    stats = await store.get_author_stats()
    for name, count, avg_price, total_stock in stats:
        print(
            f'  {name}: {count} книг, ср.цена {avg_price:.0f} руб., '
            f'всего {total_stock} шт.'
        )

    # 6. Обновление остатков
    await store.update_stock(4, 3)

    # 7. Параллельные запросы
    print('\n⚡ Параллельные запросы:')
    tasks = [
        store.get_books_by_author('Михаил Булгаков'),
        store.get_books_by_author('Лев Толстой'),
    ]
    results = await asyncio.gather(*tasks)

    for author_books in results:
        if author_books:
            author = author_books[0].author.name
            print(f'  {author}: {len(author_books)} книг')

    print('\n✅ Демонстрация завершена')


if __name__ == '__main__':
    asyncio.run(main())
