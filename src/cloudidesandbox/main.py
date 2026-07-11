from fastapi import FastAPI
from src.cloudidesandbox.api_v1.routes.websocket import router as ws_router
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
app.include_router(ws_router)

if __name__ == "__main__":
    uvicorn.run("src.cloudidesandbox.main:app", reload=True)
