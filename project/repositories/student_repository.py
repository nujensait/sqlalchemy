"""Репозиторий для работы со студентами."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from project.infrastructure.database import Student
from project.repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository[Student]):
    """Репозиторий для работы со студентами."""

    def __init__(self, session: Session) -> None:
        """Инициализирует репозиторий студентов.

        Args:
            session: Сессия базы данных
        """
        super().__init__(Student, session)

    def get_active_students(self) -> list[Student]:
        """Получает всех активных студентов.

        Returns:
            Список активных студентов
        """
        stmt = select(Student).where(Student.is_active == True)  # noqa: E712
        return list(self.session.execute(stmt).scalars().all())

    def get_by_email(self, email: str) -> Student | None:
        """Получает студента по email.

        Args:
            email: Email студента

        Returns:
            Объект студента или None
        """
        stmt = select(Student).where(Student.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_with_enrollments(self, student_id: int) -> Student | None:
        """Получает студента с загруженными записями на курсы.

        Args:
            student_id: ID студента

        Returns:
            Объект студента с enrollments или None
        """
        stmt = (
            select(Student)
            .where(Student.id == student_id)
            .options(joinedload(Student.enrollments))
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_students_with_incomplete_courses(self) -> list[Student]:
        """Получает студентов с незавершёнными курсами.

        Returns:
            Список студентов с незавершёнными курсами
        """
        stmt = (
            select(Student)
            .join(Student.enrollments)
            .where(Student.enrollments.any(is_completed=False))
            .distinct()
        )
        return list(self.session.execute(stmt).scalars().all())
