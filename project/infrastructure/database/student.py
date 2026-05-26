"""Модель студента."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.infrastructure.database.base import Base

if TYPE_CHECKING:
    from project.infrastructure.database.enrollment import Enrollment


class Student(Base):
    """Модель студента онлайн-школы.

    Attributes:
        id: Уникальный идентификатор студента
        email: Адрес электронной почты (логин)
        full_name: Полное имя студента
        enrolled_at: Дата и время регистрации
        is_active: Статус активности (True - активен, False - заблокирован)
        enrollments: Список записей студента на курсы
    """

    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    full_name: Mapped[str] = mapped_column(String)
    enrolled_at: Mapped[datetime] = mapped_column(default=datetime.now)
    is_active: Mapped[bool] = mapped_column(default=True)

    enrollments: Mapped[list['Enrollment']] = relationship(
        back_populates='student', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление студента.

        Returns:
            Строка с информацией о студенте
        """
        return (
            f"Student(id={self.id}, email='{self.email}', "
            f"full_name='{self.full_name}', is_active={self.is_active})"
        )
