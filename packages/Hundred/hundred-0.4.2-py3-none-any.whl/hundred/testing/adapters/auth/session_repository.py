from typing import AsyncIterator
from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.domain import Session
from hundred.ctx.auth.ports import SessionRepository, UserRepository
from hundred.testing.adapter.repository import InMemoryRepository


@test_singleton(on=SessionRepository, mode="fallback")
class InMemorySessionRepository(InMemoryRepository[Session], SessionRepository):
    __slots__ = ("__user_repository",)

    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__()
        self.__user_repository = user_repository

    async def get(self, application_id: UUID) -> Session | None:
        sessions = self.filter_(
            lambda session: session.application_id == application_id,
        )
        return await anext(sessions, None)

    async def get_all_(self) -> AsyncIterator[Session]:
        async for session in super().get_all_():
            user = await self.__user_repository.get(session.user.id)
            yield session.model_copy(update={"user": user})

    async def delete(self, application_id: UUID) -> None:
        session = await self.get(application_id)

        if session is None:
            return

        await super().delete(session.id)

    async def delete_by_user_id(
        self,
        user_id: UUID,
        current_application_id: UUID | None = None,
    ) -> None:
        sessions = [
            session async for session in self.filter_(lambda s: s.user.id == user_id)
        ]

        for session in sessions:
            application_id = session.application_id

            if application_id == current_application_id:
                continue

            await self.delete(application_id)
