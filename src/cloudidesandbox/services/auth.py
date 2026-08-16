from src.cloudidesandbox.schemas.user import UserSchema
from src.cloudidesandbox.core.security import (
    hash_password,
    DUMMY_HASH,
    verify_password,
    create_jwt,
)
from src.cloudidesandbox.repositories.user import UserRepository
from src.cloudidesandbox.exceptions.auth import BusyLoginError, InvalidCredentialsError
from src.cloudidesandbox.repositories.redis import RedisRepository
import asyncio
from datetime import timedelta


class AuthService:

    def __init__(
        self, user_repository: UserRepository, redis_repository: RedisRepository
    ):
        self.user_rep = user_repository
        self.redis_repository = redis_repository

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
                return await self.create_tokens(str(user.id))
            else:
                raise InvalidCredentialsError()
        await asyncio.to_thread(verify_password, user_data.password, DUMMY_HASH)
        raise InvalidCredentialsError()

    async def create_tokens(self, user_id: str) -> str:
        access_token, _ = create_jwt(
            subject=user_id, expires_delta=timedelta(minutes=30), token_type="access"
        )
        expiration = timedelta(days=14)
        refresh_token, jti = create_jwt(
            subject=user_id, expires_delta=expiration, token_type="refresh"
        )
        await self.redis_repository.set_with_expiration(
            f"refresh:user:{user_id}", jti, expiration
        )
        return {"refresh token": refresh_token, "access token": access_token}
