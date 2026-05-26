from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lesson_6.infrastructure.database.base import Base


class Address(Base):
    __tablename__ = 'address'
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(unique=True)
    user_id = mapped_column(ForeignKey('user_account.id'))
    # много адресов -> один пользователь
    user: Mapped['User'] = relationship(
        back_populates='addresses',
    )

    def __repr__(self) -> str:
        return f'Address(id={self.id!r}, email_address={self.email_address!r})'

    __table_args__ = (Index('idx_user_address', 'user_id', 'email_address'),)
