from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.cloudidesandbox.api_v1.exceptions.containers import ContainerNotFoundError


async def container_not_found_handler(request: Request, exc: ContainerNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "details": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ContainerNotFoundError, container_not_found_handler)
