import uuid
from abc import ABC, abstractmethod
from typing import TypeVar

from src.kernel.domain.aggregate import Aggregate

T = TypeVar("T", bound=Aggregate)


class Repository[T: Aggregate](ABC):
    
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> T | None: 
        """Returns an AggregateRoot by ID if exists, otherwise returns None"""

    @abstractmethod
    async def edit(self, aggregate_root: T) -> None: 
        """Updates AggregateRoot"""

    @abstractmethod
    async def add(self, aggregate_root: T) -> None:
        """Creates new AggregateRoot in the storage"""

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None: 
        """Deletes an AggregateRoot by ID"""

    @abstractmethod
    async def exists(self, id: uuid.UUID) -> bool:
        """Checks if the AggregateRoot exists"""

    async def get(self, id: uuid.UUID) -> T | None:
        """Executes self.get_by_id inside"""
        return await self.get_by_id(id)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
    