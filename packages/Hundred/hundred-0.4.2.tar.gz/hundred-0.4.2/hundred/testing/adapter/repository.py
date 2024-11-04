from abc import ABC
from collections.abc import AsyncIterator, Callable
from uuid import UUID

from hundred import Aggregate


class InMemoryRepository[A: Aggregate](ABC):
    __slots__ = ("__data",)

    def __init__(self) -> None:
        self.__data = dict[UUID, A]()

    async def get(self, uuid: UUID, /) -> A | None:
        aggregates = self.filter_(lambda aggregate: aggregate.id == uuid)
        return await anext(aggregates, None)

    async def get_all_(self) -> AsyncIterator[A]:
        for aggregate in (
            aggregate.model_copy(deep=True) for aggregate in self.__data.values()
        ):
            yield aggregate

    async def save(self, aggregate: A, /) -> None:
        self.__data[aggregate.id] = aggregate.model_copy(deep=True)

    async def delete(self, uuid: UUID, /) -> None:
        self.__data.pop(uuid, None)

    async def filter_(self, predicate: Callable[[A], bool]) -> AsyncIterator[A]:
        async for aggregate in self.get_all_():
            if predicate(aggregate):
                yield aggregate

    def clear_(self) -> None:
        self.__data.clear()
