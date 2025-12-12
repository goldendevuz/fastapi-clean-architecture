from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream import FastStream

from src.application.ports.clock import Clock
from src.application.unit_of_work import UnitOfWork
from src.framework.container import Container
from src.infrastructure.adapters.utc_clock import UTCClock
from src.infrastructure.faststream_event_bus import FastStreamEventBus
from src.infrastructure.sqlalchemy.setup import new_session
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.kernel.application.event_bus import EventBus
from src.infrastructure.faststream.setup import faststream_app, provider

from src.presentation import api
from src.presentation import consumers


class Loader:

    def __init__(self):
        self.container = Container()

    @asynccontextmanager
    async def lifespan(self, fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
        self.container.register_singleton(FastAPI, fastapi_app)
        await self.register_adapters()

        event_bus = await self.container.resolve(EventBus)

        await event_bus.start()
        yield
        await event_bus.close()

    async def register_adapters(self) -> None:
        fastapi_app = await self.container.resolve(FastAPI)
        fastapi_app.dependency_overrides[api.di.get_container] = self.get_container 

        provider[consumers.di.get_container] = self.get_container

        self.container.register_singleton(FastStream, faststream_app)
        self.container.register_singleton(
            EventBus, FastStreamEventBus(faststream_app)
        )
        self.container.register_singleton(Clock, UTCClock())
        self.container.register_sync_factory(UnitOfWork, lambda: SQLAlchemyUnitOfWork(new_session))

    async def get_container(self) -> Container:
        return self.container
    