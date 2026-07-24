from __future__ import annotations
from fastapi import APIRouter
from src.cloudidesandbox.api_v1.dependencies.containers import ContainerServiceDep

router = APIRouter(prefix="/containers")


@router
@router.post("/create")
async def create_container(container_service: ContainerServiceDep): ...


@router.post("/start/{container_id}")
async def start_container(
    container_id: str, container_service: ContainerServiceDep
): ...


@router.post("/stop/{container_id}")
async def stop_container(container_id: str, container_service: ContainerServiceDep): ...
