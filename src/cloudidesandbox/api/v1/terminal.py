from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from src.cloudidesandbox.core.logging import AppLogger
from src.cloudidesandbox.services.workspaces import initialize_user_workspace
from src.cloudidesandbox.dependencies.terminal import TerminalServiceDep
import asyncio

logger = AppLogger(__name__, to_file=True).get_logger()
router = APIRouter()


@router.websocket("/ws/terminal/{container_id}")
async def terminal_session(
    websocket: WebSocket, terminal_service: TerminalServiceDep
) -> None:
    await websocket.accept()
    await asyncio.to_thread(initialize_user_workspace())
    read_task: asyncio.Task | None = None
    try:
        await terminal_service.start()
        read_task = asyncio.create_task(terminal_service.read_loop())
        while True:
            user_input = await websocket.receive_text()
            await terminal_service.write_input(user_input)
    except WebSocketDisconnect:
        pass
    finally:
        if read_task and not read_task.done():
            read_task.cancel()
        await terminal_service.close()
        try:
            await websocket.close()
        except RuntimeError:
            pass
