import docker
from docker.errors import NotFound
from pathlib import Path
import asyncio
import uuid
from src.cloudidesandbox.api_v1.exceptions.containers import ContainerNotFoundError


class ContainerService:

    def __init__(self, docker_client: docker.DockerClient):
        self.docker_client = docker_client

    @property
    def workspace_dir(self) -> Path:
        parent_dir = None
        for parent in Path(__file__).parents:
            if parent.name == "cloudidesandbox":
                parent_dir = parent
        return parent_dir / "workspaces" / "mock_user"

    async def create_container(self, container_image: str) -> str:
        container_name = str(uuid.uuid4())
        container = await asyncio.to_thread(
            lambda: self.docker_client.containers.create(
                image=container_image,
                detach=True,
                name=container_name,
                tty=True,
                stdin_open=True,
                working_dir="/workspace",
                mem_limit="512m",
                nano_cpus=1_000_000_000,
                volumes={self.workspace_dir: {"bind": "/workspace", "mode": "rw"}},
            )
        )
        return container.name

    async def start_container(self, container_name: str) -> None:
        def _start_container():
            container = self.docker_client.containers.get(container_name)
            if container.status != "running":
                container.start()

        try:
            await asyncio.to_thread(_start_container)
        except NotFound:
            raise ContainerNotFoundError(container_name)

    async def stop_container(self, container_name: str) -> None:
        def _stop_container():
            container = self.docker_client.containers.get(container_name)
            if container.status == "running":
                container.stop()

        try:
            await asyncio.to_thread(_stop_container)
        except NotFound:
            raise ContainerNotFoundError(container_name)

    async def remove_container(self, container_name: str) -> None:
        def _remove_container():
            container = self.docker_client.containers.get(container_name)
            container.remove(force=True, v=True)

        try:
            await asyncio.to_thread(_remove_container)
        except NotFound:
            raise ContainerNotFoundError(container_name)
