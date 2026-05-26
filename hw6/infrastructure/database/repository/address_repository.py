from lesson_6.infrastructure.database.models.address import Address
from lesson_6.infrastructure.database.repository.base_repository import (
    BaseRepository,
)
from sqlalchemy import select
from sqlalchemy.orm import Session


class AddressRepository(BaseRepository[Address]):
    """Репозиторий для работы с адресами"""

    def __init__(self, session: Session):
        super().__init__(session, Address)

    def find_by_email(self, email: str) -> Address | None:
        """Найти адрес по email"""
        return self.session.execute(
            select(Address).where(Address.email_address == email)
        ).scalar_one_or_none()

    def find_by_user(self, user_id: int):
        """Найти все адреса пользователя"""
        return (
            self.session
            .execute(select(Address).where(Address.user_id == user_id))
            .scalars()
            .all()
        )

    def find_by_domain(self, domain: str):
        """Найти адреса по домену (например, 'gmail.com')"""
        return (
            self.session
            .execute(
                select(Address).where(
                    Address.email_address.like(f'%@{domain}')
                )
            )
            .scalars()
            .all()
        )
