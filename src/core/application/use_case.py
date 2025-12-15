from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.kernel.application.data_transfer_object import DataTransferObject

InDTO = TypeVar("InDTO", bound=DataTransferObject)
OutDTO = TypeVar("OutDTO", bound=DataTransferObject)


class UseCase(Generic[InDTO, OutDTO], ABC):  # noqa
    
    """
    A base UseCase class. Other *UseCase classes in Application layer should be 
    inhered from this class.
    """

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__}>"
        )
    
    @abstractmethod
    async def execute(self, data: InDTO) -> OutDTO:
        pass
    