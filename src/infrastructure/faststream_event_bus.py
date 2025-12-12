from dataclasses import asdict
from typing import cast

from faststream import FastStream
from faststream._internal.broker import BrokerUsecase

from src.kernel.application.event_bus import EventBus
from src.kernel.application.exceptions.event_bus_exceptions import (
    EventBusAlreadyClosedError,
    EventBusAlreadyStartedError,
    EventBusNotStartedError,
)
from src.kernel.domain.domain_event import DomainEvent


class FastStreamEventBus(EventBus):
    def __init__(self, app: FastStream) -> None:
        self._app = app
        self._broker = cast(BrokerUsecase[object, object], self._app.broker)
        self._is_started = False

    async def start(self):
        if self._is_started:
            raise EventBusAlreadyStartedError(
                "Attempt to call .start method second time without closing."
            )
        self._is_started = True

        await self._app.start()

    async def close(self):
        if not self._is_started:
            raise EventBusAlreadyClosedError(
                "Attempt to call .close method second time without starting."
            )
        self._is_started = False

        await self._app.stop()

    async def publish(self, event: DomainEvent) -> None:
        if not self._is_started:
            raise EventBusNotStartedError(
                "Attempt to use event bus before starting it."
            )
        
        # TODO: improve an error here
        await self._broker.publish(
            message=asdict(event),  # type: ignore
            queue=event.event_name
        )

