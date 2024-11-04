from collections.abc import AsyncIterator, Awaitable, Callable
from uuid import UUID

from hundred import Aggregate


class InMemoryRepository[A: Aggregate]:
    __slots__ = ("__data", "__post_processor")

    __data: dict[UUID, A]
    __post_processor: Callable[[A], Awaitable[A]] | None

    def __init__(
        self,
        post_processor: Callable[[A], Awaitable[A]] | None = None,
    ) -> None:
        self.__data = {}
        self.__post_processor = post_processor

    async def all(self) -> AsyncIterator[A]:
        processor = self.__post_processor or self.__default_post_processor

        for aggregate in self.__data.values():
            copy = aggregate.model_copy(deep=True)
            yield await processor(copy)

    def clear(self) -> None:
        self.__data.clear()

    async def delete(self, uuid: UUID, /) -> None:
        self.__data.pop(uuid, None)

    async def delete_by(self, predicate: Callable[[A], bool]) -> None:
        aggregates = [aggregate async for aggregate in self.filter(predicate)]

        for aggregate in aggregates:
            await self.delete(aggregate.id)

    async def filter(self, predicate: Callable[[A], bool]) -> AsyncIterator[A]:
        async for aggregate in self.all():
            if predicate(aggregate):
                yield aggregate

    async def get(self, uuid: UUID, /) -> A | None:
        return await self.get_first(lambda aggregate: aggregate.id == uuid)

    async def get_first(self, predicate: Callable[[A], bool]) -> A | None:
        aggregates = self.filter(predicate)
        return await anext(aggregates, None)

    async def save(self, aggregate: A, /) -> None:
        self.__data[aggregate.id] = aggregate.model_copy(deep=True)

    @staticmethod
    async def __default_post_processor(aggregate: A) -> A:
        return aggregate
