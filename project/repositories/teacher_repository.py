"""Репозиторий для работы с преподавателями."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from project.infrastructure.database import Teacher
from project.repositories.base_repository import BaseRepository


class TeacherRepository(BaseRepository[Teacher]):
    """Репозиторий для работы с преподавателями."""

    def __init__(self, session: Session) -> None:
        """Инициализирует репозиторий преподавателей.

        Args:
            session: Сессия базы данных
        """
        super().__init__(Teacher, session)

    def get_by_department(self, department: str) -> list[Teacher]:
        """Получает преподавателей по кафедре.

        Args:
            department: Название кафедры

        Returns:
            Список преподавателей кафедры
        """
        stmt = select(Teacher).where(Teacher.department == department)
        return list(self.session.execute(stmt).scalars().all())

    def get_with_courses(self, teacher_id: int) -> Teacher | None:
        """Получает преподавателя с загруженными курсами.

        Args:
            teacher_id: ID преподавателя

        Returns:
            Объект преподавателя с courses или None
        """
        stmt = (
            select(Teacher)
            .where(Teacher.id == teacher_id)
            .options(joinedload(Teacher.courses))
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all_with_courses(self) -> list[Teacher]:
        """Получает всех преподавателей с их курсами.

        Returns:
            Список преподавателей с загруженными курсами
        """
        stmt = select(Teacher).options(joinedload(Teacher.courses))
        return list(self.session.execute(stmt).unique().scalars().all())
