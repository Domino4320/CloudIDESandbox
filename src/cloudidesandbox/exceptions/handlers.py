from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.cloudidesandbox.exceptions.base import AppException


async def app_handlers(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "details": exc.detail, "code": exc.code},
    )
