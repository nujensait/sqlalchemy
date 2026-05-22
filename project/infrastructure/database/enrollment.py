"""Модель записи студента на курс."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.infrastructure.database.base import Base

if TYPE_CHECKING:
    from project.infrastructure.database.course import Course
    from project.infrastructure.database.student import Student


class Enrollment(Base):
    """Модель записи студента на курс (связь many-to-many).

    Attributes:
        student_id: ID студента
        course_id: ID курса
        enrolled_at: Дата и время записи на курс
        grade: Оценка за курс (0-100, None если не выставлена)
        is_completed: Флаг завершения курса
        student: Объект студента
        course: Объект курса
    """

    __tablename__ = 'enrollments'

    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id', ondelete='CASCADE'), primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True
    )
    enrolled_at: Mapped[datetime] = mapped_column(default=datetime.now)
    grade: Mapped[float | None] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(default=False)

    student: Mapped['Student'] = relationship(back_populates='enrollments')
    course: Mapped['Course'] = relationship(back_populates='enrollments')

    def __repr__(self) -> str:
        """Возвращает строковое представление записи.

        Returns:
            Строка с информацией о записи
        """
        return (
            f'Enrollment(student_id={self.student_id}, '
            f'course_id={self.course_id}, grade={self.grade}, '
            f'is_completed={self.is_completed})'
        )
