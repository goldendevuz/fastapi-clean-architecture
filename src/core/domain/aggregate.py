from uuid import UUID

from src.kernel.domain.domain_entity import DomainEntity
from src.kernel.domain.domain_event import DomainEvent


class Aggregate(DomainEntity):

    def __init__(self, id: UUID, version: int) -> None:
        super().__init__(id, version)
        self._domain_events: list[DomainEvent] = []

    def record_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_events(self) -> tuple[DomainEvent, ...]:
        events = tuple(self._domain_events)
        self._clear_events()
        return events
    
    def _clear_events(self) -> None:
        self._domain_events = []