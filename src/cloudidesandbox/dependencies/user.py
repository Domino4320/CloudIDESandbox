from src.cloudidesandbox.repositories.user import UserRepository
from src.cloudidesandbox.dependencies.database import SessionDep
from typing import Annotated
from fastapi import Depends


def get_user_repository(session: SessionDep):
    return UserRepository(session=session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
