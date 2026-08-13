from fastapi import APIRouter
from src.cloudidesandbox.api.v1.terminal import router as terminal_router
from src.cloudidesandbox.api.v1.workspaces import router as workspaces_router
from src.cloudidesandbox.api.v1.containers import router as containers_router
from src.cloudidesandbox.api.v1.auth import router as auth_router

router = APIRouter(prefix="/v1")

router.include_router(terminal_router, tags=["API v1 Terminal"])
router.include_router(workspaces_router, tags=["API v1 Workspaces"])
router.include_router(containers_router, tags=["API v1 Containers"])
router.include_router(auth_router, tags=["API v1 Auth operations"])
