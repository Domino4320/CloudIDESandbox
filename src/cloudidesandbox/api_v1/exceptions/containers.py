class ContainerError(Exception):
    pass


class ContainerNotFoundError(ContainerError):
    def __init__(self, container_id):
        super().__init__(f"Container {container_id} was not found")
