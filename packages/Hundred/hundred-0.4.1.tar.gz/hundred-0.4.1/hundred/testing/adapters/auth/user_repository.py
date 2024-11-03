from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.domain import User
from hundred.ctx.auth.ports import UserRepository
from hundred.testing.adapter.repository import InMemoryRepository


@test_singleton(on=UserRepository, inject=False, mode="fallback")
class InMemoryUserRepository(InMemoryRepository[User], UserRepository):
    async def get_by_identifier(self, identifier: str) -> User | None:
        uuid = UUID(identifier)
        return await self.get(uuid)
