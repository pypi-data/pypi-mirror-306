from abc import ABC
from collections.abc import Callable, Collection, Iterator
from uuid import UUID

from hundred import Aggregate


class InMemoryRepository[A: Aggregate](ABC):
    __slots__ = ("__data",)

    def __init__(self) -> None:
        self.__data = dict[UUID, A]()

    @property
    def values_(self) -> Collection[A]:
        return self.__data.values()

    async def get(self, uuid: UUID, /) -> A | None:
        return self.__data.get(uuid)

    async def save(self, aggregate: A, /) -> None:
        self.__data[aggregate.id] = aggregate

    async def delete(self, uuid: UUID, /) -> None:
        self.__data.pop(uuid, None)

    def filter_(self, predicate: Callable[[A], bool]) -> Iterator[A]:
        return filter(predicate, self.values_)

    def clear_(self) -> None:
        self.__data.clear()
