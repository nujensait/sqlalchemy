from typing import Any, Sequence, _T_co

from sqlalchemy import func, select, Row
from sqlalchemy.orm import Session, joinedload, load_only, selectinload

from lesson_6.infrastructure.database.models.book import Book
from lesson_6.infrastructure.database.models.user import User
from lesson_6.infrastructure.database.models.user_book_association import (
    UserBookAssociation,
)
from lesson_6.infrastructure.database.repository.base_repository import (
    BaseRepository,
)


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями.

    Args:
        session: Сессия.
    """

    def __init__(self, session: Session):
        super().__init__(session, User)

    # ========== Базовые поиски ==========

    def find_by_name(self, name: str) -> User | None:
        """Найти пользователя по имени"""
        return self.session.execute(
            select(User).where(User.name == name)
        ).scalar_one_or_none()

    def find_by_name_like(self, pattern: str):
        """Найти пользователей по части имени"""
        return (
            self.session
            .execute(select(User).where(User.name.like(f'%{pattern}%')))
            .scalars()
            .all()
        )

    # ========== Загрузка со связанными данными ==========

    def get_with_addresses(self, user_id: int) -> User | None:
        """Получить пользователя с адресами"""
        return self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.addresses))
        ).scalar_one_or_none()

    def get_with_profile(self, user_id: int) -> User | None:
        """Получить пользователя с профилем"""
        return self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.profile))
        ).scalar_one_or_none()

    def get_with_books(self, user_id: int) -> User | None:
        """Получить пользователя с его книгами (через ассоциацию)"""
        return self.session.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.book_associations).selectinload(
                    UserBookAssociation.book
                )
            )
        ).scalar_one_or_none()

    def get_all_with_books(self):
        """Получить всех пользователей с их книгами"""
        return (
            self.session
            .execute(
                select(User).options(
                    selectinload(User.book_associations).selectinload(
                        UserBookAssociation.book
                    )
                )
            )
            .scalars()
            .all()
        )

    def get_all_with_books_efficient(self):
        """Получить всех пользователей с книгами (экономичная загрузка)"""
        return (
            self.session
            .execute(
                select(User).options(
                    load_only(User.id, User.name),
                    selectinload(User.book_associations).options(
                        selectinload(UserBookAssociation.book).options(
                            load_only(Book.id, Book.title)
                        )
                    ),
                )
            )
            .scalars()
            .all()
        )

    def get_users_with_books_count(self):
        """Получить пользователей с количеством книг (агрегация).

        Returns:
            Список имен пользователей с количеством книг.

        """
        return self.session.execute(
            select(
                User.id,
                User.name,
                func.count(UserBookAssociation.book_id).label('books_count'),
            )
            .outerjoin(User.book_associations)
            .group_by(User.id, User.name)
            .order_by(func.count(UserBookAssociation.book_id).desc())
        ).all()

    # ========== Поиск по связанным данным ==========

    def find_users_by_book_title(self, title: str) -> Sequence[_T_co]:
        """Найти пользователей, читающих книгу с указанным названием.

        Args:
            title: Название книги.

        Returns:
            Список пользователей, которые читают определенную книгу
        """
        return (
            self.session
            .execute(
                select(User)
                .join(User.book_associations)
                .join(UserBookAssociation.book)
                .where(Book.title.like(f'%{title}%'))
                .distinct()
            )
            .scalars()
            .all()
        )

    def find_users_by_author(self, author: str):
        """Найти пользователей, читающих книги указанного автора"""
        return (
            self.session
            .execute(
                select(User)
                .join(User.book_associations)
                .join(UserBookAssociation.book)
                .where(Book.author == author)
                .distinct()
            )
            .scalars()
            .all()
        )

    def find_active_readers(self):
        """Найти пользователей, у которых есть хотя бы одна книга"""
        return (
            self.session
            .execute(select(User).where(User.book_associations.any()))
            .scalars()
            .all()
        )
