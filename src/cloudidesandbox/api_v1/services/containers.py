import docker
from docker.errors import NotFound
from pathlib import Path


class ContainerService:

    def __init__(
        self,
        user_id: str,
        project_id: str,
        container_image: str = "python:3.12-slim",
        mem_limit: str = "512m",
        nano_cpus=1000000000,
    ):
        self.docker_client = docker.from_env()
        self.user_id = user_id
        self.project_id = project_id
        self.container_image = container_image
        self.mem_limit = mem_limit
        self.nano_cpus = nano_cpus

    @property
    def workspace_dir(self) -> str:
        parent_dir = None
        for parent in Path(__file__).parents:
            if parent.name == "cloudidesandbox":
                parent_dir = parent
        return parent_dir / "workspaces" / self.user_id

    def start_container(self) -> str:
        container_name = f"u{self.user_id}p{self.project_id}"
        try:
            container = self.docker_client.containers.get(container_name)
            if container.status != "running":
                container.run()
            return container_name
        except NotFound:
            container = self.docker_client.containers.run(
                image=self.container_image,
                name=container_name,
                detach=True,
                tty=True,
                stdin_open=True,
                working_dir="/workspace",
                mem_limit=self.mem_limit,
                nano_cpus=self.nano_cpus,
                volumes={self.workspace_dir: {"bind": "/workspace", "mode": "rw"}},
            )
            return container.name
