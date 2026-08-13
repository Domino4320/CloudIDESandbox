from src.cloudidesandbox.schemas.user import UserSchema
from src.cloudidesandbox.core.security import hash_password
from src.cloudidesandbox.repositories.user import UserRepository
from src.cloudidesandbox.exceptions.auth import BusyLoginError
import asyncio


class AuthService:

    def __init__(self, user_rep: UserRepository):
        self.user_rep = user_rep

    async def register(self, user_data: UserSchema) -> None:
        if not await self.user_rep.get_user_by_login(user_data.login):
            hashed_password = await asyncio.to_thread(hash_password, user_data.password)
            await self.user_rep.create_user(
                hashed_password=hashed_password, other_user_data=user_data
            )
        else:
            raise BusyLoginError()
