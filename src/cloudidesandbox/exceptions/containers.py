from src.cloudidesandbox.exceptions.base import AppException


class ContainerNotFoundError(AppException):

    status_code = 404
    code = "CONTAINER_NOT_FOUND"

    def __init__(self, container_id):
        super().__init__(detail=f"Container {container_id} was not found")
