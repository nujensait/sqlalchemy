from lesson_6.infrastructure.database.repository.address_repository import (
    AddressRepository,
)
from lesson_6.infrastructure.database.repository.book_repository import (
    BookRepository,
)
from lesson_6.infrastructure.database.repository.profile_repository import (
    ProfileRepository,
)
from lesson_6.infrastructure.database.repository.user_book_association import (
    UserBookAssociationRepository,
)
from lesson_6.infrastructure.database.repository.user_repository import (
    UserRepository,
)
from sqlalchemy.orm import Session


class UnitOfWork:
    """Unit of Work — управляет транзакциями и предоставляет доступ к
    репозиториям
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session = None
        self._users = None
        self._books = None
        self._addresses = None
        self._profiles = None
        self._associations = None

    def __enter__(self):
        self._session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
        self._session.close()
        self._session = None

    @property
    def session(self) -> Session:
        """Получить текущую сессию (для низкоуровневых операций)"""
        if self._session is None:
            raise RuntimeError(
                'Unit of Work не активен. Используйте контекстный менеджер.'
            )
        return self._session

    @property
    def users(self) -> UserRepository:
        """Репозиторий пользователей"""
        if self._users is None:
            self._users = UserRepository(self.session)
        return self._users

    @property
    def books(self) -> BookRepository:
        """Репозиторий книг"""
        if self._books is None:
            self._books = BookRepository(self.session)
        return self._books

    @property
    def addresses(self) -> AddressRepository:
        """Репозиторий адресов"""
        if self._addresses is None:
            self._addresses = AddressRepository(self.session)
        return self._addresses

    @property
    def profiles(self) -> ProfileRepository:
        """Репозиторий профилей"""
        if self._profiles is None:
            self._profiles = ProfileRepository(self.session)
        return self._profiles

    @property
    def associations(self) -> UserBookAssociationRepository:
        """Репозиторий связей пользователь-книга"""
        if self._associations is None:
            self._associations = UserBookAssociationRepository(self.session)
        return self._associations

    def commit(self):
        """Фиксировать изменения"""
        self._session.commit()

    def rollback(self):
        """Откатить изменения"""
        self._session.rollback()
