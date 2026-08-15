from fastapi import FastAPI, APIRouter
from src.cloudidesandbox.pages import router as pages_router
from src.cloudidesandbox.api.v1.router import router as api_v1_router
from fastapi.middleware.cors import CORSMiddleware
from src.cloudidesandbox.exceptions.handlers import app_handlers
from src.cloudidesandbox.exceptions.base import AppException
from src.cloudidesandbox.core.redis import init_redis, close_redis
from src.cloudidesandbox.core.database import engine
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan():
    await init_redis()
    yield
    await close_redis()
    await engine.dispose()


app = FastAPI(title="CloudIDESandbox")

api_router = APIRouter(prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages_router, tags=["HTML Pages"])
api_router.include_router(api_v1_router)
app.include_router(api_router)
app.add_exception_handler(AppException, app_handlers)


if __name__ == "__main__":
    uvicorn.run("src.cloudidesandbox.main:app", reload=True)
