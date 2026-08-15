from fastapi import APIRouter, status
from src.cloudidesandbox.dependencies.auth import AuthServiceDep
from src.cloudidesandbox.schemas.user import UserSchema

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(auth_service: AuthServiceDep, user_data: UserSchema):
    await auth_service.register(user_data)
    return {"status": "ok", "detail": "registration is successfull"}


@router.post("/auth")
async def authorization(auth_service: AuthServiceDep): ...


@router.post("/token/refresh")
async def refresh_token(auth_service: AuthServiceDep): ...
