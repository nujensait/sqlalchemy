"""Репозиторий для работы с записями на курсы."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from project.infrastructure.database import Course, Enrollment
from project.repositories.base_repository import BaseRepository


class EnrollmentRepository(BaseRepository[Enrollment]):
    """Репозиторий для работы с записями на курсы."""

    def __init__(self, session: Session) -> None:
        """Инициализирует репозиторий записей.

        Args:
            session: Сессия базы данных
        """
        super().__init__(Enrollment, session)

    def get_by_student_and_course(
        self, student_id: int, course_id: int
    ) -> Enrollment | None:
        """Получает запись по ID студента и курса.

        Args:
            student_id: ID студента
            course_id: ID курса

        Returns:
            Объект записи или None
        """
        return self.session.get(Enrollment, (student_id, course_id))

    def get_student_enrollments(self, student_id: int) -> list[Enrollment]:
        """Получает все записи студента на курсы.

        Args:
            student_id: ID студента

        Returns:
            Список записей студента
        """
        stmt = (
            select(Enrollment)
            .where(Enrollment.student_id == student_id)
            .options(joinedload(Enrollment.course))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_course_enrollments(self, course_id: int) -> list[Enrollment]:
        """Получает все записи на курс.

        Args:
            course_id: ID курса

        Returns:
            Список записей на курс
        """
        stmt = (
            select(Enrollment)
            .where(Enrollment.course_id == course_id)
            .options(joinedload(Enrollment.student))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_incomplete_enrollments(self) -> list[Enrollment]:
        """Получает все незавершённые записи.

        Returns:
            Список незавершённых записей
        """
        stmt = (
            select(Enrollment)
            .where(Enrollment.is_completed == False)  # noqa: E712
            .options(
                joinedload(Enrollment.student), joinedload(Enrollment.course)
            )
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_average_grade_by_course(self) -> list[tuple]:
        """Получает среднюю оценку по каждому курсу.

        Returns:
            Список кортежей (course, avg_grade)
        """
        stmt = (
            select(Course, func.avg(Enrollment.grade).label('avg_grade'))
            .join(Enrollment)
            .where(Enrollment.grade.is_not(None))
            .group_by(Course.id)
            .order_by(func.avg(Enrollment.grade).desc())
        )
        return list(self.session.execute(stmt).all())

    def get_students_count_by_course(self) -> list[tuple]:
        """Получает количество студентов на каждом курсе.

        Returns:
            Список кортежей (course, student_count)
        """
        stmt = (
            select(Course, func.count(Enrollment.student_id).label('cnt'))
            .join(Enrollment)
            .group_by(Course.id)
            .order_by(func.count(Enrollment.student_id).desc())
        )
        return list(self.session.execute(stmt).all())
