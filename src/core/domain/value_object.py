from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ValueObject:
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ValueObject):
            return False
        return asdict(value) == asdict(self)
