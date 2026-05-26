from typing import TYPE_CHECKING

from lesson_6.infrastructure.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from lesson_6.infrastructure.database.models.user_book_association import (
        UserBookAssociation,
    )


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

    user_associations: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='book', cascade='all, delete-orphan'
    )

    @property
    def users(self):
        return [assoc.user for assoc in self.user_associations]
