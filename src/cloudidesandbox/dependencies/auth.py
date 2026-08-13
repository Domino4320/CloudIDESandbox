from src.cloudidesandbox.services.auth import AuthService
from src.cloudidesandbox.dependencies.user import UserRepositoryDep
from typing import Annotated
from fastapi import Depends


def get_auth_service(user_repository: UserRepositoryDep):
    auth_service = AuthService(user_rep=user_repository)
    return auth_service


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
