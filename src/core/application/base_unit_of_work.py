from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self


class BaseUnitOfWork(ABC):

    @abstractmethod
    async def __aenter__(self) -> Self: ...
    
    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> bool | None:
        ...
    
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
    