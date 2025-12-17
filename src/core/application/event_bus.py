from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import TypeVar

from src.core.container import Container
from src.core.domain.domain_event import DomainEvent

DomainEventT = TypeVar("DomainEventT", bound=DomainEvent)


class EventBus(ABC):
    
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...

    @abstractmethod
    def subscribe(
            self, 
            event: type[DomainEventT], 
            handler: Callable[[DomainEventT, Container], Awaitable[None]]
        ) -> None: ...

    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def stop(self): ...
    
    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
    