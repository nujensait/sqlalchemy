"""Репозиторий для работы с курсами."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from project.infrastructure.database import Course, Enrollment
from project.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """Репозиторий для работы с курсами."""

    def __init__(self, session: Session) -> None:
        """Инициализирует репозиторий курсов.

        Args:
            session: Сессия базы данных
        """
        super().__init__(Course, session)

    def get_by_title(self, title: str) -> Course | None:
        """Получает курс по названию.

        Args:
            title: Название курса

        Returns:
            Объект курса или None
        """
        stmt = select(Course).where(Course.title == title)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_with_teacher(self, course_id: int) -> Course | None:
        """Получает курс с загруженным преподавателем.

        Args:
            course_id: ID курса

        Returns:
            Объект курса с teacher или None
        """
        stmt = (
            select(Course)
            .where(Course.id == course_id)
            .options(joinedload(Course.teacher))
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_top_popular_courses(self, limit: int = 3) -> list[tuple]:
        """Получает топ самых популярных курсов по количеству студентов.

        Args:
            limit: Количество курсов в топе

        Returns:
            Список кортежей (course, student_count)
        """
        stmt = (
            select(Course, func.count(Enrollment.student_id).label('cnt'))
            .join(Enrollment)
            .group_by(Course.id)
            .order_by(func.count(Enrollment.student_id).desc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).all())

    def get_courses_by_price_range(
        self, min_price: float, max_price: float
    ) -> list[Course]:
        """Получает курсы в заданном диапазоне цен.

        Args:
            min_price: Минимальная цена
            max_price: Максимальная цена

        Returns:
            Список курсов
        """
        stmt = (
            select(Course)
            .where(Course.price >= min_price, Course.price <= max_price)
            .order_by(Course.price)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_all_ordered_by_price(self) -> list[Course]:
        """Получает все курсы, отсортированные по цене.

        Returns:
            Список курсов, отсортированных по цене
        """
        stmt = select(Course).order_by(Course.price.desc())
        return list(self.session.execute(stmt).scalars().all())
