"""Модель преподавателя."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.infrastructure.database.base import Base

if TYPE_CHECKING:
    from project.infrastructure.database.course import Course


class Teacher(Base):
    """Модель преподавателя.

    Attributes:
        id: Уникальный идентификатор преподавателя
        full_name: Полное имя преподавателя
        department: Название кафедры
        hire_date: Дата найма на работу
        phone: Номер телефона
        courses: Список курсов, которые ведёт преподаватель
    """

    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String)
    department: Mapped[str] = mapped_column(String)
    hire_date: Mapped[date | None] = mapped_column()
    phone: Mapped[str | None] = mapped_column(String(15), unique=True)

    courses: Mapped[list['Course']] = relationship(back_populates='teacher')

    def __repr__(self) -> str:
        """Возвращает строковое представление преподавателя.

        Returns:
            Строка с информацией о преподавателе
        """
        return (
            f"Teacher(id={self.id}, full_name='{self.full_name}', "
            f"department='{self.department}')"
        )
