from abc import ABC
from src.kernel.application.base_unit_of_work import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork, ABC):
    # Write your repositories there
    # e.g. 
    # users: UserRepository
    pass