from typing import ClassVar
from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.ports import TwoFactorAuthenticator


@test_singleton(on=TwoFactorAuthenticator, inject=False, mode="fallback")
class FakeTwoFactorAuthenticator(TwoFactorAuthenticator):
    check_code: ClassVar[str] = "123456"

    async def send_code(self, user_id: UUID) -> str | None:
        return self.check_code
