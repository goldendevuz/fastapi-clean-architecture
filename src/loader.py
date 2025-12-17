import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.ports.clock import Clock
from src.application.unit_of_work import UnitOfWork
from src.config import settings
from src.core.application.event_bus import EventBus
from src.core.container import Container
from src.infrastructure.adapters.utc_clock import UTCClock
from src.infrastructure.rabbitmq_event_bus import RabbitMQEventBus
from src.infrastructure.sqlalchemy.setup import new_session
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.presentation import api

logger = logging.getLogger(__name__)


class Loader:

    def __init__(self):
        self.container = Container()

    @asynccontextmanager
    async def lifespan(self, fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
        self.container.register_singleton(FastAPI, fastapi_app)
        fastapi_app.include_router(api.routers.router)
        await self.startup()
        yield
        await self.shutdown()

    async def startup(self):
        await self.setup_core_dependencies()
        await self.setup_framework_dependencies()
        await self.register_handlers()

        event_bus = await self.container.resolve(EventBus)
        await event_bus.start()

    async def shutdown(self):
        event_bus = await self.container.resolve(EventBus)
        await event_bus.stop()

    async def setup_core_dependencies(self) -> None:
        self.container.register_singleton(
            EventBus, RabbitMQEventBus(self.container, settings.AMQP_URL)
        )
        self.container.register_singleton(Clock, UTCClock())
        self.container.register_sync_factory(UnitOfWork, lambda: SQLAlchemyUnitOfWork(new_session))
    
    async def setup_framework_dependencies(self):
        fastapi_app = await self.container.resolve(FastAPI)
        fastapi_app.dependency_overrides[api.dependency_injection.get_container] = (
            self.get_container
        ) 
    
    async def get_container(self) -> Container:
        return self.container
    
    async def register_handlers(self):
        # event_bus = await self.container.resolve(EventBus)
        pass
    