from sqlalchemy.ext.asyncio import AsyncSession
from src.cloudidesandbox.schemas.user import UserSchema
from src.cloudidesandbox.db.models import User
from sqlalchemy import select


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        hashed_password: str,
        other_user_data: UserSchema,
    ) -> User:
        user_data = {
            "password": hashed_password,
            **other_user_data.model_dump(exclude={"password"}),
        }
        user = User(**user_data)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
