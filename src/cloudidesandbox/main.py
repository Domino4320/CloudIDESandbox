from fastapi import FastAPI
from src.cloudidesandbox.api_v1.routes.terminal import router as terminal_router
from src.cloudidesandbox.api_v1.routes.workspaces import router as workspaces_router
from src.cloudidesandbox.pages import router as pages_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="CloudIDESandbox")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(terminal_router, prefix="/api/v1", tags=["API v1 terminal"])
app.include_router(workspaces_router, prefix="/api/v1", tags=["API v1 workspaces"])
app.include_router(pages_router, tags=["HTML Pages"])

if __name__ == "__main__":
    uvicorn.run("src.cloudidesandbox.main:app", reload=True)
