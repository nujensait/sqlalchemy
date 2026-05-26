"""Unit of Work для управления транзакциями."""

from typing import Callable

from sqlalchemy.orm import Session

from project.repositories import (
    CourseRepository,
    EnrollmentRepository,
    StudentRepository,
    TeacherRepository,
)


class UnitOfWork:
    """Unit of Work для управления транзакциями и репозиториями.

    Attributes:
        students: Репозиторий студентов
        teachers: Репозиторий преподавателей
        courses: Репозиторий курсов
        enrollments: Репозиторий записей на курсы
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        """Инициализирует Unit of Work.

        Args:
            session_factory: Фабрика для создания сессий
        """
        self.session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> 'UnitOfWork':
        """Входит в контекст, создаёт сессию и репозитории.

        Returns:
            Экземпляр UnitOfWork
        """
        self._session = self.session_factory()
        self.students = StudentRepository(self._session)
        self.teachers = TeacherRepository(self._session)
        self.courses = CourseRepository(self._session)
        self.enrollments = EnrollmentRepository(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Выходит из контекста, закрывает сессию.

        Args:
            exc_type: Тип исключения
            exc_val: Значение исключения
            exc_tb: Traceback исключения
        """
        if exc_type is not None:
            self.rollback()
        if self._session:
            self._session.close()

    def commit(self) -> None:
        """Фиксирует транзакцию."""
        if self._session:
            self._session.commit()

    def rollback(self) -> None:
        """Откатывает транзакцию."""
        if self._session:
            self._session.rollback()

    def flush(self) -> None:
        """Выполняет flush для сессии."""
        if self._session:
            self._session.flush()
