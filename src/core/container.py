from collections.abc import Awaitable, Callable
from typing import TypeVar, cast

T = TypeVar("T")


class Container:

    def __init__(self) -> None:
        self._async_factories: dict[type[object], Callable[[], Awaitable[object]]] = {}
        self._sync_factories: dict[type[object], Callable[[], object]] = {}
        self._singletons: dict[type[object], object] = {}

    def register_sync_factory(self, type_: type[T], factory: Callable[[], T]) -> None:
        self._check_not_registered(type_)
        self._sync_factories[type_] = factory

    def register_async_factory(self, type_: type[T], factory: Callable[[], Awaitable[T]]) -> None:
        self._check_not_registered(type_)
        self._async_factories[type_] = factory

    def register_singleton(self, type_: type[T], singleton: T) -> None:
        self._check_not_registered(type_)
        self._singletons[type_] = singleton

    async def resolve(self, type_: type[T]) -> T:
        if type_ in self._async_factories:
            factory = cast(
                Callable[[], Awaitable[T]], 
                self._async_factories[type_]
            )
            return await factory()
        
        if type_ in self._sync_factories:
            factory = cast(
                Callable[[], T], 
                self._sync_factories[type_]
            )
            return factory()
        
        if type_ in self._singletons:
            return self._singletons[type_]
        
        
        raise KeyError(
            f"Dependency resolution error: '{type_.__name__}' is not registered in this "
            f"container. Ensure it is added using `register_singleton()` or "
            f"`register_factory()` before resolving."
        )
    
    def _check_not_registered(self, type_: type[object]) -> None:
        error_template = (
            "Type already has been register to the container as an {name}: {type_name}"
        )

        if self._async_factories.get(type_):
            raise ValueError(
                error_template.format(name="Async Factory", type_name=type_.__name__)
            )

        if self._sync_factories.get(type_):
            raise ValueError(
                error_template.format(name="sync Factory", type_name=type_.__name__)
            )
        
        if self._singletons.get(type_):
            raise ValueError(
                error_template.format(name="Singleton", type_name=type_.__name__)
            )
        