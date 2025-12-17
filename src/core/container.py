from collections.abc import Awaitable, Callable
from typing import TypeVar, cast

from src.core.exceptions.container_exceptions import (
    InterfaceAlreadyRegisteredError,
    InterfaceNotRegisteredError,
)

T = TypeVar("T")


class Container:
    """
    This is a Container which allows implement Dependency Injection easily
    into application. It allows register `Interfaces` with the way,
    """

    def __init__(self) -> None:
        self._async_factories: dict[type[object], Callable[[], Awaitable[object]]] = {}
        self._sync_factories: dict[type[object], Callable[[], object]] = {}
        self._singletons: dict[type[object], object] = {}

    def register_sync_factory(self, interface: type[T], factory: Callable[[], T]) -> None:
        self._check_not_registered(interface)
        self._sync_factories[interface] = factory

    def register_async_factory(
            self, 
            interface: type[T], 
            factory: Callable[[], Awaitable[T]]
        ) -> None:
        self._check_not_registered(interface)
        self._async_factories[interface] = factory

    def register_singleton(self, interface: type[T], singleton: T) -> None:
        self._check_not_registered(interface)
        self._singletons[interface] = singleton

    async def resolve(self, interface: type[T]) -> T:
        if interface in self._async_factories:
            factory = cast(
                Callable[[], Awaitable[T]], 
                self._async_factories[interface]
            )
            return await factory()
        
        if interface in self._sync_factories:
            factory = cast(
                Callable[[], T], 
                self._sync_factories[interface]
            )
            return factory()
        
        if interface in self._singletons:
            return self._singletons[interface]
        
        
        raise InterfaceNotRegisteredError(
            f"Dependency resolution error: '{interface.__name__}' is not registered in this "
            f"container. Ensure it is added using `register_singleton()` or "
            f"`register_factory()` before resolving."
        )
    
    def _check_not_registered(self, interface: type[object]) -> None:
        error_template = (
            "Interface already has been register to the container as an {name}: {interfacename}"
        )

        if self._async_factories.get(interface):
            raise InterfaceAlreadyRegisteredError(
                error_template.format(name="Async Factory", interfacename=interface.__name__)
            )

        if self._sync_factories.get(interface):
            raise InterfaceAlreadyRegisteredError(
                error_template.format(name="sync Factory", interfacename=interface.__name__)
            )
        
        if self._singletons.get(interface):
            raise InterfaceAlreadyRegisteredError(
                error_template.format(name="Singleton", interfacename=interface.__name__)
            )
