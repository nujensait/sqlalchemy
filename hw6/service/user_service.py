from lesson_6.infrastructure.database.models.user import User
from lesson_6.infrastructure.database.unit_of_work import UnitOfWork


class UserService:
    """Сервис для работы с пользователями (бизнес-логика)"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def create_user(self, name: str, fullname: str = None) -> User:
        """Создать нового пользователя"""
        # Проверка на существование
        existing = self.uow.users.find_by_name(name)
        if existing:
            raise ValueError(f'Пользователь с именем {name} уже существует')

        user = User(name=name, fullname=fullname)
        self.uow.users.add(user)
        self.uow.commit()
        return user

    def get_user_with_books(self, user_id: int) -> dict:
        """Получить пользователя с его книгами (для вывода)"""
        user = self.uow.users.get_with_books(user_id)
        if not user:
            raise ValueError(f'Пользователь {user_id} не найден')

        books = []
        for assoc in user.book_associations:
            books.append({
                'id': assoc.book.id,
                'title': assoc.book.title,
                'author': assoc.book.author,
            })

        return {
            'id': user.id,
            'name': user.name,
            'fullname': user.fullname,
            'books': books,
        }

    def get_all_users_with_books_efficient(self) -> list[dict]:
        """Получить всех пользователей с книгами (экономичная загрузка)"""
        users = self.uow.users.get_all_with_books_efficient()

        result = []
        for user in users:
            books = [assoc.book.title for assoc in user.book_associations]
            result.append({
                'name': user.name,
                'books': books,
                'books_count': len(books),
            })

        return result

    def add_book_to_user(self, user_id: int, book_id: int) -> None:
        """Добавить книгу пользователю"""
        user = self.uow.users.get(user_id)
        if not user:
            raise ValueError(f'Пользователь {user_id} не найден')

        book = self.uow.books.get(book_id)
        if not book:
            raise ValueError(f'Книга {book_id} не найдена')

        # Создаем связь
        association = self.uow.associations.get_or_create(user_id, book_id)
        self.uow.commit()

    def remove_book_from_user(self, user_id: int, book_id: int) -> None:
        """Удалить книгу у пользователя"""
        deleted = self.uow.associations.delete_by_user_and_book(
            user_id, book_id
        )
        if not deleted:
            raise ValueError(
                f'Книга {book_id} не найдена у пользователя {user_id}'
            )
        self.uow.commit()

    def get_top_books(self, limit: int = 3) -> list[tuple]:
        """Получить топ книг по популярности"""
        return self.uow.books.get_all_with_stats()[:limit]
