import uuid
from itertools import count

from src.kernel.domain.domain_exception import DomainException


class DomainEntity:
    """Base DomainEntity to be used in the application"""

    # A generator to generate an instance id for each domain object.
    _instance_id_generator = count(0)

    def __init__(self, id: uuid.UUID, version: int) -> None:
        self._id: uuid.UUID = id
        self._version: int = version
        self._discarded: bool = False
        self._instance_id: int = next(self._instance_id_generator)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, DomainEntity):
            return False
        return value.id == self._id
    
    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} id={self._id} version={self._version} "
            f"discarded={self._discarded} instance_id={self._instance_id}>"
        )
    
    def increment_version(self) -> None:
        self._version += 1

    def discard(self) -> None:
        self._discarded = True

    def _check_not_discarded(self) -> None:
        if self._discarded:
            raise DomainException(f"Attempt to use {self!r}")

    @property
    def version(self) -> int:
        self._check_not_discarded()
        return self._version
    
    @property
    def id(self) -> uuid.UUID:
        return self._id
    
    @property
    def discarded(self) -> bool:
        return self._discarded

    @property
    def instance_id(self) -> int:
        return self._instance_id