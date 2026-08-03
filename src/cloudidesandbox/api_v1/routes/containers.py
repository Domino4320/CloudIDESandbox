from __future__ import annotations
from fastapi import APIRouter, status
from src.cloudidesandbox.api_v1.dependencies.containers import ContainerServiceDep

router = APIRouter(prefix="/containers")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_container(
    container_service: ContainerServiceDep, container_image: str = "python:3.12-slim"
):
    container_id = await container_service.create_container(container_image)
    return {
        "status": "ok",
        "details": "container created successfully",
        "container_id": container_id,
    }


@router.post("/start/{container_id}")
async def start_container(container_id: str, container_service: ContainerServiceDep):
    await container_service.start_container(container_id)
    return {
        "status": "ok",
        "details": "container started successfully",
        "container_id": container_id,
    }


@router.post("/stop/{container_id}")
async def stop_container(container_id: str, container_service: ContainerServiceDep):
    await container_service.stop_container(container_id)
    return {
        "status": "ok",
        "details": "container stopped successfully",
        "container_id": container_id,
    }


@router.post("/remove/{container_id}")
async def remove_container(container_id: str, container_service: ContainerServiceDep):
    await container_service.remove_container(container_id)
    return {
        "status": "ok",
        "details": "container removed successfully",
        "container_id": container_id,
    }
