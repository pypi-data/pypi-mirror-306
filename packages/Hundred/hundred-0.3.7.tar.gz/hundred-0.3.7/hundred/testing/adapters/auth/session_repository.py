from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.domain import Session
from hundred.ctx.auth.ports import SessionRepository
from hundred.testing.adapter.repository import InMemoryRepository


@test_singleton(on=SessionRepository, inject=False, mode="fallback")
class InMemorySessionRepository(InMemoryRepository[Session], SessionRepository):
    async def get(self, application_id: UUID) -> Session | None:
        sessions = self.filter_(
            lambda session: session.application_id == application_id,
        )
        return next(sessions, None)

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
        sessions = tuple(self.filter_(lambda s: s.user.id == user_id))

        for session in sessions:
            application_id = session.application_id

            if application_id == current_application_id:
                continue

            await self.delete(application_id)
