from src.cloudidesandbox.services.auth import AuthService
from src.cloudidesandbox.dependencies.user import UserRepositoryDep
from src.cloudidesandbox.dependencies.redis import RedisRepositoryDep
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.cloudidesandbox.core.security import get_payload


def get_auth_service(
    user_repository: UserRepositoryDep, redis_repository: RedisRepositoryDep
):
    auth_service = AuthService(
        user_repository=user_repository, redis_repository=redis_repository
    )
    return auth_service


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


security = HTTPBearer()


def get_current_user(
    user_data: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = user_data.credentials
    payload = get_payload(jwt_token=token)
    return payload["sub"]


UserDep = Annotated[str, Depends(get_current_user)]
