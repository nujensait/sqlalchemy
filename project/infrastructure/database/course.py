"""Модель курса."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.infrastructure.database.base import Base

if TYPE_CHECKING:
    from project.infrastructure.database.enrollment import Enrollment
    from project.infrastructure.database.teacher import Teacher


class Course(Base):
    """Модель учебного курса.

    Attributes:
        id: Уникальный идентификатор курса
        title: Название курса
        description: Подробное описание курса
        credits: Количество кредитных часов
        max_seats: Максимальное количество студентов
        price: Стоимость курса в рублях
        teacher_id: ID преподавателя, ведущего курс
        teacher: Объект преподавателя
        enrollments: Список записей студентов на курс
    """

    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    credits: Mapped[int] = mapped_column(default=3)
    max_seats: Mapped[int] = mapped_column(default=30)
    price: Mapped[float] = mapped_column(default=0.0)
    teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey('teachers.id', ondelete='SET NULL')
    )

    teacher: Mapped['Teacher | None'] = relationship(back_populates='courses')
    enrollments: Mapped[list['Enrollment']] = relationship(
        back_populates='course', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление курса.

        Returns:
            Строка с информацией о курсе
        """
        return (
            f"Course(id={self.id}, title='{self.title}', "
            f'credits={self.credits}, price={self.price})'
        )
