"""Базовый репозиторий для работы с моделями."""

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from project.models import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Базовый репозиторий для CRUD операций.

    Args:
        model: Класс модели SQLAlchemy
        session: Сессия SQLAlchemy
    """

    def __init__(self, model: type[T], session: Session) -> None:
        """Инициализирует репозиторий.

        Args:
            model: Класс модели для работы
            session: Сессия базы данных
        """
        self.model = model
        self.session = session

    def add(self, entity: T) -> T:
        """Добавляет новую сущность в базу данных.

        Args:
            entity: Объект модели для добавления

        Returns:
            Добавленный объект
        """
        self.session.add(entity)
        self.session.flush()
        return entity

    def get_by_id(self, entity_id: int) -> T | None:
        """Получает сущность по ID.

        Args:
            entity_id: Идентификатор сущности

        Returns:
            Объект модели или None
        """
        return self.session.get(self.model, entity_id)

    def get_all(self) -> list[T]:
        """Получает все сущности.

        Returns:
            Список всех объектов модели
        """
        stmt = select(self.model)
        return list(self.session.execute(stmt).scalars().all())

    def update(self, entity: T) -> T:
        """Обновляет сущность.

        Args:
            entity: Объект модели для обновления

        Returns:
            Обновлённый объект
        """
        self.session.merge(entity)
        self.session.flush()
        return entity

    def delete(self, entity: T) -> None:
        """Удаляет сущность.

        Args:
            entity: Объект модели для удаления
        """
        self.session.delete(entity)
        self.session.flush()
