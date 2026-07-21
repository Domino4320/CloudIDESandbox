from fastapi import APIRouter
import docker

router = APIRouter(prefix="/containers")


@router.post("/start/{container_id}")
async def start_container(container_id: str = "mock_id"): ...


@router.post("/stop/{container_id}")
async def stop_container(container_id: str = "mock_id"): ...
