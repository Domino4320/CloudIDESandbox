from fastapi import FastAPI, APIRouter
from src.cloudidesandbox.exceptions.handlers import register_exception_handlers
from src.cloudidesandbox.pages import router as pages_router
from src.cloudidesandbox.api.v1.router import router as api_v1_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run("src.cloudidesandbox.main:app", reload=True)
