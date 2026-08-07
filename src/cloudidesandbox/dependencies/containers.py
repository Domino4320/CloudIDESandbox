from src.cloudidesandbox.services.containers import ContainerService
from fastapi import Depends
from functools import lru_cache
import docker
from typing import Annotated


def _get_docker_client():
    return docker.from_env()


@lru_cache
def get_container_service(
    docker_client: Annotated[docker.DockerClient, Depends(_get_docker_client)],
):
    return ContainerService(docker_client)


ContainerServiceDep = Annotated[ContainerService, Depends(get_container_service)]
