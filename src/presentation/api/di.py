from typing import Annotated
from fastapi import Depends

from src.framework import container


async def get_container() -> container.Container:
    raise ValueError(
        "This dependency function should be rewritten."
    )

type Container = Annotated[
    container.Container, Depends(get_container)
]
