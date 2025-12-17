import logging
from collections.abc import Awaitable, Callable
from dataclasses import asdict, fields, is_dataclass
from typing import cast

from faststream import FastStream
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue
from faststream.types import SendableMessage
from pydantic import BaseModel, create_model

from src.core.application.event_bus import DomainEventT, EventBus
from src.core.application.exceptions.event_bus_exceptions import (
    EventBusAlreadyClosedError,
    EventBusAlreadyStartedError,
    EventBusNotStartedError,
)
from src.core.container import Container
from src.core.domain.domain_event import DomainEvent

logger = logging.getLogger(__name__)


class RabbitMQEventBus(EventBus):
    def __init__(self, container: Container, url: str = "amqp://guest:guest@localhost:567") -> None:
        self._broker = RabbitBroker(url)
        self._app = FastStream(self._broker)
        self._exchange = RabbitExchange(
            name="APP.EXCHANGE", declare=True, durable=True, type=ExchangeType.TOPIC
        )
        self._is_started = False
        self._container = container

    async def start(self):
        if self._is_started:
            raise EventBusAlreadyStartedError(
                "Attempt to call .start method second time without closing."
            )
        self._is_started = True

        await self._app.start()
        await self._broker.declare_exchange(self._exchange)

    async def stop(self):
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
        
        event_data = cast(SendableMessage, asdict(event))
        await self._broker.publish(
            message=event_data, 
            routing_key=event.event_name,
            exchange=self._exchange
        )

    def subscribe(
            self, 
            event: type[DomainEventT], 
            handler: Callable[[DomainEventT, Container], Awaitable[None]],
        ) -> None:

        EventModel = self._pydantic_model_from_dataclass(event)
        @self._broker.subscriber(
            queue=RabbitQueue(
                name=f"{handler.__module__}.{handler.__qualname__}.queue",
                routing_key=self._get_event_name(event),
                durable=True,  
            ),
            exchange=self._exchange
        )
        async def _(data: EventModel) -> None:  # type: ignore
            domain_event = event(**data.model_dump())  # type: ignore
            await handler(domain_event, self._container)

    @staticmethod
    def _pydantic_model_from_dataclass(event_type: type[DomainEvent]) -> type[BaseModel]:
        if not is_dataclass(event_type):
            raise TypeError(f"{event_type.__name__} is not a dataclass")

        fields: dict[str, type[object]] = {}
        for name, annotation in event_type.__annotations__.items():
            fields[name] = annotation

        return create_model(  # type: ignore
            event_type.__name__ + "Model", **fields  # type: ignore
        )
    
    @staticmethod
    def _get_event_name(event_type: type[DomainEvent]) -> str:
        if not is_dataclass(event_type):
            raise TypeError(f"{event_type.__name__} is not a dataclass")
        
        for f in fields(event_type):
            if f.name == "event_name":
                return cast(str, f.default)
        else:
            raise KeyError("DomainEvent must contain event_name with default value.")
        