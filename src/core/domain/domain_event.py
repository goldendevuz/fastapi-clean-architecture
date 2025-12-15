import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for domain events."""
    
    # Class-level constant — shared across all instances
    event_name: str = "undefined"
    
    # Auto-incrementing event ID (shared counter)
    event_id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    occured_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} "
            f"event_name={self.event_name} "
            f"event_id={self.event_id} "
            f"occured_at={self.occured_at.isoformat()}>"
        )