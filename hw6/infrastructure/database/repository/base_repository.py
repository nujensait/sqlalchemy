from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Базовый репозиторий с общими CRUD операциями"""

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get(self, id: int) -> Optional[T]:
        """Получить запись по ID"""
        return self.session.get(self.model, id)

    def get_all(self) -> List[T]:
        """Получить все записи"""
        return self.session.execute(select(self.model)).scalars().all()  # noqa

    def add(self, entity: T) -> T:
        """Добавить запись"""
        self.session.add(entity)
        return entity

    def add_all(self, entities: List[T]) -> List[T]:
        """Добавить несколько записей"""
        self.session.add_all(entities)
        return entities

    def delete(self, entity: T) -> None:
        """Удалить запись"""
        self.session.delete(entity)

    def delete_by_id(self, id: int) -> bool:
        """Удалить запись по ID"""
        entity = self.get(id)
        if entity:
            self.session.delete(entity)
            return True
        return False

    def count(self) -> int:
        """Количество записей"""
        return self.session.execute(
            select(func.count()).select_from(self.model)
        ).scalar_one()
