from sqlalchemy.orm import Mapped, mapped_column, relationship

from lesson_6.infrastructure.database.base import Base


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
