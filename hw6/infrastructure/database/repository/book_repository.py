from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from lesson_6.infrastructure.database.models.book import Book
from lesson_6.infrastructure.database.models.user_book_association import (
    UserBookAssociation,
)
from lesson_6.infrastructure.database.repository.base_repository import (
    BaseRepository,
)


class BookRepository(BaseRepository[Book]):
    """Репозиторий для работы с книгами"""

    def __init__(self, session: Session):
        super().__init__(session, Book)

    def find_by_author(self, author: str):
        """Найти книги по автору"""
        return (
            self.session
            .execute(select(Book).where(Book.author == author))
            .scalars()
            .all()
        )

    def find_by_author_like(self, pattern: str):
        """Найти книги по части имени автора"""
        return (
            self.session
            .execute(select(Book).where(Book.author.like(f'%{pattern}%')))
            .scalars()
            .all()
        )

    def find_by_title(self, title: str) -> Book | None:
        """Найти книгу по названию"""
        return self.session.execute(
            select(Book).where(Book.title == title)
        ).scalar_one_or_none()

    def get_with_users(self, book_id: int) -> Book | None:
        """Получить книгу с читателями"""
        return self.session.execute(
            select(Book)
            .where(Book.id == book_id)
            .options(
                selectinload(Book.user_associations).selectinload(
                    UserBookAssociation.user
                )
            )
        ).scalar_one_or_none()

    def get_all_with_stats(self):
        """Получить все книги с количеством читателей"""
        return self.session.execute(
            select(
                Book.id,
                Book.title,
                Book.author,
                func.count(UserBookAssociation.user_id).label('readers_count'),
            )
            .outerjoin(Book.user_associations)
            .group_by(Book.id, Book.title, Book.author)
            .order_by(func.count(UserBookAssociation.user_id).desc())
        ).all()
