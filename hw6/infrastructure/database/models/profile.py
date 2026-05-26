from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lesson_6.infrastructure.database.base import Base


class Profile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('user_account.id'), unique=True)
    bio: Mapped[str | None]
    phone: Mapped[str | None]

    # одна запись - один пользователь
    user: Mapped['User'] = relationship(back_populates='profile')
