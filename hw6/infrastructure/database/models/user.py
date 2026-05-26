from lesson_6.infrastructure.database.base import Base
from lesson_6.infrastructure.database.models.address import Address
from lesson_6.infrastructure.database.models.profile import Profile
from lesson_6.infrastructure.database.models.user_book_association import (
    UserBookAssociation,
)
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'user_account'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    # один пользователь -> много адресов
    addresses: Mapped[list['Address']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    # один пользователь -> одна запись
    profile: Mapped[Profile | None] = relationship(
        back_populates='user',
        uselist=False,  # гарантирует, что будет один объект, а не список
        cascade='all, delete-orphan',
    )
    book_associations: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return (
            f'User(id={self.id!r}, '
            f'name={self.name!r}, '
            f'fullname={self.fullname!r})'
        )

    __table_args__ = (Index('idx_user_name', 'name'),)
