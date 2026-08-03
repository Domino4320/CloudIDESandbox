from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/terminal")
async def show_terminal():
    return FileResponse("src/cloudidesandbox/static/html/terminal.html")
