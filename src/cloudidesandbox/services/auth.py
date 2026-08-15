from src.cloudidesandbox.schemas.user import UserSchema
from src.cloudidesandbox.core.security import (
    hash_password,
    DUMMY_HASH,
    verify_password,
    create_jwt,
)
from src.cloudidesandbox.repositories.user import UserRepository
from src.cloudidesandbox.exceptions.auth import BusyLoginError, InvalidCredentialsError
import asyncio
from datetime import timedelta


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

    async def authenticate(self, user_data: UserSchema) -> dict:
        if user := await self.user_rep.get_user_by_login(user_data.login):
            if await asyncio.to_thread(
                verify_password, user_data.password, user.password
            ):
                access_token = create_jwt(user.id, timedelta(minutes=30), "access")
                refresh_token = create_jwt(user.id, timedelta(days=14), "refresh")
                return {"refresh token": refresh_token, "access token": access_token}
            else:
                raise InvalidCredentialsError()
        await asyncio.to_thread(verify_password, user_data.password, DUMMY_HASH)
        raise InvalidCredentialsError()
