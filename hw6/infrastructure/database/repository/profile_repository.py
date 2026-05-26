from sqlalchemy import select
from sqlalchemy.orm import Session

from lesson_6.infrastructure.database.models.profile import Profile
from lesson_6.infrastructure.database.repository.base_repository import (
    BaseRepository,
)


class ProfileRepository(BaseRepository[Profile]):
    """Репозиторий для работы с профилями"""

    def __init__(self, session: Session):
        super().__init__(session, Profile)

    def find_by_user(self, user_id: int) -> Profile | None:
        """Найти профиль пользователя"""
        return self.session.execute(
            select(Profile).where(Profile.user_id == user_id)
        ).scalar_one_or_none()

    def find_by_phone(self, phone: str) -> Profile | None:
        """Найти профиль по телефону"""
        return self.session.execute(
            select(Profile).where(Profile.phone == phone)
        ).scalar_one_or_none()
