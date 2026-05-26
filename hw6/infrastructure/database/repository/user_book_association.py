from lesson_6.infrastructure.database.models.user_book_association import (
    UserBookAssociation,
)
from lesson_6.infrastructure.database.repository.base_repository import (
    BaseRepository,
)
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload


class UserBookAssociationRepository(BaseRepository[UserBookAssociation]):
    """Репозиторий для работы со связями пользователь-книга"""

    def __init__(self, session: Session):
        super().__init__(session, UserBookAssociation)

    def find_by_user(self, user_id: int):
        """Найти все связи пользователя"""
        return (
            self.session
            .execute(
                select(UserBookAssociation)
                .where(UserBookAssociation.user_id == user_id)
                .options(selectinload(UserBookAssociation.book))
            )
            .scalars()
            .all()
        )

    def find_by_book(self, book_id: int):
        """Найти все связи книги"""
        return (
            self.session
            .execute(
                select(UserBookAssociation)
                .where(UserBookAssociation.book_id == book_id)
                .options(selectinload(UserBookAssociation.user))
            )
            .scalars()
            .all()
        )

    def get_or_create(self, user_id: int, book_id: int) -> UserBookAssociation:
        """Получить существующую связь или создать новую"""
        existing = self.session.execute(
            select(UserBookAssociation).where(
                UserBookAssociation.user_id == user_id,
                UserBookAssociation.book_id == book_id,
            )
        ).scalar_one_or_none()

        if existing:
            return existing

        association = UserBookAssociation(user_id=user_id, book_id=book_id)
        self.session.add(association)
        return association

    def delete_by_user_and_book(self, user_id: int, book_id: int) -> bool:
        """Удалить связь пользователя с книгой"""
        result = self.session.execute(
            delete(UserBookAssociation).where(
                UserBookAssociation.user_id == user_id,
                UserBookAssociation.book_id == book_id,
            )
        )
        return result.rowcount > 0
