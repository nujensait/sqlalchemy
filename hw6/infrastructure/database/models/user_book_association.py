from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lesson_6.infrastructure.database.base import Base


class UserBookAssociation(Base):
    __tablename__ = 'user_book_association'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_account.id'), primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('book.id'), primary_key=True
    )

    user: Mapped['User'] = relationship(back_populates='book_associations')
    book: Mapped['Book'] = relationship(back_populates='user_associations')
